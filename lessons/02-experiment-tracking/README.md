# Module 02: Experiment Tracking & MLflow

**Role**: MLOps Engineer (Level 2.5B)
**Duration**: 18 hours
**Prerequisites**:
- Module 01 (MLOps Foundations)
- Python + scikit-learn / PyTorch basics
- Docker basics

## Module Overview

Experiment tracking is the bedrock of every mature MLOps workflow. Without it,
teams can't answer "what hyperparameters produced this model?" or "is the new
run actually better than last week's?" This module makes you fluent in MLflow
end-to-end: backed tracking server, custom artifacts + metrics + model
signatures, model registry, promotion workflows, and integration with training
pipelines.

## Learning Objectives

By the end of this module, you will be able to:

1. **Stand up** an MLflow tracking server backed by Postgres + S3/MinIO
2. **Instrument** training code with autologging + manual metrics + artifacts + model signatures
3. **Package** trained models with `mlflow.pyfunc` for reproducible serving
4. **Operate** the model registry with stage transitions (Staging → Production)
5. **Implement** quality-gated promotion with rollback
6. **Search** the experiment store programmatically (parameter sweeps, comparison)
7. **Integrate** MLflow into a CI/CD pipeline so every training run is captured

## Module Structure

```
02-experiment-tracking/
├── README.md
├── lecture-notes.md         # Comprehensive lecture material
├── exercises/               # 5 hands-on exercises
├── quiz.md                  # 28-question assessment
└── resources.md             # Reading + tooling references
```

## Key Concepts

- **Tracking server**: where runs live (metrics, params, artifacts, models)
- **Backend store**: Postgres / MySQL / SQLite for metadata
- **Artifact store**: S3 / MinIO / local for files
- **Model registry**: versioned model store with stage transitions
- **Pyfunc**: framework-agnostic model packaging (deployable as a REST server)
- **Signature**: schema for model inputs + outputs (enforced at inference)

## Tools Covered

- MLflow (tracking + registry + projects + models)
- PostgreSQL (backend store)
- MinIO (S3-compatible artifact store)
- GitHub Actions (CI integration)
- Optional: Weights & Biases, Neptune (alternatives discussed)

## Required Setup

```bash
docker compose up -d   # Postgres + MinIO + MLflow server
export MLFLOW_TRACKING_URI=http://localhost:5000
```

## Pacing

| Week | Focus |
|---|---|
| Week 1 | Lecture + Exercise 1 (fundamentals) + Exercise 2 (registry) |
| Week 2 | Exercise 3 (advanced features) + Exercise 4 (CI/CD integration) |
| Week 3 | Exercise 5 (full pipeline) + quiz + capstone for the module |

## How this module fits the track

- Module 01 (Foundations) introduced "experiment tracking is required"; this module operationalizes it.
- Module 03 (Monitoring) builds on the model registry — every monitored model lives there.
- Module 06 (Automation) ties MLflow into orchestration (Airflow + retraining).
- Module 09 (Security) revisits MLflow with secret management for production servers.
