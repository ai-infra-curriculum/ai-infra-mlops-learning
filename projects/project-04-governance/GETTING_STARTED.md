# Getting Started: ML Governance & Compliance System

## Prerequisites

### System Requirements
- **OS**: Linux, macOS, or Windows with WSL2
- **Python**: 3.9 or higher
- **Docker**: 20.10 or higher
- **Docker Compose**: 2.0 or higher
- **Git**: 2.30 or higher
- **Memory**: Minimum 8GB RAM (16GB recommended)
- **Storage**: 20GB free space

### Knowledge Prerequisites
- Python programming
- Basic SQL
- REST APIs
- Docker basics
- ML fundamentals
- Basic cryptography concepts

## Installation

### Step 1: Clone the Repository

```bash
# Navigate to the learning repository
cd /path/to/ai-infra-mlops-learning

# Navigate to Project 4
cd projects/project-04-governance
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Step 4: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env
```

**Required Environment Variables**:
```bash
# Database
DATABASE_URL=postgresql://governance:password@localhost:5432/governance_db

# Redis
REDIS_URL=redis://localhost:6379/0

# MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=governance-artifacts

# API
API_SECRET_KEY=<generate-with-openssl-rand-hex-32>
API_HOST=0.0.0.0
API_PORT=8000

# Audit
AUDIT_ENABLED=true
MERKLE_TREE_SIZE=1000

# Fairness
FAIRNESS_THRESHOLD_DEMOGRAPHIC_PARITY=0.1
FAIRNESS_THRESHOLD_EQUALIZED_ODDS=0.1
FAIRNESS_THRESHOLD_DISPARATE_IMPACT=0.8

# GDPR
GDPR_COMPLIANCE_STRICT=true
ERASURE_VERIFICATION_REQUIRED=true

# Notifications
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
NOTIFICATION_FROM_EMAIL=governance@example.com

# Approval
APPROVAL_TIMEOUT_HOURS=72
APPROVAL_ESCALATION_ENABLED=true
```

### Step 5: Start Infrastructure

```bash
# Start PostgreSQL, Redis, and MinIO
docker-compose up -d

# Verify services are running
docker-compose ps

# Expected output:
# NAME                    STATUS
# governance-postgres     Up
# governance-redis        Up
# governance-minio        Up
```

### Step 6: Initialize Database

```bash
# Run database initialization script
python scripts/setup_database.py

# Expected output:
# ✓ Database connection successful
# ✓ Creating tables...
# ✓ Creating indexes...
# ✓ Inserting seed data...
# ✓ Database initialized successfully
```

### Step 7: Verify Installation

```bash
# Run verification script
python scripts/verify_installation.py

# Expected output:
# ✓ Python version: 3.9.x
# ✓ PostgreSQL connection: OK
# ✓ Redis connection: OK
# ✓ MinIO connection: OK
# ✓ All dependencies installed
# ✓ Environment variables configured
# ✓ Installation verified successfully
```

## Quick Start Examples

### Example 1: Fairness Assessment

```python
from src.fairness import FairnessDetector, FairnessMetrics
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

# Create sample data with bias
X, y = make_classification(n_samples=1000, n_features=10, random_state=42)
sensitive_feature = np.random.binomial(1, 0.7, size=1000)  # Imbalanced groups

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Assess fairness
detector = FairnessDetector()
report = detector.assess_model(
    model=model,
    X_test=X,
    y_test=y,
    sensitive_features=pd.DataFrame({'group': sensitive_feature}),
    sensitive_feature_names=['group']
)

# Print results
print(f"Demographic Parity Difference: {report.metrics['demographic_parity']:.3f}")
print(f"Equalized Odds Difference: {report.metrics['equalized_odds']:.3f}")
print(f"Disparate Impact: {report.metrics['disparate_impact']:.3f}")
print(f"\nViolations: {len(report.violations)}")
print(f"Severity: {report.severity}")
```

### Example 2: GDPR Compliance Check

```python
from src.compliance import GDPREngine
import pandas as pd

# Initialize GDPR engine
gdpr_engine = GDPREngine()

# Sample data
training_data = pd.DataFrame({
    'user_id': range(100),
    'age': np.random.randint(18, 80, 100),
    'income': np.random.randint(20000, 150000, 100),
    'credit_score': np.random.randint(300, 850, 100)
})

# Assess compliance
compliance_report = gdpr_engine.assess_model(
    model=model,
    training_data=training_data,
    user_id_column='user_id'
)

print(f"Overall Compliance Score: {compliance_report.score:.2%}")
print(f"Right to Explanation: {'✓' if compliance_report.has_explanation else '✗'}")
print(f"Data Minimization: {'✓' if compliance_report.is_minimal else '✗'}")
print(f"Privacy Impact: {compliance_report.privacy_risk}")

# Generate explanation for a prediction
sample = training_data.iloc[0]
explanation = gdpr_engine.explain_prediction(
    model=model,
    sample=sample.drop('user_id'),
    user_id=sample['user_id']
)

print(f"\nTop 3 Contributing Features:")
for feature, contribution in explanation.feature_contributions[:3]:
    print(f"  - {feature}: {contribution:.3f}")
```

### Example 3: Audit Logging

```python
from src.audit import AuditLogger
from datetime import datetime

# Initialize audit logger
audit_logger = AuditLogger()

# Log model training
training_event = audit_logger.log_training(
    model_id="customer-churn-v1",
    dataset_version="2025-10-26",
    hyperparameters={
        "n_estimators": 100,
        "max_depth": 10,
        "random_state": 42
    },
    metrics={
        "accuracy": 0.87,
        "precision": 0.85,
        "recall": 0.82
    },
    actor="data-scientist@example.com"
)
print(f"Training event logged: {training_event}")

# Log predictions
for i in range(10):
    prediction_event = audit_logger.log_prediction(
        model_id="customer-churn-v1",
        input_hash=f"hash_{i}",
        prediction=np.random.binomial(1, 0.3),
        actor="api-service"
    )

# Verify audit log integrity
verification_result = audit_logger.verify_chain()
print(f"\nAudit log integrity: {'✓ Valid' if verification_result.is_valid else '✗ Invalid'}")
print(f"Total events: {verification_result.total_events}")
print(f"Merkle root: {verification_result.merkle_root[:16]}...")
```

### Example 4: Model Card Generation

```python
from src.model_cards import ModelCardGenerator

# Initialize generator
card_generator = ModelCardGenerator()

# Generate model card
model_card = card_generator.generate_card(
    model_id="customer-churn-v1",
    model_name="Customer Churn Predictor",
    model_version="v1.0.0",
    model_type="Random Forest Classifier",
    owners=["data-science-team@example.com"],
    intended_use="Predict customer churn risk for retention campaigns",
    out_of_scope_uses=["Credit decisions", "Employment decisions"]
)

# Render as HTML
html_card = card_generator.render_html(model_card)

# Save to file
with open("model_card.html", "w") as f:
    f.write(html_card)

print(f"Model card generated: model_card.html")
print(f"Sections completed: {model_card.completion_percentage:.1f}%")
```

### Example 5: Approval Workflow

```python
from src.approval import ApprovalWorkflow

# Initialize workflow
workflow = ApprovalWorkflow()

# Submit model for approval
submission = workflow.submit_model(
    model_id="customer-churn-v1",
    submitter="data-scientist@example.com",
    model_card=model_card,
    fairness_report=report,
    compliance_report=compliance_report
)
print(f"Model submitted. Current state: {submission.state}")

# Technical review approval
workflow.approve(
    model_id="customer-churn-v1",
    approver="tech-lead@example.com",
    role="technical",
    comments="Model architecture looks good. Tests passing."
)
print(f"Technical approval granted. State: {workflow.get_state('customer-churn-v1')}")

# Compliance review approval
workflow.approve(
    model_id="customer-churn-v1",
    approver="compliance-officer@example.com",
    role="compliance",
    comments="GDPR compliance verified. Fairness metrics acceptable."
)
print(f"Compliance approval granted. State: {workflow.get_state('customer-churn-v1')}")

# Business review approval
workflow.approve(
    model_id="customer-churn-v1",
    approver="business-owner@example.com",
    role="business",
    comments="Business case validated. Proceeding with deployment."
)
print(f"Business approval granted. State: {workflow.get_state('customer-churn-v1')}")

# Check if approved
if workflow.is_approved("customer-churn-v1"):
    print("✓ Model fully approved and ready for deployment!")
```

### Example 6: Data Validation

```python
from src.validation import DataValidator, QualityChecker
import pandas as pd

# Initialize validator
validator = DataValidator()

# Sample data
data = pd.DataFrame({
    'age': np.random.randint(18, 80, 100),
    'income': np.random.randint(20000, 150000, 100),
    'credit_score': np.random.randint(300, 850, 100),
    'account_balance': np.random.uniform(-1000, 50000, 100)
})

# Create expectation suite
suite = validator.create_expectation_suite("customer_data")

# Add expectations
suite.expect_column_values_to_be_between("age", min_value=18, max_value=120)
suite.expect_column_values_to_be_between("income", min_value=0, max_value=1000000)
suite.expect_column_values_to_be_between("credit_score", min_value=300, max_value=850)
suite.expect_column_values_to_not_be_null("age")
suite.expect_column_values_to_not_be_null("income")

# Validate data
validation_result = validator.validate_data(data, "customer_data")

print(f"Validation Success: {validation_result.success}")
print(f"Expectations Evaluated: {validation_result.statistics['evaluated_expectations']}")
print(f"Successful Expectations: {validation_result.statistics['successful_expectations']}")
print(f"Success Percentage: {validation_result.statistics['success_percent']:.1f}%")

# Quality checks
quality_checker = QualityChecker()
quality_report = quality_checker.check_quality(data)

print(f"\nData Quality Score: {quality_report.overall_score:.2f}")
print(f"Missing Data: {quality_report.missing_percentage:.1f}%")
print(f"Outliers Detected: {quality_report.outlier_count}")
```

## Running the API Server

### Start the API Server

```bash
# Development mode (with auto-reload)
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Access API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Test API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Get API version
curl http://localhost:8000/version

# Assess fairness (requires authentication)
curl -X POST http://localhost:8000/api/v1/fairness/assess \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "customer-churn-v1",
    "test_data": {...},
    "sensitive_features": [...]
  }'
```

## Running Tests

### Unit Tests

```bash
# Run all unit tests
pytest tests/unit/ -v

# Run specific test file
pytest tests/unit/test_fairness.py -v

# Run with coverage
pytest tests/unit/ --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Integration Tests

```bash
# Ensure infrastructure is running
docker-compose up -d

# Run integration tests
pytest tests/integration/ -v

# Run end-to-end workflow test
pytest tests/integration/test_end_to_end.py -v -s
```

### All Tests

```bash
# Run complete test suite
pytest tests/ -v --cov=src --cov-report=term-missing

# Generate coverage report
pytest tests/ --cov=src --cov-report=html
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/my-new-feature
```

### 2. Make Changes

Edit source files in `src/` directory.

### 3. Write Tests

Add tests in `tests/unit/` or `tests/integration/`.

### 4. Run Tests Locally

```bash
pytest tests/ -v
```

### 5. Format Code

```bash
# Format with black
black src/ tests/

# Sort imports
isort src/ tests/

# Lint with flake8
flake8 src/ tests/

# Type check with mypy
mypy src/
```

### 6. Commit Changes

```bash
git add .
git commit -m "feat: Add new fairness metric"
```

### 7. Push and Create PR

```bash
git push origin feature/my-new-feature
```

## Common Tasks

### Reset Database

```bash
# Stop containers
docker-compose down -v

# Restart with fresh database
docker-compose up -d

# Reinitialize
python scripts/setup_database.py
```

### View Logs

```bash
# API logs
tail -f logs/api.log

# Docker logs
docker-compose logs -f

# Specific service
docker-compose logs -f postgres
```

### Generate Test Data

```bash
# Generate synthetic test data
python scripts/generate_test_data.py --num-models 10 --num-predictions 1000

# Output:
# ✓ Generated 10 model training events
# ✓ Generated 1000 prediction events
# ✓ Generated 10 model cards
# ✓ Generated 30 approval decisions
# ✓ Test data saved to data/test/
```

### Verify Audit Chain

```bash
# Verify complete audit chain integrity
python scripts/verify_audit_chain.py

# Output:
# ✓ Verifying 1234 audit events...
# ✓ Hash chain integrity: VALID
# ✓ Merkle tree integrity: VALID
# ✓ No tampering detected
# ✓ Audit chain verified successfully
```

### Export Compliance Report

```bash
# Export compliance report for all models
python scripts/export_compliance_report.py --output compliance_report.pdf

# Export for specific model
python scripts/export_compliance_report.py \
  --model-id customer-churn-v1 \
  --output customer_churn_compliance.pdf
```

## Configuration

### Fairness Thresholds

Edit `config/fairness_thresholds.yaml`:

```yaml
thresholds:
  demographic_parity:
    threshold: 0.1
    severity: HIGH

  equalized_odds:
    threshold: 0.1
    severity: HIGH

  disparate_impact:
    threshold: 0.8  # 80% rule
    severity: CRITICAL

protected_attributes:
  - race
  - gender
  - age
  - disability
```

### Approval Workflow

Edit `config/approval_workflow.yaml`:

```yaml
stages:
  - name: technical
    required_approvers: 1
    roles: [data_scientist, ml_engineer]
    timeout_hours: 48

  - name: compliance
    required_approvers: 1
    roles: [compliance_officer, legal]
    timeout_hours: 72

  - name: business
    required_approvers: 1
    roles: [product_owner, business_stakeholder]
    timeout_hours: 24

notifications:
  enabled: true
  channels: [email, slack]
  escalation_enabled: true
  escalation_after_hours: 72
```

### GDPR Requirements

Edit `config/gdpr_requirements.yaml`:

```yaml
compliance:
  strict_mode: true

  right_to_explanation:
    required: true
    methods: [shap, lime]
    format: human_readable

  right_to_erasure:
    enabled: true
    verification_required: true
    cascade_deletion: true
    max_response_days: 30

  data_minimization:
    enabled: true
    feature_importance_threshold: 0.01
    correlation_threshold: 0.95

  consent_management:
    required: true
    version_tracking: true
    purpose_limitation: true
```

### Validation Suites

Edit `config/validation_suites.yaml`:

```yaml
suites:
  customer_data:
    expectations:
      - type: expect_column_values_to_be_between
        column: age
        min_value: 18
        max_value: 120

      - type: expect_column_values_to_not_be_null
        column: user_id

      - type: expect_column_values_to_be_unique
        column: user_id

      - type: expect_column_values_to_match_regex
        column: email
        regex: "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"
```

## Troubleshooting

### Issue: Database Connection Failed

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres

# Verify connection
psql -h localhost -U governance -d governance_db
```

### Issue: Redis Connection Failed

```bash
# Check if Redis is running
docker-compose ps redis

# Test connection
redis-cli ping

# Restart Redis
docker-compose restart redis
```

### Issue: Import Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

### Issue: Tests Failing

```bash
# Clean pytest cache
pytest --cache-clear

# Run tests with verbose output
pytest tests/ -v -s

# Run specific test with debugging
pytest tests/unit/test_fairness.py::test_demographic_parity -v -s
```

### Issue: Slow Performance

```bash
# Check resource usage
docker stats

# Increase memory limits in docker-compose.yml
# Add query indexes to PostgreSQL
# Enable Redis caching
```

## Next Steps

1. **Complete the Examples**: Work through all 6 examples above
2. **Read the Documentation**: Review ARCHITECTURE.md and REQUIREMENTS.md
3. **Explore the API**: Use the Swagger UI to test endpoints
4. **Run the Tests**: Ensure all tests pass
5. **Build a Project**: Implement a governance workflow for your own model
6. **Contribute**: Add new features or improve existing ones

## Additional Resources

- **Fairness**: See `docs/fairness_metrics.md`
- **GDPR**: See `docs/gdpr_compliance.md`
- **Audit**: See `docs/audit_specification.md`
- **API**: See `docs/api_documentation.md`
- **Model Cards**: See `docs/model_card_template.md`

## Support

- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Join GitHub Discussions
- **Documentation**: Check the `/docs` directory
- **Email**: governance-support@example.com

---

**Happy Governing!** Ensure your ML models are fair, compliant, and auditable.
