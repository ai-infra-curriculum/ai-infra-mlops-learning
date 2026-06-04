## Exercise 1: MLOps Maturity Assessment (60 minutes)

**Objective**: Apply Google's MLOps maturity model (Level 0 / 1 / 2) to a real or hypothetical team and produce a prioritized roadmap.

### Background

Most teams' first MLOps conversation is vague ("we should improve our ML
operations"). A maturity assessment converts that to specific: "we're at Level
0; the next investment is X."

### Tasks

1. **Pick a team** (your own, or a representative scenario):
   - Number of models in production
   - How data is ingested and labelled
   - How models are trained
   - How models are deployed
   - How models are monitored

2. **Score against each capability**:
   - Data validation (manual / automated / continuous)
   - Feature engineering (per-notebook / shared / feature store)
   - Experiment tracking (spreadsheet / MLflow / per-run)
   - Model registry (filesystem / MLflow / promotion workflow)
   - CI/CD (none / model code only / model + data + retrain)
   - Monitoring (latency only / metrics / drift + bias)
   - Triggered retraining (manual / cron / event-driven)

3. **Identify current level**: 0, 1, or 2 — and what would move it up one.

4. **Produce a 6-month investment roadmap**: 5 next investments in priority order, with rationale.

### Deliverable

A 1-2 page `ASSESSMENT.md` covering: current level, scoring table, target level
(12mo), top 5 investments with owners + ETA, 6-month roadmap.

### Acceptance criteria

- Concrete current-state observations (not just "we're medium")
- Each investment is < 1 quarter of effort
- Roadmap surfaces the 1 thing that unlocks the most other things

---
