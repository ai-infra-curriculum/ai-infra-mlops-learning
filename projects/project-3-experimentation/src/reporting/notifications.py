"""Notifications - TODO: Implement notification service"""

class NotificationService:
    """TODO: Send notifications via email/Slack"""
    def send_experiment_started(self, experiment): raise NotImplementedError()
    def send_significant_result(self, experiment, result): raise NotImplementedError()
    def send_rollback_alert(self, deployment, reason): raise NotImplementedError()
