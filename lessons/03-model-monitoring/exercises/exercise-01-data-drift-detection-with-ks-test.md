## Exercise 1: Data Drift Detection with KS Test (75 minutes)

**Objective**: Implement data drift detection using the Kolmogorov-Smirnov statistical test.

### Background

Your production model is experiencing decreased accuracy. You need to detect if input data distribution has changed compared to training data using statistical tests.

### Tasks

1. **Implement KS test for numerical features**
2. **Set appropriate drift thresholds**
3. **Create visualization of drift**
4. **Build automated drift detection pipeline**
5. **Generate drift reports**

### Starter Code

```python
# src/monitoring/drift_detector.py
"""Data drift detection using statistical tests."""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class DriftResult:
    """Container for drift detection results."""
    feature_name: str
    ks_statistic: float
    p_value: float
    is_drift: bool
    threshold: float

class KSDriftDetector:
    """Kolmogorov-Smirnov drift detector for numerical features."""

    def __init__(self, threshold: float = 0.05):
        """
        Initialize drift detector.

        Args:
            threshold: P-value threshold for drift detection (default: 0.05)
        """
        self.threshold = threshold
        self.reference_data = None

    def fit(self, reference_data: pd.DataFrame):
        """
        Fit detector on reference (training) data.

        Args:
            reference_data: Reference dataset (typically training data)
        """
        # TODO: Store reference data
        # TODO: Validate data types
        # TODO: Handle missing values
        pass

    def detect_drift(
        self,
        current_data: pd.DataFrame,
        features: List[str] = None
    ) -> Dict[str, DriftResult]:
        """
        Detect drift in current data compared to reference.

        Args:
            current_data: Current production data
            features: List of features to check (None = all numerical features)

        Returns:
            Dictionary mapping feature names to DriftResult objects
        """
        # TODO: Validate inputs
        # TODO: Select features to test
        # TODO: For each feature:
        #   - Perform KS test
        #   - Create DriftResult
        #   - Determine if drift detected
        # TODO: Return results dictionary
        pass

    def _perform_ks_test(
        self,
        reference: np.ndarray,
        current: np.ndarray
    ) -> Tuple[float, float]:
        """
        Perform Kolmogorov-Smirnov test.

        Args:
            reference: Reference data array
            current: Current data array

        Returns:
            Tuple of (ks_statistic, p_value)
        """
        # TODO: Use scipy.stats.ks_2samp
        # TODO: Handle edge cases (empty arrays, all same values)
        pass

    def visualize_drift(
        self,
        feature_name: str,
        current_data: pd.DataFrame,
        save_path: str = None
    ):
        """
        Create visualization comparing distributions.

        Args:
            feature_name: Name of feature to visualize
            current_data: Current data
            save_path: Path to save plot (optional)
        """
        # TODO: Create overlapping histograms
        # TODO: Add KDE plots
        # TODO: Include KS statistic and p-value in title
        # TODO: Save or display plot
        pass

    def generate_report(
        self,
        drift_results: Dict[str, DriftResult],
        output_path: str = "drift_report.html"
    ):
        """
        Generate HTML report of drift detection results.

        Args:
            drift_results: Results from detect_drift()
            output_path: Path for HTML report
        """
        # TODO: Create HTML report with:
        #   - Summary table
        #   - Drift visualizations
        #   - Recommendations
        pass
```

### Validation Tests

```python
# tests/test_drift_detector.py
import pytest
import pandas as pd
import numpy as np
from src.monitoring.drift_detector import KSDriftDetector, DriftResult

@pytest.fixture
def reference_data():
    """Generate reference dataset."""
    np.random.seed(42)
    return pd.DataFrame({
        'feature_1': np.random.normal(0, 1, 1000),
        'feature_2': np.random.exponential(2, 1000),
        'feature_3': np.random.uniform(0, 10, 1000)
    })

@pytest.fixture
def drifted_data():
    """Generate drifted dataset (different distribution)."""
    np.random.seed(123)
    return pd.DataFrame({
        'feature_1': np.random.normal(2, 1.5, 1000),  # Shifted mean, different std
        'feature_2': np.random.exponential(2, 1000),   # Same distribution
        'feature_3': np.random.uniform(5, 15, 1000)    # Shifted range
    })

def test_detector_initialization():
    """Test that detector initializes correctly."""
    detector = KSDriftDetector(threshold=0.05)
    assert detector.threshold == 0.05
    # TODO: Add more assertions

def test_fit_stores_reference_data(reference_data):
    """Test that fit stores reference data."""
    # TODO: Implement test
    pass

def test_detect_drift_identifies_shifted_distribution(reference_data, drifted_data):
    """Test that drift is detected for shifted distributions."""
    detector = KSDriftDetector(threshold=0.05)
    detector.fit(reference_data)
    results = detector.detect_drift(drifted_data)

    # TODO: Assert feature_1 shows drift (shifted mean)
    # TODO: Assert feature_2 shows no drift (same distribution)
    # TODO: Assert feature_3 shows drift (shifted range)
    pass

def test_ks_test_returns_valid_values(reference_data):
    """Test that KS test returns valid statistics."""
    # TODO: Test with identical distributions (should have high p-value)
    # TODO: Test with different distributions (should have low p-value)
    pass

def test_visualization_creates_plot(reference_data, drifted_data, tmp_path):
    """Test that visualization is created."""
    # TODO: Generate visualization
    # TODO: Assert file is created
    pass
```

### Success Criteria

- [ ] KS test correctly identifies drift in shifted distributions
- [ ] P-values are calculated accurately
- [ ] Drift threshold is configurable
- [ ] Visualizations clearly show distribution differences
- [ ] Report includes all tested features
- [ ] Edge cases handled (missing values, constant features)

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **KS Test**: Use `scipy.stats.ks_2samp(reference, current)` - returns (statistic, p_value)
2. **Drift Detection**: If p_value < threshold, distributions are significantly different (drift detected)
3. **Visualization**: Use `plt.hist()` with `alpha=0.5` for overlapping histograms
4. **Missing Values**: Drop or impute before testing - KS test requires complete data
5. **Multiple Testing**: Consider Bonferroni correction when testing many features

```python
# Example KS test usage
from scipy import stats
ks_stat, p_value = stats.ks_2samp(reference_array, current_array)
is_drift = p_value < threshold
```

</details>

---
