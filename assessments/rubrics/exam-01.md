# Rubric — Exam 01 (Pipeline Design)

## Part A — Architecture (40 points)

| Component | Points | Pass criteria |
|---|---|---|
| Data ingest design | 5 | Names sources, cadence, formats; addresses late-arrival |
| Feature store design | 5 | Distinguishes offline vs online; rationalizes choice |
| Tracking + registry choice | 5 | Names tool; explains version vs stage semantics |
| Training pipeline | 5 | Schedule + orchestrator + retries + SLA |
| Serving stack | 5 | Batch + online split; autoscale; failure isolation |
| Monitoring | 5 | Drift + latency + business metric; per-slice |
| Failure modes | 5 | At least 5; each with detection mechanism |
| Cost projection | 5 | Itemized; defensible numbers |

## Part B — Build (40 points)

| Element | Points | Pass criteria |
|---|---|---|
| Compose stack runs | 10 | `docker compose up` succeeds; tracking UI loads |
| Training logs to server | 10 | Run visible in UI; metrics + params + model artifact |
| Pyfunc packaging | 10 | Model loads + predicts via `mlflow.pyfunc.load_model` |
| Promotion | 10 | Quality gate enforced; rollback path demonstrated |

## Part C — Q&A (20 points)

- 5 pts: defends architecture choices with trade-offs
- 5 pts: addresses follow-up failure scenarios coherently
- 5 pts: names what they'd build next + why
- 5 pts: identifies gaps in their own design honestly

## Pass thresholds

- **70+**: pass
- **85+**: distinction
- **< 70**: requires resubmission
