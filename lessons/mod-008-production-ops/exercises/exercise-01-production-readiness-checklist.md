## Exercise 1: Production Readiness Checklist (75 minutes)

**Objective**: Implement a comprehensive production readiness assessment system that validates models before deployment.

### Background

Before deploying any ML model to production, you must verify it meets operational standards:
- Performance requirements (latency, throughput)
- Reliability requirements (error handling, retries)
- Monitoring and observability
- Security and compliance
- Documentation and runbooks

### Tasks

1. **Create production readiness checker**:
   - Implement automated checks for all categories
   - Generate detailed reports
   - Identify blocking vs. warning issues

2. **Implement performance validation**:
   - Latency testing (P50, P95, P99)
   - Throughput capacity testing
   - Resource usage profiling

3. **Add monitoring validation**:
   - Verify metrics are instrumented
   - Check logging configuration
   - Validate alert definitions

4. **Generate deployment report**:
   - Summary of all checks
   - Recommendations for improvements
   - Go/no-go decision

### Starter Code

```python
# production_readiness.py
"""Production readiness assessment for ML models."""

import time
import numpy as np
import requests
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import mlflow
import logging

class CheckStatus(Enum):
    """Status of a readiness check."""
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    NOT_APPLICABLE = "n/a"

@dataclass
class ReadinessCheck:
    """Single production readiness check."""
    category: str
    check_name: str
    status: CheckStatus
    details: str
    blocker: bool = False
    recommendation: Optional[str] = None

class ProductionReadinessChecker:
    """Comprehensive production readiness assessment."""

    def __init__(self, model_uri: str, deployment_config: dict):
        """
        Initialize readiness checker.

        Args:
            model_uri: MLflow model URI (e.g., "models:/model-name/staging")
            deployment_config: Configuration with SLOs and service details
        """
        self.model_uri = model_uri
        self.deployment_config = deployment_config
        self.checks: List[ReadinessCheck] = []
        self.model = None

    def run_all_checks(self) -> dict:
        """
        Run all production readiness checks.

        TODO: Implement comprehensive check suite
        - Performance checks
        - Reliability checks
        - Monitoring checks
        - Security checks
        - Documentation checks
        """
        logging.info(f"Running production readiness checks for {self.model_uri}")

        # TODO: Load model
        # try:
        #     self.model = mlflow.pyfunc.load_model(self.model_uri)
        # except Exception as e:
        #     self.checks.append(ReadinessCheck(
        #         category="Model Loading",
        #         check_name="Model Load",
        #         status=CheckStatus.FAIL,
        #         details=f"Failed to load model: {str(e)}",
        #         blocker=True
        #     ))
        #     return self._generate_summary()

        # Performance checks
        self._check_latency_requirements()
        self._check_throughput_capacity()
        self._check_resource_limits()
        self._check_model_size()

        # Reliability checks
        self._check_error_handling()
        self._check_input_validation()
        self._check_retry_logic()
        self._check_circuit_breakers()

        # Monitoring checks
        self._check_metrics_instrumentation()
        self._check_logging_configuration()
        self._check_alerting_setup()
        self._check_dashboards()

        # Security checks
        self._check_authentication()
        self._check_authorization()
        self._check_secrets_management()
        self._check_input_sanitization()

        # Data checks
        self._check_feature_validation()
        self._check_drift_monitoring()
        self._check_data_versioning()

        # Documentation checks
        self._check_runbook_exists()
        self._check_slos_defined()
        self._check_api_documentation()

        return self._generate_summary()

    def _check_latency_requirements(self):
        """
        Check if model meets latency SLO.

        TODO: Implement latency testing
        - Measure P50, P95, P99 latency
        - Compare against SLO
        - Test with realistic inputs
        """
        if not self.model:
            return

        sample_input = self._get_sample_input()
        latencies = []

        # TODO: Run latency tests
        for i in range(100):
            # TODO: Measure prediction latency
            # start = time.time()
            # try:
            #     self.model.predict(sample_input)
            #     latency = time.time() - start
            #     latencies.append(latency)
            # except Exception as e:
            #     logging.error(f"Prediction failed: {e}")
            pass

        # TODO: Calculate percentiles
        # p50_latency = np.percentile(latencies, 50) * 1000  # Convert to ms
        # p95_latency = np.percentile(latencies, 95) * 1000
        # p99_latency = np.percentile(latencies, 99) * 1000

        # TODO: Compare against SLO
        # slo_latency_ms = self.deployment_config.get('latency_slo_ms', 100)

        # if p99_latency <= slo_latency_ms:
        #     status = CheckStatus.PASS
        #     details = f"P99 latency {p99_latency:.1f}ms meets SLO ({slo_latency_ms}ms)"
        #     recommendation = None
        # elif p95_latency <= slo_latency_ms:
        #     status = CheckStatus.WARNING
        #     details = f"P95 meets SLO but P99 ({p99_latency:.1f}ms) exceeds SLO ({slo_latency_ms}ms)"
        #     recommendation = "Consider model optimization or increased resources"
        # else:
        #     status = CheckStatus.FAIL
        #     details = f"P95 latency {p95_latency:.1f}ms exceeds SLO ({slo_latency_ms}ms)"
        #     recommendation = "Model optimization required before production deployment"

        # self.checks.append(ReadinessCheck(
        #     category="Performance",
        #     check_name="Latency SLO",
        #     status=status,
        #     details=details,
        #     blocker=(status == CheckStatus.FAIL),
        #     recommendation=recommendation
        # ))

        pass

    def _check_throughput_capacity(self):
        """
        Check if model can handle expected throughput.

        TODO: Implement throughput testing
        - Calculate max QPS per replica
        - Compare against expected load
        - Account for safety margin
        """
        if not self.model:
            return

        # TODO: Measure average latency
        # avg_latency_s = self._measure_average_latency()

        # TODO: Calculate max QPS (with 70% utilization for safety)
        # max_qps = int((1 / avg_latency_s) * 0.7)

        # TODO: Get expected QPS from config
        # expected_qps = self.deployment_config.get('expected_qps', 100)

        # TODO: Compare and generate check result
        # if max_qps >= expected_qps:
        #     status = CheckStatus.PASS
        #     details = f"Single replica capacity {max_qps} QPS >= expected {expected_qps} QPS"
        # else:
        #     status = CheckStatus.WARNING
        #     details = f"Single replica capacity {max_qps} QPS < expected {expected_qps} QPS"
        #     recommendation = f"Deploy {int(np.ceil(expected_qps / max_qps))} replicas minimum"

        pass

    def _check_resource_limits(self):
        """
        Check resource limit configuration.

        TODO: Verify CPU and memory limits are set
        """
        k8s_config = self.deployment_config.get('kubernetes', {})

        # TODO: Check if resource limits are defined
        # resources = k8s_config.get('resources', {})
        # limits = resources.get('limits', {})
        # requests = resources.get('requests', {})

        # if not limits or not requests:
        #     self.checks.append(ReadinessCheck(
        #         category="Performance",
        #         check_name="Resource Limits",
        #         status=CheckStatus.FAIL,
        #         details="Resource limits and requests not configured",
        #         blocker=True,
        #         recommendation="Configure resource limits to prevent OOM and CPU throttling"
        #     ))
        # elif 'memory' not in limits or 'cpu' not in limits:
        #     self.checks.append(ReadinessCheck(
        #         category="Performance",
        #         check_name="Resource Limits",
        #         status=CheckStatus.WARNING,
        #         details="Incomplete resource limits",
        #         blocker=False,
        #         recommendation="Set both CPU and memory limits"
        #     ))
        # else:
        #     self.checks.append(ReadinessCheck(
        #         category="Performance",
        #         check_name="Resource Limits",
        #         status=CheckStatus.PASS,
        #         details=f"Resources configured: {limits}",
        #         blocker=False
        #     ))

        pass

    def _check_model_size(self):
        """
        Check model size is reasonable for deployment.

        TODO: Verify model artifact size
        """
        # TODO: Get model size from MLflow
        # client = mlflow.tracking.MlflowClient()
        # run_id = self._get_model_run_id()
        # artifacts = client.list_artifacts(run_id)

        # TODO: Calculate total size
        # total_size_mb = sum(artifact.file_size for artifact in artifacts) / (1024 * 1024)

        # TODO: Check against threshold
        # max_size_mb = self.deployment_config.get('max_model_size_mb', 1000)

        # if total_size_mb > max_size_mb:
        #     recommendation = "Consider model compression or quantization"
        # else:
        #     recommendation = None

        pass

    def _check_metrics_instrumentation(self):
        """
        Check if service exposes Prometheus metrics.

        TODO: Verify metrics endpoint and required metrics
        """
        service_url = self.deployment_config.get('service_url')

        if not service_url:
            self.checks.append(ReadinessCheck(
                category="Monitoring",
                check_name="Metrics Instrumentation",
                status=CheckStatus.NOT_APPLICABLE,
                details="Service URL not configured",
                blocker=False
            ))
            return

        # TODO: Check metrics endpoint
        # try:
        #     response = requests.get(f"{service_url}/metrics", timeout=5)
        #     metrics_text = response.text

        #     required_metrics = [
        #         'prediction_latency',
        #         'prediction_total',
        #         'prediction_errors_total',
        #         'model_version'
        #     ]

        #     missing_metrics = [m for m in required_metrics if m not in metrics_text]

        #     if not missing_metrics:
        #         status = CheckStatus.PASS
        #         details = "All required metrics instrumented"
        #     else:
        #         status = CheckStatus.FAIL
        #         details = f"Missing metrics: {', '.join(missing_metrics)}"

        # except Exception as e:
        #     status = CheckStatus.FAIL
        #     details = f"Failed to check metrics: {str(e)}"

        # self.checks.append(ReadinessCheck(
        #     category="Monitoring",
        #     check_name="Metrics Instrumentation",
        #     status=status,
        #     details=details,
        #     blocker=(status == CheckStatus.FAIL)
        # ))

        pass

    def _check_alerting_setup(self):
        """
        Check if alerts are configured.

        TODO: Verify alert rules exist
        """
        alerts_config = self.deployment_config.get('alerts', [])

        required_alerts = [
            'high_error_rate',
            'high_latency',
            'low_availability'
        ]

        # TODO: Check configured alerts
        # configured_alerts = [alert['name'] for alert in alerts_config]
        # missing_alerts = [a for a in required_alerts if a not in configured_alerts]

        # if not missing_alerts:
        #     status = CheckStatus.PASS
        #     details = f"{len(configured_alerts)} alerts configured"
        # else:
        #     status = CheckStatus.WARNING
        #     details = f"Missing alerts: {', '.join(missing_alerts)}"

        pass

    def _check_runbook_exists(self):
        """
        Check if operational runbook exists.

        TODO: Verify runbook documentation
        """
        import os

        runbook_path = self.deployment_config.get('runbook_path')

        if not runbook_path:
            self.checks.append(ReadinessCheck(
                category="Documentation",
                check_name="Runbook",
                status=CheckStatus.WARNING,
                details="No runbook path configured",
                blocker=False,
                recommendation="Create operational runbook for incident response"
            ))
        elif not os.path.exists(runbook_path):
            self.checks.append(ReadinessCheck(
                category="Documentation",
                check_name="Runbook",
                status=CheckStatus.WARNING,
                details=f"Runbook not found at {runbook_path}",
                blocker=False,
                recommendation="Create runbook before production deployment"
            ))
        else:
            # TODO: Check runbook completeness
            # with open(runbook_path) as f:
            #     content = f.read()
            #     required_sections = ['Deployment', 'Monitoring', 'Incident Response', 'Rollback']
            #     missing_sections = [s for s in required_sections if s not in content]

            self.checks.append(ReadinessCheck(
                category="Documentation",
                check_name="Runbook",
                status=CheckStatus.PASS,
                details=f"Runbook exists at {runbook_path}",
                blocker=False
            ))

    def _check_slos_defined(self):
        """
        Check if SLOs are defined.

        TODO: Verify SLO configuration
        """
        slos = self.deployment_config.get('slos', {})

        required_slos = ['availability', 'latency', 'error_rate']

        # TODO: Check SLO definitions
        # defined_slos = list(slos.keys())
        # missing_slos = [s for s in required_slos if s not in defined_slos]

        # if not missing_slos:
        #     status = CheckStatus.PASS
        #     details = f"All required SLOs defined: {defined_slos}"
        # else:
        #     status = CheckStatus.FAIL
        #     details = f"Missing SLOs: {missing_slos}"

        pass

    def _check_error_handling(self):
        """Check error handling implementation."""
        # TODO: Verify error handling for common scenarios
        pass

    def _check_input_validation(self):
        """Check input validation implementation."""
        # TODO: Verify input validation and sanitization
        pass

    def _check_retry_logic(self):
        """Check retry configuration."""
        # TODO: Verify retry logic for transient failures
        pass

    def _check_circuit_breakers(self):
        """Check circuit breaker implementation."""
        # TODO: Verify circuit breaker for downstream dependencies
        pass

    def _check_logging_configuration(self):
        """Check logging configuration."""
        # TODO: Verify structured logging is implemented
        pass

    def _check_dashboards(self):
        """Check if monitoring dashboards exist."""
        # TODO: Verify Grafana/monitoring dashboards
        pass

    def _check_authentication(self):
        """Check authentication implementation."""
        # TODO: Verify API authentication
        pass

    def _check_authorization(self):
        """Check authorization implementation."""
        # TODO: Verify role-based access control
        pass

    def _check_secrets_management(self):
        """Check secrets management."""
        # TODO: Verify secrets are not hardcoded
        pass

    def _check_input_sanitization(self):
        """Check input sanitization."""
        # TODO: Verify protection against injection attacks
        pass

    def _check_feature_validation(self):
        """Check feature validation."""
        # TODO: Verify feature schema validation
        pass

    def _check_drift_monitoring(self):
        """Check drift monitoring setup."""
        # TODO: Verify drift detection is configured
        pass

    def _check_data_versioning(self):
        """Check data versioning."""
        # TODO: Verify data lineage tracking
        pass

    def _check_api_documentation(self):
        """Check API documentation."""
        # TODO: Verify API documentation exists (OpenAPI/Swagger)
        pass

    def _get_sample_input(self):
        """Get sample input for testing."""
        # TODO: Generate or load representative sample data
        return np.random.randn(1, 10)  # Placeholder

    def _measure_average_latency(self) -> float:
        """Measure average prediction latency."""
        # TODO: Implement latency measurement
        return 0.05  # Placeholder

    def _generate_summary(self) -> dict:
        """
        Generate readiness summary.

        Returns:
            Summary with go/no-go decision
        """
        blockers = [c for c in self.checks if c.blocker and c.status == CheckStatus.FAIL]
        warnings = [c for c in self.checks if c.status == CheckStatus.WARNING]
        passed = [c for c in self.checks if c.status == CheckStatus.PASS]
        failed = [c for c in self.checks if c.status == CheckStatus.FAIL]

        ready_for_production = len(blockers) == 0

        return {
            'ready_for_production': ready_for_production,
            'decision': 'GO' if ready_for_production else 'NO-GO',
            'summary': {
                'total_checks': len(self.checks),
                'passed': len(passed),
                'warnings': len(warnings),
                'failed': len(failed),
                'blockers': len(blockers)
            },
            'blocker_details': [
                {
                    'category': c.category,
                    'check': c.check_name,
                    'details': c.details,
                    'recommendation': c.recommendation
                }
                for c in blockers
            ],
            'warnings': [
                {
                    'category': c.category,
                    'check': c.check_name,
                    'details': c.details,
                    'recommendation': c.recommendation
                }
                for c in warnings
            ],
            'all_checks': [
                {
                    'category': c.category,
                    'check': c.check_name,
                    'status': c.status.value,
                    'details': c.details,
                    'blocker': c.blocker,
                    'recommendation': c.recommendation
                }
                for c in self.checks
            ]
        }


# Usage example
if __name__ == '__main__':
    checker = ProductionReadinessChecker(
        model_uri="models:/credit-classifier/staging",
        deployment_config={
            'latency_slo_ms': 100,
            'expected_qps': 500,
            'max_model_size_mb': 500,
            'service_url': 'http://localhost:8000',
            'runbook_path': 'runbooks/credit_model.md',
            'kubernetes': {
                'resources': {
                    'requests': {'cpu': '1', 'memory': '2Gi'},
                    'limits': {'cpu': '2', 'memory': '4Gi'}
                }
            },
            'slos': {
                'availability': 99.9,
                'latency': 100,
                'error_rate': 0.1
            },
            'alerts': [
                {'name': 'high_error_rate'},
                {'name': 'high_latency'},
                {'name': 'low_availability'}
            ]
        }
    )

    results = checker.run_all_checks()

    print(f"\n{'='*60}")
    print(f"Production Readiness Assessment")
    print(f"{'='*60}")
    print(f"\nDecision: {results['decision']}")
    print(f"\nSummary:")
    print(f"  Total checks: {results['summary']['total_checks']}")
    print(f"  Passed: {results['summary']['passed']}")
    print(f"  Warnings: {results['summary']['warnings']}")
    print(f"  Failed: {results['summary']['failed']}")
    print(f"  Blockers: {results['summary']['blockers']}")

    if results['blocker_details']:
        print(f"\n🚫 Blocking Issues:")
        for blocker in results['blocker_details']:
            print(f"\n  [{blocker['category']}] {blocker['check']}")
            print(f"    {blocker['details']}")
            if blocker['recommendation']:
                print(f"    💡 {blocker['recommendation']}")

    if results['warnings']:
        print(f"\n⚠️  Warnings:")
        for warning in results['warnings']:
            print(f"\n  [{warning['category']}] {warning['check']}")
            print(f"    {warning['details']}")
            if warning['recommendation']:
                print(f"    💡 {warning['recommendation']}")
```

### Validation

Test your production readiness checker:

```python
# test_production_readiness.py
import pytest
from production_readiness import ProductionReadinessChecker, CheckStatus

def test_latency_check_passes_when_within_slo():
    """Test latency check passes when within SLO."""
    # TODO: Create checker with fast model
    # TODO: Run latency check
    # TODO: Assert status is PASS
    pass

def test_latency_check_fails_when_exceeds_slo():
    """Test latency check fails when exceeding SLO."""
    # TODO: Create checker with slow model
    # TODO: Run latency check
    # TODO: Assert status is FAIL
    pass

def test_missing_metrics_marked_as_blocker():
    """Test missing metrics are blocking issues."""
    # TODO: Create checker with no metrics endpoint
    # TODO: Run metrics check
    # TODO: Assert blocker=True
    pass

def test_summary_shows_no_go_with_blockers():
    """Test summary shows NO-GO when blockers present."""
    # TODO: Create checker with failing checks
    # TODO: Generate summary
    # TODO: Assert decision is NO-GO
    pass

# Run with: pytest test_production_readiness.py -v
```

### Success Criteria

- [ ] All check categories implemented
- [ ] Latency testing works correctly
- [ ] Blocker vs. warning distinction clear
- [ ] Summary generates go/no-go decision
- [ ] Recommendations provided for failures
- [ ] Tests pass

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Latency Testing**: Use percentiles (P50, P95, P99) not just average
2. **Sample Input**: Generate realistic test data matching production schema
3. **Metrics Endpoint**: Use requests library with timeout to check /metrics
4. **Categorization**: Group related checks (performance, monitoring, security)
5. **Blockers**: Mark critical checks (latency, metrics, security) as blockers
6. **Recommendations**: Provide actionable next steps for each failure

</details>

---
