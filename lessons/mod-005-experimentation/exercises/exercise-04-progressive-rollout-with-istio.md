## Exercise 4: Progressive Rollout with Istio (90 minutes)

**Objective**: Implement progressive rollout (canary deployment) of ML models using the Istio service mesh with weighted traffic splitting, Prometheus-driven metric analysis, and automated rollback.

### Background

Shipping a new model version straight to 100% of traffic is the single most common cause of ML production outages. A progressive rollout de-risks the change by shifting traffic in stages and watching the new version's golden signals against the incumbent:

1. Deploy the new version (`v2`) alongside the current version (`v1`).
2. Send 5% of live traffic to `v2` (the canary).
3. Compare canary error rate, latency, and success rate against the baseline.
4. Promote to 25%, 50%, 100% only while the canary stays healthy.
5. Roll back instantly (canary weight to 0%) the moment a metric regresses.

Istio decouples traffic routing from the number of pods. A `VirtualService` controls the
weight split; a `DestinationRule` defines the `v1`/`v2` subsets by pod label. You never have to
scale deployments to control the split — you change weights through the Kubernetes API. This is
exactly how Flagger, Argo Rollouts, and most production canary controllers work under the hood;
here you build a minimal version yourself so you understand the mechanics.

### Tasks

1. **Deploy two model versions** with health and readiness probes (manifests below).
2. **Configure Istio traffic splitting** with a `VirtualService` + `DestinationRule`.
3. **Implement the canary controller** that drives the weight progression via the Kubernetes API.
4. **Collect real metrics from Prometheus** (error rate, p95 latency, success rate) per subset.
5. **Implement automated rollback** keyed on absolute thresholds *and* baseline comparison.
6. **Define a promotion strategy** with configurable step size, soak interval, and gates.

### Starter Code

The Kubernetes manifests below deploy both versions and wire up Istio. Note that `v2` starts with
a single replica — under weighted routing you scale the canary up only as its traffic share grows.

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
  replicas: 1  # Start with a single replica for the canary
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
  # Header-based override lets QA pin themselves to v2 regardless of weight.
  - match:
    - headers:
        x-version:
          exact: v2
    route:
    - destination:
        host: recommendation-model
        subset: v2
  # Default weighted split. The controller rewrites these weights as the rollout progresses.
  - route:
    - destination:
        host: recommendation-model
        subset: v1
      weight: 95
    - destination:
        host: recommendation-model
        subset: v2
      weight: 5
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: recommendation-model
spec:
  host: recommendation-model
  trafficPolicy:
    # Outlier detection ejects pods that return 5xx, a free second line of defense.
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

The Prometheus client is fully implemented. It issues PromQL queries scoped by the
`version` label so you can compare the canary against the baseline on identical metrics.

```python
# rollout/prometheus_client.py
"""Prometheus client for canary metric collection."""

import logging
from datetime import datetime
from typing import List, Optional

import requests

logger = logging.getLogger(__name__)


class PrometheusClient:
    """Client for querying Prometheus metrics."""

    def __init__(self, prometheus_url: str = "http://prometheus:9090", timeout: int = 10):
        """
        Initialize the Prometheus client.

        Args:
            prometheus_url: Prometheus server base URL.
            timeout: Per-request timeout in seconds.
        """
        self.base_url = prometheus_url.rstrip("/")
        self.timeout = timeout

    def query_metric(self, query: str, at_time: Optional[datetime] = None) -> List[dict]:
        """
        Execute a Prometheus instant query.

        Args:
            query: PromQL expression.
            at_time: Evaluation timestamp (defaults to "now").

        Returns:
            The ``result`` array from the Prometheus response (possibly empty).
        """
        params = {"query": query}
        if at_time is not None:
            params["time"] = at_time.timestamp()

        response = requests.get(
            f"{self.base_url}/api/v1/query", params=params, timeout=self.timeout
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("status") != "success":
            raise RuntimeError(f"Prometheus query failed: {payload.get('error')}")
        return payload["data"]["result"]

    def _scalar(self, query: str, default: float = 0.0) -> float:
        """Run a query expected to return a single scalar; fall back to ``default``."""
        try:
            result = self.query_metric(query)
        except (requests.RequestException, RuntimeError) as exc:
            logger.error("Prometheus query error for %r: %s", query, exc)
            return default
        if not result:
            return default
        return float(result[0]["value"][1])

    def get_error_rate(self, service: str, version: str, window: str = "5m") -> float:
        """
        Fraction of 5xx responses for a service/version over ``window`` (0.0-1.0).
        Returns 0.0 when there is no traffic yet.
        """
        query = (
            f'sum(rate(http_requests_total{{service="{service}",version="{version}",'
            f'status=~"5.."}}[{window}]))'
            f' / clamp_min(sum(rate(http_requests_total{{service="{service}",'
            f'version="{version}"}}[{window}])), 1)'
        )
        return self._scalar(query)

    def get_success_rate(self, service: str, version: str, window: str = "5m") -> float:
        """Fraction of 2xx/3xx responses (0.0-1.0). Returns 1.0 with no traffic."""
        query = (
            f'sum(rate(http_requests_total{{service="{service}",version="{version}",'
            f'status=~"2..|3.."}}[{window}]))'
            f' / clamp_min(sum(rate(http_requests_total{{service="{service}",'
            f'version="{version}"}}[{window}])), 1)'
        )
        return self._scalar(query, default=1.0)

    def get_latency_percentile(
        self, service: str, version: str, percentile: float = 0.95, window: str = "5m"
    ) -> float:
        """p{percentile} request latency in milliseconds for a service/version."""
        query = (
            f"histogram_quantile({percentile}, "
            f"sum(rate(http_request_duration_seconds_bucket{{"
            f'service="{service}",version="{version}"}}[{window}])) by (le)) * 1000'
        )
        return self._scalar(query)

    def get_request_rate(self, service: str, version: str, window: str = "5m") -> float:
        """Requests per second for a service/version."""
        query = (
            f'sum(rate(http_requests_total{{service="{service}",'
            f'version="{version}"}}[{window}]))'
        )
        return self._scalar(query)
```

The canary controller is the heart of the exercise. Every method is implemented: it patches the
Istio `VirtualService`, soaks for the configured interval, pulls real metrics, evaluates them
against both absolute thresholds and the baseline, and rolls back on any regression.

```python
# rollout/canary_controller.py
"""Canary deployment controller for progressive model rollout."""

import logging
import time
from dataclasses import dataclass, field
from typing import Dict, List

from kubernetes import client, config

from rollout.prometheus_client import PrometheusClient

logger = logging.getLogger(__name__)


@dataclass
class CanaryConfig:
    """Configuration for a canary deployment."""

    service_name: str
    namespace: str
    canary_version: str
    baseline_version: str
    initial_weight: int = 5
    final_weight: int = 100
    step_weight: int = 25
    step_interval_minutes: float = 10.0
    error_rate_threshold: float = 0.05      # absolute ceiling, 5%
    latency_p95_threshold_ms: float = 200.0  # absolute ceiling
    success_rate_threshold: float = 0.95    # absolute floor
    baseline_error_multiplier: float = 1.5  # canary may be at most 1.5x baseline error
    metric_window: str = "5m"
    weight_steps: List[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.weight_steps:
            steps, weight = [], self.initial_weight
            while weight < self.final_weight:
                steps.append(weight)
                weight += self.step_weight
            steps.append(self.final_weight)
            self.weight_steps = steps


class CanaryController:
    """Drives a progressive rollout of a model version through Istio."""

    def __init__(self, canary_config: CanaryConfig, prom: PrometheusClient):
        self.config = canary_config
        self.prom = prom
        config.load_kube_config()
        self.api = client.CustomObjectsApi()

    def start_rollout(self) -> bool:
        """
        Run the full rollout. Returns True if the canary reached 100% healthy,
        False if it was rolled back.
        """
        logger.info("Starting canary rollout for %s", self.config.service_name)

        for weight in self.config.weight_steps:
            logger.info("Shifting %d%% of traffic to canary", weight)
            self._update_traffic_split(weight)

            logger.info("Soaking %.1f min for metrics to stabilize", self.config.step_interval_minutes)
            time.sleep(self.config.step_interval_minutes * 60)

            metrics = self._collect_metrics()
            healthy, reasons = self._evaluate_metrics(metrics)
            if not healthy:
                logger.error("Canary unhealthy at %d%%: %s", weight, "; ".join(reasons))
                self._rollback()
                return False

            logger.info("Canary healthy at %d%% (err=%.4f, p95=%.1fms, success=%.4f)",
                        weight, metrics["canary_error_rate"],
                        metrics["canary_latency_p95"], metrics["canary_success_rate"])

        logger.info("Rollout complete — canary promoted to 100%%")
        self._promote_baseline_label()
        return True

    def _update_traffic_split(self, canary_weight: int) -> None:
        """Patch the Istio VirtualService with new weights (must sum to 100)."""
        baseline_weight = 100 - canary_weight
        body = {
            "spec": {
                "hosts": [self.config.service_name],
                "http": [
                    {
                        "route": [
                            {
                                "destination": {
                                    "host": self.config.service_name,
                                    "subset": self.config.baseline_version,
                                },
                                "weight": baseline_weight,
                            },
                            {
                                "destination": {
                                    "host": self.config.service_name,
                                    "subset": self.config.canary_version,
                                },
                                "weight": canary_weight,
                            },
                        ]
                    }
                ],
            }
        }
        self.api.patch_namespaced_custom_object(
            group="networking.istio.io",
            version="v1beta1",
            namespace=self.config.namespace,
            plural="virtualservices",
            name=self.config.service_name,
            body=body,
        )
        logger.info("Traffic split: %d%% baseline / %d%% canary", baseline_weight, canary_weight)

    def _collect_metrics(self) -> Dict[str, float]:
        """Pull canary and baseline golden signals from Prometheus."""
        svc, window = self.config.service_name, self.config.metric_window
        canary, baseline = self.config.canary_version, self.config.baseline_version
        return {
            "canary_error_rate": self.prom.get_error_rate(svc, canary, window),
            "canary_latency_p95": self.prom.get_latency_percentile(svc, canary, 0.95, window),
            "canary_success_rate": self.prom.get_success_rate(svc, canary, window),
            "baseline_error_rate": self.prom.get_error_rate(svc, baseline, window),
            "baseline_latency_p95": self.prom.get_latency_percentile(svc, baseline, 0.95, window),
            "baseline_success_rate": self.prom.get_success_rate(svc, baseline, window),
        }

    def _evaluate_metrics(self, m: Dict[str, float]) -> tuple[bool, List[str]]:
        """Return (healthy, reasons). Healthy requires every gate to pass."""
        reasons: List[str] = []

        if m["canary_error_rate"] > self.config.error_rate_threshold:
            reasons.append(
                f"error rate {m['canary_error_rate']:.4f} > {self.config.error_rate_threshold}"
            )
        if m["canary_latency_p95"] > self.config.latency_p95_threshold_ms:
            reasons.append(
                f"p95 {m['canary_latency_p95']:.1f}ms > {self.config.latency_p95_threshold_ms}ms"
            )
        if m["canary_success_rate"] < self.config.success_rate_threshold:
            reasons.append(
                f"success rate {m['canary_success_rate']:.4f} < {self.config.success_rate_threshold}"
            )

        baseline_ceiling = m["baseline_error_rate"] * self.config.baseline_error_multiplier
        if m["canary_error_rate"] > baseline_ceiling:
            reasons.append(
                f"error rate {m['canary_error_rate']:.4f} > "
                f"{self.config.baseline_error_multiplier}x baseline ({baseline_ceiling:.4f})"
            )

        return (len(reasons) == 0, reasons)

    def _rollback(self) -> None:
        """Route 100% of traffic back to the baseline."""
        logger.warning("Rolling back: routing all traffic to baseline")
        self._update_traffic_split(0)
        logger.warning("Rollback complete")

    def _promote_baseline_label(self) -> None:
        """
        After a successful rollout the canary becomes the new baseline. In production this
        means relabeling deployments / bumping replica counts; here we log the intent so the
        controller stays idempotent and side-effect-light for the exercise.
        """
        logger.info(
            "Canary %s is now the production baseline for %s",
            self.config.canary_version, self.config.service_name,
        )
```

### Validation

Run the rollout against a cluster with Istio installed and the `recommendation-model` service
emitting `http_requests_total` / `http_request_duration_seconds_bucket` metrics:

```bash
# Apply manifests
kubectl apply -f k8s/model-deployment.yaml
kubectl apply -f k8s/istio-virtual-service.yaml

# Drive the rollout (short interval for a demo run)
python -c "
from rollout.canary_controller import CanaryController, CanaryConfig
from rollout.prometheus_client import PrometheusClient

cfg = CanaryConfig(
    service_name='recommendation-model',
    namespace='default',
    canary_version='v2',
    baseline_version='v1',
    initial_weight=5,
    step_weight=25,
    step_interval_minutes=1,
)
controller = CanaryController(cfg, PrometheusClient('http://localhost:9090'))
ok = controller.start_rollout()
print('PROMOTED' if ok else 'ROLLED BACK')
"
```

Unit-test the weight progression and evaluation logic without a live cluster by mocking the
Prometheus client:

```python
# tests/test_canary_controller.py
"""Tests for canary evaluation and weight progression."""

from unittest.mock import MagicMock, patch

import pytest

from rollout.canary_controller import CanaryConfig, CanaryController


def test_weight_steps_generated_from_config():
    cfg = CanaryConfig(
        service_name="svc", namespace="ns", canary_version="v2",
        baseline_version="v1", initial_weight=5, step_weight=25,
    )
    assert cfg.weight_steps == [5, 30, 55, 80, 100]


def _controller():
    with patch("rollout.canary_controller.config.load_kube_config"):
        cfg = CanaryConfig(
            service_name="svc", namespace="ns",
            canary_version="v2", baseline_version="v1",
        )
        return CanaryController(cfg, MagicMock())


def test_healthy_canary_passes_all_gates():
    ctrl = _controller()
    healthy, reasons = ctrl._evaluate_metrics({
        "canary_error_rate": 0.01, "canary_latency_p95": 120.0,
        "canary_success_rate": 0.99, "baseline_error_rate": 0.01,
        "baseline_latency_p95": 110.0, "baseline_success_rate": 0.99,
    })
    assert healthy is True
    assert reasons == []


def test_canary_fails_when_error_rate_exceeds_baseline_multiple():
    ctrl = _controller()
    healthy, reasons = ctrl._evaluate_metrics({
        "canary_error_rate": 0.04, "canary_latency_p95": 120.0,
        "canary_success_rate": 0.99, "baseline_error_rate": 0.01,
        "baseline_latency_p95": 110.0, "baseline_success_rate": 0.99,
    })
    assert healthy is False
    assert any("baseline" in r for r in reasons)


def test_canary_fails_on_latency_breach():
    ctrl = _controller()
    healthy, reasons = ctrl._evaluate_metrics({
        "canary_error_rate": 0.0, "canary_latency_p95": 350.0,
        "canary_success_rate": 1.0, "baseline_error_rate": 0.0,
        "baseline_latency_p95": 100.0, "baseline_success_rate": 1.0,
    })
    assert healthy is False
    assert any("p95" in r for r in reasons)

# Run with: pytest tests/test_canary_controller.py -v
```

### Success Criteria

- [ ] Istio `VirtualService` + `DestinationRule` split traffic between `v1` and `v2`
- [ ] Controller progresses through 5% → 30% → 55% → 80% → 100% (or your configured steps)
- [ ] Canary and baseline metrics are pulled from Prometheus per `version` label
- [ ] Evaluation enforces absolute thresholds *and* a baseline-relative error gate
- [ ] Rollback routes 100% of traffic to the baseline on any failed gate
- [ ] A healthy canary is promoted to 100%
- [ ] Unit tests for weight generation and evaluation pass

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Istio**: `VirtualService` controls weights; `DestinationRule` maps subsets to `version` labels.
2. **Weights must sum to 100**: derive baseline weight as `100 - canary_weight`.
3. **Compare like-for-like**: scope every PromQL query by the `version` label so canary and
   baseline use identical queries.
4. **`clamp_min(..., 1)`** in the denominator avoids divide-by-zero before the canary gets traffic.
5. **Two-sided gate**: an absolute latency ceiling catches a globally slow build; a
   baseline-relative error gate catches a canary that is *worse than today* even if under the ceiling.
6. **Soak before judging**: `rate()` over a 5m window needs a few minutes of traffic before the
   numbers are trustworthy — never evaluate immediately after shifting weight.
7. **Production graduation**: real controllers (Flagger, Argo Rollouts) automate exactly this loop;
   build it once by hand, then adopt one of them.

</details>

---
