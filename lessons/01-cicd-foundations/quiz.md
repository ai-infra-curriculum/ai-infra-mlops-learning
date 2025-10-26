# Module 01: CI/CD Foundations for MLOps - Quiz

## Instructions

- **Total Questions**: 30
- **Time Limit**: 45 minutes
- **Passing Score**: 75% (23/30 correct)
- **Question Types**: Multiple choice, multiple select, code analysis

---

## Section 1: Git Workflows (Questions 1-8)

### Question 1
What is the primary purpose of using feature branches in a Git workflow?

A) To increase repository size
B) To isolate feature development from the main codebase
C) To make git history more complex
D) To avoid using pull requests

<details>
<summary>Answer</summary>

**B) To isolate feature development from the main codebase**

**Explanation**: Feature branches allow developers to work on new features independently without affecting the stable main branch. This enables parallel development, easier code review, and safer integration.

</details>

---

### Question 2
Which merge strategy creates a single commit for all changes from a feature branch?

A) Merge commit
B) Fast-forward merge
C) Squash merge
D) Rebase merge

<details>
<summary>Answer</summary>

**C) Squash merge**

**Explanation**: Squash merge combines all commits from a feature branch into a single commit before merging to the target branch. This keeps the main branch history clean and linear.

</details>

---

### Question 3
**[Multiple Select]** Which of the following are best practices for Git commit messages in an ML project? (Select all that apply)

A) Use imperative mood ("Add feature" not "Added feature")
B) Include ticket/issue numbers
C) Commit all changes in a single commit at end of day
D) Describe what and why, not how
E) Keep subject line under 50 characters

<details>
<summary>Answer</summary>

**A, B, D, E**

**Explanation**:
- **A**: Imperative mood is conventional and clear
- **B**: Links commits to issues for traceability
- **C**: INCORRECT - Commits should be atomic and logical, not time-based
- **D**: Code shows "how," commit message should explain "what" and "why"
- **E**: Short subject lines are scannable in git history

</details>

---

### Question 4
What is the purpose of a `.gitignore` file in an ML project?

A) To ignore all Python files
B) To prevent tracking of generated files, credentials, and large datasets
C) To hide files from other developers
D) To compress the repository

<details>
<summary>Answer</summary>

**B) To prevent tracking of generated files, credentials, and large datasets**

**Explanation**: `.gitignore` prevents accidentally committing files that shouldn't be in version control, such as:
- Model weights and artifacts
- Credentials and secrets
- Virtual environments
- Cache files and logs
- Large datasets (should use DVC instead)

</details>

---

### Question 5
Examine the following Git workflow scenario:

```bash
git checkout -b feature/new-model
# Make changes to model.py
git add model.py
git commit -m "Improve model accuracy"
git push origin feature/new-model
```

What should be the next step before merging to main?

A) Directly merge to main branch
B) Delete the feature branch
C) Create a pull request for code review
D) Rebase onto main

<details>
<summary>Answer</summary>

**C) Create a pull request for code review**

**Explanation**: After pushing a feature branch, the standard workflow is to create a pull request. This enables:
- Code review by team members
- Automated CI checks
- Discussion of changes
- Approval workflow before merging

</details>

---

### Question 6
What is a merge conflict, and when does it occur?

A) When two files have the same name
B) When Git cannot automatically reconcile differences in the same file/lines
C) When a branch has too many commits
D) When pushing to a protected branch

<details>
<summary>Answer</summary>

**B) When Git cannot automatically reconcile differences in the same file/lines**

**Explanation**: Merge conflicts occur when:
- Two branches modify the same lines in a file
- Git cannot determine which changes to keep
- Manual resolution is required
- Common in collaborative ML projects when multiple developers modify training configs or model code

</details>

---

### Question 7
Which branching strategy is most suitable for continuous deployment in MLOps?

A) Git Flow (main, develop, feature, release, hotfix branches)
B) GitHub Flow (main + feature branches)
C) Trunk-Based Development (short-lived feature branches, frequent merges)
D) Random branching with no strategy

<details>
<summary>Answer</summary>

**C) Trunk-Based Development (short-lived feature branches, frequent merges)**

**Explanation**: Trunk-Based Development works best for CI/CD because:
- Encourages small, frequent integrations
- Reduces merge conflicts
- Enables rapid deployment
- Short-lived branches (< 2 days)
- Main branch is always deployable

GitHub Flow (B) is also acceptable for simpler workflows.

</details>

---

### Question 8
What is the purpose of branch protection rules in a production ML repository?

A) To prevent anyone from viewing the branch
B) To enforce code review, status checks, and prevent force pushes
C) To automatically delete old branches
D) To encrypt branch contents

<details>
<summary>Answer</summary>

**B) To enforce code review, status checks, and prevent force pushes**

**Explanation**: Branch protection rules ensure:
- Required reviews before merge (e.g., 2 approvals)
- All CI checks must pass
- No force pushes that could rewrite history
- Linear history if required
- Critical for production ML systems where code quality directly impacts model performance

</details>

---

## Section 2: GitHub Actions & CI (Questions 9-16)

### Question 9
What is the correct syntax to trigger a GitHub Actions workflow on pull requests to the main branch?

A)
```yaml
on:
  pull_request:
    branch: main
```

B)
```yaml
on:
  pull_request:
    branches: [ main ]
```

C)
```yaml
trigger:
  pr: main
```

D)
```yaml
on: pull_request_to_main
```

<details>
<summary>Answer</summary>

**B)**
```yaml
on:
  pull_request:
    branches: [ main ]
```

**Explanation**: The correct syntax uses:
- `on:` to specify trigger events
- `pull_request:` as the event type
- `branches:` (plural) with array syntax `[ ]`

</details>

---

### Question 10
In a GitHub Actions workflow, what is the purpose of a matrix strategy?

A) To organize files in a grid
B) To run jobs across multiple configurations (e.g., Python versions, OS)
C) To create visual dashboards
D) To manage secrets

<details>
<summary>Answer</summary>

**B) To run jobs across multiple configurations (e.g., Python versions, OS)**

**Explanation**: Matrix strategies enable testing across multiple combinations:

```yaml
strategy:
  matrix:
    python-version: [3.9, '3.10', 3.11]
    os: [ubuntu-latest, macos-latest]
```

This creates 6 jobs (3 Python versions × 2 OS), ensuring compatibility.

</details>

---

### Question 11
Analyze this GitHub Actions workflow snippet:

```yaml
- name: Cache pip dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

What is the primary benefit of this caching strategy?

A) Reduces storage costs
B) Speeds up workflow by reusing installed dependencies
C) Improves code quality
D) Encrypts dependencies

<details>
<summary>Answer</summary>

**B) Speeds up workflow by reusing installed dependencies**

**Explanation**: Caching prevents re-downloading and re-installing dependencies on every run:
- Cache key includes `hashFiles('requirements.txt')` - invalidates when dependencies change
- `restore-keys` provides fallback for partial cache hits
- Can reduce workflow time from 5+ minutes to 30 seconds
- Critical for ML projects with heavy dependencies (PyTorch, TensorFlow)

</details>

---

### Question 12
Which GitHub Actions event should you use to run weekly model retraining?

A) `on: push`
B) `on: schedule`
C) `on: weekly`
D) `on: cron`

<details>
<summary>Answer</summary>

**B) `on: schedule`**

**Explanation**: Scheduled workflows use cron syntax:

```yaml
on:
  schedule:
    - cron: '0 2 * * 0'  # Every Sunday at 2 AM UTC
```

This is essential for:
- Periodic model retraining
- Weekly data drift checks
- Monthly model performance audits

</details>

---

### Question 13
**[Multiple Select]** Which of the following are valid uses of GitHub Actions in MLOps? (Select all that apply)

A) Running unit tests on code changes
B) Building and pushing Docker images
C) Deploying models to production
D) Automatically approving all pull requests
E) Scanning for security vulnerabilities
F) Storing production database passwords in workflow files

<details>
<summary>Answer</summary>

**A, B, C, E**

**Explanation**:
- **A**: Standard CI practice
- **B**: Automated image building and registry push
- **C**: CD deployment automation
- **D**: INCORRECT - Approval should be manual or based on strict criteria
- **E**: Security scanning (Bandit, Trivy, etc.)
- **F**: INCORRECT - Never store secrets in workflow files; use GitHub Secrets

</details>

---

### Question 14
What is the purpose of the `needs` keyword in GitHub Actions workflows?

A) To specify required software
B) To define job dependencies and execution order
C) To list required secrets
D) To indicate resource requirements

<details>
<summary>Answer</summary>

**B) To define job dependencies and execution order**

**Explanation**: `needs` creates a directed acyclic graph (DAG) of jobs:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps: [...]

  deploy:
    needs: test  # Only runs if 'test' succeeds
    runs-on: ubuntu-latest
    steps: [...]
```

Ensures you don't deploy untested code.

</details>

---

### Question 15
Examine this workflow step:

```yaml
- name: Run tests with coverage
  run: |
    pytest tests/ \
      --cov=src \
      --cov-report=xml \
      --cov-report=term-missing \
      --cov-fail-under=80
```

What happens if test coverage is 75%?

A) Tests pass with a warning
B) Workflow fails
C) Coverage report is not generated
D) Tests are skipped

<details>
<summary>Answer</summary>

**B) Workflow fails**

**Explanation**: `--cov-fail-under=80` sets a minimum coverage threshold:
- If coverage < 80%, pytest exits with non-zero code
- Workflow step fails
- Prevents merging code that decreases coverage
- Enforces quality standards in ML codebases

</details>

---

### Question 16
Which is the correct way to use a secret in a GitHub Actions workflow?

A) `password: my_secret_password`
B) `password: ${{ secrets.DB_PASSWORD }}`
C) `password: ${DB_PASSWORD}`
D) `password: env.DB_PASSWORD`

<details>
<summary>Answer</summary>

**B) `password: ${{ secrets.DB_PASSWORD }}`**

**Explanation**: GitHub Secrets syntax:
- Defined in repo settings → Secrets
- Referenced as `${{ secrets.SECRET_NAME }}`
- Automatically masked in logs
- Never committed to repository
- Essential for API keys, credentials, tokens

</details>

---

## Section 3: Docker & Containerization (Questions 17-23)

### Question 17
What is the primary advantage of multi-stage Docker builds for ML applications?

A) Faster build times
B) Smaller final image by separating build and runtime dependencies
C) Better security through multiple containers
D) Easier debugging

<details>
<summary>Answer</summary>

**B) Smaller final image by separating build and runtime dependencies**

**Explanation**: Multi-stage builds allow:
- Build stage: Install compilers, build tools, create wheels
- Runtime stage: Copy only necessary artifacts
- Reduces image size by 50-80%
- Example: Build stage has gcc for compiling, runtime stage doesn't

```dockerfile
FROM python:3.10 AS builder
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

FROM python:3.10-slim
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*
```

</details>

---

### Question 18
Analyze this Dockerfile snippet:

```dockerfile
FROM python:3.10-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "train.py"]
```

Why is `COPY requirements.txt` done before `COPY . .`?

A) It's required by Docker syntax
B) To leverage layer caching - dependencies don't change as often as code
C) Requirements.txt must be in root directory
D) To reduce image size

<details>
<summary>Answer</summary>

**B) To leverage layer caching - dependencies don't change as often as code**

**Explanation**: Docker layer caching optimization:
- Each Dockerfile instruction creates a layer
- Layers are cached if inputs haven't changed
- `requirements.txt` changes infrequently
- Application code changes frequently
- This order means dependency installation is cached, only code copy and later steps re-run
- Reduces rebuild time from 5+ minutes to seconds

</details>

---

### Question 19
What is the purpose of a `.dockerignore` file?

A) To ignore Docker commands
B) To prevent files from being added to Docker build context
C) To hide containers from Docker CLI
D) To exclude images from registry

<details>
<summary>Answer</summary>

**B) To prevent files from being added to Docker build context**

**Explanation**: `.dockerignore` excludes files from build context:

```
__pycache__/
*.pyc
.git/
venv/
*.pth  # Model weights
.env
notebooks/
```

Benefits:
- Faster builds (smaller context)
- Prevents accidentally copying secrets
- Reduces image size
- Avoids copying large datasets into image

</details>

---

### Question 20
Which Docker base image is most appropriate for a production ML inference service?

A) `python:3.10` (1GB)
B) `python:3.10-slim` (200MB)
C) `python:3.10-alpine` (50MB)
D) `ubuntu:latest` (80MB)

<details>
<summary>Answer</summary>

**B) `python:3.10-slim` (200MB)**

**Explanation**:
- **python:3.10**: Too large, includes unnecessary build tools
- **python:3.10-slim**: Optimal balance - has glibc, works with most ML libraries
- **python:3.10-alpine**: Uses musl libc, incompatible with many ML wheels (NumPy, PyTorch)
- **ubuntu:latest**: Requires manual Python installation

For inference, slim is best. For training with GPU, use `nvidia/cuda:...-cudnn8-runtime-ubuntu22.04`.

</details>

---

### Question 21
What is the purpose of a health check in a Docker container running an ML model API?

A) To check if the model is accurate
B) To verify the container is running and responsive
C) To scan for viruses
D) To validate input data

<details>
<summary>Answer</summary>

**B) To verify the container is running and responsive**

**Explanation**: Health checks enable orchestrators (K8s, Docker Compose) to:
- Detect unhealthy containers
- Automatically restart failed containers
- Route traffic only to healthy instances
- Implement rolling deployments safely

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

</details>

---

### Question 22
In a Docker Compose file for an ML project, what does the `depends_on` option do?

A) Makes one service dependent on another's code
B) Controls service startup order
C) Shares files between services
D) Manages resource allocation

<details>
<summary>Answer</summary>

**B) Controls service startup order**

**Explanation**: `depends_on` ensures services start in order:

```yaml
services:
  postgres:
    image: postgres:15

  mlflow:
    image: mlflow:latest
    depends_on:
      - postgres
```

MLflow waits for postgres to start (but not necessarily be ready - use health checks for that).

Essential for ML stacks: database → tracking server → training service.

</details>

---

### Question 23
**[Multiple Select]** Which of the following should NOT be included in a Docker image for an ML model? (Select all that apply)

A) Trained model weights
B) Production API keys and secrets
C) Training datasets
D) Python dependencies
E) Application code
F) `.git` directory

<details>
<summary>Answer</summary>

**B, C, F**

**Explanation**:
- **A**: Debatable - small models can be included, large models should be downloaded at runtime
- **B**: NEVER include secrets in images - use environment variables or secret management
- **C**: Datasets are too large and change frequently - mount as volumes or fetch from storage
- **D**: Should be included (frozen versions)
- **E**: Should be included
- **F**: Git history is unnecessary and increases image size - use .dockerignore

</details>

---

## Section 4: Testing & Quality (Questions 24-28)

### Question 24
What is the difference between unit tests and integration tests in ML projects?

A) Unit tests are faster, integration tests are more expensive
B) Unit tests verify individual components, integration tests verify component interactions
C) Unit tests use real data, integration tests use mocks
D) There is no difference

<details>
<summary>Answer</summary>

**B) Unit tests verify individual components, integration tests verify component interactions**

**Explanation**:

**Unit Tests**:
- Test single functions/classes in isolation
- Use mocks for dependencies
- Fast (milliseconds)
- Example: Test that `preprocess_data()` handles NaN correctly

**Integration Tests**:
- Test multiple components together
- Use real or realistic dependencies
- Slower (seconds to minutes)
- Example: Test entire training pipeline from data loading to model saving

Both are essential for ML reliability.

</details>

---

### Question 25
Analyze this pytest fixture:

```python
@pytest.fixture(scope='session')
def trained_model():
    model = train_expensive_model()
    return model
```

What does `scope='session'` mean?

A) The fixture runs once per test file
B) The fixture runs once per test function
C) The fixture runs once for the entire test session
D) The fixture never runs

<details>
<summary>Answer</summary>

**C) The fixture runs once for the entire test session**

**Explanation**: Pytest fixture scopes:
- `function`: Default, runs before each test (isolated but slow)
- `class`: Once per test class
- `module`: Once per test file
- `session`: Once per entire test run

For expensive operations (model training, database setup), `session` scope improves performance dramatically. Trade-off: Tests share state, less isolation.

</details>

---

### Question 26
Which metric is most important to track in a CI pipeline for ML code?

A) Number of commits
B) Code coverage percentage
C) Repository size
D) Number of branches

<details>
<summary>Answer</summary>

**B) Code coverage percentage**

**Explanation**: Code coverage measures what percentage of code is executed by tests:
- Industry standard: 80%+ coverage
- Identifies untested code paths
- Prevents regressions
- Tracked in CI with tools like `pytest-cov`

However, 100% coverage doesn't guarantee quality - tests must also be meaningful.

Other important CI metrics:
- Test pass rate
- Build duration
- Flaky test rate

</details>

---

### Question 27
**[Multiple Select]** Which of the following are characteristics of good ML tests? (Select all that apply)

A) Deterministic (same input always produces same output)
B) Fast (complete in seconds, not minutes)
C) Isolated (tests don't depend on each other)
D) Use production data exclusively
E) Provide clear failure messages

<details>
<summary>Answer</summary>

**A, B, C, E**

**Explanation**:
- **A**: Essential - random seeds should be fixed in tests
- **B**: Fast tests encourage frequent running
- **C**: Tests should be independent and parallelizable
- **D**: INCORRECT - Tests should use synthetic or sampled data, not production data (privacy, size, availability)
- **E**: Good error messages speed up debugging

</details>

---

### Question 28
What is the purpose of parametrized tests in pytest?

A) To pass command-line parameters
B) To run the same test with multiple inputs efficiently
C) To configure test environments
D) To manage test fixtures

<details>
<summary>Answer</summary>

**B) To run the same test with multiple inputs efficiently**

**Explanation**: Parametrized tests avoid duplication:

```python
@pytest.mark.parametrize('input,expected', [
    (np.array([1, 2, 3]), 2.0),
    (np.array([0, 0, 0]), 0.0),
    (np.array([-1, 1]), 0.0),
])
def test_mean_calculation(input, expected):
    assert calculate_mean(input) == expected
```

One test function, multiple test cases. Cleaner than writing separate functions.

</details>

---

## Section 5: CI/CD Best Practices (Questions 29-30)

### Question 29
What is the primary goal of Continuous Integration (CI) in MLOps?

A) To automatically deploy every code change to production
B) To frequently integrate code changes and verify them through automated builds and tests
C) To continuously monitor production models
D) To integrate data from multiple sources

<details>
<summary>Answer</summary>

**B) To frequently integrate code changes and verify them through automated builds and tests**

**Explanation**: CI core principles:
- Merge code to main branch frequently (at least daily)
- Automated build on every merge
- Automated test suite runs
- Fast feedback (< 10 minutes)
- Keeps main branch in deployable state

CI ≠ CD (Continuous Deployment). CI is about integration and verification, CD is about deployment.

</details>

---

### Question 30
You've implemented a CI/CD pipeline that automatically deploys model changes to production without any manual approval. Model performance metrics dropped by 15% after an automatic deployment. What CI/CD practice should be implemented to prevent this?

A) Remove all automation and deploy manually
B) Implement staging environment with smoke tests and manual approval gate before production
C) Disable monitoring
D) Increase deployment frequency

<details>
<summary>Answer</summary>

**B) Implement staging environment with smoke tests and manual approval gate before production**

**Explanation**: Production deployment safeguards:

1. **Staging Environment**: Identical to production
2. **Smoke Tests**: Basic functionality verification
3. **Performance Tests**: Validate model metrics on holdout data
4. **Manual Approval**: Human verification before prod
5. **Canary Deployment**: Gradual rollout with monitoring
6. **Automatic Rollback**: Revert on metric degradation

The pipeline should be: CI → Deploy to Staging → Automated Tests → Manual Approval → Deploy to Production → Monitor → Auto-rollback if issues.

</details>

---

## Scoring Guide

| Score | Grade | Feedback |
|-------|-------|----------|
| 28-30 | A+ | Excellent! You have a strong grasp of CI/CD for MLOps |
| 25-27 | A | Great job! Minor gaps in understanding |
| 23-24 | B | Good. Review missed topics |
| 20-22 | C | Passing. Revisit key concepts |
| < 20 | F | Please review lecture notes and retry |

---

## Answer Key Summary

1. B | 2. C | 3. A,B,D,E | 4. B | 5. C
6. B | 7. C | 8. B | 9. B | 10. B
11. B | 12. B | 13. A,B,C,E | 14. B | 15. B
16. B | 17. B | 18. B | 19. B | 20. B
21. B | 22. B | 23. B,C,F | 24. B | 25. C
26. B | 27. A,B,C,E | 28. B | 29. B | 30. B

---

## Next Steps

- Review any missed questions
- Revisit corresponding lecture sections
- Complete hands-on exercises
- Explore additional resources in `resources.md`

**Good luck!** 🎯
