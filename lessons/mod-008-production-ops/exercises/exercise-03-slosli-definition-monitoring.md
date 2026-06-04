## Exercise 3: SLO/SLI Definition & Monitoring (90 minutes)

**Objective**: Define and implement SLIs (Service Level Indicators) and SLOs (Service Level Objectives) with error budget tracking.

### Background

SLOs are critical for:
- Setting clear expectations for reliability
- Balancing velocity vs. stability
- Making data-driven decisions about releases
- Error budget consumption tracking

Common ML serving SLOs:
- **Availability**: 99.9% of requests succeed
- **Latency**: 95% of requests < 100ms
- **Error Rate**: < 0.1% of predictions fail

### Tasks

1. **Define SLIs and SLOs**:
   - Availability SLO
   - Latency SLO (P95, P99)
   - Error rate SLO
   - Freshness SLO (model age)

2. **Implement SLO monitoring**:
   - Track SLI metrics in Prometheus
   - Calculate error budgets
   - Alert on budget exhaustion

3. **Create SLO dashboard**:
   - Current performance vs. SLO
   - Error budget remaining
   - Historical trends

4. **Error budget policy**:
   - Define response when budget depleted
   - Automatic freeze on deployments
   - Escalation procedures

### Starter Code

```python
# slo_monitor.py
"""SLO/SLI monitoring and error budget tracking."""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import prometheus_client as prom
from prometheus_client import Counter, Histogram, Gauge
import logging

@dataclass
class SLI:
    """Service Level Indicator definition."""
    name: str
    description: str
    metric_name: str  # Prometheus metric name
    query: str  # PromQL query
    unit: str  # e.g., "ms", "%", "count"

@dataclass
class SLO:
    """Service Level Objective definition."""
    name: str
    sli: SLI
    target: float  # e.g., 99.9 for 99.9%
    window_days: int  # Rolling window, e.g., 30 days

class SLOMonitor:
    """Monitor SLOs and track error budgets."""

    def __init__(self, slos: List[SLO], prometheus_url: str = "http://localhost:9090"):
        """
        Initialize SLO monitor.

        Args:
            slos: List of SLO definitions
            prometheus_url: Prometheus server URL
        """
        self.slos = slos
        self.prometheus_url = prometheus_url

        # TODO: Initialize Prometheus client
        # from prometheus_api_client import PrometheusConnect
        # self.prom = PrometheusConnect(url=prometheus_url, disable_ssl=True)

        # Initialize metrics
        self._init_metrics()

    def _init_metrics(self):
        """Initialize Prometheus metrics for SLO tracking."""

        # TODO: Create error budget gauges
        # self.error_budget_gauge = Gauge(
        #     'slo_error_budget_remaining_percent',
        #     'Remaining error budget percentage',
        #     ['slo_name']
        # )

        # self.slo_compliance_gauge = Gauge(
        #     'slo_compliance_percent',
        #     'Current SLO compliance percentage',
        #     ['slo_name']
        # )

        pass

    def calculate_error_budget(
        self,
        slo: SLO,
        total_requests: int,
        failed_requests: int
    ) -> dict:
        """
        Calculate error budget for an SLO.

        TODO: Implement error budget calculation

        Formula:
          allowed_failure_rate = (100 - slo_target) / 100
          allowed_failures = total_requests * allowed_failure_rate
          actual_failure_rate = failed_requests / total_requests
          remaining_budget = allowed_failures - failed_requests
          budget_pct = (remaining_budget / allowed_failures) * 100

        Args:
            slo: Service Level Objective
            total_requests: Total requests in window
            failed_requests: Failed requests in window

        Returns:
            Error budget status dictionary
        """

        # TODO: Calculate allowed failures
        # allowed_failure_rate = (100 - slo.target) / 100
        # allowed_failures = int(total_requests * allowed_failure_rate)

        # TODO: Calculate actual failure rate
        # actual_failure_rate = (failed_requests / total_requests * 100) if total_requests > 0 else 0

        # TODO: Calculate remaining budget
        # remaining_failures = allowed_failures - failed_requests
        # budget_remaining_pct = (remaining_failures / allowed_failures * 100) if allowed_failures > 0 else 0

        # TODO: Determine status
        # if budget_remaining_pct <= 0:
        #     status = "EXHAUSTED"
        # elif budget_remaining_pct < 25:
        #     status = "CRITICAL"
        # elif budget_remaining_pct < 50:
        #     status = "WARNING"
        # else:
        #     status = "HEALTHY"

        # return {
        #     'slo_name': slo.name,
        #     'target': slo.target,
        #     'window_days': slo.window_days,
        #     'total_requests': total_requests,
        #     'failed_requests': failed_requests,
        #     'allowed_failures': allowed_failures,
        #     'actual_failure_rate': round(actual_failure_rate, 4),
        #     'target_failure_rate': round(allowed_failure_rate * 100, 4),
        #     'remaining_failures': remaining_failures,
        #     'budget_remaining_pct': round(budget_remaining_pct, 2),
        #     'status': status,
        #     'budget_exhausted': remaining_failures <= 0
        # }

        pass

    def check_slo_compliance(self, slo: SLO) -> dict:
        """
        Check if SLO is currently being met.

        TODO: Query Prometheus for current metrics
        - Execute PromQL query
        - Compare against target
        - Calculate compliance percentage
        """

        # TODO: Query Prometheus
        # end_time = datetime.now()
        # start_time = end_time - timedelta(days=slo.window_days)

        # try:
        #     # Execute PromQL query
        #     result = self.prom.custom_query(slo.sli.query)

        #     if not result:
        #         return {
        #             'slo_name': slo.name,
        #             'compliant': False,
        #             'error': 'No data available'
        #         }

        #     # Parse result
        #     current_value = float(result[0]['value'][1])

        #     # Check compliance
        #     compliant = current_value >= slo.target

        #     return {
        #         'slo_name': slo.name,
        #         'target': slo.target,
        #         'current_value': round(current_value, 4),
        #         'compliant': compliant,
        #         'gap': round(current_value - slo.target, 4)
        #     }

        # except Exception as e:
        #     logging.error(f"Error checking SLO {slo.name}: {e}")
        #     return {
        #         'slo_name': slo.name,
        #         'compliant': False,
        #         'error': str(e)
        #     }

        pass

    def get_latency_sli(self, percentile: int = 95, window_minutes: int = 60) -> float:
        """
        Get latency SLI (e.g., P95 latency).

        TODO: Query Prometheus for latency percentile

        PromQL query example:
          histogram_quantile(0.95,
            rate(prediction_latency_bucket[5m])
          )
        """

        # TODO: Build PromQL query
        # query = f"""
        #     histogram_quantile(
        #         {percentile / 100},
        #         rate(prediction_latency_bucket[{window_minutes}m])
        #     )
        # """

        # TODO: Execute query and return result
        # try:
        #     result = self.prom.custom_query(query)
        #     latency_ms = float(result[0]['value'][1]) * 1000  # Convert to ms
        #     return latency_ms
        # except Exception as e:
        #     logging.error(f"Error querying latency: {e}")
        #     return None

        pass

    def get_availability_sli(self, window_minutes: int = 60) -> float:
        """
        Get availability SLI (% of successful requests).

        TODO: Calculate success rate from Prometheus

        PromQL query example:
          (sum(rate(prediction_total{status="success"}[5m])) /
           sum(rate(prediction_total[5m]))) * 100
        """

        # TODO: Build PromQL query
        # query = f"""
        #     (sum(rate(prediction_total{{status="success"}}[{window_minutes}m])) /
        #      sum(rate(prediction_total[{window_minutes}m]))) * 100
        # """

        # TODO: Execute query
        # try:
        #     result = self.prom.custom_query(query)
        #     availability = float(result[0]['value'][1])
        #     return availability
        # except Exception as e:
        #     logging.error(f"Error querying availability: {e}")
        #     return None

        pass

    def check_all_slos(self) -> Dict[str, dict]:
        """
        Check all SLOs and return status.

        TODO: Check each SLO and calculate error budgets
        """

        results = {}

        for slo in self.slos:
            # TODO: Check compliance
            # compliance = self.check_slo_compliance(slo)

            # TODO: Get metrics for error budget calculation
            # if slo.name == "availability":
            #     total_requests = self._get_total_requests(slo.window_days)
            #     failed_requests = self._get_failed_requests(slo.window_days)
            #     error_budget = self.calculate_error_budget(slo, total_requests, failed_requests)
            # else:
            #     error_budget = None

            # results[slo.name] = {
            #     'compliance': compliance,
            #     'error_budget': error_budget
            # }

            # TODO: Update Prometheus metrics
            # if error_budget:
            #     self.error_budget_gauge.labels(slo_name=slo.name).set(
            #         error_budget['budget_remaining_pct']
            #     )
            # self.slo_compliance_gauge.labels(slo_name=slo.name).set(
            #     compliance['current_value']
            # )

            pass

        return results

    def _get_total_requests(self, window_days: int) -> int:
        """Get total requests in window."""
        # TODO: Query Prometheus for total requests
        # query = f"sum(increase(prediction_total[{window_days}d]))"
        # result = self.prom.custom_query(query)
        # return int(float(result[0]['value'][1]))
        return 1000000  # Placeholder

    def _get_failed_requests(self, window_days: int) -> int:
        """Get failed requests in window."""
        # TODO: Query Prometheus for failed requests
        # query = f"sum(increase(prediction_total{{status='error'}}[{window_days}d]))"
        # result = self.prom.custom_query(query)
        # return int(float(result[0]['value'][1]))
        return 100  # Placeholder

    def generate_slo_report(self) -> str:
        """
        Generate SLO compliance report.

        TODO: Create formatted report with all SLOs
        """

        results = self.check_all_slos()

        report = [
            "="*70,
            "SLO COMPLIANCE REPORT",
            "="*70,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ""
        ]

        # TODO: Add each SLO to report
        # for slo_name, data in results.items():
        #     compliance = data['compliance']
        #     error_budget = data['error_budget']

        #     report.append(f"\n{slo_name.upper()}")
        #     report.append("-" * 70)
        #     report.append(f"Target: {compliance['target']}%")
        #     report.append(f"Current: {compliance['current_value']}%")
        #     report.append(f"Status: {'✅ COMPLIANT' if compliance['compliant'] else '❌ NON-COMPLIANT'}")

        #     if error_budget:
        #         report.append(f"\nError Budget:")
        #         report.append(f"  Status: {error_budget['status']}")
        #         report.append(f"  Remaining: {error_budget['budget_remaining_pct']:.2f}%")
        #         report.append(f"  Failed Requests: {error_budget['failed_requests']:,} / {error_budget['allowed_failures']:,}")

        return "\n".join(report)


# Define SLOs
availability_sli = SLI(
    name="availability",
    description="Percentage of successful predictions",
    metric_name="prediction_total",
    query="(sum(rate(prediction_total{status='success'}[5m])) / sum(rate(prediction_total[5m]))) * 100",
    unit="%"
)

availability_slo = SLO(
    name="availability",
    sli=availability_sli,
    target=99.9,  # 99.9% availability
    window_days=30
)

latency_sli = SLI(
    name="latency_p95",
    description="95th percentile prediction latency",
    metric_name="prediction_latency",
    query="histogram_quantile(0.95, rate(prediction_latency_bucket[5m]))",
    unit="ms"
)

latency_slo = SLO(
    name="latency_p95",
    sli=latency_sli,
    target=100,  # P95 < 100ms
    window_days=30
)

# Usage
if __name__ == '__main__':
    monitor = SLOMonitor(
        slos=[availability_slo, latency_slo],
        prometheus_url="http://localhost:9090"
    )

    # Check all SLOs
    results = monitor.check_all_slos()

    # Generate report
    report = monitor.generate_slo_report()
    print(report)

    # Example error budget calculation
    budget = monitor.calculate_error_budget(
        slo=availability_slo,
        total_requests=1000000,
        failed_requests=500
    )

    print(f"\nError Budget Status: {budget['status']}")
    print(f"Budget Remaining: {budget['budget_remaining_pct']:.2f}%")
    print(f"Failed Requests: {budget['failed_requests']:,} / {budget['allowed_failures']:,}")
```

### Prometheus Alert Rules

```yaml
# prometheus_alerts.yml
"""
Prometheus alert rules for SLO monitoring.

TODO: Add alert rules for:
- Error budget exhaustion
- SLO violations
- Critical budget depletion
"""

groups:
  - name: slo_alerts
    interval: 1m
    rules:
      # Availability SLO alert
      - alert: SLOAvailabilityViolation
        expr: |
          (sum(rate(prediction_total{status="success"}[5m])) /
           sum(rate(prediction_total[5m]))) * 100 < 99.9
        for: 5m
        labels:
          severity: critical
          slo: availability
        annotations:
          summary: "Availability SLO violated"
          description: "Availability is {{ $value }}%, below 99.9% target"

      # Latency SLO alert
      - alert: SLOLatencyViolation
        expr: |
          histogram_quantile(0.95,
            rate(prediction_latency_bucket[5m])
          ) * 1000 > 100
        for: 5m
        labels:
          severity: warning
          slo: latency
        annotations:
          summary: "Latency SLO violated"
          description: "P95 latency is {{ $value }}ms, above 100ms target"

      # Error budget depletion
      - alert: ErrorBudgetCritical
        expr: slo_error_budget_remaining_percent < 25
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Error budget critically low"
          description: "Only {{ $value }}% error budget remaining for {{ $labels.slo_name }}"

      # Error budget exhausted
      - alert: ErrorBudgetExhausted
        expr: slo_error_budget_remaining_percent <= 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Error budget exhausted"
          description: "Error budget exhausted for {{ $labels.slo_name }} - halt deployments"
```

### Success Criteria

- [ ] SLIs and SLOs correctly defined
- [ ] Error budget calculation accurate
- [ ] Prometheus metrics instrumented
- [ ] Alert rules configured
- [ ] SLO report generated
- [ ] Budget status tracking works

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Error Budget Formula**: `allowed_failures = total_requests * (1 - target/100)`
2. **Availability**: Use success rate over total requests
3. **Latency**: Use histogram_quantile for percentiles
4. **Window**: Use rolling window (e.g., 30 days) not calendar month
5. **Alerts**: Alert when budget < 25% and when exhausted
6. **PromQL**: Use `rate()` for counters, `histogram_quantile()` for latency

</details>

---
