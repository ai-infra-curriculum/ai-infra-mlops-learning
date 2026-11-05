# MLOps Engineer — Job Requirements Coverage

**Role**: MLOps Engineer (level 30)
**Cycle**: 2026-11
**Postings sampled**: 25 (distinct employers, posted 2026-08-10 through 2026-11-04)
**Machine-readable source**: [`.aicg/job-requirements.json`](.aicg/job-requirements.json)

## Method

- 25 postings pulled from Greenhouse, Lever, A16Z portfolio board, SmartRecruiters, and the usual secondary aggregators where employer-direct pages render client-side (freehire.me, zapply.jobs, dynamitejobs.com, sportstechjobs.com, jobsfordevelopers.com). Evidence quotes are extracted from the posting body in every case. Zero employer overlap with the 2026-10 sample — rotation is deliberate so cycle-over-cycle deltas reflect market signal rather than posting continuity.
- Role families covered: MLOps Engineer, ML Platform Engineer, ML Infrastructure Engineer, Senior/Staff Software Engineer (Model Serving / Ads ML / Matchmaking), Senior AI Platform Engineer.
- Requirement frequency = fraction of the 25 postings that name the requirement explicitly in the Requirements, Responsibilities, or Nice-to-have sections.
- Ownership follows the "lowest-level role where genuinely required" rule. Where a companion role at the same level (e.g., AI/ML Platform Engineer, AI Infrastructure Performance Engineer) is a better fit, coverage is linked out rather than duplicated.
- Continuity bias: existing modules are not restructured; only novel, above-threshold, un-owned requirements would trigger additions. Removals are out of scope for this packet.

## Postings

| Employer | Title | Posted | URL |
|---|---|---|---|
| DoorDash | Software Engineer, ML Serving Platform | 2026-10-08 | https://zapply.jobs/jobs/1b7c7025-c63e-4270-8a7d-1faf35de476f/ |
| Anthropic | Staff+ Software Engineer, Account Abuse (Machine Learning) | 2026-09-29 | https://jobs.generalcatalyst.com/companies/anthropic/jobs/95151469-staff-software-engineer-account-abuse-machine-learning |
| AiDASH | Staff MLOps Engineer | 2026-10-10 | https://freehire.me/jobs/staff-mlops-engineer-aidash-inc-xxicxm6y |
| KNOREX | MLOps Engineer | 2026-10-13 | https://freehire.me/jobs/mlops-engineer-knorex-ycoir46m |
| The Aerospace Corporation | Senior ML Ops / AI Ops Engineer | 2026-10-30 | https://zapply.jobs/jobs/0b588fc7-607e-4652-a721-00ff0b5aa4a0/ |
| Fractal | MLOps Engineer | 2026-10-07 | https://freehire.me/jobs/mlops-engineer-fractal-7nmqmnez |
| Coinflow | ML Ops Engineer | 2026-10-30 | https://zapply.jobs/jobs/1c52a415-5e1f-4878-8b5d-9c20806d33e0/ |
| FutureFit AI | Staff ML Platform Engineer (MLOps) | 2026-11-03 | https://dynamitejobs.com/company/futurefitai/remote-job/staff-ml-platform-engineer-mlops |
| Cursor (Anysphere) | Software Engineer, ML Platform | 2026-08-31 | https://jobs.a16z.com/jobs/cursor/167f0e93-6915-4d56-803a-be89d1441fb5--software-engineer-ml-platform |
| Valarian Technologies | MLOps Engineer | 2026-10-22 | https://freehire.me/jobs/mlops-engineer-valarian-w76ul3hy |
| Elsevier | Senior MLOps Engineer | 2026-10-23 | https://freehire.me/jobs/senior-mlops-engineer-elsevier-hqsdch4z |
| KAPI LLC | Senior MLOps Engineer — Snowflake | 2026-08-27 | https://freehire.me/jobs/senior-mlops-engineer-snowflake-kapi-llc-qdil2am3 |
| Agoda | Senior / Staff MLOps Engineer | 2026-10-16 | https://freehire.me/jobs/data-engineer-senior-staff-mlops-engineer-bangkok-based-relocation-provided-agoda-bptj4ts2 |
| Reddit | Senior Staff Machine Learning Systems Engineer, Ads ML Platform | 2026-08-26 | https://jobsfordevelopers.com/jobs/senior-staff-machine-learning-systems-engineer-ads-ml-platform-at-redditinc-com-aug-26-2026-8a4341 |
| emagine | Senior MLOps Engineer | 2026-10-07 | https://freehire.me/jobs/senior-mlops-engineer-emagine-5tex4gcg |
| Nearmap | Senior Machine Learning Engineer (Platform / MLOps) | 2026-08-10 | https://freehire.me/jobs/senior-machine-learning-engineer-platform-mlops-jobr-pro-eegotwre |
| Sigma Software | Senior MLOps / ML Platform Engineer | 2026-09-10 | https://freehire.me/jobs/senior-mlops-ml-platform-engineer-sigma-software-cfpl2xbo |
| Talentcross | MLOps Engineer | 2026-10-23 | https://freehire.me/jobs/mlops-engineer-talentcross-uzhzonqk |
| Roblox | Senior Machine Learning Infrastructure Engineer, Matchmaking | 2026-11-04 | https://sportstechjobs.com/senior-machine-learning-infrastructure-engineer-matchmaking-roblox/6aeaa2428b16010be3e174d4 |
| Coinbase | Senior Machine Learning Platform Engineer (Platform — Identity) | 2026-09-18 | https://zapply.jobs/jobs/e6a58759-62d9-470b-ad69-37be3f811843/ |
| EarnIn | Senior AI Platform Engineer | 2026-09-15 | https://job-boards.greenhouse.io/earnin/jobs/8202930 |
| Shield AI | Staff Software Engineer, ML Platform (6244) | 2026-11-02 | https://jobs.lever.co/shieldai/82e0ffd1-3887-4253-b458-00f39e0a387f |
| Censys | Senior Machine Learning Engineer | 2026-08-26 | https://job-boards.greenhouse.io/censys/jobs/8731027002 |
| Kard Financial | Senior Machine Learning Engineer | 2026-08-13 | https://job-boards.greenhouse.io/kardfinancialinc/jobs/4730993005 |
| Jampp | Senior Machine Learning Engineer | 2026-09-04 | https://job-boards.greenhouse.io/jampp/jobs/8178847 |

## Requirement Frequencies (top signal)

| # | Requirement | Freq | Δ vs 2026-10 | Owner | Coverage |
|---|---|---|---|---|---|
| 1 | Python for ML tooling/services | 0.72 | −0.08 | ai-infra-junior-engineer (L10) | Prerequisite across all modules |
| 2 | Kubernetes for ML training/serving | 0.68 | **+0.28** | ai-infra-engineer (L20) | Applied across [mod-001](lessons/mod-001-mlops-foundations/), [project-02](projects/project-02-model-serving/), [project-05](projects/project-05-llmops/) |
| 3 | MLflow / experiment tracking / model registry | 0.56 | +0.04 | **mlops** | [mod-002](lessons/mod-002-experiment-tracking/) (entire module) |
| 4 | CI/CD pipelines for ML | 0.52 | 0.00 | **mlops** | [mod-002](lessons/mod-002-experiment-tracking/), [mod-006](lessons/mod-006-automation/), [mod-009](lessons/mod-009-security/), [project-01](projects/project-01-ml-pipeline/) |
| 5 | Managed cloud ML platform (SageMaker / Vertex AI / Azure ML / Databricks) | 0.44 | +0.08 | ai-infra-ml-platform (L30 companion) | Tooling landscape in [mod-001](lessons/mod-001-mlops-foundations/); depth in [AI/ML Platform Engineer track](../ai-infra-ml-platform-learning/) |
| 6 | Model monitoring / drift / observability | 0.36 | −0.16 | **mlops** | [mod-003](lessons/mod-003-model-monitoring/) (entire module) |
| 7 | Docker | 0.36 | 0.00 | ai-infra-junior-engineer (L10) | Prerequisite; applied throughout |
| 8 | Feature store (Feast / Tecton / Hopsworks / Chronon / Databricks) | 0.32 | **+0.08** | **mlops** | [mod-010 exercise-05-real-time-ml-with-feature-stores](lessons/mod-010-advanced-topics/exercises/exercise-05-real-time-ml-with-feature-stores.md) (120-min Feast end-to-end) |
| 9 | Terraform / IaC | 0.28 | −0.24 | ai-infra-engineer (L20) | Applied via `infrastructure/terraform/` in [project-01](projects/project-01-ml-pipeline/), [project-02](projects/project-02-model-serving/) |
| 10 | LLM inference / serving (vLLM / Triton / TensorRT-LLM / Ray Serve / SGLang / KServe / BentoML / TGI) | 0.28 | 0.00 | **mlops** | [mod-010 exercise-01-llmops-with-vllm-serving](lessons/mod-010-advanced-topics/exercises/exercise-01-llmops-with-vllm-serving.md), [project-05](projects/project-05-llmops/) |
| 11 | Real-time / streaming ML pipelines (Kafka / Flink / Spark Streaming / Beam) | 0.28 | **+0.20** | ai-infra-ml-platform (L30 companion) | [mod-010 Real-Time ML section](lessons/mod-010-advanced-topics/) + exercise-05; depth in companion track |
| 12 | Airflow orchestration | 0.24 | +0.12 | **mlops** | [mod-006](lessons/mod-006-automation/) Airflow module |
| 13 | Kubeflow Pipelines | 0.24 | +0.08 | **mlops** | [mod-006](lessons/mod-006-automation/) Kubeflow section |
| 14 | ArgoCD / Flux / Argo Workflows GitOps | 0.24 | +0.12 | ai-infra-engineer (L20) | GitHub Actions in projects; ArgoCD is DevOps baseline |
| 15 | GPU orchestration and utilization | 0.20 | −0.12 | ai-infra-ml-platform (L30 companion) | [mod-008](lessons/mod-008-production-ops/) capacity planning; [project-05](projects/project-05-llmops/) |
| 16 | Agentic systems in production (LangGraph / LangChain / CrewAI / AutoGen / LlamaIndex) | 0.16 | +0.04 | **mlops** | Pending 2026-10 proposal: `mod-010 exercise-06` (not yet merged). See watch list. |
| 17 | Ray distributed training/serving | 0.16 | −0.04 | ai-infra-ml-platform (L30 companion) | [mod-010](lessons/mod-010-advanced-topics/) Ray Serve mention |
| 18 | Distributed training / inference at scale (FSDP / DeepSpeed / Pipeline Parallelism) | 0.16 | 0.00 | ai-infra-ml-platform (L30 companion) + ai-infra-performance (L35) | [mod-010](lessons/mod-010-advanced-topics/) LLMOps adjacent; depth in companion/performance tracks |
| 19 | SLO/SLI/incident response for ML | 0.16 | 0.00 | **mlops** | [mod-008](lessons/mod-008-production-ops/), [mod-003](lessons/mod-003-model-monitoring/) SLO section |
| 20 | Vector DB (Pinecone / Weaviate / Qdrant / Milvus / pgvector / Chroma) | 0.12 | +0.08 | **mlops** | [project-05](projects/project-05-llmops/) (ChromaDB), [mod-010 exercise-02 RAG](lessons/mod-010-advanced-topics/exercises/exercise-02-rag-system-implementation.md) |
| 21 | Cost optimization for LLM inference | 0.12 | 0.00 | **mlops** | [mod-010](lessons/mod-010-advanced-topics/), [project-05](projects/project-05-llmops/) cost tracking |
| 22 | Weights & Biases | 0.12 | +0.04 | **mlops** | [mod-002](lessons/mod-002-experiment-tracking/) MLflow alternative |
| 23 | Data versioning (DVC / lakeFS) | 0.12 | *new* | **mlops** | [mod-004](lessons/mod-004-data-quality/) data lineage, [mod-002](lessons/mod-002-experiment-tracking/) artifact versioning |
| 24 | Shadow / canary / champion-challenger deployment patterns | 0.12 | *new* | **mlops** | [mod-005](lessons/mod-005-experimentation/) (A/B, MABs, canary), [mod-008](lessons/mod-008-production-ops/) |
| 25 | OpenTelemetry distributed tracing | 0.12 | *new* | ai-infra-engineer (L20) | L20 observability; complementary mod-003 coverage |
| 26 | AI-assisted development (Claude Code / AI coding assistants as expected tooling) | 0.12 | *new* | emerging | n/a — emerging signal |
| 27 | LLM evaluation and observability (Langfuse / LangSmith / LLM-judge / eval frameworks) | 0.08 | −0.12 | **mlops** | [mod-010](lessons/mod-010-advanced-topics/) LLM monitoring; [project-05](projects/project-05-llmops/) |
| 28 | Governance / compliance / audit | 0.04 | −0.04 | **mlops** | [mod-007](lessons/mod-007-governance/), [project-04](projects/project-04-governance/) |
| 29 | Secrets / secure serving / supply chain | 0.04 | −0.04 | **mlops** | [mod-009](lessons/mod-009-security/) (entire module) |
| 30 | MCP (Model Context Protocol) | 0.00 | −0.04 | watch_list | n/a — bundles with agentic-systems |
| 31 | LLM fine-tuning (SFT / DPO / LoRA / PEFT) | 0.00 | −0.04 | out-of-scope | External: Hugging Face PEFT, TRL |

## Grouped Coverage by Existing Module

### `mod-001-mlops-foundations` — MLOps fundamentals, maturity, tooling landscape
Covers: MLOps definition, lifecycle, maturity levels, versioning, automation, reproducibility, monitoring, governance principles, and the full tooling landscape (MLflow, Kubeflow, Airflow, Feast, Prometheus/Grafana, SageMaker/Vertex AI/Databricks awareness).
Requirements covered: #2 (as context), #5 (landscape).

### `mod-002-experiment-tracking` — MLflow + Registry + CI/CD integration
Covers: MLflow tracking server (Postgres + MinIO), autologging, model signatures, pyfunc packaging, model registry with stage transitions, quality-gated promotion, CI integration for training runs.
Requirements covered: #3, #4 (CI/CD portion), #22.

### `mod-003-model-monitoring` — Drift detection, Prometheus/Grafana, SLO/SLI
Covers: data/concept/prediction drift, KS/PSI/Chi-square/Jensen-Shannon, Evidently, Prometheus metrics, Grafana dashboards, multi-channel alerting (PagerDuty/Slack), retraining triggers, SLO/SLI for ML systems.
Requirements covered: #6, #19.

### `mod-004-data-quality` — Validation and quality gates
Covers: schema validation, Pydantic, Great Expectations, custom expectations, quality scoring, CI/CD quality gates, production data quality monitoring, lineage.
Requirements covered: complements #4 (quality gates in CI), #23 (lineage).

### `mod-005-experimentation` — A/B testing and progressive rollout
Covers: A/B design, sample-size calculation, MABs (epsilon-greedy, Thompson, UCB, contextual), progressive rollout, Istio traffic splitting, canary analysis, segment analysis.
Requirements covered: #24 (shadow/canary/champion-challenger), production experimentation implied by any posting mentioning A/B or progressive rollout.

### `mod-006-automation` — Airflow + Kubeflow Pipelines
Covers: DAG design, Airflow operators/sensors/XCom, Kubeflow Pipelines SDK, retry logic, workflow monitoring, dynamic DAGs, retraining workflows.
Requirements covered: #12, #13.

### `mod-007-governance` — Approval workflows, fairness, GDPR/CCPA
Covers: multi-stage approvals, Fairlearn, model cards, tamper-proof audit logs (Merkle trees), GDPR right-to-explanation, data lineage, bias mitigation.
Requirements covered: #28.

### `mod-008-production-ops` — Capacity planning, incident response, runbooks
Covers: production readiness checklists, capacity planning (GPU vs CPU, storage), auto-scaling, SLO/SLI + error budgets, incident response, post-mortems, runbooks.
Requirements covered: #15 (planning depth), #19, #24, feeds #10 latency work.

### `mod-009-security` — Secrets, secure serving, supply chain
Covers: OWASP ML Top 10, mTLS, HashiCorp Vault, secrets rotation, container image scanning (Trivy), SBOM/Sigstore/Cosign, differential privacy, incident response.
Requirements covered: #29, feeds #4 (secure CI/CD for ML).

### `mod-010-advanced-topics` — LLMOps, Edge, AutoML, Real-time
Covers: LLM deployment (vLLM, TGI, Ray Serve), inference optimization, prompt management, RAG operations, fine-tuning pipeline overview, LLM monitoring/evaluation, cost optimization for LLMs, real-time feature stores (Feast, Tecton, Hopsworks, Flink ML), edge deployment (TF Lite, ONNX), AutoML, federated learning. Exercises: `exercise-01-llmops-with-vllm-serving`, `exercise-02-rag-system-implementation`, `exercise-03-edge-ml-optimization`, `exercise-04-automl-pipeline`, `exercise-05-real-time-ml-with-feature-stores`.
Requirements covered: #8 (feature store — dedicated exercise-05), #10, #11 (Real-Time ML section), #17 (Ray Serve mention), #20, #21, #27 (sub-threshold). **Pending from 2026-10 cycle**: `exercise-06-agentic-systems-in-production` (not yet merged; see Watch List).

## Project Coverage

- **project-01-ml-pipeline** — end-to-end pipeline, CI/CD (GitHub Actions), Kubernetes deployment, drift detection, monitoring. Ties #4, #6, #13.
- **project-02-model-serving** — FastAPI + Kubernetes HPA, SLO/SLI monitoring, capacity planning, Vault, Pydantic validation. Ties #2, #19, #29.
- **project-03-experimentation** — MLflow + Optuna + Istio + Airflow + statsmodels. Ties #3, #12.
- **project-04-governance** — Fairlearn + audit logging + GDPR compliance + approval workflow. Ties #28.
- **project-05-llmops** — vLLM + LangChain + ChromaDB + prompt versioning + cost tracking + rate limiting. Ties #10, #20, #21, #27.

## Coverage Owned Elsewhere (linked, not duplicated)

- **Kubernetes fundamentals**, **Docker**, **Python** → [`ai-infra-junior-engineer-learning`](../ai-infra-junior-engineer-learning/) / [`ai-infra-engineer-learning`](../ai-infra-engineer-learning/).
- **Terraform / IaC**, **ArgoCD / Flux / Argo Workflows GitOps**, **OpenTelemetry fundamentals** → [`ai-infra-engineer-learning`](../ai-infra-engineer-learning/).
- **Managed ML platform ops (SageMaker / Vertex AI / Azure ML / Databricks)**, **GPU cluster orchestration**, **Ray distributed training/serving**, **real-time streaming ML pipelines (Kafka / Flink / Spark Streaming / Beam)** → [`ai-infra-ml-platform-learning`](../ai-infra-ml-platform-learning/) (companion Level-30 track).
- **Distributed training / inference at scale (FSDP, DeepSpeed, Pipeline Parallelism, kernel/mem optimization)** → [`ai-infra-ml-platform-learning`](../ai-infra-ml-platform-learning/) and [`ai-infra-performance-learning`](../ai-infra-performance-learning/) (L35).

## Out-of-Scope Requirements

- **LLM fine-tuning (SFT / DPO / LoRA / PEFT)** — 0.00 frequency this cycle; belongs to ML/Research Engineer roles. External resources: [Hugging Face PEFT](https://huggingface.co/docs/peft), [TRL](https://huggingface.co/docs/trl).

## Watch List (below threshold, revisit next cycle)

- **LLM inference / serving** — 0.28, flat for three cycles. Named vendor coverage keeps expanding (this cycle: vLLM, TGI, Ollama, TensorRT-LLM at Valarian; TF Serving/TorchServe/Triton/Seldon/KServe at Aerospace; Ray Serve at Nearmap). If next cycle clears 0.30, extend `mod-010 exercise-01-llmops-with-vllm-serving` to add KServe and TensorRT-LLM as parallel deployment tracks — do not create a new exercise.
- **Real-time / streaming ML pipelines (Kafka / Flink / Spark Streaming / Beam)** — 0.28, **+0.20** vs 2026-10. Reddit (Ads ML), Roblox (Matchmaking), Anthropic (Abuse), Coinbase (Identity), emagine, Talentcross, Fractal all name streaming/event-driven feature pipelines. Just below the gate. Ownership stays with `ai-infra-ml-platform-learning`; mod-010 Real-Time ML section + exercise-05 are the MLOps-level touchpoint. If next cycle clears 0.30 AND Streaming-specific skills (watermarking, exactly-once, backfills) remain MLOps-flavored, revisit ownership.
- **Agentic systems in production** — 0.16 (2026-11), 0.12 (2026-10), 0.32 (2026-09). Three cycles sub-threshold around a noisy mean of ~0.20. Explicit this cycle: Valarian (LangChain/LangGraph/LlamaIndex/AutoGen/CrewAI), EarnIn (LangChain/LlamaIndex/CrewAI/custom agentic), emagine (LangGraph). The 2026-10 cycle's proposed `mod-010 exercise-06-agentic-systems-in-production` is still pending and NOT withdrawn (removals out of scope). If 2026-12 again reads sub-0.30, open a separate withdrawal proposal rather than merging exercise-06.
- **GPU orchestration** — 0.20, −0.12 vs 2026-10. Sampling-driven swing (serving-heavy cycle, thinner training-infra slice). Ownership stays with `ai-infra-ml-platform-learning`.
- **Distributed training / inference at scale (FSDP / DeepSpeed / Pipeline Parallelism / NCCL)** — 0.16, flat. Ownership stays with `ai-infra-ml-platform-learning` and `ai-infra-performance-learning`.
- **ArgoCD / Argo Workflows for ML** — 0.24, +0.12. Named at Aerospace, Valarian, Nearmap, Talentcross, EarnIn. Ownership stays at L20; no MLOps-side action unless frequency jumps and L20 explicitly declines ownership.
- **LLM evaluation harnesses (LangSmith / Langfuse / LLM-as-judge / eval frameworks)** — 0.08, **−0.12** vs 2026-10. Signal receded this cycle; named vendors (LangSmith / Langfuse / Arize / Phoenix) still not surfacing. Covered partially in mod-010 and project-05. No action; keep on watch list through 2026-12.
- **Weights & Biases** — 0.12, +0.04. Shield AI, Aerospace, Nearmap name W&B this cycle. Covered as an MLflow alternative in mod-002. No action.
- **Vector DB (Pinecone / Weaviate / Qdrant / Milvus / pgvector)** — 0.12, +0.08. Valarian, Aerospace, Elsevier name vector DBs with multiple vendor options. project-05 uses ChromaDB; mod-010 exercise-02 covers RAG with vector DBs. No action.
- **Data versioning (DVC / lakeFS)** — 0.12, *new sub-threshold signal*. Aerospace, Sigma, Talentcross name DVC; Sigma names lakeFS. Covered via mod-004 data lineage and mod-002 artifact versioning. No action.
- **OpenTelemetry** — 0.12, *new sub-threshold signal*. Cursor, Valarian, Talentcross name OTel. Observability/tracing fundamentals are L20 territory; mod-003's Prometheus/Grafana coverage complements but does not duplicate.
- **AI-assisted development (Claude Code / AI coding assistants as expected tooling)** — 0.12, *new sub-threshold signal*. Anthropic, Coinflow, KNOREX name AI-native tooling as an expectation for MLOps engineers. No module ownership yet. Monitor whether this stabilizes.

## Delta Proposal

**No additions this cycle.** Justification is captured in [`.aicg/curriculum-plan-delta.json`](.aicg/curriculum-plan-delta.json).

The one above-threshold shift in this sample — feature store 0.24 → 0.32 — is absorbed by an existing dedicated exercise (`mod-010 exercise-05-real-time-ml-with-feature-stores`, 120-minute Feast end-to-end), so gate (c) fails on extensibility. All other above-threshold requirements are either already covered in this track or legitimately linked out per the ownership rule. The 2026-10 pending exercise-06 (agentic systems in production) is not re-proposed, not withdrawn, and left for the runner to adjudicate — this cycle's data shows the signal is noisy around ~0.20 across three cycles but remains sub-threshold.
