"""Metrics Logging - TODO: Implement time-series metrics logging"""

class MetricsLogger:
    """TODO: Log metrics to database and MLflow"""
    def log_metric(self, experiment_id, arm, metric_name, value, timestamp): raise NotImplementedError()
    def get_metrics(self, experiment_id): raise NotImplementedError()
