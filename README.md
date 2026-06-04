# MLOps Engineer Learning Repository

**AI Infrastructure Career Path - Level 2.5B: MLOps Engineer**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Status: Learning](https://img.shields.io/badge/status-learning-green.svg)]()

## Overview

This repository contains comprehensive learning materials for the **MLOps Engineer** role in the AI Infrastructure career path. MLOps Engineers focus on CI/CD for ML systems, monitoring, data quality, automated retraining, and governance - bridging the gap between model development and production operations.

### What You'll Learn

By completing this curriculum, you will master:

- **CI/CD for ML**: Build automated pipelines with GitHub Actions, ArgoCD, and GitOps workflows
- **Model Monitoring**: Implement drift detection, performance tracking, and automated alerting systems
- **Data Quality**: Design validation frameworks with Great Expectations and data contracts
- **Automated Retraining**: Create intelligent retraining triggers and A/B testing frameworks
- **ML Governance**: Build approval workflows, fairness assessment, and compliance systems

### Prerequisites

Before starting this curriculum, you should have:

- ✅ Completed **AI Infrastructure Engineer (Level 2)** projects or equivalent experience
- ✅ Strong Python programming skills (3.9+)
- ✅ Understanding of ML fundamentals and model lifecycle
- ✅ Kubernetes and Docker basics
- ✅ CI/CD concepts (GitHub Actions, Jenkins, or similar)
- ✅ Basic statistics knowledge
- ✅ Git version control proficiency

### Time Commitment

- **Total Duration**: 580 hours (~14.5 weeks full-time)
- **Difficulty Level**: Advanced to Expert
- **Recommended Pace**: 3-6 months part-time study
- **Projects**: 5 comprehensive hands-on projects

## Repository Structure

```
ai-infra-mlops-learning/
├── README.md                          # This file
├── CURRICULUM.md                      # Detailed learning curriculum
├── LICENSE                            # MIT License
├── CODE_OF_CONDUCT.md                # Community guidelines
├── CONTRIBUTING.md                    # Contribution guidelines
├── requirements.txt                   # Python dependencies
├── .gitignore                        # Git ignore patterns
│
├── .github/                          # GitHub configuration
│   ├── workflows/                    # CI/CD workflows
│   │   ├── validate-code.yml         # Code validation
│   │   └── test-stubs.yml            # Test stubs
│   ├── ISSUE_TEMPLATE/               # Issue templates
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   ├── question.md
│   │   └── project_help.md
│   └── PULL_REQUEST_TEMPLATE.md      # PR template
│
├── lessons/                          # Learning modules
│   ├── 01-mlops-foundations/        # Foundations
│   ├── 02-cicd-for-ml/              # CI/CD fundamentals
│   ├── 03-model-monitoring/         # Monitoring & drift
│   ├── 04-data-quality/             # Data validation
│   ├── 05-experimentation/          # A/B testing
│   ├── 06-automation/               # Workflow automation
│   ├── 07-governance/               # ML governance
│   ├── 08-production-ops/           # Production operations
│   ├── 09-security/                 # MLOps security
│   └── 10-advanced-topics/          # Advanced patterns
│
├── projects/                        # Hands-on projects
│   ├── project-01-cicd-pipeline/    # ML CI/CD Pipeline
│   ├── project-02-monitoring/       # Model Monitoring
│   ├── project-03-validation/       # Data Validation
│   ├── project-04-retraining/       # Auto Retraining & A/B
│   └── project-05-governance/       # Governance System
│
├── assessments/                     # Evaluation materials
│   ├── quizzes/                     # Knowledge checks
│   ├── practical-exams/             # Hands-on assessments
│   └── certification/               # Certification prep
│
├── resources/                       # Additional resources
│   ├── reading-list.md              # Recommended reading
│   ├── tools.md                     # Tool ecosystem
│   ├── references.md                # Reference materials
│   └── cheat-sheets/                # Quick references
│
├── progress/                        # Track your progress
│   ├── checklist.md                 # Learning checklist
│   └── notes/                       # Personal notes
│
└── community/                       # Community resources
    ├── discussions.md               # Discussion guide
    ├── study-groups.md              # Study group info
    └── mentorship.md                # Mentorship program
```

## Projects Overview

### Project 1: Comprehensive ML CI/CD Pipeline (120 hours)
**Complexity**: Advanced | **Prerequisites**: Kubernetes, CI/CD basics

Build an end-to-end ML CI/CD pipeline with:
- Multi-stage GitHub Actions workflow (10+ stages)
- Automated data validation with Great Expectations
- Model training, evaluation, and testing
- Docker image building and vulnerability scanning
- GitOps deployment with ArgoCD
- Blue-green and canary deployment strategies
- Automated rollback procedures

**Key Technologies**: GitHub Actions, MLflow, ArgoCD, Kubernetes, Great Expectations, Trivy

**Learning Outcomes**:
- Design multi-stage ML pipelines
- Implement comprehensive testing strategies
- Deploy models with zero downtime
- Automate quality gates and security scanning

**Deliverables**:
- 10+ stage CI/CD pipeline
- 90%+ test coverage
- Automated deployment workflows
- Rollback automation

---

### Project 2: Production Model Monitoring & Drift Detection (120 hours)
**Complexity**: Advanced | **Prerequisites**: Statistics, time series analysis

Create a production-grade monitoring system with:
- Data drift detection (KS test, PSI, Chi-square)
- Concept drift detection and performance tracking
- Real-time alerting with PagerDuty, Slack, email
- 5+ Grafana dashboards for visualization
- Automated retraining triggers
- Comprehensive audit logging

**Key Technologies**: Evidently AI, Prometheus, Grafana, PagerDuty, Slack API, PostgreSQL, Redis

**Learning Outcomes**:
- Implement statistical drift detection
- Build real-time monitoring systems
- Create actionable alerting workflows
- Design automated remediation strategies

**Deliverables**:
- Drift detection pipeline with <1% false positive rate
- 5+ monitoring dashboards
- Multi-channel alerting system
- Automated retraining triggers

---

### Project 3: Data Validation Framework (80 hours)
**Complexity**: Intermediate+ | **Prerequisites**: Data engineering, SQL

Build an enterprise data validation framework with:
- Schema validation and enforcement
- Statistical validation (distributions, ranges)
- Great Expectations integration
- Custom validators for domain logic
- Data quality scoring (0-100)
- Quality gates in CI/CD pipelines

**Key Technologies**: Great Expectations, Pandera, pandas, Pydantic, PostgreSQL

**Learning Outcomes**:
- Design comprehensive validation frameworks
- Implement data contracts
- Build extensible validator architectures
- Create quality scoring systems

**Deliverables**:
- 50+ validation expectations
- Custom validator framework
- Data quality dashboards
- CI/CD integration with quality gates

---

### Project 4: Automated Retraining & A/B Testing (140 hours)
**Complexity**: Expert | **Prerequisites**: Statistics, workflow orchestration

Implement intelligent model lifecycle automation with:
- Multi-trigger retraining system (drift, performance, schedule)
- Complete Airflow/Kubeflow retraining workflow
- Statistical A/B testing framework
- Progressive rollout (10% → 25% → 50% → 100%)
- Experiment tracking and decision automation
- Traffic splitting with Istio

**Key Technologies**: Airflow, Kubeflow, MLflow, Istio, scipy, statsmodels, Kubernetes

**Learning Outcomes**:
- Design automated retraining pipelines
- Implement rigorous A/B testing
- Build progressive deployment systems
- Create statistical decision engines

**Deliverables**:
- Intelligent trigger system
- Complete retraining pipeline
- A/B testing framework with 80% power
- Progressive rollout automation

---

### Project 5: Model Governance & Compliance System (120 hours)
**Complexity**: Expert | **Prerequisites**: ML ethics, compliance basics

Build an enterprise governance platform with:
- Multi-stage approval workflows (technical, fairness, business, compliance)
- Fairness assessment with Fairlearn (10+ metrics)
- Automated model card generation
- Tamper-proof audit logging with Merkle trees
- GDPR/CCPA compliance reporting
- Data lineage tracking

**Key Technologies**: Fairlearn, SHAP, Apache Airflow, PostgreSQL, ELK Stack, Jinja2

**Learning Outcomes**:
- Design approval workflow systems
- Implement bias detection and mitigation
- Build comprehensive audit trails
- Create compliance reporting systems

**Deliverables**:
- 4-stage approval workflow
- Fairness assessment pipeline
- Automated model cards
- Compliance report generator

## Technology Stack

### Core MLOps Tools
- **Orchestration**: Apache Airflow, Kubeflow Pipelines, ArgoCD
- **ML Platforms**: MLflow, Weights & Biases
- **Monitoring**: Prometheus, Grafana, Evidently AI
- **Validation**: Great Expectations, Pandera
- **Infrastructure**: Kubernetes, Docker, Helm, Istio

### Programming & Frameworks
- **Languages**: Python 3.9+, SQL, Bash, YAML
- **Web**: FastAPI, Flask
- **Testing**: pytest, coverage.py, locust
- **CI/CD**: GitHub Actions, GitLab CI

### Data & Storage
- **Databases**: PostgreSQL, MongoDB, Redis
- **Object Storage**: S3, MinIO
- **Time Series**: Prometheus, InfluxDB
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)

### Statistics & ML
- **Statistical Testing**: scipy, statsmodels, pingouin
- **Fairness**: Fairlearn, AIF360
- **Explainability**: SHAP, LIME, InterpretML
- **Drift Detection**: alibi-detect, deepchecks

## Getting Started

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/ai-infra-curriculum/ai-infra-mlops-learning.git
cd ai-infra-mlops-learning

# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import mlflow, great_expectations, evidently; print('Setup successful!')"
```

### 2. Start with Foundations

Begin with the foundational lessons before diving into projects:

```bash
# Navigate to first lesson
cd lessons/mod-001-mlops-foundations

# Read the lesson plan
cat README.md

# Work through exercises
jupyter notebook exercises/
```

### 3. Tackle Projects Sequentially

Projects build upon each other - complete them in order:

1. **Project 1**: CI/CD Pipeline (establishes deployment foundation)
2. **Project 2**: Monitoring (adds observability layer)
3. **Project 3**: Data Quality (ensures data reliability)
4. **Project 4**: Retraining (implements automation)
5. **Project 5**: Governance (adds compliance layer)

### 4. Use the Assessment System

Track your progress with built-in assessments:

```bash
# Complete quizzes after each lesson
cd assessments/quizzes
python quiz_runner.py --lesson 01

# Take practical exams after projects
cd assessments/practical-exams
python exam_runner.py --project 01
```

## Learning Path

### Months 1-2: Foundations & CI/CD
- **Weeks 1-2**: MLOps foundations, concepts, tools
- **Weeks 3-6**: Project 1 - ML CI/CD Pipeline
- **Weeks 7-8**: CI/CD deep dive, advanced patterns

### Months 3-4: Monitoring & Quality
- **Weeks 9-12**: Project 2 - Model Monitoring
- **Weeks 13-14**: Data quality frameworks
- **Weeks 15-16**: Project 3 - Data Validation

### Months 5-6: Automation & Governance
- **Weeks 17-21**: Project 4 - Automated Retraining & A/B Testing
- **Weeks 22-25**: Project 5 - Governance & Compliance
- **Week 26**: Final assessments, certification prep

## Assessment & Certification

### Project Grading (100 points each)

Each project is evaluated on:
- **Technical Implementation** (40-50 points): Functionality, completeness, best practices
- **Code Quality** (15-25 points): Code organization, testing, documentation
- **Performance** (10-15 points): Efficiency, scalability, optimization
- **Documentation** (10 points): README, API docs, runbooks

### Passing Criteria
- Minimum 70/100 per project to pass
- All 5 projects must be completed
- Final practical exam: 80/100 minimum

### Certification
Upon successful completion:
- **Certificate**: MLOps Engineer - AI Infrastructure Career Path
- **Badge**: Digital credential for LinkedIn/resume
- **Portfolio**: 5 production-ready MLOps projects

## Support & Community

### Getting Help

- **GitHub Discussions**: Ask questions, share insights
- **Discord Server**: Real-time community chat (link in community/discussions.md)
- **Office Hours**: Weekly live Q&A sessions
- **Mentorship**: Connect with experienced MLOps engineers

### Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Code of Conduct

Please read our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before participating.

## Resources

### Recommended Books
- "Introducing MLOps" by Mark Treveil et al.
- "Practical MLOps" by Noah Gift & Alfredo Deza
- "Machine Learning Design Patterns" by Lakshmanan, Robinson, Munn
- "Designing Data-Intensive Applications" by Martin Kleppmann

### Online Courses
- [MLOps Specialization (Coursera)](https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops)
- [Full Stack Deep Learning](https://fullstackdeeplearning.com/)
- [Made With ML - MLOps](https://madewithml.com/)

### Documentation
- [MLflow Documentation](https://mlflow.org/docs/latest/)
- [Kubeflow Documentation](https://www.kubeflow.org/docs/)
- [Great Expectations Docs](https://docs.greatexpectations.io/)
- [Evidently AI Docs](https://docs.evidentlyai.com/)

### Blogs & Newsletters
- [Chip Huyen's Blog](https://huyenchip.com/blog/)
- [Eugene Yan's Blog](https://eugeneyan.com/)
- [MLOps Community](https://mlops.community/)
- [The Batch (deeplearning.ai)](https://www.deeplearning.ai/the-batch/)

## Career Progression

### After MLOps Engineer

Upon completing this curriculum, you can advance to:

**Parallel Specializations** (Same Level):
- ML Platform Engineer (Level 2.5A)
- AI Infrastructure Security Engineer (Level 2.5C)
- AI/ML Performance Engineer (Level 2.5D)

**Architecture Track** (Next Level):
- AI Infrastructure Architect (Level 3)
- Senior AI Infrastructure Architect (Level 3.5)

**Leadership Track**:
- Principal AI Infrastructure Engineer (Level 4 - IC)
- AI Infrastructure Team Lead (Level 4 - Manager)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- **Email**: ai-infra-curriculum@joshua-ferguson.com
- **GitHub Org**: [@ai-infra-curriculum](https://github.com/ai-infra-curriculum)
- **Discussions**: [GitHub Discussions](https://github.com/ai-infra-curriculum/ai-infra-mlops-learning/discussions) is the supported community surface today.

## Acknowledgments

This curriculum is part of the **AI Infrastructure Career Path** project, designed to provide comprehensive, hands-on training for AI infrastructure roles from entry-level to principal/executive positions.

Special thanks to:
- The MLOps community for sharing best practices
- Contributors who reviewed and improved this curriculum
- Open-source tool maintainers whose work makes MLOps possible

---

**Ready to become an MLOps Engineer?** Start with [Lesson 1: MLOps Foundations](lessons/mod-001-mlops-foundations/) and build your path to production ML mastery!

Last Updated: October 2025


---

<!-- aicg:maintained-by -->
Maintained by [VeriSwarm.ai](https://veriswarm.ai)
