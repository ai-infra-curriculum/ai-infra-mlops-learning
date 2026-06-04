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
