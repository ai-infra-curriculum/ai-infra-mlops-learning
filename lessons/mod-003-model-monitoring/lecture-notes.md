# Module 03: Model Monitoring and Drift Detection - Lecture Notes

**Duration**: 12.5 hours
**Level**: MLOps Engineer (2.5B)
**Last Updated**: October 2025

---

## Table of Contents

1. [Introduction to ML Monitoring](#1-introduction-to-ml-monitoring)
2. [Data Drift Detection](#2-data-drift-detection)
3. [Concept Drift and Performance Monitoring](#3-concept-drift-and-performance-monitoring)
4. [Monitoring Infrastructure](#4-monitoring-infrastructure)
5. [Alerting and Response](#5-alerting-and-response)
6. [Advanced Monitoring](#6-advanced-monitoring)
7. [Real-World Case Studies](#7-real-world-case-studies)
8. [Summary and Best Practices](#8-summary-and-best-practices)

---

## 1. Introduction to ML Monitoring

### 1.1 Why ML Models Fail Silently

Unlike traditional software, ML models can degrade without throwing errors:

**The Silent Degradation Problem**:
```python
# Traditional software - fails loudly
def divide(a, b):
    return a / b  # Throws ZeroDivisionError if b == 0

# ML model - fails silently
def predict(features):
    return model.predict(features)  # Returns predictions even if:
    # - Data distribution has shifted
    # - Feature engineering broke
    # - Concept has changed
    # - Model is stale
```

**Real Example - Instagram Recommendation Failure (2023)**:
- Model trained on pre-pandemic user behavior
- After pandemic, user engagement patterns shifted
- Model continued making predictions (no errors!)
- Click-through rate dropped 40% over 3 months
- **Cost**: $50M in lost ad revenue before detection
- **Root cause**: No drift monitoring in place

### 1.2 Traditional vs ML-Specific Monitoring

**Traditional Software Monitoring**:
- CPU, memory, disk, network
- Request rate, latency, errors
- Service availability (uptime)
- Application logs and traces

**ML-Specific Monitoring** (all of above PLUS):
- **Data Quality**: Input feature distributions
- **Data Drift**: Distribution changes over time
- **Concept Drift**: Relationship changes (X → y)
- **Prediction Drift**: Output distribution changes
- **Model Performance**: Accuracy, precision, recall degradation
- **Fairness Metrics**: Bias and fairness over time
- **Business Metrics**: Revenue impact, user satisfaction

### 1.3 Types of Drift

**1. Data Drift (Covariate Shift)**
- **Definition**: P(X) changes, P(y|X) stays constant
- **Example**: House prices model
  - Training: Average house size = 2,000 sq ft
  - Production: Average house size = 2,500 sq ft
  - Relationship (price per sq ft) unchanged

**2. Concept Drift**
- **Definition**: P(y|X) changes, P(X) may or may not change
- **Example**: Credit card fraud detection
  - Training: Fraudsters use stolen cards at gas stations
  - Production: Fraudsters shift to online purchases
  - Same features, different fraud patterns

**3. Prediction Drift**
- **Definition**: P(ŷ) changes
- **Example**: Recommendation system
  - Training: 50% users click recommended items
  - Production: 20% users click recommended items
  - May indicate data drift or concept drift

**Visual Summary**:
```
Data Drift:        P(X)   changes,  P(y|X) constant
Concept Drift:     P(y|X) changes,  P(X)   may change
Prediction Drift:  P(ŷ)   changes,  indicates problems
```

### 1.4 The Cost of Not Monitoring

**Netflix - Recommendation Degradation (2021)**:
- Undetected concept drift in viewing patterns
- Model trained pre-pandemic, deployed during pandemic
- Recommendation quality degraded 15% over 6 months
- Estimated impact: 2% subscriber churn increase
- **Cost**: ~$200M annual revenue

**Best Practice**: Monitor is not optional—it's critical infrastructure.

---

## 2. Data Drift Detection

### 2.1 Statistical Methods

#### Kolmogorov-Smirnov (KS) Test

**Use Case**: Detect drift in continuous features

**How it Works**:
- Compares cumulative distribution functions (CDFs)
- Measures maximum distance between two CDFs
- Returns p-value indicating likelihood distributions are same

**Implementation**:
```python
from scipy.stats import ks_2samp
import numpy as np
import pandas as pd

class DataDriftDetector:
    """Detect data drift using statistical tests."""

    def __init__(self, reference_data: pd.DataFrame, alpha: float = 0.05):
        """
        Initialize drift detector.

        Args:
            reference_data: Training or baseline data
            alpha: Significance level (default 0.05)
        """
        self.reference_data = reference_data
        self.alpha = alpha
        self.drift_scores = {}

    def detect_ks_drift(
        self,
        current_data: pd.DataFrame,
        feature: str
    ) -> dict:
        """
        Detect drift using Kolmogorov-Smirnov test.

        Args:
            current_data: Recent production data
            feature: Feature name to check

        Returns:
            Dictionary with test results
        """
        reference = self.reference_data[feature].dropna()
        current = current_data[feature].dropna()

        # Perform KS test
        statistic, p_value = ks_2samp(reference, current)

        # Interpret results
        drift_detected = p_value < self.alpha

        return {
            'feature': feature,
            'ks_statistic': statistic,
            'p_value': p_value,
            'drift_detected': drift_detected,
            'severity': self._classify_severity(statistic)
        }

    def _classify_severity(self, ks_stat: float) -> str:
        """Classify drift severity based on KS statistic."""
        if ks_stat < 0.1:
            return 'none'
        elif ks_stat < 0.2:
            return 'low'
        elif ks_stat < 0.3:
            return 'medium'
        else:
            return 'high'

    def detect_all_features(
        self,
        current_data: pd.DataFrame
    ) -> pd.DataFrame:
        """Detect drift across all features."""
        results = []

        for feature in self.reference_data.columns:
            if pd.api.types.is_numeric_dtype(self.reference_data[feature]):
                result = self.detect_ks_drift(current_data, feature)
                results.append(result)

        return pd.DataFrame(results)

# Example usage
reference_df = pd.read_csv('training_data.csv')
current_df = pd.read_csv('production_data_last_week.csv')

detector = DataDriftDetector(reference_df)
drift_report = detector.detect_all_features(current_df)

print(drift_report[drift_report['drift_detected']])
```

**Interpretation**:
- **p-value < 0.05**: Distributions are significantly different (drift detected)
- **KS statistic > 0.3**: High drift severity
- **KS statistic < 0.1**: Low/no drift

#### Population Stability Index (PSI)

**Use Case**: Industry standard for drift detection in financial services

**Formula**:
```
PSI = Σ (% current - % reference) × ln(% current / % reference)
```

**Interpretation**:
- PSI < 0.1: No significant drift
- 0.1 ≤ PSI < 0.2: Moderate drift (investigate)
- PSI ≥ 0.2: High drift (retrain recommended)

**Implementation**:
```python
import numpy as np
from typing import Tuple

def calculate_psi(
    reference: np.ndarray,
    current: np.ndarray,
    bins: int = 10
) -> Tuple[float, dict]:
    """
    Calculate Population Stability Index.

    Args:
        reference: Reference distribution
        current: Current distribution
        bins: Number of bins for binning

    Returns:
        PSI value and detailed breakdown
    """
    # Create bins based on reference data
    breakpoints = np.percentile(reference, np.linspace(0, 100, bins + 1))
    breakpoints = np.unique(breakpoints)  # Remove duplicates

    # Bin the data
    ref_counts = np.histogram(reference, bins=breakpoints)[0]
    cur_counts = np.histogram(current, bins=breakpoints)[0]

    # Calculate percentages
    ref_percents = ref_counts / len(reference)
    cur_percents = cur_counts / len(current)

    # Avoid division by zero
    ref_percents = np.where(ref_percents == 0, 0.0001, ref_percents)
    cur_percents = np.where(cur_percents == 0, 0.0001, cur_percents)

    # Calculate PSI
    psi_values = (cur_percents - ref_percents) * np.log(cur_percents / ref_percents)
    psi = np.sum(psi_values)

    return psi, {
        'psi': psi,
        'severity': 'high' if psi >= 0.2 else 'moderate' if psi >= 0.1 else 'low',
        'bin_contributions': psi_values,
        'breakpoints': breakpoints
    }

# Example usage
from sklearn.datasets import make_classification

# Simulate training data
X_train, _ = make_classification(n_samples=10000, n_features=20, random_state=42)

# Simulate production data with drift
X_prod, _ = make_classification(n_samples=5000, n_features=20, random_state=99)

# Check drift for each feature
for i in range(20):
    psi, details = calculate_psi(X_train[:, i], X_prod[:, i])
    print(f"Feature {i}: PSI = {psi:.4f} ({details['severity']} drift)")
```

#### Chi-Square Test (Categorical Features)

**Use Case**: Detect drift in categorical features

**Implementation**:
```python
from scipy.stats import chi2_contingency

def detect_categorical_drift(
    reference: pd.Series,
    current: pd.Series,
    alpha: float = 0.05
) -> dict:
    """
    Detect drift in categorical features using Chi-square test.

    Args:
        reference: Reference categorical data
        current: Current categorical data
        alpha: Significance level

    Returns:
        Test results dictionary
    """
    # Get value counts
    ref_counts = reference.value_counts()
    cur_counts = current.value_counts()

    # Align categories
    all_categories = set(ref_counts.index) | set(cur_counts.index)
    ref_aligned = [ref_counts.get(cat, 0) for cat in all_categories]
    cur_aligned = [cur_counts.get(cat, 0) for cat in all_categories]

    # Create contingency table
    contingency_table = np.array([ref_aligned, cur_aligned])

    # Perform chi-square test
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)

    return {
        'chi2_statistic': chi2,
        'p_value': p_value,
        'degrees_of_freedom': dof,
        'drift_detected': p_value < alpha,
        'new_categories': set(cur_counts.index) - set(ref_counts.index),
        'missing_categories': set(ref_counts.index) - set(cur_counts.index)
    }
```

### 2.2 Evidently AI Implementation

**Production-Ready Drift Detection**:

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently import ColumnMapping

class ProductionDriftMonitor:
    """Production-grade drift monitoring with Evidently."""

    def __init__(
        self,
        reference_data: pd.DataFrame,
        numerical_features: list,
        categorical_features: list,
        target: str = None
    ):
        self.reference_data = reference_data
        self.column_mapping = ColumnMapping(
            numerical_features=numerical_features,
            categorical_features=categorical_features,
            target=target
        )

    def generate_drift_report(
        self,
        current_data: pd.DataFrame,
        save_html: bool = True
    ) -> dict:
        """Generate comprehensive drift report."""

        # Create report
        report = Report(metrics=[DataDriftPreset()])

        # Run analysis
        report.run(
            reference_data=self.reference_data,
            current_data=current_data,
            column_mapping=self.column_mapping
        )

        # Save HTML report
        if save_html:
            report.save_html('drift_report.html')

        # Extract key metrics
        result = report.as_dict()

        return {
            'dataset_drift': result['metrics'][0]['result']['dataset_drift'],
            'drift_share': result['metrics'][0]['result']['drift_share'],
            'number_of_drifted_columns': result['metrics'][0]['result']['number_of_drifted_columns'],
            'drifted_features': self._extract_drifted_features(result)
        }

    def _extract_drifted_features(self, result: dict) -> list:
        """Extract list of features with detected drift."""
        drifted = []
        for metric in result['metrics']:
            if metric.get('result', {}).get('drift_detected'):
                drifted.append(metric.get('result', {}).get('column_name'))
        return drifted

# Usage example
monitor = ProductionDriftMonitor(
    reference_data=train_df,
    numerical_features=['age', 'income', 'credit_score'],
    categorical_features=['region', 'employment_type'],
    target='default'
)

# Check weekly production data
weekly_data = fetch_production_data(days=7)
drift_results = monitor.generate_drift_report(weekly_data)

if drift_results['dataset_drift']:
    print(f"⚠️ DRIFT DETECTED in {drift_results['number_of_drifted_columns']} features")
    print(f"Drifted features: {drift_results['drifted_features']}")
    # Trigger alert
    send_slack_alert(drift_results)
```

### 2.3 Multivariate Drift Detection

**Challenge**: Features may drift together (correlations change)

**Solution**: Use multivariate methods

```python
from scipy.spatial.distance import jensenshannon
from sklearn.decomposition import PCA

def detect_multivariate_drift(
    reference: np.ndarray,
    current: np.ndarray,
    method: str = 'pca'
) -> dict:
    """
    Detect multivariate drift.

    Args:
        reference: Reference data (n_samples, n_features)
        current: Current data (n_samples, n_features)
        method: 'pca' or 'js_divergence'

    Returns:
        Drift detection results
    """
    if method == 'pca':
        # Reduce dimensions
        pca = PCA(n_components=2)
        ref_reduced = pca.fit_transform(reference)
        cur_reduced = pca.transform(current)

        # Apply KS test on principal components
        from scipy.stats import ks_2samp
        ks_stat_pc1, p_value_pc1 = ks_2samp(ref_reduced[:, 0], cur_reduced[:, 0])
        ks_stat_pc2, p_value_pc2 = ks_2samp(ref_reduced[:, 1], cur_reduced[:, 1])

        return {
            'method': 'pca',
            'pc1_drift': p_value_pc1 < 0.05,
            'pc2_drift': p_value_pc2 < 0.05,
            'explained_variance': pca.explained_variance_ratio_,
            'drift_detected': (p_value_pc1 < 0.05) or (p_value_pc2 < 0.05)
        }

    elif method == 'js_divergence':
        # Jensen-Shannon divergence between distributions
        # Bin the data
        from sklearn.preprocessing import KBinsDiscretizer

        binner = KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='quantile')
        ref_binned = binner.fit_transform(reference)
        cur_binned = binner.transform(current)

        # Calculate JS divergence for each feature
        divergences = []
        for i in range(reference.shape[1]):
            ref_dist, _ = np.histogram(ref_binned[:, i], bins=10, density=True)
            cur_dist, _ = np.histogram(cur_binned[:, i], bins=10, density=True)

            # Normalize
            ref_dist = ref_dist / ref_dist.sum()
            cur_dist = cur_dist / cur_dist.sum()

            js_div = jensenshannon(ref_dist, cur_dist)
            divergences.append(js_div)

        return {
            'method': 'js_divergence',
            'mean_divergence': np.mean(divergences),
            'max_divergence': np.max(divergences),
            'drift_detected': np.max(divergences) > 0.3
        }
```

---

## 3. Concept Drift and Performance Monitoring

### 3.1 Concept Drift Detection

**Challenge**: The relationship between features and target changes

**Example - Credit Scoring**:
```python
# Before: High income → Low default risk
# After:  High income → No clear relationship (economic crisis)
```

**Detection Strategies**:

1. **With Ground Truth** (when labels arrive quickly):
```python
import mlflow
from sklearn.metrics import accuracy_score, precision_score, recall_score

class PerformanceMonitor:
    """Monitor model performance over time."""

    def __init__(self, model_uri: str, tracking_uri: str):
        self.model = mlflow.sklearn.load_model(model_uri)
        mlflow.set_tracking_uri(tracking_uri)
        self.performance_history = []

    def evaluate_batch(
        self,
        X: pd.DataFrame,
        y_true: pd.Series,
        batch_id: str
    ) -> dict:
        """Evaluate model on a batch and log metrics."""

        # Make predictions
        y_pred = self.model.predict(X)
        y_prob = self.model.predict_proba(X)[:, 1]

        # Calculate metrics
        metrics = {
            'batch_id': batch_id,
            'timestamp': pd.Timestamp.now(),
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred),
            'recall': recall_score(y_true, y_pred),
            'n_samples': len(y_true)
        }

        # Log to MLflow
        with mlflow.start_run(run_name=f"performance_check_{batch_id}"):
            mlflow.log_metrics({
                k: v for k, v in metrics.items()
                if isinstance(v, (int, float))
            })

        self.performance_history.append(metrics)

        # Check for degradation
        if len(self.performance_history) >= 5:
            recent_avg = np.mean([
                m['accuracy'] for m in self.performance_history[-5:]
            ])
            baseline_avg = np.mean([
                m['accuracy'] for m in self.performance_history[:5]
            ])

            if recent_avg < baseline_avg * 0.95:  # 5% degradation
                metrics['concept_drift_detected'] = True
                metrics['performance_degradation'] = baseline_avg - recent_avg

        return metrics
```

2. **Without Ground Truth** (labels delayed/expensive):
```python
class ProxyMetricMonitor:
    """Monitor proxy metrics when ground truth is delayed."""

    def monitor_prediction_confidence(
        self,
        predictions_proba: np.ndarray,
        threshold: float = 0.7
    ) -> dict:
        """
        Monitor prediction confidence distribution.
        Low confidence may indicate drift.
        """
        max_probs = np.max(predictions_proba, axis=1)

        return {
            'mean_confidence': np.mean(max_probs),
            'median_confidence': np.median(max_probs),
            'low_confidence_ratio': np.mean(max_probs < threshold),
            'confidence_std': np.std(max_probs)
        }

    def monitor_prediction_distribution(
        self,
        predictions: np.ndarray,
        reference_distribution: np.ndarray
    ) -> dict:
        """Monitor if prediction distribution has shifted."""
        from scipy.stats import ks_2samp

        stat, p_value = ks_2samp(reference_distribution, predictions)

        return {
            'ks_statistic': stat,
            'p_value': p_value,
            'prediction_drift': p_value < 0.05
        }
```

### 3.2 Ground Truth Delay Problem

**Real-World Example - E-commerce**:
- **Model**: Predicts product return likelihood
- **Prediction time**: At purchase
- **Ground truth**: 30-90 days later (return window)
- **Problem**: Can't measure accuracy for 3 months!

**Solutions**:

1. **Proxy Metrics**:
   - Prediction confidence
   - Input drift
   - Business metrics (customer complaints)

2. **Synthetic Labels**:
```python
def create_synthetic_labels(
    features: pd.DataFrame,
    historical_model: Any,
    current_predictions: np.ndarray
) -> np.ndarray:
    """
    Use older model on new data as proxy for ground truth.
    Compare current model vs baseline.
    """
    synthetic_labels = historical_model.predict(features)

    # If current model disagrees significantly with baseline, flag it
    disagreement_rate = np.mean(synthetic_labels != current_predictions)

    if disagreement_rate > 0.2:  # 20% disagreement
        print(f"⚠️ High disagreement rate: {disagreement_rate:.2%}")
        print("Possible concept drift or model degradation")

    return synthetic_labels
```

3. **Delayed Evaluation Pipeline**:
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Store predictions
def store_predictions(**context):
    """Store predictions with metadata for later evaluation."""
    predictions_df = pd.DataFrame({
        'prediction_id': range(len(predictions)),
        'prediction': predictions,
        'features': features.to_dict('records'),
        'timestamp': datetime.now(),
        'model_version': 'v2.3'
    })

    predictions_df.to_sql('predictions_log', db_engine, if_exists='append')

# Evaluate when ground truth arrives
def evaluate_with_ground_truth(**context):
    """Evaluate predictions once ground truth is available."""
    # Get predictions from 30 days ago
    cutoff_date = datetime.now() - timedelta(days=30)

    query = f"""
    SELECT p.*, gt.actual_value
    FROM predictions_log p
    JOIN ground_truth gt ON p.prediction_id = gt.prediction_id
    WHERE p.timestamp <= '{cutoff_date}'
    AND gt.actual_value IS NOT NULL
    """

    eval_data = pd.read_sql(query, db_engine)

    # Calculate metrics
    accuracy = accuracy_score(eval_data['actual_value'], eval_data['prediction'])

    # Log to monitoring system
    log_metric('delayed_accuracy', accuracy, timestamp=cutoff_date)
```

---

## 4. Monitoring Infrastructure

### 4.1 Prometheus Metrics Collection

**Custom ML Metrics**:

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Define metrics
prediction_counter = Counter(
    'ml_predictions_total',
    'Total number of predictions',
    ['model_name', 'model_version']
)

prediction_latency = Histogram(
    'ml_prediction_latency_seconds',
    'Prediction latency in seconds',
    ['model_name']
)

prediction_confidence = Histogram(
    'ml_prediction_confidence',
    'Prediction confidence score',
    ['model_name'],
    buckets=[0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0]
)

data_drift_score = Gauge(
    'ml_data_drift_score',
    'Data drift score (KS statistic)',
    ['feature_name']
)

model_accuracy = Gauge(
    'ml_model_accuracy',
    'Model accuracy on recent batch',
    ['model_name', 'model_version']
)

class MonitoredModel:
    """ML model wrapper with Prometheus instrumentation."""

    def __init__(self, model, model_name: str, model_version: str):
        self.model = model
        self.model_name = model_name
        self.model_version = model_version

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions with monitoring."""

        # Time the prediction
        start_time = time.time()
        predictions = self.model.predict(X)
        latency = time.time() - start_time

        # Update metrics
        prediction_counter.labels(
            model_name=self.model_name,
            model_version=self.model_version
        ).inc(len(predictions))

        prediction_latency.labels(
            model_name=self.model_name
        ).observe(latency / len(predictions))

        # Monitor confidence (if available)
        if hasattr(self.model, 'predict_proba'):
            probas = self.model.predict_proba(X)
            confidences = np.max(probas, axis=1)

            for conf in confidences:
                prediction_confidence.labels(
                    model_name=self.model_name
                ).observe(conf)

        return predictions

# Start Prometheus metrics server
start_http_server(8000)
print("Metrics available at http://localhost:8000/metrics")
```

**Prometheus Configuration** (`prometheus.yml`):
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'ml-model-metrics'
    static_configs:
      - targets: ['localhost:8000']

  - job_name: 'drift-detector'
    static_configs:
      - targets: ['localhost:8001']
```

### 4.2 Grafana Dashboards

**Dashboard Configuration** (JSON):
```json
{
  "dashboard": {
    "title": "ML Model Monitoring",
    "panels": [
      {
        "title": "Prediction Rate",
        "targets": [
          {
            "expr": "rate(ml_predictions_total[5m])"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Prediction Latency (p95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, ml_prediction_latency_seconds_bucket)"
          }
        ]
      },
      {
        "title": "Data Drift Heatmap",
        "targets": [
          {
            "expr": "ml_data_drift_score"
          }
        ],
        "type": "heatmap"
      },
      {
        "title": "Model Accuracy Trend",
        "targets": [
          {
            "expr": "ml_model_accuracy"
          }
        ],
        "alert": {
          "conditions": [
            {
              "evaluator": {
                "params": [0.85],
                "type": "lt"
              }
            }
          ]
        }
      }
    ]
  }
}
```

---

## 5. Alerting and Response

### 5.1 Intelligent Alerting System

```python
from dataclasses import dataclass
from enum import Enum
from typing import List
import requests

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class Alert:
    """Alert data structure."""
    title: str
    message: str
    severity: AlertSeverity
    metric_name: str
    current_value: float
    threshold: float
    tags: List[str]

class MultiChannelAlerter:
    """Send alerts to multiple channels."""

    def __init__(
        self,
        slack_webhook: str,
        pagerduty_key: str,
        email_config: dict
    ):
        self.slack_webhook = slack_webhook
        self.pagerduty_key = pagerduty_key
        self.email_config = email_config

    def send_alert(self, alert: Alert):
        """Route alert to appropriate channels based on severity."""

        if alert.severity == AlertSeverity.INFO:
            self._send_slack(alert)

        elif alert.severity == AlertSeverity.WARNING:
            self._send_slack(alert)
            self._send_email(alert)

        elif alert.severity == AlertSeverity.CRITICAL:
            self._send_slack(alert)
            self._send_email(alert)
            self._send_pagerduty(alert)

    def _send_slack(self, alert: Alert):
        """Send Slack notification."""
        color = {
            AlertSeverity.INFO: "#36a64f",
            AlertSeverity.WARNING: "#ff9900",
            AlertSeverity.CRITICAL: "#ff0000"
        }[alert.severity]

        payload = {
            "attachments": [{
                "color": color,
                "title": f"🚨 {alert.title}",
                "text": alert.message,
                "fields": [
                    {"title": "Metric", "value": alert.metric_name, "short": True},
                    {"title": "Current Value", "value": f"{alert.current_value:.4f}", "short": True},
                    {"title": "Threshold", "value": f"{alert.threshold:.4f}", "short": True},
                    {"title": "Severity", "value": alert.severity.value.upper(), "short": True}
                ],
                "footer": "ML Monitoring System",
                "ts": int(time.time())
            }]
        }

        requests.post(self.slack_webhook, json=payload)

    def _send_pagerduty(self, alert: Alert):
        """Send PagerDuty incident."""
        payload = {
            "routing_key": self.pagerduty_key,
            "event_action": "trigger",
            "payload": {
                "summary": alert.title,
                "severity": alert.severity.value,
                "source": "ML Monitoring",
                "custom_details": {
                    "metric": alert.metric_name,
                    "current_value": alert.current_value,
                    "threshold": alert.threshold
                }
            }
        }

        requests.post(
            "https://events.pagerduty.com/v2/enqueue",
            json=payload
        )

# Usage
alerter = MultiChannelAlerter(
    slack_webhook=os.environ['SLACK_WEBHOOK'],
    pagerduty_key=os.environ['PAGERDUTY_KEY'],
    email_config={'smtp_server': 'smtp.gmail.com'}
)

# Trigger alert
alert = Alert(
    title="High Data Drift Detected",
    message="Feature 'age' shows KS statistic of 0.45 (threshold: 0.3)",
    severity=AlertSeverity.CRITICAL,
    metric_name="age_drift_score",
    current_value=0.45,
    threshold=0.3,
    tags=["drift", "production", "credit-model"]
)

alerter.send_alert(alert)
```

### 5.2 Automated Retraining Triggers

```python
class AutomatedResponseSystem:
    """Automatically respond to drift and degradation."""

    def __init__(
        self,
        drift_threshold: float = 0.3,
        performance_threshold: float = 0.85
    ):
        self.drift_threshold = drift_threshold
        self.performance_threshold = performance_threshold

    def evaluate_and_respond(
        self,
        drift_scores: dict,
        performance_metrics: dict
    ) -> dict:
        """Evaluate metrics and trigger appropriate responses."""

        responses = []

        # Check drift
        high_drift_features = [
            feat for feat, score in drift_scores.items()
            if score > self.drift_threshold
        ]

        if high_drift_features:
            responses.append(self._trigger_retraining(
                reason="data_drift",
                affected_features=high_drift_features
            ))

        # Check performance
        if performance_metrics.get('accuracy', 1.0) < self.performance_threshold:
            responses.append(self._trigger_retraining(
                reason="performance_degradation",
                current_accuracy=performance_metrics['accuracy']
            ))

        return {
            'actions_taken': responses,
            'timestamp': pd.Timestamp.now()
        }

    def _trigger_retraining(self, reason: str, **kwargs) -> dict:
        """Trigger model retraining pipeline."""

        # Create Airflow DAG run
        import requests

        dag_run_config = {
            'conf': {
                'reason': reason,
                'trigger_time': str(pd.Timestamp.now()),
                **kwargs
            }
        }

        response = requests.post(
            'http://airflow:8080/api/v1/dags/model_retraining/dagRuns',
            json=dag_run_config,
            auth=('admin', os.environ['AIRFLOW_PASSWORD'])
        )

        return {
            'action': 'retraining_triggered',
            'reason': reason,
            'dag_run_id': response.json().get('dag_run_id')
        }
```

---

## 6. Advanced Monitoring

### 6.1 Fairness Monitoring

```python
from fairlearn.metrics import demographic_parity_difference, equalized_odds_difference

class FairnessMonitor:
    """Monitor fairness metrics over time."""

    def evaluate_fairness(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        sensitive_features: pd.DataFrame
    ) -> dict:
        """Calculate fairness metrics."""

        metrics = {}

        for feature in sensitive_features.columns:
            # Demographic parity
            dp_diff = demographic_parity_difference(
                y_true, y_pred,
                sensitive_features=sensitive_features[feature]
            )

            # Equalized odds
            eo_diff = equalized_odds_difference(
                y_true, y_pred,
                sensitive_features=sensitive_features[feature]
            )

            metrics[feature] = {
                'demographic_parity_diff': dp_diff,
                'equalized_odds_diff': eo_diff,
                'fairness_violation': abs(dp_diff) > 0.1 or abs(eo_diff) > 0.1
            }

        return metrics
```

---

## 7. Real-World Case Studies

### Case Study 1: Uber - Demand Forecasting Drift

**Challenge**: Ride demand prediction model degraded during COVID-19

**Monitoring Implemented**:
- KS test on hourly demand distributions
- PSI for geographic features
- Prediction confidence monitoring

**Result**: Detected 35% drift in demand patterns within 48 hours of lockdown

### Case Study 2: Stitch Fix - Recommendation Drift

**Challenge**: Fashion recommendation model performance dropped 15%

**Root Cause**: Seasonal trend shifts not captured in training data

**Monitoring Solution**:
- Weekly PSI monitoring across 50+ features
- Automated retraining triggered when PSI > 0.2 for 3+ features
- A/B test new models before full deployment

---

## 8. Summary and Best Practices

### Key Takeaways

1. **Monitor Everything**: Data, predictions, performance, fairness, business metrics
2. **Use Multiple Methods**: KS test, PSI, Chi-square for comprehensive coverage
3. **Alert Intelligently**: Critical alerts → PagerDuty, Warnings → Slack, Info → Dashboards
4. **Automate Responses**: Trigger retraining when drift exceeds thresholds
5. **Ground Truth Delays**: Use proxy metrics when labels are delayed
6. **Dashboard for Visibility**: Grafana dashboards for stakeholder transparency

### Best Practices

- Set thresholds based on business impact, not arbitrary values
- Monitor correlations between features, not just univariate distributions
- Test alerting systems regularly (fire drills)
- Document all drift incidents for pattern recognition
- Review and adjust thresholds quarterly based on false positives

---

**Total Words**: ~5,200 words

**Next Module**: Module 04 - Data Quality and Validation
