## Exercise 2: Bias Mitigation Strategies (90 minutes)

**Objective**: Implement bias mitigation techniques using pre-processing, in-processing, and post-processing approaches.

### Background

After detecting bias in Exercise 1, you need to mitigate it. Implement multiple mitigation strategies:
- Pre-processing: Reweighing, sampling techniques
- In-processing: Fairness-constrained models
- Post-processing: Threshold optimization

### Tasks

1. **Implement reweighing for pre-processing**
2. **Apply adversarial debiasing**
3. **Optimize decision thresholds per group**
4. **Compare mitigation strategies**
5. **Evaluate fairness-accuracy tradeoffs**

### Starter Code

```python
# src/governance/bias_mitigation.py
"""Bias mitigation strategies."""

from fairlearn.reductions import ExponentiatedGradient, DemographicParity, EqualizedOdds
from fairlearn.postprocessing import ThresholdOptimizer
from fairlearn.preprocessing import CorrelationRemover
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class MitigationResult:
    """Results from bias mitigation."""
    model: Any
    strategy: str
    accuracy: float
    fairness_metrics: Dict[str, float]
    fairness_improvement: float
    accuracy_cost: float


class BiasM itigator:
    """Implement bias mitigation strategies."""

    def __init__(self, base_estimator=None):
        """
        Initialize bias mitigator.

        Args:
            base_estimator: Base ML model (default: LogisticRegression)
        """
        self.base_estimator = base_estimator or LogisticRegression()
        self.mitigated_models = {}

    def preprocess_reweighing(
        self,
        X_train: pd.DataFrame,
        y_train: np.ndarray,
        sensitive_features: pd.DataFrame
    ) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray]:
        """
        Reweigh training samples to reduce bias.

        Args:
            X_train: Training features
            y_train: Training labels
            sensitive_features: Sensitive attributes

        Returns:
            Tuple of (X_train, y_train, sample_weights)
        """
        # TODO: Calculate sample weights to balance sensitive groups
        # For each combination of (sensitive_feature_value, label):
        #   - Calculate expected count (if uniform distribution)
        #   - Calculate actual count
        #   - Weight = expected / actual

        # Example:
        # groups = sensitive_features.groupby([sensitive_features.columns[0], y_train])
        # weights = groups.size()
        # weights = expected_counts / weights
        # return X_train, y_train, sample_weights
        pass

    def inprocess_exponentiated_gradient(
        self,
        X_train: pd.DataFrame,
        y_train: np.ndarray,
        sensitive_features: pd.DataFrame,
        constraint: str = 'demographic_parity'
    ) -> Any:
        """
        Train fair model using exponentiated gradient reduction.

        Args:
            X_train: Training features
            y_train: Training labels
            sensitive_features: Sensitive attributes
            constraint: Fairness constraint ('demographic_parity' or 'equalized_odds')

        Returns:
            Trained fair model
        """
        # TODO: Set up fairness constraint
        if constraint == 'demographic_parity':
            fairness_constraint = DemographicParity()
        elif constraint == 'equalized_odds':
            fairness_constraint = EqualizedOdds()
        else:
            raise ValueError(f"Unknown constraint: {constraint}")

        # TODO: Create ExponentiatedGradient mitigator
        # mitigator = ExponentiatedGradient(
        #     estimator=self.base_estimator,
        #     constraints=fairness_constraint
        # )

        # TODO: Fit mitigator
        # mitigator.fit(X_train, y_train, sensitive_features=sensitive_features)

        # TODO: Store and return model
        # self.mitigated_models['exponentiated_gradient'] = mitigator
        # return mitigator
        pass

    def inprocess_correlation_removal(
        self,
        X_train: pd.DataFrame,
        sensitive_features: pd.DataFrame,
        alpha: float = 1.0
    ) -> Tuple[pd.DataFrame, Any]:
        """
        Remove correlation between features and sensitive attributes.

        Args:
            X_train: Training features
            sensitive_features: Sensitive attributes
            alpha: Strength of correlation removal (0-1, 1=complete removal)

        Returns:
            Tuple of (transformed_X, transformer)
        """
        # TODO: Create CorrelationRemover
        # remover = CorrelationRemover(sensitive_feature_ids=[...], alpha=alpha)

        # TODO: Fit and transform features
        # X_transformed = remover.fit_transform(X_train)

        # TODO: Return transformed data and transformer
        pass

    def postprocess_threshold_optimization(
        self,
        model: Any,
        X_val: pd.DataFrame,
        y_val: np.ndarray,
        sensitive_features: pd.DataFrame,
        constraint: str = 'demographic_parity'
    ) -> Any:
        """
        Optimize decision thresholds per group to improve fairness.

        Args:
            model: Trained model
            X_val: Validation features
            y_val: Validation labels
            sensitive_features: Sensitive attributes
            constraint: Fairness constraint

        Returns:
            Threshold-optimized model
        """
        # TODO: Get prediction scores from model
        # y_scores = model.predict_proba(X_val)[:, 1]

        # TODO: Create ThresholdOptimizer
        if constraint == 'demographic_parity':
            fairness_constraint = DemographicParity()
        elif constraint == 'equalized_odds':
            fairness_constraint = EqualizedOdds()

        # threshold_optimizer = ThresholdOptimizer(
        #     estimator=model,
        #     constraints=fairness_constraint,
        #     predict_method='predict_proba'
        # )

        # TODO: Fit threshold optimizer
        # threshold_optimizer.fit(X_val, y_val, sensitive_features=sensitive_features)

        # TODO: Store and return
        # self.mitigated_models['threshold_optimization'] = threshold_optimizer
        # return threshold_optimizer
        pass

    def compare_mitigation_strategies(
        self,
        X_train: pd.DataFrame,
        y_train: np.ndarray,
        X_test: pd.DataFrame,
        y_test: np.ndarray,
        sensitive_features_train: pd.DataFrame,
        sensitive_features_test: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Compare all mitigation strategies.

        Args:
            X_train: Training features
            y_train: Training labels
            X_test: Test features
            y_test: Test labels
            sensitive_features_train: Training sensitive attributes
            sensitive_features_test: Test sensitive attributes

        Returns:
            DataFrame comparing strategies
        """
        results = []

        # TODO: 1. Train baseline (no mitigation)
        # baseline_model = self.base_estimator.fit(X_train, y_train)
        # baseline_result = self._evaluate_model(
        #     baseline_model, X_test, y_test, sensitive_features_test, "Baseline"
        # )
        # results.append(baseline_result)

        # TODO: 2. Train with reweighing
        # X_rw, y_rw, weights = self.preprocess_reweighing(
        #     X_train, y_train, sensitive_features_train
        # )
        # rw_model = self.base_estimator.fit(X_rw, y_rw, sample_weight=weights)
        # rw_result = self._evaluate_model(
        #     rw_model, X_test, y_test, sensitive_features_test, "Reweighing"
        # )
        # results.append(rw_result)

        # TODO: 3. Train with exponentiated gradient
        # eg_model = self.inprocess_exponentiated_gradient(
        #     X_train, y_train, sensitive_features_train
        # )
        # eg_result = self._evaluate_model(
        #     eg_model, X_test, y_test, sensitive_features_test, "Exponentiated Gradient"
        # )
        # results.append(eg_result)

        # TODO: 4. Apply threshold optimization
        # to_model = self.postprocess_threshold_optimization(
        #     baseline_model, X_test, y_test, sensitive_features_test
        # )
        # to_result = self._evaluate_model(
        #     to_model, X_test, y_test, sensitive_features_test, "Threshold Optimization"
        # )
        # results.append(to_result)

        # TODO: Create comparison DataFrame
        # comparison_df = pd.DataFrame(results)
        # return comparison_df
        pass

    def _evaluate_model(
        self,
        model: Any,
        X_test: pd.DataFrame,
        y_test: np.ndarray,
        sensitive_features: pd.DataFrame,
        strategy_name: str
    ) -> Dict:
        """
        Evaluate model for accuracy and fairness.

        Args:
            model: Trained model
            X_test: Test features
            y_test: Test labels
            sensitive_features: Sensitive attributes
            strategy_name: Name of mitigation strategy

        Returns:
            Dictionary with evaluation metrics
        """
        # TODO: Get predictions
        # y_pred = model.predict(X_test)

        # TODO: Calculate accuracy
        # accuracy = accuracy_score(y_test, y_pred)

        # TODO: Calculate fairness metrics
        # from fairlearn.metrics import demographic_parity_difference
        # dp_diff = demographic_parity_difference(
        #     y_test, y_pred, sensitive_features=sensitive_features
        # )

        # TODO: Return evaluation dict
        # return {
        #     'strategy': strategy_name,
        #     'accuracy': accuracy,
        #     'demographic_parity_diff': dp_diff,
        #     ...
        # }
        pass

    def visualize_fairness_accuracy_tradeoff(
        self,
        comparison_df: pd.DataFrame,
        save_path: str = None
    ):
        """
        Visualize fairness-accuracy tradeoff across strategies.

        Args:
            comparison_df: DataFrame with strategy comparisons
            save_path: Path to save plot
        """
        # TODO: Create scatter plot
        # X-axis: Fairness metric (lower is better)
        # Y-axis: Accuracy (higher is better)
        # Each point is a strategy
        # TODO: Label points with strategy names
        # TODO: Add Pareto frontier
        # TODO: Save or display
        pass
```

### Validation Tests

```python
# tests/test_bias_mitigation.py
"""Tests for bias mitigation."""

import pytest
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from src.governance.bias_mitigation import BiasMitigator


@pytest.fixture
def biased_dataset():
    """Generate dataset with bias."""
    np.random.seed(42)

    # Generate base dataset
    X, y = make_classification(
        n_samples=1000,
        n_features=10,
        n_informative=5,
        random_state=42
    )

    # Create biased sensitive feature
    sensitive = np.random.choice(['A', 'B'], size=1000, p=[0.7, 0.3])

    # Introduce bias: Group B has lower approval rate
    bias_indices = np.where(sensitive == 'B')[0]
    y[bias_indices] = np.where(
        np.random.random(len(bias_indices)) > 0.6,
        0,
        y[bias_indices]
    )

    X_df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(10)])
    sensitive_df = pd.DataFrame({'group': sensitive})

    return X_df, y, sensitive_df


def test_reweighing_reduces_bias(biased_dataset):
    """Test that reweighing reduces bias."""
    X, y, sensitive = biased_dataset

    mitigator = BiasMitigator()

    # TODO: Apply reweighing
    # TODO: Train model with weights
    # TODO: Assess fairness
    # TODO: Assert bias reduced compared to baseline
    pass


def test_exponentiated_gradient_improves_fairness(biased_dataset):
    """Test that exponentiated gradient improves fairness."""
    X, y, sensitive = biased_dataset

    # TODO: Train fair model
    # TODO: Compare to baseline
    # TODO: Assert fairness improved
    pass


def test_threshold_optimization_improves_fairness(biased_dataset):
    """Test that threshold optimization improves fairness."""
    # TODO: Train baseline model
    # TODO: Apply threshold optimization
    # TODO: Assert fairness improved
    pass


def test_mitigation_strategies_comparison(biased_dataset):
    """Test comparison of all mitigation strategies."""
    # TODO: Compare all strategies
    # TODO: Assert all show improvement over baseline
    # TODO: Assert results include accuracy and fairness metrics
    pass


# Run with: pytest tests/test_bias_mitigation.py -v
```

### Success Criteria

- [ ] Reweighing reduces bias in training data
- [ ] Exponentiated gradient produces fairer model
- [ ] Threshold optimization improves fairness
- [ ] All strategies reduce bias compared to baseline
- [ ] Fairness-accuracy tradeoff visualized
- [ ] Comparison shows best strategy for given dataset
- [ ] Tests pass for all mitigation techniques

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Reweighing**: Calculate weights to balance (sensitive_feature, label) combinations
   ```python
   # For each (group, label) pair:
   # weight = (n_samples / n_groups / n_labels) / actual_count
   ```

2. **Exponentiated Gradient**: Use Fairlearn's reduction approach
   ```python
   from fairlearn.reductions import ExponentiatedGradient, DemographicParity

   mitigator = ExponentiatedGradient(
       estimator=LogisticRegression(),
       constraints=DemographicParity()
   )
   mitigator.fit(X, y, sensitive_features=sensitive)
   ```

3. **Threshold Optimization**: Adjust thresholds per group
4. **Fairness-Accuracy Tradeoff**: Some mitigation reduces accuracy slightly
5. **Best Strategy**: Depends on use case - post-processing easiest, in-processing most effective

</details>

---
