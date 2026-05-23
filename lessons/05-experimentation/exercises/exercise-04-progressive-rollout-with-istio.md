## Exercise 4: Progressive Rollout with Istio (90 minutes)

**Objective**: Implement progressive rollout (canary deployment) of ML models using Istio service mesh with traffic splitting and automated rollback.

### Background

Deploy new model versions gradually:
1. Start with 5% traffic to new model
2. Monitor metrics
3. Gradually increase to 25%, 50%, 100%
4. Automatically rollback if metrics degrade

### Tasks

1. **Configure Istio traffic splitting**
2. **Implement canary deployment pipeline**
3. **Add automated metric monitoring**
4. **Implement automatic rollback**
5. **Create promotion strategy**

### Starter Code

```yaml
# k8s/model-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: recommendation-model-v1
  labels:
    app: recommendation-model
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: recommendation-model
      version: v1
  template:
    metadata:
      labels:
        app: recommendation-model
        version: v1
    spec:
      containers:
      - name: model-server
        image: model-serving:v1
        ports:
        - containerPort: 8080
        env:
        - name: MODEL_URI
          value: "models:/recommendation/1"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: recommendation-model-v2
  labels:
    app: recommendation-model
    version: v2
spec:
  replicas: 1  # Start with fewer replicas for canary
  selector:
    matchLabels:
      app: recommendation-model
      version: v2
  template:
    metadata:
      labels:
        app: recommendation-model
        version: v2
    spec:
      containers:
      - name: model-server
        image: model-serving:v2
        ports:
        - containerPort: 8080
        env:
        - name: MODEL_URI
          value: "models:/recommendation/2"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
```

```yaml
# k8s/istio-virtual-service.yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: recommendation-model
spec:
  hosts:
  - recommendation-model
  http:
  - match:
    - headers:
        x-version:
          exact: v2
    route:
    - destination:
        host: recommendation-model
        subset: v2
  - route:
    - destination:
        host: recommendation-model
        subset: v1
      weight: 95  # TODO: Gradually shift traffic
    - destination:
        host: recommendation-model
        subset: v2
      weight: 5   # Start with 5% canary traffic
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: recommendation-model
spec:
  host: recommendation-model
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

```python
# rollout/canary_controller.py
"""Canary deployment controller for progressive rollout."""

import time
from typing import Dict, List, Optional
from dataclasses import dataclass
import yaml
from kubernetes import client, config

@dataclass
class CanaryConfig:
    """Configuration for canary deployment."""

    service_name: str
    namespace: str
    canary_version: str
    baseline_version: str
    initial_weight: int = 5
    final_weight: int = 100
    step_weight: int = 25
    step_interval_minutes: int = 30
    success_threshold: float = 0.95
    error_rate_threshold: float = 0.05
    latency_threshold_ms: float = 200

class CanaryController:
    """Controls progressive rollout of model versions."""

    def __init__(self, canary_config: CanaryConfig):
        """
        Initialize canary controller.

        Args:
            canary_config: Canary deployment configuration
        """
        self.config = canary_config
        config.load_kube_config()
        self.api = client.CustomObjectsApi()

    def start_rollout(self):
        """
        Start progressive rollout.

        This method orchestrates the entire canary deployment:
        1. Deploy canary version with initial traffic
        2. Monitor metrics at each step
        3. Gradually increase traffic if metrics are good
        4. Rollback if metrics degrade
        5. Complete rollout when reaching 100%
        """
        print(f"Starting canary rollout for {self.config.service_name}")

        current_weight = self.config.initial_weight

        while current_weight <= self.config.final_weight:
            print(f"\n📊 Setting canary traffic to {current_weight}%")

            # TODO: Update traffic split
            self._update_traffic_split(current_weight)

            # TODO: Wait for metrics to stabilize
            print(f"⏳ Waiting {self.config.step_interval_minutes} minutes for metrics...")
            time.sleep(self.config.step_interval_minutes * 60)

            # TODO: Evaluate metrics
            metrics = self._collect_metrics()
            is_healthy = self._evaluate_metrics(metrics)

            if not is_healthy:
                print("❌ Canary metrics degraded, rolling back!")
                self._rollback()
                return False

            print(f"✅ Canary metrics healthy at {current_weight}%")

            if current_weight == self.config.final_weight:
                print("🎉 Rollout complete!")
                return True

            # TODO: Increase traffic
            current_weight = min(current_weight + self.config.step_weight, self.config.final_weight)

        return True

    def _update_traffic_split(self, canary_weight: int):
        """
        Update Istio VirtualService with new traffic weights.

        Args:
            canary_weight: Percentage of traffic to canary (0-100)
        """
        # TODO: Load VirtualService
        # TODO: Update weights
        # TODO: Apply changes

        baseline_weight = 100 - canary_weight

        virtual_service = {
            'apiVersion': 'networking.istio.io/v1beta1',
            'kind': 'VirtualService',
            'metadata': {
                'name': self.config.service_name,
                'namespace': self.config.namespace
            },
            'spec': {
                'hosts': [self.config.service_name],
                'http': [{
                    'route': [
                        {
                            'destination': {
                                'host': self.config.service_name,
                                'subset': self.config.baseline_version
                            },
                            'weight': baseline_weight
                        },
                        {
                            'destination': {
                                'host': self.config.service_name,
                                'subset': self.config.canary_version
                            },
                            'weight': canary_weight
                        }
                    ]
                }]
            }
        }

        # TODO: Apply VirtualService update
        try:
            self.api.patch_namespaced_custom_object(
                group='networking.istio.io',
                version='v1beta1',
                namespace=self.config.namespace,
                plural='virtualservices',
                name=self.config.service_name,
                body=virtual_service
            )
            print(f"Updated traffic split: {baseline_weight}% baseline, {canary_weight}% canary")
        except Exception as e:
            print(f"Error updating traffic split: {e}")
            raise

    def _collect_metrics(self) -> Dict[str, float]:
        """
        Collect metrics from Prometheus.

        Returns:
            Dictionary of metrics
        """
        # TODO: Query Prometheus for:
        # - Error rate
        # - Latency (p50, p95, p99)
        # - Request rate
        # - Success rate

        # Placeholder - in real implementation, query Prometheus
        import random
        return {
            'canary_error_rate': random.uniform(0.01, 0.03),
            'canary_latency_p95': random.uniform(100, 150),
            'canary_success_rate': random.uniform(0.96, 0.99),
            'baseline_error_rate': random.uniform(0.01, 0.02),
            'baseline_latency_p95': random.uniform(100, 140),
            'baseline_success_rate': random.uniform(0.97, 0.99)
        }

    def _evaluate_metrics(self, metrics: Dict[str, float]) -> bool:
        """
        Evaluate if canary metrics are acceptable.

        Args:
            metrics: Collected metrics

        Returns:
            True if metrics pass thresholds
        """
        # TODO: Compare canary vs baseline
        # TODO: Check absolute thresholds
        # TODO: Return health status

        checks = []

        # Check error rate
        if metrics['canary_error_rate'] > self.config.error_rate_threshold:
            print(f"⚠️  Error rate too high: {metrics['canary_error_rate']:.3f}")
            checks.append(False)
        else:
            checks.append(True)

        # Check latency
        if metrics['canary_latency_p95'] > self.config.latency_threshold_ms:
            print(f"⚠️  Latency too high: {metrics['canary_latency_p95']:.1f}ms")
            checks.append(False)
        else:
            checks.append(True)

        # Check success rate
        if metrics['canary_success_rate'] < self.config.success_threshold:
            print(f"⚠️  Success rate too low: {metrics['canary_success_rate']:.3f}")
            checks.append(False)
        else:
            checks.append(True)

        # Compare to baseline
        if metrics['canary_error_rate'] > metrics['baseline_error_rate'] * 1.5:
            print(f"⚠️  Error rate 50% worse than baseline")
            checks.append(False)
        else:
            checks.append(True)

        return all(checks)

    def _rollback(self):
        """Rollback to baseline version."""
        print("🔄 Rolling back to baseline version...")
        self._update_traffic_split(0)  # 0% to canary = 100% to baseline
        print("✅ Rollback complete")
```

```python
# rollout/prometheus_client.py
"""Prometheus client for metrics collection."""

import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class PrometheusClient:
    """Client for querying Prometheus metrics."""

    def __init__(self, prometheus_url: str = "http://prometheus:9090"):
        """
        Initialize Prometheus client.

        Args:
            prometheus_url: Prometheus server URL
        """
        self.base_url = prometheus_url

    def query_metric(
        self,
        query: str,
        time: Optional[datetime] = None
    ) -> Dict:
        """
        Query Prometheus instant vector.

        Args:
            query: PromQL query
            time: Query time (default: now)

        Returns:
            Query result
        """
        # TODO: Build query URL
        url = f"{self.base_url}/api/v1/query"
        params = {'query': query}
        if time:
            params['time'] = time.isoformat()

        # TODO: Execute query
        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()['data']['result']

    def query_range(
        self,
        query: str,
        start: datetime,
        end: datetime,
        step: str = '1m'
    ) -> Dict:
        """
        Query Prometheus range vector.

        Args:
            query: PromQL query
            start: Start time
            end: End time
            step: Query resolution

        Returns:
            Query result
        """
        # TODO: Build range query URL
        url = f"{self.base_url}/api/v1/query_range"
        params = {
            'query': query,
            'start': start.isoformat(),
            'end': end.isoformat(),
            'step': step
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()['data']['result']

    def get_error_rate(
        self,
        service: str,
        version: str,
        window: str = '5m'
    ) -> float:
        """
        Get error rate for service version.

        Args:
            service: Service name
            version: Version label
            window: Time window

        Returns:
            Error rate (0-1)
        """
        # TODO: Build PromQL query for error rate
        query = f'''
        sum(rate(http_requests_total{{
            service="{service}",
            version="{version}",
            status=~"5.."
        }}[{window}]))
        /
        sum(rate(http_requests_total{{
            service="{service}",
            version="{version}"
        }}[{window}]))
        '''

        result = self.query_metric(query)
        if result:
            return float(result[0]['value'][1])
        return 0.0

    def get_latency_percentile(
        self,
        service: str,
        version: str,
        percentile: float = 0.95,
        window: str = '5m'
    ) -> float:
        """
        Get latency percentile for service version.

        Args:
            service: Service name
            version: Version label
            percentile: Percentile (0.95 for p95)
            window: Time window

        Returns:
            Latency in milliseconds
        """
        # TODO: Build PromQL query for latency
        query = f'''
        histogram_quantile({percentile},
          sum(rate(http_request_duration_seconds_bucket{{
            service="{service}",
            version="{version}"
          }}[{window}])) by (le)
        ) * 1000
        '''

        result = self.query_metric(query)
        if result:
            return float(result[0]['value'][1])
        return 0.0
```

### Validation

Test canary deployment:
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/model-deployment.yaml
kubectl apply -f k8s/istio-virtual-service.yaml

# Run canary controller
python -c "
from rollout.canary_controller import CanaryController, CanaryConfig

config = CanaryConfig(
    service_name='recommendation-model',
    namespace='default',
    canary_version='v2',
    baseline_version='v1',
    initial_weight=5,
    step_weight=25,
    step_interval_minutes=1  # Short for testing
)

controller = CanaryController(config)
controller.start_rollout()
"
```

### Success Criteria

- [ ] Istio VirtualService configures traffic splitting
- [ ] Canary controller gradually increases traffic
- [ ] Metrics are collected from Prometheus
- [ ] Rollback triggers on metric degradation
- [ ] Deployment completes successfully for healthy canary
- [ ] Multiple concurrent canaries are supported

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Istio**: Use VirtualService for traffic splitting, DestinationRule for subsets
2. **Traffic Weights**: Must sum to 100, update progressively (5% → 25% → 50% → 100%)
3. **Metrics**: Query Prometheus with PromQL for error rate, latency
4. **Rollback**: Set canary weight to 0 to route all traffic to baseline
5. **Monitoring**: Wait for metrics to stabilize before evaluation (2-5 minutes)
6. **Kubernetes API**: Use `kubernetes-client` library for programmatic access

</details>

---
