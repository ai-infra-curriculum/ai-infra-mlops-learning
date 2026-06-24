## Exercise 1: Production Readiness Checklist (75 minutes)

**Objective**: Build an automated production-readiness checker that validates an ML model against operational standards and produces a defensible go/no-go decision.

### Background

The most expensive ML outages trace back to a model that was *trained* well but *operationalized*
poorly: no latency budget, no metrics, no runbook, no rollback. A production-readiness review turns
those tacit expectations into an executable checklist so the same bar applies to every model and
nothing ships on optimism.

Your checker groups checks into categories and classifies each result:

- **Performance** — latency percentiles, throughput headroom, resource limits, model size.
- **Reliability** — error handling, input validation, retries, circuit breakers.
- **Monitoring** — metrics instrumentation, structured logging, alerts, dashboards.
- **Security** — authn/authz, secrets management, input sanitization.
- **Data** — feature validation, drift monitoring, data versioning.
- **Documentation** — runbook, SLOs, API docs.

A check is `PASS`, `WARNING`, `FAIL`, or `NOT_APPLICABLE`. A *blocking* `FAIL` flips the overall
decision to **NO-GO**; warnings are surfaced but do not block. The output is a structured report you
can attach to a deployment ticket.

### Tasks

1. **Implement the performance checks** — measure real p50/p95/p99 latency and compute throughput.
2. **Implement the monitoring checks** — verify the `/metrics` endpoint exposes required series.
3. **Implement the config-driven checks** — resource limits, SLOs, alerts, runbook presence.
4. **Implement the boolean policy checks** — reliability, security, and data checks from config flags.
5. **Generate the summary** with a go/no-go decision and per-blocker recommendations.

### Starter Code

Every check below is implemented. Checks that require a live model measure it directly; checks that
validate operational posture read from `deployment_config`. Replace the synthetic
`_get_sample_input` with your production feature schema.

```python
# production_readiness.py
"""Production readiness assessment for ML models."""

import logging
import os
import time
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

import numpy as np
import requests

logger = logging.getLogger(__name__)


class CheckStatus(Enum):
    """Status of a readiness check."""
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    NOT_APPLICABLE = "n/a"


@dataclass
class ReadinessCheck:
    """A single production-readiness check result."""
    category: str
    check_name: str
    status: CheckStatus
    details: str
    blocker: bool = False
    recommendation: Optional[str] = None


class ProductionReadinessChecker:
    """Comprehensive production-readiness assessment."""

    def __init__(self, model, deployment_config: dict):
        """
        Args:
            model: A loaded model exposing ``.predict(X)`` (e.g. an MLflow pyfunc model).
            deployment_config: SLOs, service URL, k8s resources, alerts, and runbook path.
        """
        self.model = model
        self.deployment_config = deployment_config
        self.checks: List[ReadinessCheck] = []

    def run_all_checks(self) -> dict:
        """Run every check and return the summary with a go/no-go decision."""
        logger.info("Running production readiness checks")

        # Performance
        self._check_latency_requirements()
        self._check_throughput_capacity()
        self._check_resource_limits()

        # Monitoring
        self._check_metrics_instrumentation()
        self._check_alerting_setup()

        # Reliability / security / data (policy-driven)
        self._check_boolean_policy("Reliability", "Input Validation", "input_validation", blocker=True)
        self._check_boolean_policy("Reliability", "Retry Logic", "retry_logic")
        self._check_boolean_policy("Reliability", "Circuit Breakers", "circuit_breakers")
        self._check_boolean_policy("Security", "Authentication", "authentication", blocker=True)
        self._check_boolean_policy("Security", "Secrets Management", "secrets_management", blocker=True)
        self._check_boolean_policy("Data", "Drift Monitoring", "drift_monitoring")
        self._check_boolean_policy("Data", "Data Versioning", "data_versioning")

        # Documentation
        self._check_runbook_exists()
        self._check_slos_defined()

        return self._generate_summary()

    def _check_latency_requirements(self) -> None:
        """Measure p50/p95/p99 latency over 100 predictions and compare to the SLO."""
        sample = self._get_sample_input()
        latencies = []
        for _ in range(100):
            start = time.perf_counter()
            try:
                self.model.predict(sample)
            except Exception as exc:  # noqa: BLE001 - record failure as a blocker
                self.checks.append(ReadinessCheck(
                    category="Performance", check_name="Latency SLO",
                    status=CheckStatus.FAIL,
                    details=f"Prediction raised during latency test: {exc}",
                    blocker=True,
                    recommendation="Fix prediction errors before measuring latency.",
                ))
                return
            latencies.append((time.perf_counter() - start) * 1000)  # ms

        p50, p95, p99 = (float(np.percentile(latencies, q)) for q in (50, 95, 99))
        slo_ms = self.deployment_config.get("latency_slo_ms", 100)

        if p99 <= slo_ms:
            status, blocker, rec = CheckStatus.PASS, False, None
            details = f"p99 {p99:.1f}ms within SLO ({slo_ms}ms); p50={p50:.1f}, p95={p95:.1f}"
        elif p95 <= slo_ms:
            status, blocker = CheckStatus.WARNING, False
            details = f"p95 within SLO but p99 {p99:.1f}ms exceeds {slo_ms}ms"
            rec = "Optimize tail latency or add replicas before high-traffic launch."
        else:
            status, blocker = CheckStatus.FAIL, True
            details = f"p95 {p95:.1f}ms exceeds SLO ({slo_ms}ms)"
            rec = "Model optimization (quantization/batching) required before deployment."

        self.checks.append(ReadinessCheck(
            category="Performance", check_name="Latency SLO",
            status=status, details=details, blocker=blocker, recommendation=rec,
        ))

    def _check_throughput_capacity(self) -> None:
        """Estimate single-replica QPS and compare to expected load."""
        avg_latency_s = self._measure_average_latency()
        if avg_latency_s <= 0:
            return
        # 70% utilization headroom for GC pauses, bursts, and noisy neighbors.
        max_qps = int((1 / avg_latency_s) * 0.7)
        expected_qps = self.deployment_config.get("expected_qps", 100)

        if max_qps >= expected_qps:
            self.checks.append(ReadinessCheck(
                category="Performance", check_name="Throughput Capacity",
                status=CheckStatus.PASS,
                details=f"Single replica {max_qps} QPS >= expected {expected_qps} QPS",
            ))
        else:
            replicas = int(np.ceil(expected_qps / max(max_qps, 1)))
            self.checks.append(ReadinessCheck(
                category="Performance", check_name="Throughput Capacity",
                status=CheckStatus.WARNING,
                details=f"Single replica {max_qps} QPS < expected {expected_qps} QPS",
                recommendation=f"Deploy at least {replicas} replicas to meet expected load.",
            ))

    def _check_resource_limits(self) -> None:
        """Verify CPU and memory requests/limits are set on the deployment."""
        resources = self.deployment_config.get("kubernetes", {}).get("resources", {})
        limits, requests_ = resources.get("limits", {}), resources.get("requests", {})

        if not limits or not requests_:
            self.checks.append(ReadinessCheck(
                category="Performance", check_name="Resource Limits",
                status=CheckStatus.FAIL,
                details="Resource limits and/or requests not configured",
                blocker=True,
                recommendation="Set CPU and memory requests and limits to prevent OOM and throttling.",
            ))
        elif "memory" not in limits or "cpu" not in limits:
            self.checks.append(ReadinessCheck(
                category="Performance", check_name="Resource Limits",
                status=CheckStatus.WARNING,
                details=f"Incomplete limits: {limits}",
                recommendation="Set both CPU and memory limits.",
            ))
        else:
            self.checks.append(ReadinessCheck(
                category="Performance", check_name="Resource Limits",
                status=CheckStatus.PASS, details=f"Resources configured: {limits}",
            ))

    def _check_metrics_instrumentation(self) -> None:
        """Verify the service exposes a /metrics endpoint with required series."""
        service_url = self.deployment_config.get("service_url")
        if not service_url:
            self.checks.append(ReadinessCheck(
                category="Monitoring", check_name="Metrics Instrumentation",
                status=CheckStatus.NOT_APPLICABLE,
                details="Service URL not configured; cannot probe /metrics",
            ))
            return

        required = ["prediction_latency", "prediction_total",
                    "prediction_errors_total", "model_version"]
        try:
            response = requests.get(f"{service_url.rstrip('/')}/metrics", timeout=5)
            response.raise_for_status()
            missing = [name for name in required if name not in response.text]
        except requests.RequestException as exc:
            self.checks.append(ReadinessCheck(
                category="Monitoring", check_name="Metrics Instrumentation",
                status=CheckStatus.FAIL,
                details=f"Failed to scrape /metrics: {exc}",
                blocker=True,
                recommendation="Expose a Prometheus /metrics endpoint before deployment.",
            ))
            return

        if missing:
            self.checks.append(ReadinessCheck(
                category="Monitoring", check_name="Metrics Instrumentation",
                status=CheckStatus.FAIL,
                details=f"Missing required metrics: {', '.join(missing)}",
                blocker=True,
                recommendation="Instrument latency, request, error, and version metrics.",
            ))
        else:
            self.checks.append(ReadinessCheck(
                category="Monitoring", check_name="Metrics Instrumentation",
                status=CheckStatus.PASS, details="All required metrics instrumented",
            ))

    def _check_alerting_setup(self) -> None:
        """Verify required alert rules are configured."""
        configured = {alert["name"] for alert in self.deployment_config.get("alerts", [])}
        required = {"high_error_rate", "high_latency", "low_availability"}
        missing = required - configured

        if not missing:
            self.checks.append(ReadinessCheck(
                category="Monitoring", check_name="Alerting",
                status=CheckStatus.PASS, details=f"{len(configured)} alerts configured",
            ))
        else:
            self.checks.append(ReadinessCheck(
                category="Monitoring", check_name="Alerting",
                status=CheckStatus.WARNING,
                details=f"Missing alerts: {', '.join(sorted(missing))}",
                recommendation="Add alerts for error rate, latency, and availability.",
            ))

    def _check_boolean_policy(
        self, category: str, check_name: str, config_key: str, blocker: bool = False
    ) -> None:
        """Generic check for a policy flag in ``deployment_config['policies']``."""
        enabled = self.deployment_config.get("policies", {}).get(config_key)
        if enabled is True:
            self.checks.append(ReadinessCheck(
                category=category, check_name=check_name,
                status=CheckStatus.PASS, details=f"{check_name} is enabled",
            ))
        else:
            self.checks.append(ReadinessCheck(
                category=category, check_name=check_name,
                status=CheckStatus.FAIL if blocker else CheckStatus.WARNING,
                details=f"{check_name} is not enabled (policies.{config_key})",
                blocker=blocker,
                recommendation=f"Enable {check_name.lower()} before production deployment.",
            ))

    def _check_runbook_exists(self) -> None:
        """Verify an operational runbook exists with the required sections."""
        path = self.deployment_config.get("runbook_path")
        if not path or not os.path.exists(path):
            self.checks.append(ReadinessCheck(
                category="Documentation", check_name="Runbook",
                status=CheckStatus.WARNING,
                details=f"Runbook not found ({path or 'no path configured'})",
                recommendation="Create a runbook covering deploy, monitor, incident, and rollback.",
            ))
            return

        with open(path, encoding="utf-8") as handle:
            content = handle.read()
        required = ["Deployment", "Monitoring", "Incident", "Rollback"]
        missing = [section for section in required if section not in content]
        if missing:
            self.checks.append(ReadinessCheck(
                category="Documentation", check_name="Runbook",
                status=CheckStatus.WARNING,
                details=f"Runbook missing sections: {', '.join(missing)}",
                recommendation="Add the missing runbook sections.",
            ))
        else:
            self.checks.append(ReadinessCheck(
                category="Documentation", check_name="Runbook",
                status=CheckStatus.PASS, details=f"Complete runbook at {path}",
            ))

    def _check_slos_defined(self) -> None:
        """Verify availability, latency, and error-rate SLOs are defined."""
        defined = set(self.deployment_config.get("slos", {}))
        required = {"availability", "latency", "error_rate"}
        missing = required - defined
        if not missing:
            self.checks.append(ReadinessCheck(
                category="Documentation", check_name="SLOs Defined",
                status=CheckStatus.PASS, details=f"SLOs defined: {sorted(defined)}",
            ))
        else:
            self.checks.append(ReadinessCheck(
                category="Documentation", check_name="SLOs Defined",
                status=CheckStatus.FAIL,
                details=f"Missing SLOs: {', '.join(sorted(missing))}",
                blocker=True,
                recommendation="Define availability, latency, and error-rate SLOs.",
            ))

    def _get_sample_input(self):
        """Return a representative input batch. Replace with your production schema."""
        n_features = self.deployment_config.get("n_features", 10)
        return np.random.randn(1, n_features)

    def _measure_average_latency(self, iterations: int = 50) -> float:
        """Average prediction latency in seconds over ``iterations`` calls."""
        sample = self._get_sample_input()
        durations = []
        for _ in range(iterations):
            start = time.perf_counter()
            try:
                self.model.predict(sample)
            except Exception:  # noqa: BLE001 - latency probe must not crash the review
                return -1.0
            durations.append(time.perf_counter() - start)
        return float(np.mean(durations))

    def _generate_summary(self) -> dict:
        """Roll up checks into a go/no-go decision."""
        blockers = [c for c in self.checks if c.blocker and c.status == CheckStatus.FAIL]
        warnings = [c for c in self.checks if c.status == CheckStatus.WARNING]
        passed = [c for c in self.checks if c.status == CheckStatus.PASS]
        failed = [c for c in self.checks if c.status == CheckStatus.FAIL]
        ready = len(blockers) == 0

        def serialize(check: ReadinessCheck) -> dict:
            return {
                "category": check.category, "check": check.check_name,
                "status": check.status.value, "details": check.details,
                "blocker": check.blocker, "recommendation": check.recommendation,
            }

        return {
            "ready_for_production": ready,
            "decision": "GO" if ready else "NO-GO",
            "summary": {
                "total_checks": len(self.checks),
                "passed": len(passed), "warnings": len(warnings),
                "failed": len(failed), "blockers": len(blockers),
            },
            "blocker_details": [serialize(c) for c in blockers],
            "warnings": [serialize(c) for c in warnings],
            "all_checks": [serialize(c) for c in self.checks],
        }


# Usage example
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    class _DummyModel:
        def predict(self, x):
            return np.zeros(len(x))

    checker = ProductionReadinessChecker(
        model=_DummyModel(),
        deployment_config={
            "latency_slo_ms": 100,
            "expected_qps": 500,
            "n_features": 10,
            "service_url": None,  # set to a real URL to probe /metrics
            "runbook_path": "runbooks/credit_model.md",
            "kubernetes": {
                "resources": {
                    "requests": {"cpu": "1", "memory": "2Gi"},
                    "limits": {"cpu": "2", "memory": "4Gi"},
                }
            },
            "slos": {"availability": 99.9, "latency": 100, "error_rate": 0.1},
            "alerts": [
                {"name": "high_error_rate"},
                {"name": "high_latency"},
                {"name": "low_availability"},
            ],
            "policies": {
                "input_validation": True,
                "retry_logic": True,
                "circuit_breakers": False,
                "authentication": True,
                "secrets_management": True,
                "drift_monitoring": True,
                "data_versioning": False,
            },
        },
    )

    results = checker.run_all_checks()
    print(f"\nDecision: {results['decision']}")
    print(f"Summary: {results['summary']}")
    for blocker in results["blocker_details"]:
        print(f"  BLOCKER [{blocker['category']}] {blocker['check']}: {blocker['details']}")
```

### Validation

```python
# test_production_readiness.py
"""Tests for the production-readiness checker."""

import time

import numpy as np
import pytest

from production_readiness import CheckStatus, ProductionReadinessChecker


class FastModel:
    def predict(self, x):
        return np.zeros(len(x))


class SlowModel:
    def predict(self, x):
        time.sleep(0.2)  # 200ms — exceeds a 100ms SLO
        return np.zeros(len(x))


def _config(**overrides):
    base = {
        "latency_slo_ms": 100, "expected_qps": 1, "n_features": 4,
        "service_url": None, "runbook_path": None,
        "kubernetes": {"resources": {
            "requests": {"cpu": "1", "memory": "1Gi"},
            "limits": {"cpu": "1", "memory": "1Gi"},
        }},
        "slos": {"availability": 99.9, "latency": 100, "error_rate": 0.1},
        "alerts": [{"name": "high_error_rate"}, {"name": "high_latency"},
                   {"name": "low_availability"}],
        "policies": {k: True for k in (
            "input_validation", "retry_logic", "circuit_breakers",
            "authentication", "secrets_management", "drift_monitoring", "data_versioning")},
    }
    base.update(overrides)
    return base


def test_latency_check_passes_when_fast():
    checker = ProductionReadinessChecker(FastModel(), _config())
    checker._check_latency_requirements()
    latency = next(c for c in checker.checks if c.check_name == "Latency SLO")
    assert latency.status == CheckStatus.PASS


def test_latency_check_fails_when_slow():
    checker = ProductionReadinessChecker(SlowModel(), _config())
    checker._check_latency_requirements()
    latency = next(c for c in checker.checks if c.check_name == "Latency SLO")
    assert latency.status == CheckStatus.FAIL
    assert latency.blocker is True


def test_missing_slo_is_blocking():
    checker = ProductionReadinessChecker(FastModel(), _config(slos={"availability": 99.9}))
    checker._check_slos_defined()
    slo = next(c for c in checker.checks if c.check_name == "SLOs Defined")
    assert slo.blocker is True


def test_summary_is_no_go_with_blockers():
    checker = ProductionReadinessChecker(SlowModel(), _config())
    results = checker.run_all_checks()
    assert results["decision"] == "NO-GO"
    assert results["summary"]["blockers"] >= 1

# Run with: pytest test_production_readiness.py -v
```

### Success Criteria

- [ ] All six check categories are implemented and runnable
- [ ] Latency check measures real p50/p95/p99 and compares to the SLO
- [ ] Throughput check estimates QPS with utilization headroom and recommends replica counts
- [ ] Metrics check probes the live `/metrics` endpoint for required series
- [ ] Blocking failures flip the decision to NO-GO; warnings do not block
- [ ] The summary returns a structured, serializable go/no-go report
- [ ] Tests pass

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Percentiles, not averages**: p99 latency is what users feel under load — gate on it.
2. **Utilization headroom**: never plan capacity at 100%; 70% leaves room for GC, bursts, and
   noisy neighbors.
3. **Blocker vs. warning**: make security, metrics, latency, and SLO checks blockers; treat
   dashboards and optional alerts as warnings.
4. **Probe, don't assume**: actually `GET /metrics` and grep for required series rather than trusting
   that instrumentation exists.
5. **Policy flags**: model reliability/security/data posture as explicit config so the review is
   reproducible and auditable.
6. **Actionable output**: every failure carries a recommendation so the report doubles as a fix list.

</details>

---
