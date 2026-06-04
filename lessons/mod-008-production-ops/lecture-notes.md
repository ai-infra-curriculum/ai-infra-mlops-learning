# Module 08: Production Operations - Lecture Notes

**Duration**: 14 hours
**Level**: MLOps Engineer (2.5B)
**Last Updated**: October 2025

---

## Table of Contents

1. [Production Readiness](#1-production-readiness)
2. [Capacity Planning](#2-capacity-planning)
3. [Performance Optimization](#3-performance-optimization)
4. [Reliability Engineering](#4-reliability-engineering)
5. [Incident Management](#5-incident-management)
6. [Operational Excellence](#6-operational-excellence)
7. [Summary and Best Practices](#7-summary-and-best-practices)

---

## 1. Production Readiness

### 1.1 Comprehensive Production Readiness Checklist

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class CheckStatus(Enum):
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

class ProductionReadinessChecklist:
    """Comprehensive production readiness assessment."""

    def __init__(self, model_uri: str, deployment_config: dict):
        self.model_uri = model_uri
        self.deployment_config = deployment_config
        self.checks: List[ReadinessCheck] = []

    def run_all_checks(self) -> dict:
        """Run all production readiness checks."""

        # Performance checks
        self._check_latency_requirements()
        self._check_throughput_capacity()
        self._check_resource_limits()

        # Reliability checks
        self._check_error_handling()
        self._check_retry_logic()
        self._check_circuit_breakers()

        # Monitoring checks
        self._check_metrics_instrumentation()
        self._check_logging_configuration()
        self._check_alerting_setup()

        # Security checks
        self._check_authentication()
        self._check_input_validation()
        self._check_secrets_management()

        # Data checks
        self._check_feature_validation()
        self._check_drift_monitoring()

        # Documentation checks
        self._check_runbook_exists()
        self._check_slos_defined()

        # Generate summary
        return self._generate_summary()

    def _check_latency_requirements(self):
        """Check if latency meets SLO."""
        import mlflow
        import time

        model = mlflow.pyfunc.load_model(self.model_uri)

        # Test latency with sample input
        sample_input = self._get_sample_input()

        latencies = []
        for _ in range(100):
            start = time.time()
            model.predict(sample_input)
            latencies.append(time.time() - start)

        p95_latency = np.percentile(latencies, 95)
        p99_latency = np.percentile(latencies, 99)

        slo_latency = self.deployment_config.get('latency_slo_ms', 100) / 1000

        if p99_latency <= slo_latency:
            status = CheckStatus.PASS
            details = f"P99 latency {p99_latency*1000:.1f}ms (SLO: {slo_latency*1000:.1f}ms)"
        else:
            status = CheckStatus.FAIL
            details = f"P99 latency {p99_latency*1000:.1f}ms exceeds SLO {slo_latency*1000:.1f}ms"

        self.checks.append(ReadinessCheck(
            category="Performance",
            check_name="Latency SLO",
            status=status,
            details=details,
            blocker=True
        ))

    def _check_throughput_capacity(self):
        """Check throughput capacity."""
        expected_qps = self.deployment_config.get('expected_qps', 100)

        # In production: use load testing results
        # For now: estimate based on latency
        max_qps = int(1 / np.mean(self._measure_latency()) * 0.8)  # 80% utilization

        if max_qps >= expected_qps:
            status = CheckStatus.PASS
            details = f"Capacity {max_qps} QPS >= expected {expected_qps} QPS"
        else:
            status = CheckStatus.FAIL
            details = f"Capacity {max_qps} QPS < expected {expected_qps} QPS"

        self.checks.append(ReadinessCheck(
            category="Performance",
            check_name="Throughput Capacity",
            status=status,
            details=details,
            blocker=True
        ))

    def _check_metrics_instrumentation(self):
        """Check Prometheus metrics are exposed."""
        import requests

        try:
            # Check if metrics endpoint exists
            response = requests.get(
                f"{self.deployment_config.get('service_url')}/metrics",
                timeout=5
            )

            required_metrics = [
                'prediction_latency',
                'prediction_total',
                'prediction_errors_total'
            ]

            metrics_text = response.text
            missing_metrics = [
                m for m in required_metrics
                if m not in metrics_text
            ]

            if not missing_metrics:
                status = CheckStatus.PASS
                details = "All required metrics instrumented"
            else:
                status = CheckStatus.FAIL
                details = f"Missing metrics: {missing_metrics}"

            self.checks.append(ReadinessCheck(
                category="Monitoring",
                check_name="Metrics Instrumentation",
                status=status,
                details=details,
                blocker=True
            ))

        except Exception as e:
            self.checks.append(ReadinessCheck(
                category="Monitoring",
                check_name="Metrics Instrumentation",
                status=CheckStatus.FAIL,
                details=f"Error checking metrics: {str(e)}",
                blocker=True
            ))

    def _check_runbook_exists(self):
        """Check operational runbook exists."""
        runbook_path = self.deployment_config.get('runbook_path')

        if runbook_path and os.path.exists(runbook_path):
            status = CheckStatus.PASS
            details = f"Runbook found at {runbook_path}"
        else:
            status = CheckStatus.WARNING
            details = "No runbook found"

        self.checks.append(ReadinessCheck(
            category="Documentation",
            check_name="Runbook Exists",
            status=status,
            details=details,
            blocker=False
        ))

    def _generate_summary(self) -> dict:
        """Generate readiness summary."""

        blockers = [c for c in self.checks if c.blocker and c.status == CheckStatus.FAIL]
        warnings = [c for c in self.checks if c.status == CheckStatus.WARNING]
        passed = [c for c in self.checks if c.status == CheckStatus.PASS]

        ready_for_production = len(blockers) == 0

        return {
            'ready_for_production': ready_for_production,
            'total_checks': len(self.checks),
            'passed': len(passed),
            'warnings': len(warnings),
            'blockers': len(blockers),
            'blocker_details': [
                {'check': c.check_name, 'details': c.details}
                for c in blockers
            ],
            'all_checks': [
                {
                    'category': c.category,
                    'check': c.check_name,
                    'status': c.status.value,
                    'details': c.details
                }
                for c in self.checks
            ]
        }

# Usage
checklist = ProductionReadinessChecklist(
    model_uri="models:/credit-model/staging",
    deployment_config={
        'latency_slo_ms': 100,
        'expected_qps': 500,
        'service_url': 'http://model-service:8000',
        'runbook_path': 'runbooks/credit_model.md'
    }
)

results = checklist.run_all_checks()

if results['ready_for_production']:
    print("✅ Model ready for production deployment")
else:
    print(f"❌ {results['blockers']} blocking issues:")
    for blocker in results['blocker_details']:
        print(f"  - {blocker['check']}: {blocker['details']}")
```

---

## 2. Capacity Planning

### 2.1 Capacity Planning Calculator

```python
class CapacityPlanner:
    """Calculate resource requirements for ML serving."""

    def __init__(
        self,
        model_latency_ms: float,
        model_memory_mb: float,
        target_qps: int,
        target_p99_latency_ms: float
    ):
        self.model_latency_ms = model_latency_ms
        self.model_memory_mb = model_memory_mb
        self.target_qps = target_qps
        self.target_p99_latency_ms = target_p99_latency_ms

    def calculate_required_replicas(self) -> dict:
        """Calculate number of replicas needed."""

        # Single replica max QPS (at 70% utilization for safety)
        single_replica_qps = (1000 / self.model_latency_ms) * 0.7

        # Required replicas for throughput
        throughput_replicas = int(np.ceil(self.target_qps / single_replica_qps))

        # Add redundancy (N+2 for high availability)
        recommended_replicas = throughput_replicas + 2

        return {
            'min_replicas': throughput_replicas,
            'recommended_replicas': recommended_replicas,
            'single_replica_capacity_qps': single_replica_qps,
            'total_capacity_qps': recommended_replicas * single_replica_qps
        }

    def calculate_memory_requirements(self, replicas: int) -> dict:
        """Calculate memory requirements."""

        # Base model memory
        model_memory = self.model_memory_mb

        # Overhead (Flask/FastAPI, OS, etc) - typically 30-50%
        overhead_multiplier = 1.5

        # Per-replica memory
        per_replica_mb = model_memory * overhead_multiplier

        # Total memory
        total_memory_mb = per_replica_mb * replicas
        total_memory_gb = total_memory_mb / 1024

        return {
            'per_replica_mb': per_replica_mb,
            'total_memory_mb': total_memory_mb,
            'total_memory_gb': total_memory_gb,
            'recommended_pod_memory_limit': f"{int(per_replica_mb * 1.2)}Mi"
        }

    def calculate_cpu_requirements(self, replicas: int) -> dict:
        """Calculate CPU requirements."""

        # CPU cores based on latency requirements
        # Rule of thumb: 1 core can handle ~5-10ms of compute time efficiently

        cores_per_replica = max(1, int(np.ceil(self.model_latency_ms / 10)))

        total_cores = cores_per_replica * replicas

        return {
            'cores_per_replica': cores_per_replica,
            'total_cores': total_cores,
            'recommended_pod_cpu_request': f"{cores_per_replica}",
            'recommended_pod_cpu_limit': f"{cores_per_replica * 1.5}"
        }

    def estimate_monthly_cost(self, replicas: int, cost_per_core_hour: float = 0.05) -> dict:
        """Estimate monthly infrastructure cost."""

        cpu_calc = self.calculate_cpu_requirements(replicas)
        mem_calc = self.calculate_memory_requirements(replicas)

        # CPU cost
        hours_per_month = 730
        monthly_cpu_cost = cpu_calc['total_cores'] * cost_per_core_hour * hours_per_month

        # Memory cost (typically 1/4 of CPU cost)
        monthly_memory_cost = (mem_calc['total_memory_gb'] / 4) * cost_per_core_hour * hours_per_month

        total_monthly_cost = monthly_cpu_cost + monthly_memory_cost

        return {
            'monthly_cpu_cost': monthly_cpu_cost,
            'monthly_memory_cost': monthly_memory_cost,
            'total_monthly_cost': total_monthly_cost,
            'cost_per_1k_predictions': (total_monthly_cost / (self.target_qps * hours_per_month * 3.6))
        }

    def generate_capacity_plan(self) -> dict:
        """Generate complete capacity plan."""

        replica_calc = self.calculate_required_replicas()
        replicas = replica_calc['recommended_replicas']

        cpu_calc = self.calculate_cpu_requirements(replicas)
        mem_calc = self.calculate_memory_requirements(replicas)
        cost_calc = self.estimate_monthly_cost(replicas)

        return {
            'summary': {
                'target_qps': self.target_qps,
                'target_p99_latency_ms': self.target_p99_latency_ms,
                'model_latency_ms': self.model_latency_ms
            },
            'replicas': replica_calc,
            'cpu': cpu_calc,
            'memory': mem_calc,
            'cost': cost_calc,
            'kubernetes_config': self._generate_k8s_config(replicas, cpu_calc, mem_calc)
        }

    def _generate_k8s_config(self, replicas: int, cpu_calc: dict, mem_calc: dict) -> str:
        """Generate Kubernetes deployment config."""

        return f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model-serving
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
            cpu: "{cpu_calc['recommended_pod_cpu_request']}"
            memory: "{mem_calc['recommended_pod_memory_limit']}"
          limits:
            cpu: "{cpu_calc['recommended_pod_cpu_limit']}"
            memory: "{int(float(mem_calc['recommended_pod_memory_limit'].replace('Mi', '')) * 1.2)}Mi"
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
  minReplicas: {int(replicas * 0.5)}
  maxReplicas: {int(replicas * 2)}
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
"""

# Usage
planner = CapacityPlanner(
    model_latency_ms=50,  # P50 latency
    model_memory_mb=500,   # Model size in memory
    target_qps=1000,
    target_p99_latency_ms=100
)

capacity_plan = planner.generate_capacity_plan()

print(f"Required replicas: {capacity_plan['replicas']['recommended_replicas']}")
print(f"Total CPU cores: {capacity_plan['cpu']['total_cores']}")
print(f"Total memory: {capacity_plan['memory']['total_memory_gb']:.1f} GB")
print(f"Monthly cost: ${capacity_plan['cost']['total_monthly_cost']:.2f}")
print(f"Cost per 1K predictions: ${capacity_plan['cost']['cost_per_1k_predictions']:.4f}")

# Save K8s config
with open('k8s-deployment.yaml', 'w') as f:
    f.write(capacity_plan['kubernetes_config'])
```

---

## 3. Performance Optimization

### 3.1 Model Optimization Techniques

```python
import time
import numpy as np
from functools import wraps

class ModelOptimizer:
    """Optimize model inference performance."""

    def __init__(self, model):
        self.model = model
        self.cache = {}

    def optimize_with_caching(self, cache_size: int = 1000):
        """Add prediction caching."""
        from functools import lru_cache

        @lru_cache(maxsize=cache_size)
        def _cached_predict_single(features_tuple):
            """Cache predictions for identical inputs."""
            features = np.array(features_tuple).reshape(1, -1)
            return self.model.predict(features)[0]

        def cached_predict(X):
            """Predict with caching."""
            if len(X.shape) == 1:
                X = X.reshape(1, -1)

            results = []
            for row in X:
                # Convert to tuple for hashing
                features_tuple = tuple(row)
                result = _cached_predict_single(features_tuple)
                results.append(result)

            return np.array(results)

        return cached_predict

    def optimize_with_batching(self, batch_size: int = 32):
        """Add request batching."""
        import queue
        import threading

        request_queue = queue.Queue()
        batch_ready = threading.Event()

        def batch_processor():
            """Process requests in batches."""
            while True:
                batch = []
                batch_promises = []

                # Collect batch
                try:
                    while len(batch) < batch_size:
                        request, promise = request_queue.get(timeout=0.05)
                        batch.append(request)
                        batch_promises.append(promise)
                except queue.Empty:
                    pass

                if batch:
                    # Process batch
                    batch_array = np.array(batch)
                    predictions = self.model.predict(batch_array)

                    # Fulfill promises
                    for promise, prediction in zip(batch_promises, predictions):
                        promise.set_result(prediction)

        # Start processor thread
        processor_thread = threading.Thread(target=batch_processor, daemon=True)
        processor_thread.start()

        def batched_predict(X):
            """Submit prediction request."""
            import asyncio

            promise = asyncio.Future()
            request_queue.put((X, promise))

            # Wait for result
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(promise)

        return batched_predict

    def optimize_with_quantization(self):
        """Quantize model for faster inference (PyTorch example)."""
        import torch

        if isinstance(self.model, torch.nn.Module):
            # Dynamic quantization
            quantized_model = torch.quantization.quantize_dynamic(
                self.model,
                {torch.nn.Linear},
                dtype=torch.qint8
            )

            return quantized_model

        return self.model

def benchmark_optimization(model, X_test, optimization_func=None):
    """Benchmark model performance."""

    if optimization_func:
        optimized_model = optimization_func(model)
    else:
        optimized_model = model

    latencies = []

    for _ in range(100):
        sample = X_test[np.random.randint(len(X_test))]

        start = time.time()
        if hasattr(optimized_model, '__call__'):
            optimized_model(sample)
        else:
            optimized_model.predict(sample.reshape(1, -1))
        latency = time.time() - start

        latencies.append(latency)

    return {
        'mean_latency_ms': np.mean(latencies) * 1000,
        'p50_latency_ms': np.percentile(latencies, 50) * 1000,
        'p95_latency_ms': np.percentile(latencies, 95) * 1000,
        'p99_latency_ms': np.percentile(latencies, 99) * 1000
    }

# Compare optimizations
optimizer = ModelOptimizer(model)

baseline = benchmark_optimization(model, X_test)
cached = benchmark_optimization(model, X_test, optimizer.optimize_with_caching)

print("Baseline:")
print(f"  P50: {baseline['p50_latency_ms']:.2f}ms")
print(f"  P95: {baseline['p95_latency_ms']:.2f}ms")

print("With caching:")
print(f"  P50: {cached['p50_latency_ms']:.2f}ms")
print(f"  P95: {cached['p95_latency_ms']:.2f}ms")
print(f"  Speedup: {baseline['p50_latency_ms'] / cached['p50_latency_ms']:.2f}x")
```

---

## 4. Reliability Engineering

### 4.1 SLOs and SLIs

```python
from dataclasses import dataclass
from typing import List

@dataclass
class SLI:
    """Service Level Indicator."""
    name: str
    description: str
    query: str  # Prometheus query
    unit: str

@dataclass
class SLO:
    """Service Level Objective."""
    name: str
    sli: SLI
    target: float  # e.g., 99.9 for 99.9%
    window_days: int  # e.g., 30 days

class SLOMonitor:
    """Monitor SLOs and calculate error budgets."""

    def __init__(self, slos: List[SLO]):
        self.slos = slos

    def calculate_error_budget(self, slo: SLO, current_performance: float) -> dict:
        """
        Calculate error budget.

        Args:
            slo: Service Level Objective
            current_performance: Current actual performance (e.g., 99.95)

        Returns:
            Error budget status
        """
        # Total requests in window
        total_requests = self._get_total_requests(slo.window_days)

        # Allowed failures
        allowed_failure_rate = (100 - slo.target) / 100
        allowed_failures = int(total_requests * allowed_failure_rate)

        # Actual failures
        actual_failure_rate = (100 - current_performance) / 100
        actual_failures = int(total_requests * actual_failure_rate)

        # Remaining budget
        remaining_failures = allowed_failures - actual_failures
        budget_remaining_pct = (remaining_failures / allowed_failures * 100) if allowed_failures > 0 else 0

        return {
            'slo_name': slo.name,
            'target': slo.target,
            'current_performance': current_performance,
            'window_days': slo.window_days,
            'total_requests': total_requests,
            'allowed_failures': allowed_failures,
            'actual_failures': actual_failures,
            'remaining_failures': remaining_failures,
            'budget_remaining_pct': budget_remaining_pct,
            'budget_exhausted': remaining_failures <= 0
        }

    def _get_total_requests(self, window_days: int) -> int:
        """Get total requests in window from Prometheus."""
        # In production: query Prometheus
        # For example: return 1M requests per day
        return 1_000_000 * window_days

# Define SLOs
availability_sli = SLI(
    name="availability",
    description="Percentage of successful requests",
    query='sum(rate(http_requests_total{status=~"2.."}[5m])) / sum(rate(http_requests_total[5m]))',
    unit="percentage"
)

latency_sli = SLI(
    name="latency_p99",
    description="99th percentile latency",
    query='histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))',
    unit="seconds"
)

slos = [
    SLO(
        name="API Availability",
        sli=availability_sli,
        target=99.9,  # 99.9% uptime
        window_days=30
    ),
    SLO(
        name="API Latency",
        sli=latency_sli,
        target=99.0,  # 99% of requests under threshold
        window_days=7
    )
]

monitor = SLOMonitor(slos)

# Check error budget
availability_budget = monitor.calculate_error_budget(
    slos[0],
    current_performance=99.95  # Current: 99.95%
)

print(f"Error Budget Status: {availability_budget['slo_name']}")
print(f"Target: {availability_budget['target']}%")
print(f"Current: {availability_budget['current_performance']}%")
print(f"Budget remaining: {availability_budget['budget_remaining_pct']:.1f}%")
print(f"Remaining failures allowed: {availability_budget['remaining_failures']:,}")

if availability_budget['budget_exhausted']:
    print("⚠️ ERROR BUDGET EXHAUSTED - Halt deployments!")
```

---

## 5. Incident Management

### 5.1 Incident Response Workflow

```python
from enum import Enum
from datetime import datetime, timedelta

class IncidentSeverity(Enum):
    SEV1 = "sev1"  # Critical - complete outage
    SEV2 = "sev2"  # Major - significant degradation
    SEV3 = "sev3"  # Minor - limited impact
    SEV4 = "sev4"  # Low - minimal impact

@dataclass
class Incident:
    """Incident tracking."""
    incident_id: str
    title: str
    severity: IncidentSeverity
    detected_at: datetime
    description: str
    affected_services: List[str]
    on_call_responder: str

    # Status tracking
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    root_cause: Optional[str] = None

    # Impact tracking
    affected_users: int = 0
    failed_requests: int = 0

class IncidentManager:
    """Manage incidents and response."""

    def __init__(self):
        self.incidents: List[Incident] = []

    def create_incident(
        self,
        title: str,
        severity: IncidentSeverity,
        description: str,
        affected_services: List[str]
    ) -> Incident:
        """Create new incident."""

        incident = Incident(
            incident_id=f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            title=title,
            severity=severity,
            detected_at=datetime.now(),
            description=description,
            affected_services=affected_services,
            on_call_responder=self._get_on_call_engineer()
        )

        self.incidents.append(incident)

        # Trigger alerts
        self._trigger_alerts(incident)

        # Create incident channel
        self._create_incident_channel(incident)

        return incident

    def acknowledge_incident(self, incident_id: str, responder: str):
        """Acknowledge incident."""
        incident = self._get_incident(incident_id)
        incident.acknowledged_at = datetime.now()
        incident.on_call_responder = responder

        # Update incident status in systems
        self._update_statuspage(incident, "investigating")

    def resolve_incident(
        self,
        incident_id: str,
        root_cause: str,
        remediation: str
    ):
        """Resolve incident."""
        incident = self._get_incident(incident_id)
        incident.resolved_at = datetime.now()
        incident.root_cause = root_cause

        # Calculate metrics
        ttd = (incident.acknowledged_at - incident.detected_at).total_seconds() / 60
        ttr = (incident.resolved_at - incident.acknowledged_at).total_seconds() / 60

        # Update status page
        self._update_statuspage(incident, "resolved")

        # Schedule post-mortem
        self._schedule_postmortem(incident)

        print(f"Incident {incident_id} resolved")
        print(f"  Time to Detect: {ttd:.1f} minutes")
        print(f"  Time to Resolve: {ttr:.1f} minutes")

    def _trigger_alerts(self, incident: Incident):
        """Send alerts based on severity."""
        if incident.severity == IncidentSeverity.SEV1:
            # Page on-call + manager
            self._page_oncall(incident)
            self._page_manager(incident)
            self._send_slack_alert(incident, channel="#incidents-critical")

        elif incident.severity == IncidentSeverity.SEV2:
            # Page on-call
            self._page_oncall(incident)
            self._send_slack_alert(incident, channel="#incidents")

        else:
            # Slack only
            self._send_slack_alert(incident, channel="#incidents")

    def _create_incident_channel(self, incident: Incident):
        """Create dedicated Slack channel for incident."""
        channel_name = f"incident-{incident.incident_id.lower()}"

        # In production: use Slack API to create channel
        print(f"Created incident channel: #{channel_name}")

    def _schedule_postmortem(self, incident: Incident):
        """Schedule post-mortem meeting."""
        # Schedule for 24-48 hours after resolution
        postmortem_time = incident.resolved_at + timedelta(hours=36)

        print(f"Post-mortem scheduled for {postmortem_time}")

    def generate_postmortem_template(self, incident: Incident) -> str:
        """Generate post-mortem template."""

        ttd = (incident.acknowledged_at - incident.detected_at).total_seconds() / 60 if incident.acknowledged_at else 0
        ttr = (incident.resolved_at - incident.acknowledged_at).total_seconds() / 60 if incident.resolved_at else 0

        template = f"""# Post-Mortem: {incident.title}

**Incident ID:** {incident.incident_id}
**Severity:** {incident.severity.value.upper()}
**Date:** {incident.detected_at.strftime('%Y-%m-%d')}
**Time to Detect:** {ttd:.1f} minutes
**Time to Resolve:** {ttr:.1f} minutes

## Summary

{incident.description}

## Impact

- **Affected Services:** {', '.join(incident.affected_services)}
- **Affected Users:** {incident.affected_users:,}
- **Failed Requests:** {incident.failed_requests:,}
- **Duration:** {ttr:.1f} minutes

## Timeline

- **{incident.detected_at.strftime('%H:%M')}** - Incident detected
- **{incident.acknowledged_at.strftime('%H:%M') if incident.acknowledged_at else 'N/A'}** - Incident acknowledged
- **{incident.resolved_at.strftime('%H:%M') if incident.resolved_at else 'N/A'}** - Incident resolved

## Root Cause

{incident.root_cause or 'To be determined'}

## Resolution

[Describe what was done to resolve the incident]

## Action Items

- [ ] Short-term fix: [Description]
- [ ] Long-term fix: [Description]
- [ ] Monitoring improvement: [Description]
- [ ] Runbook update: [Description]
- [ ] Alert tuning: [Description]

## Lessons Learned

### What Went Well

- [Point 1]
- [Point 2]

### What Didn't Go Well

- [Point 1]
- [Point 2]

### Where We Got Lucky

- [Point 1]

## Follow-up Tasks

- [ ] Task 1 (Owner: X, Due: YYYY-MM-DD)
- [ ] Task 2 (Owner: Y, Due: YYYY-MM-DD)
"""

        return template

# Usage
incident_mgr = IncidentManager()

# Create incident
incident = incident_mgr.create_incident(
    title="Model serving API returning 500 errors",
    severity=IncidentSeverity.SEV2,
    description="Credit model API experiencing high error rate (45%). Errors indicate model loading failure.",
    affected_services=["credit-model-api", "loan-application-service"]
)

# Acknowledge
incident_mgr.acknowledge_incident(incident.incident_id, "engineer@company.com")

# Resolve
incident_mgr.resolve_incident(
    incident.incident_id,
    root_cause="Model artifact corrupted during deployment due to incomplete upload to S3",
    remediation="Rolled back to previous model version, fixed deployment script to verify S3 upload"
)

# Generate post-mortem
postmortem = incident_mgr.generate_postmortem_template(incident)
print(postmortem)
```

---

## 6. Operational Excellence

### 6.1 Runbook Template

```markdown
# Runbook: Credit Model API

## Service Overview

**Service Name:** credit-model-api
**Owner:** ML Platform Team
**On-Call:** mlops-oncall@company.com
**Slack Channel:** #mlops-support

## Architecture

[Diagram of service architecture]

- **Deployment:** Kubernetes (3 replicas)
- **Model:** Random Forest (credit-model v2.3)
- **Dependencies:** PostgreSQL, Redis, S3
- **Load Balancer:** Istio

## SLOs

- **Availability:** 99.9% (30-day window)
- **Latency P99:** < 100ms
- **Throughput:** 1000 QPS

## Common Issues

### Issue 1: High Latency

**Symptoms:**
- P99 latency > 200ms
- Alert: `HighLatency` firing

**Diagnosis:**
1. Check Grafana dashboard: [link]
2. Query Prometheus: `histogram_quantile(0.99, http_request_duration_seconds_bucket)`
3. Check pod CPU/memory: `kubectl top pods -n production`

**Resolution:**
1. If CPU > 80%: Scale up replicas
   ```bash
   kubectl scale deployment credit-model-api --replicas=5 -n production
   ```
2. If memory issue: Restart pods
   ```bash
   kubectl rollout restart deployment/credit-model-api -n production
   ```
3. If database slow: Check slow query log

**Prevention:**
- Review auto-scaling configuration
- Optimize model inference code

### Issue 2: Model Loading Failure

**Symptoms:**
- 500 errors with "Model not found"
- Alert: `ModelLoadingFailure`

**Diagnosis:**
```bash
# Check pod logs
kubectl logs -f deployment/credit-model-api -n production

# Verify model in S3
aws s3 ls s3://ml-models/production/credit-model/
```

**Resolution:**
1. Verify model artifacts exist in S3
2. Check IAM permissions for S3 access
3. Rollback to previous version if needed:
   ```bash
   kubectl rollout undo deployment/credit-model-api -n production
   ```

## Escalation

- **L1:** On-call engineer (response time: 15 min)
- **L2:** ML Platform lead (if unresolved after 30 min)
- **L3:** VP Engineering (SEV1 only)

## Metrics & Dashboards

- **Grafana Dashboard:** [link]
- **Prometheus Alerts:** [link]
- **Error Logs:** [Kibana link]

## Deployment

See: [Deployment Runbook]

## Rollback Procedure

```bash
# Rollback to previous deployment
kubectl rollout undo deployment/credit-model-api -n production

# Verify rollback
kubectl rollout status deployment/credit-model-api -n production
```
```

---

## 7. Summary and Best Practices

### Key Takeaways

1. **Production Readiness**: Comprehensive checklists prevent failures
2. **Capacity Planning**: Right-size infrastructure to meet SLOs cost-effectively
3. **Performance**: Optimize for latency through caching, batching, quantization
4. **Reliability**: Define SLOs, track error budgets, build resilient systems
5. **Incidents**: Prepared response reduces impact and recovery time
6. **Operations**: Runbooks enable faster problem resolution

### Best Practices

- **Before Production**: Complete readiness checklist
- **Capacity**: Plan for 2x expected traffic
- **Monitoring**: Track SLOs continuously
- **Incidents**: Practice incident response drills
- **Documentation**: Keep runbooks up-to-date
- **Post-Mortems**: Learn from every incident

---

**Total Words**: ~5,000 words

**Next Module**: Module 09 - MLOps Security
