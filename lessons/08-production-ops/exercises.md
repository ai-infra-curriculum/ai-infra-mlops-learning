# Module 08: Production ML Operations - Exercises

## Overview

This exercise set provides hands-on practice with production ML operations, covering:
- Production readiness assessment and checklists
- Capacity planning and resource management
- SLO/SLI definition and monitoring
- Incident response and management
- Auto-scaling and performance optimization

**Time Estimate**: 6-9 hours total

---

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

## Exercise 2: Capacity Planning & Resource Management (90 minutes)

**Objective**: Build a capacity planning system that calculates resource requirements based on traffic patterns and SLOs.

### Background

Proper capacity planning ensures:
- Models meet latency SLOs under load
- Resources are cost-optimized
- Auto-scaling is configured correctly
- Peak traffic is handled without degradation

### Tasks

1. **Implement capacity calculator**:
   - Calculate required replicas
   - Estimate CPU and memory needs
   - Account for redundancy (N+2)

2. **Build traffic analyzer**:
   - Analyze historical traffic patterns
   - Identify peak periods
   - Calculate growth projections

3. **Generate scaling strategy**:
   - Configure HPA (Horizontal Pod Autoscaler)
   - Set min/max replicas
   - Define scaling metrics and thresholds

4. **Cost estimation**:
   - Calculate monthly infrastructure costs
   - Cost per prediction
   - Cost optimization recommendations

### Starter Code

```python
# capacity_planner.py
"""Capacity planning for ML model serving."""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple
import pandas as pd
from datetime import datetime, timedelta

@dataclass
class ModelProfile:
    """Model performance profile."""
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    memory_mb: float
    cpu_cores: float

@dataclass
class TrafficProfile:
    """Traffic pattern profile."""
    avg_qps: float
    peak_qps: float
    peak_duration_hours: float
    daily_pattern: List[float]  # 24-hour QPS pattern

class CapacityPlanner:
    """Calculate resource requirements for ML serving."""

    def __init__(
        self,
        model_profile: ModelProfile,
        traffic_profile: TrafficProfile,
        target_availability: float = 99.9
    ):
        """
        Initialize capacity planner.

        Args:
            model_profile: Model performance characteristics
            traffic_profile: Expected traffic patterns
            target_availability: Target availability (e.g., 99.9 for three nines)
        """
        self.model_profile = model_profile
        self.traffic_profile = traffic_profile
        self.target_availability = target_availability

    def calculate_required_replicas(self, target_qps: float, target_latency_ms: float) -> dict:
        """
        Calculate number of replicas needed.

        TODO: Implement replica calculation
        - Calculate single replica capacity
        - Account for target utilization (70%)
        - Add redundancy for HA (N+2)

        Formula:
          single_replica_qps = (1000 / model_latency_ms) * target_utilization
          min_replicas = ceil(target_qps / single_replica_qps)
          recommended_replicas = min_replicas + redundancy
        """

        # TODO: Calculate single replica capacity
        # Use P95 latency for more conservative estimate
        # target_utilization = 0.7  # 70% utilization for headroom

        # single_replica_qps = (1000 / self.model_profile.p95_latency_ms) * target_utilization

        # TODO: Calculate minimum replicas for throughput
        # min_replicas = int(np.ceil(target_qps / single_replica_qps))

        # TODO: Add redundancy (N+2 for high availability)
        # redundancy = 2 if self.target_availability >= 99.9 else 1
        # recommended_replicas = min_replicas + redundancy

        # TODO: Calculate total capacity
        # total_capacity_qps = recommended_replicas * single_replica_qps

        # return {
        #     'target_qps': target_qps,
        #     'single_replica_capacity_qps': round(single_replica_qps, 2),
        #     'min_replicas': min_replicas,
        #     'recommended_replicas': recommended_replicas,
        #     'redundancy': redundancy,
        #     'total_capacity_qps': round(total_capacity_qps, 2),
        #     'headroom_pct': round(((total_capacity_qps - target_qps) / target_qps) * 100, 1)
        # }

        pass

    def calculate_memory_requirements(self, num_replicas: int) -> dict:
        """
        Calculate memory requirements.

        TODO: Implement memory calculation
        - Base model memory
        - Framework overhead (30-50%)
        - Request buffers
        - Total per replica and cluster
        """

        # TODO: Calculate per-replica memory
        # model_memory_mb = self.model_profile.memory_mb
        # overhead_multiplier = 1.5  # 50% overhead for framework, buffers, etc.
        # per_replica_mb = model_memory_mb * overhead_multiplier

        # TODO: Calculate total memory
        # total_memory_mb = per_replica_mb * num_replicas
        # total_memory_gb = total_memory_mb / 1024

        # TODO: Kubernetes resource recommendations
        # request_mb = int(per_replica_mb)
        # limit_mb = int(per_replica_mb * 1.2)  # 20% buffer for spikes

        # return {
        #     'model_memory_mb': model_memory_mb,
        #     'per_replica_mb': round(per_replica_mb, 1),
        #     'total_memory_mb': round(total_memory_mb, 1),
        #     'total_memory_gb': round(total_memory_gb, 2),
        #     'k8s_memory_request': f"{request_mb}Mi",
        #     'k8s_memory_limit': f"{limit_mb}Mi"
        # }

        pass

    def calculate_cpu_requirements(self, num_replicas: int) -> dict:
        """
        Calculate CPU requirements.

        TODO: Implement CPU calculation
        - Cores based on latency budget
        - Total cluster cores
        - Kubernetes resource requests/limits
        """

        # TODO: Calculate cores per replica
        # Rule of thumb: 1 core can handle ~10ms of compute efficiently
        # cores_per_replica = max(1.0, self.model_profile.cpu_cores)

        # TODO: Calculate total cores
        # total_cores = cores_per_replica * num_replicas

        # TODO: Kubernetes resource recommendations
        # request_cores = cores_per_replica
        # limit_cores = cores_per_replica * 1.5  # Allow bursting

        # return {
        #     'cores_per_replica': cores_per_replica,
        #     'total_cores': total_cores,
        #     'k8s_cpu_request': f"{request_cores}",
        #     'k8s_cpu_limit': f"{limit_cores}"
        # }

        pass

    def estimate_costs(self, num_replicas: int, cost_per_core_hour: float = 0.05) -> dict:
        """
        Estimate monthly infrastructure costs.

        TODO: Implement cost estimation
        - CPU costs
        - Memory costs
        - Total monthly cost
        - Cost per 1K predictions

        Assumptions:
          - Memory cost is ~25% of CPU cost
          - 730 hours per month
        """

        cpu_calc = self.calculate_cpu_requirements(num_replicas)
        mem_calc = self.calculate_memory_requirements(num_replicas)

        # TODO: Calculate monthly costs
        # hours_per_month = 730

        # Monthly CPU cost
        # monthly_cpu_cost = cpu_calc['total_cores'] * cost_per_core_hour * hours_per_month

        # Monthly memory cost (approximately 1/4 of CPU cost)
        # monthly_memory_cost = (mem_calc['total_memory_gb'] / 4) * cost_per_core_hour * hours_per_month

        # TODO: Total cost
        # total_monthly_cost = monthly_cpu_cost + monthly_memory_cost

        # TODO: Cost per prediction
        # total_monthly_predictions = self.traffic_profile.avg_qps * hours_per_month * 3600
        # cost_per_1k_predictions = (total_monthly_cost / total_monthly_predictions) * 1000

        # return {
        #     'monthly_cpu_cost': round(monthly_cpu_cost, 2),
        #     'monthly_memory_cost': round(monthly_memory_cost, 2),
        #     'total_monthly_cost': round(total_monthly_cost, 2),
        #     'cost_per_1k_predictions': round(cost_per_1k_predictions, 4),
        #     'assumptions': {
        #         'cost_per_core_hour': cost_per_core_hour,
        #         'hours_per_month': hours_per_month
        #     }
        # }

        pass

    def generate_autoscaling_config(self, base_replicas: int) -> dict:
        """
        Generate HPA (Horizontal Pod Autoscaler) configuration.

        TODO: Implement autoscaling configuration
        - Min/max replicas based on traffic patterns
        - Scaling metrics (CPU, memory, custom)
        - Scaling behavior (scale up/down rates)
        """

        # TODO: Calculate min/max based on traffic
        # min_replicas = max(2, int(base_replicas * 0.5))  # Never go below 50%
        # max_replicas = int(base_replicas * 2)  # Allow 2x scaling for spikes

        # TODO: Define scaling metrics
        # metrics = [
        #     {
        #         'type': 'Resource',
        #         'name': 'cpu',
        #         'target': 70  # Scale when CPU > 70%
        #     },
        #     {
        #         'type': 'Resource',
        #         'name': 'memory',
        #         'target': 80  # Scale when memory > 80%
        #     }
        # ]

        # TODO: Define scaling behavior
        # behavior = {
        #     'scaleUp': {
        #         'stabilizationWindowSeconds': 60,
        #         'policies': [
        #             {
        #                 'type': 'Percent',
        #                 'value': 50,  # Max 50% increase per minute
        #                 'periodSeconds': 60
        #             }
        #         ]
        #     },
        #     'scaleDown': {
        #         'stabilizationWindowSeconds': 300,  # 5 min stabilization
        #         'policies': [
        #             {
        #                 'type': 'Percent',
        #                 'value': 10,  # Max 10% decrease per minute
        #                 'periodSeconds': 60
        #             }
        #         ]
        #     }
        # }

        # return {
        #     'min_replicas': min_replicas,
        #     'max_replicas': max_replicas,
        #     'metrics': metrics,
        #     'behavior': behavior
        # }

        pass

    def analyze_traffic_pattern(self, historical_data: pd.DataFrame) -> dict:
        """
        Analyze historical traffic to identify patterns.

        TODO: Implement traffic analysis
        - Calculate daily/weekly patterns
        - Identify peak periods
        - Calculate growth trend
        """

        # Assumes historical_data has columns: timestamp, qps

        # TODO: Calculate statistics
        # avg_qps = historical_data['qps'].mean()
        # peak_qps = historical_data['qps'].quantile(0.99)  # P99 as peak
        # min_qps = historical_data['qps'].quantile(0.01)

        # TODO: Identify daily pattern
        # historical_data['hour'] = pd.to_datetime(historical_data['timestamp']).dt.hour
        # hourly_pattern = historical_data.groupby('hour')['qps'].mean().tolist()

        # TODO: Calculate growth rate (if data spans multiple months)
        # # Simple linear regression for trend
        # from scipy import stats
        # x = range(len(historical_data))
        # y = historical_data['qps'].values
        # slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        # monthly_growth_rate = (slope * 30 * 24 * 60) / avg_qps * 100  # % per month

        # return {
        #     'avg_qps': round(avg_qps, 2),
        #     'peak_qps': round(peak_qps, 2),
        #     'min_qps': round(min_qps, 2),
        #     'peak_to_avg_ratio': round(peak_qps / avg_qps, 2),
        #     'hourly_pattern': [round(x, 2) for x in hourly_pattern],
        #     'monthly_growth_rate_pct': round(monthly_growth_rate, 2)
        # }

        pass

    def generate_capacity_plan(self) -> dict:
        """
        Generate complete capacity plan.

        TODO: Combine all calculations into comprehensive plan
        """

        # TODO: Calculate for peak traffic
        # peak_qps = self.traffic_profile.peak_qps
        # target_latency = self.model_profile.p99_latency_ms

        # TODO: Get replica calculations
        # replica_calc = self.calculate_required_replicas(peak_qps, target_latency)
        # num_replicas = replica_calc['recommended_replicas']

        # TODO: Get resource calculations
        # cpu_calc = self.calculate_cpu_requirements(num_replicas)
        # mem_calc = self.calculate_memory_requirements(num_replicas)
        # cost_calc = self.estimate_costs(num_replicas)
        # hpa_config = self.generate_autoscaling_config(num_replicas)

        # return {
        #     'model_profile': {
        #         'p99_latency_ms': self.model_profile.p99_latency_ms,
        #         'memory_mb': self.model_profile.memory_mb
        #     },
        #     'traffic_profile': {
        #         'avg_qps': self.traffic_profile.avg_qps,
        #         'peak_qps': self.traffic_profile.peak_qps
        #     },
        #     'replicas': replica_calc,
        #     'cpu': cpu_calc,
        #     'memory': mem_calc,
        #     'costs': cost_calc,
        #     'autoscaling': hpa_config,
        #     'kubernetes_manifest': self._generate_k8s_manifest(
        #         num_replicas, cpu_calc, mem_calc, hpa_config
        #     )
        # }

        pass

    def _generate_k8s_manifest(
        self,
        replicas: int,
        cpu_calc: dict,
        mem_calc: dict,
        hpa_config: dict
    ) -> str:
        """Generate Kubernetes deployment and HPA manifests."""

        deployment = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model-serving
  labels:
    app: ml-model
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: ml-model
  template:
    metadata:
      labels:
        app: ml-model
    spec:
      containers:
      - name: model-server
        image: ml-model:latest
        resources:
          requests:
            cpu: "{cpu_calc['k8s_cpu_request']}"
            memory: "{mem_calc['k8s_memory_request']}"
          limits:
            cpu: "{cpu_calc['k8s_cpu_limit']}"
            memory: "{mem_calc['k8s_memory_limit']}"
        ports:
        - containerPort: 8000
          name: http
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-model-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-model-serving
  minReplicas: {hpa_config['min_replicas']}
  maxReplicas: {hpa_config['max_replicas']}
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
"""
        return deployment


# Usage example
if __name__ == '__main__':
    # Define model profile
    model_profile = ModelProfile(
        p50_latency_ms=30,
        p95_latency_ms=50,
        p99_latency_ms=75,
        memory_mb=500,
        cpu_cores=1.0
    )

    # Define traffic profile
    traffic_profile = TrafficProfile(
        avg_qps=500,
        peak_qps=1200,
        peak_duration_hours=4,
        daily_pattern=[100, 80, 60, 50, 60, 100, 200, 400, 600, 700,
                      750, 800, 850, 900, 850, 800, 750, 700, 600, 400,
                      300, 200, 150, 120]
    )

    # Create planner
    planner = CapacityPlanner(model_profile, traffic_profile, target_availability=99.9)

    # Generate capacity plan
    capacity_plan = planner.generate_capacity_plan()

    # Print report
    print("\n" + "="*70)
    print("CAPACITY PLANNING REPORT")
    print("="*70)

    print(f"\n📊 Traffic Profile:")
    print(f"  Average QPS: {traffic_profile.avg_qps}")
    print(f"  Peak QPS: {traffic_profile.peak_qps}")
    print(f"  Peak/Avg Ratio: {traffic_profile.peak_qps / traffic_profile.avg_qps:.2f}x")

    print(f"\n⚙️  Model Profile:")
    print(f"  P99 Latency: {model_profile.p99_latency_ms}ms")
    print(f"  Memory: {model_profile.memory_mb}MB")

    print(f"\n🖥️  Resource Requirements:")
    print(f"  Recommended Replicas: {capacity_plan['replicas']['recommended_replicas']}")
    print(f"  Total CPU Cores: {capacity_plan['cpu']['total_cores']}")
    print(f"  Total Memory: {capacity_plan['memory']['total_memory_gb']:.1f}GB")

    print(f"\n💰 Cost Estimation:")
    print(f"  Monthly Cost: ${capacity_plan['costs']['total_monthly_cost']:,.2f}")
    print(f"  Cost per 1K Predictions: ${capacity_plan['costs']['cost_per_1k_predictions']:.4f}")

    print(f"\n📈 Autoscaling Configuration:")
    print(f"  Min Replicas: {capacity_plan['autoscaling']['min_replicas']}")
    print(f"  Max Replicas: {capacity_plan['autoscaling']['max_replicas']}")

    # Save Kubernetes manifest
    with open('deployment.yaml', 'w') as f:
        f.write(capacity_plan['kubernetes_manifest'])
    print(f"\n✅ Kubernetes manifest saved to deployment.yaml")
```

### Validation

Test capacity calculations:

```python
# test_capacity_planner.py
import pytest
from capacity_planner import CapacityPlanner, ModelProfile, TrafficProfile

def test_replica_calculation_includes_redundancy():
    """Test that replica calculation includes N+2 for HA."""
    model = ModelProfile(p50_latency_ms=50, p95_latency_ms=75, p99_latency_ms=100, memory_mb=500, cpu_cores=1.0)
    traffic = TrafficProfile(avg_qps=100, peak_qps=200, peak_duration_hours=2, daily_pattern=[100]*24)

    planner = CapacityPlanner(model, traffic, target_availability=99.9)
    result = planner.calculate_required_replicas(200, 100)

    assert result['recommended_replicas'] >= result['min_replicas'] + 2

def test_memory_calculation_includes_overhead():
    """Test memory calculation includes framework overhead."""
    # TODO: Implement test
    pass

def test_cost_scales_with_replicas():
    """Test cost increases linearly with replicas."""
    # TODO: Implement test
    pass

def test_autoscaling_min_replicas_reasonable():
    """Test HPA min replicas is reasonable."""
    # TODO: Implement test
    pass
```

### Success Criteria

- [ ] Replica calculation accounts for redundancy
- [ ] Memory calculation includes overhead
- [ ] CPU calculation based on latency requirements
- [ ] Cost estimation realistic
- [ ] HPA configuration generated correctly
- [ ] Kubernetes manifest valid YAML
- [ ] Tests pass

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Replica Formula**: `replicas = ceil(target_qps / single_replica_qps) + redundancy`
2. **Utilization**: Target 70% utilization for headroom, not 100%
3. **Redundancy**: N+2 for 99.9% availability, N+1 for 99%
4. **Memory Overhead**: Add 50% for framework and buffers
5. **Autoscaling**: Min replicas = 50% of base, max = 200% of base
6. **Cost**: CPU cost dominates, memory ~25% of CPU cost

</details>

---

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

## Exercise 5: Complete Production Operations (120 minutes)

**Objective**: Integrate all production operations components into a comprehensive system.

### Requirements

Build a complete production operations system that includes:

1. **Pre-deployment validation**:
   - Production readiness check
   - Capacity verification
   - SLO compliance check

2. **Continuous monitoring**:
   - SLI/SLO tracking
   - Error budget monitoring
   - Incident detection

3. **Automated response**:
   - Auto-scaling
   - Circuit breakers
   - Automatic rollback

4. **Operational dashboards**:
   - Real-time metrics
   - SLO compliance
   - Incident history

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Production Operations                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │  Readiness   │───▶│   Capacity   │───▶│   Deploy     │ │
│  │   Checker    │    │   Planner    │    │   System     │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         │                    │                    │         │
│         ▼                    ▼                    ▼         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              SLO/SLI Monitoring                      │  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐   │  │
│  │  │ Avail. │  │Latency │  │ Error  │  │Quality │   │  │
│  │  │  SLO   │  │  SLO   │  │  SLO   │  │  SLO   │   │  │
│  │  └────────┘  └────────┘  └────────┘  └────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Incident Detection & Response              │  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐   │  │
│  │  │Detector│─▶│ Alert  │─▶│Remediate│─▶│Escalate│   │  │
│  │  └────────┘  └────────┘  └────────┘  └────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Tasks

1. Create integrated system
2. Add configuration management
3. Implement observability
4. Build operational dashboard
5. Create comprehensive documentation

### Success Criteria

- [ ] All components integrated
- [ ] End-to-end workflow tested
- [ ] Monitoring comprehensive
- [ ] Automated response working
- [ ] Documentation complete
- [ ] Dashboard functional

---

## Submission Guidelines

For each exercise, submit:
1. **Code**: All implementation files with TODOs completed
2. **Tests**: Unit and integration tests
3. **Documentation**: Architecture diagrams and runbooks
4. **Metrics**: Sample metrics and dashboards
5. **Reflection**: Lessons learned and improvements

**Estimated Total Time**: 6-9 hours
**Difficulty**: Advanced

Good luck!
