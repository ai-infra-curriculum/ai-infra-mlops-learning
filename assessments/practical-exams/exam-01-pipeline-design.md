# Practical Exam 01 — End-to-End Pipeline Design

**Duration**: 3 hours • **Format**: written + small code demo • **Modules**: 1, 2, 4, 6

## Scenario

You're the MLOps lead for an e-commerce company. Product wants daily
recommendations for 1M users plus near-real-time re-ranking based on session
behavior. Three data scientists currently train models in notebooks; ops has
no view of what's in production.

## Tasks

### Part A — Design (90 min, written)
1. Architecture diagram (data ingest → features → training → registry → serving → monitoring).
2. Tooling choices with rationale (MLflow, DVC, Great Expectations, Airflow, vLLM, etc.).
3. Per-component failure modes and how the system detects them.
4. Cost projection (per-day compute + storage).

### Part B — Build (60 min, code)
Stand up:
- A minimal MLflow tracking server (Docker compose)
- A training script that logs to it
- A pyfunc model wrapping the trained model
- Promotion to Staging

### Part C — Q&A (30 min)
Verbal review of choices; defend any non-obvious decisions.

## Rubric

See `rubrics/exam-01.md`.
