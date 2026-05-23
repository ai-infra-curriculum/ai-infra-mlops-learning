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
