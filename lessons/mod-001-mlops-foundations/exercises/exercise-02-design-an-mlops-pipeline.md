## Exercise 2: Design an MLOps Pipeline (90 minutes)

**Objective**: For a given product scenario, draft a complete MLOps pipeline architecture without writing code.

### Background

The pipeline shape is set before the first line of code. Engineers who can
design well skip a lot of rework.

### Scenario

A product team wants to ship a churn-prediction model for a SaaS app:
- 500K active users
- Daily prediction batch + on-demand re-scoring on user actions
- Must retrain weekly with the last 90 days of behavior
- Must comply with GDPR (data-subject delete must propagate to features)

### Tasks

1. **Sketch the pipeline** as boxes-and-arrows. Include:
   - Data ingestion (sources, formats, cadence)
   - Storage (warehouse, feature store, model registry)
   - Training (offline pipeline, hyperparameter sweeps, evaluation)
   - Serving (batch vs online; how predictions are stored)
   - Monitoring (drift, performance, bias)
   - Retraining triggers (cron + drift)
   - Governance (data lineage, model approval, audit log)

2. **List the trade-offs** at each step: what alternatives exist + why your choice.

3. **Failure modes**: 5 ways this pipeline can break + how the system detects them.

### Deliverable

A `PIPELINE_DESIGN.md` (~1500 words) + a diagram (Mermaid or ASCII).

### Acceptance criteria

- Each layer has a named tool/technology
- Each trade-off discussion includes the alternative considered
- Failure modes are specific (not "the model could be wrong")

---
