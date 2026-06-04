# Experiment Tracking & MLflow - Comprehensive Lecture Notes

**Module**: 02-experiment-tracking
**Role**: MLOps Engineer (Level 2.5B)
**Duration**: 10 hours of content

---

## Table of Contents

1. [Why Experiment Tracking](#why-experiment-tracking)
2. [MLflow Architecture](#mlflow-architecture)
3. [The Tracking API](#the-tracking-api)
4. [Autologging](#autologging)
5. [Custom Metrics + Artifacts](#custom-metrics--artifacts)
6. [Model Signatures + Pyfunc Packaging](#model-signatures--pyfunc-packaging)
7. [Model Registry + Promotion](#model-registry--promotion)
8. [Production Tracking Server](#production-tracking-server)
9. [Integration with CI/CD](#integration-with-cicd)
10. [Beyond MLflow](#beyond-mlflow)

---

## Why Experiment Tracking

A data scientist trains 50 models in a week, tweaking hyperparameters and
features. Three months later, which one was the best? Which one shipped to
production? What data was it trained on? If the answer involves opening a
Google Doc or `model_v2_final_FINAL_use_this.pkl`, you don't have experiment
tracking — you have hope.

Experiment tracking captures, for every training run:
- **Parameters**: hyperparameters, dataset version, code version
- **Metrics**: train + validation losses, evaluation metrics, business KPIs
- **Artifacts**: trained model, plots, datasets, environment specs
- **Metadata**: who, when, with what compute, against what data

This becomes the single source of truth for "which model is best" and "can I
reproduce this result?"

### Symptoms you don't have it

- "It worked last week" — but we can't find the model
- Spreadsheet of run results that's always out of date
- Re-trained the same model 3 times because we couldn't find the original
- Production runs an unknown version because nobody recorded the promotion
- Auditor asks "show me how this model was trained" → silence

### What good looks like

- Every training run logs to a central tracking server automatically
- Comparison view shows hyperparameter vs metric trends across hundreds of runs
- Production model is a specific (registered model, version) tuple
- Rolling back is "promote previous version to Production"
- 6 months later, you can `git checkout <sha>` + `mlflow models serve <uri>` and reproduce

---

## MLflow Architecture

MLflow has four loosely-coupled components. You'll use them all.

```
┌────────────────────────────────────────────────────────────┐
│                  Training script (your code)               │
│   mlflow.log_param() / log_metric() / log_artifact() / ... │
└─────────────────────┬──────────────────────────────────────┘
                      ▼
        ┌──────────── Tracking Server ────────────┐
        │  REST API; stores run metadata in       │
        │  Backend Store (Postgres / SQLite)      │
        │  Artifacts go to Artifact Store         │
        │  (S3 / MinIO / local filesystem)        │
        └─────────────┬───────────────────────────┘
                      ▼
        ┌──────────── Model Registry ─────────────┐
        │  Versioned models with stage labels:    │
        │  None → Staging → Production → Archived │
        └─────────────────────────────────────────┘
```

### Components

1. **Tracking** — records runs (params, metrics, artifacts).
2. **Projects** — packaging format for reproducible runs (Conda env, entrypoints).
3. **Models** — standardized format for trained models (works across frameworks).
4. **Registry** — central versioned model store with lifecycle stages.

### Deployment topology (production)

- **Tracking server**: stateless app, behind a load balancer, autoscaled
- **Backend store**: Postgres (RDS in AWS / Cloud SQL in GCP)
- **Artifact store**: S3 / GCS / Azure Blob (with appropriate IAM)
- **UI**: served by the tracking server (or use a separate read replica)

---

## The Tracking API

### Quickstart

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("iris-classifier")

with mlflow.start_run(run_name="rf-baseline"):
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 8)

    model = RandomForestClassifier(n_estimators=100, max_depth=8)
    model.fit(X_train, y_train)

    train_acc = model.score(X_train, y_train)
    val_acc = model.score(X_val, y_val)
    mlflow.log_metric("train_acc", train_acc)
    mlflow.log_metric("val_acc", val_acc)

    mlflow.sklearn.log_model(model, "model")
```

### Concepts

- **Experiment**: a named collection of runs (e.g., `iris-classifier`)
- **Run**: one training execution (parent of params, metrics, artifacts)
- **Run ID**: unique identifier (32-char hex)
- **Active run**: the one currently inside a `with mlflow.start_run():` block

### What to log

| Type | Examples |
|---|---|
| `log_param` | hyperparameters, dataset version, git SHA, random seed |
| `log_metric` | loss, accuracy, F1, AUC, business KPI proxies |
| `log_artifact` | trained model, plots, confusion matrices, dataset samples |
| `log_dict` | small structured data (config, schema) |
| `log_text` | training logs, model card text |

### Search

```python
runs = mlflow.search_runs(experiment_names=["iris-classifier"],
                          filter_string="metrics.val_acc > 0.85")
```

---

## Autologging

```python
import mlflow.sklearn
mlflow.sklearn.autolog()
```

Autolog wires in framework-specific logging without per-call code. Available
for sklearn, PyTorch, TensorFlow, XGBoost, LightGBM, and others.

What it captures (sklearn example):
- Every estimator parameter
- Training metric per epoch (when applicable)
- Final model + signature
- Input example (shape, dtypes)

Autolog gets you 80% there. Add explicit `log_metric` calls for the metrics
that matter to your business (which sklearn doesn't know).

### Pitfalls

- Autolog hides what's being captured; read the docs for your framework
- Auto-inferred signatures may be wrong if your training data isn't representative
- For high-cardinality runs (parameter sweeps), autologging can flood the
  backend; consider sampling

---

## Custom Metrics + Artifacts

Beyond auto-logged metrics, log business-aligned signals:

```python
from sklearn.metrics import f1_score, confusion_matrix
import matplotlib.pyplot as plt

f1 = f1_score(y_val, preds, average="macro")
mlflow.log_metric("f1_macro", f1)

# Per-class accuracy
for cls in np.unique(y_val):
    mask = y_val == cls
    mlflow.log_metric(f"acc_class_{cls}", (preds[mask] == cls).mean())

# Confusion matrix as PNG
fig, ax = plt.subplots()
ax.imshow(confusion_matrix(y_val, preds))
mlflow.log_figure(fig, "confusion_matrix.png")

# Dataset hash (for reproducibility)
mlflow.log_param("dataset_sha256", sha256_of_dataset)
```

Custom artifacts you'll commonly log:
- Confusion matrices, ROC curves, calibration plots
- SHAP value summaries
- Per-slice metrics
- Sampled hard examples (false positives, false negatives)
- Training environment freeze (`pip freeze > requirements.txt`)

---

## Model Signatures + Pyfunc Packaging

A **signature** records input + output schema. Enforced at inference, it
catches "I sent floats but the model expects ints" before that error reaches
prod.

```python
from mlflow.models.signature import infer_signature

signature = infer_signature(X_train, model.predict(X_train))
mlflow.sklearn.log_model(model, "model", signature=signature, input_example=X_train[:3])
```

**Pyfunc** is the framework-agnostic packaging:

```python
class IrisModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        self.model = joblib.load(context.artifacts["model"])

    def predict(self, context, model_input):
        # Preprocessing happens here, not in the calling code
        X = np.clip(model_input, 0, 10)
        return self.model.predict(X)

mlflow.pyfunc.log_model(
    artifact_path="iris-pyfunc",
    python_model=IrisModel(),
    artifacts={"model": "models/rf.joblib"},
    pip_requirements=["scikit-learn>=1.5"],
)
```

Result: anyone can `mlflow models serve -m models:/iris-pyfunc/Production`
and get a REST endpoint with the right Python env + preprocessing baked in.

---

## Model Registry + Promotion

A model in the registry has:
- A **name** (e.g., `iris-rf`)
- Multiple **versions** (1, 2, 3, ...)
- Each version has a **stage**: None / Staging / Production / Archived

### Promotion workflow

```python
from mlflow.tracking import MlflowClient

c = MlflowClient()

# Register a new version
result = mlflow.register_model("runs:/<run_id>/model", "iris-rf")
version = result.version

# Promote to Staging (with quality gate)
c.transition_model_version_stage(name="iris-rf", version=version, stage="Staging")

# Test in staging environment
# ...

# Promote to Production
c.transition_model_version_stage(
    name="iris-rf",
    version=version,
    stage="Production",
    archive_existing_versions=True,   # automatically archive the previous Production version
)
```

### Quality gates

A gate is just code that runs before promotion:

```python
prev_acc = get_metric(client, "iris-rf", current_prod_version, "val_acc")
new_acc = get_metric(client, "iris-rf", candidate_version, "val_acc")
if new_acc < prev_acc - 0.005:
    raise PromotionError(f"Quality gate failed: {new_acc} < {prev_acc - 0.005}")
```

Gates that work in practice:
- Aggregate metric delta vs current Production
- Per-slice metric (must not regress > Xpp on any required slice)
- Bias check vs reference dataset
- Latency budget (model file size, inference benchmark)

### Rollback

Rollback is "promote previous version":

```python
versions = c.search_model_versions(f"name='iris-rf'")
prev = next(v for v in versions if v.current_stage == "Staging")  # last good
c.transition_model_version_stage("iris-rf", prev.version, "Production",
                                  archive_existing_versions=True)
```

---

## Production Tracking Server

The default `mlflow server` is fine for one developer. For a team, run it
like any other production service:

### docker-compose.yaml (minimal production-ish)

```yaml
services:
  pg:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: mlflow
      POSTGRES_PASSWORD: mlflow
      POSTGRES_DB: mlflow

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    ports: ["9000:9000", "9001:9001"]
    environment:
      MINIO_ROOT_USER: admin
      MINIO_ROOT_PASSWORD: adminadmin

  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.16.0
    ports: ["5000:5000"]
    command: >
      mlflow server
        --host 0.0.0.0
        --backend-store-uri postgresql://mlflow:mlflow@pg/mlflow
        --default-artifact-root s3://mlflow/
    environment:
      MLFLOW_S3_ENDPOINT_URL: http://minio:9000
      AWS_ACCESS_KEY_ID: admin
      AWS_SECRET_ACCESS_KEY: adminadmin
    depends_on: [pg, minio]
```

### Production hardening checklist

- [ ] Backend store on managed Postgres (RDS / Cloud SQL); 7-day PITR
- [ ] Artifact bucket with versioning + lifecycle (cold-tier after 90d)
- [ ] Auth: front the tracking server with an OAuth2 proxy (oauth2-proxy + nginx)
- [ ] HTTPS termination
- [ ] Per-team access control to the artifact bucket via IAM
- [ ] Backups + retention policy for runs (likely 2+ years)
- [ ] Audit log of registry stage transitions

---

## Integration with CI/CD

The pattern most teams use:

```yaml
# .github/workflows/train.yml
on: { push: { branches: [main] }, workflow_dispatch: }
jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_URL }}
          MLFLOW_TRACKING_USERNAME: ${{ secrets.MLFLOW_USER }}
          MLFLOW_TRACKING_PASSWORD: ${{ secrets.MLFLOW_PASS }}
        run: python -m src.train
      - run: python -m src.evaluate_and_promote
```

The `evaluate_and_promote` step is the quality gate. It compares the freshly
trained run vs current Production and promotes (or fails) accordingly.

---

## Beyond MLflow

MLflow is the default for open-source. Other tools serve similar roles:

| Tool | When it wins |
|---|---|
| **Weights & Biases** | Best-in-class UI for hyperparameter sweeps; team collaboration |
| **Neptune** | Lightweight; good for academic research |
| **Comet** | Strong dashboarding |
| **ClearML** | Pipeline + tracking + queue in one |
| **Sagemaker Experiments** | If you're all-in on AWS |
| **Vertex AI Experiments** | If you're all-in on GCP |

Most teams: MLflow until > 50 ML engineers, then evaluate a paid alternative
for sweep / collaboration features.

---

## Summary

- Every training run goes through a tracking server. No exceptions.
- The registry is the source of truth for "what's in production."
- Pyfunc packaging lets one team's model run in another team's serving stack.
- Promotion is gated by quality checks; rollback is "promote previous."
- Production tracking servers are real services: Postgres + S3 + auth + backups.
- Tooling beyond MLflow exists; defer the decision until you've outgrown free.
