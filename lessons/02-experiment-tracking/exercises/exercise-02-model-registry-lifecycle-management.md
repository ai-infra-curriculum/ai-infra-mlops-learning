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
