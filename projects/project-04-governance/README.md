# Project 4: ML Governance & Compliance System

## Overview

A comprehensive governance system for machine learning models that ensures fairness, regulatory compliance (GDPR), and complete auditability. This system provides end-to-end governance from model development through deployment, with cryptographic audit trails and automated compliance checking.

## Problem Statement

Modern ML systems require:
- **Fairness**: Models must not discriminate based on protected attributes
- **Compliance**: GDPR and other regulations mandate transparency and user rights
- **Auditability**: Complete, tamper-proof records of all model decisions and changes
- **Governance**: Multi-stakeholder approval workflows before deployment
- **Quality**: Automated validation of data and model quality

## Key Features

### 1. Fairness Assessment & Mitigation
- **Metrics**: Demographic parity, equalized odds, disparate impact analysis
- **Detection**: Automated bias detection across protected groups
- **Mitigation**: Reweighting, ExponentiatedGradient, threshold optimization
- **Reporting**: Comprehensive fairness reports with visualizations

### 2. GDPR Compliance
- **Right to Explanation**: Model decision explanations using SHAP/LIME
- **Right to Erasure**: Data deletion with cascade tracking
- **Data Minimization**: Automated feature reduction recommendations
- **Privacy Impact**: Assessment tools for privacy risk
- **Consent Management**: Track and enforce data usage consent

### 3. Tamper-Proof Audit Logging
- **Merkle Trees**: Cryptographic proof of log integrity
- **SHA-256 Hashing**: Immutable event records
- **Chain Verification**: Continuous integrity checking
- **Event Tracking**: Model training, predictions, updates, access

### 4. Automated Model Cards
- **Template-Based**: Standardized documentation format
- **Auto-Population**: Extract metadata from training runs
- **Version Control**: Track model card evolution
- **Compliance Mapping**: Link to regulatory requirements

### 5. Multi-Stage Approval Workflow
- **State Machine**: Defined approval stages and transitions
- **Role-Based**: Data scientist, compliance officer, business owner
- **Notifications**: Automated alerts for pending approvals
- **Audit Trail**: Complete history of approval decisions

### 6. Data Quality Validation
- **Great Expectations**: Comprehensive data validation
- **Schema Validation**: Type and constraint checking
- **Statistical Tests**: Distribution and correlation analysis
- **Automated Reporting**: Quality reports and alerts

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     ML Governance System                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Fairness   │  │  Compliance  │  │    Audit     │     │
│  │  Assessment  │  │    Engine    │  │   Logging    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         └──────────────────┴──────────────────┘            │
│                          │                                 │
│                 ┌────────▼────────┐                        │
│                 │  Model Cards    │                        │
│                 │   Generator     │                        │
│                 └────────┬────────┘                        │
│                          │                                 │
│                 ┌────────▼────────┐                        │
│                 │    Approval     │                        │
│                 │    Workflow     │                        │
│                 └────────┬────────┘                        │
│                          │                                 │
│                 ┌────────▼────────┐                        │
│                 │   Validation    │                        │
│                 │     Engine      │                        │
│                 └─────────────────┘                        │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                    Data Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  PostgreSQL  │  │     Redis    │  │   MinIO      │     │
│  │  Audit Logs  │  │    Cache     │  │  Artifacts   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Core ML & Governance
- **Fairlearn**: Fairness assessment and mitigation
- **SHAP/LIME**: Model interpretability
- **Great Expectations**: Data validation
- **MLflow**: Model tracking and registry

### Infrastructure
- **FastAPI**: REST API for governance operations
- **PostgreSQL**: Audit logs and compliance records
- **Redis**: Caching and session management
- **MinIO**: Model artifact storage
- **Docker**: Containerization

### Security & Cryptography
- **hashlib**: SHA-256 hashing
- **cryptography**: Encryption utilities
- **PyJWT**: Token-based authentication
- **bcrypt**: Password hashing

## Project Structure

```
project-4-governance/
├── README.md                      # This file
├── REQUIREMENTS.md                # Detailed requirements
├── ARCHITECTURE.md                # System architecture
├── GETTING_STARTED.md             # Setup and quickstart
├── VALIDATION.md                  # Testing and validation
├── requirements.txt               # Python dependencies
├── docker-compose.yml             # Infrastructure setup
├── .env.example                   # Environment template
│
├── src/
│   ├── fairness/                  # Fairness assessment
│   │   ├── __init__.py
│   │   ├── metrics.py             # Fairness metrics
│   │   ├── detector.py            # Bias detection
│   │   ├── mitigator.py           # Mitigation strategies
│   │   └── reporter.py            # Fairness reports
│   │
│   ├── audit/                     # Audit logging
│   │   ├── __init__.py
│   │   ├── logger.py              # Event logging
│   │   ├── merkle_tree.py         # Merkle tree implementation
│   │   ├── verifier.py            # Integrity verification
│   │   └── storage.py             # PostgreSQL storage
│   │
│   ├── compliance/                # GDPR compliance
│   │   ├── __init__.py
│   │   ├── gdpr_engine.py         # GDPR compliance checks
│   │   ├── explainer.py           # Right to explanation
│   │   ├── erasure.py             # Right to erasure
│   │   ├── privacy_impact.py      # Privacy assessment
│   │   └── consent.py             # Consent management
│   │
│   ├── model_cards/               # Model documentation
│   │   ├── __init__.py
│   │   ├── generator.py           # Card generation
│   │   ├── template.py            # Card templates
│   │   ├── metadata.py            # Metadata extraction
│   │   └── renderer.py            # HTML/PDF rendering
│   │
│   ├── approval/                  # Approval workflow
│   │   ├── __init__.py
│   │   ├── workflow.py            # State machine
│   │   ├── approver.py            # Approval logic
│   │   ├── notifier.py            # Notifications
│   │   └── history.py             # Approval history
│   │
│   ├── validation/                # Data validation
│   │   ├── __init__.py
│   │   ├── expectations.py        # Great Expectations
│   │   ├── schema_validator.py    # Schema validation
│   │   ├── quality_checker.py     # Quality metrics
│   │   └── reporter.py            # Validation reports
│   │
│   ├── api/                       # FastAPI endpoints
│   │   ├── __init__.py
│   │   ├── main.py                # API application
│   │   ├── routes/                # API routes
│   │   └── models.py              # Pydantic models
│   │
│   └── utils/                     # Utilities
│       ├── __init__.py
│       ├── crypto.py              # Cryptographic utilities
│       ├── database.py            # Database utilities
│       └── config.py              # Configuration
│
├── tests/
│   ├── unit/                      # Unit tests
│   │   ├── test_fairness.py
│   │   ├── test_audit.py
│   │   ├── test_compliance.py
│   │   ├── test_model_cards.py
│   │   ├── test_approval.py
│   │   └── test_validation.py
│   │
│   └── integration/               # Integration tests
│       ├── test_end_to_end.py
│       ├── test_api.py
│       └── test_workflow.py
│
├── config/                        # Configuration files
│   ├── fairness_thresholds.yaml
│   ├── approval_workflow.yaml
│   ├── gdpr_requirements.yaml
│   └── validation_suites.yaml
│
├── docs/                          # Additional documentation
│   ├── fairness_metrics.md
│   ├── gdpr_compliance.md
│   ├── audit_specification.md
│   ├── model_card_template.md
│   └── api_documentation.md
│
├── scripts/                       # Utility scripts
│   ├── setup_database.py
│   ├── generate_test_data.py
│   ├── verify_audit_chain.py
│   └── export_compliance_report.py
│
└── infrastructure/                # Infrastructure as code
    ├── docker/
    │   ├── Dockerfile.api
    │   └── Dockerfile.worker
    ├── postgresql/
    │   └── init.sql
    └── kubernetes/
        ├── deployment.yaml
        └── service.yaml
```

## Quick Start

```bash
# 1. Clone and navigate
cd /path/to/project-04-governance

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start infrastructure
docker-compose up -d

# 4. Initialize database
python scripts/setup_database.py

# 5. Run example governance workflow
python examples/complete_workflow.py

# 6. Start API server
uvicorn src.api.main:app --reload

# 7. Run tests
pytest tests/ -v --cov=src
```

## Use Cases

### 1. Fairness Assessment
```python
from src.fairness import FairnessDetector, FairnessMitigator

# Detect bias
detector = FairnessDetector()
report = detector.assess_model(model, X_test, y_test, sensitive_features)

# Mitigate if needed
if report.has_violations():
    mitigator = FairnessMitigator(strategy="exponentiated_gradient")
    fair_model = mitigator.mitigate(model, X_train, y_train, sensitive_features)
```

### 2. GDPR Compliance
```python
from src.compliance import GDPREngine

# Check compliance
engine = GDPREngine()
compliance_report = engine.assess_model(model, training_data)

# Generate explanation
explanation = engine.explain_prediction(model, sample_data, user_id)

# Process erasure request
engine.erase_user_data(user_id, cascade=True)
```

### 3. Audit Logging
```python
from src.audit import AuditLogger

# Log model training
logger = AuditLogger()
logger.log_training(
    model_id="model-123",
    dataset_version="v1.0",
    hyperparameters=params,
    metrics=results
)

# Verify integrity
verifier = logger.verify_chain()
assert verifier.is_valid()
```

### 4. Approval Workflow
```python
from src.approval import ApprovalWorkflow

# Submit for approval
workflow = ApprovalWorkflow()
workflow.submit_model(model_id="model-123", submitter="data-scientist")

# Approve stages
workflow.approve(model_id="model-123", approver="compliance-officer", role="compliance")
workflow.approve(model_id="model-123", approver="business-owner", role="business")

# Deploy if all approved
if workflow.is_approved(model_id="model-123"):
    deploy_model(model_id)
```

## Learning Objectives

After completing this project, you will understand:

1. **ML Fairness**: Metrics, detection, and mitigation techniques
2. **GDPR Compliance**: Legal requirements and implementation
3. **Cryptographic Auditing**: Merkle trees and tamper-proof logs
4. **Workflow Automation**: State machines and approval processes
5. **Data Governance**: Quality validation and schema enforcement
6. **API Design**: RESTful governance APIs
7. **System Integration**: Combining multiple governance components

## Related Projects

- **Project 1**: Model Monitoring (metrics and alerts)
- **Project 2**: Feature Store (data lineage)
- **Project 3**: AutoML Pipeline (model development)
- **Project 5**: Distributed Training (scalability)

## Resources

### Fairness in ML
- [Fairlearn Documentation](https://fairlearn.org/)
- [Aequitas Toolkit](http://www.datasciencepublicpolicy.org/projects/aequitas/)
- [AI Fairness 360](https://aif360.mybluemix.net/)

### GDPR
- [GDPR Official Text](https://gdpr-info.eu/)
- [ICO Guidelines](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/)

### Model Cards
- [Model Cards Paper](https://arxiv.org/abs/1810.03993)
- [Google Model Cards](https://modelcards.withgoogle.com/)

### Audit & Compliance
- [NIST AI Risk Management](https://www.nist.gov/itl/ai-risk-management-framework)
- [ISO/IEC 23894:2023](https://www.iso.org/standard/77304.html)

## License

MIT License - See LICENSE file for details

## Contributors

Built for the AI Infrastructure & MLOps Learning Path

---

**Next Steps**: See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed setup instructions
