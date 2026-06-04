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
