## Exercise 3: SLO/SLI Definition & Monitoring (90 minutes)

**Objective**: Define SLIs and SLOs for an ML serving system and implement error-budget tracking with Prometheus, alert rules, and a compliance report.

### Background

An SLO turns "the service should be reliable" into a measurable contract. The pieces:

- **SLI (Service Level Indicator)** — the metric: success rate, p95 latency, error rate.
- **SLO (Service Level Objective)** — the target over a rolling window: "99.9% availability over 30 days".
- **Error budget** — the allowed failure: `1 - SLO`. At 99.9%, you may fail 0.1% of requests. Spend
  it on risky deploys; freeze deploys when it runs out.

Error budgets are the mechanism that makes SLOs actionable. Instead of arguing about whether to ship,
you check the budget: budget remaining → ship; budget exhausted → freeze and stabilize. This exercise
implements the budget math, queries SLIs from Prometheus, and wires alerts to fire at 25% remaining
and on exhaustion.

Common ML serving SLOs:

- **Availability**: 99.9% of requests succeed.
- **Latency**: 95% of requests complete in < 100ms.
- **Error rate**: < 0.1% of predictions fail.
- **Freshness**: model artifact age < 7 days.

### Tasks

1. **Define SLIs and SLOs** as typed objects (availability, latency, freshness).
2. **Implement error-budget math** — allowed failures, remaining budget, status banding.
3. **Query live SLIs from Prometheus** (availability, latency percentile).
4. **Check compliance** of each SLO against its target.
5. **Generate a compliance report** and **author alert rules** for budget burn.

### Starter Code

`calculate_error_budget`, `check_slo_compliance`, the SLI queries, and the report are fully
implemented. The Prometheus integration uses `prometheus-api-client`; swap in a mock for tests.

```python
# slo_monitor.py
"""SLO/SLI monitoring and error-budget tracking."""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from prometheus_api_client import PrometheusConnect

logger = logging.getLogger(__name__)


@dataclass
class SLI:
    """Service Level Indicator definition."""
    name: str
    description: str
    metric_name: str
    query: str           # PromQL returning the current SLI value
    unit: str            # "%", "ms", "count"


@dataclass
class SLO:
    """Service Level Objective definition."""
    name: str
    sli: SLI
    target: float        # e.g. 99.9 for 99.9%
    window_days: int     # rolling window, e.g. 30
    comparison: str = "gte"  # "gte": value must be >= target; "lte": value must be <= target


def _band(budget_remaining_pct: float) -> str:
    """Map remaining-budget percentage to a status band."""
    if budget_remaining_pct <= 0:
        return "EXHAUSTED"
    if budget_remaining_pct < 25:
        return "CRITICAL"
    if budget_remaining_pct < 50:
        return "WARNING"
    return "HEALTHY"


class SLOMonitor:
    """Monitor SLOs and track error budgets."""

    def __init__(self, slos: List[SLO], prometheus_url: str = "http://localhost:9090"):
        self.slos = slos
        self.prometheus_url = prometheus_url
        self.prom = PrometheusConnect(url=prometheus_url, disable_ssl=True)

    def calculate_error_budget(
        self, slo: SLO, total_requests: int, failed_requests: int
    ) -> dict:
        """
        Compute the error budget for a request-based SLO.

        allowed_failure_rate = (100 - target) / 100
        allowed_failures     = total_requests * allowed_failure_rate
        remaining_failures   = allowed_failures - failed_requests
        budget_remaining_pct = remaining_failures / allowed_failures * 100
        """
        allowed_failure_rate = (100 - slo.target) / 100
        allowed_failures = int(total_requests * allowed_failure_rate)
        actual_failure_rate = (
            failed_requests / total_requests * 100 if total_requests else 0.0
        )
        remaining_failures = allowed_failures - failed_requests
        budget_remaining_pct = (
            remaining_failures / allowed_failures * 100 if allowed_failures else 0.0
        )

        return {
            "slo_name": slo.name,
            "target": slo.target,
            "window_days": slo.window_days,
            "total_requests": total_requests,
            "failed_requests": failed_requests,
            "allowed_failures": allowed_failures,
            "actual_failure_rate": round(actual_failure_rate, 4),
            "target_failure_rate": round(allowed_failure_rate * 100, 4),
            "remaining_failures": remaining_failures,
            "budget_remaining_pct": round(budget_remaining_pct, 2),
            "status": _band(budget_remaining_pct),
            "budget_exhausted": remaining_failures <= 0,
        }

    def check_slo_compliance(self, slo: SLO) -> dict:
        """Query the SLI and compare against the target per ``slo.comparison``."""
        try:
            result = self.prom.custom_query(slo.sli.query)
        except Exception as exc:  # noqa: BLE001 - surface query failures in the report
            logger.error("Error querying SLO %s: %s", slo.name, exc)
            return {"slo_name": slo.name, "compliant": False, "error": str(exc)}

        if not result:
            return {"slo_name": slo.name, "compliant": False, "error": "no data"}

        current = float(result[0]["value"][1])
        compliant = current >= slo.target if slo.comparison == "gte" else current <= slo.target
        gap = current - slo.target if slo.comparison == "gte" else slo.target - current
        return {
            "slo_name": slo.name,
            "target": slo.target,
            "current_value": round(current, 4),
            "compliant": compliant,
            "gap": round(gap, 4),
        }

    def get_availability_sli(self, window_minutes: int = 60) -> Optional[float]:
        """Success rate (%) over the window."""
        query = (
            f"(sum(rate(prediction_total{{status=\"success\"}}[{window_minutes}m])) / "
            f"clamp_min(sum(rate(prediction_total[{window_minutes}m])), 1)) * 100"
        )
        return self._scalar(query)

    def get_latency_sli(self, percentile: int = 95, window_minutes: int = 60) -> Optional[float]:
        """p{percentile} latency in milliseconds over the window."""
        query = (
            f"histogram_quantile({percentile / 100}, "
            f"rate(prediction_latency_bucket[{window_minutes}m])) * 1000"
        )
        return self._scalar(query)

    def _scalar(self, query: str) -> Optional[float]:
        try:
            result = self.prom.custom_query(query)
        except Exception as exc:  # noqa: BLE001
            logger.error("Prometheus query failed: %s", exc)
            return None
        return float(result[0]["value"][1]) if result else None

    def _get_total_requests(self, window_days: int) -> int:
        result = self._scalar(f"sum(increase(prediction_total[{window_days}d]))")
        return int(result) if result is not None else 0

    def _get_failed_requests(self, window_days: int) -> int:
        result = self._scalar(
            f"sum(increase(prediction_total{{status=\"error\"}}[{window_days}d]))"
        )
        return int(result) if result is not None else 0

    def check_all_slos(self) -> Dict[str, dict]:
        """Check compliance and (for request-based SLOs) error budget for every SLO."""
        results: Dict[str, dict] = {}
        for slo in self.slos:
            compliance = self.check_slo_compliance(slo)
            error_budget = None
            if slo.name == "availability":
                total = self._get_total_requests(slo.window_days)
                failed = self._get_failed_requests(slo.window_days)
                if total:
                    error_budget = self.calculate_error_budget(slo, total, failed)
            results[slo.name] = {"compliance": compliance, "error_budget": error_budget}
        return results

    def generate_slo_report(self) -> str:
        """Render a human-readable SLO compliance report."""
        results = self.check_all_slos()
        lines = [
            "=" * 70,
            "SLO COMPLIANCE REPORT",
            "=" * 70,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ]
        for slo_name, data in results.items():
            compliance = data["compliance"]
            lines += ["", slo_name.upper(), "-" * 70]
            if compliance.get("error"):
                lines.append(f"  ERROR: {compliance['error']}")
                continue
            mark = "COMPLIANT" if compliance["compliant"] else "NON-COMPLIANT"
            lines += [
                f"  Target:  {compliance['target']}",
                f"  Current: {compliance['current_value']}",
                f"  Status:  {mark} (gap {compliance['gap']:+})",
            ]
            budget = data["error_budget"]
            if budget:
                lines += [
                    "  Error Budget:",
                    f"    Status:    {budget['status']}",
                    f"    Remaining: {budget['budget_remaining_pct']:.2f}%",
                    f"    Failures:  {budget['failed_requests']:,} / {budget['allowed_failures']:,}",
                ]
        return "\n".join(lines)


# SLO definitions
availability_slo = SLO(
    name="availability",
    sli=SLI(
        name="availability",
        description="Percentage of successful predictions",
        metric_name="prediction_total",
        query="(sum(rate(prediction_total{status=\"success\"}[5m])) / "
              "clamp_min(sum(rate(prediction_total[5m])), 1)) * 100",
        unit="%",
    ),
    target=99.9,
    window_days=30,
    comparison="gte",
)

latency_slo = SLO(
    name="latency_p95",
    sli=SLI(
        name="latency_p95",
        description="95th percentile prediction latency",
        metric_name="prediction_latency",
        query="histogram_quantile(0.95, rate(prediction_latency_bucket[5m])) * 1000",
        unit="ms",
    ),
    target=100,        # p95 must be <= 100ms
    window_days=30,
    comparison="lte",
)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    monitor = SLOMonitor([availability_slo, latency_slo], "http://localhost:9090")
    print(monitor.generate_slo_report())

    budget = monitor.calculate_error_budget(
        slo=availability_slo, total_requests=1_000_000, failed_requests=500
    )
    print(f"\nError budget status: {budget['status']}")
    print(f"Budget remaining: {budget['budget_remaining_pct']:.2f}%")
    print(f"Failures: {budget['failed_requests']:,} / {budget['allowed_failures']:,}")
```

### Prometheus Alert Rules

These rules alert on direct SLO violations and on error-budget burn. The
`slo_error_budget_remaining_percent` gauge is exported by a recording job (or pushed by the monitor
above) so Alertmanager can page before the budget is fully gone.

```yaml
# prometheus_alerts.yml
groups:
  - name: slo_alerts
    interval: 1m
    rules:
      - alert: SLOAvailabilityViolation
        expr: |
          (sum(rate(prediction_total{status="success"}[5m])) /
           clamp_min(sum(rate(prediction_total[5m])), 1)) * 100 < 99.9
        for: 5m
        labels:
          severity: critical
          slo: availability
        annotations:
          summary: "Availability SLO violated"
          description: "Availability is {{ $value }}%, below the 99.9% target."

      - alert: SLOLatencyViolation
        expr: |
          histogram_quantile(0.95, rate(prediction_latency_bucket[5m])) * 1000 > 100
        for: 5m
        labels:
          severity: warning
          slo: latency
        annotations:
          summary: "Latency SLO violated"
          description: "p95 latency is {{ $value }}ms, above the 100ms target."

      - alert: ErrorBudgetCritical
        expr: slo_error_budget_remaining_percent < 25
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Error budget critically low"
          description: "Only {{ $value }}% budget remaining for {{ $labels.slo_name }}."

      - alert: ErrorBudgetExhausted
        expr: slo_error_budget_remaining_percent <= 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Error budget exhausted"
          description: "Budget exhausted for {{ $labels.slo_name }}; freeze deployments."
```

### Validation

```python
# test_slo_monitor.py
"""Tests for error-budget math and compliance checks."""

from unittest.mock import MagicMock, patch

import pytest

from slo_monitor import SLI, SLO, SLOMonitor, _band


@pytest.fixture
def availability():
    return SLO(
        name="availability",
        sli=SLI(name="a", description="", metric_name="m", query="q", unit="%"),
        target=99.9, window_days=30, comparison="gte",
    )


def _monitor(slos):
    with patch("slo_monitor.PrometheusConnect"):
        return SLOMonitor(slos, "http://localhost:9090")


def test_error_budget_healthy(availability):
    monitor = _monitor([availability])
    budget = monitor.calculate_error_budget(availability, total_requests=1_000_000,
                                             failed_requests=100)
    # Allowed = 1000 failures; 100 used → 90% remaining.
    assert budget["allowed_failures"] == 1000
    assert budget["status"] == "HEALTHY"
    assert budget["budget_exhausted"] is False


def test_error_budget_exhausted(availability):
    monitor = _monitor([availability])
    budget = monitor.calculate_error_budget(availability, total_requests=1_000_000,
                                             failed_requests=1500)
    assert budget["budget_exhausted"] is True
    assert budget["status"] == "EXHAUSTED"


def test_band_thresholds():
    assert _band(80) == "HEALTHY"
    assert _band(40) == "WARNING"
    assert _band(10) == "CRITICAL"
    assert _band(0) == "EXHAUSTED"


def test_latency_compliance_uses_lte():
    latency = SLO(
        name="latency_p95",
        sli=SLI(name="l", description="", metric_name="m", query="q", unit="ms"),
        target=100, window_days=30, comparison="lte",
    )
    monitor = _monitor([latency])
    monitor.prom.custom_query = MagicMock(return_value=[{"value": [0, "85.0"]}])
    result = monitor.check_slo_compliance(latency)
    assert result["compliant"] is True  # 85ms <= 100ms target

# Run with: pytest test_slo_monitor.py -v
```

### Success Criteria

- [ ] SLIs and SLOs are defined for availability, latency, and freshness
- [ ] Error-budget math is correct (allowed failures, remaining %, status band)
- [ ] Compliance checks query Prometheus and respect `gte`/`lte` comparison direction
- [ ] The compliance report renders every SLO with budget status
- [ ] Alert rules fire on SLO violation, budget < 25%, and budget exhaustion
- [ ] Tests pass

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Error budget = `1 - SLO`**: at 99.9% you may fail 0.1% of requests; `allowed = total * 0.001`.
2. **Comparison direction matters**: availability is "value ≥ target"; latency is "value ≤ target".
   Storing the direction on the SLO keeps `check_slo_compliance` generic.
3. **Rolling window, not calendar month**: use `[30d]` ranges so the budget reflects a moving window.
4. **`clamp_min(..., 1)`** prevents divide-by-zero in availability queries during low traffic.
5. **Burn alerts before exhaustion**: page at 25% remaining so on-call has time to react, then a hard
   critical at 0%.
6. **Freeze policy**: an exhausted budget should automatically block non-emergency deploys — wire the
   `ErrorBudgetExhausted` alert into your release gate.

</details>

---
