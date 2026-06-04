# Module 02: Experiment Tracking & MLflow - Quiz

## Instructions

- **Total Questions**: 28
- **Time Limit**: 40 minutes
- **Passing Score**: 75% (21/28 correct)
- **Question Types**: Multiple choice, multiple select, code analysis

---

## Section 1: MLflow Fundamentals (Questions 1-8)

### Question 1
What are the four main components of MLflow?

A) Tracking, Models, Projects, Deploy
B) Tracking, Projects, Models, Registry
C) Tracking, Models, Serving, Registry
D) Experiments, Runs, Models, Registry

<details>
<summary>Answer</summary>

**B) Tracking, Projects, Models, Registry**

**Explanation**: The four core MLflow components are:
1. **Tracking**: Log parameters, metrics, and artifacts
2. **Projects**: Package ML code in reusable format
3. **Models**: Standard format for packaging models
4. **Registry**: Centralized model store with versioning and lifecycle management

</details>

---

### Question 2
What is the difference between an MLflow Experiment and a Run?

A) There is no difference; they are the same
B) An Experiment is a collection of Runs; a Run is a single execution
C) A Run contains multiple Experiments
D) Experiments are for training; Runs are for inference

<details>
<summary>Answer</summary>

**B) An Experiment is a collection of Runs; a Run is a single execution**

**Explanation**:
- **Experiment**: A group of related runs (e.g., "Customer Churn Model Development")
- **Run**: A single execution of ML code (one training session with specific hyperparameters)
- Hierarchy: Project → Experiment → Run
- Use experiments to organize related work

</details>

---

### Question 3
Analyze this code snippet:

```python
with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("loss", 0.15, step=10)
```

What is the purpose of the `step` parameter in `log_metric`?

A) To specify which training step this metric belongs to
B) To increment the metric value
C) To define the logging interval
D) To skip logging every N steps

<details>
<summary>Answer</summary>

**A) To specify which training step this metric belongs to**

**Explanation**: The `step` parameter enables time-series logging:
- Useful for tracking metrics across epochs/iterations
- Allows visualization of training curves
- Example: `mlflow.log_metric("loss", 0.5, step=1)` → epoch 1 loss
- Without `step`, metrics are overwritten

</details>

---

### Question 4
What is the purpose of the MLflow backend store?

A) To store model binaries
B) To store run metadata (parameters, metrics, tags)
C) To store training data
D) To cache API responses

<details>
<summary>Answer</summary>

**B) To store run metadata (parameters, metrics, tags)**

**Explanation**: MLflow has two storage systems:
- **Backend Store**: Metadata (params, metrics, tags, run info) - uses SQLite, PostgreSQL, MySQL
- **Artifact Store**: Large files (models, plots, datasets) - uses local filesystem, S3, GCS, Azure Blob

This separation enables efficient querying and scalable artifact storage.

</details>

---

### Question 5
**[Multiple Select]** Which of the following can be logged to MLflow? (Select all that apply)

A) Hyperparameters
B) Training/validation metrics
C) Model artifacts
D) Plots and visualizations
E) Code version (Git commit hash)
F) Production database credentials

<details>
<summary>Answer</summary>

**A, B, C, D, E**

**Explanation**:
- **A**: Use `mlflow.log_param()` or `mlflow.log_params()`
- **B**: Use `mlflow.log_metric()` or `mlflow.log_metrics()`
- **C**: Use `mlflow.log_model()` or `mlflow.sklearn.log_model()`
- **D**: Use `mlflow.log_figure()` or `mlflow.log_artifact()`
- **E**: Use `mlflow.set_tag("git_commit", commit_hash)`
- **F**: NEVER log credentials - use environment variables or secret management

</details>

---

### Question 6
What command starts an MLflow tracking server?

A) `mlflow start`
B) `mlflow server --backend-store-uri <uri> --default-artifact-root <path>`
C) `mlflow run server`
D) `mlflow tracking start`

<details>
<summary>Answer</summary>

**B) `mlflow server --backend-store-uri <uri> --default-artifact-root <path>`**

**Explanation**: Complete command:
```bash
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 0.0.0.0 \
  --port 5000
```

- `backend-store-uri`: Where to store metadata
- `default-artifact-root`: Where to store artifacts
- `host`: Interface to bind to
- `port`: Port to listen on

</details>

---

### Question 7
Examine this code:

```python
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("model_development")

with mlflow.start_run(run_name="baseline"):
    mlflow.log_param("model_type", "random_forest")
    # Train model...
    mlflow.sklearn.log_model(model, "model")
```

What happens if the experiment "model_development" doesn't exist?

A) An error is raised
B) The default experiment is used
C) The experiment is created automatically
D) Logging is disabled

<details>
<summary>Answer</summary>

**C) The experiment is created automatically**

**Explanation**: `mlflow.set_experiment()` behavior:
- If experiment exists: use it
- If experiment doesn't exist: create it
- Returns experiment ID
- Ensures experiment exists before starting runs

To create explicitly: `mlflow.create_experiment(name, artifact_location)`

</details>

---

### Question 8
What is the purpose of tags in MLflow?

A) To version control code
B) To add searchable metadata to runs/experiments
C) To price usage
D) To compress artifacts

<details>
<summary>Answer</summary>

**B) To add searchable metadata to runs/experiments**

**Explanation**: Tags enable organization and filtering:
```python
mlflow.set_tag("team", "data-science")
mlflow.set_tag("model_type", "classifier")
mlflow.set_tag("priority", "high")
```

Use cases:
- Filter runs in UI
- Programmatic search: `client.search_runs(filter_string="tags.team='data-science'")`
- Organize experiments by project, team, priority
- Track deployment status

</details>

---

## Section 2: Model Registry (Questions 9-15)

### Question 9
What are the standard stages in the MLflow Model Registry?

A) Development, Testing, Production
B) None, Staging, Production, Archived
C) Draft, Review, Approved, Deployed
D) Train, Validate, Test, Deploy

<details>
<summary>Answer</summary>

**B) None, Staging, Production, Archived**

**Explanation**: Model Registry stages:
- **None**: Default stage after registration
- **Staging**: For validation and testing
- **Production**: Currently deployed model
- **Archived**: Retired models

Custom stages are not supported; use tags for additional categorization.

</details>

---

### Question 10
How do you register a model in MLflow?

A) `mlflow.register_model(model_uri, name)`
B) `mlflow.save_model(model, name)`
C) `mlflow.create_model(name)`
D) `mlflow.deploy_model(model)`

<details>
<summary>Answer</summary>

**A) `mlflow.register_model(model_uri, name)`**

**Explanation**: Model registration:
```python
# During training
mlflow.sklearn.log_model(model, "model", registered_model_name="churn_predictor")

# Or after training
model_uri = "runs:/RUN_ID/model"
mlflow.register_model(model_uri, "churn_predictor")
```

- Creates new model or new version if model exists
- Returns `ModelVersion` object
- Model must be logged to a run first

</details>

---

### Question 11
Analyze this workflow:

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()
client.transition_model_version_stage(
    name="churn_predictor",
    version=3,
    stage="Production"
)
```

What happens to the previous Production model?

A) It is automatically archived
B) It remains in Production (multiple models can be in Production)
C) It transitions to Staging
D) It is deleted

<details>
<summary>Answer</summary>

**B) It remains in Production (multiple models can be in Production)**

**Explanation**: MLflow allows multiple versions in the same stage.

Best practice for single-production model:
```python
# Archive existing production models
for mv in client.get_latest_versions("churn_predictor", stages=["Production"]):
    client.transition_model_version_stage(
        name="churn_predictor",
        version=mv.version,
        stage="Archived"
    )

# Then promote new version
client.transition_model_version_stage(
    name="churn_predictor",
    version=3,
    stage="Production"
)
```

</details>

---

### Question 12
What is the correct way to load a Production model from the registry?

A) `mlflow.sklearn.load_model("models:/churn_predictor/Production")`
B) `mlflow.load_model("churn_predictor", stage="Production")`
C) `mlflow.get_model("churn_predictor").production`
D) `mlflow.registry.load_production("churn_predictor")`

<details>
<summary>Answer</summary>

**A) `mlflow.sklearn.load_model("models:/churn_predictor/Production")`**

**Explanation**: Model URI formats:
```python
# By stage
model = mlflow.sklearn.load_model("models:/churn_predictor/Production")

# By version number
model = mlflow.sklearn.load_model("models:/churn_predictor/3")

# By run ID
model = mlflow.sklearn.load_model("runs:/RUN_ID/model")
```

Format: `models:/<model_name>/<stage_or_version>`

</details>

---

### Question 13
**[Multiple Select]** Which operations can be performed on a model version in the registry? (Select all that apply)

A) Transition to a different stage
B) Add/update description
C) Add/update tags
D) Delete the version
E) Modify logged parameters
F) Change the model artifact

<details>
<summary>Answer</summary>

**A, B, C, D**

**Explanation**:
- **A**: `transition_model_version_stage()`
- **B**: `update_model_version(description="...")`
- **C**: `set_model_version_tag()`
- **D**: `delete_model_version()` (if not in Production)
- **E**: CANNOT modify - parameters are immutable once logged
- **F**: CANNOT modify - artifacts are immutable, must create new version

</details>

---

### Question 14
What is the purpose of model aliases in MLflow?

A) To rename models
B) To create human-readable references to model versions
C) To encrypt model names
D) To compress models

<details>
<summary>Answer</summary>

**B) To create human-readable references to model versions**

**Explanation**: Model aliases (MLflow 2.0+) provide mutable references:
```python
client.set_registered_model_alias("churn_predictor", "champion", version=5)
client.set_registered_model_alias("churn_predictor", "challenger", version=6)

# Load by alias
model = mlflow.sklearn.load_model("models:/churn_predictor@champion")
```

Benefits over stages:
- Multiple aliases per version
- Custom naming
- Easy A/B testing setup

</details>

---

### Question 15
How do you implement model rollback in MLflow?

A) Use `mlflow.rollback()` function
B) Transition the previous Production version back to Production
C) Delete the current Production version
D) Rollback is not supported

<details>
<summary>Answer</summary>

**B) Transition the previous Production version back to Production**

**Explanation**: Manual rollback process:
```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Archive current production model (version 5)
client.transition_model_version_stage("churn_predictor", version=5, stage="Archived")

# Promote previous version back to production (version 4)
client.transition_model_version_stage("churn_predictor", version=4, stage="Production")
```

Automated rollback requires:
- Monitoring production metrics
- Automatic stage transitions on performance degradation
- Implementation in CD pipeline

</details>

---

## Section 3: Hyperparameter Tracking (Questions 16-21)

### Question 16
What is the benefit of integrating Optuna with MLflow?

A) Faster training
B) Automatic hyperparameter tuning with comprehensive tracking of all trials
C) Better model accuracy
D) Reduced memory usage

<details>
<summary>Answer</summary>

**B) Automatic hyperparameter tuning with comprehensive tracking of all trials**

**Explanation**: Optuna + MLflow integration:
- Optuna: Efficient hyperparameter optimization (TPE, CMA-ES)
- MLflow: Tracks every trial as a run
- Combined: Automated search + complete experiment history

```python
from optuna.integration.mlflow import MLflowCallback

mlflc = MLflowCallback(tracking_uri="http://localhost:5000", metric_name="accuracy")

study.optimize(objective, n_trials=50, callbacks=[mlflc])
```

Benefits:
- Compare all trials in MLflow UI
- Reproduce best configuration
- Analyze parameter importance

</details>

---

### Question 17
What is the purpose of the `step` parameter when logging metrics during training?

A) To control training speed
B) To log metrics at specific epochs/iterations for time-series visualization
C) To skip logging on some iterations
D) To aggregate metrics

<details>
<summary>Answer</summary>

**B) To log metrics at specific epochs/iterations for time-series visualization**

**Explanation**: Time-series metric logging:
```python
for epoch in range(num_epochs):
    train_loss = train_one_epoch()
    val_loss = validate()

    mlflow.log_metric("train_loss", train_loss, step=epoch)
    mlflow.log_metric("val_loss", val_loss, step=epoch)
```

Enables:
- Training curve visualization
- Detecting overfitting (train vs. val divergence)
- Early stopping decisions
- Comparing convergence across runs

</details>

---

### Question 18
Examine this hyperparameter logging:

```python
params = {
    'model': {
        'n_estimators': 100,
        'max_depth': 10
    },
    'preprocessing': {
        'scaler': 'standard'
    }
}

mlflow.log_params(params)
```

What happens when you try to log nested dictionaries?

A) Nested structure is preserved
B) An error is raised - params must be flattened
C) Only top-level keys are logged
D) Nested dicts are converted to JSON strings

<details>
<summary>Answer</summary>

**B) An error is raised - params must be flattened**

**Explanation**: MLflow params must be flat key-value pairs.

Solution - flatten the dict:
```python
def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

flat_params = flatten_dict(params)
# {'model.n_estimators': 100, 'model.max_depth': 10, 'preprocessing.scaler': 'standard'}
mlflow.log_params(flat_params)
```

</details>

---

### Question 19
What is the purpose of experiment runs hierarchy (parent-child runs)?

A) To compress experiment data
B) To organize related runs (e.g., all hyperparameter tuning trials under one parent)
C) To share parameters between runs
D) To enable concurrent training

<details>
<summary>Answer</summary>

**B) To organize related runs (e.g., all hyperparameter tuning trials under one parent)**

**Explanation**: Nested runs create hierarchy:
```python
with mlflow.start_run(run_name="hyperparameter_optimization") as parent_run:
    mlflow.log_param("optimization_strategy", "grid_search")

    for params in param_grid:
        with mlflow.start_run(run_name=f"trial_{i}", nested=True):
            # Train model with params
            mlflow.log_params(params)
            mlflow.log_metric("accuracy", accuracy)
```

Use cases:
- Hyperparameter search (parent = search, children = trials)
- Cross-validation (parent = experiment, children = folds)
- Ensemble models (parent = ensemble, children = base models)

</details>

---

### Question 20
**[Multiple Select]** Which of the following are valid strategies for comparing ML experiments in MLflow? (Select all that apply)

A) Use MLflow UI's comparison view
B) Query runs programmatically with `search_runs()`
C) Export runs to DataFrame for analysis
D) Use MLflow's automatic best model selection
E) Create custom visualization with logged metrics

<details>
<summary>Answer</summary>

**A, B, C, E**

**Explanation**:
- **A**: UI provides parallel coordinates, scatter plots, table view
- **B**: `mlflow.search_runs(filter_string="metrics.accuracy > 0.9")` returns DataFrame
- **C**: `runs_df = mlflow.search_runs(experiment_ids=[exp_id])`
- **D**: No automatic selection - you must implement criteria
- **E**: Load metrics and create custom plots with matplotlib/plotly

</details>

---

### Question 21
What is the best practice for organizing experiments in MLflow?

A) Create one experiment for all models
B) Create separate experiments per model type or project
C) Create a new experiment for each run
D) Use only the default experiment

<details>
<summary>Answer</summary>

**B) Create separate experiments per model type or project**

**Explanation**: Experiment organization strategies:

**Good**:
```
- customer_churn_rf (Random Forest experiments)
- customer_churn_xgboost (XGBoost experiments)
- customer_churn_neural_net (Deep learning experiments)
```

**Better**:
```
- customer_churn/model_development
- customer_churn/hyperparameter_optimization
- customer_churn/production_validation
```

Principles:
- Group related runs
- Enable easy comparison within experiment
- Use tags for finer categorization
- Avoid too many experiments (hard to navigate)

</details>

---

## Section 4: MLflow Models (Questions 22-25)

### Question 22
What is an MLflow Model flavor?

A) Different model architectures
B) Format-specific implementations for loading/saving models (e.g., sklearn, pytorch, tensorflow)
C) Model versions
D) Hyperparameter configurations

<details>
<summary>Answer</summary>

**B) Format-specific implementations for loading/saving models (e.g., sklearn, pytorch, tensorflow)**

**Explanation**: MLflow supports multiple frameworks through "flavors":
- `mlflow.sklearn` - scikit-learn
- `mlflow.pytorch` - PyTorch
- `mlflow.tensorflow` - TensorFlow
- `mlflow.xgboost` - XGBoost
- `mlflow.pyfunc` - Generic Python function (custom models)

Example:
```python
# Log with sklearn flavor
mlflow.sklearn.log_model(sklearn_model, "model")

# Log with multiple flavors
mlflow.pyfunc.log_model(
    artifact_path="model",
    python_model=custom_wrapper,
    artifacts={"sklearn_model": sklearn_model_path}
)
```

</details>

---

### Question 23
What is the purpose of the `pyfunc` flavor?

A) To improve Python performance
B) To create a generic Python function interface for any model
C) To compress models
D) To deploy models to cloud functions

<details>
<summary>Answer</summary>

**B) To create a generic Python function interface for any model**

**Explanation**: `pyfunc` is a universal interface:

```python
class CustomModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        # Load model and preprocessing artifacts
        self.model = joblib.load(context.artifacts["model_path"])
        self.scaler = joblib.load(context.artifacts["scaler_path"])

    def predict(self, context, model_input):
        # Custom prediction logic with preprocessing
        scaled_input = self.scaler.transform(model_input)
        return self.model.predict(scaled_input)
```

Benefits:
- Wrap any model (even non-ML libraries)
- Include preprocessing/postprocessing
- Consistent API across frameworks
- Compatible with all MLflow deployment tools

</details>

---

### Question 24
How do you serve an MLflow model locally for testing?

A) `mlflow deploy models:/model_name/Production`
B) `mlflow models serve -m models:/model_name/Production -p 5001`
C) `mlflow run serve --model-name model_name`
D) `mlflow start-server --model model_name`

<details>
<summary>Answer</summary>

**B) `mlflow models serve -m models:/model_name/Production -p 5001`**

**Explanation**: Local model serving:
```bash
# Serve by stage
mlflow models serve -m models:/churn_predictor/Production -p 5001

# Serve by version
mlflow models serve -m models:/churn_predictor/3 -p 5001

# Serve by run ID
mlflow models serve -m runs:/RUN_ID/model -p 5001
```

Test with:
```bash
curl -X POST http://localhost:5001/invocations \
  -H 'Content-Type: application/json' \
  -d '{"dataframe_split": {"columns": ["feature1", "feature2"], "data": [[1.0, 2.0]]}}'
```

</details>

---

### Question 25
What information is stored in the `MLmodel` file?

A) Model weights
B) Model metadata (flavors, signature, dependencies, etc.)
C) Training data
D) Hyperparameters

<details>
<summary>Answer</summary>

**B) Model metadata (flavors, signature, dependencies, etc.)**

**Explanation**: `MLmodel` is a YAML file containing:

```yaml
artifact_path: model
flavors:
  python_function:
    env: conda.yaml
    loader_module: mlflow.sklearn
    model_path: model.pkl
    python_version: 3.10.0
  sklearn:
    pickled_model: model.pkl
    serialization_format: cloudpickle
    sklearn_version: 1.3.0
signature:
  inputs: '[{"name": "feature1", "type": "double"}, {"name": "feature2", "type": "double"}]'
  outputs: '[{"type": "long"}]'
utc_time_created: '2024-01-15 10:30:00.123456'
```

Enables:
- Loading model with correct flavor
- Reproducing environment
- Input/output validation
- Cross-framework compatibility

</details>

---

## Section 5: Best Practices (Questions 26-28)

### Question 26
What is the recommended way to handle large datasets in MLflow?

A) Log full dataset as artifact
B) Log dataset metadata (path, version, hash) instead of data itself
C) Compress dataset before logging
D) Store in backend database

<details>
<summary>Answer</summary>

**B) Log dataset metadata (path, version, hash) instead of data itself**

**Explanation**: Best practices for datasets:

```python
# DON'T: Log entire dataset
# mlflow.log_artifact("train_data.csv")  # Bad for large files

# DO: Log metadata
import hashlib

data_path = "s3://bucket/datasets/train_data_v2.csv"
data_hash = hashlib.md5(open("train_data.csv", "rb").read()).hexdigest()

mlflow.log_param("data_path", data_path)
mlflow.log_param("data_version", "v2")
mlflow.log_param("data_hash", data_hash)
mlflow.log_param("n_samples", len(df))

# Or use dataset tracking (MLflow 2.0+)
dataset = mlflow.data.from_pandas(df, source=data_path)
mlflow.log_input(dataset, context="training")
```

For large data:
- Use external versioning (DVC, Delta Lake)
- Log references, not data
- Track data lineage

</details>

---

### Question 27
**[Multiple Select]** Which of the following should be logged to MLflow for reproducibility? (Select all that apply)

A) Hyperparameters
B) Random seed
C) Library versions
D) Git commit hash
E) Hardware specifications
F) API keys and passwords

<details>
<summary>Answer</summary>

**A, B, C, D, E**

**Explanation** - Log for reproducibility:
- **A**: All hyperparameters (`mlflow.log_params()`)
- **B**: Random seed for determinism (`mlflow.log_param("random_seed", 42)`)
- **C**: Dependencies (`pip freeze > requirements.txt`, log as artifact)
- **D**: Code version (`mlflow.set_tag("git_commit", commit_hash)`)
- **E**: For performance benchmarking (`mlflow.set_tag("gpu_type", "A100")`)
- **F**: NEVER log secrets - use env vars or secret management

Additional:
- OS and Python version
- Training duration
- Data version/hash

</details>

---

### Question 28
You trained a model and logged it to MLflow, but forgot to log some important metrics. What should you do?

A) Restart the run and retrain the model
B) Use `MlflowClient` to log metrics to the existing run
C) Delete the run and create a new one
D) Metrics cannot be added after run completion

<details>
<summary>Answer</summary>

**B) Use `MlflowClient` to log metrics to the existing run**

**Explanation**: Add metrics to completed runs:

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Log to existing run
run_id = "existing_run_id"
client.log_metric(run_id, "forgotten_metric", 0.95)
client.log_param(run_id, "forgotten_param", "value")
client.set_tag(run_id, "forgotten_tag", "value")

# Or reopen the run
with mlflow.start_run(run_id=run_id):
    mlflow.log_metric("new_metric", 0.88)
```

Best practice:
- Log everything during training when possible
- Use comprehensive tracking wrapper class
- Validate logged data after run

</details>

---

## Scoring Guide

| Score | Grade | Feedback |
|-------|-------|----------|
| 26-28 | A+ | Excellent! Expert-level understanding of MLflow |
| 23-25 | A | Great job! Strong grasp of experiment tracking |
| 21-22 | B | Good. Review model registry concepts |
| 18-20 | C | Passing. Revisit MLflow fundamentals |
| < 18 | F | Please review lecture notes and retry |

---

## Answer Key Summary

1. B | 2. B | 3. A | 4. B | 5. A,B,C,D,E
6. B | 7. C | 8. B | 9. B | 10. A
11. B | 12. A | 13. A,B,C,D | 14. B | 15. B
16. B | 17. B | 18. B | 19. B | 20. A,B,C,E
21. B | 22. B | 23. B | 24. B | 25. B
26. B | 27. A,B,C,D,E | 28. B

---

## Practical Challenge

After completing this quiz, try this hands-on challenge:

**Challenge**: Create a complete experiment tracking workflow:
1. Train 3 different models (Logistic Regression, Random Forest, XGBoost)
2. Log all hyperparameters, metrics, and artifacts to MLflow
3. Register the best model in the registry
4. Transition it through Staging → Production
5. Serve the production model locally
6. Make a prediction via REST API

**Time**: 30-45 minutes

---

## Next Steps

- Review any missed questions
- Complete the hands-on exercises
- Practice with your own ML projects
- Explore MLflow UI features
- Read `resources.md` for advanced topics

**Good luck!** 🎯
