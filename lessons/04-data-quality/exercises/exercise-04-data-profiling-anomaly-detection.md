## Exercise 4: Data Profiling & Anomaly Detection (90 minutes)

**Objective**: Build automated data profiling and anomaly detection system.

### Background

You need to automatically profile datasets to:
- Generate comprehensive data reports
- Detect anomalies in production data
- Compare datasets (train vs. test vs. production)
- Create data quality dashboards

### Tasks

1. **Implement comprehensive data profiler**
2. **Create anomaly detection pipeline**
3. **Build dataset comparison tool**
4. **Generate HTML profiling reports**
5. **Create real-time monitoring dashboard**

### Starter Code

```python
# data_profiler.py
"""Comprehensive data profiling for ML datasets."""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import json
from pathlib import Path


@dataclass
class ColumnProfile:
    """Profile for a single column."""
    name: str
    dtype: str
    count: int
    missing_count: int
    missing_percentage: float
    unique_count: int
    unique_percentage: float

    # For numerical columns
    mean: Optional[float] = None
    std: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    q25: Optional[float] = None
    median: Optional[float] = None
    q75: Optional[float] = None
    skewness: Optional[float] = None
    kurtosis: Optional[float] = None

    # For categorical columns
    mode: Optional[str] = None
    mode_frequency: Optional[int] = None
    top_values: Optional[Dict] = None

    # Data quality flags
    has_outliers: bool = False
    has_high_cardinality: bool = False
    is_constant: bool = False
    is_unique_id: bool = False


@dataclass
class DatasetProfile:
    """Complete dataset profile."""
    name: str
    n_rows: int
    n_columns: int
    memory_usage_mb: float
    duplicate_rows: int
    column_profiles: List[ColumnProfile]
    correlations: Optional[Dict] = None
    warnings: List[str] = None


class DataProfiler:
    """Generate comprehensive data profiles."""

    def __init__(self, high_cardinality_threshold: int = 100):
        self.high_cardinality_threshold = high_cardinality_threshold

    def profile_column(
        self,
        series: pd.Series,
        detect_outliers: bool = True
    ) -> ColumnProfile:
        """
        Profile a single column.

        Args:
            series: Pandas Series to profile
            detect_outliers: Whether to detect outliers

        Returns:
            ColumnProfile with statistics
        """
        # TODO: Implement column profiling
        # - Basic stats (count, missing, unique)
        # - Type-specific stats (numerical vs categorical)
        # - Outlier detection
        # - Quality flags
        pass

    def profile_dataset(
        self,
        df: pd.DataFrame,
        name: str = "dataset",
        compute_correlations: bool = True
    ) -> DatasetProfile:
        """
        Profile entire dataset.

        Args:
            df: DataFrame to profile
            name: Dataset name
            compute_correlations: Whether to compute correlation matrix

        Returns:
            DatasetProfile
        """
        # TODO: Implement dataset profiling
        # - Overall statistics
        # - Profile each column
        # - Compute correlations
        # - Generate warnings
        pass

    def detect_data_quality_issues(
        self,
        profile: DatasetProfile
    ) -> List[str]:
        """
        Detect data quality issues from profile.

        Args:
            profile: Dataset profile

        Returns:
            List of data quality warnings
        """
        warnings = []

        # TODO: Check for issues
        # - High missing rate (>20%)
        # - High duplicate rate (>5%)
        # - Constant columns
        # - High cardinality categoricals
        # - Highly correlated features (>0.95)
        # - Columns with all unique values (potential IDs)
        # - Imbalanced target variable

        return warnings

    def compare_profiles(
        self,
        profile1: DatasetProfile,
        profile2: DatasetProfile
    ) -> Dict:
        """
        Compare two dataset profiles.

        Args:
            profile1: First dataset profile
            profile2: Second dataset profile

        Returns:
            Comparison report
        """
        # TODO: Compare profiles
        # - Schema differences
        # - Statistical differences
        # - Distribution changes
        # - Return detailed comparison
        pass

    def export_profile(
        self,
        profile: DatasetProfile,
        output_path: str,
        format: str = 'json'
    ):
        """
        Export profile to file.

        Args:
            profile: Dataset profile
            output_path: Output file path
            format: Export format ('json', 'html', 'markdown')
        """
        # TODO: Export profile
        if format == 'json':
            # TODO: Export as JSON
            pass
        elif format == 'html':
            # TODO: Generate HTML report
            pass
        elif format == 'markdown':
            # TODO: Generate Markdown report
            pass
```

```python
# anomaly_detector.py
"""Production anomaly detection system."""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


class ProductionAnomalyDetector:
    """Real-time anomaly detection for production data."""

    def __init__(
        self,
        reference_data: pd.DataFrame,
        contamination: float = 0.05
    ):
        """
        Initialize anomaly detector.

        Args:
            reference_data: Clean reference data for training
            contamination: Expected anomaly rate
        """
        self.reference_data = reference_data
        self.contamination = contamination
        self.scaler = StandardScaler()
        self.detector = None
        self._train_detector()

    def _train_detector(self):
        """Train anomaly detection model on reference data."""
        # TODO: Prepare data
        # - Select numerical features
        # - Handle missing values
        # - Scale features

        # TODO: Train Isolation Forest
        # self.detector = IsolationForest(
        #     contamination=self.contamination,
        #     random_state=42
        # )
        # self.detector.fit(scaled_data)
        pass

    def detect_anomalies(
        self,
        data: pd.DataFrame,
        return_scores: bool = True
    ) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Detect anomalies in new data.

        Args:
            data: New data to check
            return_scores: Whether to return anomaly scores

        Returns:
            Tuple of (anomaly_labels, anomaly_scores)
        """
        # TODO: Preprocess data
        # TODO: Predict anomalies
        # TODO: Return labels and optionally scores
        pass

    def detect_point_anomaly(
        self,
        data_point: Dict
    ) -> Dict:
        """
        Detect if single data point is anomalous.

        Args:
            data_point: Dictionary with feature values

        Returns:
            Detection result with details
        """
        # TODO: Convert to DataFrame
        # TODO: Detect anomaly
        # TODO: Return detailed result
        pass

    def get_anomaly_explanation(
        self,
        data_point: Dict,
        top_n: int = 5
    ) -> List[Dict]:
        """
        Explain why a point is anomalous.

        Args:
            data_point: Anomalous data point
            top_n: Number of top contributing features

        Returns:
            List of feature contributions
        """
        # TODO: Calculate feature contributions
        # - Compare to reference statistics
        # - Identify most unusual features
        # - Return ranked explanations
        pass


class AnomalyMonitor:
    """Monitor anomalies over time."""

    def __init__(self, detector: ProductionAnomalyDetector):
        self.detector = detector
        self.anomaly_history = []

    def log_batch(
        self,
        batch_data: pd.DataFrame,
        timestamp: str = None
    ) -> Dict:
        """
        Process and log a batch of data.

        Args:
            batch_data: Batch to process
            timestamp: Batch timestamp

        Returns:
            Batch anomaly report
        """
        # TODO: Detect anomalies in batch
        # TODO: Calculate metrics
        # TODO: Log to history
        # TODO: Return report
        pass

    def get_anomaly_rate_over_time(self) -> pd.DataFrame:
        """Get time series of anomaly rates."""
        # TODO: Extract anomaly rates from history
        # TODO: Return as DataFrame
        pass

    def alert_if_threshold_exceeded(
        self,
        threshold: float = 0.10
    ) -> Optional[str]:
        """
        Check if recent anomaly rate exceeds threshold.

        Args:
            threshold: Anomaly rate threshold

        Returns:
            Alert message if threshold exceeded
        """
        # TODO: Calculate recent anomaly rate
        # TODO: Compare to threshold
        # TODO: Return alert if exceeded
        pass
```

```python
# comparison_report.py
"""Generate dataset comparison reports."""

import pandas as pd
from data_profiler import DataProfiler, DatasetProfile


def compare_train_test_production(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    production_df: pd.DataFrame
) -> str:
    """
    Compare training, test, and production datasets.

    Args:
        train_df: Training data
        test_df: Test data
        production_df: Production data

    Returns:
        Formatted comparison report
    """
    profiler = DataProfiler()

    # TODO: Profile each dataset
    train_profile = profiler.profile_dataset(train_df, "training")
    test_profile = profiler.profile_dataset(test_df, "test")
    prod_profile = profiler.profile_dataset(production_df, "production")

    # TODO: Compare profiles
    train_test_comparison = profiler.compare_profiles(train_profile, test_profile)
    train_prod_comparison = profiler.compare_profiles(train_profile, prod_profile)

    # TODO: Generate report
    # - Schema differences
    # - Distribution differences
    # - Data quality differences
    # - Recommendations

    # TODO: Return formatted report
    pass
```

### Success Criteria

- [ ] Data profiler generates complete column profiles
- [ ] Dataset-level statistics computed correctly
- [ ] Anomaly detector trained on reference data
- [ ] Real-time anomaly detection works
- [ ] Profile comparison identifies differences
- [ ] HTML reports generated
- [ ] Monitoring tracks anomalies over time

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Profiling**: Use `df.describe()`, `df.dtypes`, `df.memory_usage()` for basics
2. **Categorical Stats**: Use `value_counts()` for mode and top values
3. **Outlier Detection**: Use IQR method or Isolation Forest
4. **Correlations**: Use `df.corr()` but only for numerical columns
5. **HTML Export**: Use Jinja2 templates or pandas `to_html()`
6. **Anomaly Explanation**: Calculate z-scores for each feature

</details>

---
