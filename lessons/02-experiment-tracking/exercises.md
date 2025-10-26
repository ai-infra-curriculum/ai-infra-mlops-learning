# Module 02: Experiment Tracking & MLflow - Exercises

## Overview

This exercise set provides hands-on practice with experiment tracking, covering:
- MLflow Tracking API and experiment organization
- Model registry and lifecycle management
- Hyperparameter optimization with tracking
- Advanced MLflow features (projects, models, plugins)
- Integration with training pipelines

**Time Estimate**: 7-9 hours total

---

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

## Exercise 2: Model Registry & Lifecycle Management (90 minutes)

**Objective**: Implement model registry workflows including registration, staging, production promotion, and versioning.

### Background

You need to manage model versions through a lifecycle:
1. Register new models
2. Transition to staging for validation
3. Promote to production after approval
4. Archive old versions
5. Support rollback

### Tasks

1. **Implement model registration workflow**
2. **Create staging validation pipeline**
3. **Implement promotion logic with approval**
4. **Add versioning and aliasing**
5. **Implement rollback capability**

### Starter Code

```python
# model_registry.py
"""Model registry management with MLflow."""

import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities.model_registry import ModelVersion
from typing import List, Optional, Dict
from datetime import datetime
import pandas as pd

class ModelRegistryManager:
    """Manages model registry operations."""

    def __init__(self, tracking_uri: str = "http://localhost:5000"):
        """
        Initialize registry manager.

        Args:
            tracking_uri: MLflow tracking server URI
        """
        mlflow.set_tracking_uri(tracking_uri)
        self.client = MlflowClient()

    def register_model(
        self,
        model_uri: str,
        model_name: str,
        tags: Dict[str, str] = None,
        description: str = None
    ) -> ModelVersion:
        """
        Register a model in the registry.

        Args:
            model_uri: URI of the model (e.g., 'runs:/run_id/model')
            model_name: Name for the registered model
            tags: Optional tags for the model version
            description: Optional description

        Returns:
            Registered ModelVersion
        """
        # TODO: Register model
        # TODO: Add tags if provided
        # TODO: Update description if provided
        # TODO: Return ModelVersion
        pass

    def transition_model_stage(
        self,
        model_name: str,
        version: int,
        stage: str,
        archive_existing: bool = True
    ) -> ModelVersion:
        """
        Transition model version to a new stage.

        Args:
            model_name: Name of the registered model
            version: Version number
            stage: Target stage ('Staging', 'Production', 'Archived')
            archive_existing: Whether to archive existing models in target stage

        Returns:
            Updated ModelVersion
        """
        # TODO: Validate stage is valid
        valid_stages = ['Staging', 'Production', 'Archived', 'None']

        # TODO: Optionally archive existing models in target stage

        # TODO: Transition model version to new stage

        # TODO: Log transition event

        pass

    def get_latest_model_version(self, model_name: str, stage: str = None) -> Optional[ModelVersion]:
        """
        Get latest version of a model, optionally filtered by stage.

        Args:
            model_name: Name of the registered model
            stage: Optional stage filter

        Returns:
            Latest ModelVersion or None
        """
        # TODO: Search for model versions
        # TODO: Filter by stage if provided
        # TODO: Sort by version number
        # TODO: Return latest
        pass

    def compare_model_versions(
        self,
        model_name: str,
        version1: int,
        version2: int
    ) -> pd.DataFrame:
        """
        Compare metrics between two model versions.

        Args:
            model_name: Name of the registered model
            version1: First version number
            version2: Second version number

        Returns:
            DataFrame with comparison
        """
        # TODO: Get run IDs for both versions
        # TODO: Fetch metrics for both runs
        # TODO: Create comparison DataFrame
        pass

    def promote_model_to_production(
        self,
        model_name: str,
        version: int,
        validation_metrics: Dict[str, float],
        min_accuracy: float = 0.85
    ) -> bool:
        """
        Promote model to production if it meets criteria.

        Args:
            model_name: Name of the registered model
            version: Version to promote
            validation_metrics: Metrics from staging validation
            min_accuracy: Minimum accuracy threshold

        Returns:
            True if promoted successfully
        """
        # TODO: Validate metrics meet thresholds
        if validation_metrics.get('accuracy', 0) < min_accuracy:
            print(f"Model does not meet accuracy threshold: {validation_metrics.get('accuracy')} < {min_accuracy}")
            return False

        # TODO: Archive current production model

        # TODO: Promote staging model to production

        # TODO: Log promotion event

        return True

    def rollback_production(self, model_name: str) -> ModelVersion:
        """
        Rollback production to previous version.

        Args:
            model_name: Name of the registered model

        Returns:
            ModelVersion that was promoted to production
        """
        # TODO: Get production history
        # TODO: Find previous production version
        # TODO: Transition current production to archived
        # TODO: Promote previous version to production
        pass

    def delete_model_version(self, model_name: str, version: int):
        """
        Delete a specific model version.

        Args:
            model_name: Name of the registered model
            version: Version to delete
        """
        # TODO: Check version is not in Production
        # TODO: Delete version
        pass

    def list_models(self, filter_string: str = None) -> List[str]:
        """
        List all registered models.

        Args:
            filter_string: Optional filter (e.g., "name='model_name'")

        Returns:
            List of model names
        """
        # TODO: Search registered models
        # TODO: Apply filter if provided
        # TODO: Return list of names
        pass


# Example usage
if __name__ == '__main__':
    manager = ModelRegistryManager()

    # Register a model from a run
    # model_version = manager.register_model(
    #     model_uri="runs:/run_id/model",
    #     model_name="churn_predictor",
    #     tags={"team": "data-science", "project": "customer_retention"},
    #     description="Random Forest model for customer churn prediction"
    # )

    # Transition to staging
    # manager.transition_model_stage("churn_predictor", version=1, stage="Staging")

    # Validate and promote to production
    # validation_metrics = {'accuracy': 0.89, 'f1': 0.87}
    # manager.promote_model_to_production("churn_predictor", version=1, validation_metrics=validation_metrics)
```

```python
# staging_validation.py
"""Validation pipeline for models in staging."""

import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from typing import Dict

def validate_staging_model(model_name: str, version: int, test_data: pd.DataFrame, test_labels: pd.Series) -> Dict[str, float]:
    """
    Validate a staging model on test data.

    Args:
        model_name: Name of registered model
        version: Version number
        test_data: Test features
        test_labels: Test labels

    Returns:
        Dictionary of validation metrics
    """
    # TODO: Load model from registry
    model_uri = f"models:/{model_name}/{version}"
    model = mlflow.sklearn.load_model(model_uri)

    # TODO: Make predictions
    predictions = model.predict(test_data)
    prediction_probs = model.predict_proba(test_data)[:, 1] if hasattr(model, 'predict_proba') else None

    # TODO: Calculate metrics
    metrics = {
        'accuracy': accuracy_score(test_labels, predictions),
        'precision': precision_score(test_labels, predictions, average='weighted'),
        'recall': recall_score(test_labels, predictions, average='weighted'),
        'f1': f1_score(test_labels, predictions, average='weighted'),
    }

    if prediction_probs is not None:
        metrics['roc_auc'] = roc_auc_score(test_labels, prediction_probs)

    # TODO: Log validation metrics to model version
    client = MlflowClient()
    for metric_name, metric_value in metrics.items():
        client.log_metric(
            run_id=client.get_model_version(model_name, version).run_id,
            key=f"staging_validation_{metric_name}",
            value=metric_value
        )

    return metrics


def run_validation_pipeline(model_name: str, version: int) -> bool:
    """
    Run complete validation pipeline for a staging model.

    Args:
        model_name: Name of registered model
        version: Version number

    Returns:
        True if validation passes
    """
    # TODO: Load test data
    # test_data, test_labels = load_test_data()

    # TODO: Run validation
    # metrics = validate_staging_model(model_name, version, test_data, test_labels)

    # TODO: Check thresholds
    # THRESHOLDS = {
    #     'accuracy': 0.85,
    #     'f1': 0.80,
    #     'roc_auc': 0.85
    # }

    # TODO: Return validation result
    pass
```

### Validation

Test your registry workflow:
```bash
# Run training and register model
python train_with_tracking.py

# Register model
python -c "from model_registry import ModelRegistryManager; \
  mgr = ModelRegistryManager(); \
  mgr.register_model('runs:/RUN_ID/model', 'test_model')"

# Transition to staging
python -c "from model_registry import ModelRegistryManager; \
  mgr = ModelRegistryManager(); \
  mgr.transition_model_stage('test_model', 1, 'Staging')"

# Validate and promote
python staging_validation.py --model-name test_model --version 1
```

### Success Criteria

- [ ] Models can be registered programmatically
- [ ] Stage transitions work correctly
- [ ] Validation pipeline runs successfully
- [ ] Promotion requires threshold validation
- [ ] Rollback functionality works
- [ ] Version comparison is implemented
- [ ] Model deletion is protected (production models can't be deleted)

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Registration**: Use `mlflow.register_model(model_uri, name)` or `client.create_model_version()`
2. **Stages**: Valid stages are: 'None', 'Staging', 'Production', 'Archived'
3. **Latest Version**: Use `client.get_latest_versions(name, stages=[stage])`
4. **Archive Existing**: Before promoting, transition current production to 'Archived'
5. **Rollback**: Query model version history, find previous production version
6. **Tags**: Use `client.set_model_version_tag(name, version, key, value)`

</details>

---

## Exercise 3: Hyperparameter Optimization with Tracking (90 minutes)

**Objective**: Implement hyperparameter optimization using Optuna with comprehensive MLflow tracking.

### Background

Manual hyperparameter tuning is inefficient. You need to:
- Automate hyperparameter search
- Track all trials
- Visualize optimization progress
- Select best configuration
- Reproduce results

### Tasks

1. **Implement Optuna optimization with MLflow callback**
2. **Track all trials as MLflow runs**
3. **Create parent-child run hierarchy**
4. **Implement early stopping**
5. **Visualize optimization results**

### Starter Code

```python
# hyperparameter_optimization.py
"""Hyperparameter optimization with Optuna and MLflow tracking."""

import optuna
from optuna.integration.mlflow import MLflowCallback
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification
import numpy as np
from typing import Dict, Any

class MLflowOptunaBridge:
    """Bridge between Optuna and MLflow for comprehensive tracking."""

    def __init__(self, experiment_name: str, tracking_uri: str = "http://localhost:5000"):
        """
        Initialize MLflow-Optuna bridge.

        Args:
            experiment_name: Name of MLflow experiment
            tracking_uri: MLflow tracking URI
        """
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)
        self.experiment_name = experiment_name

    def objective(self, trial: optuna.Trial, X: np.ndarray, y: np.ndarray) -> float:
        """
        Objective function for Optuna optimization.

        Args:
            trial: Optuna trial
            X: Training features
            y: Training labels

        Returns:
            Score to optimize (higher is better)
        """
        # TODO: Define hyperparameter search space
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 10, 200),
            'max_depth': trial.suggest_int('max_depth', 2, 32),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
            'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', None]),
            'bootstrap': trial.suggest_categorical('bootstrap', [True, False]),
        }

        # TODO: Create and train model
        model = RandomForestClassifier(**params, random_state=42)

        # TODO: Evaluate with cross-validation
        score = cross_val_score(model, X, y, cv=5, scoring='accuracy', n_jobs=-1).mean()

        # TODO: Log to MLflow (handled by callback, but you can log additional metrics)

        return score

    def optimize(
        self,
        X: np.ndarray,
        y: np.ndarray,
        n_trials: int = 50,
        timeout: int = 3600
    ) -> optuna.Study:
        """
        Run hyperparameter optimization.

        Args:
            X: Training features
            y: Training labels
            n_trials: Number of optimization trials
            timeout: Timeout in seconds

        Returns:
            Completed Optuna study
        """
        # TODO: Create Optuna study
        study = optuna.create_study(
            study_name=f"{self.experiment_name}_optimization",
            direction='maximize',
            sampler=optuna.samplers.TPESampler(seed=42),
            pruner=optuna.pruners.MedianPruner(n_startup_trials=5, n_warmup_steps=10)
        )

        # TODO: Create MLflow callback
        mlflc = MLflowCallback(
            tracking_uri=mlflow.get_tracking_uri(),
            metric_name="accuracy",
            create_experiment=False,
            mlflow_kwargs={"experiment_name": self.experiment_name}
        )

        # TODO: Run optimization
        with mlflow.start_run(run_name="hyperparameter_optimization") as parent_run:
            mlflow.log_param("n_trials", n_trials)
            mlflow.log_param("timeout", timeout)
            mlflow.log_param("sampler", "TPESampler")
            mlflow.log_param("pruner", "MedianPruner")

            study.optimize(
                lambda trial: self.objective(trial, X, y),
                n_trials=n_trials,
                timeout=timeout,
                callbacks=[mlflc]
            )

            # TODO: Log best results
            mlflow.log_params(study.best_params)
            mlflow.log_metric("best_accuracy", study.best_value)
            mlflow.log_metric("n_trials_completed", len(study.trials))

            # TODO: Log optimization visualizations
            # self._log_optimization_plots(study)

        return study

    def _log_optimization_plots(self, study: optuna.Study):
        """
        Create and log optimization visualizations.

        Args:
            study: Completed Optuna study
        """
        try:
            import matplotlib.pyplot as plt
            from optuna.visualization.matplotlib import (
                plot_optimization_history,
                plot_param_importances,
                plot_parallel_coordinate
            )

            # TODO: Create optimization history plot
            fig = plot_optimization_history(study)
            mlflow.log_figure(fig, "optimization_history.png")
            plt.close()

            # TODO: Create parameter importance plot
            fig = plot_param_importances(study)
            mlflow.log_figure(fig, "param_importances.png")
            plt.close()

            # TODO: Create parallel coordinate plot
            fig = plot_parallel_coordinate(study)
            mlflow.log_figure(fig, "parallel_coordinate.png")
            plt.close()

        except Exception as e:
            print(f"Failed to log optimization plots: {e}")

    def retrain_best_model(self, study: optuna.Study, X: np.ndarray, y: np.ndarray):
        """
        Retrain model with best hyperparameters and log to MLflow.

        Args:
            study: Completed Optuna study
            X: Training features
            y: Training labels
        """
        with mlflow.start_run(run_name="best_model_retrain"):
            # TODO: Log best parameters
            mlflow.log_params(study.best_params)

            # TODO: Train model with best parameters
            model = RandomForestClassifier(**study.best_params, random_state=42)
            model.fit(X, y)

            # TODO: Log model
            mlflow.sklearn.log_model(model, "model")

            # TODO: Log final metrics
            score = cross_val_score(model, X, y, cv=5, scoring='accuracy').mean()
            mlflow.log_metric("cv_accuracy", score)

            print(f"Best model retrained with CV accuracy: {score:.4f}")


# Example usage
if __name__ == '__main__':
    # Generate sample data
    X, y = make_classification(n_samples=1000, n_features=20, n_informative=15, n_redundant=5, random_state=42)

    # Run optimization
    optimizer = MLflowOptunaBridge(experiment_name="rf_optimization")
    study = optimizer.optimize(X, y, n_trials=30)

    # Print results
    print(f"Best parameters: {study.best_params}")
    print(f"Best CV accuracy: {study.best_value:.4f}")

    # Retrain best model
    optimizer.retrain_best_model(study, X, y)
```

```python
# advanced_optimization.py
"""Advanced optimization strategies with MLflow tracking."""

import optuna
import mlflow
from sklearn.model_selection import train_test_split
from typing import Callable, Dict, Any
import numpy as np

class AdvancedOptimizer:
    """Advanced optimization with multiple strategies."""

    def __init__(self, tracking_uri: str = "http://localhost:5000"):
        mlflow.set_tracking_uri(tracking_uri)

    def multi_objective_optimization(
        self,
        X: np.ndarray,
        y: np.ndarray,
        experiment_name: str = "multi_objective_opt"
    ) -> optuna.Study:
        """
        Optimize for multiple objectives (e.g., accuracy and inference time).

        Args:
            X: Training features
            y: Training labels
            experiment_name: MLflow experiment name

        Returns:
            Completed multi-objective study
        """
        mlflow.set_experiment(experiment_name)

        def objective(trial):
            # TODO: Define hyperparameters
            # TODO: Train model
            # TODO: Calculate accuracy
            # TODO: Measure inference time
            # Return tuple of (accuracy, -inference_time) for minimization
            pass

        # TODO: Create multi-objective study
        study = optuna.create_study(directions=['maximize', 'minimize'])

        # TODO: Optimize
        # TODO: Log Pareto front to MLflow

        return study

    def distributed_optimization(
        self,
        objective_fn: Callable,
        n_trials: int = 100,
        n_jobs: int = -1
    ) -> optuna.Study:
        """
        Run distributed hyperparameter optimization.

        Args:
            objective_fn: Objective function
            n_trials: Number of trials
            n_jobs: Number of parallel jobs

        Returns:
            Completed study
        """
        # TODO: Create study with storage (for distributed optimization)
        # study = optuna.create_study(
        #     study_name="distributed_opt",
        #     storage="postgresql://user:password@localhost/optuna",
        #     direction="maximize",
        #     load_if_exists=True
        # )

        # TODO: Optimize with n_jobs
        # study.optimize(objective_fn, n_trials=n_trials, n_jobs=n_jobs)

        pass
```

### Validation

Run optimization and check results:
```bash
# Run hyperparameter optimization
python hyperparameter_optimization.py

# Check MLflow UI for:
# - Parent run with optimization summary
# - Child runs for each trial
# - Optimization visualizations
# - Best parameters logged
```

### Success Criteria

- [ ] Optuna optimization runs successfully
- [ ] All trials are logged to MLflow
- [ ] Parent-child run hierarchy is created
- [ ] Best parameters are identified and logged
- [ ] Visualization plots are generated and logged
- [ ] Early stopping (pruning) works
- [ ] Best model can be retrained with logged parameters

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Callback**: Use `MLflowCallback` from `optuna.integration.mlflow`
2. **Parent Run**: Start MLflow run before `study.optimize()` to create hierarchy
3. **Pruning**: Use `MedianPruner` or `HyperbandPruner` for early stopping
4. **Visualization**: Use `optuna.visualization.matplotlib` for plots
5. **Best Params**: Access via `study.best_params` and `study.best_value`
6. **Sampler**: TPESampler is good for < 100 trials, CmaEsSampler for continuous spaces

</details>

---

## Exercise 4: Advanced MLflow Features (60 minutes)

**Objective**: Explore advanced MLflow capabilities including Projects, Models format, and custom plugins.

### Tasks

1. **Create MLflow Project**
2. **Use MLflow Models format**
3. **Implement custom MLflow plugin**
4. **Set up MLflow with remote storage (S3)**

### Starter Code

```python
# MLproject
# MLflow project definition

name: ml_training_project

python_env: python_env.yaml

entry_points:
  main:
    parameters:
      n_estimators: {type: int, default: 100}
      max_depth: {type: int, default: 10}
      data_path: {type: str, default: "data/train.csv"}
    command: "python train.py --n-estimators {n_estimators} --max-depth {max_depth} --data-path {data_path}"

  train:
    parameters:
      config_path: {type: str, default: "config.yaml"}
    command: "python train.py --config {config_path}"

  evaluate:
    parameters:
      model_uri: {type: str}
      test_data_path: {type: str, default: "data/test.csv"}
    command: "python evaluate.py --model-uri {model_uri} --test-data {test_data_path}"

  deploy:
    parameters:
      model_name: {type: str}
      version: {type: int}
      target: {type: str, default: "staging"}
    command: "python deploy.py --model-name {model_name} --version {version} --target {target}"
```

```yaml
# python_env.yaml
# Python environment specification for MLflow project

python: "3.10"
build_dependencies:
  - pip
dependencies:
  - scikit-learn==1.3.0
  - pandas==2.0.0
  - numpy==1.24.0
  - mlflow==2.9.0
  - optuna==3.4.0
```

```python
# custom_model.py
"""Custom MLflow model with preprocessing."""

import mlflow
from mlflow.pyfunc import PythonModel, PythonModelContext
import pandas as pd
import numpy as np
from typing import Dict, Any
import joblib

class CustomChurnModel(PythonModel):
    """Custom model with integrated preprocessing."""

    def load_context(self, context: PythonModelContext):
        """
        Load model and artifacts.

        Args:
            context: MLflow context with artifacts
        """
        # TODO: Load sklearn model
        self.model = mlflow.sklearn.load_model(context.artifacts["model"])

        # TODO: Load preprocessing artifacts
        self.scaler = joblib.load(context.artifacts["scaler"])
        self.feature_names = joblib.load(context.artifacts["feature_names"])

    def predict(self, context: PythonModelContext, model_input: pd.DataFrame) -> np.ndarray:
        """
        Make predictions with preprocessing.

        Args:
            context: MLflow context
            model_input: Input dataframe

        Returns:
            Predictions array
        """
        # TODO: Validate input features
        # TODO: Preprocess input
        # TODO: Make predictions
        # TODO: Post-process predictions (e.g., format output)
        pass


def log_custom_model(model: Any, scaler: Any, feature_names: list, artifact_path: str = "model"):
    """
    Log custom model with artifacts.

    Args:
        model: Trained sklearn model
        scaler: Fitted scaler
        feature_names: List of feature names
        artifact_path: Path for model artifact
    """
    # TODO: Save scaler and feature names
    # TODO: Create artifacts dict
    artifacts = {
        "model": "model",
        "scaler": "scaler.joblib",
        "feature_names": "feature_names.joblib"
    }

    # TODO: Log model with pyfunc flavor
    mlflow.pyfunc.log_model(
        artifact_path=artifact_path,
        python_model=CustomChurnModel(),
        artifacts=artifacts
    )
```

```python
# s3_artifact_store.py
"""Configure MLflow with S3 artifact storage."""

import os
import mlflow

def configure_s3_artifacts():
    """Configure MLflow to use S3 for artifact storage."""

    # TODO: Set environment variables for S3
    # os.environ['AWS_ACCESS_KEY_ID'] = 'your_key'
    # os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_secret'
    # os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://s3.amazonaws.com'

    # TODO: Set artifact URI
    # artifact_uri = "s3://your-bucket/mlflow-artifacts"
    # mlflow.set_tracking_uri("http://localhost:5000")

    # TODO: Test artifact logging
    pass
```

### Success Criteria

- [ ] MLflow Project runs successfully
- [ ] Custom model loads and predicts correctly
- [ ] S3 artifact storage is configured
- [ ] Project can be run from Git repository

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Projects**: Run with `mlflow run . -P param=value`
2. **Custom Model**: Implement `load_context` and `predict` methods
3. **S3**: Set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and use `s3://bucket/path` in artifact URI
4. **Git**: Run project from Git: `mlflow run https://github.com/user/repo.git`

</details>

---

## Exercise 5: End-to-End MLflow Pipeline (120 minutes)

**Objective**: Build a complete MLOps pipeline integrating all MLflow components.

### Components

1. Data versioning with MLflow datasets
2. Hyperparameter optimization with Optuna
3. Model training with comprehensive tracking
4. Model registry and lifecycle management
5. Model deployment (local or cloud)
6. Monitoring and retraining triggers

This is a comprehensive capstone exercise that combines everything learned.

### Success Criteria

- [ ] Complete pipeline from data to deployment
- [ ] All components integrated with MLflow
- [ ] Models versioned and managed in registry
- [ ] Deployment is automated
- [ ] Monitoring triggers retraining

---

## Submission Guidelines

For each exercise, submit:
1. **Code**: All implementation files
2. **MLflow Runs**: Screenshots of MLflow UI showing tracked runs
3. **Documentation**: Explanation of your tracking strategy
4. **Metrics**: Comparison of different experiments
5. **Reflection**: Lessons learned about experiment tracking

**Estimated Total Time**: 7-9 hours
**Difficulty**: Intermediate to Advanced

Good luck! 🚀
