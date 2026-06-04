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
