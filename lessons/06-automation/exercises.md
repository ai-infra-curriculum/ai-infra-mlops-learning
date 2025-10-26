# Module 06: Automation & Orchestration - Exercises

## Overview

This exercise set provides hands-on practice with workflow automation and orchestration, covering:
- Apache Airflow DAG development for ML workflows
- Kubeflow Pipelines for container-native orchestration
- Error handling, retry logic, and failure recovery
- MLflow integration in automated pipelines
- Production-grade ML pipeline design

**Time Estimate**: 6-9 hours total

---

## Exercise 1: Apache Airflow ML DAG (90 minutes)

**Objective**: Build a complete ML training pipeline using Apache Airflow with proper task dependencies, error handling, and monitoring.

### Background

You need to create an automated ML training pipeline that:
- Runs daily to fetch new data
- Preprocesses and validates data quality
- Trains a model with hyperparameter tuning
- Evaluates model performance
- Registers model in MLflow if performance meets threshold
- Sends notifications on success/failure

### Tasks

1. **Set up Airflow environment**:
   - Configure Airflow with LocalExecutor or CeleryExecutor
   - Set up connections for MLflow and data sources
   - Configure email/Slack alerts

2. **Create ML training DAG**:
   - Data ingestion task
   - Data validation task
   - Preprocessing task
   - Training task
   - Evaluation task
   - Model registration task (conditional)

3. **Implement task dependencies**:
   - Define proper task order
   - Handle branching logic
   - Configure retries and timeouts

4. **Add monitoring and alerting**:
   - Email on failure
   - Success callbacks
   - SLA monitoring

### Starter Code

```python
# dags/ml_training_pipeline.py
"""
Airflow DAG for automated ML model training pipeline.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.email import EmailOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable
import pandas as pd
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import logging

# DAG default arguments
default_args = {
    'owner': 'ml-team',
    'depends_on_past': False,
    'email': ['ml-team@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=2),
}

# TODO: Define DAG
dag = DAG(
    'ml_training_pipeline',
    default_args=default_args,
    description='Automated ML model training and deployment pipeline',
    schedule_interval='@daily',  # TODO: Adjust schedule as needed
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['ml', 'training', 'production'],
)


def fetch_data(**context):
    """
    Fetch training data from data source.

    TODO: Implement data fetching logic
    - Connect to data warehouse/database
    - Apply date filters based on execution_date
    - Save data to staging location
    - Push data path to XCom
    """
    execution_date = context['execution_date']
    logging.info(f"Fetching data for date: {execution_date}")

    # TODO: Implement data fetching
    # data = fetch_from_source(start_date=execution_date - timedelta(days=30),
    #                          end_date=execution_date)

    # TODO: Save data and push path to XCom
    # data_path = f"/tmp/data_{execution_date.strftime('%Y%m%d')}.csv"
    # data.to_csv(data_path, index=False)
    # context['task_instance'].xcom_push(key='data_path', value=data_path)

    pass


def validate_data(**context):
    """
    Validate data quality and schema.

    TODO: Implement data validation
    - Check for missing values
    - Validate schema
    - Check data volume
    - Raise exception if validation fails
    """
    ti = context['task_instance']
    data_path = ti.xcom_pull(task_ids='fetch_data', key='data_path')

    logging.info(f"Validating data at: {data_path}")

    # TODO: Load and validate data
    # data = pd.read_csv(data_path)

    # TODO: Validation checks
    # if data.isnull().sum().sum() / (data.shape[0] * data.shape[1]) > 0.1:
    #     raise ValueError("More than 10% missing values detected")

    # if data.shape[0] < 1000:
    #     raise ValueError("Insufficient data volume")

    # TODO: Push validation results to XCom
    # ti.xcom_push(key='validation_passed', value=True)

    pass


def preprocess_data(**context):
    """
    Preprocess and feature engineer data.

    TODO: Implement preprocessing
    - Handle missing values
    - Encode categorical variables
    - Scale numerical features
    - Create train/val/test splits
    """
    ti = context['task_instance']
    data_path = ti.xcom_pull(task_ids='fetch_data', key='data_path')

    logging.info(f"Preprocessing data from: {data_path}")

    # TODO: Load data
    # data = pd.read_csv(data_path)

    # TODO: Preprocessing steps
    # - Feature engineering
    # - Encoding
    # - Scaling

    # TODO: Train/val/test split
    # X_train, X_val, y_train, y_val = train_test_split(...)

    # TODO: Save processed data and push paths to XCom
    # processed_data_path = "/tmp/processed_data.pkl"
    # ti.xcom_push(key='processed_data_path', value=processed_data_path)

    pass


def train_model(**context):
    """
    Train ML model with MLflow tracking.

    TODO: Implement model training
    - Load processed data
    - Set up MLflow tracking
    - Train model
    - Log parameters, metrics, and artifacts
    """
    ti = context['task_instance']
    processed_data_path = ti.xcom_pull(task_ids='preprocess_data', key='processed_data_path')

    logging.info(f"Training model with data from: {processed_data_path}")

    # TODO: Set MLflow tracking URI
    mlflow_tracking_uri = Variable.get("mlflow_tracking_uri", "http://mlflow:5000")
    mlflow.set_tracking_uri(mlflow_tracking_uri)

    # TODO: Start MLflow run
    with mlflow.start_run(run_name=f"airflow_training_{context['ds']}"):

        # TODO: Load processed data
        # X_train, y_train, X_val, y_val = load_processed_data(processed_data_path)

        # TODO: Define hyperparameters
        params = {
            'n_estimators': 100,
            'max_depth': 10,
            'min_samples_split': 5,
            'random_state': 42
        }

        # TODO: Log parameters
        mlflow.log_params(params)

        # TODO: Train model
        # model = RandomForestClassifier(**params)
        # model.fit(X_train, y_train)

        # TODO: Evaluate on validation set
        # val_predictions = model.predict(X_val)
        # accuracy = accuracy_score(y_val, val_predictions)
        # f1 = f1_score(y_val, val_predictions, average='weighted')

        # TODO: Log metrics
        # mlflow.log_metric('val_accuracy', accuracy)
        # mlflow.log_metric('val_f1', f1)

        # TODO: Log model
        # mlflow.sklearn.log_model(model, "model")

        # TODO: Get run ID and push to XCom
        # run_id = mlflow.active_run().info.run_id
        # ti.xcom_push(key='mlflow_run_id', value=run_id)
        # ti.xcom_push(key='val_accuracy', value=accuracy)

    pass


def evaluate_model(**context):
    """
    Evaluate model on test set and generate evaluation report.

    TODO: Implement model evaluation
    - Load model from MLflow
    - Evaluate on test set
    - Generate confusion matrix
    - Log evaluation metrics
    """
    ti = context['task_instance']
    run_id = ti.xcom_pull(task_ids='train_model', key='mlflow_run_id')

    logging.info(f"Evaluating model from run: {run_id}")

    # TODO: Load model from MLflow
    # model_uri = f"runs:/{run_id}/model"
    # model = mlflow.sklearn.load_model(model_uri)

    # TODO: Load test data
    # X_test, y_test = load_test_data()

    # TODO: Make predictions and evaluate
    # test_predictions = model.predict(X_test)
    # test_accuracy = accuracy_score(y_test, test_predictions)

    # TODO: Log test metrics to MLflow
    # with mlflow.start_run(run_id=run_id):
    #     mlflow.log_metric('test_accuracy', test_accuracy)

    # TODO: Push test accuracy to XCom for decision making
    # ti.xcom_push(key='test_accuracy', value=test_accuracy)

    pass


def check_model_performance(**context):
    """
    Check if model meets performance threshold for registration.

    Returns:
        str: 'register_model' if threshold met, 'skip_registration' otherwise
    """
    ti = context['task_instance']
    test_accuracy = ti.xcom_pull(task_ids='evaluate_model', key='test_accuracy')

    # TODO: Get threshold from Airflow Variable
    accuracy_threshold = float(Variable.get("model_accuracy_threshold", "0.85"))

    logging.info(f"Test accuracy: {test_accuracy}, Threshold: {accuracy_threshold}")

    if test_accuracy >= accuracy_threshold:
        logging.info("Model meets threshold - will register")
        return 'register_model'
    else:
        logging.warning("Model does not meet threshold - skipping registration")
        return 'skip_registration'


def register_model(**context):
    """
    Register model in MLflow Model Registry.

    TODO: Implement model registration
    - Get run ID from XCom
    - Register model with descriptive name
    - Transition to Staging
    - Add tags and description
    """
    ti = context['task_instance']
    run_id = ti.xcom_pull(task_ids='train_model', key='mlflow_run_id')
    test_accuracy = ti.xcom_pull(task_ids='evaluate_model', key='test_accuracy')

    logging.info(f"Registering model from run: {run_id}")

    # TODO: Set MLflow tracking URI
    mlflow_tracking_uri = Variable.get("mlflow_tracking_uri", "http://mlflow:5000")
    mlflow.set_tracking_uri(mlflow_tracking_uri)

    # TODO: Register model
    # model_name = "customer_churn_classifier"
    # model_uri = f"runs:/{run_id}/model"

    # model_version = mlflow.register_model(
    #     model_uri=model_uri,
    #     name=model_name,
    #     tags={
    #         'training_date': context['ds'],
    #         'trained_by': 'airflow',
    #         'test_accuracy': test_accuracy
    #     }
    # )

    # TODO: Transition to Staging
    # client = mlflow.tracking.MlflowClient()
    # client.transition_model_version_stage(
    #     name=model_name,
    #     version=model_version.version,
    #     stage="Staging"
    # )

    logging.info(f"Model registered and transitioned to Staging")

    pass


def send_success_notification(**context):
    """Send success notification with training summary."""
    ti = context['task_instance']
    test_accuracy = ti.xcom_pull(task_ids='evaluate_model', key='test_accuracy')

    # TODO: Format notification message
    message = f"""
    ML Training Pipeline Completed Successfully

    Execution Date: {context['ds']}
    Test Accuracy: {test_accuracy:.4f}

    MLflow UI: {Variable.get("mlflow_tracking_uri", "http://mlflow:5000")}
    """

    logging.info(message)
    # TODO: Send to Slack/email
    pass


# Define tasks
with dag:
    start = DummyOperator(task_id='start')

    fetch_data_task = PythonOperator(
        task_id='fetch_data',
        python_callable=fetch_data,
        provide_context=True,
    )

    validate_data_task = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data,
        provide_context=True,
    )

    preprocess_data_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data,
        provide_context=True,
    )

    train_model_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
        provide_context=True,
    )

    evaluate_model_task = PythonOperator(
        task_id='evaluate_model',
        python_callable=evaluate_model,
        provide_context=True,
    )

    check_performance = BranchPythonOperator(
        task_id='check_model_performance',
        python_callable=check_model_performance,
        provide_context=True,
    )

    register_model_task = PythonOperator(
        task_id='register_model',
        python_callable=register_model,
        provide_context=True,
    )

    skip_registration = DummyOperator(task_id='skip_registration')

    notify_success = PythonOperator(
        task_id='send_success_notification',
        python_callable=send_success_notification,
        provide_context=True,
        trigger_rule='none_failed',  # Run if no task failed
    )

    end = DummyOperator(task_id='end', trigger_rule='none_failed')

    # TODO: Define task dependencies
    # start >> fetch_data_task >> validate_data_task >> preprocess_data_task
    # preprocess_data_task >> train_model_task >> evaluate_model_task
    # evaluate_model_task >> check_performance
    # check_performance >> [register_model_task, skip_registration]
    # [register_model_task, skip_registration] >> notify_success >> end
```

### Airflow Configuration

```yaml
# docker-compose.yml for Airflow
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data

  # TODO: Add Redis for CeleryExecutor (if needed)

  airflow-webserver:
    image: apache/airflow:2.7.0-python3.10
    depends_on:
      - postgres
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
      AIRFLOW__CORE__FERNET_KEY: ''
      AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'true'
      AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
      AIRFLOW__WEBSERVER__EXPOSE_CONFIG: 'true'
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    ports:
      - "8080:8080"
    command: webserver

  airflow-scheduler:
    image: apache/airflow:2.7.0-python3.10
    depends_on:
      - postgres
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    command: scheduler

  # TODO: Add airflow-worker for CeleryExecutor

volumes:
  postgres-db-volume:
```

### Validation

Test your DAG:
```bash
# Initialize Airflow database
docker-compose run airflow-webserver airflow db init

# Create admin user
docker-compose run airflow-webserver airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

# Start Airflow
docker-compose up -d

# Test DAG syntax
docker-compose run airflow-webserver airflow dags test ml_training_pipeline 2024-01-01

# Trigger DAG manually
docker-compose run airflow-webserver airflow dags trigger ml_training_pipeline
```

### Success Criteria

- [ ] Airflow DAG parses without errors
- [ ] All tasks execute in correct order
- [ ] XCom is used to pass data between tasks
- [ ] Branching logic works (register vs skip)
- [ ] MLflow integration works correctly
- [ ] Retries are configured and work
- [ ] Email/notifications are sent on failure
- [ ] DAG completes successfully end-to-end

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **XCom**: Use `ti.xcom_push(key='name', value=data)` and `ti.xcom_pull(task_ids='task', key='name')`
2. **Branching**: BranchPythonOperator returns task_id to execute next
3. **Trigger Rules**: Use `trigger_rule='none_failed'` for tasks that should run even if upstream was skipped
4. **Variables**: Store config in Airflow Variables UI or use `Variable.set()` / `Variable.get()`
5. **Dependencies**: Use `>>` for linear, `[task1, task2] >> task3` for multiple upstream
6. **Sensors**: Use `ExternalTaskSensor` to wait for other DAGs

</details>

---

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

## Exercise 3: Workflow Error Handling & Retry Logic (75 minutes)

**Objective**: Implement robust error handling, retry logic, and failure recovery in ML pipelines.

### Background

Production pipelines must handle:
- Transient failures (network, API limits)
- Data quality issues
- Resource constraints
- Downstream service failures
- Partial failures requiring cleanup

### Tasks

1. **Implement retry logic with exponential backoff**
2. **Add error handling for different failure types**
3. **Create failure recovery mechanisms**
4. **Implement circuit breakers**
5. **Add comprehensive logging and alerting**

### Starter Code

```python
# robust_pipeline.py
"""
ML pipeline with comprehensive error handling and retry logic.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowException, AirflowSkipException
from airflow.utils.trigger_rule import TriggerRule
import logging
import time
import requests
from functools import wraps
from typing import Callable, Any
import random

# Custom exceptions
class DataQualityException(AirflowException):
    """Raised when data quality checks fail."""
    pass

class ExternalServiceException(AirflowException):
    """Raised when external service is unavailable."""
    pass

class RetryableException(AirflowException):
    """Raised for errors that should be retried."""
    pass


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    Decorator for retry logic with exponential backoff.

    TODO: Implement retry decorator
    - Catch specified exceptions
    - Retry with exponential backoff
    - Log retry attempts
    - Raise after max_retries exceeded
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay

            for attempt in range(max_retries + 1):
                try:
                    # TODO: Execute function
                    result = func(*args, **kwargs)

                    if attempt > 0:
                        logging.info(f"{func.__name__} succeeded after {attempt} retries")

                    return result

                except exceptions as e:
                    if attempt == max_retries:
                        logging.error(f"{func.__name__} failed after {max_retries} retries: {e}")
                        raise

                    # TODO: Calculate next delay with jitter
                    jitter = random.uniform(0, delay * 0.1)
                    sleep_time = delay + jitter

                    logging.warning(
                        f"{func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {e}. "
                        f"Retrying in {sleep_time:.2f}s..."
                    )

                    time.sleep(sleep_time)
                    delay *= backoff_factor

        return wrapper
    return decorator


class CircuitBreaker:
    """
    Circuit breaker pattern for external service calls.

    TODO: Implement circuit breaker
    - Track failure rate
    - Open circuit after threshold
    - Half-open state for recovery testing
    - Close circuit when recovered
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: type = Exception
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection.

        TODO: Implement circuit breaker logic
        """

        # TODO: Check if circuit is OPEN
        if self.state == 'OPEN':
            if self._should_attempt_reset():
                self.state = 'HALF_OPEN'
                logging.info("Circuit breaker entering HALF_OPEN state")
            else:
                raise ExternalServiceException(
                    f"Circuit breaker is OPEN. Service unavailable."
                )

        try:
            # TODO: Execute function
            result = func(*args, **kwargs)

            # TODO: On success in HALF_OPEN, close circuit
            if self.state == 'HALF_OPEN':
                self._reset()
                logging.info("Circuit breaker CLOSED - service recovered")

            return result

        except self.expected_exception as e:
            # TODO: Record failure
            self._record_failure()

            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
                logging.error(
                    f"Circuit breaker OPENED after {self.failure_count} failures"
                )

            raise

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt recovery."""
        # TODO: Implement timeout check
        if self.last_failure_time is None:
            return True

        return (time.time() - self.last_failure_time) >= self.recovery_timeout

    def _record_failure(self):
        """Record a failure."""
        self.failure_count += 1
        self.last_failure_time = time.time()

    def _reset(self):
        """Reset circuit breaker to closed state."""
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'


# Example usage in Airflow tasks
@retry_with_backoff(
    max_retries=3,
    initial_delay=2.0,
    backoff_factor=2.0,
    exceptions=(requests.exceptions.RequestException, RetryableException)
)
def fetch_data_with_retry(**context):
    """
    Fetch data with automatic retry on transient failures.

    TODO: Implement data fetching with error handling
    """
    logging.info("Fetching data from external API")

    # TODO: Make API request
    # response = requests.get('https://api.example.com/data', timeout=30)

    # TODO: Handle different status codes
    # if response.status_code == 429:  # Rate limited
    #     raise RetryableException("Rate limited - will retry")
    # elif response.status_code >= 500:  # Server error
    #     raise RetryableException(f"Server error {response.status_code} - will retry")
    # elif response.status_code != 200:
    #     raise AirflowException(f"Failed to fetch data: {response.status_code}")

    # TODO: Parse and validate response
    # data = response.json()
    # if not data:
    #     raise DataQualityException("Empty response received")

    # return data
    pass


def validate_data_quality(**context):
    """
    Validate data quality with specific error handling.

    TODO: Implement data quality checks
    - Check for missing values
    - Validate schema
    - Check distributions
    - Raise appropriate exceptions
    """
    ti = context['task_instance']
    data = ti.xcom_pull(task_ids='fetch_data_with_retry')

    try:
        # TODO: Validation logic
        # if data is None:
        #     raise DataQualityException("No data received")

        # TODO: Check missing values
        # missing_pct = calculate_missing_percentage(data)
        # if missing_pct > 0.3:  # 30% threshold
        #     raise DataQualityException(f"Too many missing values: {missing_pct:.1%}")

        # TODO: Schema validation
        # if not validate_schema(data):
        #     raise DataQualityException("Schema validation failed")

        logging.info("Data quality validation passed")

    except DataQualityException as e:
        # TODO: Log data quality issue
        logging.error(f"Data quality check failed: {e}")

        # TODO: Send alert
        # send_alert(f"Data quality issue: {e}")

        # Re-raise to fail task
        raise


def cleanup_on_failure(**context):
    """
    Cleanup task that runs on pipeline failure.

    TODO: Implement cleanup logic
    - Remove temporary files
    - Release resources
    - Rollback partial changes
    - Send failure notifications
    """
    logging.info("Running failure cleanup")

    # TODO: Get failed task details
    # failed_task_id = context['task_instance'].task_id
    # execution_date = context['execution_date']

    # TODO: Cleanup temporary files
    # cleanup_temp_files(execution_date)

    # TODO: Release resources
    # release_db_connections()

    # TODO: Send detailed failure notification
    # send_failure_alert(
    #     task=failed_task_id,
    #     execution_date=execution_date,
    #     error=context.get('exception')
    # )

    pass


def graceful_degradation(**context):
    """
    Implement graceful degradation when optimal path fails.

    TODO: Implement fallback logic
    - Try primary data source
    - Fall back to secondary source if primary fails
    - Use cached data as last resort
    """
    logging.info("Attempting primary data source")

    try:
        # TODO: Try primary source
        # data = fetch_from_primary_source()
        # return data
        pass

    except Exception as e:
        logging.warning(f"Primary source failed: {e}. Trying secondary source...")

        try:
            # TODO: Try secondary source
            # data = fetch_from_secondary_source()
            # logging.info("Successfully retrieved data from secondary source")
            # return data
            pass

        except Exception as e2:
            logging.error(f"Secondary source also failed: {e2}. Using cached data...")

            # TODO: Use cached data
            # data = load_cached_data()
            # if data is not None:
            #     logging.warning("Using cached data - may be stale")
            #     return data

            # If all fail, raise
            raise AirflowException("All data sources failed")


# DAG definition
default_args = {
    'owner': 'ml-team',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(minutes=30),
    'on_failure_callback': lambda context: logging.error(f"Task failed: {context['task_instance'].task_id}"),
}

dag = DAG(
    'robust_ml_pipeline',
    default_args=default_args,
    description='ML pipeline with robust error handling',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['ml', 'robust', 'production'],
)

with dag:
    # Tasks with different error handling strategies
    fetch_data = PythonOperator(
        task_id='fetch_data_with_retry',
        python_callable=fetch_data_with_retry,
        provide_context=True,
    )

    validate_data = PythonOperator(
        task_id='validate_data_quality',
        python_callable=validate_data_quality,
        provide_context=True,
    )

    graceful_task = PythonOperator(
        task_id='graceful_degradation',
        python_callable=graceful_degradation,
        provide_context=True,
    )

    cleanup = PythonOperator(
        task_id='cleanup_on_failure',
        python_callable=cleanup_on_failure,
        provide_context=True,
        trigger_rule=TriggerRule.ONE_FAILED,  # Run only if upstream failed
    )

    # Define dependencies
    fetch_data >> validate_data >> graceful_task
    [fetch_data, validate_data, graceful_task] >> cleanup
```

### Validation

Test error scenarios:
```python
# test_error_handling.py
import pytest
from unittest.mock import Mock, patch
import requests

def test_retry_with_backoff_success_after_retries():
    """Test that retry succeeds after transient failures."""
    # TODO: Implement test
    pass

def test_retry_with_backoff_max_retries_exceeded():
    """Test that function raises after max retries."""
    # TODO: Implement test
    pass

def test_circuit_breaker_opens_after_threshold():
    """Test circuit breaker opens after failure threshold."""
    # TODO: Implement test
    pass

def test_circuit_breaker_half_open_recovery():
    """Test circuit breaker recovery mechanism."""
    # TODO: Implement test
    pass
```

### Success Criteria

- [ ] Retry logic works with exponential backoff
- [ ] Circuit breaker opens/closes correctly
- [ ] Different exception types handled appropriately
- [ ] Cleanup runs on failure
- [ ] Graceful degradation works
- [ ] Comprehensive logging implemented
- [ ] Alerts sent on failures

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Retries**: Use `time.sleep()` with exponential backoff, add jitter to prevent thundering herd
2. **Circuit Breaker**: Track state (CLOSED/OPEN/HALF_OPEN), use timestamps for recovery
3. **Exception Types**: Create custom exceptions for different failure modes
4. **Cleanup**: Use `trigger_rule=TriggerRule.ONE_FAILED` for cleanup tasks
5. **Callbacks**: Use `on_failure_callback` in default_args for centralized failure handling
6. **Logging**: Use structured logging with context (task_id, execution_date)

</details>

---

## Exercise 4: MLflow Integration in Pipelines (75 minutes)

**Objective**: Integrate MLflow comprehensively into orchestrated pipelines for experiment tracking, model registry, and artifact management.

### Background

MLflow integration in pipelines enables:
- Automatic experiment tracking
- Model versioning and lineage
- Artifact storage and retrieval
- Performance comparison across runs
- Reproducible pipeline executions

### Tasks

1. **Create pipeline with full MLflow tracking**
2. **Implement model comparison logic**
3. **Automate model promotion based on metrics**
4. **Track pipeline lineage**
5. **Generate comparison reports**

### Starter Code

```python
# mlflow_integrated_pipeline.py
"""
ML pipeline with comprehensive MLflow integration.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.models import Variable
import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from typing import Dict, List, Tuple
import logging
import json


class MLflowPipelineTracker:
    """Utility class for MLflow integration in pipelines."""

    def __init__(self, tracking_uri: str, experiment_name: str):
        """
        Initialize MLflow tracker.

        TODO: Set up MLflow client and experiment
        """
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)
        self.client = MlflowClient(tracking_uri=tracking_uri)
        self.experiment = mlflow.get_experiment_by_name(experiment_name)

    def start_pipeline_run(self, pipeline_id: str, run_date: str, **kwargs) -> str:
        """
        Start parent run for entire pipeline.

        TODO: Create parent run for pipeline tracking
        """
        tags = {
            'pipeline_id': pipeline_id,
            'run_date': run_date,
            'pipeline_type': 'airflow',
            **kwargs
        }

        # TODO: Start run
        run = self.client.create_run(
            experiment_id=self.experiment.experiment_id,
            tags=tags,
            run_name=f"pipeline_{run_date}"
        )

        return run.info.run_id

    def log_data_stats(self, run_id: str, data: pd.DataFrame, stage: str):
        """
        Log dataset statistics to MLflow.

        TODO: Log comprehensive data stats
        """
        with mlflow.start_run(run_id=run_id):
            # TODO: Log basic stats
            mlflow.log_param(f'{stage}_num_samples', data.shape[0])
            mlflow.log_param(f'{stage}_num_features', data.shape[1])

            # TODO: Log feature statistics
            # for col in data.select_dtypes(include=[np.number]).columns:
            #     mlflow.log_metric(f'{stage}_{col}_mean', data[col].mean())
            #     mlflow.log_metric(f'{stage}_{col}_std', data[col].std())

    def log_model_comparison(
        self,
        run_id: str,
        models: Dict[str, any],
        X_val: pd.DataFrame,
        y_val: pd.Series
    ) -> Tuple[str, float]:
        """
        Train multiple models and compare performance.

        TODO: Implement model comparison
        - Train each model
        - Log metrics
        - Return best model
        """
        best_model_name = None
        best_score = 0.0
        results = {}

        with mlflow.start_run(run_id=run_id):
            for model_name, model in models.items():
                # TODO: Create child run for each model
                with mlflow.start_run(run_name=f"{model_name}_training", nested=True):

                    # TODO: Log model parameters
                    mlflow.log_params(model.get_params())

                    # TODO: Train model
                    # model.fit(X_train, y_train)

                    # TODO: Evaluate
                    # y_pred = model.predict(X_val)
                    # accuracy = accuracy_score(y_val, y_pred)
                    # precision = precision_score(y_val, y_pred, average='weighted')
                    # recall = recall_score(y_val, y_pred, average='weighted')
                    # f1 = f1_score(y_val, y_pred, average='weighted')

                    # TODO: Log metrics
                    # mlflow.log_metric('accuracy', accuracy)
                    # mlflow.log_metric('precision', precision)
                    # mlflow.log_metric('recall', recall)
                    # mlflow.log_metric('f1', f1)

                    # TODO: Log model
                    # mlflow.sklearn.log_model(model, f"{model_name}_model")

                    # TODO: Track best model
                    # results[model_name] = accuracy
                    # if accuracy > best_score:
                    #     best_score = accuracy
                    #     best_model_name = model_name

        return best_model_name, best_score

    def compare_with_production(
        self,
        new_run_id: str,
        model_name: str,
        metrics: List[str] = ['accuracy', 'f1']
    ) -> Dict[str, float]:
        """
        Compare new model with current production model.

        TODO: Implement production comparison
        """
        # TODO: Get current production model version
        prod_versions = self.client.get_latest_versions(
            name=model_name,
            stages=["Production"]
        )

        if not prod_versions:
            logging.info("No production model found - new model will be promoted")
            return {'improvement': float('inf')}

        prod_version = prod_versions[0]
        prod_run_id = prod_version.run_id

        # TODO: Get metrics from both runs
        new_metrics = self.client.get_run(new_run_id).data.metrics
        prod_metrics = self.client.get_run(prod_run_id).data.metrics

        # TODO: Calculate improvements
        improvements = {}
        for metric in metrics:
            new_value = new_metrics.get(metric, 0)
            prod_value = prod_metrics.get(metric, 0)
            improvement = ((new_value - prod_value) / prod_value) * 100 if prod_value > 0 else 0
            improvements[metric] = improvement

        return improvements

    def promote_model(
        self,
        run_id: str,
        model_name: str,
        model_path: str,
        metrics: Dict[str, float],
        min_improvement: float = 2.0
    ) -> bool:
        """
        Promote model to production if it meets criteria.

        TODO: Implement model promotion logic
        """
        # TODO: Get current production model
        improvements = self.compare_with_production(run_id, model_name)

        # TODO: Check if improvement meets threshold
        avg_improvement = np.mean(list(improvements.values()))

        if avg_improvement < min_improvement:
            logging.info(
                f"Model improvement ({avg_improvement:.2f}%) below threshold ({min_improvement}%)"
            )
            return False

        # TODO: Register model
        with mlflow.start_run(run_id=run_id):
            model_uri = f"runs:/{run_id}/{model_path}"
            model_version = mlflow.register_model(
                model_uri=model_uri,
                name=model_name,
                tags={
                    'trained_by': 'airflow_pipeline',
                    'promoted_date': datetime.now().isoformat(),
                    **{f'improvement_{k}': f"{v:.2f}%" for k, v in improvements.items()}
                }
            )

        # TODO: Archive current production model
        prod_versions = self.client.get_latest_versions(name=model_name, stages=["Production"])
        for version in prod_versions:
            self.client.transition_model_version_stage(
                name=model_name,
                version=version.version,
                stage="Archived"
            )

        # TODO: Promote new model to production
        self.client.transition_model_version_stage(
            name=model_name,
            version=model_version.version,
            stage="Production"
        )

        logging.info(
            f"Model promoted to production (v{model_version.version}). "
            f"Average improvement: {avg_improvement:.2f}%"
        )

        return True


# Pipeline tasks
def initialize_pipeline(**context):
    """
    Initialize pipeline run in MLflow.

    TODO: Create parent run and store run_id
    """
    tracker = MLflowPipelineTracker(
        tracking_uri=Variable.get("mlflow_tracking_uri"),
        experiment_name="automated_ml_pipeline"
    )

    pipeline_run_id = tracker.start_pipeline_run(
        pipeline_id=context['dag'].dag_id,
        run_date=context['ds'],
        execution_date=str(context['execution_date'])
    )

    # TODO: Store run_id in XCom for downstream tasks
    context['task_instance'].xcom_push(key='pipeline_run_id', value=pipeline_run_id)

    logging.info(f"Initialized pipeline run: {pipeline_run_id}")


def train_and_compare_models(**context):
    """
    Train multiple models and compare performance.

    TODO: Implement multi-model training with comparison
    """
    ti = context['task_instance']
    pipeline_run_id = ti.xcom_pull(task_ids='initialize_pipeline', key='pipeline_run_id')

    tracker = MLflowPipelineTracker(
        tracking_uri=Variable.get("mlflow_tracking_uri"),
        experiment_name="automated_ml_pipeline"
    )

    # TODO: Load data
    # X_train, X_val, y_train, y_val = load_data()

    # TODO: Define models to compare
    models = {
        'random_forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
        'gradient_boosting': GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42),
    }

    # TODO: Train and compare
    # best_model_name, best_score = tracker.log_model_comparison(
    #     run_id=pipeline_run_id,
    #     models=models,
    #     X_val=X_val,
    #     y_val=y_val
    # )

    # TODO: Push results to XCom
    # ti.xcom_push(key='best_model_name', value=best_model_name)
    # ti.xcom_push(key='best_score', value=best_score)

    pass


def decide_promotion(**context):
    """
    Decide whether to promote model based on performance.

    TODO: Implement promotion decision logic
    """
    ti = context['task_instance']
    best_score = ti.xcom_pull(task_ids='train_and_compare_models', key='best_score')

    # TODO: Get threshold from Variables
    threshold = float(Variable.get("promotion_threshold", "0.85"))

    if best_score >= threshold:
        logging.info(f"Model score {best_score:.4f} meets threshold {threshold}")
        return 'promote_model'
    else:
        logging.warning(f"Model score {best_score:.4f} below threshold {threshold}")
        return 'skip_promotion'


def promote_best_model(**context):
    """
    Promote best model to production in MLflow registry.

    TODO: Implement model promotion
    """
    ti = context['task_instance']
    pipeline_run_id = ti.xcom_pull(task_ids='initialize_pipeline', key='pipeline_run_id')
    best_model_name = ti.xcom_pull(task_ids='train_and_compare_models', key='best_model_name')

    tracker = MLflowPipelineTracker(
        tracking_uri=Variable.get("mlflow_tracking_uri"),
        experiment_name="automated_ml_pipeline"
    )

    # TODO: Get metrics and promote
    # success = tracker.promote_model(
    #     run_id=pipeline_run_id,
    #     model_name="production_classifier",
    #     model_path=f"{best_model_name}_model",
    #     metrics={'accuracy': best_score},
    #     min_improvement=2.0
    # )

    # if success:
    #     logging.info("Model successfully promoted to production")
    # else:
    #     logging.info("Model not promoted - insufficient improvement")

    pass


# Define DAG
default_args = {
    'owner': 'ml-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'mlflow_integrated_pipeline',
    default_args=default_args,
    description='ML pipeline with comprehensive MLflow integration',
    schedule_interval='@weekly',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['ml', 'mlflow', 'production'],
)

with dag:
    init = PythonOperator(
        task_id='initialize_pipeline',
        python_callable=initialize_pipeline,
        provide_context=True,
    )

    train_compare = PythonOperator(
        task_id='train_and_compare_models',
        python_callable=train_and_compare_models,
        provide_context=True,
    )

    decide = BranchPythonOperator(
        task_id='decide_promotion',
        python_callable=decide_promotion,
        provide_context=True,
    )

    promote = PythonOperator(
        task_id='promote_model',
        python_callable=promote_best_model,
        provide_context=True,
    )

    skip = DummyOperator(task_id='skip_promotion')

    # Dependencies
    init >> train_compare >> decide >> [promote, skip]
```

### Success Criteria

- [ ] Pipeline run tracked as parent in MLflow
- [ ] Each model logged as nested run
- [ ] Model comparison generates correct metrics
- [ ] Production comparison works
- [ ] Model promotion based on improvement threshold
- [ ] Complete lineage tracked in MLflow

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Parent Runs**: Use `mlflow.start_run()` at pipeline level, nested runs for tasks
2. **Comparison**: Query MLflow API to get production model metrics
3. **Promotion**: Use `MlflowClient().transition_model_version_stage()`
4. **Lineage**: Use tags to link pipeline runs to models
5. **XCom**: Pass run_id through XCom for consistent tracking

</details>

---

## Exercise 5: Production ML Pipeline (120 minutes)

**Objective**: Design and implement a production-grade end-to-end ML pipeline incorporating all best practices.

### Requirements

Build a complete pipeline that includes:

1. **Data Pipeline**:
   - Data ingestion from multiple sources
   - Data quality validation
   - Feature engineering
   - Data versioning

2. **Training Pipeline**:
   - Hyperparameter optimization
   - Multi-model training and comparison
   - Cross-validation
   - Model evaluation

3. **Deployment Pipeline**:
   - Model registration
   - A/B testing setup
   - Canary deployment
   - Rollback capability

4. **Monitoring Pipeline**:
   - Drift detection
   - Performance monitoring
   - Alert generation
   - Retraining triggers

### Success Criteria

- [ ] All pipeline stages implemented
- [ ] Error handling and retries configured
- [ ] MLflow integration complete
- [ ] Monitoring and alerting working
- [ ] Pipeline is parameterized and configurable
- [ ] Documentation complete
- [ ] Tests passing

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Modularity**: Create reusable components/operators
2. **Configuration**: Use Airflow Variables and Connections
3. **Testing**: Write unit tests for each task
4. **Monitoring**: Integrate with existing monitoring stack
5. **Documentation**: Use docstrings and README
6. **CI/CD**: Integrate pipeline with version control

</details>

---

## Submission Guidelines

For each exercise, submit:
1. **Code**: All implementation files with TODOs completed
2. **Documentation**: Architecture diagrams and design decisions
3. **Test Results**: Screenshots of successful pipeline runs
4. **Metrics**: Performance metrics from MLflow
5. **Reflection**: Challenges faced and solutions implemented

**Estimated Total Time**: 6-9 hours
**Difficulty**: Advanced

Good luck!
