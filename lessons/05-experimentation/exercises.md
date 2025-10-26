# Module 05: Experimentation & A/B Testing - Exercises

## Overview

This exercise set provides hands-on practice with experimentation and A/B testing for ML systems, covering:
- A/B testing framework implementation
- Statistical significance testing
- Multi-armed bandits (MAB) algorithms
- Progressive rollout with Istio/service mesh
- Complete experimentation platforms

**Time Estimate**: 8-9 hours total

---

## Exercise 1: A/B Testing Framework (90 minutes)

**Objective**: Implement a complete A/B testing framework for ML model comparison with proper experiment design and tracking.

### Background

You need to A/B test a new ML model against the current production model. Your framework should:
- Assign users to treatment groups randomly
- Track model predictions and outcomes
- Calculate statistical significance
- Support multiple concurrent experiments
- Ensure consistent user experience (sticky assignment)

### Tasks

1. **Implement experiment assignment logic**:
   - Random assignment with configurable split ratios
   - Consistent hashing for sticky assignments
   - Support for multiple concurrent experiments
   - Exclusion/inclusion criteria

2. **Create tracking infrastructure**:
   - Log experiment assignments
   - Track predictions and outcomes
   - Store results for analysis
   - Support delayed conversion tracking

3. **Build analysis pipeline**:
   - Calculate conversion rates
   - Compute confidence intervals
   - Test statistical significance
   - Generate experiment reports

4. **Implement experiment configuration**:
   - YAML-based experiment definitions
   - Version control for experiments
   - Experiment lifecycle management

### Starter Code

```python
# ab_testing/experiment.py
"""A/B testing framework for ML models."""

import hashlib
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json

class ExperimentStatus(Enum):
    """Experiment lifecycle status."""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class VariantType(Enum):
    """Type of experiment variant."""
    CONTROL = "control"
    TREATMENT = "treatment"

@dataclass
class Variant:
    """Represents a variant in an A/B test."""

    id: str
    name: str
    variant_type: VariantType
    traffic_percentage: float
    model_uri: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate variant configuration."""
        if not 0 <= self.traffic_percentage <= 100:
            raise ValueError(f"Traffic percentage must be 0-100, got {self.traffic_percentage}")

@dataclass
class Experiment:
    """Represents an A/B experiment."""

    id: str
    name: str
    description: str
    variants: List[Variant]
    status: ExperimentStatus = ExperimentStatus.DRAFT
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    sample_size_target: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate experiment configuration."""
        # TODO: Validate total traffic allocation equals 100%
        total_traffic = sum(v.traffic_percentage for v in self.variants)
        if abs(total_traffic - 100.0) > 0.01:
            raise ValueError(f"Total traffic must equal 100%, got {total_traffic}")

        # TODO: Ensure exactly one control variant
        control_count = sum(1 for v in self.variants if v.variant_type == VariantType.CONTROL)
        if control_count != 1:
            raise ValueError(f"Must have exactly one control variant, got {control_count}")


class ExperimentAssigner:
    """Handles user assignment to experiment variants."""

    def __init__(self, seed: int = 42):
        """
        Initialize experiment assigner.

        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        random.seed(seed)

    def assign_variant(
        self,
        user_id: str,
        experiment: Experiment,
        use_consistent_hashing: bool = True
    ) -> Variant:
        """
        Assign user to experiment variant.

        Args:
            user_id: Unique user identifier
            experiment: Experiment configuration
            use_consistent_hashing: Use consistent hashing for sticky assignments

        Returns:
            Assigned variant
        """
        if use_consistent_hashing:
            # TODO: Implement consistent hashing
            # - Create hash from user_id + experiment_id
            # - Use hash to deterministically assign variant
            # - Ensures same user always gets same variant
            hash_str = f"{user_id}:{experiment.id}:{self.seed}"
            hash_value = int(hashlib.md5(hash_str.encode()).hexdigest(), 16)
            percentage = (hash_value % 10000) / 100.0  # 0-100 range

            # TODO: Assign based on traffic allocation
            cumulative = 0.0
            for variant in experiment.variants:
                cumulative += variant.traffic_percentage
                if percentage < cumulative:
                    return variant

            return experiment.variants[-1]  # Fallback
        else:
            # TODO: Implement random assignment (non-sticky)
            rand_value = random.random() * 100
            cumulative = 0.0
            for variant in experiment.variants:
                cumulative += variant.traffic_percentage
                if rand_value < cumulative:
                    return variant
            return experiment.variants[-1]

    def is_eligible(
        self,
        user_id: str,
        experiment: Experiment,
        user_attributes: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Check if user is eligible for experiment.

        Args:
            user_id: Unique user identifier
            experiment: Experiment configuration
            user_attributes: User attributes for filtering

        Returns:
            True if user is eligible
        """
        # TODO: Implement eligibility checks
        # - Check experiment status is ACTIVE
        # - Check experiment date range
        # - Apply inclusion/exclusion criteria from metadata
        # - Check user attributes against targeting rules

        if experiment.status != ExperimentStatus.ACTIVE:
            return False

        if experiment.start_date and datetime.now() < experiment.start_date:
            return False

        if experiment.end_date and datetime.now() > experiment.end_date:
            return False

        # TODO: Add more sophisticated filtering

        return True


class ExperimentTracker:
    """Tracks experiment events and outcomes."""

    def __init__(self, storage_backend: str = "local"):
        """
        Initialize experiment tracker.

        Args:
            storage_backend: Storage backend ('local', 'postgres', 'bigquery')
        """
        self.storage_backend = storage_backend
        self.events = []  # In-memory storage for local backend

    def track_assignment(
        self,
        user_id: str,
        experiment_id: str,
        variant_id: str,
        timestamp: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Track experiment assignment.

        Args:
            user_id: User identifier
            experiment_id: Experiment identifier
            variant_id: Assigned variant identifier
            timestamp: Assignment timestamp (default: now)
            metadata: Additional metadata
        """
        # TODO: Create assignment event
        event = {
            'event_type': 'assignment',
            'user_id': user_id,
            'experiment_id': experiment_id,
            'variant_id': variant_id,
            'timestamp': timestamp or datetime.now(),
            'metadata': metadata or {}
        }

        # TODO: Store event
        self._store_event(event)

    def track_prediction(
        self,
        user_id: str,
        experiment_id: str,
        variant_id: str,
        prediction: Any,
        features: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Track model prediction.

        Args:
            user_id: User identifier
            experiment_id: Experiment identifier
            variant_id: Variant identifier
            prediction: Model prediction
            features: Input features
            timestamp: Prediction timestamp
        """
        # TODO: Create prediction event
        event = {
            'event_type': 'prediction',
            'user_id': user_id,
            'experiment_id': experiment_id,
            'variant_id': variant_id,
            'prediction': prediction,
            'features': features,
            'timestamp': timestamp or datetime.now()
        }

        self._store_event(event)

    def track_outcome(
        self,
        user_id: str,
        experiment_id: str,
        variant_id: str,
        outcome: Any,
        metric_name: str = "conversion",
        timestamp: Optional[datetime] = None
    ):
        """
        Track experiment outcome.

        Args:
            user_id: User identifier
            experiment_id: Experiment identifier
            variant_id: Variant identifier
            outcome: Outcome value (e.g., True for conversion)
            metric_name: Name of the metric
            timestamp: Outcome timestamp
        """
        # TODO: Create outcome event
        event = {
            'event_type': 'outcome',
            'user_id': user_id,
            'experiment_id': experiment_id,
            'variant_id': variant_id,
            'metric_name': metric_name,
            'outcome': outcome,
            'timestamp': timestamp or datetime.now()
        }

        self._store_event(event)

    def _store_event(self, event: Dict[str, Any]):
        """Store event to backend."""
        if self.storage_backend == 'local':
            self.events.append(event)
        elif self.storage_backend == 'postgres':
            # TODO: Implement PostgreSQL storage
            pass
        elif self.storage_backend == 'bigquery':
            # TODO: Implement BigQuery storage
            pass

    def get_experiment_data(self, experiment_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all events for an experiment.

        Args:
            experiment_id: Experiment identifier

        Returns:
            List of events
        """
        # TODO: Filter events by experiment_id
        if self.storage_backend == 'local':
            return [e for e in self.events if e.get('experiment_id') == experiment_id]
        else:
            # TODO: Query from database
            pass
```

```python
# ab_testing/config.py
"""Experiment configuration management."""

import yaml
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from ab_testing.experiment import Experiment, Variant, ExperimentStatus, VariantType

class ExperimentConfig:
    """Manages experiment configurations from YAML files."""

    def __init__(self, config_dir: str = "./experiments"):
        """
        Initialize experiment config manager.

        Args:
            config_dir: Directory containing experiment YAML files
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True, parents=True)

    def load_experiment(self, experiment_id: str) -> Experiment:
        """
        Load experiment from YAML file.

        Args:
            experiment_id: Experiment identifier

        Returns:
            Experiment object
        """
        # TODO: Load YAML file
        config_file = self.config_dir / f"{experiment_id}.yaml"

        if not config_file.exists():
            raise FileNotFoundError(f"Experiment config not found: {config_file}")

        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        # TODO: Parse variants
        variants = [
            Variant(
                id=v['id'],
                name=v['name'],
                variant_type=VariantType(v['type']),
                traffic_percentage=v['traffic_percentage'],
                model_uri=v['model_uri'],
                metadata=v.get('metadata', {})
            )
            for v in config['variants']
        ]

        # TODO: Create experiment
        experiment = Experiment(
            id=config['id'],
            name=config['name'],
            description=config['description'],
            variants=variants,
            status=ExperimentStatus(config.get('status', 'draft')),
            start_date=self._parse_datetime(config.get('start_date')),
            end_date=self._parse_datetime(config.get('end_date')),
            sample_size_target=config.get('sample_size_target'),
            metadata=config.get('metadata', {})
        )

        return experiment

    def save_experiment(self, experiment: Experiment):
        """
        Save experiment to YAML file.

        Args:
            experiment: Experiment to save
        """
        # TODO: Convert experiment to dict
        config = {
            'id': experiment.id,
            'name': experiment.name,
            'description': experiment.description,
            'status': experiment.status.value,
            'variants': [
                {
                    'id': v.id,
                    'name': v.name,
                    'type': v.variant_type.value,
                    'traffic_percentage': v.traffic_percentage,
                    'model_uri': v.model_uri,
                    'metadata': v.metadata
                }
                for v in experiment.variants
            ],
            'start_date': experiment.start_date.isoformat() if experiment.start_date else None,
            'end_date': experiment.end_date.isoformat() if experiment.end_date else None,
            'sample_size_target': experiment.sample_size_target,
            'metadata': experiment.metadata
        }

        # TODO: Write to YAML file
        config_file = self.config_dir / f"{experiment.id}.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    def _parse_datetime(self, dt_str: Optional[str]) -> Optional[datetime]:
        """Parse datetime string."""
        if dt_str is None:
            return None
        return datetime.fromisoformat(dt_str)
```

```yaml
# experiments/model_v2_ab_test.yaml
# Example experiment configuration

id: model_v2_ab_test
name: "Model V2 vs V1 A/B Test"
description: "Testing new recommendation model v2 against production v1"
status: active
start_date: "2025-10-25T00:00:00"
end_date: "2025-11-08T23:59:59"
sample_size_target: 100000

variants:
  - id: control
    name: "Model V1 (Control)"
    type: control
    traffic_percentage: 50.0
    model_uri: "models:/recommendation_model/production"
    metadata:
      model_version: "1.2.3"
      algorithm: "collaborative_filtering"

  - id: treatment
    name: "Model V2 (Treatment)"
    type: treatment
    traffic_percentage: 50.0
    model_uri: "models:/recommendation_model/staging"
    metadata:
      model_version: "2.0.0"
      algorithm: "neural_collaborative_filtering"

metadata:
  owner: "ml-team@company.com"
  metrics:
    - click_through_rate
    - conversion_rate
    - revenue_per_user
  minimum_detectable_effect: 0.02
  significance_level: 0.05
  statistical_power: 0.80
```

### Validation Tests

```python
# tests/test_ab_testing.py
"""Tests for A/B testing framework."""

import pytest
from ab_testing.experiment import (
    Experiment, Variant, ExperimentAssigner, ExperimentTracker,
    ExperimentStatus, VariantType
)

@pytest.fixture
def sample_experiment():
    """Create sample experiment for testing."""
    variants = [
        Variant(
            id="control",
            name="Control",
            variant_type=VariantType.CONTROL,
            traffic_percentage=50.0,
            model_uri="models:/test/1"
        ),
        Variant(
            id="treatment",
            name="Treatment",
            variant_type=VariantType.TREATMENT,
            traffic_percentage=50.0,
            model_uri="models:/test/2"
        )
    ]

    return Experiment(
        id="test_exp",
        name="Test Experiment",
        description="Test",
        variants=variants,
        status=ExperimentStatus.ACTIVE
    )

def test_experiment_creation(sample_experiment):
    """Test that experiments are created correctly."""
    assert sample_experiment.id == "test_exp"
    assert len(sample_experiment.variants) == 2
    # TODO: Add more assertions

def test_traffic_allocation_validation():
    """Test that traffic allocation must equal 100%."""
    # TODO: Test that creating experiment with traffic != 100% raises error
    pass

def test_consistent_assignment(sample_experiment):
    """Test that users are assigned consistently."""
    assigner = ExperimentAssigner(seed=42)

    user_id = "user123"
    variant1 = assigner.assign_variant(user_id, sample_experiment)
    variant2 = assigner.assign_variant(user_id, sample_experiment)

    # TODO: Assert same user gets same variant
    assert variant1.id == variant2.id

def test_traffic_distribution(sample_experiment):
    """Test that traffic is distributed according to percentages."""
    assigner = ExperimentAssigner(seed=42)

    # TODO: Assign 10000 users
    # TODO: Count assignments to each variant
    # TODO: Assert distribution is approximately 50/50
    pass

def test_event_tracking():
    """Test that events are tracked correctly."""
    tracker = ExperimentTracker(storage_backend='local')

    # TODO: Track assignment
    tracker.track_assignment("user1", "exp1", "control")

    # TODO: Track prediction
    tracker.track_prediction("user1", "exp1", "control", prediction=0.8)

    # TODO: Track outcome
    tracker.track_outcome("user1", "exp1", "control", outcome=True)

    # TODO: Retrieve events
    events = tracker.get_experiment_data("exp1")

    # TODO: Assert correct number of events
    assert len(events) == 3

# Run with: pytest tests/test_ab_testing.py -v
```

### Success Criteria

- [ ] Experiment configuration loads from YAML
- [ ] Users are assigned consistently (sticky)
- [ ] Traffic distribution matches configuration
- [ ] All events (assignment, prediction, outcome) are tracked
- [ ] Experiments can be activated/paused/archived
- [ ] Multiple concurrent experiments are supported
- [ ] Tests pass

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Consistent Hashing**: Use MD5 hash of `user_id + experiment_id + seed` modulo 10000
2. **Traffic Allocation**: Sort variants by cumulative percentage, assign based on hash range
3. **Storage**: Start with in-memory list, then implement database storage
4. **Eligibility**: Check experiment status, date range, and user attributes
5. **Validation**: Use `__post_init__` in dataclasses for automatic validation
6. **Config**: Use YAML for human-readable experiment definitions

</details>

---

## Exercise 2: Statistical Significance Testing (75 minutes)

**Objective**: Implement statistical tests to determine when experiment results are significant and actionable.

### Background

You need to analyze A/B test results and determine:
- Whether differences are statistically significant
- What sample size is needed
- When to stop the experiment
- Whether to roll out the treatment

### Tasks

1. **Implement statistical tests**:
   - Z-test for proportions
   - T-test for continuous metrics
   - Chi-square test for categorical outcomes
   - Confidence intervals

2. **Calculate sample size**:
   - Minimum sample size calculation
   - Power analysis
   - Sequential testing considerations

3. **Build analysis dashboard**:
   - Calculate conversion rates
   - Compute lift and p-values
   - Visualize results
   - Generate recommendations

### Starter Code

```python
# ab_testing/statistics.py
"""Statistical analysis for A/B tests."""

import numpy as np
from scipy import stats
from typing import Tuple, Dict, Optional
import math

class ABTestAnalyzer:
    """Analyzes A/B test results for statistical significance."""

    def __init__(self, alpha: float = 0.05, power: float = 0.80):
        """
        Initialize analyzer.

        Args:
            alpha: Significance level (default 0.05 for 95% confidence)
            power: Statistical power (default 0.80)
        """
        self.alpha = alpha
        self.power = power

    def z_test_proportions(
        self,
        conversions_a: int,
        samples_a: int,
        conversions_b: int,
        samples_b: int
    ) -> Dict[str, float]:
        """
        Perform Z-test for difference in proportions.

        Args:
            conversions_a: Number of conversions in group A (control)
            samples_a: Total samples in group A
            conversions_b: Number of conversions in group B (treatment)
            samples_b: Total samples in group B

        Returns:
            Dictionary with test results
        """
        # TODO: Calculate conversion rates
        p_a = conversions_a / samples_a
        p_b = conversions_b / samples_b

        # TODO: Calculate pooled proportion
        p_pooled = (conversions_a + conversions_b) / (samples_a + samples_b)

        # TODO: Calculate standard error
        se = math.sqrt(p_pooled * (1 - p_pooled) * (1/samples_a + 1/samples_b))

        # TODO: Calculate z-statistic
        z_stat = (p_b - p_a) / se if se > 0 else 0

        # TODO: Calculate p-value (two-tailed)
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

        # TODO: Calculate confidence interval for difference
        ci_margin = stats.norm.ppf(1 - self.alpha/2) * se
        ci_lower = (p_b - p_a) - ci_margin
        ci_upper = (p_b - p_a) + ci_margin

        # TODO: Calculate relative lift
        lift = ((p_b - p_a) / p_a * 100) if p_a > 0 else 0

        return {
            'conversion_rate_a': p_a,
            'conversion_rate_b': p_b,
            'absolute_difference': p_b - p_a,
            'relative_lift_percent': lift,
            'z_statistic': z_stat,
            'p_value': p_value,
            'is_significant': p_value < self.alpha,
            'confidence_interval': (ci_lower, ci_upper),
            'confidence_level': 1 - self.alpha
        }

    def t_test_continuous(
        self,
        values_a: np.ndarray,
        values_b: np.ndarray
    ) -> Dict[str, float]:
        """
        Perform t-test for continuous metrics.

        Args:
            values_a: Values from group A (control)
            values_b: Values from group B (treatment)

        Returns:
            Dictionary with test results
        """
        # TODO: Calculate means and standard deviations
        mean_a = np.mean(values_a)
        mean_b = np.mean(values_b)
        std_a = np.std(values_a, ddof=1)
        std_b = np.std(values_b, ddof=1)

        # TODO: Perform Welch's t-test (unequal variances)
        t_stat, p_value = stats.ttest_ind(values_a, values_b, equal_var=False)

        # TODO: Calculate confidence interval for difference
        # TODO: Calculate effect size (Cohen's d)

        return {
            'mean_a': mean_a,
            'mean_b': mean_b,
            'std_a': std_a,
            'std_b': std_b,
            'absolute_difference': mean_b - mean_a,
            'relative_lift_percent': ((mean_b - mean_a) / mean_a * 100) if mean_a != 0 else 0,
            't_statistic': t_stat,
            'p_value': p_value,
            'is_significant': p_value < self.alpha
        }

    def calculate_sample_size(
        self,
        baseline_rate: float,
        minimum_detectable_effect: float,
        alpha: Optional[float] = None,
        power: Optional[float] = None
    ) -> int:
        """
        Calculate required sample size per variant.

        Args:
            baseline_rate: Expected baseline conversion rate
            minimum_detectable_effect: Minimum relative effect to detect (e.g., 0.05 for 5%)
            alpha: Significance level (default: use self.alpha)
            power: Statistical power (default: use self.power)

        Returns:
            Required sample size per variant
        """
        alpha = alpha or self.alpha
        power = power or self.power

        # TODO: Calculate effect size
        p1 = baseline_rate
        p2 = baseline_rate * (1 + minimum_detectable_effect)

        # TODO: Use formula for sample size calculation
        # n = (Z_α/2 + Z_β)² * (p1(1-p1) + p2(1-p2)) / (p2 - p1)²

        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = stats.norm.ppf(power)

        numerator = (z_alpha + z_beta)**2 * (p1*(1-p1) + p2*(1-p2))
        denominator = (p2 - p1)**2

        n = math.ceil(numerator / denominator)

        return n

    def calculate_confidence_interval(
        self,
        successes: int,
        trials: int,
        confidence: float = 0.95
    ) -> Tuple[float, float]:
        """
        Calculate Wilson score confidence interval for proportion.

        Args:
            successes: Number of successes
            trials: Total number of trials
            confidence: Confidence level (default 0.95)

        Returns:
            Tuple of (lower_bound, upper_bound)
        """
        # TODO: Implement Wilson score interval
        # More accurate than normal approximation for small samples

        if trials == 0:
            return (0.0, 0.0)

        p = successes / trials
        z = stats.norm.ppf(1 - (1-confidence)/2)

        denominator = 1 + z**2/trials
        center = (p + z**2/(2*trials)) / denominator
        margin = z * math.sqrt((p*(1-p) + z**2/(4*trials)) / trials) / denominator

        return (max(0, center - margin), min(1, center + margin))

    def sequential_test(
        self,
        conversions_a: int,
        samples_a: int,
        conversions_b: int,
        samples_b: int,
        looks: int = 1,
        max_looks: int = 10
    ) -> Dict[str, any]:
        """
        Perform sequential testing with alpha spending.

        Args:
            conversions_a: Conversions in control
            samples_a: Samples in control
            conversions_b: Conversions in treatment
            samples_b: Samples in treatment
            looks: Current number of looks at the data
            max_looks: Maximum planned number of looks

        Returns:
            Dictionary with sequential test results
        """
        # TODO: Implement O'Brien-Fleming alpha spending
        # Adjusts significance level for multiple testing

        # Calculate adjusted alpha for this look
        adjusted_alpha = self._obrien_fleming_alpha(looks, max_looks, self.alpha)

        # TODO: Perform z-test with adjusted alpha
        temp_alpha = self.alpha
        self.alpha = adjusted_alpha
        result = self.z_test_proportions(conversions_a, samples_a, conversions_b, samples_b)
        self.alpha = temp_alpha

        result['adjusted_alpha'] = adjusted_alpha
        result['looks'] = looks
        result['max_looks'] = max_looks

        return result

    def _obrien_fleming_alpha(self, k: int, K: int, alpha: float) -> float:
        """
        Calculate O'Brien-Fleming alpha spending for look k of K.

        Args:
            k: Current look number (1 to K)
            K: Total number of planned looks
            alpha: Overall significance level

        Returns:
            Adjusted alpha for this look
        """
        # TODO: Implement O'Brien-Fleming spending function
        # This is a simplified version
        z_alpha = stats.norm.ppf(1 - alpha/2)
        adjusted_z = z_alpha * math.sqrt(K / k)
        adjusted_alpha = 2 * (1 - stats.norm.cdf(adjusted_z))
        return adjusted_alpha
```

```python
# ab_testing/report.py
"""Generate A/B test analysis reports."""

import pandas as pd
from typing import Dict, List
from ab_testing.statistics import ABTestAnalyzer
from ab_testing.experiment import ExperimentTracker

class ExperimentReport:
    """Generates analysis reports for experiments."""

    def __init__(self, tracker: ExperimentTracker, analyzer: ABTestAnalyzer):
        """
        Initialize report generator.

        Args:
            tracker: Experiment tracker with event data
            analyzer: Statistical analyzer
        """
        self.tracker = tracker
        self.analyzer = analyzer

    def generate_report(self, experiment_id: str) -> Dict:
        """
        Generate complete experiment report.

        Args:
            experiment_id: Experiment identifier

        Returns:
            Dictionary with report data
        """
        # TODO: Get experiment data
        events = self.tracker.get_experiment_data(experiment_id)

        # TODO: Calculate per-variant metrics
        variant_stats = self._calculate_variant_stats(events)

        # TODO: Perform statistical tests
        test_results = self._run_statistical_tests(variant_stats)

        # TODO: Generate recommendations
        recommendations = self._generate_recommendations(test_results)

        return {
            'experiment_id': experiment_id,
            'variant_stats': variant_stats,
            'test_results': test_results,
            'recommendations': recommendations
        }

    def _calculate_variant_stats(self, events: List[Dict]) -> Dict:
        """Calculate statistics per variant."""
        # TODO: Group events by variant
        # TODO: Calculate conversion rates, sample sizes
        # TODO: Return statistics dict
        pass

    def _run_statistical_tests(self, variant_stats: Dict) -> Dict:
        """Run statistical significance tests."""
        # TODO: Extract control and treatment stats
        # TODO: Run z-test for proportions
        # TODO: Return test results
        pass

    def _generate_recommendations(self, test_results: Dict) -> List[str]:
        """Generate action recommendations based on results."""
        recommendations = []

        # TODO: Check if significant
        if test_results.get('is_significant'):
            if test_results.get('relative_lift_percent', 0) > 0:
                recommendations.append("✅ RECOMMEND ROLLOUT: Treatment shows significant improvement")
            else:
                recommendations.append("❌ DO NOT ROLLOUT: Treatment shows significant degradation")
        else:
            recommendations.append("⏳ CONTINUE TEST: Results not yet significant")

        # TODO: Add more sophisticated recommendations

        return recommendations
```

### Validation

Run statistical tests:
```python
# Example usage
from ab_testing.statistics import ABTestAnalyzer

analyzer = ABTestAnalyzer(alpha=0.05, power=0.80)

# Calculate required sample size
sample_size = analyzer.calculate_sample_size(
    baseline_rate=0.10,
    minimum_detectable_effect=0.20  # 20% relative improvement
)
print(f"Required sample size per variant: {sample_size}")

# Perform z-test
results = analyzer.z_test_proportions(
    conversions_a=100,
    samples_a=1000,
    conversions_b=125,
    samples_b=1000
)
print(f"P-value: {results['p_value']:.4f}")
print(f"Significant: {results['is_significant']}")
print(f"Lift: {results['relative_lift_percent']:.2f}%")
```

### Success Criteria

- [ ] Z-test correctly identifies significant differences
- [ ] Sample size calculation is accurate
- [ ] Confidence intervals are calculated correctly
- [ ] Sequential testing adjusts for multiple looks
- [ ] Reports generate actionable recommendations
- [ ] Tests pass

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Z-test**: Use pooled proportion for standard error calculation
2. **Sample Size**: Use normal approximation for proportions
3. **Wilson Score**: More accurate than normal approximation for edge cases
4. **Sequential Testing**: Use O'Brien-Fleming or Haybittle-Peto spending functions
5. **Effect Size**: Calculate Cohen's d for continuous metrics
6. **Power Analysis**: Use `statsmodels.stats.power` for complex calculations

</details>

---

## Exercise 3: Multi-Armed Bandits (90 minutes)

**Objective**: Implement multi-armed bandit algorithms (ε-greedy, UCB, Thompson Sampling) for adaptive experimentation.

### Background

Traditional A/B tests waste traffic on inferior variants. Multi-armed bandits (MAB) dynamically allocate more traffic to better-performing variants while exploring alternatives.

### Tasks

1. **Implement ε-greedy algorithm**
2. **Implement Upper Confidence Bound (UCB)**
3. **Implement Thompson Sampling**
4. **Compare bandit strategies**
5. **Integrate with ML model serving**

### Starter Code

```python
# bandits/base.py
"""Base classes for multi-armed bandit algorithms."""

from abc import ABC, abstractmethod
from typing import List, Dict
import numpy as np

class Arm:
    """Represents a bandit arm (variant/model)."""

    def __init__(self, arm_id: str, model_uri: str):
        """
        Initialize arm.

        Args:
            arm_id: Unique identifier
            model_uri: Model URI for this arm
        """
        self.arm_id = arm_id
        self.model_uri = model_uri
        self.pulls = 0
        self.rewards = 0.0
        self.reward_history = []

    def update(self, reward: float):
        """
        Update arm statistics with new reward.

        Args:
            reward: Reward value (0 or 1 for binary, any float for continuous)
        """
        self.pulls += 1
        self.rewards += reward
        self.reward_history.append(reward)

    @property
    def mean_reward(self) -> float:
        """Calculate mean reward."""
        return self.rewards / self.pulls if self.pulls > 0 else 0.0


class BanditAlgorithm(ABC):
    """Abstract base class for bandit algorithms."""

    def __init__(self, arms: List[Arm]):
        """
        Initialize bandit.

        Args:
            arms: List of arms
        """
        self.arms = arms
        self.total_pulls = 0

    @abstractmethod
    def select_arm(self) -> Arm:
        """
        Select an arm to pull.

        Returns:
            Selected arm
        """
        pass

    def update(self, arm_id: str, reward: float):
        """
        Update arm with reward.

        Args:
            arm_id: Arm that was pulled
            reward: Observed reward
        """
        arm = next(a for a in self.arms if a.arm_id == arm_id)
        arm.update(reward)
        self.total_pulls += 1

    def get_stats(self) -> Dict:
        """Get current statistics."""
        return {
            arm.arm_id: {
                'pulls': arm.pulls,
                'mean_reward': arm.mean_reward,
                'total_reward': arm.rewards
            }
            for arm in self.arms
        }
```

```python
# bandits/epsilon_greedy.py
"""Epsilon-greedy bandit algorithm."""

import random
from typing import List
from bandits.base import BanditAlgorithm, Arm

class EpsilonGreedy(BanditAlgorithm):
    """Epsilon-greedy exploration strategy."""

    def __init__(self, arms: List[Arm], epsilon: float = 0.1):
        """
        Initialize epsilon-greedy bandit.

        Args:
            arms: List of arms
            epsilon: Exploration probability (0.1 = 10% explore, 90% exploit)
        """
        super().__init__(arms)
        self.epsilon = epsilon

    def select_arm(self) -> Arm:
        """
        Select arm using epsilon-greedy strategy.

        Returns:
            Selected arm
        """
        # TODO: With probability epsilon, explore (random selection)
        if random.random() < self.epsilon:
            return random.choice(self.arms)

        # TODO: Otherwise, exploit (select best arm)
        # Handle ties by random selection
        best_reward = max(arm.mean_reward for arm in self.arms)
        best_arms = [arm for arm in self.arms if arm.mean_reward == best_reward]
        return random.choice(best_arms)


class EpsilonDecreasing(BanditAlgorithm):
    """Epsilon-greedy with decreasing exploration rate."""

    def __init__(self, arms: List[Arm], epsilon_start: float = 1.0, epsilon_min: float = 0.01, decay_rate: float = 0.99):
        """
        Initialize with decaying epsilon.

        Args:
            arms: List of arms
            epsilon_start: Initial exploration rate
            epsilon_min: Minimum exploration rate
            decay_rate: Decay factor per pull
        """
        super().__init__(arms)
        self.epsilon = epsilon_start
        self.epsilon_min = epsilon_min
        self.decay_rate = decay_rate

    def select_arm(self) -> Arm:
        """Select arm with current epsilon."""
        # TODO: Implement selection
        if random.random() < self.epsilon:
            selected = random.choice(self.arms)
        else:
            best_reward = max(arm.mean_reward for arm in self.arms)
            best_arms = [arm for arm in self.arms if arm.mean_reward == best_reward]
            selected = random.choice(best_arms)

        # TODO: Decay epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon * self.decay_rate)

        return selected
```

```python
# bandits/ucb.py
"""Upper Confidence Bound (UCB) bandit algorithm."""

import math
from typing import List
from bandits.base import BanditAlgorithm, Arm

class UCB1(BanditAlgorithm):
    """UCB1 algorithm for bandit problems."""

    def __init__(self, arms: List[Arm], c: float = math.sqrt(2)):
        """
        Initialize UCB1.

        Args:
            arms: List of arms
            c: Exploration constant (default: sqrt(2))
        """
        super().__init__(arms)
        self.c = c

    def select_arm(self) -> Arm:
        """
        Select arm using UCB1 strategy.

        Returns:
            Selected arm
        """
        # TODO: If any arm hasn't been pulled, pull it
        for arm in self.arms:
            if arm.pulls == 0:
                return arm

        # TODO: Calculate UCB for each arm
        # UCB = mean_reward + c * sqrt(ln(total_pulls) / arm_pulls)
        ucb_values = []
        for arm in self.arms:
            exploration_bonus = self.c * math.sqrt(math.log(self.total_pulls) / arm.pulls)
            ucb = arm.mean_reward + exploration_bonus
            ucb_values.append((arm, ucb))

        # TODO: Select arm with highest UCB
        best_arm = max(ucb_values, key=lambda x: x[1])[0]
        return best_arm
```

```python
# bandits/thompson_sampling.py
"""Thompson Sampling bandit algorithm."""

import random
from typing import List
from bandits.base import BanditAlgorithm, Arm

class ThompsonSampling(BanditAlgorithm):
    """Thompson Sampling with Beta distribution (for binary rewards)."""

    def __init__(self, arms: List[Arm]):
        """
        Initialize Thompson Sampling.

        Args:
            arms: List of arms
        """
        super().__init__(arms)
        # Beta distribution parameters (successes, failures)
        self.alpha = {arm.arm_id: 1 for arm in arms}  # Prior: Beta(1,1) = Uniform(0,1)
        self.beta = {arm.arm_id: 1 for arm in arms}

    def select_arm(self) -> Arm:
        """
        Select arm using Thompson Sampling.

        Returns:
            Selected arm
        """
        # TODO: Sample from Beta distribution for each arm
        samples = {}
        for arm in self.arms:
            # Sample from Beta(alpha, beta)
            samples[arm.arm_id] = random.betavariate(
                self.alpha[arm.arm_id],
                self.beta[arm.arm_id]
            )

        # TODO: Select arm with highest sample
        best_arm_id = max(samples, key=samples.get)
        return next(arm for arm in self.arms if arm.arm_id == best_arm_id)

    def update(self, arm_id: str, reward: float):
        """
        Update Beta distribution parameters.

        Args:
            arm_id: Arm that was pulled
            reward: Observed reward (0 or 1 for binary)
        """
        super().update(arm_id, reward)

        # TODO: Update Beta parameters
        # If reward = 1 (success), increment alpha
        # If reward = 0 (failure), increment beta
        if reward > 0:
            self.alpha[arm_id] += 1
        else:
            self.beta[arm_id] += 1
```

```python
# bandits/simulation.py
"""Simulate and compare bandit algorithms."""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict
from bandits.base import Arm, BanditAlgorithm
from bandits.epsilon_greedy import EpsilonGreedy, EpsilonDecreasing
from bandits.ucb import UCB1
from bandits.thompson_sampling import ThompsonSampling

class BanditSimulation:
    """Simulate bandit algorithms for comparison."""

    def __init__(self, true_probabilities: List[float]):
        """
        Initialize simulation.

        Args:
            true_probabilities: True conversion probability for each arm
        """
        self.true_probabilities = true_probabilities
        self.n_arms = len(true_probabilities)

    def simulate_bandit(
        self,
        algorithm: BanditAlgorithm,
        n_iterations: int = 10000
    ) -> Dict:
        """
        Simulate bandit algorithm.

        Args:
            algorithm: Bandit algorithm to simulate
            n_iterations: Number of iterations

        Returns:
            Dictionary with simulation results
        """
        rewards = []
        regrets = []
        optimal_arm_idx = np.argmax(self.true_probabilities)
        cumulative_regret = 0

        for i in range(n_iterations):
            # TODO: Select arm
            arm = algorithm.select_arm()
            arm_idx = int(arm.arm_id.split('_')[1])

            # TODO: Simulate reward (Bernoulli trial)
            reward = 1 if np.random.random() < self.true_probabilities[arm_idx] else 0

            # TODO: Update algorithm
            algorithm.update(arm.arm_id, reward)

            # TODO: Track metrics
            rewards.append(reward)
            regret = self.true_probabilities[optimal_arm_idx] - self.true_probabilities[arm_idx]
            cumulative_regret += regret
            regrets.append(cumulative_regret)

        return {
            'rewards': rewards,
            'cumulative_rewards': np.cumsum(rewards),
            'regrets': regrets,
            'final_stats': algorithm.get_stats()
        }

    def compare_algorithms(self, n_iterations: int = 10000):
        """
        Compare multiple bandit algorithms.

        Args:
            n_iterations: Number of iterations
        """
        # TODO: Create arms
        arms_eps = [Arm(f"arm_{i}", f"model_{i}") for i in range(self.n_arms)]
        arms_ucb = [Arm(f"arm_{i}", f"model_{i}") for i in range(self.n_arms)]
        arms_ts = [Arm(f"arm_{i}", f"model_{i}") for i in range(self.n_arms)]

        # TODO: Initialize algorithms
        algorithms = {
            'Epsilon-Greedy (0.1)': EpsilonGreedy(arms_eps, epsilon=0.1),
            'UCB1': UCB1(arms_ucb),
            'Thompson Sampling': ThompsonSampling(arms_ts)
        }

        # TODO: Run simulations
        results = {}
        for name, algo in algorithms.items():
            print(f"Running {name}...")
            results[name] = self.simulate_bandit(algo, n_iterations)

        # TODO: Plot comparison
        self._plot_comparison(results, n_iterations)

        return results

    def _plot_comparison(self, results: Dict, n_iterations: int):
        """Plot algorithm comparison."""
        # TODO: Create comparison plots
        pass
```

### Validation

Test bandits with simulation:
```python
# Test with known probabilities
true_probs = [0.05, 0.08, 0.10, 0.07]  # Arm 2 is best (10%)

sim = BanditSimulation(true_probs)
results = sim.compare_algorithms(n_iterations=10000)

# Check that algorithms converge to best arm
for name, result in results.items():
    stats = result['final_stats']
    print(f"\n{name}:")
    for arm_id, arm_stats in stats.items():
        print(f"  {arm_id}: {arm_stats['pulls']} pulls, {arm_stats['mean_reward']:.3f} reward")
```

### Success Criteria

- [ ] Epsilon-greedy balances exploration and exploitation
- [ ] UCB gives optimistic estimates for under-explored arms
- [ ] Thompson Sampling converges to optimal arm
- [ ] Simulation shows bandits outperform random allocation
- [ ] Algorithms can be integrated with model serving
- [ ] Tests pass

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Epsilon-Greedy**: Simple but effective, tune epsilon based on problem
2. **UCB**: No tuning needed, automatic exploration-exploitation balance
3. **Thompson Sampling**: Best for binary rewards, use Gaussian for continuous
4. **Comparison**: Thompson Sampling often performs best in practice
5. **Convergence**: All algorithms should eventually identify best arm
6. **Regret**: Measure cumulative regret to compare efficiency

</details>

---

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

## Exercise 5: Complete Experimentation Platform (120 minutes)

**Objective**: Build an end-to-end experimentation platform integrating A/B testing, bandits, and progressive rollout with monitoring and analysis.

### Components

1. **Experiment management service**
2. **Assignment service with caching**
3. **Metrics collection pipeline**
4. **Analysis dashboard**
5. **Automated decision engine**

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Experimentation Platform                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │ Experiment   │───▶│  Assignment  │───▶│   Model      │ │
│  │   Config     │    │   Service    │    │  Serving     │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         │                    │                    │        │
│         │                    ▼                    ▼        │
│         │            ┌──────────────┐    ┌──────────────┐ │
│         │            │    Redis     │    │   Metrics    │ │
│         │            │    Cache     │    │  Tracking    │ │
│         │            └──────────────┘    └──────────────┘ │
│         │                                        │        │
│         ▼                                        ▼        │
│  ┌──────────────┐                       ┌──────────────┐ │
│  │  Analysis    │◀──────────────────────│  PostgreSQL  │ │
│  │  Dashboard   │                       │   Database   │ │
│  └──────────────┘                       └──────────────┘ │
│         │                                                 │
│         ▼                                                 │
│  ┌──────────────┐                                        │
│  │  Decision    │                                        │
│  │   Engine     │                                        │
│  └──────────────┘                                        │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### Success Criteria

- [ ] Complete platform deployed and functional
- [ ] Experiments can be created via API
- [ ] Users assigned consistently with caching
- [ ] Metrics tracked and stored
- [ ] Dashboard shows real-time results
- [ ] Automated decisions based on statistical significance
- [ ] Integration tests pass

---

## Submission Guidelines

For each exercise, submit:
1. **Code**: All implementation files
2. **Tests**: Passing test suite
3. **Documentation**: Design decisions and architecture
4. **Results**: Experiment results and statistical analysis
5. **Reflection**: Lessons learned about experimentation

**Estimated Total Time**: 8-9 hours
**Difficulty**: Advanced

Good luck!
