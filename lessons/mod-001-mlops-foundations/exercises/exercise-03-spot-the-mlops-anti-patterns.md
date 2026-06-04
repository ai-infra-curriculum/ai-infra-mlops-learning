## Exercise 3: Spot the MLOps Anti-Patterns (45 minutes)

**Objective**: Read a deliberately-bad ML system and identify the MLOps anti-patterns.

### Background

Pattern recognition is half the job. Naming what's wrong makes it fixable.

### The Scenario

A team has the following workflow:
- One data scientist manually copies the training dataset to their laptop
- Trains a model in a Jupyter notebook
- Saves the model as `.pkl` in a Google Drive folder
- Engineer copies the `.pkl` into the production Flask app and redeploys
- Monitoring is checking the Flask container is "up"
- When the model gets stale (months later), the data scientist tries to retrain
  but can't find the original training data

### Tasks

1. List at least 8 distinct anti-patterns in the workflow above. For each:
   - **Name** the anti-pattern
   - **Why** it's a problem (concrete failure scenarios)
   - **The fix** (what a mature MLOps team would do instead)

2. Order them by blast radius: which one, if not fixed, causes the most pain?

3. Pick one anti-pattern. Write a 1-page "case for fixing this first" you'd send to leadership.

### Deliverable

`ANTI_PATTERNS.md` with the list, ordering, and one-pager.

### Acceptance criteria

- ≥ 8 distinct anti-patterns named
- Each fix references a specific tool/practice from the lecture
- The one-pager is leadership-ready (no jargon)

---
