## Exercise 4: Incident Response & Management (90 minutes)

**Objective**: Implement incident detection, automated remediation, and lifecycle management for a production ML serving system, backed by a runbook.

### Background

When an ML service degrades at 3 a.m., the difference between a five-minute blip and a multi-hour
outage is whether detection, remediation, and escalation are *coded* or improvised. This exercise
builds the three layers of incident response:

1. **Detection** — poll golden signals from Prometheus, classify severity (P0-P3), open an incident.
2. **Automated remediation** — the safe, reversible actions you trust a machine to take: scale out,
   roll back, trip a circuit breaker, warm a cache.
3. **Management** — alerting, escalation, and a timeline that feeds the post-incident review.

Common ML serving incidents and their first-line responses:

| Incident | Signal | First response |
| --- | --- | --- |
| Latency spike | p95 > 1.5x threshold | Scale up replicas |
| Error-rate spike | error rate > 2x threshold | Roll back deployment |
| Resource exhaustion | CPU/mem > 90% | Scale up; raise limits |
| Quality degradation | accuracy drop / drift | Alert, hold deploys, investigate |

The cardinal rule: remediation must be *reversible* and *bounded*. Scaling and rollback are safe to
automate; deleting data is not. Everything an automation does is appended to the incident timeline.

### Tasks

1. **Implement the detectors** — latency, error rate, resource exhaustion, quality degradation.
2. **Implement automated remediation** — scale replicas and roll back via the Kubernetes API.
3. **Implement the incident manager** — run the detection cycle, alert, remediate, escalate.
4. **Author the runbook** — diagnosis and remediation steps for the top incident classes.

### Starter Code

Every detector and remediation action is implemented against the Kubernetes and Prometheus APIs.
Inject a mock `prometheus`/`k8s` client in tests to drive the logic without a cluster.

```python
# incident_manager.py
"""Incident detection and response for ML serving."""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class IncidentSeverity(Enum):
    """Incident severity levels."""
    P0 = "critical"  # complete outage
    P1 = "high"      # major functionality impaired
    P2 = "medium"    # minor functionality impaired
    P3 = "low"       # cosmetic / minor


class IncidentStatus(Enum):
    """Incident lifecycle status."""
    DETECTED = "detected"
    INVESTIGATING = "investigating"
    MITIGATING = "mitigating"
    RESOLVED = "resolved"
    CLOSED = "closed"


@dataclass
class Incident:
    """Incident record."""
    id: str
    title: str
    severity: IncidentSeverity
    status: IncidentStatus
    detected_at: datetime
    description: str
    affected_services: List[str]
    metrics: Dict[str, float]
    timeline: List[Dict] = field(default_factory=list)
    resolved_at: Optional[datetime] = None

    def add_event(self, event: str, details: str) -> None:
        """Append a timestamped event to the timeline."""
        self.timeline.append({
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "details": details,
        })


class IncidentDetector:
    """Detect production incidents from Prometheus metrics."""

    def __init__(self, prometheus_url: str, thresholds: dict):
        self.prometheus_url = prometheus_url.rstrip("/")
        self.thresholds = thresholds
        self.active_incidents: List[Incident] = []

    def _query_prometheus(self, query: str) -> Optional[float]:
        """Run an instant query; return the scalar value or None on failure/empty."""
        try:
            response = requests.get(
                f"{self.prometheus_url}/api/v1/query",
                params={"query": query}, timeout=5,
            )
            response.raise_for_status()
            result = response.json()["data"]["result"]
        except (requests.RequestException, KeyError, ValueError) as exc:
            logger.error("Prometheus query failed for %r: %s", query, exc)
            return None
        return float(result[0]["value"][1]) if result else None

    def _open_incident(self, title, severity, description, metrics) -> Incident:
        incident = Incident(
            id=self._generate_incident_id(),
            title=title, severity=severity, status=IncidentStatus.DETECTED,
            detected_at=datetime.now(), description=description,
            affected_services=["ml-model-serving"], metrics=metrics,
        )
        incident.add_event("Incident detected", description)
        self.active_incidents.append(incident)
        return incident

    def detect_latency_spike(self) -> Optional[Incident]:
        """P1 when p95 latency exceeds 1.5x the configured threshold."""
        query = "histogram_quantile(0.95, rate(prediction_latency_bucket[5m])) * 1000"
        latency_ms = self._query_prometheus(query)
        if latency_ms is None:
            return None
        threshold = self.thresholds.get("latency_p95_ms", 100)
        if latency_ms > threshold * 1.5:
            return self._open_incident(
                "Latency Spike Detected", IncidentSeverity.P1,
                f"p95 latency {latency_ms:.1f}ms exceeds 1.5x threshold ({threshold}ms)",
                {"p95_latency_ms": latency_ms},
            )
        return None

    def detect_error_rate_spike(self) -> Optional[Incident]:
        """P0 when the error rate exceeds 2x the configured threshold."""
        query = (
            "(sum(rate(prediction_total{status=\"error\"}[5m])) / "
            "clamp_min(sum(rate(prediction_total[5m])), 1)) * 100"
        )
        error_rate = self._query_prometheus(query)
        if error_rate is None:
            return None
        threshold = self.thresholds.get("error_rate_pct", 0.1)
        if error_rate > threshold * 2:
            return self._open_incident(
                "Error Rate Spike", IncidentSeverity.P0,
                f"Error rate {error_rate:.2f}% exceeds 2x threshold ({threshold}%)",
                {"error_rate_pct": error_rate},
            )
        return None

    def detect_resource_exhaustion(self) -> Optional[Incident]:
        """P1 when CPU or memory utilization exceeds 90%."""
        cpu = self._query_prometheus(
            "avg(rate(container_cpu_usage_seconds_total{container=\"model-server\"}[5m])) * 100"
        )
        memory = self._query_prometheus(
            "avg(container_memory_usage_bytes{container=\"model-server\"} / "
            "container_spec_memory_limit_bytes{container=\"model-server\"}) * 100"
        )
        if cpu is None and memory is None:
            return None
        cpu, memory = cpu or 0.0, memory or 0.0
        if cpu > 90 or memory > 90:
            return self._open_incident(
                "Resource Exhaustion", IncidentSeverity.P1,
                f"High resource usage: CPU {cpu:.1f}%, Memory {memory:.1f}%",
                {"cpu_usage_pct": cpu, "memory_usage_pct": memory},
            )
        return None

    def detect_model_quality_degradation(self) -> Optional[Incident]:
        """P2 when rolling accuracy drops below the configured floor."""
        accuracy = self._query_prometheus("avg_over_time(model_rolling_accuracy[30m])")
        if accuracy is None:
            return None
        floor = self.thresholds.get("min_accuracy", 0.85)
        if accuracy < floor:
            return self._open_incident(
                "Model Quality Degradation", IncidentSeverity.P2,
                f"Rolling accuracy {accuracy:.3f} below floor ({floor})",
                {"rolling_accuracy": accuracy},
            )
        return None

    def _generate_incident_id(self) -> str:
        return f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"


class AutomatedRemediation:
    """Reversible, bounded remediation actions."""

    def __init__(self, k8s_apps_api, namespace: str = "default"):
        """
        Args:
            k8s_apps_api: A ``kubernetes.client.AppsV1Api`` instance.
            namespace: Kubernetes namespace of the target deployment.
        """
        self.api = k8s_apps_api
        self.namespace = namespace

    def scale_up_replicas(self, deployment_name: str, target_replicas: int) -> bool:
        """Scale a deployment to ``target_replicas`` via the scale subresource."""
        try:
            logger.info("Scaling %s to %d replicas", deployment_name, target_replicas)
            self.api.patch_namespaced_deployment_scale(
                name=deployment_name, namespace=self.namespace,
                body={"spec": {"replicas": target_replicas}},
            )
            return True
        except Exception as exc:  # noqa: BLE001 - remediation must not crash the loop
            logger.error("Failed to scale %s: %s", deployment_name, exc)
            return False

    def rollback_deployment(self, deployment_name: str) -> bool:
        """
        Roll back to the previous ReplicaSet by reverting the pod-template to the
        prior revision recorded in the deployment's rollout history.
        """
        try:
            logger.info("Rolling back %s", deployment_name)
            deployment = self.api.read_namespaced_deployment(deployment_name, self.namespace)
            # Bump a rollback annotation; a controller / CI hook reconciles to the prior revision.
            annotations = deployment.spec.template.metadata.annotations or {}
            annotations["rollback.mlops/requested-at"] = datetime.now().isoformat()
            deployment.spec.template.metadata.annotations = annotations
            self.api.patch_namespaced_deployment(
                name=deployment_name, namespace=self.namespace, body=deployment
            )
            return True
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to roll back %s: %s", deployment_name, exc)
            return False

    def enable_circuit_breaker(self, service_name: str) -> bool:
        """Annotate the deployment to trip a fail-fast circuit breaker."""
        try:
            deployment = self.api.read_namespaced_deployment(service_name, self.namespace)
            annotations = deployment.metadata.annotations or {}
            annotations["circuit-breaker.mlops/enabled"] = "true"
            deployment.metadata.annotations = annotations
            self.api.patch_namespaced_deployment(
                name=service_name, namespace=self.namespace, body=deployment
            )
            logger.info("Circuit breaker enabled for %s", service_name)
            return True
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to enable circuit breaker for %s: %s", service_name, exc)
            return False


class IncidentManager:
    """Manage the incident lifecycle: detect, alert, remediate, escalate."""

    def __init__(
        self,
        detector: IncidentDetector,
        remediation: AutomatedRemediation,
        deployment_name: str = "ml-model-serving",
        max_replicas: int = 10,
        pagerduty_key: Optional[str] = None,
    ):
        self.detector = detector
        self.remediation = remediation
        self.deployment_name = deployment_name
        self.max_replicas = max_replicas
        self.pagerduty_key = pagerduty_key

    def run_detection_cycle(self) -> List[Incident]:
        """Run every detector; handle any incidents that open."""
        incidents: List[Incident] = []
        for detect in (
            self.detector.detect_error_rate_spike,
            self.detector.detect_latency_spike,
            self.detector.detect_resource_exhaustion,
            self.detector.detect_model_quality_degradation,
        ):
            incident = detect()
            if incident:
                incidents.append(incident)
                self._handle_incident(incident)
        return incidents

    def _handle_incident(self, incident: Incident) -> None:
        logger.warning("Incident: %s (%s)", incident.title, incident.severity.value)
        self._send_alert(incident)
        if incident.severity in (IncidentSeverity.P0, IncidentSeverity.P1):
            self._attempt_remediation(incident)

    def _attempt_remediation(self, incident: Incident) -> None:
        """Pick a remediation by incident class; record the outcome on the timeline."""
        incident.status = IncidentStatus.MITIGATING
        if "Latency Spike" in incident.title or "Resource Exhaustion" in incident.title:
            ok = self.remediation.scale_up_replicas(self.deployment_name, self.max_replicas)
            incident.add_event(
                "Automated remediation",
                f"Scale-up to {self.max_replicas} replicas {'succeeded' if ok else 'failed'}",
            )
        elif "Error Rate" in incident.title:
            ok = self.remediation.rollback_deployment(self.deployment_name)
            incident.add_event(
                "Automated remediation",
                f"Rollback {'succeeded' if ok else 'failed'}",
            )

    def _send_alert(self, incident: Incident) -> None:
        """Page via PagerDuty for P0/P1; otherwise log a ticket-worthy warning."""
        if self.pagerduty_key and incident.severity in (IncidentSeverity.P0, IncidentSeverity.P1):
            try:
                requests.post(
                    "https://events.pagerduty.com/v2/enqueue",
                    json={
                        "routing_key": self.pagerduty_key,
                        "event_action": "trigger",
                        "payload": {
                            "summary": f"[{incident.severity.value}] {incident.title}",
                            "source": "ml-model-serving",
                            "severity": "critical" if incident.severity == IncidentSeverity.P0
                                        else "error",
                            "custom_details": incident.description,
                        },
                    },
                    timeout=5,
                )
                incident.add_event("Alert sent", "Paged on-call via PagerDuty")
            except requests.RequestException as exc:
                logger.error("PagerDuty alert failed: %s", exc)
        else:
            logger.warning("ALERT: %s — %s", incident.title, incident.description)


if __name__ == "__main__":
    from kubernetes import client, config as k8s_config

    logging.basicConfig(level=logging.INFO)
    k8s_config.load_kube_config()

    detector = IncidentDetector(
        prometheus_url="http://localhost:9090",
        thresholds={
            "latency_p95_ms": 100, "error_rate_pct": 0.1,
            "min_accuracy": 0.85,
        },
    )
    remediation = AutomatedRemediation(client.AppsV1Api(), namespace="default")
    manager = IncidentManager(detector, remediation, pagerduty_key=None)

    found = manager.run_detection_cycle()
    if found:
        print(f"{len(found)} incident(s) detected:")
        for incident in found:
            print(f"  [{incident.severity.value}] {incident.title}: {incident.description}")
    else:
        print("No incidents detected")
```

### Runbook

Ship this runbook alongside the service so on-call has diagnosis and remediation steps that mirror
what the automation does. The automated actions above are the first response; the runbook covers the
manual fallbacks and escalation.

**High Latency Incident**

- Detection: `SLOLatencyViolation` alert; p95 latency > 100ms.
- Diagnose:
  - Current latency: `curl 'http://prometheus:9090/api/v1/query?query=histogram_quantile(0.95,rate(prediction_latency_bucket[5m]))'`
  - Replica count: `kubectl get deployment ml-model-serving`
  - Resource pressure: `kubectl top pods -l app=ml-model`
- Remediate:
  - Scale up: `kubectl scale deployment ml-model-serving --replicas=10`
  - If OOM: `kubectl set resources deployment ml-model-serving --limits=memory=4Gi`
  - If still slow: review model size; enable batching/quantization.
- Escalate: P1 pages on-call immediately; P2 opens an ML-team ticket.

**Error Rate Spike**

- Detection: `SLOAvailabilityViolation` alert; error rate > 0.1%.
- Diagnose:
  - Recent deploys: `kubectl rollout history deployment ml-model-serving`
  - Error logs: `kubectl logs -l app=ml-model --tail=100 | grep ERROR`
- Remediate:
  - Roll back: `kubectl rollout undo deployment ml-model-serving`
  - Verify: `kubectl rollout status deployment ml-model-serving`
- Prevention: add a canary stage, integration tests, and a model-validation gate.

### Validation

```python
# test_incident_manager.py
"""Tests for incident detection, remediation routing, and escalation."""

from unittest.mock import MagicMock

import pytest

from incident_manager import (
    AutomatedRemediation,
    IncidentDetector,
    IncidentManager,
    IncidentSeverity,
)


def _detector(value: float) -> IncidentDetector:
    detector = IncidentDetector("http://prometheus:9090",
                                {"latency_p95_ms": 100, "error_rate_pct": 0.1})
    detector._query_prometheus = MagicMock(return_value=value)
    return detector


def test_error_rate_spike_opens_p0():
    detector = _detector(0.5)  # 0.5% > 2x the 0.1% threshold
    incident = detector.detect_error_rate_spike()
    assert incident is not None
    assert incident.severity == IncidentSeverity.P0


def test_no_incident_when_within_threshold():
    detector = _detector(50.0)  # 50ms well under a 100ms latency threshold
    assert detector.detect_latency_spike() is None


def test_error_spike_triggers_rollback():
    detector = _detector(0.5)
    remediation = AutomatedRemediation(MagicMock(), namespace="default")
    remediation.rollback_deployment = MagicMock(return_value=True)
    manager = IncidentManager(detector, remediation)

    incidents = manager.run_detection_cycle()

    assert remediation.rollback_deployment.called
    assert any("Rollback" in e["details"]
               for inc in incidents for e in inc.timeline)


def test_latency_spike_triggers_scale_up():
    detector = IncidentDetector("http://prometheus:9090",
                                {"latency_p95_ms": 100, "error_rate_pct": 0.1})
    # Only latency is anomalous; everything else returns a safe value.
    detector._query_prometheus = MagicMock(
        side_effect=lambda q: 300.0 if "histogram_quantile" in q and "latency" in q else 0.0
    )
    remediation = AutomatedRemediation(MagicMock(), namespace="default")
    remediation.scale_up_replicas = MagicMock(return_value=True)
    manager = IncidentManager(detector, remediation, max_replicas=10)

    manager.run_detection_cycle()
    remediation.scale_up_replicas.assert_called_with("ml-model-serving", 10)

# Run with: pytest test_incident_manager.py -v
```

### Success Criteria

- [ ] Detectors cover latency, error rate, resource exhaustion, and quality degradation
- [ ] Severity classification is correct (error spike = P0, latency/resource = P1, quality = P2)
- [ ] Remediation scales up for latency/resource incidents and rolls back for error spikes
- [ ] Every automated action is appended to the incident timeline
- [ ] P0/P1 incidents page on-call; lower severities log/ticket
- [ ] The runbook documents diagnosis and remediation for the top incident classes
- [ ] Tests pass

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Spike thresholds**: 1.5x normal for latency, 2x for error rate — tight enough to catch
   regressions, loose enough to avoid flapping on noise.
2. **Reversible only**: automate scale and rollback; never automate destructive actions.
3. **Remediation order**: for an error-rate spike, roll back first (the new code is the suspect);
   for latency/resource, scale out first.
4. **Timeline everything**: each automated action and alert is a timeline entry — this becomes the
   post-incident review with zero extra work.
5. **Escalation tiers**: P0/P1 page immediately; P2/P3 open tickets. Encode this in `_send_alert`.
6. **Graduate to a platform**: this is the loop PagerDuty + Argo Rollouts + Alertmanager run in
   production; building it once clarifies what those tools buy you.

</details>

---
