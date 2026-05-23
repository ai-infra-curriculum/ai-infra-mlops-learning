## Exercise 2: Population Stability Index (PSI) Implementation (90 minutes)

**Objective**: Implement PSI calculation for monitoring feature distribution stability.

### Background

PSI (Population Stability Index) is widely used in production ML systems to measure how much a feature's distribution has changed. Implement PSI calculation and interpretation.

### Tasks

1. **Implement PSI calculation**
2. **Set interpretation thresholds**
3. **Handle edge cases (zero bins)**
4. **Create PSI tracking over time**
5. **Build alerting logic**

### Starter Code

```python
# src/monitoring/psi_calculator.py
"""Population Stability Index (PSI) calculator."""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import warnings

class PSICalculator:
    """Calculate Population Stability Index for features."""

    def __init__(self, n_bins: int = 10, bin_strategy: str = 'quantile'):
        """
        Initialize PSI calculator.

        Args:
            n_bins: Number of bins for discretization
            bin_strategy: 'quantile' or 'uniform' binning
        """
        self.n_bins = n_bins
        self.bin_strategy = bin_strategy
        self.bin_edges = {}

    def fit(self, reference_data: pd.DataFrame, features: List[str] = None):
        """
        Fit PSI calculator on reference data.

        Args:
            reference_data: Reference (training) data
            features: Features to track (None = all numerical)
        """
        # TODO: Determine features to track
        # TODO: Create bins for each feature
        # TODO: Store bin edges
        pass

    def _create_bins(self, data: np.ndarray) -> np.ndarray:
        """
        Create bin edges for a feature.

        Args:
            data: Feature values

        Returns:
            Array of bin edges
        """
        # TODO: Create bins based on strategy
        # TODO: Handle edge cases (< n_bins unique values)
        # Quantile: np.percentile
        # Uniform: np.linspace
        pass

    def calculate_psi(
        self,
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame,
        feature: str
    ) -> float:
        """
        Calculate PSI for a single feature.

        PSI = Σ (current_pct - reference_pct) * ln(current_pct / reference_pct)

        Args:
            reference_data: Reference data
            current_data: Current data
            feature: Feature name

        Returns:
            PSI value
        """
        # TODO: Get bin edges for feature
        # TODO: Bin both datasets
        # TODO: Calculate percentages in each bin
        # TODO: Handle zero percentages (add small epsilon)
        # TODO: Calculate PSI formula
        pass

    def calculate_psi_all_features(
        self,
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame
    ) -> Dict[str, float]:
        """
        Calculate PSI for all tracked features.

        Args:
            reference_data: Reference data
            current_data: Current data

        Returns:
            Dictionary mapping feature names to PSI values
        """
        # TODO: Calculate PSI for each feature
        # TODO: Return dictionary of results
        pass

    def interpret_psi(self, psi_value: float) -> str:
        """
        Interpret PSI value.

        Args:
            psi_value: Calculated PSI

        Returns:
            Interpretation string
        """
        # TODO: Implement interpretation rules:
        # PSI < 0.1: No significant change
        # 0.1 <= PSI < 0.2: Moderate change
        # PSI >= 0.2: Significant change (requires investigation)
        pass

    def track_psi_over_time(
        self,
        reference_data: pd.DataFrame,
        current_batches: List[pd.DataFrame],
        timestamps: List[str]
    ) -> pd.DataFrame:
        """
        Track PSI over multiple time periods.

        Args:
            reference_data: Reference data
            current_batches: List of data batches
            timestamps: Timestamps for each batch

        Returns:
            DataFrame with PSI values over time
        """
        # TODO: Calculate PSI for each batch
        # TODO: Create time series DataFrame
        # TODO: Return results
        pass

    def generate_alerts(
        self,
        psi_values: Dict[str, float],
        threshold: float = 0.2
    ) -> List[str]:
        """
        Generate alerts for features exceeding PSI threshold.

        Args:
            psi_values: Dictionary of PSI values
            threshold: Alert threshold

        Returns:
            List of alert messages
        """
        # TODO: Check each PSI value
        # TODO: Generate alert message for violations
        # TODO: Return list of alerts
        pass
```

### Validation Tests

```python
# tests/test_psi_calculator.py
import pytest
import pandas as pd
import numpy as np
from src.monitoring.psi_calculator import PSICalculator

@pytest.fixture
def reference_data():
    np.random.seed(42)
    return pd.DataFrame({
        'feature_1': np.random.normal(0, 1, 1000),
        'feature_2': np.random.exponential(2, 1000)
    })

def test_psi_identical_distributions(reference_data):
    """Test PSI is ~0 for identical distributions."""
    calculator = PSICalculator(n_bins=10)
    calculator.fit(reference_data)
    psi = calculator.calculate_psi(reference_data, reference_data, 'feature_1')

    # TODO: Assert PSI is close to 0
    assert psi < 0.01

def test_psi_shifted_distribution(reference_data):
    """Test PSI detects shifted distribution."""
    calculator = PSICalculator(n_bins=10)
    calculator.fit(reference_data)

    # Create shifted data
    shifted_data = reference_data.copy()
    shifted_data['feature_1'] = shifted_data['feature_1'] + 3

    psi = calculator.calculate_psi(reference_data, shifted_data, 'feature_1')

    # TODO: Assert PSI > 0.2 (significant change)
    pass

def test_psi_interpretation():
    """Test PSI interpretation logic."""
    # TODO: Test interpretation for different PSI values
    pass

def test_handles_edge_cases():
    """Test handling of edge cases."""
    # TODO: Test with constant feature
    # TODO: Test with very few unique values
    # TODO: Test with missing values
    pass
```

### Success Criteria

- [ ] PSI calculation is mathematically correct
- [ ] Handles zero bin percentages (epsilon smoothing)
- [ ] Interpretation thresholds are appropriate
- [ ] Time series tracking works correctly
- [ ] Alerts are generated for violations
- [ ] Edge cases handled gracefully

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **PSI Formula**: `PSI = Σ (current% - reference%) * ln(current% / reference%)`
2. **Zero Handling**: Add small epsilon (1e-10) to avoid log(0)
3. **Binning**: Use `pd.cut()` with pre-computed bin edges
4. **Interpretation**:
   - PSI < 0.1: Stable
   - 0.1-0.2: Moderate shift
   - \> 0.2: Significant shift
5. **Quantile Bins**: `np.percentile(data, np.linspace(0, 100, n_bins + 1))`

</details>

---
