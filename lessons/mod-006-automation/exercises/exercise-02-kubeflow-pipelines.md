## Exercise 2: Kubeflow Pipelines (90 minutes)

**Objective**: Build a containerized ML pipeline using Kubeflow Pipelines with reusable components.

### Background

Kubeflow Pipelines provides:
- Container-native workflow execution
- Reusable pipeline components
- Strong typing and data passing
- Native Kubernetes integration
- Experiment tracking

### Tasks

1. **Set up Kubeflow Pipelines environment**
2. **Create reusable pipeline components**
3. **Build complete ML pipeline**
4. **Configure resource requirements**
5. **Run and monitor pipeline**

### Starter Code

```python
# ml_pipeline.py
"""
Kubeflow Pipeline for ML model training.
"""

import kfp
from kfp import dsl
from kfp.dsl import Dataset, Model, Input, Output, Metrics
from typing import NamedTuple

# TODO: Define component for data loading
@dsl.component(
    packages_to_install=['pandas==2.0.0', 'scikit-learn==1.3.0'],
    base_image='python:3.10-slim'
)
def load_data(
    dataset_url: str,
    output_dataset: Output[Dataset],
) -> NamedTuple('Outputs', [('num_rows', int), ('num_features', int)]):
    """
    Load dataset from URL.

    TODO: Implement data loading
    - Fetch data from URL
    - Perform basic validation
    - Save to output_dataset path
    - Return dataset statistics
    """
    import pandas as pd
    from collections import namedtuple

    # TODO: Load data
    # df = pd.read_csv(dataset_url)

    # TODO: Save dataset
    # df.to_csv(output_dataset.path, index=False)

    # TODO: Return statistics
    # outputs = namedtuple('Outputs', ['num_rows', 'num_features'])
    # return outputs(num_rows=df.shape[0], num_features=df.shape[1])

    pass


@dsl.component(
    packages_to_install=['pandas==2.0.0', 'scikit-learn==1.3.0'],
    base_image='python:3.10-slim'
)
def preprocess_data(
    input_dataset: Input[Dataset],
    train_dataset: Output[Dataset],
    test_dataset: Output[Dataset],
    test_size: float = 0.2,
):
    """
    Preprocess and split data.

    TODO: Implement preprocessing
    - Load input dataset
    - Handle missing values
    - Encode categorical features
    - Split into train/test
    - Save processed datasets
    """
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, LabelEncoder

    # TODO: Load data
    # df = pd.read_csv(input_dataset.path)

    # TODO: Preprocessing steps
    # - Handle missing values
    # - Encode categorical variables
    # - Scale numerical features

    # TODO: Split data
    # train, test = train_test_split(df, test_size=test_size, random_state=42)

    # TODO: Save datasets
    # train.to_csv(train_dataset.path, index=False)
    # test.to_csv(test_dataset.path, index=False)

    pass


@dsl.component(
    packages_to_install=['pandas==2.0.0', 'scikit-learn==1.3.0', 'mlflow==2.9.0'],
    base_image='python:3.10-slim'
)
def train_model(
    train_dataset: Input[Dataset],
    model: Output[Model],
    metrics: Output[Metrics],
    n_estimators: int = 100,
    max_depth: int = 10,
    mlflow_tracking_uri: str = "http://mlflow:5000",
) -> float:
    """
    Train ML model.

    TODO: Implement model training
    - Load training data
    - Train model
    - Log to MLflow
    - Save model
    - Return accuracy
    """
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import cross_val_score
    import mlflow
    import mlflow.sklearn
    import joblib

    # TODO: Set up MLflow
    # mlflow.set_tracking_uri(mlflow_tracking_uri)

    # TODO: Load training data
    # df = pd.read_csv(train_dataset.path)
    # X = df.drop('target', axis=1)
    # y = df['target']

    # TODO: Start MLflow run
    with mlflow.start_run(run_name="kubeflow_training"):

        # TODO: Log parameters
        # mlflow.log_param('n_estimators', n_estimators)
        # mlflow.log_param('max_depth', max_depth)

        # TODO: Train model
        # clf = RandomForestClassifier(
        #     n_estimators=n_estimators,
        #     max_depth=max_depth,
        #     random_state=42
        # )
        # clf.fit(X, y)

        # TODO: Cross-validation
        # cv_scores = cross_val_score(clf, X, y, cv=5, scoring='accuracy')
        # accuracy = cv_scores.mean()

        # TODO: Log metrics
        # mlflow.log_metric('cv_accuracy', accuracy)
        # mlflow.log_metric('cv_std', cv_scores.std())

        # TODO: Log model to MLflow
        # mlflow.sklearn.log_model(clf, "model")

        # TODO: Save model locally for Kubeflow
        # joblib.dump(clf, model.path)

        # TODO: Log metrics for Kubeflow UI
        # metrics.log_metric('accuracy', accuracy)
        # metrics.log_metric('n_estimators', n_estimators)

    # return accuracy
    pass


@dsl.component(
    packages_to_install=['pandas==2.0.0', 'scikit-learn==1.3.0'],
    base_image='python:3.10-slim'
)
def evaluate_model(
    model: Input[Model],
    test_dataset: Input[Dataset],
    metrics: Output[Metrics],
) -> NamedTuple('EvalMetrics', [('accuracy', float), ('precision', float), ('recall', float)]):
    """
    Evaluate model on test set.

    TODO: Implement evaluation
    - Load model and test data
    - Make predictions
    - Calculate metrics
    - Save metrics
    """
    import pandas as pd
    from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
    import joblib
    from collections import namedtuple

    # TODO: Load model and test data
    # clf = joblib.load(model.path)
    # df = pd.read_csv(test_dataset.path)
    # X_test = df.drop('target', axis=1)
    # y_test = df['target']

    # TODO: Make predictions
    # y_pred = clf.predict(X_test)

    # TODO: Calculate metrics
    # acc = accuracy_score(y_test, y_pred)
    # prec = precision_score(y_test, y_pred, average='weighted')
    # rec = recall_score(y_test, y_pred, average='weighted')

    # TODO: Log metrics
    # metrics.log_metric('test_accuracy', acc)
    # metrics.log_metric('test_precision', prec)
    # metrics.log_metric('test_recall', rec)

    # TODO: Return metrics
    # EvalMetrics = namedtuple('EvalMetrics', ['accuracy', 'precision', 'recall'])
    # return EvalMetrics(accuracy=acc, precision=prec, recall=rec)

    pass


@dsl.component(
    packages_to_install=['mlflow==2.9.0'],
    base_image='python:3.10-slim'
)
def register_model(
    model: Input[Model],
    model_name: str,
    accuracy: float,
    mlflow_tracking_uri: str = "http://mlflow:5000",
) -> str:
    """
    Register model in MLflow registry if it meets threshold.

    TODO: Implement conditional registration
    - Check accuracy threshold
    - Register model if threshold met
    - Return registration status
    """
    import mlflow
    from mlflow.tracking import MlflowClient

    # TODO: Set up MLflow
    # mlflow.set_tracking_uri(mlflow_tracking_uri)
    # client = MlflowClient()

    # TODO: Check threshold
    # threshold = 0.85
    # if accuracy < threshold:
    #     return f"Model not registered (accuracy {accuracy:.4f} < {threshold})"

    # TODO: Register model
    # model_version = mlflow.register_model(
    #     model_uri=f"file://{model.path}",
    #     name=model_name
    # )

    # TODO: Transition to staging
    # client.transition_model_version_stage(
    #     name=model_name,
    #     version=model_version.version,
    #     stage="Staging"
    # )

    # return f"Model registered as {model_name} v{model_version.version}"
    pass


# TODO: Define the pipeline
@dsl.pipeline(
    name='ML Training Pipeline',
    description='End-to-end ML training pipeline with MLflow integration'
)
def ml_training_pipeline(
    dataset_url: str = 'https://example.com/data.csv',
    n_estimators: int = 100,
    max_depth: int = 10,
    test_size: float = 0.2,
    model_name: str = 'sklearn_classifier',
    mlflow_tracking_uri: str = 'http://mlflow:5000',
):
    """
    Complete ML training pipeline.

    TODO: Wire components together
    - Load data
    - Preprocess
    - Train
    - Evaluate
    - Register
    """

    # TODO: Load data
    # load_data_task = load_data(dataset_url=dataset_url)

    # TODO: Preprocess
    # preprocess_task = preprocess_data(
    #     input_dataset=load_data_task.outputs['output_dataset'],
    #     test_size=test_size
    # )

    # TODO: Train model
    # train_task = train_model(
    #     train_dataset=preprocess_task.outputs['train_dataset'],
    #     n_estimators=n_estimators,
    #     max_depth=max_depth,
    #     mlflow_tracking_uri=mlflow_tracking_uri
    # )

    # TODO: Evaluate model
    # eval_task = evaluate_model(
    #     model=train_task.outputs['model'],
    #     test_dataset=preprocess_task.outputs['test_dataset']
    # )

    # TODO: Register model
    # register_task = register_model(
    #     model=train_task.outputs['model'],
    #     model_name=model_name,
    #     accuracy=eval_task.outputs['accuracy'],
    #     mlflow_tracking_uri=mlflow_tracking_uri
    # )

    # TODO: Configure resource requirements
    # train_task.set_cpu_limit('2')
    # train_task.set_memory_limit('4G')

    pass


if __name__ == '__main__':
    # Compile pipeline
    from kfp import compiler

    compiler.Compiler().compile(
        pipeline_func=ml_training_pipeline,
        package_path='ml_pipeline.yaml'
    )

    print("Pipeline compiled to ml_pipeline.yaml")

    # TODO: Submit to Kubeflow
    # client = kfp.Client(host='http://localhost:8080')
    # run = client.create_run_from_pipeline_func(
    #     ml_training_pipeline,
    #     arguments={
    #         'dataset_url': 'https://example.com/data.csv',
    #         'n_estimators': 150,
    #         'max_depth': 12
    #     }
    # )
```

### Validation

```bash
# Compile pipeline
python ml_pipeline.py

# Submit pipeline (if Kubeflow is running)
# kfp run submit -f ml_pipeline.yaml

# Monitor in Kubeflow UI
# Open http://localhost:8080
```

### Success Criteria

- [ ] Pipeline compiles without errors
- [ ] All components are properly typed
- [ ] Data flows correctly between components
- [ ] MLflow integration works
- [ ] Resource limits are configured
- [ ] Pipeline runs successfully in Kubeflow
- [ ] Metrics are visible in Kubeflow UI

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Components**: Use `@dsl.component` decorator for lightweight components
2. **Data Passing**: Use `Input[Dataset]` and `Output[Dataset]` for type-safe data passing
3. **Metrics**: Use `Output[Metrics]` and `metrics.log_metric()` for Kubeflow UI
4. **Resources**: Use `.set_cpu_limit()`, `.set_memory_limit()`, `.set_gpu_limit()`
5. **Compilation**: Use `compiler.Compiler().compile()` to generate YAML
6. **Dependencies**: Components download packages at runtime - keep minimal

</details>

---
