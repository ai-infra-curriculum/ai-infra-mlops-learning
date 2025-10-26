# Project 1: End-to-End ML Pipeline

## Overview

This project implements a production-ready, end-to-end machine learning pipeline for a customer churn prediction system. The system demonstrates best practices in MLOps, including automated data validation, feature engineering, model training with hyperparameter optimization, model serving, and real-time drift detection.

## Business Scenario

**Context**: A telecommunications company wants to predict customer churn to proactively engage at-risk customers and reduce revenue loss.

**Problem Statement**: Build a scalable ML pipeline that:
- Ingests customer data from multiple sources
- Validates data quality and detects anomalies
- Engineers features for model training
- Trains and optimizes churn prediction models
- Deploys models to production with monitoring
- Detects data and model drift in real-time

**Success Metrics**:
- Model AUC-ROC > 0.85
- Prediction latency < 100ms (p95)
- Data validation coverage > 95%
- Drift detection within 1 hour
- Pipeline orchestration with 99.5% reliability

## Learning Objectives

By completing this project, you will:

1. **Data Engineering**
   - Implement robust data ingestion from multiple sources
   - Build comprehensive data validation with Great Expectations
   - Handle data quality issues and schema evolution

2. **Feature Engineering**
   - Design and implement scalable feature pipelines
   - Create time-based and aggregation features
   - Implement feature versioning and lineage tracking

3. **Model Development**
   - Build training pipelines with MLflow tracking
   - Implement hyperparameter optimization (Optuna/Ray Tune)
   - Version models and manage model registry

4. **ML Operations**
   - Orchestrate pipelines with Apache Airflow
   - Containerize ML workloads with Docker
   - Deploy models on Kubernetes

5. **Monitoring & Observability**
   - Implement data drift detection
   - Monitor model performance metrics
   - Set up alerting with Prometheus and Grafana

6. **CI/CD for ML**
   - Automate testing (unit, integration, E2E)
   - Build CI/CD pipelines for ML code
   - Implement automated model validation

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Data Validation | Great Expectations | Schema validation, data quality checks |
| Experiment Tracking | MLflow | Track experiments, model versioning |
| Orchestration | Apache Airflow | Pipeline scheduling and dependency management |
| Model Training | Scikit-learn, XGBoost | Churn prediction models |
| Hyperparameter Optimization | Optuna | Automated hyperparameter tuning |
| Model Serving | FastAPI | REST API for predictions |
| Monitoring | Prometheus + Grafana | Metrics collection and visualization |
| Drift Detection | Evidently AI | Data and model drift detection |
| Containerization | Docker | Package applications |
| Orchestration | Kubernetes | Container orchestration |
| CI/CD | GitHub Actions | Automated testing and deployment |

## Project Structure

```
project-1-ml-pipeline/
├── src/                    # Source code
│   ├── data/              # Data ingestion and validation
│   ├── features/          # Feature engineering
│   ├── models/            # Model training and prediction
│   ├── monitoring/        # Drift detection and monitoring
│   └── api/               # Model serving API
├── tests/                 # Test suites
├── infrastructure/        # Docker and Kubernetes configs
├── airflow/              # Airflow DAGs
├── config/               # Configuration files
└── docs/                 # Additional documentation
```

## Quick Start

See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed setup instructions.

```bash
# Clone and navigate to project
cd project-1-ml-pipeline

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env

# Start services with Docker Compose
docker-compose up -d

# Run the training pipeline
make train

# Start the API server
make serve
```

## Key Features

### 1. Automated Data Pipeline
- **Multi-source ingestion**: CSV, databases, APIs
- **Schema validation**: Automatic schema detection and validation
- **Data quality checks**: Completeness, uniqueness, value ranges
- **Anomaly detection**: Statistical outlier detection

### 2. Feature Engineering
- **Automated feature generation**: Time-based, aggregations, interactions
- **Feature store integration**: Centralized feature management
- **Feature validation**: Type checking, range validation
- **Feature versioning**: Track feature evolution

### 3. Model Training
- **Experiment tracking**: Log all experiments with MLflow
- **Hyperparameter optimization**: Automated tuning with Optuna
- **Model evaluation**: Comprehensive metrics and validation
- **Model registry**: Version control for models

### 4. Model Serving
- **REST API**: FastAPI-based prediction service
- **Batch predictions**: Scheduled batch inference
- **Model versioning**: A/B testing support
- **Performance optimization**: Caching, async processing

### 5. Monitoring & Alerting
- **Data drift detection**: Monitor feature distributions
- **Model drift detection**: Track prediction quality
- **Performance metrics**: Latency, throughput, error rates
- **Alerting**: Automated notifications for issues

### 6. Infrastructure as Code
- **Docker containers**: Reproducible environments
- **Kubernetes deployment**: Scalable model serving
- **CI/CD pipelines**: Automated testing and deployment
- **Infrastructure monitoring**: Resource utilization tracking

## Implementation Phases

### Phase 1: Data Foundation (Week 1)
- Set up data ingestion pipeline
- Implement Great Expectations validation
- Create basic feature engineering

### Phase 2: Model Development (Week 2)
- Build training pipeline with MLflow
- Implement hyperparameter optimization
- Set up model registry

### Phase 3: Deployment (Week 3)
- Containerize applications
- Deploy on Kubernetes
- Set up model serving API

### Phase 4: Monitoring (Week 4)
- Implement drift detection
- Set up Prometheus metrics
- Configure Grafana dashboards

### Phase 5: Automation (Week 5)
- Build Airflow DAGs
- Set up CI/CD pipelines
- Implement automated retraining

## Documentation

- [REQUIREMENTS.md](REQUIREMENTS.md) - Detailed technical requirements
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture and design
- [GETTING_STARTED.md](GETTING_STARTED.md) - Setup and development guide
- [VALIDATION.md](VALIDATION.md) - Testing and validation strategy

## Assessment Criteria

Your implementation will be evaluated on:

1. **Code Quality** (25%)
   - Clean, readable, well-documented code
   - Proper error handling and logging
   - Type hints and docstrings

2. **Functionality** (30%)
   - All components working as specified
   - Meets performance requirements
   - Handles edge cases

3. **MLOps Practices** (25%)
   - Proper experiment tracking
   - Model versioning and registry
   - Comprehensive monitoring

4. **Infrastructure** (10%)
   - Docker containers properly configured
   - Kubernetes deployment working
   - CI/CD pipeline functional

5. **Testing** (10%)
   - Unit test coverage > 80%
   - Integration tests for pipelines
   - E2E tests for critical paths

## Resources

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Great Expectations Guide](https://docs.greatexpectations.io/)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

## Support

For questions or issues:
1. Check the documentation files
2. Review the TODO comments in stub files
3. Consult the technology-specific documentation
4. Reach out to instructors or mentors

## License

This project is part of the AI Infrastructure curriculum and is for educational purposes.
