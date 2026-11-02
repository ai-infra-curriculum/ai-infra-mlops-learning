# MLOps Engineer — Job Requirements Coverage

**Role**: MLOps Engineer (level 30)
**Cycle**: 2026-10
**Postings sampled**: 25 (distinct employers, all posted 2026-07-16 through 2026-10-02)
**Machine-readable source**: [`.aicg/job-requirements.json`](.aicg/job-requirements.json)

## Method

- 25 postings pulled from Greenhouse, Lever, SmartRecruiters, Workable, direct corporate career pages (Pinterest, Databricks, Chime, Instacart, General Motors, Uber, Intuitive Surgical), and curated boards. Zero employer overlap with the 2026-09 sample — chosen deliberately so cycle-over-cycle deltas reflect market signal rather than posting continuity.
- Requirement frequency = fraction of the 25 postings that name the requirement explicitly.
- Ownership follows the "lowest-level role where genuinely required" rule. Where a companion role at the same level (e.g., AI/ML Platform Engineer, AI Infrastructure Performance Engineer) is a better fit, coverage is linked out rather than duplicated.
- Continuity bias: existing modules are not restructured; only novel, above-threshold, un-owned requirements would trigger additions. Removals are out of scope for this packet.

## Postings

| Employer | Title | Posted | URL |
|---|---|---|---|
| BEES (AB InBev) | Mid Level Machine Learning Engineer | 2026-07-22 | https://job-boards.greenhouse.io/bees/jobs/8645028002 |
| Hungryroot | Senior Machine Learning Operations Engineer | 2026-08-11 | https://job-boards.greenhouse.io/hungryroot/jobs/6141572004 |
| Interwell Health | Machine Learning Engineer | 2026-09-01 | https://job-boards.greenhouse.io/interwellhealth/jobs/5136653008 |
| Muon Space | Staff Software Engineer, IR Data Products | 2026-10-02 | https://job-boards.greenhouse.io/muonspace/jobs/5256159007 |
| Zscaler | Senior Machine Learning Engineer | 2026-09-30 | https://job-boards.greenhouse.io/zscaler/jobs/5246776007 |
| Tripadvisor | ML Ops Engineer II (Experiences) | 2026-09-22 | https://job-boards.greenhouse.io/tripadvisor/jobs/8222892 |
| Versant | Senior ML Engineer — AI Platform | 2026-08-20 | https://jobs.smartrecruiters.com/Versant3/744000143084859-senior-ml-engineer-ai-platform |
| Institute of Foundation Models (MBZUAI) | Senior MLOps Engineer | 2026-10-02 | https://jobs.lever.co/ifm-us/5f0feab3-1309-4c24-a703-ed1993c448b9 |
| Zoox | Software Engineer, ML Platform (ML Training) | 2026-07-20 | https://jobs.lever.co/zoox/d4108968-e83d-4d87-a92c-e4cd1823801c |
| Easygo | Senior Machine Learning Operations Engineer (MLOps) | 2026-09-11 | https://job-boards.greenhouse.io/easygo/jobs/5119804007 |
| Baton (Ryder Technology Lab) | Software Engineer, MLOps — Machine Learning | 2026-10-02 | https://job-boards.greenhouse.io/baton/jobs/5200002007 |
| Freenome | Senior Machine Learning Engineer | 2026-07-16 | https://job-boards.greenhouse.io/freenome/jobs/8535248002 |
| General Motors | Senior Machine Learning Engineer — ML Training Infrastructure | 2026-09-28 | https://search-careers.gm.com/en/jobs/jr-202618569/senior-machine-learning-engineer-ml-training-infrastructure/ |
| Uber | Senior Staff Machine Learning Engineer — Core Services Engineering | 2026-08-03 | https://jobs.uber.com/en/jobs/149797/ |
| Datavant | Staff ML Platform Engineer | 2026-09-26 | https://boards.greenhouse.io/datavant2/jobs/5425428008 |
| Mercury | Senior Machine Learning Operations Engineer | 2026-09-30 | https://job-boards.greenhouse.io/mercury/jobs/6186862004 |
| Pinterest | Sr. Staff Software Engineer, Product ML Infrastructure | 2026-10-02 | https://www.pinterestcareers.com/jobs/8046860/sr-staff-software-engineer-product-ml-infrastructure/ |
| Robinhood | Senior Machine Learning Engineer, AI Infra | 2026-09-25 | https://job-boards.greenhouse.io/robinhood/jobs/8189874 |
| Intuitive Surgical | Senior MLOps Engineer | 2026-08-06 | https://careers.intuitive.com/en/jobs/744000145565870/JOB218319/sr-machine-learning-engineer/ |
| Zeitview | Senior MLOps Engineer I | 2026-07-21 | https://zeitview.hire.trakstar.com/jobs/fk0zrn8/ |
| Atomic Machines | MLOps Engineer | 2026-08-27 | https://www.dice.com/job-detail/5b0c7ba9-6284-4d48-a18d-5f1d7d22265e |
| TetraScience | Lead Software Platform Engineer, MLOps | 2026-08-05 | https://apply.workable.com/tetrascience/j/7CEF637F8F/ |
| Databricks | Senior Software Engineer, Model Serving | 2026-09-21 | https://www.databricks.com/company/careers/engineering/senior-software-engineer-model-serving-8211648002 |
| Chime | Senior Software Engineer, Machine Learning Platform | 2026-08-10 | https://careers.chime.com/jobs/8004505002/senior-software-engineer-machine-learning-platform/ |
| Instacart | Senior Machine Learning Engineer, Digital Twin Platform | 2026-08-21 | https://www.instacart.careers/job?id=8143145 |

## Requirement Frequencies (top signal)

| # | Requirement | Freq | Δ vs 2026-09 | Owner | Coverage |
|---|---|---|---|---|---|
| 1 | Python for ML tooling/services | 0.80 | −0.13 | ai-infra-junior-engineer (L10) | Prerequisite across all modules |
| 2 | CI/CD pipelines for ML | 0.52 | +0.06 | **mlops** | [mod-002](lessons/mod-002-experiment-tracking/), [mod-006](lessons/mod-006-automation/), [mod-009](lessons/mod-009-security/), [project-01](projects/project-01-ml-pipeline/) |
| 3 | MLflow / experiment tracking / model registry | 0.52 | +0.23 | **mlops** | [mod-002](lessons/mod-002-experiment-tracking/) (entire module) |
| 4 | Terraform / IaC | 0.52 | +0.27 | ai-infra-engineer (L20) | Applied via `infrastructure/terraform/` stubs in [project-01](projects/project-01-ml-pipeline/), [project-02](projects/project-02-model-serving/) |
| 5 | Model monitoring / drift / observability | 0.52 | −0.05 | **mlops** | [mod-003](lessons/mod-003-model-monitoring/) (entire module) |
| 6 | Kubernetes for ML training/serving | 0.40 | +0.01 | ai-infra-engineer (L20) | Applied across [mod-001](lessons/mod-001-mlops-foundations/), [project-02](projects/project-02-model-serving/), [project-05](projects/project-05-llmops/) |
| 7 | Managed cloud ML platform (SageMaker / Vertex AI / Azure ML / Databricks) | 0.36 | 0.00 | ai-infra-ml-platform (L30 companion) | Tooling landscape in [mod-001](lessons/mod-001-mlops-foundations/); depth owned by [AI/ML Platform Engineer track](../ai-infra-ml-platform-learning/) |
| 8 | Docker | 0.36 | 0.00 | ai-infra-junior-engineer (L10) | Prerequisite; applied throughout |
| 9 | GPU orchestration and utilization | 0.32 | +0.14 | ai-infra-ml-platform (L30 companion) | [mod-008](lessons/mod-008-production-ops/) capacity planning; [project-05](projects/project-05-llmops/); depth in companion track |
| 10 | LLM inference / serving (vLLM / Triton / TensorRT / Ray Serve / SGLang / KServe) | 0.28 | +0.07 | **mlops** | [mod-010](lessons/mod-010-advanced-topics/) LLMOps section, [project-05](projects/project-05-llmops/) |
| 11 | Feature store (Feast / Tecton / Hopsworks) | 0.24 | +0.20 | **mlops** | [mod-010](lessons/mod-010-advanced-topics/) Real-Time ML section |
| 12 | Ray distributed training/serving | 0.20 | +0.09 | ai-infra-ml-platform (L30 companion) | [mod-010](lessons/mod-010-advanced-topics/) Ray Serve mention |
| 13 | LLM evaluation and observability (Langfuse / LangSmith / LLM-judge / eval frameworks) | 0.20 | +0.16 | **mlops** | [mod-010](lessons/mod-010-advanced-topics/) LLM monitoring; [project-05](projects/project-05-llmops/) |
| 14 | Distributed training / inference at scale (FSDP, DeepSpeed, Pipeline Parallelism) | 0.16 | +0.09 | ai-infra-ml-platform (L30 companion) + ai-infra-performance (L35) | [mod-010](lessons/mod-010-advanced-topics/) LLMOps adjacent; depth in companion/performance tracks |
| 15 | Kubeflow Pipelines | 0.16 | +0.09 | **mlops** | [mod-006](lessons/mod-006-automation/) Kubeflow section |
| 16 | SLO/SLI/incident response for ML | 0.16 | +0.05 | **mlops** | [mod-008](lessons/mod-008-production-ops/), [mod-003](lessons/mod-003-model-monitoring/) SLO section |
| 17 | Airflow orchestration (named) | 0.12 | −0.02 | **mlops** | [mod-006](lessons/mod-006-automation/) Airflow module |
| 18 | Agentic systems in production (LangGraph, agent eval, tool use) | 0.12 | **−0.20** | **mlops** | Pending from 2026-09 proposal: `mod-010 exercise-06` (not yet merged). See watch-list note below. |
| 19 | Cost optimization for LLM inference | 0.12 | +0.01 | **mlops** | [mod-010](lessons/mod-010-advanced-topics/), [project-05](projects/project-05-llmops/) cost tracking |
| 20 | ArgoCD / Flux / Argo Workflows GitOps | 0.12 | +0.08 | ai-infra-engineer (L20) | GitHub Actions in projects; ArgoCD is DevOps baseline |
| 21 | Governance / compliance / audit | 0.08 | +0.01 | **mlops** | [mod-007](lessons/mod-007-governance/), [project-04](projects/project-04-governance/) |
| 22 | Secrets / secure serving / supply chain | 0.08 | +0.01 | **mlops** | [mod-009](lessons/mod-009-security/) (entire module) |
| 23 | Weights & Biases | 0.08 | +0.04 | **mlops** | [mod-002](lessons/mod-002-experiment-tracking/) MLflow alternative |
| 24 | Real-time / streaming ML (Kafka, Flink) | 0.08 | +0.01 | ai-infra-ml-platform (L30 companion) | [mod-010](lessons/mod-010-advanced-topics/) Real-Time ML section |
| 25 | MCP (Model Context Protocol) | 0.04 | −0.10 | watch_list | n/a — bundles with agentic-systems if signal returns |
| 26 | Vector DB (ChromaDB / Pinecone / Weaviate / pgvector) | 0.04 | −0.07 | **mlops** | [project-05](projects/project-05-llmops/) (ChromaDB) |
| 27 | LLM fine-tuning (SFT/DPO/LoRA) | 0.04 | 0.00 | out-of-scope | External: Hugging Face PEFT, TRL |
| 28 | GCP Vertex AI (named) | 0.00 | −0.07 | ai-infra-ml-platform (L30 companion) | Tooling landscape in [mod-001](lessons/mod-001-mlops-foundations/) |

## Grouped Coverage by Existing Module

### `mod-001-mlops-foundations` — MLOps fundamentals, maturity, tooling landscape
Covers: MLOps definition, lifecycle, maturity levels, versioning, automation, reproducibility, monitoring, governance principles, and the full tooling landscape (MLflow, Kubeflow, Airflow, Feast, Prometheus/Grafana, SageMaker/Vertex AI/Databricks awareness).
Requirements covered: #6 (as context), #7 (landscape), #28 (landscape).

### `mod-002-experiment-tracking` — MLflow + Registry + CI/CD integration
Covers: MLflow tracking server (Postgres + MinIO), autologging, model signatures, pyfunc packaging, model registry with stage transitions, quality-gated promotion, CI integration for training runs.
Requirements covered: #2 (CI/CD portion), #3, #23.

### `mod-003-model-monitoring` — Drift detection, Prometheus/Grafana, SLO/SLI
Covers: data/concept/prediction drift, KS/PSI/Chi-square/Jensen-Shannon, Evidently, Prometheus metrics, Grafana dashboards, multi-channel alerting (PagerDuty/Slack), retraining triggers, SLO/SLI for ML systems.
Requirements covered: #5, #16.

### `mod-004-data-quality` — Validation and quality gates
Covers: schema validation, Pydantic, Great Expectations, custom expectations, quality scoring, CI/CD quality gates, production data quality monitoring, lineage.
Requirements covered: complements #2 (quality gates in CI).

### `mod-005-experimentation` — A/B testing and progressive rollout
Covers: A/B design, sample-size calculation, MABs (epsilon-greedy, Thompson, UCB, contextual), progressive rollout, Istio traffic splitting, canary analysis, segment analysis.
Requirements covered: production experimentation implied by any posting mentioning A/B or progressive rollout.

### `mod-006-automation` — Airflow + Kubeflow Pipelines
Covers: DAG design, Airflow operators/sensors/XCom, Kubeflow Pipelines SDK, retry logic, workflow monitoring, dynamic DAGs, retraining workflows.
Requirements covered: #15, #17.

### `mod-007-governance` — Approval workflows, fairness, GDPR/CCPA
Covers: multi-stage approvals, Fairlearn, model cards, tamper-proof audit logs (Merkle trees), GDPR right-to-explanation, data lineage, bias mitigation.
Requirements covered: #21.

### `mod-008-production-ops` — Capacity planning, incident response, runbooks
Covers: production readiness checklists, capacity planning (GPU vs CPU, storage), auto-scaling, SLO/SLI + error budgets, incident response, post-mortems, runbooks.
Requirements covered: #9 (planning depth), #16, feeds #10 latency work.

### `mod-009-security` — Secrets, secure serving, supply chain
Covers: OWASP ML Top 10, mTLS, HashiCorp Vault, secrets rotation, container image scanning (Trivy), SBOM/Sigstore/Cosign, differential privacy, incident response.
Requirements covered: #22, feeds #2 (secure CI/CD for ML).

### `mod-010-advanced-topics` — LLMOps, Edge, AutoML, Real-time
Covers: LLM deployment (vLLM, TGI, Ray Serve), inference optimization, prompt management, RAG operations, fine-tuning pipeline overview, LLM monitoring/evaluation, cost optimization for LLMs, real-time feature stores (Feast, Tecton, Hopsworks, Flink ML), edge deployment (TF Lite, ONNX), AutoML, federated learning.
Requirements covered: #10, #11, #13 (sub-threshold), #19, #24. **Pending from 2026-09 cycle**: `exercise-06-agentic-systems-in-production` (not yet merged; see Watch List).

## Project Coverage

- **project-01-ml-pipeline** — end-to-end pipeline, CI/CD (GitHub Actions), Kubernetes deployment, drift detection, monitoring. Ties #2, #5, #15.
- **project-02-model-serving** — FastAPI + Kubernetes HPA, SLO/SLI monitoring, capacity planning, Vault, Pydantic validation. Ties #6, #16, #22.
- **project-03-experimentation** — MLflow + Optuna + Istio + Airflow + statsmodels. Ties #3, #17.
- **project-04-governance** — Fairlearn + audit logging + GDPR compliance + approval workflow. Ties #21.
- **project-05-llmops** — vLLM + LangChain + ChromaDB + prompt versioning + cost tracking + rate limiting. Ties #10, #13, #19, #26.

## Coverage Owned Elsewhere (linked, not duplicated)

- **Kubernetes fundamentals**, **Docker**, **Python** → [`ai-infra-junior-engineer-learning`](../ai-infra-junior-engineer-learning/) / [`ai-infra-engineer-learning`](../ai-infra-engineer-learning/).
- **Terraform / IaC**, **ArgoCD / Flux / Argo Workflows GitOps** → [`ai-infra-engineer-learning`](../ai-infra-engineer-learning/).
- **Managed ML platform ops (SageMaker / Vertex AI / Azure ML / Databricks)**, **GPU cluster orchestration**, **Ray distributed training/serving**, **real-time streaming ML pipelines** → [`ai-infra-ml-platform-learning`](../ai-infra-ml-platform-learning/) (companion Level-30 track).
- **Distributed training / inference at scale (FSDP, DeepSpeed, Pipeline Parallelism, kernel/mem optimization)** → [`ai-infra-ml-platform-learning`](../ai-infra-ml-platform-learning/) and [`ai-infra-performance-learning`](../ai-infra-performance-learning/) (L35).

## Out-of-Scope Requirements

- **LLM fine-tuning (SFT/DPO/LoRA)** — 0.04 frequency; belongs to ML/Research Engineer roles. External resources: [Hugging Face PEFT](https://huggingface.co/docs/peft), [TRL](https://huggingface.co/docs/trl).

## Watch List (below threshold, revisit next cycle)

- **Agentic systems in production** — 0.12 this cycle (down from 0.32 in 2026-09). Explicit hits: Zscaler (LangGraph, tool/function calling, multi-step orchestration), TetraScience (agents + MCP in production), Zeitview (LLM/agentic nice-to-have). The 2026-09 cycle's proposed `mod-010 exercise-06-agentic-systems-in-production` is still pending and NOT withdrawn this cycle (removals are out of scope). If the signal remains below 0.30 in the next cycle, open a separate withdrawal proposal rather than merging exercise-06.
- **Model Context Protocol (MCP)** — 0.04 (down from 0.14). Receded alongside agentic systems. Bundles conceptually with the agentic-systems requirement; no standalone action.
- **LLM inference / serving** — 0.28, +0.07. Just under the 0.30 line. SGLang and KServe newly named at MBZUAI and Tripadvisor. If next cycle clears 0.30 with those names persisting, propose extending `mod-010-advanced-topics` LLMOps section to add KServe/SGLang explicitly as deployment options.
- **Feature store (Feast / Tecton / Hopsworks)** — 0.24, +0.20. Significant jump driven by platform-engineer postings (BEES, Baton, Robinhood, Chime, Pinterest, Atomic Machines). Currently a sub-section of mod-010. If next cycle clears 0.30, consider promoting feature-store from a mod-010 sub-section to its own dedicated exercise under mod-010 (not a new module — mod-010 is the right home per ownership).
- **LLM evaluation harnesses (LangSmith / Langfuse / LLM-as-judge / eval frameworks)** — 0.20, +0.16. Evaluation-framework language reappeared this cycle (Interwell, Datavant, TetraScience, Versant, Zeitview) but named vendors (LangSmith/Langfuse) are still not showing. If next cycle clears 0.30 AND named vendors appear, propose one exercise added to `mod-010-advanced-topics` covering an eval harness end-to-end (offline eval dataset, judge model, dashboards).
- **GPU orchestration** — 0.32, +0.14. Just above threshold, but signal is from distributed-training infra postings. Ownership rule unchanged — stays with `ai-infra-ml-platform-learning`.
- **Distributed training / inference at scale (FSDP, DeepSpeed, Pipeline Parallelism)** — 0.16, +0.09. Resurgent via GM, Zoox, Pinterest, Freenome. Ownership stays with `ai-infra-ml-platform-learning` and `ai-infra-performance-learning`.
- **ArgoCD / Argo Workflows for ML** — 0.12. Named at Tripadvisor, Intuitive Surgical, Muon Space. Ownership stays at L20; no MLOps-side action unless frequency jumps and L20 explicitly declines ownership.

## Delta Proposal

**No additions this cycle.** Justification is captured in [`.aicg/curriculum-plan-delta.json`](.aicg/curriculum-plan-delta.json).

No above-threshold requirement in the 25-posting sample lacks either existing coverage in this track or a cleaner owner at another level. The 2026-09 pending proposal (`mod-010 exercise-06 agentic systems in production`) is not re-proposed, not withdrawn, and left for the runner to adjudicate — this cycle's data shows the signal receded (0.32 → 0.12), but removals are explicitly out of scope for this packet per the continuity bias.
