"""
Locust load testing script

Run with:
    locust -f tests/load/locustfile.py --host=http://localhost:8000

TODO: Implement comprehensive load tests
"""

from locust import HttpUser, task, between
import random


class ModelServerUser(HttpUser):
    """
    Simulated user for load testing

    TODO: Implement realistic user behavior:
    - Model predictions with various payloads
    - Batch predictions
    - Model info queries
    - Mix of different models
    """

    # Wait time between tasks (1-3 seconds)
    wait_time = between(1, 3)

    def on_start(self):
        """
        Called when user starts

        TODO: Implement setup:
        - Get authentication token if needed
        - Get list of available models
        """
        pass

    @task(10)
    def predict_single(self):
        """
        Make single prediction

        TODO: Implement with:
        - Random model selection
        - Random valid input data
        - Verify response
        """
        # payload = {
        #     "features": [random.random() for _ in range(10)]
        # }
        # self.client.post(
        #     "/predict/sample-model",
        #     json=payload,
        #     name="/predict/[model]"
        # )
        pass

    @task(3)
    def predict_batch(self):
        """
        Make batch prediction

        TODO: Implement batch prediction load test
        """
        pass

    @task(2)
    def list_models(self):
        """
        List available models

        TODO: Implement model listing
        """
        # self.client.get("/models")
        pass

    @task(1)
    def get_model_info(self):
        """
        Get model information

        TODO: Implement model info query
        """
        pass


class HighLoadUser(HttpUser):
    """
    High-load user for stress testing

    TODO: Implement aggressive load patterns
    """

    wait_time = between(0.1, 0.5)

    @task
    def rapid_predictions(self):
        """Rapid-fire predictions"""
        pass


# TODO: Add custom load shapes for spike testing
# class SpikeLoadShape(LoadTestShape):
#     """
#     Spike load shape
#
#     Simulates sudden traffic spikes
#     """
#     pass
