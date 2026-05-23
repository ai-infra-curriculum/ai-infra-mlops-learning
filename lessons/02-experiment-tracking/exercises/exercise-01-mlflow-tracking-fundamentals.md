## Exercise 1: MLflow Tracking Fundamentals (75 minutes)

**Objective**: Implement comprehensive experiment tracking for a machine learning project using MLflow.

### Background

You're training a classification model and need to track experiments systematically. Your tracking should capture:
- Hyperparameters
- Training/validation metrics over time
- Model artifacts
- Dataset versions
- Environment configuration

### Tasks

1. **Set up MLflow tracking server**:
   - Configure backend store (SQLite or PostgreSQL)
   - Configure artifact store (local or S3)
   - Start tracking server

2. **Implement tracking in training script**:
   - Log hyperparameters
   - Log metrics at each epoch
   - Log final model and artifacts
   - Tag runs with metadata

3. **Create experiment organization structure**:
   - Experiments by model type
   - Consistent naming conventions
   - Meaningful tags

4. **Compare multiple runs**:
   - Use MLflow UI to compare experiments
   - Analyze parameter vs. metric relationships
   - Identify best performing model

### Starter Code

```python
# train_with_tracking.py
"""Training script with comprehensive MLflow tracking."""

import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
import numpy as np
from typing import Dict, Any
import json

class MLflowTracker:
    """Wrapper for MLflow tracking operations."""

    def __init__(self, tracking_uri: str = "http://localhost:5000", experiment_name: str = "default"):
        """
        Initialize MLflow tracker.

        Args:
            tracking_uri: MLflow tracking server URI
            experiment_name: Name of the experiment
        """
        # TODO: Set MLflow tracking URI
        # TODO: Set or create experiment
        # TODO: Store experiment ID
        pass

    def start_run(self, run_name: str = None, tags: Dict[str, str] = None) -> Any:
        """
        Start a new MLflow run.

        Args:
            run_name: Optional name for the run
            tags: Optional tags to apply to the run

        Returns:
            MLflow run context manager
        """
        # TODO: Implement run start with optional name and tags
        pass

    def log_params(self, params: Dict[str, Any]):
        """
        Log parameters to MLflow.

        Args:
            params: Dictionary of parameters
        """
        # TODO: Log parameters
        # Handle nested dictionaries by flattening
        pass

    def log_metrics(self, metrics: Dict[str, float], step: int = None):
        """
        Log metrics to MLflow.

        Args:
            metrics: Dictionary of metrics
            step: Optional step number for time-series metrics
        """
        # TODO: Log metrics with optional step
        pass

    def log_model(self, model: Any, artifact_path: str, **kwargs):
        """
        Log model to MLflow.

        Args:
            model: Trained model
            artifact_path: Path within run's artifact URI
            **kwargs: Additional arguments for model logging
        """
        # TODO: Log model with sklearn flavor
        pass

    def log_dataset_info(self, X: pd.DataFrame, y: pd.Series, split: str):
        """
        Log dataset information.

        Args:
            X: Feature dataframe
            y: Target series
            split: 'train', 'val', or 'test'
        """
        # TODO: Log dataset statistics
        # - Number of samples
        # - Number of features
        # - Class distribution
        # - Feature names
        pass


def train_model(config: Dict[str, Any]) -> Dict[str, float]:
    """
    Train a model with MLflow tracking.

    Args:
        config: Configuration dictionary with hyperparameters

    Returns:
        Dictionary of evaluation metrics
    """
    # TODO: Initialize MLflowTracker

    # TODO: Load data (use sklearn.datasets or your own data)

    # TODO: Split data
    X_train, X_val, y_train, y_val = train_test_split(...)

    # TODO: Start MLflow run
    with tracker.start_run(run_name=config.get('run_name'), tags=config.get('tags')):

        # TODO: Log hyperparameters
        tracker.log_params(config['model_params'])

        # TODO: Log dataset info
        tracker.log_dataset_info(X_train, y_train, 'train')
        tracker.log_dataset_info(X_val, y_val, 'val')

        # TODO: Train model
        model = RandomForestClassifier(**config['model_params'])
        # TODO: Implement training loop if applicable

        # TODO: Evaluate and log metrics
        # Calculate accuracy, precision, recall, F1
        metrics = {}  # Populate with metrics

        tracker.log_metrics(metrics)

        # TODO: Log model
        tracker.log_model(model, "model")

        # TODO: Log additional artifacts (confusion matrix, feature importance, etc.)

        return metrics


if __name__ == '__main__':
    # Example configuration
    config = {
        'run_name': 'rf_baseline',
        'tags': {
            'model_type': 'random_forest',
            'dataset': 'customer_churn',
            'developer': 'your_name'
        },
        'model_params': {
            'n_estimators': 100,
            'max_depth': 10,
            'min_samples_split': 5,
            'random_state': 42
        }
    }

    metrics = train_model(config)
    print(f"Model trained with metrics: {metrics}")
```

### Configuration Files

```python
# mlflow_config.py
"""MLflow configuration management."""

import os
from pathlib import Path

class MLflowConfig:
    """MLflow configuration settings."""

    # Tracking server
    TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI', 'http://localhost:5000')

    # Backend store (where run metadata is stored)
    # Options: 'sqlite:///mlflow.db' or 'postgresql://user:pass@host:5432/mlflow'
    BACKEND_STORE_URI = os.getenv('MLFLOW_BACKEND_STORE_URI', 'sqlite:///mlflow.db')

    # Artifact store (where artifacts like models are stored)
    # Options: './mlruns', 's3://bucket/path', 'gs://bucket/path'
    ARTIFACT_ROOT = os.getenv('MLFLOW_ARTIFACT_ROOT', './mlruns')

    # Experiment names
    DEFAULT_EXPERIMENT = 'default'

    @classmethod
    def get_tracking_uri(cls) -> str:
        """Get configured tracking URI."""
        return cls.TRACKING_URI

    @classmethod
    def setup_tracking(cls):
        """Configure MLflow tracking."""
        import mlflow
        mlflow.set_tracking_uri(cls.TRACKING_URI)
```

```bash
# scripts/start_mlflow_server.sh
#!/bin/bash
# Script to start MLflow tracking server

set -e

# Configuration
BACKEND_STORE_URI=${MLFLOW_BACKEND_STORE_URI:-"sqlite:///mlflow.db"}
ARTIFACT_ROOT=${MLFLOW_ARTIFACT_ROOT:-"./mlruns"}
HOST=${MLFLOW_HOST:-"0.0.0.0"}
PORT=${MLFLOW_PORT:-5000}

echo "Starting MLflow tracking server..."
echo "Backend store: $BACKEND_STORE_URI"
echo "Artifact root: $ARTIFACT_ROOT"
echo "Listening on: $HOST:$PORT"

# TODO: Add command to start MLflow server
# mlflow server \
#   --backend-store-uri $BACKEND_STORE_URI \
#   --default-artifact-root $ARTIFACT_ROOT \
#   --host $HOST \
#   --port $PORT
```

### Validation Tests

```python
# tests/test_tracking.py
"""Tests for MLflow tracking functionality."""

import pytest
import mlflow
from train_with_tracking import MLflowTracker, train_model

@pytest.fixture
def mlflow_tracker():
    """Create MLflow tracker for testing."""
    # TODO: Set up test tracking URI
    # TODO: Create test experiment
    tracker = MLflowTracker(tracking_uri="sqlite:///test_mlflow.db", experiment_name="test_experiment")
    yield tracker
    # TODO: Cleanup test artifacts

def test_mlflow_tracker_initialization(mlflow_tracker):
    """Test that MLflow tracker initializes correctly."""
    # TODO: Assert tracker is configured
    # TODO: Assert experiment exists
    pass

def test_run_logging(mlflow_tracker):
    """Test that runs are logged correctly."""
    with mlflow_tracker.start_run(run_name="test_run"):
        # TODO: Log test parameters
        mlflow_tracker.log_params({'test_param': 'value'})

        # TODO: Log test metrics
        mlflow_tracker.log_metrics({'test_metric': 0.95})

    # TODO: Verify run was logged
    # TODO: Verify parameters were logged
    # TODO: Verify metrics were logged

def test_model_logging(mlflow_tracker):
    """Test that models are logged correctly."""
    # TODO: Create simple test model
    # TODO: Log model
    # TODO: Verify model artifact exists

# Run with: pytest tests/test_tracking.py -v
```

### Success Criteria

- [ ] MLflow tracking server running and accessible
- [ ] Experiments are organized logically
- [ ] All hyperparameters are logged
- [ ] Metrics are logged at each epoch/step
- [ ] Models are saved and retrievable
- [ ] Dataset information is captured
- [ ] Runs are searchable and comparable in UI
- [ ] Tests pass

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Tracking Server**: Use `mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns`
2. **Nested Params**: Flatten nested dicts: `{'model.n_estimators': 100}` instead of `{'model': {'n_estimators': 100}}`
3. **Metrics Over Time**: Use `step` parameter: `mlflow.log_metric('loss', 0.5, step=epoch)`
4. **Tags**: Use for filtering: `mlflow.set_tag('model_type', 'random_forest')`
5. **Artifacts**: Log plots with `mlflow.log_figure()` or files with `mlflow.log_artifact()`

</details>

---
