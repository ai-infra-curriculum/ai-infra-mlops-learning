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
