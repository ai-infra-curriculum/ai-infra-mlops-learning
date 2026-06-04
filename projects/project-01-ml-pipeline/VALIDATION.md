# Validation & Testing Strategy

## 1. Overview

This document outlines the comprehensive testing and validation strategy for the End-to-End ML Pipeline project. It covers all aspects from unit tests to production validation.

## 2. Testing Pyramid

```
                    ▲
                   ╱ ╲
                  ╱   ╲
                 ╱ E2E ╲
                ╱───────╲
               ╱         ╲
              ╱Integration╲
             ╱─────────────╲
            ╱               ╲
           ╱   Unit Tests    ╲
          ╱───────────────────╲
         ╱                     ╲
        ╱     Static Analysis   ╲
       ╱───────────────────────────╲

Levels (bottom to top):
1. Static Analysis: Linting, type checking, security scanning
2. Unit Tests: Individual component testing (70% of tests)
3. Integration Tests: Component interaction testing (20% of tests)
4. E2E Tests: Full workflow testing (10% of tests)
```

## 3. Testing Standards

### 3.1 Coverage Requirements

| Component | Unit Test Coverage | Integration Coverage |
|-----------|-------------------|---------------------|
| Data Ingestion | ≥ 85% | ≥ 70% |
| Data Validation | ≥ 90% | ≥ 80% |
| Feature Engineering | ≥ 85% | ≥ 75% |
| Model Training | ≥ 80% | ≥ 70% |
| Model Serving | ≥ 90% | ≥ 85% |
| Monitoring | ≥ 85% | ≥ 70% |
| **Overall** | **≥ 80%** | **≥ 70%** |

### 3.2 Test Quality Criteria

All tests must:
- [ ] Have descriptive names that explain what is being tested
- [ ] Be independent (no dependencies between tests)
- [ ] Be deterministic (same result every time)
- [ ] Be fast (unit tests < 1s, integration tests < 10s)
- [ ] Clean up after themselves (no side effects)
- [ ] Use appropriate assertions
- [ ] Include both positive and negative cases
- [ ] Handle edge cases

## 4. Unit Testing

### 4.1 Data Ingestion Tests

**File**: `tests/unit/test_data_ingestion.py`

```python
class TestCSVConnector:
    """Test CSV data ingestion."""

    def test_read_csv_file_success(self):
        """Test successful CSV file reading."""
        # Setup
        # Execute
        # Assert

    def test_read_csv_file_with_missing_columns(self):
        """Test handling of CSV with missing columns."""

    def test_read_csv_file_with_invalid_encoding(self):
        """Test handling of invalid file encoding."""

    def test_read_csv_file_not_found(self):
        """Test handling of non-existent file."""

    def test_incremental_load_with_watermark(self):
        """Test incremental loading using watermark."""

class TestDatabaseConnector:
    """Test database data ingestion."""

    def test_connect_to_database_success(self):
        """Test successful database connection."""

    def test_query_with_pagination(self):
        """Test paginated query execution."""

    def test_connection_retry_on_failure(self):
        """Test retry logic for failed connections."""

    def test_connection_pool_management(self):
        """Test connection pool behavior."""
```

**Test Data**:
- Sample CSV files in `tests/fixtures/data/`
- Mock database with SQLite
- Test data generators for various scenarios

**Acceptance Criteria**:
- [ ] All connector types tested
- [ ] Error handling covered
- [ ] Retry logic validated
- [ ] Edge cases tested
- [ ] Coverage ≥ 85%

### 4.2 Data Validation Tests

**File**: `tests/unit/test_data_validation.py`

```python
class TestSchemaValidator:
    """Test schema validation."""

    def test_valid_schema_passes(self):
        """Test that valid schema passes validation."""

    def test_missing_column_fails(self):
        """Test that missing column fails validation."""

    def test_wrong_data_type_fails(self):
        """Test that wrong data type fails validation."""

    def test_extra_columns_handled(self):
        """Test handling of unexpected columns."""

class TestQualityValidator:
    """Test data quality validation."""

    def test_null_check_fails_with_nulls(self):
        """Test null check fails when nulls present."""

    def test_range_validation_with_outliers(self):
        """Test range validation detects outliers."""

    def test_uniqueness_check_with_duplicates(self):
        """Test uniqueness validation with duplicates."""

class TestGreatExpectationsIntegration:
    """Test Great Expectations integration."""

    def test_expectation_suite_creation(self):
        """Test creation of expectation suite."""

    def test_validation_run_with_failures(self):
        """Test validation run with some failures."""

    def test_validation_report_generation(self):
        """Test generation of validation reports."""
```

**Test Scenarios**:
- Valid data (should pass)
- Missing values
- Out-of-range values
- Wrong data types
- Duplicate records
- Schema mismatches

**Acceptance Criteria**:
- [ ] All validators tested
- [ ] All expectation types covered
- [ ] Report generation validated
- [ ] Coverage ≥ 90%

### 4.3 Feature Engineering Tests

**File**: `tests/unit/test_feature_engineering.py`

```python
class TestBasicTransformers:
    """Test basic feature transformations."""

    def test_normalization_scales_correctly(self):
        """Test that normalization produces correct scale."""

    def test_one_hot_encoding_creates_correct_columns(self):
        """Test one-hot encoding creates expected columns."""

    def test_missing_value_imputation(self):
        """Test missing value imputation strategies."""

class TestDerivedFeatures:
    """Test derived feature generation."""

    def test_service_count_calculation(self):
        """Test total service count calculation."""

    def test_tenure_grouping(self):
        """Test tenure group assignment."""

    def test_average_charge_per_service(self):
        """Test charge per service calculation."""

class TestTimeBasedFeatures:
    """Test time-based features."""

    def test_days_since_calculation(self):
        """Test days since calculation."""

    def test_rolling_average_computation(self):
        """Test rolling average over time windows."""

    def test_trend_detection(self):
        """Test trend detection (increasing/decreasing)."""

class TestFeatureValidation:
    """Test feature validation."""

    def test_feature_type_validation(self):
        """Test feature type checking."""

    def test_feature_range_validation(self):
        """Test feature value range validation."""

    def test_feature_distribution_check(self):
        """Test feature distribution validation."""
```

**Test Data**:
- Sample customer records with known feature values
- Edge cases (nulls, extremes, etc.)
- Time series data for temporal features

**Acceptance Criteria**:
- [ ] All transformer types tested
- [ ] Mathematical correctness validated
- [ ] Edge cases covered
- [ ] Coverage ≥ 85%

### 4.4 Model Training Tests

**File**: `tests/unit/test_model_training.py`

```python
class TestDataLoader:
    """Test data loading for training."""

    def test_train_test_split_ratio(self):
        """Test train/test split produces correct ratio."""

    def test_stratified_split_maintains_distribution(self):
        """Test stratified split maintains class balance."""

    def test_data_loader_batching(self):
        """Test batch loading functionality."""

class TestModelFactory:
    """Test model creation."""

    def test_create_logistic_regression_model(self):
        """Test creation of logistic regression model."""

    def test_create_xgboost_model(self):
        """Test creation of XGBoost model."""

    def test_model_with_custom_parameters(self):
        """Test model creation with custom parameters."""

class TestHyperparameterOptimizer:
    """Test hyperparameter optimization."""

    def test_optuna_search_space_definition(self):
        """Test search space definition."""

    def test_optimization_runs_trials(self):
        """Test that optimization runs specified trials."""

    def test_best_parameters_selected(self):
        """Test that best parameters are correctly selected."""

class TestModelEvaluator:
    """Test model evaluation."""

    def test_accuracy_calculation(self):
        """Test accuracy metric calculation."""

    def test_auc_roc_calculation(self):
        """Test AUC-ROC calculation."""

    def test_confusion_matrix_generation(self):
        """Test confusion matrix generation."""

    def test_feature_importance_extraction(self):
        """Test feature importance extraction."""
```

**Test Scenarios**:
- Small synthetic datasets for fast testing
- Known outcomes for metric validation
- Edge cases (imbalanced classes, perfect separation, etc.)

**Acceptance Criteria**:
- [ ] All model types tested
- [ ] Metrics correctly calculated
- [ ] Optimization logic validated
- [ ] Coverage ≥ 80%

### 4.5 Model Serving Tests

**File**: `tests/unit/test_model_serving.py`

```python
class TestModelLoader:
    """Test model loading."""

    def test_load_model_from_mlflow(self):
        """Test loading model from MLflow registry."""

    def test_model_caching(self):
        """Test model caching mechanism."""

    def test_model_version_switching(self):
        """Test switching between model versions."""

class TestPredictionService:
    """Test prediction service."""

    def test_single_prediction(self):
        """Test single prediction."""

    def test_batch_prediction(self):
        """Test batch predictions."""

    def test_prediction_with_missing_features(self):
        """Test handling of missing features."""

    def test_prediction_confidence_calculation(self):
        """Test confidence score calculation."""

class TestAPIEndpoints:
    """Test API endpoints (using TestClient)."""

    def test_predict_endpoint_returns_200(self):
        """Test predict endpoint returns success."""

    def test_predict_with_invalid_input(self):
        """Test predict with invalid input returns 400."""

    def test_health_endpoint(self):
        """Test health check endpoint."""

    def test_metrics_endpoint_returns_prometheus_format(self):
        """Test metrics endpoint format."""

    def test_rate_limiting(self):
        """Test rate limiting functionality."""
```

**Test Tools**:
- FastAPI TestClient for API testing
- Mock MLflow for model loading
- Sample prediction requests

**Acceptance Criteria**:
- [ ] All endpoints tested
- [ ] Error handling validated
- [ ] Input validation tested
- [ ] Coverage ≥ 90%

### 4.6 Monitoring Tests

**File**: `tests/unit/test_monitoring.py`

```python
class TestDataDriftDetector:
    """Test data drift detection."""

    def test_ks_test_detects_drift(self):
        """Test KS test detects distribution shift."""

    def test_chi_square_test_categorical_drift(self):
        """Test Chi-square test for categorical features."""

    def test_psi_calculation(self):
        """Test PSI calculation."""

    def test_no_drift_on_same_distribution(self):
        """Test no drift detected for same distribution."""

class TestModelDriftDetector:
    """Test model drift detection."""

    def test_prediction_distribution_shift(self):
        """Test detection of prediction distribution shift."""

    def test_confidence_degradation_detection(self):
        """Test detection of confidence degradation."""

class TestMetricsCollector:
    """Test metrics collection."""

    def test_counter_increment(self):
        """Test Prometheus counter increment."""

    def test_histogram_observation(self):
        """Test Prometheus histogram observation."""

    def test_gauge_update(self):
        """Test Prometheus gauge update."""
```

**Test Scenarios**:
- Known distributions with/without drift
- Synthetic prediction data
- Metrics validation

**Acceptance Criteria**:
- [ ] All drift detection methods tested
- [ ] Statistical tests validated
- [ ] Metrics correctly collected
- [ ] Coverage ≥ 85%

## 5. Integration Testing

### 5.1 Data Pipeline Integration Tests

**File**: `tests/integration/test_data_pipeline.py`

```python
class TestDataPipelineIntegration:
    """Test complete data pipeline."""

    @pytest.fixture
    def test_database(self):
        """Setup test database."""
        # Create test database
        # Load sample data
        yield db
        # Cleanup

    def test_ingest_validate_engineer_flow(self, test_database):
        """Test complete flow from ingestion to features."""
        # Ingest data
        # Validate data
        # Engineer features
        # Assert features are correct

    def test_pipeline_with_invalid_data(self, test_database):
        """Test pipeline handles invalid data gracefully."""

    def test_pipeline_with_schema_evolution(self, test_database):
        """Test pipeline handles schema changes."""

    def test_incremental_pipeline_run(self, test_database):
        """Test incremental data processing."""
```

**Test Environment**:
- Docker containers for PostgreSQL
- Test data fixtures
- Isolated test environment

**Acceptance Criteria**:
- [ ] End-to-end data flow tested
- [ ] Error scenarios covered
- [ ] Data quality maintained
- [ ] Performance acceptable

### 5.2 Training Pipeline Integration Tests

**File**: `tests/integration/test_training_pipeline.py`

```python
class TestTrainingPipelineIntegration:
    """Test complete training pipeline."""

    def test_feature_to_model_flow(self):
        """Test flow from features to trained model."""
        # Load features
        # Train model
        # Evaluate model
        # Register model
        # Assert model is in registry

    def test_hyperparameter_optimization_pipeline(self):
        """Test complete hyperparameter optimization."""

    def test_experiment_tracking_integration(self):
        """Test MLflow integration throughout pipeline."""

    def test_model_registry_workflow(self):
        """Test model promotion workflow."""
```

**Test Tools**:
- Test MLflow server
- Sample feature data
- Mock training data

**Acceptance Criteria**:
- [ ] Full training flow works
- [ ] MLflow tracking functional
- [ ] Model registry operational
- [ ] Artifacts saved correctly

### 5.3 Serving Pipeline Integration Tests

**File**: `tests/integration/test_serving_pipeline.py`

```python
class TestServingPipelineIntegration:
    """Test complete serving pipeline."""

    def test_api_with_real_model(self):
        """Test API with real model from registry."""

    def test_feature_retrieval_and_prediction(self):
        """Test feature retrieval and prediction flow."""

    def test_batch_prediction_pipeline(self):
        """Test complete batch prediction process."""

    def test_api_monitoring_integration(self):
        """Test API monitoring metrics collection."""
```

**Test Environment**:
- Running API server
- Test MLflow instance
- Test database

**Acceptance Criteria**:
- [ ] API serves predictions correctly
- [ ] Features retrieved properly
- [ ] Monitoring metrics collected
- [ ] Performance meets requirements

### 5.4 Monitoring Integration Tests

**File**: `tests/integration/test_monitoring_integration.py`

```python
class TestMonitoringIntegration:
    """Test monitoring system integration."""

    def test_drift_detection_pipeline(self):
        """Test complete drift detection workflow."""

    def test_prometheus_metrics_collection(self):
        """Test Prometheus metrics collection."""

    def test_alerting_workflow(self):
        """Test alert generation and delivery."""

    def test_dashboard_data_flow(self):
        """Test data flow to Grafana dashboards."""
```

**Test Environment**:
- Running Prometheus
- Test alert manager
- Sample monitoring data

**Acceptance Criteria**:
- [ ] Drift detected correctly
- [ ] Metrics exported properly
- [ ] Alerts triggered appropriately
- [ ] Dashboards show correct data

## 6. End-to-End Testing

### 6.1 Complete Pipeline E2E Tests

**File**: `tests/e2e/test_complete_pipeline.py`

```python
class TestCompleteMLPipeline:
    """Test complete ML pipeline end-to-end."""

    def test_raw_data_to_prediction_workflow(self):
        """
        Test complete workflow:
        1. Ingest raw data
        2. Validate data
        3. Engineer features
        4. Train model
        5. Register model
        6. Serve predictions
        7. Monitor predictions
        """

    def test_model_retraining_workflow(self):
        """
        Test model retraining workflow:
        1. Detect drift
        2. Trigger retraining
        3. Train new model
        4. Validate new model
        5. Promote to production
        6. Retire old model
        """

    def test_ab_testing_workflow(self):
        """
        Test A/B testing workflow:
        1. Deploy model A
        2. Deploy model B
        3. Route traffic to both
        4. Collect metrics
        5. Compare performance
        6. Promote winner
        """
```

**Test Duration**: Each E2E test may take 5-15 minutes

**Acceptance Criteria**:
- [ ] Complete workflow executes successfully
- [ ] All components interact correctly
- [ ] Data flows through entire system
- [ ] Results match expectations

### 6.2 Performance E2E Tests

**File**: `tests/e2e/test_performance.py`

```python
class TestPerformanceE2E:
    """Test system performance end-to-end."""

    def test_api_latency_under_load(self):
        """Test API latency with concurrent requests."""
        # Send 1000 concurrent requests
        # Assert p95 latency < 100ms

    def test_batch_prediction_throughput(self):
        """Test batch prediction throughput."""
        # Process 100K records
        # Assert throughput > 100K/minute

    def test_training_pipeline_duration(self):
        """Test training pipeline completion time."""
        # Run complete training
        # Assert completes within time limit
```

**Load Testing Tools**:
- Locust for API load testing
- Custom scripts for batch testing

**Acceptance Criteria**:
- [ ] Latency requirements met
- [ ] Throughput requirements met
- [ ] Resource usage acceptable
- [ ] No memory leaks

## 7. Testing Tools & Frameworks

### 7.1 Required Tools

```python
# requirements-dev.txt
pytest==7.4.0
pytest-cov==4.1.0
pytest-mock==3.11.1
pytest-asyncio==0.21.0
pytest-xdist==3.3.1  # Parallel testing
httpx==0.24.1  # For FastAPI testing
faker==19.3.0  # Test data generation
factory-boy==3.3.0  # Test fixtures
hypothesis==6.82.0  # Property-based testing
locust==2.15.1  # Load testing
```

### 7.2 Test Configuration

**File**: `pytest.ini`

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --verbose
    --strict-markers
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
    smoke: Smoke tests for quick validation
```

### 7.3 Running Tests

```bash
# Run all tests
pytest

# Run specific test types
pytest -m unit
pytest -m integration
pytest -m e2e

# Run with coverage
pytest --cov=src --cov-report=html

# Run in parallel
pytest -n auto

# Run specific test file
pytest tests/unit/test_data_ingestion.py

# Run specific test
pytest tests/unit/test_data_ingestion.py::TestCSVConnector::test_read_csv_file_success

# Run with verbose output
pytest -vv

# Run only failed tests
pytest --lf

# Run smoke tests (fast validation)
pytest -m smoke
```

## 8. Static Analysis

### 8.1 Code Linting

```bash
# Flake8 configuration (.flake8)
[flake8]
max-line-length = 100
exclude = .git,__pycache__,venv
ignore = E203,W503

# Run linting
flake8 src/ tests/
```

### 8.2 Code Formatting

```bash
# Black configuration
# Run formatting
black src/ tests/ --check  # Check only
black src/ tests/  # Format in place
```

### 8.3 Type Checking

```bash
# Mypy configuration (mypy.ini)
[mypy]
python_version = 3.9
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True

# Run type checking
mypy src/
```

### 8.4 Security Scanning

```bash
# Run Bandit security scanner
bandit -r src/

# Run safety check for dependencies
safety check

# Run pip-audit
pip-audit
```

## 9. Continuous Integration

### 9.1 CI Pipeline

**File**: `.github/workflows/ci.yml`

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint
        run: make lint

      - name: Type check
        run: make type-check

      - name: Security scan
        run: make security-check

      - name: Unit tests
        run: pytest -m unit --cov=src --cov-report=xml

      - name: Integration tests
        run: pytest -m integration

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### 9.2 PR Checks

All pull requests must pass:
- [ ] All tests (unit, integration)
- [ ] Code coverage ≥ 80%
- [ ] Linting (flake8)
- [ ] Type checking (mypy)
- [ ] Security scanning (bandit)
- [ ] Code formatting (black)

## 10. Model Validation

### 10.1 Model Performance Validation

```python
def validate_model_performance(model, test_data):
    """Validate model meets performance requirements."""

    metrics = evaluate_model(model, test_data)

    # Performance requirements
    assert metrics['auc_roc'] >= 0.85, "AUC-ROC below threshold"
    assert metrics['f1_score'] >= 0.70, "F1 score below threshold"
    assert metrics['precision'] >= 0.75, "Precision below threshold"
    assert metrics['recall'] >= 0.65, "Recall below threshold"

    return True
```

### 10.2 Model Fairness Validation

```python
def validate_model_fairness(model, test_data):
    """Validate model fairness across demographics."""

    # Check demographic parity
    predictions_by_group = group_predictions(test_data)

    # Assert similar prediction rates
    max_disparity = calculate_demographic_parity(predictions_by_group)
    assert max_disparity <= 0.10, "Demographic disparity too high"

    # Check equal opportunity
    tpr_by_group = calculate_tpr_by_group(predictions_by_group)
    max_tpr_diff = max(tpr_by_group) - min(tpr_by_group)
    assert max_tpr_diff <= 0.10, "TPR disparity too high"

    return True
```

### 10.3 Model Explainability Validation

```python
def validate_model_explainability(model, test_data):
    """Validate model can be explained."""

    # Check feature importance available
    assert hasattr(model, 'feature_importances_'), "No feature importance"

    # Check SHAP values can be computed
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(test_data)

    # Validate explanation quality
    assert shap_values is not None, "Cannot generate SHAP values"

    return True
```

## 11. Production Validation

### 11.1 Smoke Tests

```bash
# Run smoke tests after deployment
pytest -m smoke

# Test critical paths only
pytest tests/e2e/test_smoke.py
```

### 11.2 Deployment Validation Checklist

Pre-deployment:
- [ ] All tests pass in staging
- [ ] Model performance validated
- [ ] API load tested
- [ ] Monitoring configured
- [ ] Alerts set up
- [ ] Rollback plan ready

Post-deployment:
- [ ] Health checks passing
- [ ] API responding correctly
- [ ] Predictions being made
- [ ] Metrics being collected
- [ ] No error spikes in logs
- [ ] Performance within SLAs

### 11.3 Canary Deployment Validation

```python
def validate_canary_deployment(canary_metrics, baseline_metrics):
    """Validate canary deployment performs well."""

    # Compare error rates
    error_rate_increase = (
        canary_metrics['error_rate'] - baseline_metrics['error_rate']
    )
    assert error_rate_increase <= 0.01, "Error rate increased"

    # Compare latency
    latency_increase = (
        canary_metrics['p95_latency'] - baseline_metrics['p95_latency']
    )
    assert latency_increase <= 10, "Latency increased too much"

    # Compare prediction quality (if labels available)
    if canary_metrics.get('accuracy'):
        accuracy_decrease = (
            baseline_metrics['accuracy'] - canary_metrics['accuracy']
        )
        assert accuracy_decrease <= 0.02, "Accuracy decreased"

    return True
```

## 12. Testing Checklist

### Pre-Development
- [ ] Test environment set up
- [ ] Test data prepared
- [ ] Test fixtures created
- [ ] CI/CD configured

### During Development
- [ ] Unit tests written for new code
- [ ] Tests pass locally
- [ ] Code coverage maintained
- [ ] Integration tests updated

### Pre-Deployment
- [ ] All tests passing
- [ ] E2E tests executed
- [ ] Performance tests passed
- [ ] Security scans clean
- [ ] Documentation updated

### Post-Deployment
- [ ] Smoke tests passed
- [ ] Monitoring validated
- [ ] Production metrics normal
- [ ] No errors in logs

## 13. Success Criteria

The project validation is successful when:

1. **Test Coverage**
   - Overall coverage ≥ 80%
   - Critical paths coverage = 100%
   - All test types implemented

2. **Test Quality**
   - All tests are deterministic
   - No flaky tests
   - Fast test execution
   - Clear test naming

3. **CI/CD**
   - All checks automated
   - PR validation working
   - Deployment pipeline functional
   - Rollback tested

4. **Performance**
   - API latency < 100ms (p95)
   - Batch throughput > 100K/min
   - No resource leaks
   - Stable under load

5. **Production Readiness**
   - Smoke tests passing
   - Monitoring operational
   - Alerts configured
   - Documentation complete
