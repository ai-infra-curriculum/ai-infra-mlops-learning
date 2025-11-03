# CI/CD Foundations for MLOps - Comprehensive Lecture Notes

**Module**: 01-cicd-foundations
**Role**: MLOps Engineer (Level 2.5B)
**Duration**: 15 hours of content
**Last Updated**: November 2025

---

## Table of Contents

1. [Introduction to CI/CD for ML](#1-introduction-to-cicd-for-ml)
2. [Version Control with Git](#2-version-control-with-git)
3. [Branch Strategies and Workflows](#3-branch-strategies-and-workflows)
4. [Continuous Integration Fundamentals](#4-continuous-integration-fundamentals)
5. [GitHub Actions for ML](#5-github-actions-for-ml)
6. [Docker and Containerization](#6-docker-and-containerization)
7. [Testing Strategies for ML Systems](#7-testing-strategies-for-ml-systems)
8. [Continuous Deployment](#8-continuous-deployment)
9. [Deployment Strategies](#9-deployment-strategies)
10. [Monitoring and Rollback](#10-monitoring-and-rollback)
11. [Best Practices and Common Pitfalls](#11-best-practices-and-common-pitfalls)
12. [Summary and Key Takeaways](#12-summary-and-key-takeaways)

---

## 1. Introduction to CI/CD for ML

### 1.1 What is CI/CD?

**Continuous Integration (CI)** and **Continuous Deployment/Delivery (CD)** are software engineering practices that enable teams to deliver code changes more frequently and reliably.

```
CI/CD Pipeline Flow:
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Code   │───▶│  Build  │───▶│  Test   │───▶│ Deploy  │───▶│Monitor  │
│ Commit  │    │         │    │         │    │Staging  │    │         │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
                                                     │
                                                     ▼
                                               ┌─────────┐
                                               │ Deploy  │
                                               │  Prod   │
                                               └─────────┘
```

**Continuous Integration** ensures that:
- Code changes are automatically tested
- Multiple developers can work simultaneously
- Integration issues are detected early
- Code quality is maintained through automation

**Continuous Deployment** ensures that:
- Tested code is automatically deployed
- Deployments are consistent and repeatable
- Rollbacks are possible and automated
- Deployment risks are minimized

### 1.2 Traditional CI/CD vs ML CI/CD

Traditional software CI/CD focuses on code, but **ML CI/CD** must handle additional complexities:

| Aspect | Traditional CI/CD | ML CI/CD |
|--------|------------------|-----------|
| **Artifacts** | Code, binaries | Code + data + models + parameters |
| **Testing** | Unit, integration tests | Data validation + model validation + code tests |
| **Deployment** | Deploy application | Deploy model + serving infrastructure |
| **Monitoring** | Application metrics | Model performance + data drift + concept drift |
| **Triggers** | Code changes | Code changes + data changes + scheduled retraining |
| **Rollback** | Revert to previous code | Revert code + model + data pipeline |
| **Dependencies** | Libraries, packages | Libraries + data schemas + model versions |
| **Reproducibility** | Build from source | Code + data + environment + randomness |

### 1.3 Why CI/CD Matters for MLOps

According to Algorithmia's 2023 State of Enterprise ML report:
- **68%** of ML models take 30+ days to deploy to production
- **53%** of organizations struggle with model deployment
- **40%** of production ML models are never updated after initial deployment

**CI/CD solves these problems by**:

1. **Automating model deployment** - Reduce 30+ day deployment to hours
2. **Ensuring reproducibility** - Same code + data = same results
3. **Detecting issues early** - Catch problems before production
4. **Enabling continuous improvement** - Regular model updates and retraining
5. **Reducing manual errors** - Automation eliminates human mistakes
6. **Improving collaboration** - Team members can work independently

### 1.4 The ML CI/CD Lifecycle

An end-to-end ML CI/CD pipeline includes:

```
┌─────────────────────────────────────────────────────────────┐
│                   ML CI/CD Lifecycle                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Development                                             │
│     ├─ Write code (features, training, serving)           │
│     ├─ Commit to version control                          │
│     └─ Create pull request                                │
│                                                             │
│  2. Continuous Integration                                 │
│     ├─ Lint and format code                               │
│     ├─ Run unit tests                                     │
│     ├─ Run integration tests                              │
│     ├─ Validate data schemas                              │
│     ├─ Build Docker images                                │
│     └─ Security scanning                                  │
│                                                             │
│  3. Model Training (scheduled or triggered)                │
│     ├─ Fetch training data                                │
│     ├─ Validate data quality                              │
│     ├─ Train model                                        │
│     ├─ Evaluate model performance                         │
│     ├─ Compare with baseline                              │
│     └─ Register model in MLflow                           │
│                                                             │
│  4. Continuous Deployment                                  │
│     ├─ Deploy to staging environment                      │
│     ├─ Run smoke tests                                    │
│     ├─ Run integration tests                              │
│     ├─ Performance testing                                │
│     ├─ Manual approval (optional)                         │
│     └─ Deploy to production                               │
│                                                             │
│  5. Monitoring and Feedback                                │
│     ├─ Monitor model performance                          │
│     ├─ Detect data drift                                  │
│     ├─ Track prediction latency                           │
│     ├─ Collect feedback                                   │
│     └─ Trigger retraining if needed                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1.5 Key Components of ML CI/CD

**1. Version Control System (VCS)**
- Git for code versioning
- DVC (Data Version Control) for data versioning
- Model registry for model versioning

**2. CI/CD Platform**
- GitHub Actions, GitLab CI, Jenkins, CircleCI
- Orchestrates the automation pipeline
- Manages secrets and environment variables

**3. Containerization**
- Docker for packaging code and dependencies
- Ensures consistency across environments
- Enables reproducible builds

**4. Testing Framework**
- pytest for Python testing
- Great Expectations for data validation
- Custom model validation tests

**5. Model Registry**
- MLflow, Weights & Biases, or Neptune
- Tracks experiments and model versions
- Stores model artifacts and metadata

**6. Deployment Platform**
- Kubernetes for container orchestration
- Cloud services (AWS, GCP, Azure)
- Model serving frameworks (TorchServe, TensorFlow Serving)

**7. Monitoring System**
- Prometheus + Grafana for metrics
- ELK Stack for logging
- Custom model performance monitoring

### 1.6 CI/CD Maturity Levels for ML

Similar to MLOps maturity, ML CI/CD has distinct levels:

**Level 0: Manual Process**
- Manual testing and deployment
- No automation
- High error rate
- Deployment takes days/weeks

**Level 1: Automated CI**
- Automated testing on code changes
- Automated builds
- Still manual deployment
- Deployment takes hours/days

**Level 2: Automated CD to Staging**
- Automated deployment to staging
- Manual production deployment
- Automated smoke tests
- Deployment takes hours

**Level 3: Full CI/CD Automation**
- Fully automated pipeline
- Automated production deployment (with approval gates)
- Comprehensive testing
- Deployment takes minutes

**Level 4: Self-Healing CI/CD**
- Automated rollback on failures
- Automated retraining triggers
- Adaptive deployment strategies
- Self-optimizing pipelines

**Industry Benchmarks** (2024):
- **Tech Leaders** (Google, Meta, Netflix): Level 3-4
- **ML-Mature Companies**: Level 2-3
- **Most Enterprises**: Level 1-2
- **ML Startups**: Level 0-1

---

## 2. Version Control with Git

### 2.1 Git Fundamentals for ML

Git is a distributed version control system that tracks changes to code over time. For ML projects, Git tracks:
- Training code
- Inference/serving code
- Configuration files
- Pipeline definitions
- Documentation

**Core Git Concepts**:

```
Working Directory → Staging Area → Local Repository → Remote Repository
      ↓                 ↓                ↓                    ↓
  git add          git commit       git push
```

**Essential Git Commands**:

```bash
# Initialize repository
git init
git clone <repository-url>

# Check status
git status
git log --oneline --graph --all

# Stage and commit changes
git add <file>
git add .  # Add all changes
git commit -m "Descriptive commit message"

# Branching
git branch <branch-name>
git checkout <branch-name>
git checkout -b <new-branch>  # Create and switch

# Merging
git merge <branch-name>
git merge --no-ff <branch-name>  # No fast-forward

# Remote operations
git fetch origin
git pull origin main
git push origin <branch-name>
git push -u origin <branch-name>  # Set upstream

# Undoing changes
git reset HEAD <file>  # Unstage
git checkout -- <file>  # Discard changes
git revert <commit>  # Create new commit that undoes
git reset --hard <commit>  # Dangerous: reset to commit

# Viewing changes
git diff
git diff --staged
git diff main..feature-branch

# Stashing changes
git stash
git stash pop
git stash list
```

### 2.2 Git Configuration for ML Teams

**Global Configuration**:

```bash
# Identity
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"

# Editor
git config --global core.editor "vim"

# Default branch name
git config --global init.defaultBranch main

# Merge strategy
git config --global merge.ff false  # Always create merge commit

# Pull strategy
git config --global pull.rebase false

# Color output
git config --global color.ui auto

# Credential caching
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=3600'
```

**Repository-Specific Configuration** (`.gitconfig` in repo):

```ini
[core]
    fileMode = false
    autocrlf = input

[merge]
    tool = vimdiff

[diff]
    tool = vimdiff

[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = log --oneline --graph --all --decorate
```

### 2.3 .gitignore for ML Projects

**Comprehensive .gitignore**:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environments
venv/
env/
ENV/
.venv

# Jupyter Notebooks
.ipynb_checkpoints
*.ipynb

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# ML Artifacts
*.h5
*.pkl
*.joblib
*.onnx
*.pt
*.pth
models/
checkpoints/

# Data (usually too large for git)
data/
*.csv
*.parquet
*.feather
*.hdf5

# Logs
logs/
*.log
mlruns/
wandb/

# Environment
.env
.env.local
secrets/
*.key
*.pem

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/

# Temporary files
tmp/
temp/
*.tmp

# OS
Thumbs.db
.DS_Store
```

### 2.4 Commit Message Best Practices

Good commit messages are essential for ML projects where understanding the "why" behind changes is critical.

**Conventional Commits Format**:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code restructuring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes
- `data`: Data-related changes (ML-specific)
- `model`: Model architecture changes (ML-specific)
- `exp`: Experiment tracking (ML-specific)

**Examples**:

```bash
# Good commits
git commit -m "feat(training): add learning rate scheduler

Implemented ReduceLROnPlateau scheduler to improve model convergence.
Learning rate now reduces by 50% if validation loss plateaus for 5 epochs.

Closes #234"

git commit -m "fix(preprocessing): handle missing values in categorical features

Previous implementation raised error for NaN in categorical columns.
Now uses 'missing' category for NaN values.

Impact: Fixes data pipeline failures in production"

git commit -m "data: update training dataset schema

Added new features: user_tenure, last_purchase_date
Removed deprecated feature: legacy_user_id

Schema version: 2.1.0"

git commit -m "model: upgrade to Transformer architecture

Replaced LSTM with Transformer encoder.
Improves accuracy by 3.2% (0.89 → 0.92) on validation set.

Training time: 45min → 32min
Inference latency: 120ms → 95ms"

# Bad commits (avoid these)
git commit -m "fix stuff"  # Too vague
git commit -m "WIP"  # Work in progress, should squash before merging
git commit -m "asdfasdf"  # Meaningless
git commit -m "Updated code"  # Doesn't say what changed
```

**Why Good Commit Messages Matter in ML**:
1. **Experiment tracking**: Understand what changed between experiment runs
2. **Reproducibility**: Know exactly what code produced which results
3. **Debugging**: Quickly identify when bugs were introduced
4. **Collaboration**: Help teammates understand changes
5. **Model lineage**: Track model evolution over time

### 2.5 Git for Large Files (LFS)

ML projects often include large files (models, datasets) that exceed Git's recommended size limits.

**Git LFS (Large File Storage)**:

```bash
# Install Git LFS
brew install git-lfs  # macOS
apt-get install git-lfs  # Ubuntu

# Initialize LFS in repository
git lfs install

# Track large files
git lfs track "*.h5"
git lfs track "*.pkl"
git lfs track "*.pth"
git lfs track "*.onnx"
git lfs track "data/*.parquet"

# This creates/updates .gitattributes
cat .gitattributes
# *.h5 filter=lfs diff=lfs merge=lfs -text
# *.pkl filter=lfs diff=lfs merge=lfs -text

# Add and commit
git add .gitattributes
git add models/model.h5
git commit -m "model: add trained model with Git LFS"
git push origin main

# Check LFS status
git lfs ls-files
git lfs status

# Pull LFS files
git lfs pull
```

**Alternatives to Git LFS for ML**:

1. **DVC (Data Version Control)**:
```bash
pip install dvc
dvc init
dvc add data/large_dataset.parquet
git add data/large_dataset.parquet.dvc .dvc/config
git commit -m "data: add dataset with DVC"
dvc push  # Push to remote storage (S3, GCS, etc.)
```

2. **Cloud Storage with Pointers**:
```python
# Store reference in git, not actual file
# dataset_config.yaml
dataset:
  name: "training_data_v1"
  location: "s3://ml-datasets/training_data_v1.parquet"
  size: "5.2GB"
  checksum: "md5:a1b2c3d4e5f6..."
```

3. **Model Registry**:
```python
# Store models in MLflow registry, reference in git
# model_config.yaml
model:
  name: "classifier_v2"
  version: 5
  mlflow_uri: "models:/classifier_v2/5"
  framework: "pytorch"
```

---

## 3. Branch Strategies and Workflows

### 3.1 Why Branch Strategies Matter

Branch strategies define how teams organize their work and collaborate. For ML teams, good branch strategies enable:
- **Parallel experimentation**: Multiple data scientists can experiment simultaneously
- **Feature isolation**: New features don't interfere with stable code
- **Code review**: Changes are reviewed before merging
- **Release management**: Clear process for deploying to production
- **Rollback capability**: Easy to revert problematic changes

### 3.2 Git Flow

**Git Flow** is a popular branching strategy that uses multiple long-lived branches.

```
Main Branches:
├─ main (production-ready code)
└─ develop (integration branch)

Supporting Branches:
├─ feature/* (new features)
├─ release/* (release preparation)
├─ hotfix/* (production fixes)
└─ experiment/* (ML experiments)
```

**Git Flow Workflow**:

```bash
# 1. Create feature branch from develop
git checkout develop
git checkout -b feature/new-preprocessing

# 2. Work on feature
# ... make changes ...
git add .
git commit -m "feat(preprocessing): add StandardScaler"

# 3. Merge back to develop
git checkout develop
git merge --no-ff feature/new-preprocessing
git branch -d feature/new-preprocessing

# 4. Create release branch
git checkout -b release/1.2.0 develop
# ... final testing, version bumps ...
git commit -m "chore: bump version to 1.2.0"

# 5. Merge release to main and develop
git checkout main
git merge --no-ff release/1.2.0
git tag -a v1.2.0 -m "Version 1.2.0"

git checkout develop
git merge --no-ff release/1.2.0
git branch -d release/1.2.0

# 6. Hotfix for production issue
git checkout -b hotfix/fix-nan-error main
# ... fix bug ...
git commit -m "fix: handle NaN in preprocessing"

git checkout main
git merge --no-ff hotfix/fix-nan-error
git tag -a v1.2.1 -m "Hotfix 1.2.1"

git checkout develop
git merge --no-ff hotfix/fix-nan-error
git branch -d hotfix/fix-nan-error
```

**Pros of Git Flow**:
- Clear separation of production and development
- Supports scheduled releases
- Easy to track versions

**Cons of Git Flow**:
- Complex with many branches
- Merge conflicts can be frequent
- Overhead for small teams

### 3.2 GitHub Flow (Simplified)

**GitHub Flow** is a simpler alternative with one main branch and short-lived feature branches.

```
main (always deployable)
  ├─ feature/add-feature-x
  ├─ fix/bug-123
  └─ experiment/new-model
```

**GitHub Flow Workflow**:

```bash
# 1. Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/add-new-model

# 2. Work on feature, commit frequently
git add .
git commit -m "model: add Transformer architecture"
git push -u origin feature/add-new-model

# 3. Open pull request on GitHub
# (done through GitHub UI or gh CLI)
gh pr create --title "Add Transformer model" --body "Implements new model architecture"

# 4. Code review and CI checks
# (automated tests run, reviewers comment)

# 5. Merge to main (after approval)
# Merge via GitHub UI with squash or merge commit
# Or via CLI:
git checkout main
git merge --no-ff feature/add-new-model
git push origin main
git branch -d feature/add-new-model
git push origin --delete feature/add-new-model

# 6. Deploy (automatically or manually)
```

**Pros of GitHub Flow**:
- Simple and easy to understand
- Encourages continuous deployment
- Fast feedback loop

**Cons**:
- No explicit staging/release branches
- Main branch must always be stable
- Requires discipline and good CI/CD

### 3.3 Trunk-Based Development

**Trunk-Based Development** emphasizes short-lived branches and frequent integration to main.

```
main (trunk)
  ├─ Very short-lived branches (1-2 days max)
  └─ Frequent merges to main
```

**Trunk-Based Workflow**:

```bash
# 1. Create very short-lived branch
git checkout main
git pull origin main
git checkout -b add-logging

# 2. Make small, focused changes
git add .
git commit -m "chore: add debug logging"

# 3. Merge to main quickly (within 1-2 days)
git checkout main
git pull origin main  # Get latest changes
git merge add-logging
git push origin main
git branch -d add-logging

# Alternative: Commit directly to main (for tiny changes)
git checkout main
git pull origin main
# ... make change ...
git add .
git commit -m "fix: typo in config"
git push origin main
```

**Pros of Trunk-Based Development**:
- Minimal merge conflicts
- Fast integration
- Simplified git history

**Cons**:
- Requires strong CI/CD
- Feature flags needed for incomplete features
- High discipline required

### 3.4 ML-Specific Branch Strategy

For ML teams, a **hybrid approach** often works best:

```
main (production models and serving code)
  ├─ develop (integration branch)
  │    ├─ feature/* (new features)
  │    └─ experiment/* (ML experiments)
  └─ hotfix/* (production fixes)
```

**ML Branch Naming Conventions**:

```bash
# Feature branches
feature/add-preprocessing
feature/api-authentication
feature/batch-inference

# Experiment branches (kept separate from features)
experiment/transformer-architecture
experiment/focal-loss
experiment/data-augmentation

# Data pipeline branches
data/update-schema-v2
data/add-feature-engineering

# Model branches
model/upgrade-to-pytorch-2.0
model/quantization

# Bug fixes
fix/nan-handling
fix/memory-leak

# Hotfixes (critical production issues)
hotfix/prediction-timeout
hotfix/authentication-bug
```

**Experiment Branch Best Practices**:

1. **Keep experiments isolated**:
```bash
git checkout develop
git checkout -b experiment/focal-loss

# Work on experiment
# Log results to MLflow or W&B

# If experiment succeeds:
git checkout develop
git merge --squash experiment/focal-loss
git commit -m "model: implement focal loss (improves F1 by 0.05)"

# If experiment fails:
# Don't merge, but keep branch for reference
git tag experiment-focal-loss-failed experiment/focal-loss
```

2. **Use tags for successful experiments**:
```bash
git tag -a exp-v1.5-baseline -m "Baseline model accuracy: 0.87"
git tag -a exp-v2.0-transformer -m "Transformer model accuracy: 0.92"
```

3. **Document experiments in commits**:
```bash
git commit -m "exp: test focal loss with gamma=2.0

Results:
- Accuracy: 0.89 (+0.02)
- F1 Score: 0.86 (+0.05)
- Training time: 45min (+10min)

Config:
- focal_loss_gamma: 2.0
- learning_rate: 0.001
- batch_size: 32

MLflow run: runs:/abc123def456"
```

### 3.5 Merge Strategies

Different merge strategies affect git history and collaboration.

**1. Merge Commit (--no-ff)**:
```bash
git merge --no-ff feature/new-model
```
- Preserves branch history
- Shows when feature was developed
- Creates explicit merge commit
- **Best for**: Feature branches, releases

**2. Fast-Forward Merge (default)**:
```bash
git merge feature/tiny-fix
```
- Linear history
- No merge commit
- Clean git log
- **Best for**: Small changes, hotfixes

**3. Squash Merge**:
```bash
git merge --squash feature/many-commits
git commit -m "feat: add new model architecture"
```
- Combines all commits into one
- Clean history on main branch
- Loses detailed commit history
- **Best for**: Feature branches with many WIP commits

**4. Rebase**:
```bash
git checkout feature/my-feature
git rebase main
# Resolve conflicts if any
git checkout main
git merge feature/my-feature  # Fast-forward
```
- Linear history
- No merge commits
- Rewrites history (dangerous for shared branches)
- **Best for**: Updating feature branch with main changes

**Merge Strategy Recommendations for ML**:

| Scenario | Strategy | Why |
|----------|----------|-----|
| Feature → develop | Merge commit (--no-ff) | Preserve feature development context |
| develop → main | Merge commit (--no-ff) | Clear release points |
| Hotfix → main | Fast-forward or merge commit | Quick fixes, clear in history |
| Experiment → develop | Squash merge | Clean up experiment commits |
| Small fixes | Fast-forward | Keep history simple |

### 3.6 Pull Requests (PRs) and Code Review

**Pull Request Workflow**:

```bash
# 1. Push feature branch
git push -u origin feature/add-new-model

# 2. Create PR (via GitHub CLI)
gh pr create \
  --title "Add Transformer model architecture" \
  --body "## Changes
  - Implemented Transformer encoder
  - Added attention mechanism
  - Updated training loop

## Performance
- Accuracy: 0.92 (+0.05)
- Training time: 32min (-13min)
- Model size: 45MB

## Testing
- [x] Unit tests pass
- [x] Integration tests pass
- [x] Model validation passed
- [x] Performance benchmarks met

## MLflow Run
- Run ID: runs:/abc123
- Experiment: transformer-experiments" \
  --reviewer @teammate1,@teammate2 \
  --assignee @me \
  --label enhancement,ml-model

# 3. Address review comments
# ... make changes based on feedback ...
git add .
git commit -m "address review feedback: add docstrings"
git push origin feature/add-new-model

# 4. Merge after approval
gh pr merge --squash --delete-branch
```

**PR Template** (`.github/pull_request_template.md`):

```markdown
## Description
<!-- Describe the changes in this PR -->

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] ML model update (new architecture, hyperparameters, or training data)
- [ ] Documentation update

## ML-Specific Changes
<!-- If this PR includes ML changes, provide details -->
- **Model Architecture**:
- **Performance Metrics**:
  - Accuracy:
  - F1 Score:
  - Inference Latency:
- **MLflow/W&B Run**:

## Testing
- [ ] Unit tests pass (`pytest tests/unit`)
- [ ] Integration tests pass (`pytest tests/integration`)
- [ ] Model validation tests pass
- [ ] Manual testing completed
- [ ] Performance benchmarks met

## Data Changes
- [ ] No data changes
- [ ] Data schema updated (version: ___)
- [ ] New features added
- [ ] Training dataset updated

## Deployment Impact
- [ ] No deployment changes needed
- [ ] Requires model retraining
- [ ] Requires configuration updates
- [ ] Requires database migration

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Commented hard-to-understand areas
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added for new functionality
- [ ] Dependent changes merged

## Additional Notes
<!-- Any additional information -->
```

**Code Review Checklist for ML**:

**General Code Quality**:
- [ ] Code is readable and well-documented
- [ ] No hardcoded values (use config files)
- [ ] Error handling is appropriate
- [ ] Logging is comprehensive
- [ ] No security vulnerabilities

**ML-Specific**:
- [ ] Model architecture is clearly documented
- [ ] Hyperparameters are in config files
- [ ] Training data versioning is tracked
- [ ] Model performance metrics are logged
- [ ] Inference latency is acceptable
- [ ] Model size is reasonable
- [ ] Reproducibility is ensured (seeds set)
- [ ] Data validation is implemented
- [ ] Model validation metrics pass thresholds

**Testing**:
- [ ] Unit tests cover new code
- [ ] Integration tests cover workflow
- [ ] Model validation tests exist
- [ ] Edge cases are tested

**Documentation**:
- [ ] README updated if needed
- [ ] API docs updated
- [ ] Model card created/updated
- [ ] Training instructions clear

---

## 4. Continuous Integration Fundamentals

### 4.1 What is Continuous Integration?

**Continuous Integration (CI)** is the practice of automatically building and testing code changes. Every code commit triggers an automated process that:
1. Builds the code
2. Runs tests
3. Checks code quality
4. Scans for security vulnerabilities
5. Reports results

**Benefits of CI**:
- **Early bug detection**: Catch issues before they reach production
- **Faster feedback**: Know immediately if changes break anything
- **Improved code quality**: Automated checks enforce standards
- **Reduced integration problems**: Frequent integration prevents conflicts
- **Increased confidence**: Automated tests provide safety net

### 4.2 CI Pipeline Components

A comprehensive CI pipeline for ML includes:

```
┌─────────────────────────────────────────────────────────────┐
│                   CI Pipeline Stages                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Source Stage                                           │
│     └─ Checkout code from repository                       │
│                                                             │
│  2. Build Stage                                            │
│     ├─ Set up environment (Python, dependencies)          │
│     ├─ Cache dependencies                                  │
│     └─ Build Docker images (if needed)                     │
│                                                             │
│  3. Code Quality Stage                                     │
│     ├─ Linting (flake8, pylint)                          │
│     ├─ Formatting check (black, isort)                    │
│     ├─ Type checking (mypy)                               │
│     └─ Complexity analysis (radon)                        │
│                                                             │
│  4. Security Stage                                         │
│     ├─ Dependency scanning (safety, pip-audit)           │
│     ├─ SAST scanning (bandit)                            │
│     ├─ Secret detection (detect-secrets)                  │
│     └─ License compliance                                  │
│                                                             │
│  5. Test Stage                                             │
│     ├─ Unit tests (pytest)                                │
│     ├─ Integration tests                                   │
│     ├─ Data validation tests (Great Expectations)        │
│     ├─ Model validation tests                             │
│     └─ Coverage reporting (pytest-cov)                    │
│                                                             │
│  6. Artifact Stage                                         │
│     ├─ Build Docker images                                 │
│     ├─ Push to registry                                    │
│     └─ Upload test reports                                 │
│                                                             │
│  7. Notification Stage                                     │
│     └─ Notify team of results (Slack, email)              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Quality Gates

**Quality gates** are criteria that must be met for CI to pass. For ML projects:

**Code Quality Gates**:
- Linting score > 8.0/10.0
- No critical security vulnerabilities
- Code coverage > 80%
- No type errors (mypy)
- Maximum cyclomatic complexity < 10

**ML-Specific Quality Gates**:
- Data validation tests pass
- Model performance > baseline
- Inference latency < threshold
- Model size < limit
- Training reproducibility verified

**Example Quality Gate Configuration**:

```yaml
# quality_gates.yaml
code_quality:
  pylint_score_min: 8.0
  flake8_max_errors: 0
  mypy_strict: true
  max_complexity: 10

testing:
  min_coverage: 80
  require_unit_tests: true
  require_integration_tests: true

security:
  allow_high_vulnerabilities: false
  allow_medium_vulnerabilities: false
  allow_low_vulnerabilities: true

ml_validation:
  min_accuracy: 0.85
  max_inference_latency_ms: 100
  max_model_size_mb: 500
  require_data_validation: true
```

### 4.4 CI Best Practices

**1. Keep CI Fast**:
- Target: CI should complete in < 10 minutes
- Use caching for dependencies
- Parallelize independent jobs
- Run expensive tests only on main branch

**2. Fail Fast**:
- Run quick checks first (linting, formatting)
- Stop pipeline on first failure
- Provide clear error messages

**3. Make CI Deterministic**:
- Use fixed versions for dependencies
- Set random seeds for ML code
- Avoid time-dependent tests
- Use consistent test data

**4. Comprehensive Testing**:
- Unit tests for individual functions
- Integration tests for workflows
- Data validation for input data
- Model validation for performance

**5. Clear Feedback**:
- Provide detailed logs
- Show exactly what failed
- Include links to artifacts
- Notify relevant team members

**6. Security First**:
- Scan dependencies for vulnerabilities
- Check for hardcoded secrets
- Validate input data
- Use secure base images

### 4.5 CI Configuration Files

**Example .flake8**:
```ini
[flake8]
max-line-length = 100
exclude =
    .git,
    __pycache__,
    venv,
    build,
    dist,
    *.egg-info,
    .tox

ignore =
    E203,  # Whitespace before ':'
    W503,  # Line break before binary operator
    E501   # Line too long (covered by black)

per-file-ignores =
    __init__.py:F401,F403
    tests/*:D

max-complexity = 10
```

**Example mypy.ini**:
```ini
[mypy]
python_version = 3.10
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = False
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True
strict_equality = True

[mypy-numpy.*]
ignore_missing_imports = True

[mypy-pandas.*]
ignore_missing_imports = True

[mypy-sklearn.*]
ignore_missing_imports = True
```

**Example .bandit**:
```yaml
# .bandit
exclude_dirs:
  - /tests/
  - /venv/
  - /.tox/

tests:
  - B201  # flask_debug_true
  - B301  # pickle
  - B302  # marshal
  - B303  # md5
  - B304  # ciphers
  - B305  # cipher_modes
  - B306  # mktemp_q

skips:
  - B101  # assert_used (OK in tests)
  - B601  # paramiko_calls
```

---

## 5. GitHub Actions for ML

### 5.1 GitHub Actions Basics

**GitHub Actions** is a CI/CD platform that automates workflows directly in your GitHub repository.

**Key Concepts**:
- **Workflow**: Automated process defined in YAML
- **Job**: Set of steps that execute on the same runner
- **Step**: Individual task (run command, use action)
- **Runner**: Server that runs workflows (GitHub-hosted or self-hosted)
- **Action**: Reusable unit of code

**Workflow File Structure**:
```yaml
name: Workflow Name
on: [triggers]
env:
  [environment variables]
jobs:
  job-name:
    runs-on: ubuntu-latest
    steps:
      - name: Step Name
        uses: action@version
        with:
          [parameters]
```

### 5.2 Workflow Triggers

**Common Triggers**:

```yaml
# Trigger on push to specific branches
on:
  push:
    branches: [ main, develop ]

# Trigger on pull requests
on:
  pull_request:
    branches: [ main ]

# Trigger on schedule (cron)
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC

# Trigger manually
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        type: choice
        options:
          - staging
          - production

# Multiple triggers
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday
```

### 5.3 Complete ML CI Workflow

**`.github/workflows/ci.yml`**:

```yaml
name: ML CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  PYTHON_VERSION: '3.10'
  CACHE_KEY: ml-deps-v1

jobs:
  # Job 1: Code Quality
  code-quality:
    name: Code Quality Checks
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install flake8 pylint mypy black isort
          pip install -r requirements.txt

      - name: Run black (formatting check)
        run: black --check --diff src/ tests/

      - name: Run isort (import sorting)
        run: isort --check-only --diff src/ tests/

      - name: Run flake8 (linting)
        run: flake8 src/ tests/ --count --statistics

      - name: Run pylint (linting)
        run: pylint src/ --fail-under=8.0

      - name: Run mypy (type checking)
        run: mypy src/

  # Job 2: Security Scanning
  security:
    name: Security Scan
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install security tools
        run: |
          pip install bandit safety detect-secrets pip-audit

      - name: Run Bandit (SAST)
        run: bandit -r src/ -f json -o bandit-report.json

      - name: Run Safety (dependency scan)
        run: safety check --json

      - name: Run pip-audit (vulnerability scan)
        run: pip-audit --requirement requirements.txt

      - name: Detect secrets
        run: detect-secrets scan --baseline .secrets.baseline

      - name: Upload security reports
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: security-reports
          path: "*-report.json"

  # Job 3: Unit Tests
  test-unit:
    name: Unit Tests (Python ${{ matrix.python-version }})
    runs-on: ubuntu-latest
    timeout-minutes: 15
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-xdist

      - name: Run unit tests
        run: pytest tests/unit -v --cov=src --cov-report=xml --cov-report=html -n auto

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-${{ matrix.python-version }}

      - name: Upload coverage report
        uses: actions/upload-artifact@v3
        with:
          name: coverage-report-${{ matrix.python-version }}
          path: htmlcov/

  # Job 4: Integration Tests
  test-integration:
    name: Integration Tests
    runs-on: ubuntu-latest
    needs: test-unit
    timeout-minutes: 20

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest

      - name: Run integration tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/testdb
        run: pytest tests/integration -v

  # Job 5: Data Validation
  test-data:
    name: Data Validation Tests
    runs-on: ubuntu-latest
    needs: test-unit
    timeout-minutes: 15

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install great-expectations pytest

      - name: Run data validation tests
        run: pytest tests/data -v

      - name: Upload data validation report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: data-validation-report
          path: great_expectations/uncommitted/data_docs/

  # Job 6: Model Validation
  test-model:
    name: Model Validation Tests
    runs-on: ubuntu-latest
    needs: [test-unit, test-data]
    timeout-minutes: 30

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest

      - name: Download test data
        run: |
          # Download test dataset from S3/GCS or use cached
          python scripts/download_test_data.py

      - name: Run model validation tests
        run: pytest tests/model -v

      - name: Check model performance
        run: |
          python scripts/validate_model_performance.py \
            --min-accuracy 0.85 \
            --max-latency-ms 100

  # Job 7: Build Docker Images
  build:
    name: Build Docker Images
    runs-on: ubuntu-latest
    needs: [code-quality, security, test-unit, test-integration]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    timeout-minutes: 20

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push training image
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./Dockerfile.train
          push: true
          tags: |
            ghcr.io/${{ github.repository }}/training:latest
            ghcr.io/${{ github.repository }}/training:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Build and push serving image
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./Dockerfile.serve
          push: true
          tags: |
            ghcr.io/${{ github.repository }}/serving:latest
            ghcr.io/${{ github.repository }}/serving:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # Job 8: Notification
  notify:
    name: Send Notifications
    runs-on: ubuntu-latest
    needs: [code-quality, security, test-unit, test-integration, test-data, test-model]
    if: always()

    steps:
      - name: Send Slack notification
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: |
            CI Pipeline ${{ job.status }}
            Repository: ${{ github.repository }}
            Branch: ${{ github.ref }}
            Commit: ${{ github.sha }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
        if: always()
```

### 5.4 Caching Strategies

Caching dramatically speeds up CI by reusing dependencies and build artifacts.

**Pip Cache**:
```yaml
- name: Cache pip dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

**Poetry Cache**:
```yaml
- name: Cache Poetry dependencies
  uses: actions/cache@v3
  with:
    path: |
      ~/.cache/pypoetry
      ~/.virtualenvs
    key: ${{ runner.os }}-poetry-${{ hashFiles('**/poetry.lock') }}
    restore-keys: |
      ${{ runner.os }}-poetry-
```

**Docker Layer Cache**:
```yaml
- name: Build with layer caching
  uses: docker/build-push-action@v4
  with:
    context: .
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**Model/Data Cache** (for testing):
```yaml
- name: Cache test data
  uses: actions/cache@v3
  with:
    path: data/test
    key: test-data-${{ hashFiles('data/test/**') }}

- name: Cache test models
  uses: actions/cache@v3
  with:
    path: models/test
    key: test-models-v1
```

### 5.5 Matrix Builds

Test across multiple Python versions, OS, or configurations:

```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']
    os: [ubuntu-latest, macos-latest, windows-latest]
    exclude:
      # Exclude Python 3.11 on Windows (example)
      - os: windows-latest
        python-version: '3.11'

steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v4
    with:
      python-version: ${{ matrix.python-version }}
  - run: pytest
```

### 5.6 Secrets Management

**Store secrets in GitHub Secrets**:
```yaml
steps:
  - name: Deploy to AWS
    env:
      AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
    run: |
      python deploy.py
```

**Never log secrets**:
```yaml
- name: Use secret safely
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: |
    # Don't echo secrets!
    # echo "API_KEY=$API_KEY"  # ❌ BAD
    python script.py  # ✅ GOOD (script uses env var)
```

---

## 6. Docker and Containerization

### 6.1 Why Docker for ML?

**Docker** packages your application and dependencies into containers that run consistently across any environment.

**Benefits for ML**:
- **Reproducibility**: Same environment everywhere
- **Isolation**: Dependencies don't conflict
- **Portability**: Works on any system with Docker
- **Scalability**: Easy to deploy multiple instances
- **Version control**: Docker images are versioned

**ML-Specific Challenges**:
- Large images (models, data, dependencies)
- GPU support requirements
- Long build times
- Frequent model updates

### 6.2 Docker Basics

**Core Docker Concepts**:
```
Dockerfile → Docker Image → Docker Container
   (recipe)    (template)      (running instance)
```

**Essential Docker Commands**:
```bash
# Build image
docker build -t my-ml-app:latest .
docker build -f Dockerfile.train -t training:v1 .

# Run container
docker run -p 8000:8000 my-ml-app:latest
docker run -it --rm my-ml-app:latest /bin/bash  # Interactive

# List images and containers
docker images
docker ps
docker ps -a  # Include stopped containers

# Remove images and containers
docker rmi image-name
docker rm container-id

# Push to registry
docker tag my-ml-app:latest ghcr.io/username/my-ml-app:latest
docker push ghcr.io/username/my-ml-app:latest

# Pull from registry
docker pull ghcr.io/username/my-ml-app:latest

# View logs
docker logs container-id
docker logs -f container-id  # Follow logs

# Execute command in running container
docker exec -it container-id /bin/bash
docker exec container-id python script.py

# Inspect container
docker inspect container-id
docker stats container-id
```

### 6.3 Dockerfile Best Practices

**Training Dockerfile**:

```dockerfile
# Use official Python slim image for smaller size
FROM python:3.10-slim AS base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 mluser && chown -R mluser:mluser /app
USER mluser

# Copy and install Python dependencies first (layer caching)
COPY --chown=mluser:mluser requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application code
COPY --chown=mluser:mluser src/ ./src/
COPY --chown=mluser:mluser scripts/ ./scripts/

# Set Python path
ENV PYTHONPATH=/app
ENV PATH=/home/mluser/.local/bin:$PATH

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV MODEL_DIR=/models
ENV DATA_DIR=/data

# Create directories
RUN mkdir -p /models /data

# Healthcheck (if applicable)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python scripts/healthcheck.py || exit 1

# Default command
CMD ["python", "src/train.py"]
```

**Serving Dockerfile (Multi-Stage Build)**:

```dockerfile
# Stage 1: Builder
FROM python:3.10-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.10-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 mluser && chown -R mluser:mluser /app
USER mluser

# Copy Python dependencies from builder
COPY --from=builder --chown=mluser:mluser /root/.local /home/mluser/.local

# Copy application code
COPY --chown=mluser:mluser src/ ./src/
COPY --chown=mluser:mluser models/ ./models/

# Environment variables
ENV PYTHONPATH=/app
ENV PATH=/home/mluser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=/app/models/model.pkl

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run FastAPI server
CMD ["uvicorn", "src.serve:app", "--host", "0.0.0.0", "--port", "8000"]
```

**GPU Dockerfile**:

```dockerfile
# Use NVIDIA CUDA base image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Install Python
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install PyTorch with CUDA support
RUN pip3 install --no-cache-dir \
    torch==2.0.0+cu118 \
    torchvision==0.15.0+cu118 \
    --index-url https://download.pytorch.org/whl/cu118

# Copy and install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy code
COPY src/ ./src/

# Set environment
ENV PYTHONPATH=/app
ENV CUDA_VISIBLE_DEVICES=0

CMD ["python3", "src/train.py"]
```

### 6.4 Dockerfile Optimization Techniques

**1. Layer Caching**:
```dockerfile
# ❌ BAD: Installs deps every time code changes
COPY . .
RUN pip install -r requirements.txt

# ✅ GOOD: Caches deps until requirements change
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

**2. Multi-Stage Builds**:
```dockerfile
# Build stage: includes build tools
FROM python:3.10 AS builder
RUN apt-get install build-essential
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage: slim, only runtime deps
FROM python:3.10-slim
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
```

**3. .dockerignore**:
```
# .dockerignore
__pycache__/
*.pyc
.git/
.gitignore
.env
venv/
tests/
docs/
*.md
.pytest_cache/
.coverage
mlruns/
data/  # Don't copy large data into image
models/  # Download models at runtime
```

**4. Minimize Layers**:
```dockerfile
# ❌ BAD: Creates 3 layers
RUN apt-get update
RUN apt-get install -y python3
RUN rm -rf /var/lib/apt/lists/*

# ✅ GOOD: Single layer
RUN apt-get update && \
    apt-get install -y python3 && \
    rm -rf /var/lib/apt/lists/*
```

**5. Use --no-cache-dir**:
```dockerfile
# Saves space
RUN pip install --no-cache-dir -r requirements.txt
```

**6. Pin Versions**:
```dockerfile
# ❌ BAD: Version can change
FROM python:3.10

# ✅ GOOD: Specific version
FROM python:3.10.12-slim-bullseye
```

### 6.5 Docker Compose for ML

**docker-compose.yml**:

```yaml
version: '3.8'

services:
  # Model training service
  training:
    build:
      context: .
      dockerfile: Dockerfile.train
    volumes:
      - ./data:/data
      - ./models:/models
      - ./mlruns:/mlruns
    environment:
      - MLFLOW_TRACKING_URI=http://mlflow:5000
      - DATA_PATH=/data
      - MODEL_PATH=/models
    networks:
      - ml-network
    depends_on:
      - mlflow
      - postgres

  # Model serving service
  serving:
    build:
      context: .
      dockerfile: Dockerfile.serve
    ports:
      - "8000:8000"
    volumes:
      - ./models:/models:ro  # Read-only
    environment:
      - MODEL_PATH=/models/model.pkl
      - LOG_LEVEL=INFO
    networks:
      - ml-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 5s
    restart: unless-stopped

  # MLflow tracking server
  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.9.2
    ports:
      - "5000:5000"
    volumes:
      - ./mlruns:/mlruns
    environment:
      - BACKEND_STORE_URI=postgresql://mlflow:mlflow@postgres:5432/mlflow
      - DEFAULT_ARTIFACT_ROOT=/mlruns
    command: >
      mlflow server
      --backend-store-uri postgresql://mlflow:mlflow@postgres:5432/mlflow
      --default-artifact-root /mlruns
      --host 0.0.0.0
      --port 5000
    networks:
      - ml-network
    depends_on:
      - postgres

  # PostgreSQL database
  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=mlflow
      - POSTGRES_USER=mlflow
      - POSTGRES_PASSWORD=mlflow
    networks:
      - ml-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mlflow"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Prometheus (monitoring)
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    networks:
      - ml-network

  # Grafana (visualization)
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    networks:
      - ml-network
    depends_on:
      - prometheus

networks:
  ml-network:
    driver: bridge

volumes:
  postgres-data:
  prometheus-data:
  grafana-data:
```

**Usage**:
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f serving

# Stop all services
docker-compose down

# Rebuild and start
docker-compose up -d --build

# Scale serving instances
docker-compose up -d --scale serving=3

# Run command in service
docker-compose exec training python scripts/train.py
```

### 6.6 Docker Security Best Practices

**1. Use Non-Root User**:
```dockerfile
RUN useradd -m -u 1000 mluser
USER mluser
```

**2. Scan for Vulnerabilities**:
```bash
# Trivy scanner
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image my-ml-app:latest

# Snyk
snyk container test my-ml-app:latest
```

**3. Use Minimal Base Images**:
```dockerfile
# Prefer slim/alpine variants
FROM python:3.10-slim
# or
FROM python:3.10-alpine
```

**4. Don't Store Secrets in Images**:
```dockerfile
# ❌ BAD
ENV API_KEY=secret123

# ✅ GOOD: Pass at runtime
docker run -e API_KEY=$API_KEY my-ml-app
```

**5. Read-Only Filesystem** (where possible):
```yaml
services:
  serving:
    read_only: true
    tmpfs:
      - /tmp
```

**6. Limit Resources**:
```yaml
services:
  training:
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 8G
        reservations:
          cpus: '2.0'
          memory: 4G
```

---

_[Due to length constraints, I'll continue with the remaining sections in the next part. This covers the first 6 major sections of the lecture notes. Would you like me to continue with sections 7-12?]_


## 7. Testing Strategies for ML Systems

### 7.1 The ML Testing Pyramid

Traditional software has a testing pyramid, but **ML systems require an expanded testing pyramid**:

```
                    ┌─────────────┐
                    │   Manual    │
                    │   Testing   │
                    └─────────────┘
               ┌──────────────────────┐
               │  Model Validation    │
               │   Tests (Perf)       │
               └──────────────────────┘
          ┌───────────────────────────────┐
          │    Integration Tests          │
          │  (Pipeline, Data, Model)      │
          └───────────────────────────────┘
     ┌──────────────────────────────────────────┐
     │         Data Validation Tests            │
     │    (Schema, Quality, Drift)              │
     └──────────────────────────────────────────┘
┌────────────────────────────────────────────────────┐
│              Unit Tests                            │
│   (Code, Preprocessing, Utils)                     │
└────────────────────────────────────────────────────┘
```

**Test Types for ML**:
1. **Unit Tests**: Test individual functions and classes
2. **Data Validation Tests**: Validate data quality and schema
3. **Integration Tests**: Test component interactions
4. **Model Validation Tests**: Test model performance
5. **End-to-End Tests**: Test complete ML pipeline
6. **Manual/Exploratory Testing**: Human validation

### 7.2 Unit Testing for ML Code

**Test Data Processing Functions**:

```python
# src/preprocessing.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def handle_missing_values(df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
    """Fill missing values using specified strategy."""
    if strategy == 'mean':
        return df.fillna(df.mean())
    elif strategy == 'median':
        return df.fillna(df.median())
    elif strategy == 'zero':
        return df.fillna(0)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

def encode_categorical(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """One-hot encode categorical columns."""
    return pd.get_dummies(df, columns=columns, drop_first=True)

# tests/unit/test_preprocessing.py
import pytest
import pandas as pd
import numpy as np
from src.preprocessing import handle_missing_values, encode_categorical

class TestHandleMissingValues:
    """Test suite for missing value handling."""

    def test_mean_strategy(self):
        """Test that mean strategy fills with column mean."""
        df = pd.DataFrame({
            'a': [1.0, 2.0, np.nan, 4.0],
            'b': [10.0, np.nan, 30.0, 40.0]
        })

        result = handle_missing_values(df, strategy='mean')

        assert result['a'].isna().sum() == 0
        assert result['b'].isna().sum() == 0
        assert result.loc[2, 'a'] == pytest.approx(2.33, abs=0.01)
        assert result.loc[1, 'b'] == pytest.approx(26.67, abs=0.01)

    def test_median_strategy(self):
        """Test that median strategy fills with column median."""
        df = pd.DataFrame({'a': [1.0, 2.0, np.nan, 100.0]})

        result = handle_missing_values(df, strategy='median')

        assert result['a'].isna().sum() == 0
        assert result.loc[2, 'a'] == 2.0  # Median of [1, 2, 100]

    def test_zero_strategy(self):
        """Test that zero strategy fills with 0."""
        df = pd.DataFrame({'a': [1.0, np.nan, 3.0]})

        result = handle_missing_values(df, strategy='zero')

        assert result.loc[1, 'a'] == 0.0

    def test_invalid_strategy_raises_error(self):
        """Test that invalid strategy raises ValueError."""
        df = pd.DataFrame({'a': [1.0, np.nan, 3.0]})

        with pytest.raises(ValueError, match="Unknown strategy"):
            handle_missing_values(df, strategy='invalid')

    @pytest.mark.parametrize('strategy', ['mean', 'median', 'zero'])
    def test_no_missing_values_unchanged(self, strategy):
        """Test that data without NaN is unchanged."""
        df = pd.DataFrame({'a': [1.0, 2.0, 3.0], 'b': [4.0, 5.0, 6.0]})
        original = df.copy()

        result = handle_missing_values(df, strategy=strategy)

        pd.testing.assert_frame_equal(result, original)


class TestEncodeCategorical:
    """Test suite for categorical encoding."""

    def test_one_hot_encoding(self):
        """Test basic one-hot encoding."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'A', 'C'],
            'value': [1, 2, 3, 4]
        })

        result = encode_categorical(df, columns=['category'])

        assert 'category' not in result.columns
        assert 'category_B' in result.columns
        assert 'category_C' in result.columns
        assert result.shape[1] == 3  # value + 2 encoded columns

    def test_multiple_columns(self):
        """Test encoding multiple categorical columns."""
        df = pd.DataFrame({
            'cat1': ['A', 'B', 'A'],
            'cat2': ['X', 'Y', 'X'],
            'value': [1, 2, 3]
        })

        result = encode_categorical(df, columns=['cat1', 'cat2'])

        assert 'cat1' not in result.columns
        assert 'cat2' not in result.columns
        assert 'cat1_B' in result.columns
        assert 'cat2_Y' in result.columns
```

**Test Model Training Functions**:

```python
# tests/unit/test_training.py
import pytest
import numpy as np
from sklearn.datasets import make_classification
from src.train import train_model, evaluate_model

@pytest.fixture
def training_data():
    """Generate synthetic training data."""
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        random_state=42
    )
    return X, y

def test_train_model_returns_fitted_model(training_data):
    """Test that train_model returns a fitted estimator."""
    X, y = training_data

    model = train_model(X, y, model_type='random_forest')

    assert hasattr(model, 'predict')
    assert hasattr(model, 'predict_proba')
    assert model.n_features_in_ == 20

def test_evaluate_model_returns_metrics(training_data):
    """Test that evaluate_model returns expected metrics."""
    X, y = training_data
    model = train_model(X, y, model_type='random_forest')

    metrics = evaluate_model(model, X, y)

    assert 'accuracy' in metrics
    assert 'precision' in metrics
    assert 'recall' in metrics
    assert 'f1' in metrics
    assert 0.0 <= metrics['accuracy'] <= 1.0
```

### 7.3 Data Validation Testing

**Using Great Expectations**:

```python
# tests/data/test_data_quality.py
import pytest
import pandas as pd
import great_expectations as gx

@pytest.fixture
def sample_training_data():
    """Load sample training data."""
    return pd.read_parquet('data/sample_train.parquet')

def test_data_schema_validation(sample_training_data):
    """Test that data conforms to expected schema."""
    df = sample_training_data

    # Check required columns exist
    required_columns = ['feature_1', 'feature_2', 'feature_3', 'target']
    assert all(col in df.columns for col in required_columns)

    # Check column types
    assert df['feature_1'].dtype == np.float64
    assert df['feature_2'].dtype == np.int64
    assert df['target'].dtype == np.int64

def test_data_completeness(sample_training_data):
    """Test that data has minimal missing values."""
    df = sample_training_data

    # Check for excessive missing values
    missing_pct = df.isnull().sum() / len(df) * 100

    assert missing_pct['feature_1'] < 5.0, "feature_1 has >5% missing"
    assert missing_pct['target'] == 0.0, "Target has missing values"

def test_data_ranges_with_great_expectations(sample_training_data):
    """Test data ranges using Great Expectations."""
    df = sample_training_data

    context = gx.get_context()

    # Create validator
    validator = context.sources.pandas_default.read_dataframe(df)

    # Add expectations
    validator.expect_column_values_to_be_between(
        column="feature_1",
        min_value=-5.0,
        max_value=5.0
    )

    validator.expect_column_values_to_be_in_set(
        column="target",
        value_set=[0, 1]
    )

    validator.expect_table_row_count_to_be_between(
        min_value=1000,
        max_value=100000
    )

    # Validate
    results = validator.validate()

    assert results['success'], f"Validation failed: {results}"

def test_no_data_leakage(sample_training_data):
    """Test for data leakage indicators."""
    df = sample_training_data

    # Check for duplicate rows
    duplicates = df.duplicated().sum()
    assert duplicates == 0, f"Found {duplicates} duplicate rows"

    # Check for target leakage (perfect correlation)
    for col in df.columns:
        if col != 'target':
            correlation = df[col].corr(df['target'])
            assert abs(correlation) < 0.99, f"{col} has suspicious correlation with target: {correlation}"
```

### 7.4 Integration Testing

**Test Complete Pipeline**:

```python
# tests/integration/test_pipeline.py
import pytest
import mlflow
import pandas as pd
from src.pipeline import MLPipeline

@pytest.fixture(scope="module")
def mlflow_tracking():
    """Set up MLflow tracking for tests."""
    mlflow.set_tracking_uri("sqlite:///test_mlruns.db")
    mlflow.set_experiment("test_pipeline")
    yield
    # Cleanup after all tests
    mlflow.end_run()

def test_end_to_end_training_pipeline(mlflow_tracking, tmp_path):
    """Test complete training pipeline execution."""
    # Arrange
    config = {
        'data_path': 'data/test_data.parquet',
        'model_type': 'random_forest',
        'test_size': 0.2,
        'random_state': 42
    }

    pipeline = MLPipeline(config)

    # Act
    with mlflow.start_run():
        model, metrics = pipeline.run_training()

    # Assert
    assert model is not None
    assert 'accuracy' in metrics
    assert metrics['accuracy'] > 0.7  # Minimum acceptable
    assert mlflow.active_run() is not None

def test_pipeline_handles_missing_data():
    """Test that pipeline gracefully handles missing data."""
    config = {'data_path': 'data/data_with_missing.parquet'}
    pipeline = MLPipeline(config)

    # Should not raise exception
    model, metrics = pipeline.run_training()

    assert model is not None

def test_pipeline_logs_to_mlflow(mlflow_tracking):
    """Test that pipeline logs artifacts to MLflow."""
    config = {'data_path': 'data/test_data.parquet'}
    pipeline = MLPipeline(config)

    with mlflow.start_run() as run:
        pipeline.run_training()

        # Check logged parameters
        run_data = mlflow.get_run(run.info.run_id).data
        assert 'model_type' in run_data.params
        assert 'test_size' in run_data.params

        # Check logged metrics
        assert 'accuracy' in run_data.metrics
        assert 'precision' in run_data.metrics
```

### 7.5 Model Validation Testing

**Performance and Behavior Tests**:

```python
# tests/model/test_model_validation.py
import pytest
import numpy as np
import pickle
from sklearn.metrics import accuracy_score, f1_score

@pytest.fixture
def trained_model():
    """Load trained model for testing."""
    with open('models/test_model.pkl', 'rb') as f:
        return pickle.load(f)

@pytest.fixture
def test_data():
    """Load test dataset."""
    import pandas as pd
    df = pd.read_parquet('data/test_data.parquet')
    X = df.drop('target', axis=1)
    y = df['target']
    return X, y

def test_model_meets_accuracy_threshold(trained_model, test_data):
    """Test that model meets minimum accuracy requirement."""
    X_test, y_test = test_data

    y_pred = trained_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    assert accuracy >= 0.85, f"Accuracy {accuracy:.3f} below threshold 0.85"

def test_model_meets_f1_threshold(trained_model, test_data):
    """Test that model meets minimum F1 score."""
    X_test, y_test = test_data

    y_pred = trained_model.predict(X_test)
    f1 = f1_score(y_test, y_pred)

    assert f1 >= 0.80, f"F1 score {f1:.3f} below threshold 0.80"

def test_model_predictions_are_valid(trained_model, test_data):
    """Test that model outputs are in valid range."""
    X_test, _ = test_data

    predictions = trained_model.predict(X_test)
    probabilities = trained_model.predict_proba(X_test)

    # Check predictions are binary
    assert set(predictions).issubset({0, 1})

    # Check probabilities sum to 1
    assert np.allclose(probabilities.sum(axis=1), 1.0)

    # Check probabilities are in [0, 1]
    assert np.all(probabilities >= 0.0) and np.all(probabilities <= 1.0)

def test_model_is_deterministic(trained_model, test_data):
    """Test that model produces consistent predictions."""
    X_test, _ = test_data

    pred1 = trained_model.predict(X_test)
    pred2 = trained_model.predict(X_test)

    np.testing.assert_array_equal(pred1, pred2)

def test_model_inference_latency(trained_model, test_data):
    """Test that model inference is fast enough."""
    import time

    X_test, _ = test_data
    X_sample = X_test.iloc[:100]  # Test on 100 samples

    start = time.time()
    _ = trained_model.predict(X_sample)
    end = time.time()

    latency_ms = (end - start) * 1000 / len(X_sample)

    assert latency_ms < 10.0, f"Inference latency {latency_ms:.2f}ms exceeds 10ms threshold"

def test_model_handles_edge_cases(trained_model):
    """Test model behavior on edge cases."""
    import pandas as pd

    # Test with all zeros
    X_zeros = pd.DataFrame(np.zeros((10, 20)))
    pred_zeros = trained_model.predict(X_zeros)
    assert len(pred_zeros) == 10

    # Test with extreme values
    X_extreme = pd.DataFrame(np.ones((10, 20)) * 1000)
    pred_extreme = trained_model.predict(X_extreme)
    assert len(pred_extreme) == 10

@pytest.mark.slow
def test_model_performance_on_subgroups(trained_model, test_data):
    """Test model fairness across subgroups."""
    X_test, y_test = test_data

    # Test performance on different segments
    # (Assuming feature_3 is a sensitive attribute)
    segments = X_test['feature_3'].unique()

    accuracies = {}
    for segment in segments:
        mask = X_test['feature_3'] == segment
        X_seg = X_test[mask]
        y_seg = y_test[mask]

        if len(X_seg) > 0:
            y_pred = trained_model.predict(X_seg)
            accuracies[segment] = accuracy_score(y_seg, y_pred)

    # Check that performance is reasonably consistent
    if len(accuracies) > 1:
        max_diff = max(accuracies.values()) - min(accuracies.values())
        assert max_diff < 0.10, f"Performance varies too much across segments: {accuracies}"
```

### 7.6 pytest Configuration

**pytest.ini**:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (slower, dependencies)
    model: Model validation tests
    data: Data validation tests
    slow: Slow running tests (> 1 minute)
    smoke: Smoke tests for quick validation

addopts =
    -v
    --strict-markers
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-report=xml
    --cov-fail-under=80
    --maxfail=5
    --tb=short

# Timeout for tests (seconds)
timeout = 300

# Parallel execution
# Run with: pytest -n auto
# Requires: pip install pytest-xdist

filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning

[coverage:run]
source = src
omit =
    */tests/*
    */venv/*
    */__pycache__/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
```

**conftest.py** (Shared Fixtures):

```python
# tests/conftest.py
"""Shared pytest fixtures and configuration."""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import mlflow

@pytest.fixture(scope="session")
def test_data_dir():
    """Get test data directory."""
    return Path(__file__).parent / "data"

@pytest.fixture
def sample_dataframe():
    """Generate sample DataFrame for testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'feature_1': np.random.normal(0, 1, 1000),
        'feature_2': np.random.exponential(2, 1000),
        'feature_3': np.random.choice(['A', 'B', 'C'], 1000),
        'target': np.random.binomial(1, 0.3, 1000)
    })

@pytest.fixture
def temp_directory():
    """Create temporary directory for test artifacts."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture(scope="session")
def mlflow_test_tracking():
    """Set up MLflow tracking for test session."""
    mlflow.set_tracking_uri("sqlite:///test_mlruns.db")
    yield
    # Cleanup handled by temporary file

@pytest.fixture(autouse=True)
def reset_random_seeds():
    """Reset random seeds before each test."""
    np.random.seed(42)
    import random
    random.seed(42)
```

---

## 8. Continuous Deployment

### 8.1 CD vs CD: Deployment vs Delivery

**Continuous Delivery**:
- Automated preparation for release
- Manual approval required for production
- Every change is deployment-ready
- Human decision to deploy

**Continuous Deployment**:
- Fully automated release process
- No manual intervention
- Every passing change goes to production
- Requires high confidence in automation

**For ML Systems**, most organizations use **Continuous Delivery** with:
- Automated deployment to staging
- Manual approval for production
- Automated rollback capabilities

### 8.2 Deployment Pipeline Stages

```
┌────────────────────────────────────────────────────────────┐
│              Continuous Deployment Pipeline                │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Build Stage                                           │
│     ├─ Build Docker images                                │
│     ├─ Tag with version/git SHA                          │
│     └─ Push to container registry                         │
│                                                            │
│  2. Deploy to Staging                                     │
│     ├─ Update Kubernetes manifests                       │
│     ├─ Apply deployment                                   │
│     ├─ Wait for rollout completion                       │
│     └─ Verify health checks pass                         │
│                                                            │
│  3. Test in Staging                                       │
│     ├─ Run smoke tests                                    │
│     ├─ Run integration tests                             │
│     ├─ Performance testing                               │
│     └─ Generate test report                              │
│                                                            │
│  4. Manual Approval (optional)                            │
│     └─ Review metrics and approve                         │
│                                                            │
│  5. Deploy to Production                                  │
│     ├─ Blue-green or canary deployment                   │
│     ├─ Monitor error rates                               │
│     ├─ Monitor model performance                         │
│     └─ Complete rollout or rollback                      │
│                                                            │
│  6. Post-Deployment                                       │
│     ├─ Verify production health                          │
│     ├─ Update model registry                             │
│     ├─ Send notifications                                │
│     └─ Archive artifacts                                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 8.3 Kubernetes Deployment Manifests

**Deployment YAML**:

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model-serving
  namespace: production
  labels:
    app: ml-model
    version: v1.2.0
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: ml-model
  template:
    metadata:
      labels:
        app: ml-model
        version: v1.2.0
    spec:
      containers:
      - name: model-server
        image: ghcr.io/org/ml-model:v1.2.0
        ports:
        - containerPort: 8000
          name: http
        env:
        - name: MODEL_PATH
          value: /models/model.pkl
        - name: LOG_LEVEL
          value: INFO
        - name: WORKERS
          value: "4"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        volumeMounts:
        - name: model-storage
          mountPath: /models
          readOnly: true
      volumes:
      - name: model-storage
        persistentVolumeClaim:
          claimName: model-pvc
```

**Service YAML**:

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: ml-model-service
  namespace: production
spec:
  type: LoadBalancer
  selector:
    app: ml-model
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
    name: http
  sessionAffinity: None
```

**HorizontalPodAutoscaler**:

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-model-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-model-serving
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 2
        periodSeconds: 15
      selectPolicy: Max
```

### 8.4 CD Workflow with GitHub Actions

**`.github/workflows/cd.yml`**:

```yaml
name: Continuous Deployment

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        type: choice
        options:
          - staging
          - production

env:
  IMAGE_NAME: ghcr.io/${{ github.repository }}/ml-model

jobs:
  build-and-push:
    name: Build and Push Docker Image
    runs-on: ubuntu-latest
    outputs:
      image_tag: ${{ steps.meta.outputs.tags }}
      image_digest: ${{ steps.build.outputs.digest }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-

      - name: Build and push
        id: build
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./Dockerfile.serve
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    name: Deploy to Staging
    needs: build-and-push
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging-ml.example.com

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG_STAGING }}

      - name: Update deployment image
        run: |
          kubectl set image deployment/ml-model-serving \
            model-server=${{ needs.build-and-push.outputs.image_tag }} \
            -n staging

      - name: Wait for rollout
        run: |
          kubectl rollout status deployment/ml-model-serving -n staging
          kubectl wait --for=condition=available --timeout=300s \
            deployment/ml-model-serving -n staging

      - name: Run smoke tests
        run: |
          python scripts/smoke_tests.py --endpoint https://staging-ml.example.com

  deploy-production:
    name: Deploy to Production
    needs: [build-and-push, deploy-staging]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v')
    environment:
      name: production
      url: https://ml.example.com

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG_PROD }}

      - name: Deploy with blue-green strategy
        run: |
          # Deploy to green environment
          kubectl apply -f k8s/deployment-green.yaml
          kubectl set image deployment/ml-model-green \
            model-server=${{ needs.build-and-push.outputs.image_tag }} \
            -n production

          # Wait for green deployment
          kubectl rollout status deployment/ml-model-green -n production

      - name: Run production smoke tests
        run: |
          python scripts/smoke_tests.py --endpoint https://green.ml.example.com

      - name: Switch traffic to green
        run: |
          kubectl patch service ml-model-service -n production \
            -p '{"spec":{"selector":{"version":"green"}}}'

      - name: Monitor for 5 minutes
        run: |
          python scripts/monitor_deployment.py \
            --duration 300 \
            --error-threshold 0.01 \
            --latency-threshold 200

      - name: Cleanup old blue deployment
        if: success()
        run: |
          kubectl delete deployment ml-model-blue -n production --ignore-not-found

      - name: Rollback on failure
        if: failure()
        run: |
          kubectl patch service ml-model-service -n production \
            -p '{"spec":{"selector":{"version":"blue"}}}'
          kubectl delete deployment ml-model-green -n production

  notify:
    name: Send Deployment Notification
    needs: [deploy-staging, deploy-production]
    runs-on: ubuntu-latest
    if: always()

    steps:
      - name: Send Slack notification
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: |
            Deployment ${{ job.status }}
            Image: ${{ needs.build-and-push.outputs.image_tag }}
            Environment: ${{ github.event.inputs.environment || 'staging + production' }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 9. Deployment Strategies

### 9.1 Rolling Deployment

**Default Kubernetes strategy**. Gradually replaces old pods with new ones.

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Max new pods beyond desired count
      maxUnavailable: 0   # Max old pods that can be down
```

**Pros**:
- Zero downtime
- Simple to implement
- Automatic rollback if health checks fail

**Cons**:
- Two versions running simultaneously
- Slow rollout for many replicas
- Can't easily test before full rollout

**Use When**: Low-risk changes, established ML models

### 9.2 Blue-Green Deployment

**Two identical environments** (blue = current, green = new). Switch traffic after validation.

```bash
# Deploy to green environment
kubectl apply -f deployment-green.yaml

# Wait for green to be ready
kubectl wait --for=condition=available deployment/ml-model-green

# Run smoke tests on green
python smoke_tests.py --endpoint http://green.ml.example.com

# Switch traffic to green
kubectl patch service ml-model-service \
  -p '{"spec":{"selector":{"version":"green"}}}'

# Monitor green for issues

# If successful, delete blue
kubectl delete deployment ml-model-blue

# If issues, rollback to blue
kubectl patch service ml-model-service \
  -p '{"spec":{"selector":{"version":"blue"}}}'
```

**Pros**:
- Instant rollback (switch service back)
- Full testing before production traffic
- Clean separation of versions

**Cons**:
- Requires double resources temporarily
- Database migrations can be complex
- Stateful applications are challenging

**Use When**: High-risk deployments, major model changes

### 9.3 Canary Deployment

**Gradually shift traffic** from old version to new version while monitoring.

```yaml
# Canary deployment with Istio
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: ml-model-canary
spec:
  hosts:
  - ml-model.example.com
  http:
  - match:
    - headers:
        user-type:
          exact: beta-tester
    route:
    - destination:
        host: ml-model-v2
        subset: canary
  - route:
    - destination:
        host: ml-model-v1
        subset: stable
      weight: 90
    - destination:
        host: ml-model-v2
        subset: canary
      weight: 10
```

**Canary Strategy Script**:

```python
# scripts/canary_deployment.py
import time
import requests
from prometheus_api_client import PrometheusConnect

def deploy_canary(
    old_version: str,
    new_version: str,
    stages: list = [10, 25, 50, 75, 100],
    monitor_duration: int = 300  # 5 minutes per stage
):
    """
    Gradually shift traffic to new version with monitoring.

    Args:
        old_version: Current stable version
        new_version: New canary version
        stages: Traffic percentage stages
        monitor_duration: Seconds to monitor each stage
    """
    prom = PrometheusConnect(url="http://prometheus:9090")

    for stage in stages:
        print(f"Shifting {stage}% traffic to {new_version}...")

        # Update traffic split
        update_traffic_split(old_version, new_version, stage)

        # Monitor for issues
        print(f"Monitoring for {monitor_duration}s...")
        time.sleep(monitor_duration)

        # Check metrics
        error_rate = get_error_rate(prom, new_version)
        latency_p99 = get_latency_p99(prom, new_version)
        model_accuracy = get_model_accuracy(new_version)

        print(f"Metrics - Error: {error_rate:.2%}, Latency: {latency_p99:.0f}ms, Accuracy: {model_accuracy:.3f}")

        # Decision: continue or rollback
        if error_rate > 0.01:  # >1% errors
            print(f"ERROR RATE TOO HIGH! Rolling back...")
            rollback(old_version)
            return False

        if latency_p99 > 500:  # >500ms
            print(f"LATENCY TOO HIGH! Rolling back...")
            rollback(old_version)
            return False

        if model_accuracy < 0.80:  # <80% accuracy
            print(f"MODEL ACCURACY TOO LOW! Rolling back...")
            rollback(old_version)
            return False

    print(f"Canary deployment successful! {new_version} is now stable.")
    return True

def update_traffic_split(old_version: str, new_version: str, new_percentage: int):
    """Update traffic split using kubectl or Istio."""
    # Implementation depends on your setup
    pass

def get_error_rate(prom: PrometheusConnect, version: str) -> float:
    """Get error rate from Prometheus."""
    query = f'rate(http_requests_total{{status=~"5..",version="{version}"}}[5m])'
    result = prom.custom_query(query)
    return float(result[0]['value'][1]) if result else 0.0

def rollback(old_version: str):
    """Rollback to old version."""
    update_traffic_split(old_version, "", 100)
```

**Pros**:
- Progressive rollout with safety
- Real production testing
- Easy rollback at any stage
- Minimal risk

**Cons**:
- Complex to implement
- Requires good monitoring
- Longer deployment time

**Use When**: New model architectures, major feature changes

### 9.4 A/B Testing Deployment

**Split traffic based on user attributes** for experimentation.

```python
# Routing logic for A/B testing
def route_prediction_request(user_id: str, features: dict):
    """Route request to model A or B based on user assignment."""

    # Deterministic assignment based on user_id
    import hashlib
    hash_value = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
    bucket = hash_value % 100

    # 50/50 split
    if bucket < 50:
        model_version = 'model-a'
    else:
        model_version = 'model-b'

    # Make prediction
    prediction = call_model(model_version, features)

    # Log for analysis
    log_prediction(user_id, model_version, prediction)

    return prediction
```

**Pros**:
- Statistical comparison of models
- User-based routing
- Gather production data for each variant

**Cons**:
- Requires experiment tracking
- Needs sufficient traffic for significance
- Complex analysis

**Use When**: Comparing model performance, optimizing for business metrics

### 9.5 Shadow Deployment

**New version receives copy of production traffic** but doesn't serve users.

```python
# Shadow deployment proxy
async def handle_request(request):
    """Send request to both production and shadow model."""

    # Always serve from production
    prod_response = await call_model('production', request)

    # Asynchronously send to shadow (don't wait)
    asyncio.create_task(shadow_prediction(request))

    return prod_response

async def shadow_prediction(request):
    """Make shadow prediction and log for comparison."""
    try:
        shadow_response = await call_model('shadow', request)

        # Log for later comparison
        log_shadow_result(
            request_id=request.id,
            prod_prediction=request.prod_prediction,
            shadow_prediction=shadow_response.prediction
        )

        # Compare predictions
        if shadow_response.prediction != request.prod_prediction:
            log_divergence(request.id, shadow_response, request)

    except Exception as e:
        log_shadow_error(request.id, str(e))
```

**Pros**:
- Zero risk to users
- Real production data testing
- Compare model predictions

**Cons**:
- Double infrastructure cost
- Complex to implement
- Doesn't test user impact

**Use When**: Testing risky changes, validating new models

---

## 10. Monitoring and Rollback

### 10.1 Deployment Monitoring

**Key Metrics to Monitor**:

1. **System Metrics**:
   - Pod status and health
   - CPU and memory usage
   - Request rate and latency
   - Error rate (4xx, 5xx)

2. **ML-Specific Metrics**:
   - Model prediction latency
   - Prediction distribution
   - Model accuracy (if ground truth available)
   - Feature distribution shifts

3. **Business Metrics**:
   - User engagement
   - Conversion rates
   - Revenue impact

**Monitoring Script**:

```python
# scripts/monitor_deployment.py
import time
import sys
from prometheus_api_client import PrometheusConnect
from datetime import datetime, timedelta

def monitor_deployment(
    service_name: str,
    duration_seconds: int = 300,
    error_threshold: float = 0.01,
    latency_threshold: float = 200.0,
    check_interval: int = 30
):
    """
    Monitor a deployment and alert on issues.

    Args:
        service_name: Name of the service to monitor
        duration_seconds: How long to monitor
        error_threshold: Maximum acceptable error rate (e.g., 0.01 = 1%)
        latency_threshold: Maximum acceptable p99 latency (ms)
        check_interval: Seconds between checks
    """
    prom = PrometheusConnect(url="http://prometheus:9090")

    end_time = datetime.now() + timedelta(seconds=duration_seconds)
    checks_passed = 0
    checks_failed = 0

    print(f"Monitoring {service_name} for {duration_seconds}s...")
    print(f"Error threshold: {error_threshold:.2%}")
    print(f"Latency threshold: {latency_threshold}ms")
    print("=" * 60)

    while datetime.now() < end_time:
        # Check error rate
        error_rate = get_error_rate(prom, service_name)

        # Check latency
        latency_p99 = get_latency_percentile(prom, service_name, 0.99)
        latency_p50 = get_latency_percentile(prom, service_name, 0.50)

        # Check request rate
        request_rate = get_request_rate(prom, service_name)

        # Print status
        print(f"[{datetime.now().strftime('%H:%M:%S')}] " +
              f"Errors: {error_rate:.3%} | " +
              f"Latency p99: {latency_p99:.0f}ms | " +
              f"Latency p50: {latency_p50:.0f}ms | " +
              f"RPS: {request_rate:.1f}")

        # Check thresholds
        if error_rate > error_threshold:
            print(f"❌ ERROR RATE EXCEEDED: {error_rate:.3%} > {error_threshold:.3%}")
            checks_failed += 1
        elif latency_p99 > latency_threshold:
            print(f"❌ LATENCY EXCEEDED: {latency_p99:.0f}ms > {latency_threshold}ms")
            checks_failed += 1
        else:
            checks_passed += 1

        # Fail fast if multiple consecutive failures
        if checks_failed >= 3:
            print("\n❌ DEPLOYMENT UNHEALTHY - 3 consecutive failures!")
            print("Recommend immediate rollback.")
            sys.exit(1)

        time.sleep(check_interval)

    # Final report
    print("\n" + "=" * 60)
    print(f"Monitoring complete!")
    print(f"Checks passed: {checks_passed}")
    print(f"Checks failed: {checks_failed}")

    if checks_failed == 0:
        print("✅ Deployment is healthy!")
        sys.exit(0)
    elif checks_failed < checks_passed:
        print("⚠️  Some issues detected but mostly healthy")
        sys.exit(0)
    else:
        print("❌ Deployment has significant issues!")
        sys.exit(1)

def get_error_rate(prom, service):
    """Calculate 5xx error rate over last 5 minutes."""
    query = f'sum(rate(http_requests_total{{service="{service}",status=~"5.."}}[5m])) / sum(rate(http_requests_total{{service="{service}"}}[5m]))'
    result = prom.custom_query(query)
    return float(result[0]['value'][1]) if result else 0.0

def get_latency_percentile(prom, service, percentile):
    """Get latency percentile."""
    query = f'histogram_quantile({percentile}, rate(http_request_duration_seconds_bucket{{service="{service}"}}[5m]))'
    result = prom.custom_query(query)
    return float(result[0]['value'][1]) * 1000 if result else 0.0  # Convert to ms

def get_request_rate(prom, service):
    """Get request rate (requests per second)."""
    query = f'sum(rate(http_requests_total{{service="{service}"}}[1m]))'
    result = prom.custom_query(query)
    return float(result[0]['value'][1]) if result else 0.0
```

### 10.2 Automated Rollback

**Rollback Triggers**:
1. Health check failures
2. Error rate exceeds threshold
3. Latency exceeds threshold
4. Model performance degrades
5. Manual trigger

**Rollback Workflow**:

```yaml
# .github/workflows/rollback.yml
name: Automated Rollback

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to rollback'
        required: true
        type: choice
        options:
          - staging
          - production
      target_version:
        description: 'Version to rollback to (leave empty for previous)'
        required: false
        type: string

jobs:
  rollback:
    name: Rollback Deployment
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG }}

      - name: Get current deployment
        id: current
        run: |
          CURRENT=$(kubectl get deployment ml-model-serving \
            -n ${{ inputs.environment }} \
            -o jsonpath='{.spec.template.spec.containers[0].image}')
          echo "current_image=$CURRENT" >> $GITHUB_OUTPUT

      - name: Determine rollback target
        id: target
        run: |
          if [ -n "${{ inputs.target_version }}" ]; then
            TARGET="${{ inputs.target_version }}"
          else
            # Get previous deployment from history
            TARGET=$(kubectl rollout history deployment/ml-model-serving \
              -n ${{ inputs.environment }} \
              --revision=0 \
              | tail -n 2 | head -n 1 | awk '{print $1}')
          fi
          echo "target=$TARGET" >> $GITHUB_OUTPUT

      - name: Confirm rollback
        run: |
          echo "Rolling back in ${{ inputs.environment }}"
          echo "From: ${{ steps.current.outputs.current_image }}"
          echo "To:   ${{ steps.target.outputs.target }}"

      - name: Execute rollback
        run: |
          if [ -n "${{ inputs.target_version }}" ]; then
            # Rollback to specific version
            kubectl set image deployment/ml-model-serving \
              model-server=${{ inputs.target_version }} \
              -n ${{ inputs.environment }}
          else
            # Rollback to previous revision
            kubectl rollout undo deployment/ml-model-serving \
              -n ${{ inputs.environment }}
          fi

      - name: Wait for rollback
        run: |
          kubectl rollout status deployment/ml-model-serving \
            -n ${{ inputs.environment }} \
            --timeout=5m

      - name: Verify rollback
        run: |
          python scripts/smoke_tests.py \
            --endpoint https://${{ inputs.environment }}-ml.example.com

      - name: Send notification
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: |
            Rollback ${{ job.status }} in ${{ inputs.environment }}
            From: ${{ steps.current.outputs.current_image }}
            To: ${{ steps.target.outputs.target }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
        if: always()
```

**Kubernetes Rollback Commands**:

```bash
# Rollback to previous revision
kubectl rollout undo deployment/ml-model-serving

# Rollback to specific revision
kubectl rollout undo deployment/ml-model-serving --to-revision=5

# View rollout history
kubectl rollout history deployment/ml-model-serving

# Pause rollout (emergency)
kubectl rollout pause deployment/ml-model-serving

# Resume rollout
kubectl rollout resume deployment/ml-model-serving

# Check rollout status
kubectl rollout status deployment/ml-model-serving
```

---

## 11. Best Practices and Common Pitfalls

### 11.1 CI/CD Best Practices for ML

**1. Version Everything**:
```python
# config.yaml
model:
  name: "classifier"
  version: "2.1.0"
  architecture: "transformer"
  git_commit: "abc123def"

data:
  train_dataset: "s3://bucket/train_v2.parquet"
  dataset_version: "2.0"
  schema_version: "1.5"

code:
  git_branch: "main"
  git_commit: "abc123def"
  requirements_hash: "sha256:xyz789"
```

**2. Make Builds Reproducible**:
```dockerfile
# Pin exact versions
FROM python:3.10.12-slim-bullseye

# Pin dependencies
COPY requirements.txt .
# requirements.txt:
# torch==2.0.1
# numpy==1.24.3
# pandas==2.0.2

# Set random seeds
ENV PYTHONHASHSEED=0

# Deterministic Python
RUN pip install --no-cache-dir -r requirements.txt
```

**3. Separate Configuration from Code**:
```python
# config/production.yaml
model_serving:
  host: "0.0.0.0"
  port: 8000
  workers: 4
  timeout: 30

model:
  path: "s3://models/prod/model.pkl"
  reload_interval: 3600

logging:
  level: "INFO"
  format: "json"

# Load via environment
import os
import yaml

env = os.getenv('ENV', 'development')
with open(f'config/{env}.yaml') as f:
    config = yaml.safe_load(f)
```

**4. Use Feature Flags for Gradual Rollout**:
```python
from flagsmith import Flagsmith

flagsmith = Flagsmith(environment_key=os.getenv('FLAGSMITH_KEY'))

def predict(features):
    """Make prediction with feature-flagged model selection."""

    # Check which model to use
    flags = flagsmith.get_identity_flags(identifier=user_id)

    if flags.is_feature_enabled("use_new_model"):
        model = load_model('new_model')
    else:
        model = load_model('old_model')

    return model.predict(features)
```

**5. Implement Comprehensive Logging**:
```python
import structlog

logger = structlog.get_logger()

def predict(request_id, features):
    logger.info(
        "prediction_request",
        request_id=request_id,
        model_version="v2.1.0",
        features=features
    )

    prediction = model.predict(features)

    logger.info(
        "prediction_response",
        request_id=request_id,
        prediction=prediction,
        latency_ms=elapsed_time * 1000
    )

    return prediction
```

### 11.2 Common Pitfalls and How to Avoid Them

**Pitfall 1: Forgetting to Version Data**

❌ **Bad**:
```python
# Load whatever data is there
df = pd.read_csv('data/train.csv')
```

✅ **Good**:
```python
# Version and validate data
DATA_VERSION = "v2.1.0"
data_path = f's3://bucket/train_{DATA_VERSION}.parquet'
df = pd.read_parquet(data_path)

# Validate schema
assert set(df.columns) == {'feature1', 'feature2', 'target'}
assert df['target'].isnull().sum() == 0
```

**Pitfall 2: Not Testing in Production-Like Environment**

❌ **Bad**:
```bash
# Test only on laptop
pytest tests/
# Deploy directly to production
```

✅ **Good**:
```bash
# Test in staging environment identical to production
# Deploy to staging
kubectl apply -f k8s/staging/
# Run integration tests against staging
pytest tests/integration --endpoint=https://staging.example.com
# If passed, deploy to production
```

**Pitfall 3: No Rollback Plan**

❌ **Bad**:
```bash
# Deploy and hope for the best
kubectl apply -f deployment.yaml
```

✅ **Good**:
```bash
# Deploy with rollback capability
kubectl apply -f deployment.yaml --record
# Monitor for issues
./monitor_deployment.sh
# Rollback if needed
kubectl rollout undo deployment/ml-model
```

**Pitfall 4: Ignoring Model Performance in Production**

❌ **Bad**:
```python
# Just serve predictions, no monitoring
def predict(features):
    return model.predict(features)
```

✅ **Good**:
```python
def predict(features):
    prediction = model.predict(features)

    # Log prediction for monitoring
    log_prediction(
        model_version=MODEL_VERSION,
        features=features,
        prediction=prediction,
        timestamp=datetime.now()
    )

    # Monitor prediction distribution
    PREDICTION_DISTRIBUTION.observe(prediction)

    return prediction

# Separate job to check for drift
def check_drift_daily():
    recent_predictions = get_recent_predictions()
    training_predictions = get_training_predictions()

    drift_score = calculate_drift(recent_predictions, training_predictions)

    if drift_score > DRIFT_THRESHOLD:
        alert("Model drift detected!", drift_score)
        trigger_retraining()
```

**Pitfall 5: Hardcoding Secrets**

❌ **Bad**:
```python
# Hardcoded credentials
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
mlflow.set_tracking_uri("http://mlflow.example.com")
```

✅ **Good**:
```python
# Use environment variables
import os

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
if not AWS_ACCESS_KEY:
    raise ValueError("AWS_ACCESS_KEY not set")

MLFLOW_URI = os.getenv('MLFLOW_TRACKING_URI')
mlflow.set_tracking_uri(MLFLOW_URI)
```

**Pitfall 6: Not Setting Resource Limits**

❌ **Bad**:
```yaml
# No resource limits
containers:
- name: ml-model
  image: model:latest
  # No resources specified
```

✅ **Good**:
```yaml
containers:
- name: ml-model
  image: model:latest
  resources:
    requests:
      memory: "1Gi"
      cpu: "500m"
    limits:
      memory: "2Gi"
      cpu: "1000m"
```

---

## 12. Summary and Key Takeaways

### 12.1 Core Concepts Review

**CI/CD for ML includes**:
1. **Version Control** - Git for code, DVC/MLflow for data/models
2. **Continuous Integration** - Automated testing and validation
3. **Continuous Deployment** - Automated deployment to staging/production
4. **Testing** - Unit, integration, data, and model validation tests
5. **Containerization** - Docker for consistent environments
6. **Orchestration** - Kubernetes for deployment management
7. **Monitoring** - Track performance, errors, and model drift
8. **Rollback** - Quick recovery from failed deployments

**ML-Specific Considerations**:
- **Data versioning** is as important as code versioning
- **Model validation** goes beyond code testing
- **A/B testing** for comparing model performance
- **Feature flags** for gradual rollouts
- **Drift detection** for model monitoring
- **Retraining pipelines** for continuous improvement

### 12.2 Recommended Toolchain

**Essential Tools**:
- **Git** - Version control
- **GitHub Actions** - CI/CD orchestration
- **Docker** - Containerization
- **Kubernetes** - Container orchestration
- **MLflow** - Experiment tracking and model registry
- **Prometheus + Grafana** - Monitoring
- **pytest** - Testing framework
- **Great Expectations** - Data validation

**Nice-to-Have Tools**:
- **ArgoCD** - GitOps deployment
- **Istio** - Service mesh for canary deployments
- **DVC** - Data version control
- **Weights & Biases** - Experiment tracking alternative
- **Evidently** - ML monitoring and drift detection

### 12.3 Implementation Roadmap

**Phase 1: Basic CI** (Week 1-2)
- [ ] Set up Git repository with proper .gitignore
- [ ] Create comprehensive README
- [ ] Set up GitHub Actions for linting and testing
- [ ] Write unit tests for core functions
- [ ] Set up code coverage reporting

**Phase 2: Docker & Testing** (Week 3-4)
- [ ] Create Dockerfiles for training and serving
- [ ] Set up docker-compose for local development
- [ ] Add integration tests
- [ ] Add data validation tests
- [ ] Add model validation tests

**Phase 3: CD to Staging** (Week 5-6)
- [ ] Set up Kubernetes cluster (staging)
- [ ] Create K8s manifests (deployment, service, etc.)
- [ ] Automate deployment to staging
- [ ] Add smoke tests
- [ ] Set up monitoring (Prometheus/Grafana)

**Phase 4: Production Deployment** (Week 7-8)
- [ ] Set up production Kubernetes cluster
- [ ] Implement blue-green or canary deployment
- [ ] Add production monitoring
- [ ] Create rollback procedures
- [ ] Document runbooks for incidents

**Phase 5: Advanced Features** (Week 9-10)
- [ ] Implement A/B testing framework
- [ ] Add drift detection
- [ ] Automate retraining pipeline
- [ ] Set up alerts and notifications
- [ ] Optimize for cost and performance

### 12.4 Key Metrics to Track

**CI Metrics**:
- Build time (target: < 10 minutes)
- Test pass rate (target: > 95%)
- Code coverage (target: > 80%)
- Time to detect failures (target: < 5 minutes)

**CD Metrics**:
- Deployment frequency (target: multiple per day)
- Lead time for changes (target: < 1 hour)
- Mean time to recovery (MTTR) (target: < 30 minutes)
- Change failure rate (target: < 5%)

**ML Metrics**:
- Model accuracy/performance
- Prediction latency (target: < 100ms)
- Error rate (target: < 1%)
- Model drift score
- Data quality score

### 12.5 Final Checklist

Before considering your CI/CD pipeline complete:

**Code**:
- [ ] All code is version controlled
- [ ] Commit messages are descriptive
- [ ] Branch strategy is defined and followed
- [ ] Code reviews are mandatory

**Testing**:
- [ ] Unit tests cover core logic
- [ ] Integration tests cover workflows
- [ ] Data validation tests exist
- [ ] Model validation tests exist
- [ ] All tests run in CI

**Deployment**:
- [ ] Deployments are automated
- [ ] Staging environment exists
- [ ] Production deployment requires approval
- [ ] Rollback procedures are documented
- [ ] Runbooks exist for common issues

**Monitoring**:
- [ ] System metrics are tracked
- [ ] Model performance is monitored
- [ ] Alerts are configured
- [ ] Dashboards are set up
- [ ] On-call rotation is established

**Documentation**:
- [ ] README is comprehensive
- [ ] Architecture is documented
- [ ] Deployment process is documented
- [ ] Troubleshooting guide exists
- [ ] API documentation is up-to-date

---

## Additional Resources

**Books**:
- "Continuous Delivery" by Jez Humble and David Farley
- "The DevOps Handbook" by Gene Kim et al.
- "Building Machine Learning Powered Applications" by Emmanuel Ameisen
- "Machine Learning Engineering" by Andriy Burkov

**Online Resources**:
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Great Expectations Documentation](https://docs.greatexpectations.io/)

**Articles & Blogs**:
- [Rules of Machine Learning by Google](https://developers.google.com/machine-learning/guides/rules-of-ml)
- [Hidden Technical Debt in ML Systems](https://papers.nips.cc/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf)
- [Netflix Tech Blog - Data Science](https://netflixtechblog.com/tagged/data-science)
- [Uber Engineering Blog - ML Platform](https://eng.uber.com/tag/machine-learning/)

**Courses**:
- [MLOps Specialization (Coursera)](https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops)
- [Full Stack Deep Learning](https://fullstackdeeplearning.com/)
- [Made With ML - MLOps](https://madewithml.com/)

---

**Module Complete!** You should now have a comprehensive understanding of CI/CD foundations for MLOps. Practice the exercises to solidify these concepts.
