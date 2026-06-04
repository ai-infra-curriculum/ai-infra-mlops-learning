## Exercise 4: Incident Response & Management (90 minutes)

**Objective**: Implement incident detection, response procedures, and automated remediation for production ML systems.

### Background

Production incidents require:
- Automated detection and alerting
- Structured response procedures (runbooks)
- Quick mitigation (rollback, scaling, circuit breakers)
- Post-incident analysis and prevention

Common ML incidents:
- Model serving latency spikes
- Prediction accuracy degradation
- Resource exhaustion (OOM, CPU throttling)
- Dependency failures (database, feature store)

### Tasks

1. **Create incident detector**:
   - Monitor key metrics
   - Detect anomalies
   - Classify incident severity
   - Trigger alerts

2. **Implement automated remediation**:
   - Auto-scaling on high load
   - Circuit breaker on dependency failure
   - Automatic rollback on error rate spike
   - Graceful degradation

3. **Build runbook system**:
   - Structured troubleshooting guides
   - Automated diagnostic commands
   - Escalation procedures

4. **Post-incident analysis**:
   - Incident timeline reconstruction
   - Root cause analysis
   - Action items and prevention

### Starter Code

```python
# incident_manager.py
"""Incident detection and response for ML serving."""

import time
import logging
from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
import requests

class IncidentSeverity(Enum):
    """Incident severity levels."""
    P0 = "critical"  # Complete outage
    P1 = "high"      # Major functionality impaired
    P2 = "medium"    # Minor functionality impaired
    P3 = "low"       # Cosmetic or minor issue

class IncidentStatus(Enum):
    """Incident status."""
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
    timeline: List[Dict]
    resolved_at: Optional[datetime] = None

class IncidentDetector:
    """Detect production incidents from metrics."""

    def __init__(self, prometheus_url: str, thresholds: dict):
        """
        Initialize incident detector.

        Args:
            prometheus_url: Prometheus server URL
            thresholds: Detection thresholds for metrics
        """
        self.prometheus_url = prometheus_url
        self.thresholds = thresholds
        self.active_incidents: List[Incident] = []

    def detect_latency_spike(self) -> Optional[Incident]:
        """
        Detect latency spike incident.

        TODO: Implement latency spike detection
        - Query P95 latency from Prometheus
        - Compare against threshold
        - Check rate of change
        - Create incident if threshold exceeded
        """

        # TODO: Query current P95 latency
        # query = "histogram_quantile(0.95, rate(prediction_latency_bucket[5m]))"
        # current_latency_ms = self._query_prometheus(query) * 1000

        # TODO: Get threshold
        # threshold_ms = self.thresholds.get('latency_p95_ms', 100)

        # TODO: Check if spike
        # if current_latency_ms > threshold_ms * 1.5:  # 50% above threshold
        #     incident = Incident(
        #         id=self._generate_incident_id(),
        #         title="Latency Spike Detected",
        #         severity=IncidentSeverity.P1,
        #         status=IncidentStatus.DETECTED,
        #         detected_at=datetime.now(),
        #         description=f"P95 latency {current_latency_ms:.1f}ms exceeds threshold {threshold_ms}ms",
        #         affected_services=["ml-model-serving"],
        #         metrics={'p95_latency_ms': current_latency_ms},
        #         timeline=[{
        #             'timestamp': datetime.now(),
        #             'event': 'Incident detected',
        #             'details': 'Latency spike detected by automated monitoring'
        #         }]
        #     )
        #     self.active_incidents.append(incident)
        #     return incident

        # return None

        pass

    def detect_error_rate_spike(self) -> Optional[Incident]:
        """
        Detect error rate spike.

        TODO: Implement error rate spike detection
        - Calculate current error rate
        - Compare against baseline
        - Create incident if significant increase
        """

        # TODO: Query error rate
        # query = """
        #     (sum(rate(prediction_total{status="error"}[5m])) /
        #      sum(rate(prediction_total[5m]))) * 100
        # """
        # current_error_rate = self._query_prometheus(query)

        # TODO: Get threshold
        # threshold_pct = self.thresholds.get('error_rate_pct', 0.1)

        # TODO: Check if spike
        # if current_error_rate > threshold_pct * 2:  # 2x threshold
        #     incident = Incident(
        #         id=self._generate_incident_id(),
        #         title="Error Rate Spike",
        #         severity=IncidentSeverity.P0,
        #         status=IncidentStatus.DETECTED,
        #         detected_at=datetime.now(),
        #         description=f"Error rate {current_error_rate:.2f}% exceeds threshold {threshold_pct}%",
        #         affected_services=["ml-model-serving"],
        #         metrics={'error_rate_pct': current_error_rate},
        #         timeline=[{
        #             'timestamp': datetime.now(),
        #             'event': 'Incident detected',
        #             'details': 'High error rate detected'
        #         }]
        #     )
        #     self.active_incidents.append(incident)
        #     return incident

        pass

    def detect_resource_exhaustion(self) -> Optional[Incident]:
        """
        Detect resource exhaustion (CPU, memory).

        TODO: Implement resource exhaustion detection
        - Query CPU and memory usage
        - Check against limits
        - Detect OOM conditions
        """

        # TODO: Query resource usage
        # cpu_query = "avg(rate(container_cpu_usage_seconds_total[5m])) * 100"
        # memory_query = "avg(container_memory_usage_bytes / container_spec_memory_limit_bytes) * 100"

        # cpu_usage = self._query_prometheus(cpu_query)
        # memory_usage = self._query_prometheus(memory_query)

        # TODO: Check thresholds
        # if cpu_usage > 90 or memory_usage > 90:
        #     incident = Incident(
        #         id=self._generate_incident_id(),
        #         title="Resource Exhaustion",
        #         severity=IncidentSeverity.P1,
        #         status=IncidentStatus.DETECTED,
        #         detected_at=datetime.now(),
        #         description=f"High resource usage: CPU {cpu_usage:.1f}%, Memory {memory_usage:.1f}%",
        #         affected_services=["ml-model-serving"],
        #         metrics={'cpu_usage_pct': cpu_usage, 'memory_usage_pct': memory_usage},
        #         timeline=[...]
        #     )
        #     return incident

        pass

    def detect_model_quality_degradation(self) -> Optional[Incident]:
        """
        Detect model quality degradation.

        TODO: Implement quality monitoring
        - Compare recent predictions vs. ground truth
        - Detect accuracy drops
        - Monitor drift metrics
        """
        pass

    def _query_prometheus(self, query: str) -> float:
        """Query Prometheus and return single value."""
        # TODO: Implement Prometheus query
        # response = requests.get(
        #     f"{self.prometheus_url}/api/v1/query",
        #     params={'query': query}
        # )
        # result = response.json()
        # return float(result['data']['result'][0]['value'][1])
        return 0.0  # Placeholder

    def _generate_incident_id(self) -> str:
        """Generate unique incident ID."""
        return f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"


class AutomatedRemediation:
    """Automated remediation actions for common incidents."""

    def __init__(self, k8s_client=None):
        """
        Initialize remediation system.

        Args:
            k8s_client: Kubernetes client for scaling operations
        """
        self.k8s_client = k8s_client

    def scale_up_replicas(self, deployment_name: str, target_replicas: int) -> bool:
        """
        Scale up deployment replicas.

        TODO: Implement auto-scaling
        - Use Kubernetes API to scale deployment
        - Wait for pods to be ready
        - Verify scaling completed
        """

        # TODO: Scale deployment
        # try:
        #     logging.info(f"Scaling {deployment_name} to {target_replicas} replicas")

        #     # Update deployment
        #     self.k8s_client.patch_namespaced_deployment_scale(
        #         name=deployment_name,
        #         namespace="default",
        #         body={'spec': {'replicas': target_replicas}}
        #     )

        #     # Wait for scaling
        #     self._wait_for_ready_replicas(deployment_name, target_replicas)

        #     logging.info(f"Successfully scaled {deployment_name} to {target_replicas}")
        #     return True

        # except Exception as e:
        #     logging.error(f"Failed to scale {deployment_name}: {e}")
        #     return False

        pass

    def rollback_deployment(self, deployment_name: str) -> bool:
        """
        Rollback deployment to previous version.

        TODO: Implement rollback
        - Get previous revision
        - Perform rollback
        - Verify rollback success
        """

        # TODO: Rollback deployment
        # try:
        #     logging.info(f"Rolling back {deployment_name}")

        #     # Execute rollback
        #     self.k8s_client.rollback_namespaced_deployment(
        #         name=deployment_name,
        #         namespace="default"
        #     )

        #     logging.info(f"Successfully rolled back {deployment_name}")
        #     return True

        # except Exception as e:
        #     logging.error(f"Failed to rollback {deployment_name}: {e}")
        #     return False

        pass

    def enable_circuit_breaker(self, service_name: str) -> bool:
        """
        Enable circuit breaker for service.

        TODO: Implement circuit breaker activation
        - Update service configuration
        - Apply circuit breaker rules
        """
        pass

    def trigger_cache_warming(self, model_uri: str) -> bool:
        """
        Trigger cache warming to reduce latency.

        TODO: Implement cache warming
        - Pre-load model
        - Warm up prediction cache
        """
        pass


class IncidentManager:
    """Manage incident lifecycle and response."""

    def __init__(
        self,
        detector: IncidentDetector,
        remediation: AutomatedRemediation,
        pagerduty_key: Optional[str] = None
    ):
        """
        Initialize incident manager.

        Args:
            detector: Incident detector
            remediation: Automated remediation system
            pagerduty_key: PagerDuty API key for alerting
        """
        self.detector = detector
        self.remediation = remediation
        self.pagerduty_key = pagerduty_key

    def run_detection_cycle(self) -> List[Incident]:
        """
        Run incident detection cycle.

        TODO: Run all detectors and collect incidents
        """

        incidents = []

        # TODO: Run detectors
        # latency_incident = self.detector.detect_latency_spike()
        # if latency_incident:
        #     incidents.append(latency_incident)
        #     self._handle_incident(latency_incident)

        # error_incident = self.detector.detect_error_rate_spike()
        # if error_incident:
        #     incidents.append(error_incident)
        #     self._handle_incident(error_incident)

        # resource_incident = self.detector.detect_resource_exhaustion()
        # if resource_incident:
        #     incidents.append(resource_incident)
        #     self._handle_incident(resource_incident)

        return incidents

    def _handle_incident(self, incident: Incident):
        """
        Handle detected incident.

        TODO: Implement incident handling
        - Send alerts
        - Attempt automated remediation
        - Escalate if needed
        """

        logging.warning(f"Incident detected: {incident.title} (Severity: {incident.severity.value})")

        # TODO: Send alert
        # self._send_alert(incident)

        # TODO: Attempt automated remediation
        # if incident.severity in [IncidentSeverity.P0, IncidentSeverity.P1]:
        #     self._attempt_remediation(incident)

        pass

    def _attempt_remediation(self, incident: Incident):
        """
        Attempt automated remediation.

        TODO: Implement remediation logic based on incident type
        """

        # if "Latency Spike" in incident.title:
        #     # Scale up to handle load
        #     success = self.remediation.scale_up_replicas("ml-model-serving", 10)
        #     if success:
        #         incident.timeline.append({
        #             'timestamp': datetime.now(),
        #             'event': 'Automated remediation',
        #             'details': 'Scaled up to 10 replicas'
        #         })

        # elif "Error Rate" in incident.title:
        #     # Rollback to previous version
        #     success = self.remediation.rollback_deployment("ml-model-serving")
        #     if success:
        #         incident.timeline.append({
        #             'timestamp': datetime.now(),
        #             'event': 'Automated remediation',
        #             'details': 'Rolled back to previous version'
        #         })

        pass

    def _send_alert(self, incident: Incident):
        """Send alert to on-call engineer."""

        if self.pagerduty_key:
            # TODO: Send PagerDuty alert
            # import pdpyras
            # session = pdpyras.APISession(self.pagerduty_key)
            # session.trigger_incident(
            #     title=incident.title,
            #     severity=incident.severity.value,
            #     description=incident.description
            # )
            pass
        else:
            logging.warning(f"ALERT: {incident.title} - {incident.description}")


# Usage example
if __name__ == '__main__':
    # Initialize components
    detector = IncidentDetector(
        prometheus_url="http://localhost:9090",
        thresholds={
            'latency_p95_ms': 100,
            'error_rate_pct': 0.1,
            'cpu_usage_pct': 80,
            'memory_usage_pct': 85
        }
    )

    remediation = AutomatedRemediation()

    manager = IncidentManager(
        detector=detector,
        remediation=remediation,
        pagerduty_key=None  # Set if using PagerDuty
    )

    # Run detection cycle
    print("Running incident detection...")
    incidents = manager.run_detection_cycle()

    if incidents:
        print(f"\n{len(incidents)} incidents detected:")
        for inc in incidents:
            print(f"  - [{inc.severity.value}] {inc.title}")
            print(f"    {inc.description}")
    else:
        print("No incidents detected")
```

### Runbook Example

```markdown
# ML Model Serving Runbook

## High Latency Incident

### Detection
- Alert: "SLOLatencyViolation"
- Metric: P95 latency > 100ms

### Diagnosis
1. Check current latency:
   ```bash
   # Query Prometheus
   curl 'http://prometheus:9090/api/v1/query?query=histogram_quantile(0.95,rate(prediction_latency_bucket[5m]))'
   ```

2. Check replica count:
   ```bash
   kubectl get deployment ml-model-serving
   ```

3. Check resource usage:
   ```bash
   kubectl top pods -l app=ml-model
   ```

### Remediation
1. **Immediate**: Scale up replicas
   ```bash
   kubectl scale deployment ml-model-serving --replicas=10
   ```

2. **If OOM**: Increase memory limits
   ```bash
   kubectl set resources deployment ml-model-serving --limits=memory=4Gi
   ```

3. **If still slow**: Check model size and consider optimization

### Escalation
- P1: Page on-call engineer immediately
- P2: Create ticket for ML team

## Error Rate Spike

### Detection
- Alert: "SLOAvailabilityViolation"
- Metric: Error rate > 0.1%

### Diagnosis
1. Check recent deployments:
   ```bash
   kubectl rollout history deployment ml-model-serving
   ```

2. Check logs for errors:
   ```bash
   kubectl logs -l app=ml-model --tail=100 | grep ERROR
   ```

### Remediation
1. **Immediate**: Rollback to previous version
   ```bash
   kubectl rollout undo deployment ml-model-serving
   ```

2. Verify rollback success:
   ```bash
   kubectl rollout status deployment ml-model-serving
   ```

### Prevention
- Add canary deployment
- Improve integration tests
- Add model validation step
```

### Success Criteria

- [ ] Incident detection works for multiple scenarios
- [ ] Automated remediation triggers correctly
- [ ] Alerts sent on incident detection
- [ ] Runbook procedures documented
- [ ] Incident timeline tracked
- [ ] Post-incident analysis generated

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Detection Thresholds**: Use 1.5x-2x normal for spike detection
2. **Remediation Order**: Scale first, rollback if that doesn't help
3. **Circuit Breaker**: Fail fast to prevent cascade failures
4. **Alerting**: P0/P1 page immediately, P2/P3 create tickets
5. **Timeline**: Track all actions for post-incident review
6. **Escalation**: Define clear escalation paths and timeouts

</details>

---
