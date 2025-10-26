# Module 01: CI/CD Foundations for MLOps - Exercises

## Overview

This exercise set provides hands-on practice with CI/CD concepts for MLOps, including:
- Git workflows and branch strategies
- GitHub Actions automation
- Docker containerization for ML
- Code quality and testing
- CI/CD pipeline design

**Time Estimate**: 6-8 hours total

---

## Exercise 1: Git Workflow Implementation (60 minutes)

**Objective**: Implement a complete Git workflow with feature branches, pull requests, and merge strategies.

### Background

Your team is developing an ML model training service. You need to establish a Git workflow that supports:
- Feature development in isolation
- Code review before merging
- Protection of the main branch
- Clear commit history

### Tasks

1. **Create a repository structure**:
   ```bash
   ml-training-service/
   ├── src/
   │   ├── data/
   │   ├── models/
   │   └── utils/
   ├── tests/
   ├── .github/
   │   └── workflows/
   └── README.md
   ```

2. **Implement feature branch workflow**:
   - Create a new feature branch for adding a data preprocessing module
   - Add the preprocessing code
   - Create a pull request with a descriptive template
   - Simulate code review with comments
   - Merge using squash merge strategy

3. **Set up branch protection rules** (document what you would configure):
   - Require pull request reviews
   - Require status checks to pass
   - Enforce linear history
   - Require branches to be up to date

4. **Handle merge conflicts**:
   - Create two branches that modify the same file
   - Attempt to merge and resolve conflicts
   - Document the resolution strategy

### Starter Code

```python
# src/data/preprocessor.py
"""Data preprocessing module for ML training pipeline."""

import pandas as pd
import numpy as np
from typing import Tuple, List
from sklearn.preprocessing import StandardScaler

class DataPreprocessor:
    """Handles data preprocessing for ML models."""

    def __init__(self, scaling_strategy: str = 'standard'):
        """
        Initialize the preprocessor.

        Args:
            scaling_strategy: Type of scaling ('standard', 'minmax', 'robust')
        """
        # TODO: Initialize the scaler based on strategy
        pass

    def fit_transform(self, X: pd.DataFrame, y: pd.Series = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fit the preprocessor and transform the data.

        Args:
            X: Feature dataframe
            y: Target series (optional)

        Returns:
            Tuple of transformed features and target
        """
        # TODO: Implement fit_transform logic
        # - Handle missing values
        # - Encode categorical variables
        # - Scale numerical features
        # - Handle outliers
        pass

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """
        Transform new data using fitted preprocessor.

        Args:
            X: Feature dataframe

        Returns:
            Transformed features
        """
        # TODO: Implement transform logic
        pass
```

### Validation Tests

```python
# tests/test_preprocessor.py
import pytest
import pandas as pd
import numpy as np
from src.data.preprocessor import DataPreprocessor

def test_preprocessor_initialization():
    """Test that preprocessor initializes correctly."""
    preprocessor = DataPreprocessor(scaling_strategy='standard')
    assert preprocessor is not None
    # TODO: Add more assertions

def test_fit_transform_handles_missing_values():
    """Test that fit_transform handles missing values."""
    # TODO: Create test data with missing values
    # TODO: Run fit_transform
    # TODO: Assert no NaN values in output
    pass

def test_transform_without_fit_raises_error():
    """Test that transform before fit raises appropriate error."""
    # TODO: Implement test
    pass

# Run with: pytest tests/test_preprocessor.py -v
```

### Success Criteria

- [ ] Feature branch created with descriptive name
- [ ] Code follows PEP 8 standards
- [ ] All tests pass
- [ ] Pull request includes description and testing notes
- [ ] Merge conflict resolved correctly
- [ ] Commit history is clean and meaningful

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Branch naming**: Use format `feature/data-preprocessing` or `feat/preprocessing-module`
2. **Missing values**: Use `SimpleImputer` from sklearn or `fillna()` with strategy-based logic
3. **Categorical encoding**: Use `OneHotEncoder` or `LabelEncoder` depending on cardinality
4. **Merge conflicts**: Use `git mergetool` or manual resolution, always test after resolving
5. **PR template**: Include sections for description, changes, testing, and checklist

</details>

---

## Exercise 2: GitHub Actions CI Pipeline (90 minutes)

**Objective**: Build a comprehensive CI pipeline that runs on every pull request.

### Background

You need to create a GitHub Actions workflow that:
- Runs on pull requests to main branch
- Tests code on multiple Python versions
- Checks code quality
- Runs security scans
- Posts results as PR comments

### Tasks

1. **Create workflow file**: `.github/workflows/ci.yml`
2. **Implement multi-version testing**: Test on Python 3.9, 3.10, 3.11
3. **Add code quality checks**:
   - Linting with `flake8`
   - Type checking with `mypy`
   - Security scanning with `bandit`
4. **Add test coverage reporting**
5. **Cache dependencies** for faster runs
6. **Add status badge** to README

### Starter Code

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  pull_request:
    branches: [ main, develop ]
  push:
    branches: [ main ]

jobs:
  # TODO: Implement test job
  test:
    name: Test on Python ${{ matrix.python-version }}
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, '3.10', 3.11]

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      # TODO: Add steps for:
      # - Setting up Python
      # - Caching pip dependencies
      # - Installing dependencies
      # - Running pytest with coverage
      # - Uploading coverage reports

  # TODO: Implement code-quality job
  code-quality:
    name: Code Quality Checks
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      # TODO: Add steps for:
      # - Linting with flake8
      # - Type checking with mypy
      # - Security scan with bandit
      # - Formatting check with black

  # TODO: Implement security job
  security:
    name: Security Scan
    runs-on: ubuntu-latest

    steps:
      # TODO: Add steps for:
      # - Dependency vulnerability scanning
      # - Secret detection
      # - SAST scanning
```

### Configuration Files

```ini
# .flake8
[flake8]
max-line-length = 100
exclude = .git,__pycache__,venv,build,dist
ignore = E203,W503
per-file-ignores = __init__.py:F401

# TODO: Add more configuration
```

```ini
# mypy.ini
[mypy]
python_version = 3.10
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True

# TODO: Add module-specific configuration
```

```yaml
# .bandit
exclude_dirs:
  - /tests/
  - /venv/

# TODO: Configure security checks
```

### Validation

Test your workflow by:
1. Creating a PR with intentional code quality issues
2. Verifying that the workflow fails appropriately
3. Fixing issues and confirming the workflow passes
4. Checking that coverage reports are generated

### Success Criteria

- [ ] Workflow runs on PR creation
- [ ] Tests execute on multiple Python versions
- [ ] Code quality checks catch common issues
- [ ] Security scans detect vulnerabilities
- [ ] Coverage report is generated and accessible
- [ ] Workflow completes in under 5 minutes
- [ ] Status badge appears in README

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Caching**: Use `actions/cache@v3` with key based on `requirements.txt` hash
2. **Coverage**: Use `pytest-cov` and upload to Codecov or Coveralls
3. **Parallel jobs**: Use `needs: []` to run jobs in parallel
4. **Status badge**: Format is `![CI](https://github.com/USER/REPO/workflows/CI%20Pipeline/badge.svg)`
5. **Secrets**: Use GitHub Secrets for API tokens, never hardcode

</details>

---

## Exercise 3: Docker Containerization for ML (90 minutes)

**Objective**: Create optimized Docker images for ML model training and serving.

### Background

You need to containerize an ML training pipeline with:
- Efficient layer caching
- Multi-stage builds for smaller images
- GPU support (optional)
- Proper dependency management

### Tasks

1. **Create training Dockerfile**:
   - Use appropriate base image
   - Install dependencies efficiently
   - Set up training environment
   - Optimize for layer caching

2. **Create serving Dockerfile**:
   - Use slim base image
   - Copy only necessary artifacts
   - Expose API endpoint
   - Health check endpoint

3. **Implement docker-compose**:
   - Training service
   - Model registry (MLflow)
   - Database (PostgreSQL)
   - Network configuration

4. **Add .dockerignore** for efficient builds

### Starter Code

```dockerfile
# Dockerfile.train
# TODO: Choose appropriate base image
FROM python:3.10-slim AS base

# TODO: Set working directory
WORKDIR /app

# TODO: Install system dependencies
# Consider: build-essential, git, etc.

# TODO: Copy and install Python dependencies
# Use layer caching effectively

# TODO: Copy application code

# TODO: Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MODEL_DIR=/models

# TODO: Create volume mount points

# TODO: Set entrypoint
CMD ["python", "src/train.py"]
```

```dockerfile
# Dockerfile.serve
# Multi-stage build for smaller final image
FROM python:3.10-slim AS builder

# TODO: Install build dependencies and create wheel

FROM python:3.10-slim AS runtime

# TODO: Copy only runtime dependencies and artifacts
# TODO: Set up FastAPI serving
# TODO: Add health check

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# TODO: Expose port and set command
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  # TODO: Define training service
  training:
    build:
      context: .
      dockerfile: Dockerfile.train
    # TODO: Add volumes, environment, networks

  # TODO: Define serving service
  serving:
    build:
      context: .
      dockerfile: Dockerfile.serve
    # TODO: Configure ports, health checks, dependencies

  # TODO: Define MLflow service
  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.9.2
    # TODO: Configure tracking server

  # TODO: Define PostgreSQL service
  postgres:
    image: postgres:15-alpine
    # TODO: Configure database

# TODO: Define networks and volumes
```

```
# .dockerignore
__pycache__/
*.pyc
*.pyo
*.pyd
.git/
.gitignore
*.md
tests/
.pytest_cache/
.coverage
htmlcov/
venv/
.env

# TODO: Add more patterns
```

### Training Script

```python
# src/train.py
"""Model training script for containerized execution."""

import os
import mlflow
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier

def train_model():
    """Train and log model to MLflow."""

    # TODO: Set MLflow tracking URI from environment
    tracking_uri = os.getenv('MLFLOW_TRACKING_URI', 'http://mlflow:5000')

    # TODO: Load data from volume mount
    data_path = Path(os.getenv('DATA_PATH', '/data'))

    # TODO: Start MLflow run
    with mlflow.start_run():
        # TODO: Train model
        # TODO: Log parameters, metrics, and model
        # TODO: Register model
        pass

if __name__ == '__main__':
    train_model()
```

### Validation

Build and test your containers:
```bash
# Build images
docker build -f Dockerfile.train -t ml-training:latest .
docker build -f Dockerfile.serve -t ml-serving:latest .

# Test training container
docker run --rm -v $(pwd)/data:/data ml-training:latest

# Test serving container
docker run --rm -p 8000:8000 ml-serving:latest

# Run full stack
docker-compose up -d
```

### Success Criteria

- [ ] Training image builds successfully
- [ ] Serving image is under 500MB
- [ ] Layer caching works (rebuild is fast)
- [ ] Containers can communicate via docker-compose
- [ ] Health checks work correctly
- [ ] Volumes persist data correctly
- [ ] Environment variables configure services

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Base images**: Use `python:3.10-slim` for smaller size, `nvidia/cuda` for GPU
2. **Layer caching**: Copy `requirements.txt` first, then install, then copy code
3. **Multi-stage**: Build in one stage, copy artifacts to slim runtime stage
4. **MLflow**: Use official image, mount volume for artifact store
5. **Networks**: Create custom network for service discovery
6. **Secrets**: Use Docker secrets or environment files, never bake into image

</details>

---

## Exercise 4: Automated Testing Strategy (75 minutes)

**Objective**: Implement a comprehensive testing strategy for ML code.

### Background

ML code requires different types of testing:
- Unit tests for data processing logic
- Integration tests for pipeline components
- Model validation tests
- Data quality tests

### Tasks

1. **Unit tests**: Test preprocessing functions
2. **Integration tests**: Test full training pipeline
3. **Model tests**: Test model performance and behavior
4. **Data tests**: Test data quality and schema
5. **Configure pytest**: Setup fixtures, markers, and plugins

### Starter Code

```python
# tests/conftest.py
"""Pytest configuration and shared fixtures."""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path

@pytest.fixture
def sample_data():
    """Generate sample dataset for testing."""
    np.random.seed(42)
    n_samples = 1000

    data = {
        'feature_1': np.random.normal(0, 1, n_samples),
        'feature_2': np.random.exponential(2, n_samples),
        'feature_3': np.random.choice(['A', 'B', 'C'], n_samples),
        'target': np.random.binomial(1, 0.3, n_samples)
    }

    return pd.DataFrame(data)

# TODO: Add more fixtures
# - trained_model fixture
# - mock_mlflow_client fixture
# - temporary_directory fixture
# - database_connection fixture
```

```python
# tests/unit/test_preprocessor.py
"""Unit tests for data preprocessing."""

import pytest
import numpy as np
from src.data.preprocessor import DataPreprocessor

class TestDataPreprocessor:
    """Test suite for DataPreprocessor class."""

    def test_handles_missing_values(self, sample_data):
        """Test that missing values are handled correctly."""
        # TODO: Add NaN values to sample_data
        # TODO: Fit and transform
        # TODO: Assert no NaN in output
        pass

    def test_scales_features_correctly(self, sample_data):
        """Test that feature scaling is applied correctly."""
        # TODO: Fit and transform
        # TODO: Check that mean ≈ 0 and std ≈ 1
        pass

    def test_categorical_encoding(self, sample_data):
        """Test categorical variable encoding."""
        # TODO: Test one-hot encoding
        # TODO: Verify correct number of columns
        pass

    @pytest.mark.parametrize('strategy', ['standard', 'minmax', 'robust'])
    def test_different_scaling_strategies(self, sample_data, strategy):
        """Test different scaling strategies."""
        # TODO: Test each strategy
        pass

    def test_transform_without_fit_raises_error(self):
        """Test that transform before fit raises appropriate error."""
        preprocessor = DataPreprocessor()
        with pytest.raises(Exception):  # TODO: Specify exact exception
            preprocessor.transform(sample_data)
```

```python
# tests/integration/test_training_pipeline.py
"""Integration tests for ML training pipeline."""

import pytest
import mlflow
from src.train import train_model

@pytest.mark.integration
class TestTrainingPipeline:
    """Test suite for end-to-end training pipeline."""

    def test_full_training_pipeline(self, sample_data, tmp_path):
        """Test complete training pipeline execution."""
        # TODO: Set up MLflow tracking
        # TODO: Run training
        # TODO: Verify model is logged
        # TODO: Check metrics are within expected ranges
        pass

    def test_pipeline_handles_data_errors(self):
        """Test pipeline error handling for bad data."""
        # TODO: Test with malformed data
        # TODO: Verify appropriate errors are raised
        pass

    def test_model_registry_integration(self):
        """Test model registration in MLflow."""
        # TODO: Train model
        # TODO: Register model
        # TODO: Verify model appears in registry
        pass
```

```python
# tests/model/test_model_validation.py
"""Model validation and performance tests."""

import pytest
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score

@pytest.mark.model
class TestModelValidation:
    """Test suite for model validation."""

    def test_model_meets_performance_thresholds(self, trained_model, test_data):
        """Test that model meets minimum performance requirements."""
        # TODO: Make predictions
        # TODO: Calculate metrics
        # TODO: Assert metrics > thresholds
        # Example: assert accuracy > 0.85
        pass

    def test_model_predictions_are_valid(self, trained_model, test_data):
        """Test that model outputs are valid."""
        # TODO: Get predictions
        # TODO: Check predictions are in valid range
        # TODO: Check prediction probabilities sum to 1
        pass

    def test_model_is_deterministic(self, trained_model, test_data):
        """Test that model produces consistent predictions."""
        # TODO: Run predictions twice
        # TODO: Assert predictions are identical
        pass

    def test_model_inference_latency(self, trained_model, test_data):
        """Test that model inference is fast enough."""
        import time

        # TODO: Time predictions
        # TODO: Assert latency < threshold (e.g., 100ms)
        pass
```

```python
# tests/data/test_data_quality.py
"""Data quality and schema validation tests."""

import pytest
import pandas as pd
from great_expectations.dataset import PandasDataset

@pytest.mark.data
class TestDataQuality:
    """Test suite for data quality checks."""

    def test_data_schema_validation(self, sample_data):
        """Test that data conforms to expected schema."""
        # TODO: Define expected schema
        # TODO: Validate column names and types
        pass

    def test_no_duplicate_records(self, sample_data):
        """Test that data has no unexpected duplicates."""
        # TODO: Check for duplicates
        assert sample_data.duplicated().sum() == 0

    def test_value_ranges(self, sample_data):
        """Test that values are within expected ranges."""
        # TODO: Use Great Expectations
        # ge_df = PandasDataset(sample_data)
        # TODO: Add expectations for value ranges
        pass

    def test_no_data_leakage(self, train_data, test_data):
        """Test that train and test sets don't overlap."""
        # TODO: Check for overlap
        pass
```

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

markers =
    unit: Unit tests
    integration: Integration tests
    model: Model validation tests
    data: Data quality tests
    slow: Slow running tests

addopts =
    -v
    --strict-markers
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80

# TODO: Add more pytest configuration
```

### Validation

Run your tests:
```bash
# Run all tests
pytest

# Run specific test types
pytest -m unit
pytest -m integration
pytest -m "not slow"

# Run with coverage
pytest --cov=src --cov-report=html

# Run in parallel
pytest -n auto
```

### Success Criteria

- [ ] All test types are implemented
- [ ] Test coverage > 80%
- [ ] Tests are fast (< 30 seconds total)
- [ ] Tests are deterministic and reliable
- [ ] Fixtures are reusable and well-organized
- [ ] Parametrized tests cover multiple scenarios
- [ ] Integration tests verify end-to-end workflow

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Fixtures**: Use `scope='session'` for expensive setup, `scope='function'` for isolation
2. **Mocking**: Use `pytest-mock` or `unittest.mock` for external dependencies
3. **Parametrize**: Use `@pytest.mark.parametrize` to test multiple inputs efficiently
4. **Coverage**: Aim for 80%+ but focus on critical paths, not 100%
5. **Speed**: Use `pytest-xdist` for parallel execution
6. **Data**: Use `faker` or `hypothesis` for property-based testing

</details>

---

## Exercise 5: Complete CI/CD Pipeline Design (90 minutes)

**Objective**: Design and implement a production-ready CI/CD pipeline for an ML project.

### Background

Design a complete pipeline that:
- Builds and tests code on every commit
- Trains and validates models on schedule
- Deploys models to staging and production
- Monitors deployed models
- Supports rollback

### Tasks

1. **Design pipeline architecture** (document with diagram)
2. **Implement CI pipeline** (test, build, scan)
3. **Implement CD pipeline** (deploy to staging, test, promote to prod)
4. **Add model training pipeline** (scheduled retraining)
5. **Implement monitoring and alerting**

### Starter Code

```yaml
# .github/workflows/ci-cd-complete.yml
name: Complete CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    # Run model training weekly
    - cron: '0 2 * * 0'  # Sunday 2 AM UTC

env:
  PYTHON_VERSION: '3.10'
  DOCKER_REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # CI: Test and Build
  test:
    name: Test & Quality Checks
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      # TODO: Add test steps
      # - Install dependencies
      # - Run unit tests
      # - Run integration tests
      # - Upload coverage

  build:
    name: Build Docker Images
    needs: test
    runs-on: ubuntu-latest

    steps:
      # TODO: Build and push Docker images
      # - Build training image
      # - Build serving image
      # - Tag with git SHA and latest
      # - Push to registry
      pass

  # CD: Deploy to Staging
  deploy-staging:
    name: Deploy to Staging
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: staging
      url: https://staging.example.com

    steps:
      # TODO: Deploy to staging environment
      # - Update Kubernetes manifests
      # - Apply deployment
      # - Wait for rollout
      # - Run smoke tests
      pass

  # Model Training (scheduled)
  train-model:
    name: Train Model
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest

    steps:
      # TODO: Run model training
      # - Fetch latest data
      # - Train model
      # - Validate performance
      # - Log to MLflow
      # - Compare with production model
      pass

  # CD: Deploy to Production
  deploy-production:
    name: Deploy to Production
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://api.example.com

    steps:
      # TODO: Deploy to production
      # - Require manual approval
      # - Blue-green or canary deployment
      # - Monitor metrics
      # - Auto-rollback on errors
      pass
```

```yaml
# .github/workflows/rollback.yml
name: Rollback Deployment

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
      version:
        description: 'Version to rollback to (git SHA or tag)'
        required: true
        type: string

jobs:
  rollback:
    name: Rollback to ${{ inputs.version }}
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}

    steps:
      # TODO: Implement rollback logic
      # - Validate version exists
      # - Update deployment
      # - Verify rollback success
      # - Notify team
      pass
```

```python
# scripts/deploy.py
"""Deployment automation script."""

import os
import subprocess
import time
from typing import Dict

def deploy_to_kubernetes(
    namespace: str,
    image_tag: str,
    replicas: int = 3,
    deployment_strategy: str = 'rolling'
) -> bool:
    """
    Deploy ML model to Kubernetes.

    Args:
        namespace: K8s namespace
        image_tag: Docker image tag
        replicas: Number of replicas
        deployment_strategy: 'rolling', 'blue-green', or 'canary'

    Returns:
        True if deployment successful
    """
    # TODO: Implement deployment logic
    # - Update deployment manifest
    # - Apply to cluster
    # - Wait for rollout
    # - Run health checks
    # - Monitor metrics
    pass

def run_smoke_tests(endpoint: str) -> bool:
    """
    Run smoke tests against deployed endpoint.

    Args:
        endpoint: API endpoint URL

    Returns:
        True if all tests pass
    """
    # TODO: Implement smoke tests
    # - Test health endpoint
    # - Test prediction endpoint
    # - Verify response format
    # - Check latency
    pass

def rollback_deployment(namespace: str, revision: int = None) -> bool:
    """
    Rollback Kubernetes deployment.

    Args:
        namespace: K8s namespace
        revision: Revision number (default: previous)

    Returns:
        True if rollback successful
    """
    # TODO: Implement rollback
    pass

if __name__ == '__main__':
    # TODO: Parse CLI arguments
    # TODO: Execute deployment
    pass
```

```python
# scripts/model_training.py
"""Automated model training and validation."""

import mlflow
from sklearn.metrics import accuracy_score, f1_score
from typing import Dict

def train_and_validate_model() -> Dict:
    """
    Train model and validate performance.

    Returns:
        Dict with training results and metrics
    """
    # TODO: Implement training pipeline
    # - Load latest data
    # - Preprocess
    # - Train model
    # - Validate on holdout set
    # - Log to MLflow
    pass

def compare_with_production(new_metrics: Dict, threshold: float = 0.02) -> bool:
    """
    Compare new model with production model.

    Args:
        new_metrics: Metrics from new model
        threshold: Minimum improvement required

    Returns:
        True if new model is better
    """
    # TODO: Fetch production model metrics
    # TODO: Compare metrics
    # TODO: Return decision
    pass

def promote_model_to_production(model_uri: str, model_name: str):
    """
    Promote model to production in MLflow registry.

    Args:
        model_uri: URI of model to promote
        model_name: Name in model registry
    """
    # TODO: Transition model to production stage
    # TODO: Archive old production model
    pass
```

### Architecture Diagram Template

```
┌─────────────────────────────────────────────────────────────┐
│                      CI/CD Pipeline                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐            │
│  │   Code   │───▶│  Build   │───▶│  Deploy  │            │
│  │  Commit  │    │  & Test  │    │  Staging │            │
│  └──────────┘    └──────────┘    └──────────┘            │
│                        │               │                   │
│                        ▼               ▼                   │
│                  ┌──────────┐    ┌──────────┐            │
│                  │ Security │    │  Smoke   │            │
│                  │   Scan   │    │  Tests   │            │
│                  └──────────┘    └──────────┘            │
│                                       │                   │
│                                       ▼                   │
│                                 ┌──────────┐             │
│                                 │  Deploy  │             │
│                                 │   Prod   │             │
│                                 └──────────┘             │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │         Model Training (Scheduled)               │   │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐ │   │
│  │  │ Fetch  │─▶│ Train  │─▶│Validate│─▶│Promote │ │   │
│  │  │  Data  │  │ Model  │  │ Model  │  │to Prod │ │   │
│  │  └────────┘  └────────┘  └────────┘  └────────┘ │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
└─────────────────────────────────────────────────────────┘

TODO: Enhance this diagram with your specific implementation
```

### Validation Checklist

Test your complete pipeline:
- [ ] CI runs on every PR
- [ ] Images are built and tagged correctly
- [ ] Deployment to staging is automatic
- [ ] Smoke tests catch deployment issues
- [ ] Production deployment requires approval
- [ ] Scheduled training runs successfully
- [ ] Model comparison works correctly
- [ ] Rollback can be triggered manually
- [ ] Notifications are sent on failures

### Success Criteria

- [ ] Complete pipeline diagram created
- [ ] All workflow files are valid YAML
- [ ] CI completes in under 10 minutes
- [ ] Deployment includes health checks
- [ ] Rollback is tested and works
- [ ] Model training is automated
- [ ] Metrics are logged for every deployment
- [ ] Pipeline handles errors gracefully

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Environments**: Use GitHub Environments for staging/prod with protection rules
2. **Secrets**: Store credentials in GitHub Secrets, reference as `${{ secrets.NAME }}`
3. **Approval**: Use `environment.protection_rules.reviewers` for manual approval
4. **Monitoring**: Integrate with Prometheus/Grafana, alert on metric degradation
5. **Blue-Green**: Maintain two identical environments, switch traffic after validation
6. **Canary**: Gradually shift traffic (10%, 50%, 100%) while monitoring
7. **Rollback**: Use `kubectl rollout undo` or deploy previous image tag

</details>

---

## Bonus Challenges

### Challenge 1: Multi-Environment Matrix Testing

Implement matrix testing across:
- Python versions: 3.9, 3.10, 3.11
- Operating systems: Ubuntu, macOS, Windows
- Dependencies: minimum, latest

### Challenge 2: Semantic Versioning Automation

Implement automatic version bumping based on:
- Commit message conventions (feat, fix, BREAKING CHANGE)
- Automatic changelog generation
- Git tag creation

### Challenge 3: Cost Optimization

Optimize CI/CD costs by:
- Caching dependencies effectively
- Running expensive tests only on main branch
- Using self-hosted runners for training
- Implementing smart test selection

---

## Additional Resources

- **Git**: [Pro Git Book](https://git-scm.com/book/en/v2)
- **GitHub Actions**: [Official Documentation](https://docs.github.com/en/actions)
- **Docker**: [Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- **Testing**: [pytest Documentation](https://docs.pytest.org/)
- **CI/CD**: [Continuous Delivery Book](https://continuousdelivery.com/)

---

## Submission Guidelines

For each exercise, submit:
1. **Code**: All implementation files
2. **Tests**: Passing test suite
3. **Documentation**: README explaining your approach
4. **Artifacts**: Screenshots of successful pipeline runs
5. **Reflection**: What you learned and challenges faced

**Estimated Total Time**: 6-8 hours
**Difficulty**: Intermediate

Good luck! 🚀
