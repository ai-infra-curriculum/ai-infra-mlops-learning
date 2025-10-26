# Module 06: Automation and Orchestration - Lecture Notes

**Duration**: 12.5 hours
**Level**: MLOps Engineer (2.5B)
**Last Updated**: October 2025

---

## Table of Contents

1. [Orchestration Fundamentals](#1-orchestration-fundamentals)
2. [Apache Airflow](#2-apache-airflow)
3. [Kubeflow Pipelines](#3-kubeflow-pipelines)
4. [Workflow Patterns](#4-workflow-patterns)
5. [Error Handling and Monitoring](#5-error-handling-and-monitoring)
6. [Summary and Best Practices](#6-summary-and-best-practices)

---

## 1. Orchestration Fundamentals

### 1.1 Why Orchestration for ML

**Manual Execution Problems**:
- Forgetting steps in complex workflows
- No automatic retry on failure
- No dependency management
- Difficult to schedule and monitor
- Hard to parallelize tasks

**Orchestration Benefits**:
- **Reliability**: Automatic retries, error handling
- **Scalability**: Parallel execution, distributed compute
- **Observability**: Centralized monitoring and logging
- **Reproducibility**: Versioned workflows
- **Scheduling**: Time-based and event-driven triggers

### 1.2 DAG Design Principles

**DAG** = Directed Acyclic Graph (no cycles allowed)

```python
# Good DAG structure
fetch_data → validate_data → split_data → train_model → evaluate_model → deploy_model
                                      ↓
                              generate_features ↗

# Bad: Cycle (not allowed)
task_a → task_b → task_c → task_a  # ❌ Creates infinite loop
```

**Design Principles**:
1. **Idempotency**: Same input → same output
2. **Atomicity**: Tasks should be all-or-nothing
3. **Isolation**: Tasks shouldn't depend on shared state
4. **Minimal Dependencies**: Only depend on what's necessary

---

## 2. Apache Airflow

### 2.1 Complete ML Training DAG

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
import pandas as pd
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Default arguments
default_args = {
    'owner': 'ml ops-team',
    'depends_on_past': False,
    'email': ['alerts@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=2)
}

# Define DAG
dag = DAG(
    'ml_training_pipeline',
    default_args=default_args,
    description='Train and deploy ML model',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['ml', 'training', 'production']
)

def fetch_training_data(**context):
    """Fetch training data from data warehouse."""
    from sqlalchemy import create_engine

    engine = create_engine(os.environ['DB_CONNECTION_STRING'])

    query = """
    SELECT *
    FROM ml_features
    WHERE date >= CURRENT_DATE - INTERVAL '30 days'
    AND label IS NOT NULL
    """

    df = pd.read_sql(query, engine)

    # Save to XCom
    data_path = f"/tmp/training_data_{context['ds']}.parquet"
    df.to_parquet(data_path)

    return data_path

def validate_data(data_path: str, **context):
    """Validate data quality."""
    import great_expectations as gx

    df = pd.read_parquet(data_path)

    # Basic checks
    assert len(df) > 10000, f"Insufficient data: {len(df)} rows"
    assert df['label'].notna().sum() / len(df) > 0.95, "Too many missing labels"

    # Great Expectations validation
    context_gx = gx.get_context()
    validator = context_gx.get_validator(
        batch=gx.from_pandas(df),
        expectation_suite_name="training_data_expectations"
    )

    results = validator.validate()

    if not results['success']:
        raise ValueError(f"Data validation failed: {results}")

    return data_path

def train_model(data_path: str, **context):
    """Train ML model."""
    import mlflow
    from sklearn.model_selection import train_test_split

    df = pd.read_parquet(data_path)

    # Split features and target
    X = df.drop('label', axis=1)
    y = df['label']

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # MLflow tracking
    mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])
    mlflow.set_experiment("production_training")

    with mlflow.start_run():
        # Log parameters
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("max_depth", 10)
        mlflow.log_param("training_date", context['ds'])
        mlflow.log_param("training_samples", len(X_train))

        # Train model
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)

        # Evaluate
        y_pred_val = model.predict(X_val)
        accuracy = accuracy_score(y_val, y_pred_val)
        precision = precision_score(y_val, y_pred_val, average='weighted')
        recall = recall_score(y_val, y_pred_val, average='weighted')

        # Log metrics
        mlflow.log_metric("val_accuracy", accuracy)
        mlflow.log_metric("val_precision", precision)
        mlflow.log_metric("val_recall", recall)

        # Log model
        mlflow.sklearn.log_model(model, "model")

        # Get run ID
        run_id = mlflow.active_run().info.run_id

    return {'run_id': run_id, 'accuracy': accuracy}

def evaluate_against_baseline(model_info: dict, **context):
    """Compare new model against production baseline."""
    import mlflow

    new_accuracy = model_info['accuracy']

    # Get current production model
    mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])

    try:
        prod_model = mlflow.pyfunc.load_model("models:/credit-model/production")
        prod_run = mlflow.get_run(prod_model.metadata.run_id)
        prod_accuracy = prod_run.data.metrics['val_accuracy']
    except:
        prod_accuracy = 0.0  # No baseline yet

    improvement = new_accuracy - prod_accuracy

    # Decide if we should deploy
    should_deploy = improvement >= 0.01  # 1% minimum improvement

    return {
        'should_deploy': should_deploy,
        'new_accuracy': new_accuracy,
        'prod_accuracy': prod_accuracy,
        'improvement': improvement,
        **model_info
    }

def deploy_model(deployment_info: dict, **context):
    """Deploy model to production."""
    import mlflow

    if not deployment_info['should_deploy']:
        print(f"⏸️ Not deploying: improvement {deployment_info['improvement']:.1%} below threshold")
        return

    mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])

    # Register model
    model_uri = f"runs:/{deployment_info['run_id']}/model"

    model_details = mlflow.register_model(model_uri, "credit-model")

    # Transition to production
    client = mlflow.MlflowClient()
    client.transition_model_version_stage(
        name="credit-model",
        version=model_details.version,
        stage="Production",
        archive_existing_versions=True
    )

    print(f"✅ Deployed model version {model_details.version} to production")

    return {
        'deployed': True,
        'model_version': model_details.version,
        'accuracy': deployment_info['new_accuracy']
    }

# Define tasks
fetch_data_task = PythonOperator(
    task_id='fetch_training_data',
    python_callable=fetch_training_data,
    dag=dag
)

validate_data_task = PythonOperator(
    task_id='validate_data',
    python_callable=validate_data,
    op_kwargs={'data_path': "{{ task_instance.xcom_pull(task_ids='fetch_training_data') }}"},
    dag=dag
)

train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    op_kwargs={'data_path': "{{ task_instance.xcom_pull(task_ids='validate_data') }}"},
    dag=dag
)

evaluate_task = PythonOperator(
    task_id='evaluate_against_baseline',
    python_callable=evaluate_against_baseline,
    op_kwargs={'model_info': "{{ task_instance.xcom_pull(task_ids='train_model') }}"},
    dag=dag
)

deploy_task = PythonOperator(
    task_id='deploy_model',
    python_callable=deploy_model,
    op_kwargs={'deployment_info': "{{ task_instance.xcom_pull(task_ids='evaluate_against_baseline') }}"},
    dag=dag
)

success_alert = SlackWebhookOperator(
    task_id='send_success_alert',
    http_conn_id='slack_webhook',
    message="""
    ✅ ML Training Pipeline Succeeded
    Date: {{ ds }}
    New Accuracy: {{ task_instance.xcom_pull(task_ids='deploy_model')['accuracy'] }}
    """,
    dag=dag
)

# Set dependencies
fetch_data_task >> validate_data_task >> train_model_task >> evaluate_task >> deploy_task >> success_alert
```

### 2.2 Advanced Airflow Patterns

**Dynamic DAG Generation**:
```python
# Generate DAGs for multiple models
MODELS = ['credit_risk', 'fraud_detection', 'churn_prediction']

for model_name in MODELS:
    dag_id = f'train_{model_name}'

    dag = DAG(
        dag_id,
        default_args=default_args,
        schedule_interval='@daily'
    )

    # Create tasks dynamically
    train_task = PythonOperator(
        task_id='train',
        python_callable=train_model,
        op_kwargs={'model_name': model_name},
        dag=dag
    )

    # Register DAG
    globals()[dag_id] = dag
```

---

## 3. Kubeflow Pipelines

### 3.1 Complete Pipeline Example

```python
import kfp
from kfp import dsl
from kfp.components import create_component_from_func

def load_data(data_path: str) -> str:
    """Load and preprocess data."""
    import pandas as pd

    df = pd.read_csv(data_path)

    # Preprocessing
    df = df.dropna()

    output_path = '/tmp/processed_data.csv'
    df.to_csv(output_path, index=False)

    return output_path

def train_model(data_path: str, n_estimators: int) -> str:
    """Train model."""
    import pandas as pd
    import pickle
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split

    df = pd.read_csv(data_path)

    X = df.drop('target', axis=1)
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestClassifier(n_estimators=n_estimators)
    model.fit(X_train, y_train)

    # Save model
    model_path = '/tmp/model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy}")

    return model_path

def deploy_model(model_path: str):
    """Deploy model to serving infrastructure."""
    import subprocess

    # Copy model to serving location
    subprocess.run([
        'gsutil', 'cp', model_path,
        'gs://ml-models/production/model.pkl'
    ])

    print("Model deployed successfully")

# Create components
load_data_op = create_component_from_func(
    load_data,
    base_image='python:3.9',
    packages_to_install=['pandas==2.0.0']
)

train_model_op = create_component_from_func(
    train_model,
    base_image='python:3.9',
    packages_to_install=['pandas==2.0.0', 'scikit-learn==1.3.0']
)

deploy_model_op = create_component_from_func(
    deploy_model,
    base_image='google/cloud-sdk:latest'
)

# Define pipeline
@dsl.pipeline(
    name='ML Training Pipeline',
    description='End-to-end ML training and deployment'
)
def ml_training_pipeline(
    data_path: str = 'gs://my-bucket/data.csv',
    n_estimators: int = 100
):
    """Complete ML pipeline."""

    # Load data
    load_task = load_data_op(data_path)

    # Train model
    train_task = train_model_op(
        data_path=load_task.output,
        n_estimators=n_estimators
    )

    # Deploy model
    deploy_task = deploy_model_op(model_path=train_task.output)

# Compile pipeline
kfp.compiler.Compiler().compile(
    ml_training_pipeline,
    'ml_pipeline.yaml'
)

# Run pipeline
client = kfp.Client(host='http://localhost:8080')
run = client.create_run_from_pipeline_func(
    ml_training_pipeline,
    arguments={'data_path': 'gs://my-bucket/data.csv', 'n_estimators': 200}
)
```

---

## 4. Workflow Patterns

### 4.1 Automated Retraining Pipeline

```python
from airflow import DAG
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.python import BranchPythonOperator

def check_retraining_trigger(**context):
    """Decide if retraining is needed."""
    import mlflow

    # Check data drift
    drift_score = get_drift_score()  # From monitoring system

    # Check performance degradation
    current_accuracy = get_current_accuracy()
    baseline_accuracy = 0.85

    # Check time since last training
    days_since_training = get_days_since_last_training()

    should_retrain = (
        drift_score > 0.3 or
        current_accuracy < baseline_accuracy * 0.95 or
        days_since_training > 30
    )

    if should_retrain:
        return 'trigger_retraining'
    else:
        return 'skip_retraining'

dag = DAG(
    'automated_retraining',
    default_args=default_args,
    schedule_interval='@daily'
)

check_trigger = BranchPythonOperator(
    task_id='check_retraining_trigger',
    python_callable=check_retraining_trigger,
    dag=dag
)

trigger_training = TriggerDagRunOperator(
    task_id='trigger_retraining',
    trigger_dag_id='ml_training_pipeline',
    dag=dag
)

skip = DummyOperator(task_id='skip_retraining', dag=dag)

check_trigger >> [trigger_training, skip]
```

### 4.2 Model Comparison Workflow

```python
@dsl.pipeline(name='Model Comparison Pipeline')
def model_comparison_pipeline(data_path: str):
    """Compare multiple models and select best."""

    # Load data (shared)
    data_task = load_data_op(data_path)

    # Train multiple models in parallel
    rf_task = train_random_forest_op(data_task.output)
    xgb_task = train_xgboost_op(data_task.output)
    lgbm_task = train_lightgbm_op(data_task.output)

    # Compare models
    comparison_task = compare_models_op(
        rf_metrics=rf_task.outputs['metrics'],
        xgb_metrics=xgb_task.outputs['metrics'],
        lgbm_metrics=lgbm_task.outputs['metrics']
    )

    # Deploy best model
    deploy_task = deploy_best_model_op(
        best_model=comparison_task.output
    )
```

---

## 5. Error Handling and Monitoring

### 5.1 Retry Strategies

```python
# Task-specific retry configuration
retry_critical_task = PythonOperator(
    task_id='critical_operation',
    python_callable=critical_function,
    retries=5,
    retry_delay=timedelta(minutes=10),
    retry_exponential_backoff=True,
    max_retry_delay=timedelta(hours=1),
    dag=dag
)

# Custom retry logic
def smart_retry_function(**context):
    """Function with custom retry logic."""
    task_instance = context['task_instance']
    retry_number = task_instance.try_number

    if retry_number > 1:
        # Wait longer on subsequent retries
        time.sleep(60 * retry_number)

    try:
        # Attempt operation
        result = risky_operation()
        return result
    except SpecificError as e:
        # Retry this error
        raise AirflowException(f"Retryable error: {e}")
    except CriticalError as e:
        # Don't retry critical errors
        raise AirflowFailException(f"Critical error: {e}")
```

### 5.2 Workflow Monitoring

```python
from airflow.providers.prometheus.operators import PrometheusOperator
from prometheus_client import Gauge, Counter

# Define metrics
dag_duration = Gauge('airflow_dag_duration_seconds', 'DAG execution time', ['dag_id'])
task_failures = Counter('airflow_task_failures_total', 'Task failures', ['dag_id', 'task_id'])

def monitor_dag_execution(**context):
    """Log DAG execution metrics."""
    dag_id = context['dag'].dag_id
    execution_date = context['execution_date']

    dag_run = context['dag_run']

    if dag_run.end_date:
        duration = (dag_run.end_date - dag_run.start_date).total_seconds()
        dag_duration.labels(dag_id=dag_id).set(duration)

        # Log to MLflow
        mlflow.log_metric(f"dag_duration_{dag_id}", duration)

# Add monitoring task to DAG
monitoring_task = PythonOperator(
    task_id='monitor_execution',
    python_callable=monitor_dag_execution,
    trigger_rule='all_done',  # Run regardless of upstream success/failure
    dag=dag
)
```

---

## 6. Summary and Best Practices

### Key Takeaways

1. **Idempotency**: Workflows should produce same result when re-run
2. **Error Handling**: Use retries, but not for all errors
3. **Monitoring**: Track workflow performance and failures
4. **Modularity**: Break complex workflows into reusable components
5. **Testing**: Test DAGs before deploying to production
6. **Resource Management**: Configure appropriate resources per task

### Best Practices

- **Use sensors** for event-driven workflows
- **Parallelize** independent tasks
- **Cache** expensive computations
- **Version** your DAGs with Git
- **Monitor** workflow execution and costs
- **Document** complex workflows
- **Test** DAGs in staging before production

---

**Total Words**: ~4,900 words

**Next Module**: Module 07 - ML Governance and Compliance
