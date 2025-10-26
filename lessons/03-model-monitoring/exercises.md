# Module 03: Model Monitoring - Exercises

## Overview

This exercise set provides hands-on practice with model monitoring concepts, including:
- Drift detection (data and concept drift)
- Statistical tests (KS test, PSI)
- Monitoring with Evidently AI
- Alert configuration and response
- Performance degradation analysis

**Time Estimate**: 6-9 hours total

---

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

## Exercise 4: Alert Configuration and Response (60 minutes)

**Objective**: Implement alerting system for monitoring violations.

### Background

Build an alerting system that monitors drift and performance metrics and sends notifications when thresholds are violated.

### Tasks

1. **Define alert rules and thresholds**
2. **Implement alert evaluation logic**
3. **Create notification system**
4. **Build alert history tracking**
5. **Implement alert aggregation**

### Starter Code

```python
# src/monitoring/alerting.py
"""Alerting system for model monitoring."""

import pandas as pd
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import json
from enum import Enum

class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class Alert:
    """Alert data structure."""
    timestamp: datetime
    metric_name: str
    current_value: float
    threshold: float
    severity: AlertSeverity
    message: str
    metadata: Dict = None

class AlertRule:
    """Defines an alert rule."""

    def __init__(
        self,
        name: str,
        metric_name: str,
        threshold: float,
        comparison: str,  # 'greater', 'less', 'equal'
        severity: AlertSeverity,
        message_template: str
    ):
        """
        Initialize alert rule.

        Args:
            name: Rule name
            metric_name: Name of metric to monitor
            threshold: Threshold value
            comparison: Comparison operator
            severity: Alert severity
            message_template: Message template (can include {value}, {threshold})
        """
        # TODO: Store rule parameters
        # TODO: Validate inputs
        pass

    def evaluate(self, metric_value: float) -> Optional[Alert]:
        """
        Evaluate rule against metric value.

        Args:
            metric_value: Current metric value

        Returns:
            Alert if threshold violated, None otherwise
        """
        # TODO: Compare metric_value with threshold
        # TODO: If violated, create Alert object
        # TODO: Format message using template
        # TODO: Return Alert or None
        pass

class AlertManager:
    """Manages alert rules and notifications."""

    def __init__(self):
        """Initialize alert manager."""
        self.rules: List[AlertRule] = []
        self.alert_history: List[Alert] = []
        self.notification_handlers: List[Callable] = []

    def add_rule(self, rule: AlertRule):
        """Add alert rule."""
        # TODO: Add rule to rules list
        pass

    def add_notification_handler(self, handler: Callable):
        """
        Add notification handler function.

        Args:
            handler: Function that takes Alert and sends notification
        """
        # TODO: Add handler to list
        pass

    def evaluate_metrics(self, metrics: Dict[str, float]) -> List[Alert]:
        """
        Evaluate all rules against current metrics.

        Args:
            metrics: Dictionary of metric names to values

        Returns:
            List of triggered alerts
        """
        # TODO: For each rule:
        #   - Get metric value from dict
        #   - Evaluate rule
        #   - Collect triggered alerts
        # TODO: Return all alerts
        pass

    def process_alerts(self, alerts: List[Alert]):
        """
        Process and send alerts.

        Args:
            alerts: List of alerts to process
        """
        # TODO: For each alert:
        #   - Add to history
        #   - Send to all notification handlers
        # TODO: Log processing
        pass

    def get_alert_history(
        self,
        start_time: datetime = None,
        end_time: datetime = None,
        severity: AlertSeverity = None
    ) -> List[Alert]:
        """
        Get alert history with optional filters.

        Args:
            start_time: Filter alerts after this time
            end_time: Filter alerts before this time
            severity: Filter by severity

        Returns:
            Filtered list of alerts
        """
        # TODO: Filter alert_history based on parameters
        # TODO: Return filtered alerts
        pass

    def aggregate_alerts(
        self,
        time_window: str = '1H'  # e.g., '1H', '1D'
    ) -> pd.DataFrame:
        """
        Aggregate alerts by time window.

        Args:
            time_window: Pandas time window string

        Returns:
            DataFrame with aggregated alert counts
        """
        # TODO: Convert alerts to DataFrame
        # TODO: Group by time window and severity
        # TODO: Count alerts
        # TODO: Return aggregated DataFrame
        pass

# Notification Handlers

def slack_notification_handler(alert: Alert, webhook_url: str):
    """
    Send alert to Slack.

    Args:
        alert: Alert to send
        webhook_url: Slack webhook URL
    """
    # TODO: Format Slack message
    # TODO: Send POST request to webhook
    # TODO: Handle errors
    pass

def email_notification_handler(alert: Alert, recipients: List[str]):
    """
    Send alert via email.

    Args:
        alert: Alert to send
        recipients: List of email addresses
    """
    # TODO: Format email message
    # TODO: Send email using SMTP
    # TODO: Handle errors
    pass

def pagerduty_notification_handler(alert: Alert, api_key: str):
    """
    Send critical alert to PagerDuty.

    Args:
        alert: Alert to send
        api_key: PagerDuty API key
    """
    # TODO: Only send if severity is CRITICAL
    # TODO: Create PagerDuty event
    # TODO: Send via API
    pass
```

### Configuration Example

```yaml
# config/alert_rules.yaml
alert_rules:
  - name: "High Data Drift"
    metric_name: "psi_score"
    threshold: 0.2
    comparison: "greater"
    severity: "warning"
    message: "PSI score {value:.3f} exceeds threshold {threshold}"

  - name: "Critical Data Drift"
    metric_name: "psi_score"
    threshold: 0.5
    comparison: "greater"
    severity: "critical"
    message: "CRITICAL: PSI score {value:.3f} indicates severe drift"

  - name: "Accuracy Degradation"
    metric_name: "accuracy"
    threshold: 0.85
    comparison: "less"
    severity: "critical"
    message: "Model accuracy {value:.3f} below acceptable threshold"

  - name: "High Prediction Latency"
    metric_name: "p95_latency_ms"
    threshold: 200
    comparison: "greater"
    severity: "warning"
    message: "P95 latency {value:.0f}ms exceeds SLA"

notification_channels:
  - type: "slack"
    webhook_url: "${SLACK_WEBHOOK_URL}"
    severities: ["warning", "critical"]

  - type: "email"
    recipients: ["ml-team@example.com"]
    severities: ["critical"]

  - type: "pagerduty"
    api_key: "${PAGERDUTY_API_KEY}"
    severities: ["critical"]
```

### Validation Tests

```python
# tests/test_alerting.py
import pytest
from datetime import datetime
from src.monitoring.alerting import (
    AlertRule, AlertManager, Alert, AlertSeverity
)

def test_alert_rule_triggers_on_violation():
    """Test that alert rule triggers when threshold violated."""
    rule = AlertRule(
        name="Test Rule",
        metric_name="accuracy",
        threshold=0.85,
        comparison="less",
        severity=AlertSeverity.WARNING,
        message_template="Accuracy {value} below {threshold}"
    )

    alert = rule.evaluate(0.80)
    # TODO: Assert alert is not None
    # TODO: Assert alert severity is WARNING
    pass

def test_alert_rule_does_not_trigger_when_ok():
    """Test that alert rule doesn't trigger when within threshold."""
    # TODO: Implement test
    pass

def test_alert_manager_evaluates_multiple_rules():
    """Test alert manager evaluates all rules."""
    # TODO: Create manager with multiple rules
    # TODO: Evaluate metrics
    # TODO: Assert correct alerts triggered
    pass

def test_alert_history_filtering():
    """Test alert history can be filtered."""
    # TODO: Add alerts to history
    # TODO: Filter by time range
    # TODO: Filter by severity
    # TODO: Assert correct alerts returned
    pass

def test_alert_aggregation():
    """Test alert aggregation by time window."""
    # TODO: Create alerts at different times
    # TODO: Aggregate by hour
    # TODO: Assert counts are correct
    pass
```

### Success Criteria

- [ ] Alert rules evaluate correctly
- [ ] Notifications are sent when thresholds violated
- [ ] Alert history is tracked
- [ ] Alerts can be filtered and queried
- [ ] Aggregation provides useful summaries
- [ ] Multiple notification channels supported

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Comparison Logic**:
```python
comparisons = {
    'greater': lambda v, t: v > t,
    'less': lambda v, t: v < t,
    'equal': lambda v, t: abs(v - t) < 1e-6
}
```

2. **Slack Webhook**: Use `requests.post(webhook_url, json={"text": message})`
3. **Email**: Use `smtplib` library for sending emails
4. **Alert Aggregation**: Convert to DataFrame and use `pd.Grouper` with `freq` parameter
5. **Configuration**: Use `pyyaml` to load alert rules from YAML config

</details>

---

## Exercise 5: Complete Monitoring Pipeline (120 minutes)

**Objective**: Build an end-to-end monitoring pipeline integrating all components.

### Background

Create a production-ready monitoring pipeline that continuously monitors model performance, data drift, and data quality, with automated alerting.

### Tasks

1. **Design monitoring architecture**
2. **Implement data collection pipeline**
3. **Integrate drift detection and alerting**
4. **Create monitoring dashboard**
5. **Set up automated monitoring jobs**

### Starter Code

```python
# src/monitoring/pipeline.py
"""End-to-end monitoring pipeline."""

import pandas as pd
from typing import Dict, List, Optional
from pathlib import Path
import logging
from datetime import datetime

from src.monitoring.drift_detector import KSDriftDetector
from src.monitoring.psi_calculator import PSICalculator
from src.monitoring.evidently_monitor import EvidentlyMonitor
from src.monitoring.alerting import AlertManager, AlertRule, AlertSeverity

class MonitoringPipeline:
    """Complete monitoring pipeline orchestrator."""

    def __init__(
        self,
        reference_data: pd.DataFrame,
        config: Dict,
        output_dir: str = "monitoring_output"
    ):
        """
        Initialize monitoring pipeline.

        Args:
            reference_data: Reference (training) data
            config: Configuration dictionary
            output_dir: Output directory for reports
        """
        self.reference_data = reference_data
        self.config = config
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # TODO: Initialize components
        self.ks_detector = None
        self.psi_calculator = None
        self.evidently_monitor = None
        self.alert_manager = None

        # TODO: Set up logging
        self.logger = logging.getLogger(__name__)

        # TODO: Initialize components based on config
        self._initialize_components()

    def _initialize_components(self):
        """Initialize all monitoring components."""
        # TODO: Initialize KS detector
        # TODO: Initialize PSI calculator
        # TODO: Initialize Evidently monitor
        # TODO: Initialize alert manager and rules
        # TODO: Fit detectors on reference data
        pass

    def run_monitoring(
        self,
        current_data: pd.DataFrame,
        timestamp: Optional[datetime] = None
    ) -> Dict:
        """
        Run complete monitoring pipeline on current data.

        Args:
            current_data: Current production data
            timestamp: Timestamp for this monitoring run

        Returns:
            Dictionary containing all monitoring results
        """
        if timestamp is None:
            timestamp = datetime.now()

        self.logger.info(f"Running monitoring pipeline at {timestamp}")

        results = {
            'timestamp': timestamp,
            'data_stats': {},
            'drift_metrics': {},
            'quality_metrics': {},
            'performance_metrics': {},
            'alerts': []
        }

        # TODO: 1. Collect data statistics
        results['data_stats'] = self._collect_data_stats(current_data)

        # TODO: 2. Run drift detection
        results['drift_metrics'] = self._run_drift_detection(current_data)

        # TODO: 3. Check data quality
        results['quality_metrics'] = self._check_data_quality(current_data)

        # TODO: 4. Evaluate model performance (if actuals available)
        if self.config.get('target_column') in current_data.columns:
            results['performance_metrics'] = self._evaluate_performance(current_data)

        # TODO: 5. Generate reports
        self._generate_reports(current_data, timestamp)

        # TODO: 6. Evaluate alerts
        results['alerts'] = self._evaluate_alerts(results)

        # TODO: 7. Save results
        self._save_results(results)

        return results

    def _collect_data_stats(self, data: pd.DataFrame) -> Dict:
        """Collect basic data statistics."""
        # TODO: Return dict with:
        #   - Number of samples
        #   - Number of features
        #   - Missing value counts
        #   - Basic statistics (mean, std)
        pass

    def _run_drift_detection(self, data: pd.DataFrame) -> Dict:
        """Run drift detection using multiple methods."""
        drift_metrics = {}

        # TODO: Run KS test
        # TODO: Calculate PSI
        # TODO: Run Evidently drift detection
        # TODO: Combine results

        return drift_metrics

    def _check_data_quality(self, data: pd.DataFrame) -> Dict:
        """Check data quality metrics."""
        # TODO: Check for:
        #   - Missing values
        #   - Duplicates
        #   - Outliers
        #   - Schema validation
        pass

    def _evaluate_performance(self, data: pd.DataFrame) -> Dict:
        """Evaluate model performance."""
        # TODO: Calculate:
        #   - Accuracy, Precision, Recall, F1
        #   - Confusion matrix
        #   - ROC AUC
        pass

    def _generate_reports(self, data: pd.DataFrame, timestamp: datetime):
        """Generate monitoring reports."""
        # TODO: Generate Evidently reports
        # TODO: Create visualizations
        # TODO: Save to output directory
        pass

    def _evaluate_alerts(self, results: Dict) -> List:
        """Evaluate alert rules against results."""
        # TODO: Extract metrics from results
        # TODO: Evaluate alert rules
        # TODO: Process and send alerts
        # TODO: Return list of triggered alerts
        pass

    def _save_results(self, results: Dict):
        """Save monitoring results to storage."""
        # TODO: Save to JSON
        # TODO: Append to time series database
        # TODO: Update dashboard data
        pass

    def run_continuous_monitoring(
        self,
        data_source: Callable,
        interval_seconds: int = 3600
    ):
        """
        Run monitoring continuously.

        Args:
            data_source: Callable that returns current data
            interval_seconds: Monitoring interval in seconds
        """
        # TODO: Set up continuous monitoring loop
        # TODO: Fetch data from source
        # TODO: Run monitoring pipeline
        # TODO: Sleep for interval
        # TODO: Handle errors and retries
        pass
```

### Configuration File

```python
# config/monitoring_config.py
"""Monitoring pipeline configuration."""

MONITORING_CONFIG = {
    'target_column': 'target',
    'prediction_column': 'prediction',
    'numerical_features': ['feature_1', 'feature_2', 'feature_3'],
    'categorical_features': ['feature_4', 'feature_5'],

    'drift_detection': {
        'ks_threshold': 0.05,
        'psi_bins': 10,
        'psi_threshold': 0.2,
        'evidently_drift_share': 0.3
    },

    'data_quality': {
        'max_missing_ratio': 0.1,
        'detect_outliers': True,
        'outlier_method': 'iqr'
    },

    'performance': {
        'min_accuracy': 0.85,
        'min_f1': 0.80,
        'min_samples': 100
    },

    'alerting': {
        'rules': [
            {
                'name': 'High PSI',
                'metric': 'psi_max',
                'threshold': 0.2,
                'comparison': 'greater',
                'severity': 'warning'
            },
            {
                'name': 'Low Accuracy',
                'metric': 'accuracy',
                'threshold': 0.85,
                'comparison': 'less',
                'severity': 'critical'
            }
        ],
        'notification_channels': ['slack', 'email']
    },

    'output': {
        'save_reports': True,
        'save_metrics': True,
        'dashboard_update': True
    }
}
```

### Deployment Script

```python
# scripts/deploy_monitoring.py
"""Deploy monitoring pipeline."""

import pandas as pd
from src.monitoring.pipeline import MonitoringPipeline
from config.monitoring_config import MONITORING_CONFIG

def fetch_current_data() -> pd.DataFrame:
    """Fetch current production data."""
    # TODO: Implement data fetching from:
    #   - Database
    #   - Data warehouse
    #   - API
    #   - File storage
    pass

def main():
    # Load reference data
    reference_data = pd.read_csv('data/reference_data.csv')

    # Initialize pipeline
    pipeline = MonitoringPipeline(
        reference_data=reference_data,
        config=MONITORING_CONFIG,
        output_dir='monitoring_output'
    )

    # Run one-time monitoring
    current_data = fetch_current_data()
    results = pipeline.run_monitoring(current_data)

    print(f"Monitoring complete. Triggered {len(results['alerts'])} alerts.")

    # Or run continuous monitoring
    # pipeline.run_continuous_monitoring(
    #     data_source=fetch_current_data,
    #     interval_seconds=3600  # Every hour
    # )

if __name__ == '__main__':
    main()
```

### Success Criteria

- [ ] Pipeline integrates all monitoring components
- [ ] Runs successfully on production data
- [ ] Generates comprehensive reports
- [ ] Alerts are triggered appropriately
- [ ] Results are saved and accessible
- [ ] Can run continuously or on-demand
- [ ] Handles errors gracefully
- [ ] Performance is acceptable (< 5 min per run)

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Data Source**: Use `sqlalchemy` for database connections or `boto3` for S3
2. **Continuous Monitoring**: Use `schedule` library or run as Kubernetes CronJob
3. **Error Handling**: Wrap each monitoring component in try-except, continue on non-critical errors
4. **Performance**: Run drift detection in parallel for different features
5. **Storage**: Save metrics to TimescaleDB or Prometheus for time series analysis
6. **Dashboard**: Use Grafana with metrics from Prometheus or custom dashboard with Plotly Dash

</details>

---

## Bonus Challenges

### Challenge 1: Model Performance Decay Detection

Implement CUSUM (Cumulative Sum Control Chart) to detect gradual model performance decay over time.

### Challenge 2: Multivariate Drift Detection

Implement multivariate drift detection that considers feature interactions, not just individual features.

### Challenge 3: Adaptive Thresholds

Implement adaptive alerting thresholds that adjust based on historical patterns and seasonality.

---

## Additional Resources

- **Evidently AI**: [Documentation](https://docs.evidentlyai.com/)
- **Statistical Tests**: [SciPy Stats](https://docs.scipy.org/doc/scipy/reference/stats.html)
- **PSI**: [Population Stability Index Explained](https://www.lexjansen.com/wuss/2017/47_Final_Paper_PDF.pdf)
- **Monitoring Best Practices**: [Google SRE Book](https://sre.google/sre-book/monitoring-distributed-systems/)

---

## Submission Guidelines

For each exercise, submit:
1. **Code**: All implementation files
2. **Tests**: Passing test suite
3. **Reports**: Example monitoring reports
4. **Configuration**: Alert rules and thresholds
5. **Documentation**: How to deploy and operate

**Estimated Total Time**: 6-9 hours
**Difficulty**: Intermediate to Advanced

Good luck!
