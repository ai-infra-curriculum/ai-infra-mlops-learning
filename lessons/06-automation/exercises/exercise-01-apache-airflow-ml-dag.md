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
