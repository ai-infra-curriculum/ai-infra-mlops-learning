## Exercise 3: Monitoring with Evidently AI (120 minutes)

**Objective**: Implement comprehensive monitoring using the Evidently AI library.

### Background

Evidently AI provides production-ready monitoring capabilities. Implement drift detection, data quality checks, and model performance monitoring using Evidently.

### Tasks

1. **Set up Evidently reports**
2. **Configure drift detection**
3. **Monitor data quality metrics**
4. **Track model performance**
5. **Generate interactive dashboards**

### Starter Code

```python
# src/monitoring/evidently_monitor.py
"""Model monitoring using Evidently AI."""

from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from evidently.metrics import (
    ColumnDriftMetric,
    DatasetDriftMetric,
    ColumnSummaryMetric,
    ClassificationQualityMetric
)
from evidently.test_suite import TestSuite
from evidently.tests import (
    TestNumberOfDriftedColumns,
    TestShareOfDriftedColumns,
    TestColumnDrift
)
import pandas as pd
from typing import Dict, List, Optional
from pathlib import Path

class EvidentlyMonitor:
    """Comprehensive monitoring using Evidently AI."""

    def __init__(
        self,
        target_column: str,
        prediction_column: str,
        numerical_features: List[str] = None,
        categorical_features: List[str] = None
    ):
        """
        Initialize Evidently monitor.

        Args:
            target_column: Name of target column
            prediction_column: Name of prediction column
            numerical_features: List of numerical feature names
            categorical_features: List of categorical feature names
        """
        self.target_column = target_column
        self.prediction_column = prediction_column
        self.numerical_features = numerical_features or []
        self.categorical_features = categorical_features or []

        # TODO: Create ColumnMapping object
        self.column_mapping = None

    def create_drift_report(
        self,
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame,
        output_path: str = "drift_report.html"
    ) -> Report:
        """
        Create data drift report.

        Args:
            reference_data: Reference (training) data
            current_data: Current production data
            output_path: Path to save HTML report

        Returns:
            Evidently Report object
        """
        # TODO: Create Report with DataDriftPreset
        # TODO: Run report on reference and current data
        # TODO: Save as HTML
        # TODO: Return report object
        pass

    def create_data_quality_report(
        self,
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame,
        output_path: str = "data_quality_report.html"
    ) -> Report:
        """
        Create data quality report.

        Args:
            reference_data: Reference data
            current_data: Current data
            output_path: Path to save HTML report

        Returns:
            Evidently Report object
        """
        # TODO: Create Report with DataQualityPreset
        # TODO: Run and save report
        pass

    def create_model_performance_report(
        self,
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame,
        output_path: str = "model_performance_report.html"
    ) -> Report:
        """
        Create model performance report.

        Args:
            reference_data: Reference data with predictions and actuals
            current_data: Current data with predictions and actuals
            output_path: Path to save HTML report

        Returns:
            Evidently Report object
        """
        # TODO: Create Report with ClassificationQualityMetric
        # TODO: Include metrics: accuracy, precision, recall, F1
        # TODO: Run and save report
        pass

    def run_drift_test_suite(
        self,
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame,
        max_drift_share: float = 0.3
    ) -> TestSuite:
        """
        Run drift test suite with pass/fail tests.

        Args:
            reference_data: Reference data
            current_data: Current data
            max_drift_share: Maximum allowed share of drifted columns

        Returns:
            TestSuite object
        """
        # TODO: Create TestSuite with drift tests
        # TODO: Add TestShareOfDriftedColumns
        # TODO: Add TestNumberOfDriftedColumns
        # TODO: Add TestColumnDrift for critical features
        # TODO: Run tests
        # TODO: Return results
        pass

    def extract_drift_metrics(self, report: Report) -> Dict:
        """
        Extract drift metrics from Evidently report.

        Args:
            report: Evidently Report object

        Returns:
            Dictionary of drift metrics
        """
        # TODO: Extract metrics from report
        # TODO: Get dataset drift score
        # TODO: Get per-column drift scores
        # TODO: Get number of drifted columns
        # TODO: Return structured dictionary
        pass

    def create_monitoring_dashboard(
        self,
        reference_data: pd.DataFrame,
        current_batches: List[pd.DataFrame],
        batch_timestamps: List[str],
        output_dir: str = "monitoring_dashboard"
    ):
        """
        Create monitoring dashboard with time series of metrics.

        Args:
            reference_data: Reference data
            current_batches: List of data batches
            batch_timestamps: Timestamps for each batch
            output_dir: Directory to save dashboard files
        """
        # TODO: Create output directory
        # TODO: For each batch:
        #   - Generate drift report
        #   - Extract metrics
        #   - Store time series data
        # TODO: Create time series visualizations
        # TODO: Generate dashboard HTML
        pass
```

### Example Usage

```python
# scripts/run_evidently_monitoring.py
"""Example script for running Evidently monitoring."""

import pandas as pd
from src.monitoring.evidently_monitor import EvidentlyMonitor

def main():
    # TODO: Load reference data (training data with predictions)
    reference_data = pd.read_csv('data/reference.csv')

    # TODO: Load current production data
    current_data = pd.read_csv('data/current.csv')

    # TODO: Initialize monitor
    monitor = EvidentlyMonitor(
        target_column='target',
        prediction_column='prediction',
        numerical_features=['feature_1', 'feature_2'],
        categorical_features=['feature_3']
    )

    # TODO: Generate drift report
    drift_report = monitor.create_drift_report(
        reference_data,
        current_data,
        output_path='reports/drift_report.html'
    )

    # TODO: Generate data quality report
    quality_report = monitor.create_data_quality_report(
        reference_data,
        current_data,
        output_path='reports/quality_report.html'
    )

    # TODO: Run test suite
    test_suite = monitor.run_drift_test_suite(
        reference_data,
        current_data,
        max_drift_share=0.3
    )

    # TODO: Print test results
    print("Test Results:", test_suite)

if __name__ == '__main__':
    main()
```

### Validation Tests

```python
# tests/test_evidently_monitor.py
import pytest
import pandas as pd
import numpy as np
from src.monitoring.evidently_monitor import EvidentlyMonitor

@pytest.fixture
def reference_data():
    """Generate reference dataset with predictions."""
    np.random.seed(42)
    n_samples = 1000
    return pd.DataFrame({
        'feature_1': np.random.normal(0, 1, n_samples),
        'feature_2': np.random.exponential(2, n_samples),
        'feature_3': np.random.choice(['A', 'B', 'C'], n_samples),
        'target': np.random.binomial(1, 0.3, n_samples),
        'prediction': np.random.binomial(1, 0.3, n_samples)
    })

def test_monitor_initialization():
    """Test monitor initializes correctly."""
    # TODO: Test initialization
    pass

def test_drift_report_generation(reference_data, tmp_path):
    """Test drift report is generated."""
    # TODO: Generate report
    # TODO: Assert HTML file is created
    # TODO: Assert report contains expected sections
    pass

def test_drift_metrics_extraction(reference_data):
    """Test drift metrics can be extracted."""
    # TODO: Generate report
    # TODO: Extract metrics
    # TODO: Assert metrics have expected structure
    pass

def test_test_suite_passes_for_identical_data(reference_data):
    """Test suite should pass for identical distributions."""
    # TODO: Run test suite
    # TODO: Assert all tests pass
    pass

def test_test_suite_fails_for_drifted_data(reference_data):
    """Test suite should fail for drifted data."""
    # TODO: Create drifted data
    # TODO: Run test suite
    # TODO: Assert drift tests fail
    pass
```

### Success Criteria

- [ ] Drift reports are generated successfully
- [ ] Reports are saved as interactive HTML
- [ ] Metrics can be extracted programmatically
- [ ] Test suites provide pass/fail results
- [ ] Dashboard shows metrics over time
- [ ] Integration with existing monitoring pipeline

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Column Mapping**: Define feature types for Evidently
```python
column_mapping = ColumnMapping(
    target='target',
    prediction='prediction',
    numerical_features=['feature_1', 'feature_2'],
    categorical_features=['feature_3']
)
```

2. **Report Creation**:
```python
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=ref, current_data=cur, column_mapping=mapping)
report.save_html('report.html')
```

3. **Extracting Metrics**: Use `report.as_dict()` to get JSON representation
4. **Test Suite**: Similar to Report but returns pass/fail for each test
5. **Dashboard**: Generate multiple reports over time and aggregate metrics

</details>

---
