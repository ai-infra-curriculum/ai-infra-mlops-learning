## Exercise 3: Statistical Data Quality Checks (75 minutes)

**Objective**: Implement statistical validation to detect data drift and anomalies.

### Background

Production data distributions can shift over time (data drift). You need to:
- Compare new data against reference distributions
- Detect outliers using multiple methods
- Validate correlation structure
- Alert on significant changes

### Tasks

1. **Build statistical validator** with reference data
2. **Implement distribution testing** (KS test, Chi-square)
3. **Create multi-method outlier detection**
4. **Validate correlation structure**
5. **Generate drift detection reports**

### Starter Code

```python
# statistical_validator.py
"""Statistical validation for data quality."""

from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of statistical validation check."""
    check_name: str
    passed: bool
    statistic: float
    threshold: float
    details: dict


class StatisticalValidator:
    """Statistical validation against reference data."""

    def __init__(self, reference_data: pd.DataFrame):
        """
        Initialize validator with reference data.

        Args:
            reference_data: Clean training/validation data as reference
        """
        self.reference_data = reference_data
        self.stats = self._compute_reference_stats()
        self.correlations = self._compute_correlations()

    def _compute_reference_stats(self) -> Dict[str, Dict]:
        """Compute statistical properties of reference data."""
        stats_dict = {}

        for col in self.reference_data.select_dtypes(include=[np.number]).columns:
            # TODO: Compute statistics for each numerical column
            # - mean, std, min, max
            # - quantiles (0.01, 0.25, 0.5, 0.75, 0.99)
            # - skewness, kurtosis
            # - Store in stats_dict[col]
            pass

        return stats_dict

    def _compute_correlations(self) -> pd.DataFrame:
        """Compute correlation matrix of reference data."""
        # TODO: Calculate and return correlation matrix
        pass

    def validate_distribution(
        self,
        data: pd.DataFrame,
        column: str,
        test: str = 'ks',
        p_threshold: float = 0.05
    ) -> ValidationResult:
        """
        Test if distribution matches reference.

        Args:
            data: New data to validate
            column: Column name
            test: Statistical test ('ks' or 'chi2')
            p_threshold: P-value threshold for significance

        Returns:
            ValidationResult with test outcome
        """
        ref_values = self.reference_data[column].dropna()
        new_values = data[column].dropna()

        if test == 'ks':
            # TODO: Perform Kolmogorov-Smirnov test
            # statistic, p_value = stats.ks_2samp(ref_values, new_values)
            pass
        elif test == 'chi2':
            # TODO: Perform Chi-square test
            # - Bin data
            # - Compare distributions
            pass
        else:
            raise ValueError(f"Unknown test: {test}")

        # TODO: Create and return ValidationResult
        pass

    def validate_range(
        self,
        data: pd.DataFrame,
        column: str,
        method: str = 'iqr',
        **kwargs
    ) -> ValidationResult:
        """
        Validate that values are within expected range.

        Args:
            data: Data to validate
            column: Column name
            method: Method ('iqr', 'zscore', 'quantile')
            **kwargs: Method-specific parameters

        Returns:
            ValidationResult with outlier information
        """
        values = data[column]
        ref_stats = self.stats[column]

        if method == 'iqr':
            # TODO: IQR method
            # multiplier = kwargs.get('multiplier', 1.5)
            # Q1, Q3 = ref_stats['q25'], ref_stats['q75']
            # IQR = Q3 - Q1
            # lower = Q1 - multiplier * IQR
            # upper = Q3 + multiplier * IQR
            # outliers = (values < lower) | (values > upper)
            pass

        elif method == 'zscore':
            # TODO: Z-score method
            # threshold = kwargs.get('threshold', 3.0)
            # z_scores = np.abs((values - ref_stats['mean']) / ref_stats['std'])
            # outliers = z_scores > threshold
            pass

        elif method == 'quantile':
            # TODO: Quantile method
            # lower_q = kwargs.get('lower_quantile', 0.01)
            # upper_q = kwargs.get('upper_quantile', 0.99)
            # lower = ref_stats[f'q{int(lower_q*100):02d}']
            # upper = ref_stats[f'q{int(upper_q*100):02d}']
            # outliers = (values < lower) | (values > upper)
            pass

        # TODO: Create and return ValidationResult
        pass

    def validate_correlation_structure(
        self,
        data: pd.DataFrame,
        threshold: float = 0.3
    ) -> ValidationResult:
        """
        Validate that correlation structure hasn't changed.

        Args:
            data: New data
            threshold: Maximum allowed correlation change

        Returns:
            ValidationResult with correlation drift information
        """
        # TODO: Compute correlation matrix for new data
        new_corr = data[self.correlations.columns].corr()

        # TODO: Calculate correlation difference
        corr_diff = np.abs(self.correlations - new_corr)

        # TODO: Find largest changes
        # Get upper triangle to avoid duplicates
        mask = np.triu(np.ones_like(corr_diff, dtype=bool), k=1)
        significant_changes = []

        # TODO: Identify significant changes
        # for i, j in zip(*np.where((corr_diff > threshold) & mask)):
        #     significant_changes.append({
        #         'features': (corr_diff.index[i], corr_diff.columns[j]),
        #         'ref_correlation': self.correlations.iloc[i, j],
        #         'new_correlation': new_corr.iloc[i, j],
        #         'change': corr_diff.iloc[i, j]
        #     })

        # TODO: Create and return ValidationResult
        pass

    def validate_all(
        self,
        data: pd.DataFrame,
        config: dict = None
    ) -> List[ValidationResult]:
        """
        Run all statistical validations.

        Args:
            data: Data to validate
            config: Configuration for validation checks

        Returns:
            List of ValidationResults
        """
        # TODO: Use default config if not provided
        if config is None:
            config = {
                'distribution_tests': ['ks'],
                'range_methods': ['iqr', 'zscore'],
                'check_correlations': True
            }

        results = []

        # TODO: Run distribution tests for numerical columns
        # TODO: Run range validations
        # TODO: Run correlation validation

        return results


class OutlierDetector:
    """Multivariate outlier detection."""

    @staticmethod
    def detect_isolation_forest(
        data: pd.DataFrame,
        contamination: float = 0.1,
        random_state: int = 42
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect outliers using Isolation Forest.

        Args:
            data: Input data
            contamination: Expected proportion of outliers
            random_state: Random seed

        Returns:
            Tuple of (outlier_labels, outlier_scores)
        """
        # TODO: Fit Isolation Forest
        # TODO: Predict outliers (-1 for outliers, 1 for inliers)
        # TODO: Get anomaly scores
        # TODO: Return labels and scores
        pass

    @staticmethod
    def detect_elliptic_envelope(
        data: pd.DataFrame,
        contamination: float = 0.1
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect outliers using Elliptic Envelope (assumes Gaussian).

        Args:
            data: Input data
            contamination: Expected proportion of outliers

        Returns:
            Tuple of (outlier_labels, outlier_scores)
        """
        # TODO: Fit Elliptic Envelope
        # TODO: Predict outliers
        # TODO: Get Mahalanobis distances
        # TODO: Return labels and scores
        pass

    @staticmethod
    def detect_lof(
        data: pd.DataFrame,
        n_neighbors: int = 20,
        contamination: float = 0.1
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect outliers using Local Outlier Factor.

        Args:
            data: Input data
            n_neighbors: Number of neighbors
            contamination: Expected proportion of outliers

        Returns:
            Tuple of (outlier_labels, outlier_scores)
        """
        from sklearn.neighbors import LocalOutlierFactor

        # TODO: Fit LOF
        # TODO: Predict outliers
        # TODO: Get LOF scores
        # TODO: Return labels and scores
        pass

    @staticmethod
    def ensemble_detection(
        data: pd.DataFrame,
        methods: List[str] = None,
        voting: str = 'majority'
    ) -> np.ndarray:
        """
        Ensemble outlier detection using multiple methods.

        Args:
            data: Input data
            methods: List of methods to use
            voting: 'majority' or 'unanimous'

        Returns:
            Array of outlier labels
        """
        if methods is None:
            methods = ['isolation_forest', 'elliptic_envelope', 'lof']

        # TODO: Run each detection method
        # TODO: Combine results based on voting strategy
        # TODO: Return ensemble outlier labels
        pass
```

```python
# drift_detector.py
"""Detect data drift over time."""

import pandas as pd
import numpy as np
from typing import Dict, List
import matplotlib.pyplot as plt
import seaborn as sns


class DataDriftDetector:
    """Monitor and detect data drift."""

    def __init__(self, reference_data: pd.DataFrame):
        self.reference_data = reference_data
        self.validator = StatisticalValidator(reference_data)
        self.drift_history = []

    def detect_drift(
        self,
        new_data: pd.DataFrame,
        timestamp: str = None
    ) -> Dict:
        """
        Detect drift in new data batch.

        Args:
            new_data: New data batch
            timestamp: Timestamp for this batch

        Returns:
            Drift detection results
        """
        # TODO: Run statistical validations
        results = self.validator.validate_all(new_data)

        # TODO: Identify drifted features
        drifted_features = [
            r for r in results
            if not r.passed and r.check_name.startswith('distribution')
        ]

        # TODO: Calculate drift score
        drift_score = len(drifted_features) / len(results)

        # TODO: Create drift report
        drift_report = {
            'timestamp': timestamp or pd.Timestamp.now(),
            'drift_score': drift_score,
            'drifted_features': [r.details.get('column') for r in drifted_features],
            'validation_results': results
        }

        # TODO: Store in history
        self.drift_history.append(drift_report)

        return drift_report

    def plot_drift_over_time(self, save_path: str = None):
        """
        Plot drift score over time.

        Args:
            save_path: Optional path to save plot
        """
        # TODO: Extract timestamps and drift scores
        # TODO: Create time series plot
        # TODO: Add threshold line
        # TODO: Save or show plot
        pass

    def generate_drift_report(self) -> str:
        """Generate human-readable drift report."""
        # TODO: Create formatted report
        # - Current drift status
        # - Trend over time
        # - Most frequently drifted features
        # - Recommendations
        pass
```

### Validation Tests

```python
# tests/test_statistical_validation.py
"""Tests for statistical validation."""

import pytest
import pandas as pd
import numpy as np
from statistical_validator import StatisticalValidator, OutlierDetector


def test_distribution_validation_no_drift(reference_data):
    """Test that same distribution passes validation."""
    validator = StatisticalValidator(reference_data)

    # TODO: Create data from same distribution
    # TODO: Validate distribution
    # TODO: Assert passed=True
    pass


def test_distribution_validation_detects_drift(reference_data):
    """Test that shifted distribution fails validation."""
    validator = StatisticalValidator(reference_data)

    # TODO: Create data with shifted distribution
    # TODO: Validate distribution
    # TODO: Assert passed=False
    pass


def test_outlier_detection_isolation_forest():
    """Test Isolation Forest outlier detection."""
    # TODO: Create data with known outliers
    # TODO: Run detection
    # TODO: Assert outliers are detected
    pass


@pytest.fixture
def reference_data():
    """Generate reference data."""
    np.random.seed(42)
    return pd.DataFrame({
        'feature1': np.random.normal(100, 15, 1000),
        'feature2': np.random.exponential(2, 1000),
        'feature3': np.random.uniform(0, 100, 1000)
    })

# Run with: pytest tests/test_statistical_validation.py -v
```

### Success Criteria

- [ ] Statistical validator computes reference statistics
- [ ] Distribution tests (KS, Chi-square) work correctly
- [ ] Multiple outlier detection methods implemented
- [ ] Correlation structure validation works
- [ ] Drift detector identifies shifted distributions
- [ ] Ensemble outlier detection combines methods
- [ ] Tests pass for various scenarios

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **KS Test**: Use `scipy.stats.ks_2samp()` for continuous distributions
2. **IQR Method**: `Q1 - 1.5*IQR` to `Q3 + 1.5*IQR` for outlier bounds
3. **Isolation Forest**: Set `contamination` based on expected outlier rate
4. **Correlation**: Use `pandas.DataFrame.corr()` for correlation matrix
5. **Ensemble**: Combine multiple methods with voting (2/3 methods agree)
6. **Performance**: Use vectorized operations instead of loops

</details>

---
