"""
Monitoring module

Provides Prometheus metrics, alerts, and observability features.
"""

from .metrics import setup_metrics, record_prediction
from .alerts import AlertManager

__all__ = ["setup_metrics", "record_prediction", "AlertManager"]
