# MLOps Midterm Quiz (Modules 1-5)

Integrated quiz covering Foundations → Experimentation. Designed for a 90-min
cohort sitting.

- **Total Questions**: 40
- **Time Limit**: 90 minutes
- **Passing Score**: 75%
- **Coverage**: modules 1-5 (foundations, tracking, monitoring, quality, experimentation)

---

### 1. Which best describes MLOps?
- [ ] a) DevOps with extra Python
- [x] b) Machine Learning + DevOps + Data Engineering practices for production ML
- [ ] c) Strictly model-deployment automation
- [ ] d) The Kubernetes-only deployment pattern

### 2. The single biggest cause of MLOps maturity-blocking is typically:
- [ ] a) Lack of GPUs
- [x] b) No experiment tracking + no model registry
- [ ] c) Inability to scale beyond 10 models
- [ ] d) Missing data labeling pipeline

### 3. PSI (Population Stability Index) > 0.25 typically indicates:
- [ ] a) The model is overfit
- [x] b) Significant distributional shift between reference and current data
- [ ] c) Low recall
- [ ] d) High inference latency

### 4. Great Expectations checkpoints are most useful when:
- [x] a) Embedded in pipelines as gating steps that fail on quality violations
- [ ] b) Run after model deployment as a smoke test
- [ ] c) Run once a month for compliance
- [ ] d) Only used in notebook EDA

### 5. A "shadow" model deployment:
- [ ] a) Replaces production immediately
- [x] b) Receives production traffic but does not return responses to users
- [ ] c) Runs only at night
- [ ] d) Is deployed but receives no traffic

### 6. Multi-armed bandits compared to A/B tests:
- [x] a) Continuously allocate more traffic to better-performing variants
- [ ] b) Always require a control group of 50%
- [ ] c) Are statistically less rigorous
- [ ] d) Replace bandits with manual reviews

### 7-40 (abbreviated for repo example — fill in to taste)

Use the per-module `quiz.md` files as a source of additional questions when
expanding this midterm.
