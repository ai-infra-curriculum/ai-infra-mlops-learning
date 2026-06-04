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
