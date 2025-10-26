# Module 07: ML Governance & Compliance - Exercises

## Overview

This exercise set provides hands-on practice with ML governance and compliance, covering:
- Fairness assessment and bias detection with Fairlearn
- Bias mitigation strategies and techniques
- Model card generation and documentation
- Audit logging and compliance tracking
- Complete governance frameworks

**Time Estimate**: 6-9 hours total

---

## Exercise 1: Fairness Assessment with Fairlearn (90 minutes)

**Objective**: Implement comprehensive fairness assessment using Fairlearn to detect and measure bias in ML models.

### Background

You're building a loan approval model. Regulators require fairness analysis across protected attributes (race, gender, age). You need to:
- Measure fairness metrics across demographic groups
- Identify disparate impact
- Generate fairness reports
- Document findings for compliance

### Tasks

1. **Implement fairness metrics calculation**
2. **Detect disparate impact across protected groups**
3. **Create fairness dashboards**
4. **Generate compliance reports**
5. **Compare multiple models for fairness**

### Starter Code

```python
# src/governance/fairness_assessment.py
"""Fairness assessment using Fairlearn."""

from fairlearn.metrics import (
    MetricFrame,
    demographic_parity_difference,
    demographic_parity_ratio,
    equalized_odds_difference,
    equalized_odds_ratio,
    selection_rate
)
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
import numpy as np
from typing import Dict, List, Any
from dataclasses import dataclass
import matplotlib.pyplot as plt
import seaborn as sns


@dataclass
class FairnessReport:
    """Container for fairness assessment results."""
    overall_metrics: Dict[str, float]
    group_metrics: pd.DataFrame
    disparate_impact_ratio: Dict[str, float]
    fairness_violations: List[str]
    demographic_parity_diff: float
    equalized_odds_diff: float
    compliance_status: str


class FairnessAssessor:
    """Assess model fairness across protected attributes."""

    def __init__(
        self,
        sensitive_features: List[str],
        fairness_threshold: float = 0.8
    ):
        """
        Initialize fairness assessor.

        Args:
            sensitive_features: List of sensitive/protected attribute names
            fairness_threshold: Minimum acceptable disparate impact ratio (0.8 is 80% rule)
        """
        self.sensitive_features = sensitive_features
        self.fairness_threshold = fairness_threshold

    def assess_fairness(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        sensitive_features: pd.DataFrame
    ) -> FairnessReport:
        """
        Comprehensive fairness assessment.

        Args:
            y_true: True labels
            y_pred: Predicted labels
            sensitive_features: DataFrame with sensitive attributes

        Returns:
            FairnessReport with complete analysis
        """
        # TODO: Calculate overall model metrics
        # overall_metrics = {
        #     'accuracy': accuracy_score(y_true, y_pred),
        #     'precision': precision_score(y_true, y_pred),
        #     'recall': recall_score(y_true, y_pred),
        #     'f1': f1_score(y_true, y_pred)
        # }

        # TODO: Calculate metrics by group for each sensitive feature
        # group_metrics = {}
        # for feature in self.sensitive_features:
        #     metric_frame = MetricFrame(
        #         metrics={
        #             'accuracy': accuracy_score,
        #             'selection_rate': selection_rate,
        #             'precision': precision_score,
        #             'recall': recall_score
        #         },
        #         y_true=y_true,
        #         y_pred=y_pred,
        #         sensitive_features=sensitive_features[feature]
        #     )
        #     group_metrics[feature] = metric_frame.by_group

        # TODO: Calculate fairness metrics
        # disparate_impact = self._calculate_disparate_impact(
        #     y_pred, sensitive_features
        # )

        # TODO: Calculate demographic parity difference
        # dp_diff = demographic_parity_difference(
        #     y_true, y_pred, sensitive_features=sensitive_features
        # )

        # TODO: Calculate equalized odds difference
        # eo_diff = equalized_odds_difference(
        #     y_true, y_pred, sensitive_features=sensitive_features
        # )

        # TODO: Identify fairness violations
        # violations = self._identify_violations(disparate_impact)

        # TODO: Determine compliance status
        # compliance = self._determine_compliance(violations)

        # TODO: Create and return FairnessReport
        pass

    def _calculate_disparate_impact(
        self,
        y_pred: np.ndarray,
        sensitive_features: pd.DataFrame
    ) -> Dict[str, float]:
        """
        Calculate disparate impact ratio for each sensitive feature.

        Disparate Impact Ratio = (Selection rate for protected group) /
                                (Selection rate for reference group)

        Args:
            y_pred: Predicted labels
            sensitive_features: DataFrame with sensitive attributes

        Returns:
            Dictionary mapping feature names to disparate impact ratios
        """
        # TODO: For each sensitive feature:
        #   1. Calculate selection rate for each group
        #   2. Identify reference group (typically majority group)
        #   3. Calculate disparate impact ratio
        #   4. Store in results dictionary

        # Example for gender:
        # male_selection_rate = y_pred[sensitive_features['gender'] == 'male'].mean()
        # female_selection_rate = y_pred[sensitive_features['gender'] == 'female'].mean()
        # disparate_impact = female_selection_rate / male_selection_rate

        pass

    def _identify_violations(
        self,
        disparate_impact: Dict[str, float]
    ) -> List[str]:
        """
        Identify fairness violations based on thresholds.

        80% rule: Disparate impact ratio should be >= 0.8

        Args:
            disparate_impact: Disparate impact ratios by feature

        Returns:
            List of violation messages
        """
        violations = []

        # TODO: For each feature in disparate_impact:
        #   - If ratio < threshold (0.8), add violation
        #   - Format: "Feature 'race': DI ratio = 0.65 (< 0.8)"

        return violations

    def _determine_compliance(
        self,
        violations: List[str]
    ) -> str:
        """
        Determine overall compliance status.

        Args:
            violations: List of fairness violations

        Returns:
            Compliance status: "COMPLIANT", "NEEDS_REVIEW", "NON_COMPLIANT"
        """
        # TODO: Determine status based on number/severity of violations
        # - No violations: "COMPLIANT"
        # - 1-2 minor violations: "NEEDS_REVIEW"
        # - 3+ or severe violations: "NON_COMPLIANT"
        pass

    def compare_models(
        self,
        models: Dict[str, Any],
        X_test: pd.DataFrame,
        y_test: np.ndarray,
        sensitive_features: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Compare fairness across multiple models.

        Args:
            models: Dictionary of model_name -> model object
            X_test: Test features
            y_test: Test labels
            sensitive_features: Sensitive attributes

        Returns:
            DataFrame comparing fairness metrics across models
        """
        # TODO: For each model:
        #   - Make predictions
        #   - Assess fairness
        #   - Extract key metrics
        #   - Add to comparison DataFrame

        # TODO: Rank models by fairness
        pass

    def visualize_fairness(
        self,
        group_metrics: pd.DataFrame,
        metric_name: str = 'selection_rate',
        save_path: str = None
    ):
        """
        Visualize fairness metrics across groups.

        Args:
            group_metrics: Metrics by demographic group
            metric_name: Metric to visualize
            save_path: Path to save plot
        """
        # TODO: Create bar chart showing metric by group
        # TODO: Add reference line for overall average
        # TODO: Highlight groups below fairness threshold
        # TODO: Save or display plot
        pass

    def generate_fairness_report(
        self,
        report: FairnessReport,
        output_path: str = "fairness_report.html"
    ):
        """
        Generate comprehensive HTML fairness report.

        Args:
            report: FairnessReport object
            output_path: Path to save HTML report
        """
        # TODO: Create HTML report with:
        #   - Executive summary
        #   - Overall metrics
        #   - Group-level metrics
        #   - Fairness violations
        #   - Visualizations
        #   - Recommendations
        #   - Compliance status
        pass
```

### Validation Tests

```python
# tests/test_fairness_assessment.py
"""Tests for fairness assessment."""

import pytest
import pandas as pd
import numpy as np
from src.governance.fairness_assessment import FairnessAssessor, FairnessReport


@pytest.fixture
def biased_predictions():
    """Generate biased predictions for testing."""
    np.random.seed(42)
    n_samples = 1000

    # Create sensitive features
    gender = np.random.choice(['male', 'female'], n_samples, p=[0.6, 0.4])
    race = np.random.choice(['white', 'black', 'hispanic'], n_samples, p=[0.5, 0.3, 0.2])

    # True labels (balanced)
    y_true = np.random.binomial(1, 0.3, n_samples)

    # Biased predictions (favor males and whites)
    y_pred = y_true.copy()
    # Introduce bias: reduce approval rate for females and minorities
    female_indices = np.where(gender == 'female')[0]
    y_pred[female_indices] = np.where(
        np.random.random(len(female_indices)) > 0.3,
        0,
        y_pred[female_indices]
    )

    sensitive_df = pd.DataFrame({
        'gender': gender,
        'race': race
    })

    return y_true, y_pred, sensitive_df


def test_fairness_assessor_initialization():
    """Test that assessor initializes correctly."""
    assessor = FairnessAssessor(
        sensitive_features=['gender', 'race'],
        fairness_threshold=0.8
    )

    # TODO: Add assertions
    assert assessor.fairness_threshold == 0.8
    assert 'gender' in assessor.sensitive_features


def test_disparate_impact_calculation(biased_predictions):
    """Test disparate impact calculation detects bias."""
    y_true, y_pred, sensitive_features = biased_predictions

    assessor = FairnessAssessor(sensitive_features=['gender'])

    # TODO: Calculate disparate impact
    # TODO: Assert that bias is detected (ratio < 0.8 for gender)
    pass


def test_fairness_violations_identified(biased_predictions):
    """Test that fairness violations are identified."""
    y_true, y_pred, sensitive_features = biased_predictions

    assessor = FairnessAssessor(sensitive_features=['gender', 'race'])
    report = assessor.assess_fairness(y_true, y_pred, sensitive_features)

    # TODO: Assert violations were identified
    # TODO: Assert compliance status is not "COMPLIANT"
    pass


def test_fair_model_passes():
    """Test that fair model passes fairness checks."""
    np.random.seed(42)
    n_samples = 1000

    # Create unbiased predictions
    y_true = np.random.binomial(1, 0.3, n_samples)
    y_pred = y_true.copy()  # Perfect predictions, no bias

    sensitive_features = pd.DataFrame({
        'gender': np.random.choice(['male', 'female'], n_samples)
    })

    assessor = FairnessAssessor(sensitive_features=['gender'])
    report = assessor.assess_fairness(y_true, y_pred, sensitive_features)

    # TODO: Assert no violations
    # TODO: Assert compliance status is "COMPLIANT"
    pass


# Run with: pytest tests/test_fairness_assessment.py -v
```

### Success Criteria

- [ ] Fairness metrics calculated correctly for all groups
- [ ] Disparate impact ratio computed accurately
- [ ] Violations identified when bias present
- [ ] Fair models pass fairness checks
- [ ] Visualizations clearly show group disparities
- [ ] HTML report includes all required sections
- [ ] Model comparison ranks by fairness

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **MetricFrame**: Use Fairlearn's MetricFrame to compute metrics by group
   ```python
   from fairlearn.metrics import MetricFrame

   mf = MetricFrame(
       metrics={'accuracy': accuracy_score},
       y_true=y_true,
       y_pred=y_pred,
       sensitive_features=sensitive_features['gender']
   )
   group_metrics = mf.by_group
   ```

2. **Disparate Impact**: Calculate as ratio of selection rates
   ```python
   # Selection rate = proportion of positive predictions
   protected_rate = y_pred[group == 'protected'].mean()
   reference_rate = y_pred[group == 'reference'].mean()
   disparate_impact = protected_rate / reference_rate
   ```

3. **80% Rule**: Disparate impact ratio should be >= 0.8
4. **Demographic Parity**: Selection rates should be similar across groups
5. **Equalized Odds**: True positive rates and false positive rates should be similar across groups

</details>

---

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

## Exercise 3: Model Card Generation & Documentation (75 minutes)

**Objective**: Create comprehensive model cards following industry standards for ML model documentation.

### Background

Model cards provide transparent documentation of ML models including:
- Model details and architecture
- Intended use and limitations
- Training data and evaluation metrics
- Fairness analysis
- Ethical considerations

### Tasks

1. **Implement model card generator**
2. **Document model details and performance**
3. **Include fairness and bias analysis**
4. **Add ethical considerations**
5. **Generate HTML/Markdown reports**

### Starter Code

```python
# src/governance/model_card.py
"""Model card generation for ML model documentation."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import markdown
from jinja2 import Template


@dataclass
class ModelDetails:
    """Basic model information."""
    name: str
    version: str
    model_type: str
    model_architecture: str
    training_date: datetime
    developer: str
    contact: str
    license: str = "Proprietary"
    repository: Optional[str] = None
    paper: Optional[str] = None


@dataclass
class IntendedUse:
    """Intended use and limitations."""
    primary_uses: List[str]
    primary_users: List[str]
    out_of_scope_uses: List[str]
    limitations: List[str]
    warnings: List[str] = field(default_factory=list)


@dataclass
class TrainingData:
    """Training data information."""
    dataset_name: str
    dataset_size: int
    dataset_description: str
    data_sources: List[str]
    preprocessing: List[str]
    train_test_split: Dict[str, float]
    data_collection_period: str
    known_biases: List[str] = field(default_factory=list)


@dataclass
class PerformanceMetrics:
    """Model performance metrics."""
    overall_metrics: Dict[str, float]
    performance_by_group: Optional[Dict[str, Dict[str, float]]] = None
    test_set_size: Optional[int] = None
    confidence_intervals: Optional[Dict[str, tuple]] = None


@dataclass
class FairnessAnalysis:
    """Fairness and bias analysis."""
    protected_attributes: List[str]
    fairness_metrics: Dict[str, float]
    disparate_impact_ratio: Dict[str, float]
    bias_mitigation_applied: List[str]
    residual_bias: str
    ongoing_monitoring: str


@dataclass
class EthicalConsiderations:
    """Ethical considerations and risks."""
    risks: List[str]
    mitigation_strategies: List[str]
    use_cases_to_avoid: List[str]
    stakeholder_impact: Dict[str, str]
    fairness_tradeoffs: str


@dataclass
class ModelCard:
    """Complete model card."""
    model_details: ModelDetails
    intended_use: IntendedUse
    training_data: TrainingData
    performance_metrics: PerformanceMetrics
    fairness_analysis: FairnessAnalysis
    ethical_considerations: EthicalConsiderations
    additional_info: Optional[Dict[str, Any]] = None


class ModelCardGenerator:
    """Generate model cards for ML models."""

    def __init__(self):
        """Initialize model card generator."""
        self.card = None

    def create_model_card(
        self,
        model_details: ModelDetails,
        intended_use: IntendedUse,
        training_data: TrainingData,
        performance_metrics: PerformanceMetrics,
        fairness_analysis: FairnessAnalysis,
        ethical_considerations: EthicalConsiderations
    ) -> ModelCard:
        """
        Create complete model card.

        Args:
            model_details: Model information
            intended_use: Use cases and limitations
            training_data: Training data details
            performance_metrics: Performance metrics
            fairness_analysis: Fairness analysis
            ethical_considerations: Ethical considerations

        Returns:
            Complete ModelCard object
        """
        # TODO: Create ModelCard object
        # self.card = ModelCard(...)
        # return self.card
        pass

    def generate_markdown(self, card: ModelCard) -> str:
        """
        Generate Markdown representation of model card.

        Args:
            card: ModelCard object

        Returns:
            Markdown string
        """
        # TODO: Generate Markdown following this structure:
        markdown_content = """
# Model Card: {model_name}

## Model Details
- **Name:** {model_name}
- **Version:** {version}
- **Type:** {model_type}
- **Architecture:** {architecture}
- **Developer:** {developer}
- **Training Date:** {training_date}
- **License:** {license}

## Intended Use

### Primary Uses
{primary_uses}

### Primary Users
{primary_users}

### Out-of-Scope Uses
{out_of_scope}

### Limitations
{limitations}

## Training Data

### Dataset
- **Name:** {dataset_name}
- **Size:** {dataset_size:,} samples
- **Description:** {dataset_description}

### Data Sources
{data_sources}

### Preprocessing
{preprocessing}

## Performance Metrics

### Overall Performance
{overall_metrics}

### Performance by Group
{performance_by_group}

## Fairness Analysis

### Protected Attributes
{protected_attributes}

### Fairness Metrics
{fairness_metrics}

### Disparate Impact Analysis
{disparate_impact}

### Bias Mitigation
{bias_mitigation}

## Ethical Considerations

### Risks
{risks}

### Mitigation Strategies
{mitigation_strategies}

### Use Cases to Avoid
{use_cases_to_avoid}

## Additional Information
{additional_info}

---

*Generated: {generation_date}*
"""

        # TODO: Fill in template with card data
        # TODO: Return formatted markdown
        pass

    def generate_html(self, card: ModelCard) -> str:
        """
        Generate HTML representation of model card.

        Args:
            card: ModelCard object

        Returns:
            HTML string
        """
        # TODO: Generate HTML with styling
        # Option 1: Convert markdown to HTML
        # Option 2: Use Jinja2 HTML template
        # TODO: Include CSS for nice formatting
        # TODO: Add interactive elements (collapsible sections)
        pass

    def generate_json(self, card: ModelCard) -> str:
        """
        Generate JSON representation of model card.

        Args:
            card: ModelCard object

        Returns:
            JSON string
        """
        # TODO: Convert ModelCard to dictionary
        # TODO: Serialize to JSON
        # TODO: Return JSON string
        pass

    def save_model_card(
        self,
        card: ModelCard,
        output_path: str,
        format: str = 'markdown'
    ):
        """
        Save model card to file.

        Args:
            card: ModelCard object
            output_path: Output file path
            format: Output format ('markdown', 'html', 'json')
        """
        # TODO: Generate content in requested format
        # TODO: Write to file
        pass

    def validate_model_card(self, card: ModelCard) -> List[str]:
        """
        Validate model card completeness.

        Args:
            card: ModelCard object

        Returns:
            List of validation warnings/errors
        """
        issues = []

        # TODO: Check required fields are present
        # - Model name, version, type
        # - At least one intended use
        # - At least one limitation
        # - Training data information
        # - Performance metrics
        # - Fairness analysis

        # TODO: Check for completeness
        # - Are all sections filled in?
        # - Are there placeholder values?
        # - Are fairness metrics included?

        # TODO: Return list of issues
        return issues
```

### Example Usage

```python
# scripts/create_model_card.py
"""Example script to create model card."""

from src.governance.model_card import (
    ModelCardGenerator,
    ModelDetails,
    IntendedUse,
    TrainingData,
    PerformanceMetrics,
    FairnessAnalysis,
    EthicalConsiderations
)
from datetime import datetime


def main():
    """Create example model card for loan approval model."""

    # TODO: Define model details
    model_details = ModelDetails(
        name="Loan Approval Model",
        version="1.2.0",
        model_type="Binary Classification",
        model_architecture="Gradient Boosted Trees (XGBoost)",
        training_date=datetime(2024, 10, 15),
        developer="ML Team - Financial Services Division",
        contact="ml-team@company.com",
        license="Proprietary",
        repository="https://github.com/company/loan-model"
    )

    # TODO: Define intended use
    intended_use = IntendedUse(
        primary_uses=[
            "Automated loan approval decisions for personal loans under $50,000",
            "Risk assessment for loan applications",
            "Prioritization of applications for manual review"
        ],
        primary_users=[
            "Loan officers",
            "Risk assessment teams",
            "Automated lending platform"
        ],
        out_of_scope_uses=[
            "Mortgage or business loan approvals",
            "Loans over $50,000",
            "Decisions without human oversight",
            "Use in jurisdictions with different lending regulations"
        ],
        limitations=[
            "Model performance degrades for applicants with thin credit files",
            "May not generalize to economic conditions outside training period",
            "Requires quarterly retraining to maintain performance",
            "Not suitable for first-time borrowers without credit history"
        ],
        warnings=[
            "Must be used in compliance with fair lending regulations",
            "Human review required for declined applications",
            "Monitor for fairness violations in production"
        ]
    )

    # TODO: Define training data
    training_data = TrainingData(
        dataset_name="Historical Loan Applications 2020-2024",
        dataset_size=150000,
        dataset_description="Historical loan applications with outcomes (approved/denied) and repayment data",
        data_sources=[
            "Internal loan application database",
            "Credit bureau data",
            "Income verification systems"
        ],
        preprocessing=[
            "Removal of personally identifiable information",
            "Feature engineering: debt-to-income ratio, credit utilization",
            "Handling missing values: median imputation for numerical, mode for categorical",
            "Outlier capping at 99th percentile for continuous features"
        ],
        train_test_split={
            "train": 0.7,
            "validation": 0.15,
            "test": 0.15
        },
        data_collection_period="January 2020 - June 2024",
        known_biases=[
            "Historical bias: Lower approval rates for minority groups due to systemic factors",
            "Geographic bias: Underrepresentation of rural applicants"
        ]
    )

    # TODO: Define performance metrics
    performance_metrics = PerformanceMetrics(
        overall_metrics={
            "accuracy": 0.87,
            "precision": 0.84,
            "recall": 0.82,
            "f1_score": 0.83,
            "auc_roc": 0.91
        },
        performance_by_group={
            "gender": {
                "male": {"accuracy": 0.88, "precision": 0.85},
                "female": {"accuracy": 0.86, "precision": 0.83}
            },
            "race": {
                "white": {"accuracy": 0.88, "precision": 0.86},
                "black": {"accuracy": 0.85, "precision": 0.81},
                "hispanic": {"accuracy": 0.86, "precision": 0.82}
            }
        },
        test_set_size=22500,
        confidence_intervals={
            "accuracy": (0.85, 0.89),
            "precision": (0.82, 0.86)
        }
    )

    # TODO: Define fairness analysis
    fairness_analysis = FairnessAnalysis(
        protected_attributes=["gender", "race", "age"],
        fairness_metrics={
            "demographic_parity_difference": 0.05,
            "equalized_odds_difference": 0.08,
            "equal_opportunity_difference": 0.06
        },
        disparate_impact_ratio={
            "gender": 0.92,
            "race": 0.85,
            "age": 0.88
        },
        bias_mitigation_applied=[
            "Reweighing of training samples",
            "Post-processing threshold optimization",
            "Regular fairness audits"
        ],
        residual_bias="Minor disparate impact detected for race (DI ratio: 0.85). Ongoing monitoring required.",
        ongoing_monitoring="Monthly fairness audits, quarterly model retraining with fairness constraints"
    )

    # TODO: Define ethical considerations
    ethical_considerations = EthicalConsiderations(
        risks=[
            "Potential for discriminatory outcomes if fairness monitoring lapses",
            "Over-reliance on model could reduce human judgment in edge cases",
            "Privacy risk if model features inadvertently expose sensitive information",
            "Economic harm to applicants if model errors lead to unfair denials"
        ],
        mitigation_strategies=[
            "Mandatory human review for all denials",
            "Regular fairness audits by independent team",
            "Adverse action explanations for all denied applications",
            "Appeals process with human adjudication",
            "Quarterly model retraining with updated fairness constraints"
        ],
        use_cases_to_avoid=[
            "Fully automated decisions without human oversight",
            "Use on protected classes without fairness validation",
            "Deployment without adverse action explanation capability"
        ],
        stakeholder_impact={
            "applicants": "Direct impact on loan access and financial opportunities",
            "loan_officers": "Tool to support but not replace decision-making",
            "company": "Regulatory compliance and reputation risk",
            "regulators": "Fair lending compliance oversight"
        },
        fairness_tradeoffs="Slight reduction in overall accuracy (2%) in exchange for improved fairness across demographic groups"
    )

    # TODO: Create model card
    generator = ModelCardGenerator()
    card = generator.create_model_card(
        model_details=model_details,
        intended_use=intended_use,
        training_data=training_data,
        performance_metrics=performance_metrics,
        fairness_analysis=fairness_analysis,
        ethical_considerations=ethical_considerations
    )

    # TODO: Validate model card
    issues = generator.validate_model_card(card)
    if issues:
        print("Model card validation issues:")
        for issue in issues:
            print(f"  - {issue}")

    # TODO: Generate and save in multiple formats
    generator.save_model_card(card, "model_card.md", format="markdown")
    generator.save_model_card(card, "model_card.html", format="html")
    generator.save_model_card(card, "model_card.json", format="json")

    print("Model card generated successfully!")


if __name__ == "__main__":
    main()
```

### Success Criteria

- [ ] Model card includes all required sections
- [ ] Markdown generation produces well-formatted output
- [ ] HTML generation includes styling
- [ ] JSON export is valid and complete
- [ ] Validation detects missing fields
- [ ] Card follows industry best practices
- [ ] Generated cards are human-readable

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Markdown Generation**: Use f-strings or templates
2. **HTML Generation**: Convert markdown or use Jinja2 templates
3. **JSON Serialization**: Use `dataclasses.asdict()` and `json.dumps()`
4. **Validation**: Check for None values and empty lists
5. **Follow Standards**: Reference Google's Model Cards paper and examples

</details>

---

## Exercise 4: Audit Logging & Compliance Tracking (90 minutes)

**Objective**: Implement tamper-proof audit logging for ML model predictions and decisions.

### Background

Regulatory compliance requires complete audit trails of model predictions, including:
- Who made predictions
- What inputs were used
- What outputs were generated
- When predictions occurred
- Why decisions were made (explanations)

### Tasks

1. **Implement tamper-proof audit logging**
2. **Log predictions with full context**
3. **Generate audit reports**
4. **Implement compliance checks**
5. **Create audit trail query system**

### Starter Code

```python
# src/governance/audit_logging.py
"""Tamper-proof audit logging for ML models."""

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import sqlite3
from pathlib import Path


@dataclass
class PredictionLog:
    """Single prediction audit log entry."""
    log_id: str
    timestamp: datetime
    model_name: str
    model_version: str
    user_id: str
    input_data: Dict[str, Any]
    prediction: Any
    confidence: float
    explanation: Optional[Dict] = None
    sensitive_features: Optional[Dict] = None
    fairness_check_passed: bool = True
    previous_hash: str = ""
    current_hash: str = ""


class AuditLogger:
    """Tamper-proof audit logging system."""

    def __init__(self, db_path: str = "audit_log.db"):
        """
        Initialize audit logger.

        Args:
            db_path: Path to SQLite database for audit logs
        """
        self.db_path = Path(db_path)
        self._initialize_database()
        self.previous_hash = self._get_last_hash()

    def _initialize_database(self):
        """Create audit log database if it doesn't exist."""
        # TODO: Create SQLite database with audit_logs table
        # Columns:
        #   - log_id (PRIMARY KEY)
        #   - timestamp
        #   - model_name
        #   - model_version
        #   - user_id
        #   - input_data (JSON)
        #   - prediction (JSON)
        #   - confidence
        #   - explanation (JSON)
        #   - sensitive_features (JSON)
        #   - fairness_check_passed
        #   - previous_hash
        #   - current_hash
        pass

    def _calculate_hash(self, log_entry: PredictionLog) -> str:
        """
        Calculate cryptographic hash of log entry.

        Args:
            log_entry: Prediction log entry

        Returns:
            SHA-256 hash string
        """
        # TODO: Create hash of log entry
        # Include all fields except current_hash
        # Concatenate with previous_hash to create chain
        # Use SHA-256 for cryptographic security

        # Example:
        # data_string = json.dumps({
        #     'log_id': log_entry.log_id,
        #     'timestamp': log_entry.timestamp.isoformat(),
        #     ...
        #     'previous_hash': log_entry.previous_hash
        # }, sort_keys=True)
        # hash_value = hashlib.sha256(data_string.encode()).hexdigest()
        # return hash_value
        pass

    def log_prediction(
        self,
        model_name: str,
        model_version: str,
        user_id: str,
        input_data: Dict[str, Any],
        prediction: Any,
        confidence: float,
        explanation: Optional[Dict] = None,
        sensitive_features: Optional[Dict] = None,
        fairness_check_passed: bool = True
    ) -> str:
        """
        Log a model prediction.

        Args:
            model_name: Name of the model
            model_version: Version of the model
            user_id: User making the prediction
            input_data: Input features
            prediction: Model prediction
            confidence: Prediction confidence score
            explanation: Explanation of prediction (optional)
            sensitive_features: Sensitive attributes (optional)
            fairness_check_passed: Whether fairness check passed

        Returns:
            Log ID
        """
        # TODO: Generate unique log ID
        # log_id = f"{model_name}_{datetime.now().timestamp()}"

        # TODO: Create PredictionLog entry
        # log_entry = PredictionLog(
        #     log_id=log_id,
        #     timestamp=datetime.now(),
        #     model_name=model_name,
        #     model_version=model_version,
        #     user_id=user_id,
        #     input_data=input_data,
        #     prediction=prediction,
        #     confidence=confidence,
        #     explanation=explanation,
        #     sensitive_features=sensitive_features,
        #     fairness_check_passed=fairness_check_passed,
        #     previous_hash=self.previous_hash
        # )

        # TODO: Calculate hash
        # log_entry.current_hash = self._calculate_hash(log_entry)

        # TODO: Store in database
        # self._store_log(log_entry)

        # TODO: Update previous_hash for next log
        # self.previous_hash = log_entry.current_hash

        # TODO: Return log_id
        pass

    def _store_log(self, log_entry: PredictionLog):
        """
        Store log entry in database.

        Args:
            log_entry: Prediction log to store
        """
        # TODO: Connect to database
        # TODO: Insert log entry
        # TODO: Commit transaction
        pass

    def _get_last_hash(self) -> str:
        """
        Get hash of last log entry.

        Returns:
            Last hash or empty string if no logs
        """
        # TODO: Query database for last log entry
        # TODO: Return current_hash or "" if no entries
        pass

    def verify_log_integrity(self) -> tuple[bool, List[str]]:
        """
        Verify integrity of entire audit log.

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        # TODO: Query all log entries in order
        # TODO: Verify hash chain:
        #   - For each entry:
        #     - Recalculate hash
        #     - Compare to stored hash
        #     - Verify previous_hash matches previous entry's current_hash
        #   - If any mismatch, add to issues list

        # TODO: Return (len(issues) == 0, issues)
        pass

    def query_logs(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        model_name: Optional[str] = None,
        user_id: Optional[str] = None,
        fairness_check_failed: bool = False
    ) -> List[PredictionLog]:
        """
        Query audit logs with filters.

        Args:
            start_date: Filter logs after this date
            end_date: Filter logs before this date
            model_name: Filter by model name
            user_id: Filter by user ID
            fairness_check_failed: If True, return only failed fairness checks

        Returns:
            List of matching prediction logs
        """
        # TODO: Build SQL query with WHERE clauses based on filters
        # TODO: Execute query
        # TODO: Convert results to PredictionLog objects
        # TODO: Return list
        pass

    def generate_audit_report(
        self,
        start_date: datetime,
        end_date: datetime,
        output_path: str = "audit_report.html"
    ):
        """
        Generate compliance audit report.

        Args:
            start_date: Report start date
            end_date: Report end date
            output_path: Path to save report
        """
        # TODO: Query logs for date range
        logs = self.query_logs(start_date=start_date, end_date=end_date)

        # TODO: Calculate statistics
        #   - Total predictions
        #   - Predictions by model
        #   - Predictions by user
        #   - Fairness check failures
        #   - Average confidence
        #   - Sensitive feature usage

        # TODO: Generate HTML report with:
        #   - Summary statistics
        #   - Fairness violations
        #   - Model usage
        #   - User activity
        #   - Compliance status

        # TODO: Save report
        pass

    def export_logs(
        self,
        output_path: str,
        format: str = 'json',
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ):
        """
        Export audit logs for compliance.

        Args:
            output_path: Output file path
            format: Export format ('json', 'csv')
            start_date: Optional start date filter
            end_date: Optional end date filter
        """
        # TODO: Query logs with filters
        # TODO: Convert to requested format
        # TODO: Write to file
        pass
```

### Validation Tests

```python
# tests/test_audit_logging.py
"""Tests for audit logging."""

import pytest
from datetime import datetime, timedelta
from src.governance.audit_logging import AuditLogger, PredictionLog


@pytest.fixture
def audit_logger(tmp_path):
    """Create temporary audit logger."""
    db_path = tmp_path / "test_audit.db"
    return AuditLogger(str(db_path))


def test_audit_logger_initialization(audit_logger):
    """Test that audit logger initializes."""
    # TODO: Assert database created
    # TODO: Assert previous_hash is empty initially
    pass


def test_log_prediction(audit_logger):
    """Test logging a prediction."""
    log_id = audit_logger.log_prediction(
        model_name="loan_model",
        model_version="1.0",
        user_id="user123",
        input_data={"age": 35, "income": 50000},
        prediction="approved",
        confidence=0.85
    )

    # TODO: Assert log_id returned
    # TODO: Assert log stored in database
    # TODO: Assert hash calculated
    pass


def test_hash_chain_integrity(audit_logger):
    """Test that hash chain maintains integrity."""
    # TODO: Log multiple predictions
    # TODO: Verify hash chain integrity
    # TODO: Assert verification passes
    pass


def test_tamper_detection(audit_logger):
    """Test that tampering is detected."""
    # TODO: Log prediction
    # TODO: Manually modify database entry
    # TODO: Run verify_log_integrity()
    # TODO: Assert tampering detected
    pass


def test_query_logs_with_filters(audit_logger):
    """Test querying logs with filters."""
    # TODO: Log multiple predictions with different attributes
    # TODO: Query with model_name filter
    # TODO: Assert correct logs returned
    # TODO: Query with date filter
    # TODO: Assert correct logs returned
    pass


def test_fairness_check_logging(audit_logger):
    """Test logging fairness check results."""
    # TODO: Log prediction with fairness_check_passed=False
    # TODO: Query for failed fairness checks
    # TODO: Assert failed check is returned
    pass


# Run with: pytest tests/test_audit_logging.py -v
```

### Success Criteria

- [ ] Audit logs stored in tamper-proof manner
- [ ] Hash chain maintains integrity
- [ ] Tampering is detected
- [ ] Logs queryable with multiple filters
- [ ] Audit reports generated correctly
- [ ] Export functionality works
- [ ] Tests verify all functionality

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Hash Chain**: Each entry's hash includes previous entry's hash
   ```python
   data = {**log_data, 'previous_hash': previous_hash}
   current_hash = hashlib.sha256(json.dumps(data).encode()).hexdigest()
   ```

2. **Tamper Detection**: Recalculate hashes and compare to stored values
3. **SQLite**: Use `sqlite3` module for database operations
4. **JSON Storage**: Store complex fields as JSON strings in SQLite
5. **Verification**: Check hash chain in order from oldest to newest

</details>

---

## Exercise 5: Complete Governance Framework (120 minutes)

**Objective**: Build an end-to-end ML governance framework integrating fairness, model cards, audit logging, and compliance.

### Background

Create a production-ready governance system that:
1. Assesses fairness before deployment
2. Generates model cards automatically
3. Logs all predictions with audit trail
4. Monitors ongoing compliance
5. Generates governance reports

### Tasks

1. **Design governance architecture**
2. **Integrate all governance components**
3. **Create governance pipeline**
4. **Implement compliance dashboard**
5. **Set up automated governance checks**

### Starter Code

```python
# src/governance/governance_framework.py
"""Complete ML governance framework."""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.governance.fairness_assessment import FairnessAssessor
from src.governance.bias_mitigation import BiasMitigator
from src.governance.model_card import ModelCardGenerator, ModelCard
from src.governance.audit_logging import AuditLogger


class GovernanceFramework:
    """Complete ML governance and compliance framework."""

    def __init__(
        self,
        model_name: str,
        model_version: str,
        sensitive_features: List[str],
        audit_db_path: str = "governance_audit.db"
    ):
        """
        Initialize governance framework.

        Args:
            model_name: Name of model
            model_version: Model version
            sensitive_features: List of protected attributes
            audit_db_path: Path to audit log database
        """
        self.model_name = model_name
        self.model_version = model_version
        self.sensitive_features = sensitive_features

        # Initialize components
        self.fairness_assessor = FairnessAssessor(sensitive_features)
        self.bias_mitigator = BiasMitigator()
        self.model_card_generator = ModelCardGenerator()
        self.audit_logger = AuditLogger(audit_db_path)

        self.governance_status = "NOT_ASSESSED"
        self.fairness_report = None
        self.model_card = None

    def assess_model_governance(
        self,
        model: Any,
        X_test: pd.DataFrame,
        y_test: np.ndarray,
        sensitive_features_test: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Comprehensive governance assessment before deployment.

        Args:
            model: Trained model
            X_test: Test features
            y_test: Test labels
            sensitive_features_test: Test sensitive attributes

        Returns:
            Governance assessment results
        """
        assessment = {
            'timestamp': datetime.now(),
            'model_name': self.model_name,
            'model_version': self.model_version,
            'checks': {}
        }

        # ============================================
        # 1. FAIRNESS ASSESSMENT
        # ============================================
        print("Running fairness assessment...")

        # TODO: Get predictions
        # y_pred = model.predict(X_test)

        # TODO: Assess fairness
        # self.fairness_report = self.fairness_assessor.assess_fairness(
        #     y_test, y_pred, sensitive_features_test
        # )

        # TODO: Record results
        # assessment['checks']['fairness'] = {
        #     'passed': self.fairness_report.compliance_status == 'COMPLIANT',
        #     'disparate_impact': self.fairness_report.disparate_impact_ratio,
        #     'violations': self.fairness_report.fairness_violations
        # }

        # ============================================
        # 2. PERFORMANCE ASSESSMENT
        # ============================================
        print("Assessing model performance...")

        # TODO: Calculate performance metrics
        # assessment['checks']['performance'] = {
        #     'accuracy': accuracy_score(y_test, y_pred),
        #     'precision': precision_score(y_test, y_pred),
        #     'recall': recall_score(y_test, y_pred),
        #     'f1': f1_score(y_test, y_pred)
        # }

        # ============================================
        # 3. BIAS MITIGATION CHECK
        # ============================================
        print("Checking if bias mitigation needed...")

        # TODO: If fairness check failed, recommend mitigation
        # if not assessment['checks']['fairness']['passed']:
        #     print("Fairness violations detected. Running bias mitigation...")
        #     mitigation_results = self.bias_mitigator.compare_mitigation_strategies(
        #         X_train, y_train, X_test, y_test,
        #         sensitive_features_train, sensitive_features_test
        #     )
        #     assessment['checks']['bias_mitigation'] = {
        #         'required': True,
        #         'strategies_evaluated': mitigation_results
        #     }

        # ============================================
        # 4. MODEL CARD GENERATION
        # ============================================
        print("Generating model card...")

        # TODO: Generate model card with all information
        # self.model_card = self._generate_model_card(
        #     assessment['checks']['performance'],
        #     self.fairness_report
        # )

        # TODO: Save model card
        # self.model_card_generator.save_model_card(
        #     self.model_card,
        #     f"model_cards/{self.model_name}_v{self.model_version}.md"
        # )

        # assessment['checks']['model_card'] = {
        #     'generated': True,
        #     'path': f"model_cards/{self.model_name}_v{self.model_version}.md"
        # }

        # ============================================
        # 5. DETERMINE OVERALL GOVERNANCE STATUS
        # ============================================

        # TODO: Determine if model passes governance
        # all_checks_passed = all(
        #     check.get('passed', True)
        #     for check in assessment['checks'].values()
        # )

        # if all_checks_passed:
        #     self.governance_status = "APPROVED"
        # elif assessment['checks']['fairness']['passed']:
        #     self.governance_status = "APPROVED_WITH_CONDITIONS"
        # else:
        #     self.governance_status = "REJECTED"

        # assessment['governance_status'] = self.governance_status

        return assessment

    def _generate_model_card(
        self,
        performance_metrics: Dict,
        fairness_report: Any
    ) -> ModelCard:
        """Generate model card from assessment results."""
        # TODO: Create model card sections
        # TODO: Include performance and fairness information
        # TODO: Return ModelCard object
        pass

    def log_prediction_with_governance(
        self,
        user_id: str,
        input_data: Dict[str, Any],
        prediction: Any,
        confidence: float,
        sensitive_features: Dict[str, Any],
        explanation: Dict = None
    ) -> Dict[str, Any]:
        """
        Make prediction with full governance logging.

        Args:
            user_id: User making prediction
            input_data: Input features
            prediction: Model prediction
            confidence: Prediction confidence
            sensitive_features: Sensitive attributes
            explanation: Prediction explanation

        Returns:
            Prediction result with governance metadata
        """
        # ============================================
        # 1. PRE-PREDICTION CHECKS
        # ============================================

        # TODO: Check if model is approved for use
        # if self.governance_status not in ['APPROVED', 'APPROVED_WITH_CONDITIONS']:
        #     return {
        #         'error': 'Model not approved for production use',
        #         'governance_status': self.governance_status
        #     }

        # ============================================
        # 2. FAIRNESS CHECK ON INDIVIDUAL PREDICTION
        # ============================================

        # TODO: Run fairness check if sensitive features provided
        fairness_check_passed = True
        # if sensitive_features:
        #     fairness_check_passed = self._check_individual_fairness(
        #         input_data, prediction, sensitive_features
        #     )

        # ============================================
        # 3. AUDIT LOGGING
        # ============================================

        # TODO: Log prediction
        # log_id = self.audit_logger.log_prediction(
        #     model_name=self.model_name,
        #     model_version=self.model_version,
        #     user_id=user_id,
        #     input_data=input_data,
        #     prediction=prediction,
        #     confidence=confidence,
        #     explanation=explanation,
        #     sensitive_features=sensitive_features,
        #     fairness_check_passed=fairness_check_passed
        # )

        # ============================================
        # 4. RETURN RESULT
        # ============================================

        # return {
        #     'prediction': prediction,
        #     'confidence': confidence,
        #     'explanation': explanation,
        #     'fairness_check_passed': fairness_check_passed,
        #     'log_id': log_id,
        #     'governance_status': self.governance_status
        # }
        pass

    def _check_individual_fairness(
        self,
        input_data: Dict,
        prediction: Any,
        sensitive_features: Dict
    ) -> bool:
        """
        Check fairness for individual prediction.

        Args:
            input_data: Input features
            prediction: Prediction
            sensitive_features: Sensitive attributes

        Returns:
            True if fairness check passed
        """
        # TODO: Implement individual fairness check
        # - Check if prediction is consistent with similar individuals
        # - Check if sensitive features influenced decision inappropriately
        # - Return True/False
        pass

    def generate_governance_report(
        self,
        start_date: datetime,
        end_date: datetime,
        output_path: str = "governance_report.html"
    ):
        """
        Generate comprehensive governance report.

        Args:
            start_date: Report period start
            end_date: Report period end
            output_path: Output file path
        """
        # TODO: Query audit logs
        logs = self.audit_logger.query_logs(start_date, end_date, self.model_name)

        # TODO: Calculate governance metrics
        governance_metrics = self._calculate_governance_metrics(logs)

        # TODO: Generate HTML report with:
        #   - Executive summary
        #   - Model card
        #   - Fairness assessment results
        #   - Audit log statistics
        #   - Compliance status
        #   - Recommendations

        # TODO: Save report
        pass

    def _calculate_governance_metrics(self, logs: List) -> Dict:
        """Calculate governance metrics from logs."""
        # TODO: Calculate:
        #   - Total predictions
        #   - Fairness check pass rate
        #   - Predictions by sensitive group
        #   - Average confidence
        #   - Trend analysis
        pass

    def monitor_ongoing_compliance(
        self,
        lookback_days: int = 30
    ) -> Dict[str, Any]:
        """
        Monitor ongoing compliance over time.

        Args:
            lookback_days: Number of days to look back

        Returns:
            Compliance monitoring results
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=lookback_days)

        # TODO: Query recent logs
        logs = self.audit_logger.query_logs(start_date, end_date, self.model_name)

        # TODO: Check for compliance issues
        #   - Fairness degradation
        #   - High failure rate
        #   - Unusual patterns
        #   - Bias drift

        # TODO: Generate alerts if issues detected

        # TODO: Return monitoring results
        pass

    def verify_governance_integrity(self) -> Dict[str, Any]:
        """
        Verify integrity of governance system.

        Returns:
            Integrity check results
        """
        results = {
            'timestamp': datetime.now(),
            'checks': {}
        }

        # TODO: 1. Verify audit log integrity
        # is_valid, issues = self.audit_logger.verify_log_integrity()
        # results['checks']['audit_log_integrity'] = {
        #     'passed': is_valid,
        #     'issues': issues
        # }

        # TODO: 2. Verify model card exists and is valid
        # if self.model_card:
        #     validation_issues = self.model_card_generator.validate_model_card(
        #         self.model_card
        #     )
        #     results['checks']['model_card_validity'] = {
        #         'passed': len(validation_issues) == 0,
        #         'issues': validation_issues
        #     }

        # TODO: 3. Check governance status is current
        # results['checks']['governance_status'] = {
        #     'status': self.governance_status,
        #     'last_assessment': 'timestamp of last assessment'
        # }

        # TODO: Return results
        return results
```

### Deployment Example

```python
# scripts/deploy_with_governance.py
"""Deploy model with governance framework."""

import joblib
from src.governance.governance_framework import GovernanceFramework


def deploy_model_with_governance():
    """Deploy model with full governance."""

    # TODO: Load trained model
    model = joblib.load("models/loan_approval_model.pkl")

    # TODO: Load test data
    X_test = pd.read_csv("data/X_test.csv")
    y_test = pd.read_csv("data/y_test.csv").values.ravel()
    sensitive_features = pd.read_csv("data/sensitive_features_test.csv")

    # TODO: Initialize governance framework
    governance = GovernanceFramework(
        model_name="loan_approval_model",
        model_version="1.2.0",
        sensitive_features=['gender', 'race', 'age']
    )

    # TODO: Assess governance before deployment
    assessment = governance.assess_model_governance(
        model, X_test, y_test, sensitive_features
    )

    print(f"\nGovernance Status: {assessment['governance_status']}")

    # TODO: Only deploy if approved
    if assessment['governance_status'] in ['APPROVED', 'APPROVED_WITH_CONDITIONS']:
        print("Model approved for deployment!")

        # TODO: Save model with governance metadata
        deployment_package = {
            'model': model,
            'governance': governance,
            'assessment': assessment
        }
        joblib.dump(deployment_package, "deployed_models/loan_model_v1.2.0.pkl")

        print("Model deployed with governance framework.")
    else:
        print("Model REJECTED for deployment due to governance violations.")
        print("Violations:", assessment['checks']['fairness']['violations'])


if __name__ == "__main__":
    deploy_model_with_governance()
```

### Success Criteria

- [ ] Complete governance framework integrates all components
- [ ] Pre-deployment assessment works correctly
- [ ] Predictions logged with full governance
- [ ] Governance reports generated
- [ ] Ongoing compliance monitoring functions
- [ ] Integrity verification works
- [ ] Framework ready for production use

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Integration**: Use composition to combine governance components
2. **Assessment Pipeline**: Run checks in sequence, collect results
3. **Approval Logic**: Define clear criteria for approval/rejection
4. **Monitoring**: Track metrics over time windows
5. **Reporting**: Combine data from all components into unified report
6. **Production Ready**: Handle errors gracefully, log all operations

</details>

---

## Bonus Challenges

### Challenge 1: GDPR Compliance Module

Implement GDPR-compliant features:
- Right to explanation
- Right to be forgotten
- Data minimization
- Consent tracking

### Challenge 2: Model Risk Management

Implement model risk tier classification:
- Risk assessment based on use case
- Different governance requirements by tier
- Approval workflows

### Challenge 3: Fairness Drift Detection

Implement fairness monitoring over time:
- Detect fairness degradation
- Trigger retraining when fairness drifts
- Adaptive fairness thresholds

---

## Additional Resources

- **Fairlearn**: [Documentation](https://fairlearn.org/)
- **Model Cards**: [Google Research Paper](https://arxiv.org/abs/1810.03993)
- **EU AI Act**: [Regulatory Framework](https://artificialintelligenceact.eu/)
- **NIST AI Risk Management**: [Framework](https://www.nist.gov/itl/ai-risk-management-framework)

---

## Submission Guidelines

For each exercise, submit:
1. **Code**: All implementation files
2. **Model Cards**: Generated documentation
3. **Audit Logs**: Example audit trails
4. **Reports**: Governance and fairness reports
5. **Documentation**: Governance framework guide

**Estimated Total Time**: 6-9 hours
**Difficulty**: Intermediate to Advanced

Good luck!
