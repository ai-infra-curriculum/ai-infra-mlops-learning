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
