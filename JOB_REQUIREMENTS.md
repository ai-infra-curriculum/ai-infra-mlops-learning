# MLOps Engineer — Job Requirements Coverage

**Role**: MLOps Engineer (level 30)
**Cycle**: 2026-07
**Postings sampled**: 25 (distinct employers, ≥90% dated within the last 90 days)
**Machine-readable source**: [`.aicg/job-requirements.json`](.aicg/job-requirements.json)

## Method

- Sample of 25 postings pulled from Greenhouse, Ashby, Lever, Workday, direct company career pages (NVIDIA, Stripe, Salesforce/Slack, Toyota, Cloudflare) and job aggregators.
- Requirement frequency = fraction of the 25 postings that name the requirement explicitly.
- Ownership uses the "lowest-level role where genuinely required" rule. Where a companion role at the same level (e.g., AI/ML Platform Engineer) is a better fit, coverage is linked out rather than duplicated.
- Continuity bias applies: existing modules are not restructured; only novel, above-threshold, un-owned requirements would trigger additions.

## Postings

| Employer | Title | Posted | URL |
|---|---|---|---|
| Experian | MLOps Engineer, Machine Learning Engineer (Remote) | 2026-Q2 | https://jobs.experian.com/job/mlops-engineer-machine-learning-engineer-remote-in-united-states-jid-3846 |
| Samsara | Staff/Lead Machine Learning Engineer - ML Infrastructure | 2026-Q2 | https://www.samsara.com/company/careers/roles/7721193 |
| The New York Times | ML Ops Engineer, Machine Learning & AI | 2026 | https://job-boards.greenhouse.io/thenewyorktimes/jobs/4655096005 |
| iCapital | DevOps Engineer - SVP (MLOps focus) | 2026 | https://job-boards.greenhouse.io/icapitalnetwork/jobs/8390699002 |
| Later | DevOps Engineer | 2026-05 | https://job-boards.greenhouse.io/later/jobs/8552308002 |
| Gong.io | Senior AI Infrastructure / MLOps Engineer | 2026-06-02 | https://job-boards.greenhouse.io/gongio/jobs/4684943006 |
| General Assembly | MLOps / AI Platform Engineer SME | 2026-04-22 | https://job-boards.greenhouse.io/generalassembly/jobs/7842854 |
| Prolific | Senior MLOps Engineer | 2026 | https://job-boards.greenhouse.io/prolific/jobs/4769093101 |
| DoorDash | Senior SWE, ML Infrastructure — GenAI | 2026 | https://job-boards.greenhouse.io/doordashusa/jobs/8044246 |
| Glean | MLE, LLM Evals & Observability | 2026 | https://job-boards.greenhouse.io/gleanwork/jobs/4669417005 |
| Sigma Computing | Senior AI/ML Engineer | 2026 | https://job-boards.greenhouse.io/sigmacomputing/jobs/7767728003 |
| Justworks | Senior IT Systems Engineer, AI (AI Operations) | 2026 | https://job-boards.greenhouse.io/justworks/jobs/7743119 |
| Medallion (First Layer AI) | Staff Machine Learning Engineer | 2026 | https://job-boards.greenhouse.io/medallionakafirstlayerai/jobs/4195457009 |
| Bloomreach | Engineering Manager, Infrastructure Team | 2026 | https://job-boards.greenhouse.io/bloomreach/jobs/7549131 |
| JetBrains | Senior MLOps Engineer (ML Workflows Engineering) | 2026 | https://job-boards.eu.greenhouse.io/jetbrains/jobs/4764813101 |
| Quanata | Senior Data Engineer, MLOps | 2026 | https://job-boards.greenhouse.io/quanata/jobs/5732610004 |
| NVIDIA | Senior MLOps Engineer, GenAI Framework | 2026 | https://jobs.nvidia.com/careers/job/893393550206 |
| Stripe | Software Engineer, ML Infrastructure | 2026 | https://stripe.com/jobs/listing/software-engineer-machine-learning-infrastructure/7528260 |
| Salesforce (Slack) | SWE (Multiple Levels) — ML Infrastructure, Slack | 2026-04-10 | https://careers.salesforce.com/en/jobs/jr329145/software-engineer-multiple-levels-machine-learning-infrastructure-slack/ |
| Toyota North America | MLOps Platform Engineer (SageMaker) | 2026-06-18 | https://toyota.willhire.co/jobs |
| Cloudflare | ML Engineer (ML Platform) | 2026 | https://startup.jobs/machine-learning-engineer-cloudflare-4764362 |
| JPMorgan Chase | Lead ML Engineer — MLOps | 2026-04 | https://bebee.com/us/jobs/lead-machine-learning-engineer-mlops-jpmorgan-chase-co-new-york--whatjobs-4881_3913826 |
| Together AI | Machine Learning, Platform Engineer | 2026 | https://job-boards.greenhouse.io/togetherai/jobs/4835988007 |
| Reddit | Senior MLE, ML Training Platform | 2026 | https://job-boards.greenhouse.io/reddit/jobs/7074776 |
| EarnIn | Staff ML Engineer (ML Platform) | 2026 | https://job-boards.greenhouse.io/earnin/jobs/6157785 |

## Requirement Frequencies (top signal)

| # | Requirement | Freq | Owner | Coverage |
|---|---|---|---|---|
| 1 | Kubernetes for ML training/serving | 0.76 | ai-infra-engineer (L20) | Applied across [mod-001](lessons/mod-001-mlops-foundations/), [project-02](projects/project-02-model-serving/), [project-05](projects/project-05-llmops/) |
| 2 | Python for ML tooling/services | 0.72 | ai-infra-junior-engineer (L10) | Prerequisite across all modules |
| 3 | CI/CD pipelines for ML | 0.64 | **mlops** | [mod-002](lessons/mod-002-experiment-tracking/), [mod-006](lessons/mod-006-automation/), [mod-009](lessons/mod-009-security/), [project-01](projects/project-01-ml-pipeline/) |
| 4 | MLflow / experiment tracking / model registry | 0.48 | **mlops** | [mod-002](lessons/mod-002-experiment-tracking/) (entire module) |
| 5 | Managed cloud ML platform (SageMaker / Vertex AI / Azure ML) | 0.44 | ai-infra-ml-platform (L30 companion) | Tooling landscape in [mod-001](lessons/mod-001-mlops-foundations/); depth owned by AI/ML Platform Engineer track |
| 6 | Terraform / IaC | 0.40 | ai-infra-engineer (L20) | Applied via `infrastructure/terraform/` stubs in [project-01](projects/project-01-ml-pipeline/), [project-02](projects/project-02-model-serving/) |
| 7 | Airflow / Kubeflow / orchestration | 0.40 | **mlops** | [mod-006](lessons/mod-006-automation/) (entire module) |
| 8 | Docker | 0.36 | ai-infra-junior-engineer (L10) | Prerequisite; applied throughout |
| 9 | Model monitoring / drift / observability | 0.32 | **mlops** | [mod-003](lessons/mod-003-model-monitoring/) (entire module) |
| 10 | LLM inference / serving (vLLM / Triton / TensorRT / Ray Serve) | 0.32 | **mlops** | [mod-010](lessons/mod-010-advanced-topics/) LLMOps section, [project-05](projects/project-05-llmops/) |
| 11 | Kubeflow Pipelines | 0.24 | **mlops** | [mod-006](lessons/mod-006-automation/) Kubeflow section |
| 12 | GCP Vertex AI | 0.24 | ai-infra-ml-platform (L30 companion) | Tooling landscape in [mod-001](lessons/mod-001-mlops-foundations/); depth in companion track |
| 13 | Weights & Biases | 0.20 | **mlops** | [mod-002](lessons/mod-002-experiment-tracking/) (MLflow alternative) |
| 14 | Ray distributed training/serving | 0.20 | ai-infra-ml-platform (L30 companion) | [mod-010](lessons/mod-010-advanced-topics/) Ray Serve mention |
| 15 | GPU orchestration and utilization | 0.20 | ai-infra-ml-platform (L30 companion) | [mod-008](lessons/mod-008-production-ops/) capacity planning; [project-05](projects/project-05-llmops/) |
| 16 | ArgoCD / Flux GitOps | 0.20 | ai-infra-engineer (L20) | GitHub Actions covered in projects; ArgoCD is DevOps baseline |
| 17 | SLO/SLI/incident response for ML | 0.20 | **mlops** | [mod-008](lessons/mod-008-production-ops/), [mod-003](lessons/mod-003-model-monitoring/) SLO section |
| 18 | LLM evaluation and observability (Langfuse / LangSmith / LLM-judge) | 0.20 | **mlops** | [mod-010](lessons/mod-010-advanced-topics/) LLM monitoring/evaluation; [project-05](projects/project-05-llmops/) monitoring |
| 19 | Feature store (Feast / Tecton / Hopsworks) | 0.16 | **mlops** | [mod-010](lessons/mod-010-advanced-topics/) Real-Time ML section |
| 20 | Cost optimization for LLM inference (caching, batching) | 0.16 | **mlops** | [mod-010](lessons/mod-010-advanced-topics/), [project-05](projects/project-05-llmops/) cost tracking |
| 21 | Secrets, secure model serving, supply-chain security | 0.16 | **mlops** | [mod-009](lessons/mod-009-security/) (entire module) |
| 22 | ML governance / compliance / audit | 0.16 | **mlops** | [mod-007](lessons/mod-007-governance/), [project-04](projects/project-04-governance/) |
| 23 | Real-time / streaming ML pipelines | 0.16 | ai-infra-ml-platform (L30 companion) | [mod-010](lessons/mod-010-advanced-topics/) Real-Time ML section |
| 24 | LLM fine-tuning (SFT/DPO/LoRA) | 0.08 | out-of-scope | External: Hugging Face PEFT, TRL |

## Grouped Coverage by Existing Module

### `mod-001-mlops-foundations` — MLOps fundamentals, maturity, tooling landscape
Covers: MLOps definition, lifecycle, maturity levels, versioning, automation, reproducibility, monitoring, governance principles, and the full tooling landscape (MLflow, Kubeflow, Airflow, Feast, Prometheus/Grafana, SageMaker/Vertex AI awareness).
Requirements covered: #1 (as context), #5 (landscape), #12 (landscape).

### `mod-002-experiment-tracking` — MLflow + Registry + CI/CD integration
Covers: MLflow tracking server (Postgres + MinIO), autologging, model signatures, pyfunc packaging, model registry with stage transitions, quality-gated promotion, CI integration for training runs.
Requirements covered: #3 (CI/CD portion), #4, #13.

### `mod-003-model-monitoring` — Drift detection, Prometheus/Grafana, SLO/SLI
Covers: data/concept/prediction drift, KS/PSI/Chi-square/Jensen-Shannon, Evidently, Prometheus metrics, Grafana dashboards, multi-channel alerting (PagerDuty/Slack), retraining triggers, SLO/SLI for ML systems.
Requirements covered: #9, #17.

### `mod-004-data-quality` — Validation and quality gates
Covers: schema validation, Pydantic, Great Expectations, custom expectations, quality scoring, CI/CD quality gates, production data quality monitoring, lineage.
Requirements covered: complements #3 (quality gates in CI).

### `mod-005-experimentation` — A/B testing and progressive rollout
Covers: A/B design, sample-size calculation, MABs (epsilon-greedy, Thompson, UCB, contextual), progressive rollout, Istio traffic splitting, canary analysis, segment analysis.
Requirements covered: production experimentation used in every above posting mentioning A/B or progressive rollout.

### `mod-006-automation` — Airflow + Kubeflow Pipelines
Covers: DAG design, Airflow operators/sensors/XCom, Kubeflow Pipelines SDK, retry logic, workflow monitoring, dynamic DAGs, retraining workflows.
Requirements covered: #7, #11.

### `mod-007-governance` — Approval workflows, fairness, GDPR/CCPA
Covers: multi-stage approvals, Fairlearn, model cards, tamper-proof audit logs (Merkle trees), GDPR right-to-explanation, data lineage, bias mitigation.
Requirements covered: #22.

### `mod-008-production-ops` — Capacity planning, incident response, runbooks
Covers: production readiness checklists, capacity planning (GPU vs CPU, storage), auto-scaling, SLO/SLI + error budgets, incident response, post-mortems, runbooks.
Requirements covered: #15 (planning depth), #17, feeds #10 latency work.

### `mod-009-security` — Secrets, secure serving, supply chain
Covers: OWASP ML Top 10, mTLS, HashiCorp Vault, secrets rotation, container image scanning (Trivy), SBOM/Sigstore/Cosign, differential privacy, incident response.
Requirements covered: #21, feeds #3 (secure CI/CD for ML).

### `mod-010-advanced-topics` — LLMOps, Edge, AutoML, Real-time
Covers: LLM deployment (vLLM, TGI, Ray Serve), inference optimization, prompt management, RAG operations, fine-tuning pipeline overview, LLM monitoring/evaluation, cost optimization for LLMs, real-time feature stores (Feast, Tecton, Hopsworks, Flink ML), edge deployment (TF Lite, ONNX), AutoML, federated learning.
Requirements covered: #10, #14, #18 (LLM monitoring/eval — sub-threshold), #19, #20, #23.

## Project Coverage

- **project-01-ml-pipeline** — end-to-end pipeline, CI/CD (GitHub Actions), Kubernetes deployment, drift detection, monitoring. Ties #3, #7, #9.
- **project-02-model-serving** — FastAPI + Kubernetes HPA, SLO/SLI monitoring, capacity planning, Vault, Pydantic validation. Ties #1, #17, #21.
- **project-03-experimentation** — MLflow + Optuna + Istio + Airflow + statsmodels. Ties #4, #7.
- **project-04-governance** — Fairlearn + audit logging + GDPR compliance + approval workflow. Ties #22.
- **project-05-llmops** — vLLM + LangChain + ChromaDB + prompt versioning + cost tracking + rate limiting. Ties #10, #18, #20.

## Coverage Owned Elsewhere (linked, not duplicated)

- **Kubernetes fundamentals**, **Docker**, **Python** → `ai-infra-junior-engineer-learning` / `ai-infra-engineer-learning`.
- **Terraform / IaC**, **ArgoCD / Flux GitOps** → `ai-infra-engineer-learning`.
- **Managed ML platform ops (SageMaker / Vertex AI / Azure ML)**, **GPU cluster orchestration**, **Ray distributed training/serving**, **real-time streaming ML pipelines** → `ai-infra-ml-platform-learning` (companion Level-30 track).

## Out-of-Scope Requirements

- **LLM fine-tuning (SFT/DPO/LoRA)** — 0.08 frequency; belongs to ML/Research Engineer roles. External resources: [Hugging Face PEFT](https://huggingface.co/docs/peft), [TRL](https://huggingface.co/docs/trl).

## Watch List (below threshold, revisit next cycle)

- **LLM evaluation harnesses (LangSmith, Langfuse, LLM-as-judge)** — 0.20 frequency. Curriculum touches LLM monitoring generically in mod-010 and project-05. If frequency clears 0.30 next cycle, propose one exercise added to `mod-010-advanced-topics` covering an eval harness end-to-end (offline eval dataset, judge model, dashboards).
- **ArgoCD / Flux GitOps for ML** — 0.20 frequency. If frequency clears 0.30 and ownership stays at Level 20, no MLOps-side action; otherwise propose an exercise added to `mod-006-automation` on GitOps for model rollout.

## Delta Proposal

No additions this cycle. Justification is captured in [`.aicg/curriculum-plan-delta.json`](.aicg/curriculum-plan-delta.json). No above-threshold requirement in the 25-posting sample lacks either existing coverage in this track or a cleaner owner at another level. Continuity bias applied.
