# Module 01: MLOps Foundations - Quiz

## Instructions

- **Total Questions**: 25
- **Time Limit**: 35 minutes
- **Passing Score**: 75% (19/25 correct)
- **Question Types**: Multiple choice, multiple select

---

### 1. MLOps is best described as the combination of:
- [ ] a) DevOps + Data Science
- [x] b) Machine Learning + DevOps + Data Engineering
- [ ] c) Machine Learning + Kubernetes
- [ ] d) Data Engineering + Cloud Engineering

### 2. The Google MLOps maturity model defines levels 0-2. Level 1 is characterized primarily by:
- [ ] a) Single-model deployment from notebook
- [x] b) Automated training pipeline + reproducibility
- [ ] c) Full CI/CD for the model code and the pipeline
- [ ] d) Multi-model orchestration

### 3. Which of the following are valid MLOps artifacts? (Select all that apply)
- [x] a) Trained model weights
- [x] b) Feature transformations / preprocessing logic
- [x] c) Training datasets (with versions)
- [x] d) Hyperparameter configurations
- [x] e) Environment specifications (deps, GPU drivers)

### 4. The primary risk of "It works on my laptop" in ML is:
- [ ] a) Performance is too fast
- [x] b) Lack of reproducibility in production
- [ ] c) Higher cloud bills
- [ ] d) Inability to use Python

### 5. What is "training-serving skew"?
- [x] a) Features computed differently between training and serving lead to wrong predictions
- [ ] b) The serving infrastructure is more expensive than training
- [ ] c) Training data is older than serving data
- [ ] d) Inference latency is higher than training step time

### 6. Which is NOT a typical MLOps responsibility?
- [ ] a) Model deployment
- [ ] b) Drift monitoring
- [x] c) Choosing the model architecture
- [ ] d) Reproducible training pipelines

### 7. A feature store primarily solves:
- [x] a) Training-serving skew + feature reuse across teams
- [ ] b) Model serving latency
- [ ] c) GPU memory limits
- [ ] d) Hyperparameter tuning

### 8. Why is silent model drift particularly dangerous in production?
- [x] a) Models keep returning responses; users see degraded experience without alerts firing
- [ ] b) Models crash without warning
- [ ] c) Drift triggers immediate API errors
- [ ] d) Drift is always caught by load tests

### 9. The MLOps lifecycle typically includes which of these stages? (Select all)
- [x] a) Data ingestion
- [x] b) Feature engineering
- [x] c) Model training
- [x] d) Deployment
- [x] e) Monitoring
- [x] f) Retraining

### 10. A "shadow deployment" of a new model means:
- [x] a) The new model receives traffic but its responses are not returned to users; used to validate behavior
- [ ] b) The new model replaces the old in 50% of traffic
- [ ] c) The new model is deployed but never receives traffic
- [ ] d) The old model continues serving while the new one trains

### 11. Which of these is NOT a Google MLOps maturity Level 2 capability?
- [ ] a) CI/CD for model code + pipeline
- [ ] b) Automated continuous training
- [x] c) Single deployment per quarter
- [ ] d) Automated model performance validation

### 12. What is the primary purpose of an experiment tracking system?
- [x] a) Record hyperparameters + metrics + artifacts for every training run
- [ ] b) Replace version control
- [ ] c) Serve models at scale
- [ ] d) Encrypt training data

### 13. A model card is typically used for:
- [x] a) Documenting intended use, performance, limitations, and known biases of a model
- [ ] b) Storing trained model weights
- [ ] c) Tracking GPU utilization
- [ ] d) Serving predictions

### 14. When should you NOT automate retraining? (Select all that apply)
- [x] a) When the cost of a bad model outweighs the cost of being slightly stale
- [x] b) When you can't reliably detect bad retrained models
- [ ] c) When data drifts daily
- [x] d) When humans are required to approve every promotion (regulated industries)

### 15. The "challenger / champion" pattern refers to:
- [x] a) Running a new model in parallel with the production model to compare
- [ ] b) Two competing models in production simultaneously
- [ ] c) A/B test with two equal-weight variants
- [ ] d) The hierarchical model registry

### 16. CI/CD for ML differs from CI/CD for software primarily because:
- [x] a) Data dependencies make tests harder; non-determinism complicates pass/fail
- [ ] b) ML uses Python and CI/CD tools don't support Python
- [ ] c) Models are larger than typical software artifacts
- [ ] d) ML deployments are riskier than software deployments

### 17. A "blue-green" model deployment:
- [x] a) Deploys the new model alongside the old; flips traffic atomically
- [ ] b) Gradually shifts traffic from 5% to 100%
- [ ] c) Replaces the old model immediately
- [ ] d) Runs the new model only at night

### 18. Which of these is the strongest indicator of MLOps maturity?
- [ ] a) Number of GPUs owned
- [ ] b) Number of models in production
- [x] c) Time from "model trained" to "model in production"
- [ ] d) Number of data scientists hired

### 19. A "feature freeze" before a model retraining is useful because:
- [x] a) It establishes a reproducible baseline data state
- [ ] b) It reduces GPU costs
- [ ] c) It speeds up training
- [ ] d) It's required by GDPR

### 20. Which monitoring signal would detect a label-distribution shift?
- [ ] a) Latency p99
- [x] b) Predicted-class distribution over time
- [ ] c) CPU utilization
- [ ] d) Request rate

### 21. Population Stability Index (PSI) measures:
- [x] a) The distributional difference between a reference and a production data window
- [ ] b) Model accuracy
- [ ] c) Network round-trip latency
- [ ] d) Inference cost per request

### 22. Reproducibility in ML requires capturing: (Select all)
- [x] a) Random seeds
- [x] b) Library versions
- [x] c) Hardware (e.g., GPU model + driver)
- [x] d) Data snapshot (or hash)
- [x] e) Hyperparameters

### 23. An "MLOps platform team" is most likely to own:
- [x] a) Tracking server, registry, feature store, serving runtime, monitoring stack
- [ ] b) The model architecture decisions
- [ ] c) The business KPI definitions
- [ ] d) The training data labelling process

### 24. In a regulated industry (banking, healthcare), MLOps must additionally include:
- [x] a) Decision logs + lineage + auditable approval workflows
- [ ] b) Open-source-only tooling
- [ ] c) Single-region deployment
- [ ] d) Manual approval for every prediction

### 25. The "platform vs gatekeeper" trap describes:
- [x] a) Becoming a bottleneck instead of an enabler — every team must go through your queue
- [ ] b) Choosing between SaaS and self-hosted
- [ ] c) Whether to require approval for production deploys
- [ ] d) Whether to charge teams for compute

---

## Answer Key Summary

1.b  2.b  3.all  4.b  5.a  6.c  7.a  8.a  9.all  10.a
11.c  12.a  13.a  14.a+b+d  15.a  16.a  17.a  18.c  19.a  20.b
21.a  22.all  23.a  24.a  25.a
