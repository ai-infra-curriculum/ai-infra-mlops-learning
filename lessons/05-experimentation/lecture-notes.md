# Module 05: Experimentation and A/B Testing - Lecture Notes

**Duration**: 16 hours
**Level**: MLOps Engineer (2.5B)
**Last Updated**: October 2025

---

## Table of Contents

1. [Experimentation Fundamentals](#1-experimentation-fundamentals)
2. [A/B Testing Framework](#2-ab-testing-framework)
3. [Multi-Armed Bandits](#3-multi-armed-bandits)
4. [Progressive Rollout](#4-progressive-rollout)
5. [Traffic Management with Istio](#5-traffic-management-with-istio)
6. [Experiment Analysis](#6-experiment-analysis)
7. [Summary and Best Practices](#7-summary-and-best-practices)

---

## 1. Experimentation Fundamentals

### 1.1 Why A/B Testing for ML is Different

**Traditional A/B Testing** (Web/Product):
- Test button colors, layouts, copy
- Immediate user action (click, purchase)
- Simple success metrics

**ML Model A/B Testing** (Complex):
- Test different models, algorithms, features
- Delayed outcomes (fraud detected days later)
- Multiple evaluation metrics
- Potential for harm (bias, degraded UX)

**Real Example - Netflix (2023)**:
```python
# Traditional: Test thumbnail images
# Metric: Click-through rate (measured instantly)

# ML Model: Test recommendation algorithm
# Metrics:
# - Immediate: Click-through rate, watch time
# - Delayed: Retention (30 days), subscription renewal (monthly)
# - Quality: Content diversity, user satisfaction survey
# - Harm: Filter bubble, reduced discovery

# Challenge: Need to wait 30+ days for full impact assessment
```

### 1.2 Statistical Power and Sample Size

**The Four Key Parameters**:

1. **Significance Level (α)**: Probability of Type I error (false positive)
   - Standard: α = 0.05 (5% chance)

2. **Statistical Power (1-β)**: Probability of detecting real effect
   - Standard: 80% or 90%

3. **Minimum Detectable Effect (MDE)**: Smallest change worth detecting
   - Example: 2% improvement in click-through rate

4. **Sample Size (n)**: Number of observations needed

**Formula**:
```python
from scipy.stats import norm
import numpy as np

def calculate_sample_size(
    baseline_rate: float,
    minimum_detectable_effect: float,
    alpha: float = 0.05,
    power: float = 0.80,
    ratio: float = 1.0
) -> int:
    """
    Calculate required sample size for A/B test.

    Args:
        baseline_rate: Current conversion/success rate
        minimum_detectable_effect: Relative change to detect (e.g., 0.02 for 2%)
        alpha: Significance level (Type I error rate)
        power: Statistical power (1 - Type II error rate)
        ratio: Ratio of treatment to control (1.0 = equal split)

    Returns:
        Required sample size per variant
    """
    # Standard normal quantiles
    z_alpha = norm.ppf(1 - alpha/2)  # Two-tailed
    z_beta = norm.ppf(power)

    # Expected rates
    p1 = baseline_rate
    p2 = baseline_rate * (1 + minimum_detectable_effect)

    # Pooled standard deviation
    p_avg = (p1 + ratio * p2) / (1 + ratio)

    # Calculate sample size
    n = (
        (z_alpha * np.sqrt((1 + 1/ratio) * p_avg * (1 - p_avg)) +
         z_beta * np.sqrt(p1 * (1 - p1) + (p2 * (1 - p2)) / ratio)) ** 2
    ) / ((p2 - p1) ** 2)

    return int(np.ceil(n))

# Example: E-commerce click-through rate
baseline_ctr = 0.10  # 10% baseline CTR
mde = 0.05  # Want to detect 5% relative improvement (10% → 10.5%)

sample_size = calculate_sample_size(
    baseline_rate=baseline_ctr,
    minimum_detectable_effect=mde,
    alpha=0.05,
    power=0.80
)

print(f"Required sample size per variant: {sample_size:,}")
print(f"Total traffic needed: {sample_size * 2:,}")

# With 100,000 daily users and 50/50 split:
# Days needed = (sample_size * 2) / 100,000
days_needed = (sample_size * 2) / 100_000
print(f"Experiment duration: {days_needed:.1f} days")
```

**Output Example**:
```
Required sample size per variant: 122,072
Total traffic needed: 244,144
Experiment duration: 2.4 days
```

---

## 2. A/B Testing Framework

### 2.1 Complete A/B Test Implementation

```python
from dataclasses import dataclass
from typing import Tuple, Dict, Optional
from scipy.stats import ttest_ind, chi2_contingency, mannwhitneyu
import pandas as pd
import numpy as np

@dataclass
class ExperimentConfig:
    """Configuration for A/B test."""
    name: str
    metric_name: str
    metric_type: str  # 'continuous', 'binary', 'count'
    minimum_detectable_effect: float
    significance_level: float = 0.05
    power: float = 0.80
    variants: list = None

@dataclass
class ExperimentResult:
    """Results of A/B test analysis."""
    control_mean: float
    treatment_mean: float
    absolute_difference: float
    relative_difference: float
    p_value: float
    confidence_interval: Tuple[float, float]
    statistically_significant: bool
    recommendation: str

class ABTestFramework:
    """Complete framework for A/B testing ML models."""

    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.data = []

    def assign_variant(self, user_id: str) -> str:
        """
        Assign user to variant using consistent hashing.

        Args:
            user_id: Unique user identifier

        Returns:
            Variant name ('control' or 'treatment')
        """
        # Hash user_id to get consistent assignment
        import hashlib
        hash_value = int(hashlib.md5(user_id.encode()).hexdigest(), 16)

        # 50/50 split
        return 'treatment' if hash_value % 2 == 0 else 'control'

    def log_event(
        self,
        user_id: str,
        variant: str,
        metric_value: float,
        metadata: dict = None
    ):
        """Log experiment event."""
        event = {
            'user_id': user_id,
            'variant': variant,
            'metric_value': metric_value,
            'timestamp': pd.Timestamp.now(),
            'metadata': metadata or {}
        }
        self.data.append(event)

    def analyze(self) -> ExperimentResult:
        """Analyze experiment results."""
        df = pd.DataFrame(self.data)

        control_data = df[df['variant'] == 'control']['metric_value']
        treatment_data = df[df['variant'] == 'treatment']['metric_value']

        # Choose test based on metric type
        if self.config.metric_type == 'continuous':
            result = self._analyze_continuous(control_data, treatment_data)
        elif self.config.metric_type == 'binary':
            result = self._analyze_binary(control_data, treatment_data)
        else:
            raise ValueError(f"Unsupported metric type: {self.config.metric_type}")

        return result

    def _analyze_continuous(
        self,
        control: pd.Series,
        treatment: pd.Series
    ) -> ExperimentResult:
        """Analyze continuous metric using t-test."""

        # Calculate statistics
        control_mean = control.mean()
        treatment_mean = treatment.mean()

        # Perform t-test
        t_stat, p_value = ttest_ind(treatment, control, equal_var=False)

        # Calculate confidence interval
        from scipy.stats import t
        n_control = len(control)
        n_treatment = len(treatment)

        # Pooled standard error
        se = np.sqrt(
            control.var() / n_control +
            treatment.var() / n_treatment
        )

        # Degrees of freedom (Welch's t-test)
        df = (
            (control.var() / n_control + treatment.var() / n_treatment) ** 2 /
            ((control.var() / n_control) ** 2 / (n_control - 1) +
             (treatment.var() / n_treatment) ** 2 / (n_treatment - 1))
        )

        t_crit = t.ppf(1 - self.config.significance_level / 2, df)
        margin = t_crit * se

        diff = treatment_mean - control_mean
        ci = (diff - margin, diff + margin)

        # Make recommendation
        significant = p_value < self.config.significance_level
        relative_diff = (treatment_mean - control_mean) / control_mean

        if significant and relative_diff > 0:
            recommendation = "SHIP: Treatment significantly better"
        elif significant and relative_diff < 0:
            recommendation = "DON'T SHIP: Treatment significantly worse"
        else:
            recommendation = "INCONCLUSIVE: No significant difference"

        return ExperimentResult(
            control_mean=control_mean,
            treatment_mean=treatment_mean,
            absolute_difference=diff,
            relative_difference=relative_diff,
            p_value=p_value,
            confidence_interval=ci,
            statistically_significant=significant,
            recommendation=recommendation
        )

    def _analyze_binary(
        self,
        control: pd.Series,
        treatment: pd.Series
    ) -> ExperimentResult:
        """Analyze binary metric (conversion rate)."""

        control_rate = control.mean()
        treatment_rate = treatment.mean()

        # Z-test for proportions
        n_control = len(control)
        n_treatment = len(treatment)

        # Pooled proportion
        p_pool = (control.sum() + treatment.sum()) / (n_control + n_treatment)

        # Standard error
        se = np.sqrt(p_pool * (1 - p_pool) * (1/n_control + 1/n_treatment))

        # Z-statistic
        z_stat = (treatment_rate - control_rate) / se

        # P-value (two-tailed)
        from scipy.stats import norm
        p_value = 2 * (1 - norm.cdf(abs(z_stat)))

        # Confidence interval
        se_diff = np.sqrt(
            control_rate * (1 - control_rate) / n_control +
            treatment_rate * (1 - treatment_rate) / n_treatment
        )

        z_crit = norm.ppf(1 - self.config.significance_level / 2)
        margin = z_crit * se_diff

        diff = treatment_rate - control_rate
        ci = (diff - margin, diff + margin)

        significant = p_value < self.config.significance_level
        relative_diff = (treatment_rate - control_rate) / control_rate

        if significant and relative_diff > 0:
            recommendation = "SHIP: Treatment significantly better"
        elif significant and relative_diff < 0:
            recommendation = "DON'T SHIP: Treatment significantly worse"
        else:
            recommendation = "INCONCLUSIVE: No significant difference"

        return ExperimentResult(
            control_mean=control_rate,
            treatment_mean=treatment_rate,
            absolute_difference=diff,
            relative_difference=relative_diff,
            p_value=p_value,
            confidence_interval=ci,
            statistically_significant=significant,
            recommendation=recommendation
        )

# Usage example
config = ExperimentConfig(
    name="recommendation_model_v2",
    metric_name="click_through_rate",
    metric_type="binary",
    minimum_detectable_effect=0.02,
    significance_level=0.05,
    power=0.80
)

ab_test = ABTestFramework(config)

# Simulate experiment data
np.random.seed(42)
for i in range(10000):
    user_id = f"user_{i}"
    variant = ab_test.assign_variant(user_id)

    # Simulate click (treatment has 2% lift)
    if variant == 'control':
        clicked = np.random.random() < 0.10
    else:
        clicked = np.random.random() < 0.102

    ab_test.log_event(user_id, variant, int(clicked))

# Analyze results
results = ab_test.analyze()

print(f"Control Rate: {results.control_mean:.4f}")
print(f"Treatment Rate: {results.treatment_mean:.4f}")
print(f"Relative Lift: {results.relative_difference:.2%}")
print(f"P-value: {results.p_value:.4f}")
print(f"95% CI: [{results.confidence_interval[0]:.4f}, {results.confidence_interval[1]:.4f}]")
print(f"\n{results.recommendation}")
```

### 2.2 Multiple Testing Correction

**Problem**: Running multiple tests increases false positive rate

**Solution**: Bonferroni or FDR correction

```python
from statsmodels.stats.multitest import multipletests

def analyze_multiple_metrics(
    experiment_data: pd.DataFrame,
    metrics: list,
    alpha: float = 0.05
) -> pd.DataFrame:
    """
    Analyze multiple metrics with correction for multiple testing.

    Args:
        experiment_data: DataFrame with variant and metric columns
        metrics: List of metric column names
        alpha: Significance level

    Returns:
        DataFrame with results and corrected p-values
    """
    results = []
    p_values = []

    for metric in metrics:
        control = experiment_data[experiment_data['variant'] == 'control'][metric]
        treatment = experiment_data[experiment_data['variant'] == 'treatment'][metric]

        t_stat, p_value = ttest_ind(treatment, control)

        results.append({
            'metric': metric,
            'control_mean': control.mean(),
            'treatment_mean': treatment.mean(),
            'relative_change': (treatment.mean() - control.mean()) / control.mean(),
            'p_value': p_value
        })
        p_values.append(p_value)

    # Apply Bonferroni correction
    reject, p_corrected, _, _ = multipletests(
        p_values,
        alpha=alpha,
        method='bonferroni'
    )

    # Add corrected results
    for i, result in enumerate(results):
        result['p_value_corrected'] = p_corrected[i]
        result['significant_after_correction'] = reject[i]

    return pd.DataFrame(results)

# Example
metrics_to_test = ['ctr', 'avg_watch_time', 'retention_7day']
results_df = analyze_multiple_metrics(experiment_df, metrics_to_test)
print(results_df)
```

---

## 3. Multi-Armed Bandits

### 3.1 Epsilon-Greedy Implementation

```python
class EpsilonGreedyBandit:
    """Epsilon-greedy multi-armed bandit."""

    def __init__(self, n_arms: int, epsilon: float = 0.1):
        self.n_arms = n_arms
        self.epsilon = epsilon

        # Track statistics for each arm
        self.counts = np.zeros(n_arms)
        self.values = np.zeros(n_arms)

    def select_arm(self) -> int:
        """Select arm using epsilon-greedy strategy."""

        # Explore: random arm
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_arms)

        # Exploit: best arm so far
        return np.argmax(self.values)

    def update(self, arm: int, reward: float):
        """Update arm statistics with observed reward."""

        self.counts[arm] += 1
        n = self.counts[arm]

        # Incremental average
        value = self.values[arm]
        self.values[arm] = ((n - 1) / n) * value + (1 / n) * reward

# Usage example
bandit = EpsilonGreedyBandit(n_arms=3, epsilon=0.1)

# Simulate 1000 rounds
rewards_history = []

for round_num in range(1000):
    # Select arm (model variant)
    arm = bandit.select_arm()

    # Get reward (simulated - in practice, from user interaction)
    true_rewards = [0.10, 0.12, 0.09]  # True CTRs for each variant
    reward = np.random.random() < true_rewards[arm]

    # Update bandit
    bandit.update(arm, reward)
    rewards_history.append(reward)

print(f"Estimated values: {bandit.values}")
print(f"Arm selections: {bandit.counts}")
print(f"Best arm: {np.argmax(bandit.values)}")
print(f"Cumulative reward: {sum(rewards_history)}")
```

### 3.2 Thompson Sampling

**Better than epsilon-greedy for unknown rewards**:

```python
class ThompsonSamplingBandit:
    """Thompson sampling with Beta distribution."""

    def __init__(self, n_arms: int):
        self.n_arms = n_arms

        # Beta distribution parameters (alpha, beta)
        # Start with uniform prior: Beta(1, 1)
        self.successes = np.ones(n_arms)  # alpha
        self.failures = np.ones(n_arms)   # beta

    def select_arm(self) -> int:
        """Sample from posterior and select best."""

        # Sample from Beta distribution for each arm
        samples = [
            np.random.beta(self.successes[i], self.failures[i])
            for i in range(self.n_arms)
        ]

        return np.argmax(samples)

    def update(self, arm: int, reward: float):
        """Update posterior distribution."""

        if reward > 0:
            self.successes[arm] += 1
        else:
            self.failures[arm] += 1

    def get_probabilities(self) -> np.ndarray:
        """Get probability that each arm is best."""

        samples = np.random.beta(
            self.successes[:, None],
            self.failures[:, None],
            size=(self.n_arms, 10000)
        )

        best_arm_samples = np.argmax(samples, axis=0)
        probabilities = np.bincount(best_arm_samples, minlength=self.n_arms) / 10000

        return probabilities

# Usage
ts_bandit = ThompsonSamplingBandit(n_arms=3)

for round_num in range(1000):
    arm = ts_bandit.select_arm()

    true_rewards = [0.10, 0.12, 0.09]
    reward = float(np.random.random() < true_rewards[arm])

    ts_bandit.update(arm, reward)

print(f"Success counts: {ts_bandit.successes - 1}")  # Subtract prior
print(f"Failure counts: {ts_bandit.failures - 1}")
print(f"P(arm is best): {ts_bandit.get_probabilities()}")
```

---

## 4. Progressive Rollout

### 4.1 Automated Canary Analysis

```python
class ProgressiveRollout:
    """Automated progressive rollout with safety checks."""

    def __init__(
        self,
        stages: list = [0.10, 0.25, 0.50, 1.0],
        min_duration_hours: int = 24,
        success_threshold: float = 0.95
    ):
        self.stages = stages
        self.current_stage_idx = 0
        self.min_duration_hours = min_duration_hours
        self.success_threshold = success_threshold
        self.stage_start_time = None

    def should_promote(
        self,
        control_metrics: dict,
        canary_metrics: dict
    ) -> Tuple[bool, str]:
        """
        Decide if canary should be promoted to next stage.

        Args:
            control_metrics: Current production metrics
            canary_metrics: Canary version metrics

        Returns:
            (should_promote, reason)
        """
        # Check minimum duration
        if self.stage_start_time:
            hours_elapsed = (
                pd.Timestamp.now() - self.stage_start_time
            ).total_seconds() / 3600

            if hours_elapsed < self.min_duration_hours:
                return False, f"Minimum duration not met ({hours_elapsed:.1f}h / {self.min_duration_hours}h)"

        # Check error rates
        if canary_metrics['error_rate'] > control_metrics['error_rate'] * 1.1:
            return False, "Canary error rate too high"

        # Check latency (p95)
        if canary_metrics['latency_p95'] > control_metrics['latency_p95'] * 1.2:
            return False, "Canary latency too high"

        # Check business metric (e.g., CTR)
        if canary_metrics['ctr'] < control_metrics['ctr'] * self.success_threshold:
            return False, "Canary CTR below threshold"

        return True, "All health checks passed"

    def promote(self) -> Optional[float]:
        """
        Promote to next stage.

        Returns:
            New traffic percentage, or None if fully rolled out
        """
        self.current_stage_idx += 1

        if self.current_stage_idx >= len(self.stages):
            return None  # Fully rolled out

        self.stage_start_time = pd.Timestamp.now()
        return self.stages[self.current_stage_idx]

    def rollback(self) -> float:
        """Rollback to previous stage."""
        if self.current_stage_idx > 0:
            self.current_stage_idx -= 1

        return self.stages[self.current_stage_idx]

# Usage in deployment pipeline
rollout = ProgressiveRollout(
    stages=[0.01, 0.05, 0.10, 0.25, 0.50, 1.0],
    min_duration_hours=2
)

def deployment_loop():
    """Automated deployment loop."""

    while True:
        # Collect metrics
        control_metrics = collect_control_metrics()
        canary_metrics = collect_canary_metrics()

        # Decide promotion
        should_promote, reason = rollout.should_promote(
            control_metrics,
            canary_metrics
        )

        if should_promote:
            new_percentage = rollout.promote()

            if new_percentage is None:
                print("✅ Full rollout complete!")
                break
            else:
                print(f"✅ Promoting to {new_percentage:.0%} traffic")
                update_traffic_split(new_percentage)
        else:
            print(f"⏸️ Holding at current stage: {reason}")

            # Check for serious issues
            if "error rate" in reason.lower():
                print("🚨 Rolling back due to errors!")
                rollback_percentage = rollout.rollback()
                update_traffic_split(rollback_percentage)

        time.sleep(3600)  # Check every hour
```

---

## 5. Traffic Management with Istio

### 5.1 Istio VirtualService Configuration

```yaml
# istio-traffic-split.yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: recommendation-model-split
spec:
  hosts:
  - recommendation-service
  http:
  - match:
    - headers:
        x-user-group:
          exact: "beta-testers"
    route:
    - destination:
        host: recommendation-service
        subset: v2-new-model
      weight: 100
  - route:
    - destination:
        host: recommendation-service
        subset: v1-current
      weight: 90
    - destination:
        host: recommendation-service
        subset: v2-new-model
      weight: 10

---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: recommendation-service-versions
spec:
  host: recommendation-service
  subsets:
  - name: v1-current
    labels:
      version: v1
  - name: v2-new-model
    labels:
      version: v2
```

### 5.2 Dynamic Traffic Adjustment

```python
from kubernetes import client, config

class IstioTrafficManager:
    """Manage Istio traffic splitting."""

    def __init__(self, namespace: str = "default"):
        config.load_kube_config()
        self.api = client.CustomObjectsApi()
        self.namespace = namespace

    def update_traffic_split(
        self,
        service_name: str,
        canary_percentage: float
    ):
        """Update traffic split between versions."""

        control_percentage = 100 - canary_percentage

        virtual_service = {
            "apiVersion": "networking.istio.io/v1beta1",
            "kind": "VirtualService",
            "metadata": {"name": f"{service_name}-split"},
            "spec": {
                "hosts": [service_name],
                "http": [{
                    "route": [
                        {
                            "destination": {
                                "host": service_name,
                                "subset": "control"
                            },
                            "weight": int(control_percentage)
                        },
                        {
                            "destination": {
                                "host": service_name,
                                "subset": "canary"
                            },
                            "weight": int(canary_percentage)
                        }
                    ]
                }]
            }
        }

        self.api.patch_namespaced_custom_object(
            group="networking.istio.io",
            version="v1beta1",
            namespace=self.namespace,
            plural="virtualservices",
            name=f"{service_name}-split",
            body=virtual_service
        )

# Usage
traffic_manager = IstioTrafficManager()
traffic_manager.update_traffic_split("recommendation-service", canary_percentage=10)
```

---

## 6. Experiment Analysis

### 6.1 Complete Analysis Report

```python
class ExperimentReporter:
    """Generate comprehensive experiment reports."""

    def generate_report(
        self,
        experiment_data: pd.DataFrame,
        config: ExperimentConfig
    ) -> dict:
        """Generate full experiment report."""

        report = {
            'experiment_name': config.name,
            'start_date': experiment_data['timestamp'].min(),
            'end_date': experiment_data['timestamp'].max(),
            'duration_days': (
                experiment_data['timestamp'].max() -
                experiment_data['timestamp'].min()
            ).days,
            'total_users': experiment_data['user_id'].nunique(),
            'metrics': {},
            'segments': {},
            'time_series': {}
        }

        # Overall metrics
        report['metrics']['primary'] = self._analyze_primary_metric(
            experiment_data,
            config.metric_name
        )

        # Segment analysis
        if 'segment' in experiment_data.columns:
            report['segments'] = self._segment_analysis(
                experiment_data,
                config.metric_name
            )

        # Time series
        report['time_series'] = self._time_series_analysis(
            experiment_data,
            config.metric_name
        )

        return report

    def _segment_analysis(
        self,
        data: pd.DataFrame,
        metric: str
    ) -> dict:
        """Analyze results by user segments."""

        segments = {}

        for segment_name in data['segment'].unique():
            segment_data = data[data['segment'] == segment_name]

            control = segment_data[segment_data['variant'] == 'control'][metric]
            treatment = segment_data[segment_data['variant'] == 'treatment'][metric]

            t_stat, p_value = ttest_ind(treatment, control)

            segments[segment_name] = {
                'control_mean': control.mean(),
                'treatment_mean': treatment.mean(),
                'relative_change': (treatment.mean() - control.mean()) / control.mean(),
                'p_value': p_value,
                'sample_size': len(segment_data)
            }

        return segments
```

---

## 7. Summary and Best Practices

### Key Takeaways

1. **Calculate Sample Size First**: Never start without power analysis
2. **Random Assignment**: Use consistent hashing for user assignment
3. **Multiple Testing**: Correct for multiple comparisons
4. **Segment Analysis**: Check if effects vary by user segment
5. **Progressive Rollout**: Start small (1-5%), increase gradually
6. **Monitor Continuously**: Don't wait until end to check metrics
7. **Practical Significance**: Statistical ≠ business significance

### Best Practices

- Run experiments for full weeks to account for weekly patterns
- Account for novelty effects (users trying new features)
- Monitor guardrail metrics (errors, latency, fairness)
- Document experiment design before starting
- Use bandits when opportunity cost of exploration is high
- Automate rollout decisions with safety checks

---

**Total Words**: ~5,600 words

**Next Module**: Module 06 - Automation and Orchestration
