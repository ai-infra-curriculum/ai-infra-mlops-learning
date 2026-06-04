# System Architecture

## 1. Overview

This document describes the architecture of the End-to-End ML Pipeline for customer churn prediction. The system follows MLOps best practices and implements a modular, scalable design.

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Data Sources                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │   CSV    │  │   DB     │  │   API    │  │  Kafka   │           │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘           │
└───────┼─────────────┼─────────────┼─────────────┼──────────────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                      │
        ┌─────────────▼─────────────┐
        │   Data Ingestion Layer    │
        │  - Multi-source connectors │
        │  - Data normalization      │
        │  - Schema detection        │
        └─────────────┬──────────────┘
                      │
        ┌─────────────▼──────────────┐
        │  Data Validation Layer     │
        │  - Great Expectations      │
        │  - Quality checks          │
        │  - Anomaly detection       │
        └─────────────┬──────────────┘
                      │
        ┌─────────────▼──────────────┐
        │  Feature Engineering       │
        │  - Feature generation      │
        │  - Feature validation      │
        │  - Feature store           │
        └─────────────┬──────────────┘
                      │
        ┌─────────────▼──────────────┐
        │   Model Training Layer     │
        │  - Multiple algorithms     │
        │  - Hyperparameter tuning   │
        │  - Experiment tracking     │
        └─────────────┬──────────────┘
                      │
        ┌─────────────▼──────────────┐
        │    Model Registry          │
        │  - Version management      │
        │  - Model metadata          │
        │  - Lifecycle management    │
        └─────────────┬──────────────┘
                      │
        ┌─────────────▼──────────────┐
        │   Model Serving Layer      │
        │  - REST API (FastAPI)      │
        │  - Batch predictions       │
        │  - A/B testing support     │
        └─────────────┬──────────────┘
                      │
        ┌─────────────▼──────────────┐
        │   Monitoring Layer         │
        │  - Data drift detection    │
        │  - Model drift detection   │
        │  - Performance metrics     │
        └────────────────────────────┘
```

## 3. Component Architecture

### 3.1 Data Ingestion Layer

**Purpose**: Collect and normalize data from multiple sources.

**Components**:

```python
DataIngestion
├── CSVConnector
│   ├── S3Reader
│   └── LocalFileReader
├── DatabaseConnector
│   ├── PostgreSQLReader
│   └── ConnectionPool
├── APIConnector
│   ├── RESTClient
│   └── RetryHandler
└── StreamConnector
    ├── KafkaConsumer
    └── EventProcessor
```

**Design Decisions**:
- **Pluggable connectors**: Each data source has its own connector class
- **Connection pooling**: Reuse database connections for efficiency
- **Retry logic**: Exponential backoff for transient failures
- **Incremental loading**: Track watermarks to load only new data
- **Schema inference**: Automatically detect data schemas

**Data Flow**:
1. Connector reads data from source
2. Data normalized to common schema
3. Metadata captured (timestamp, source, row count)
4. Data written to staging area
5. Ingestion logged to MLflow

### 3.2 Data Validation Layer

**Purpose**: Ensure data quality before processing.

**Components**:

```python
DataValidation
├── SchemaValidator
│   ├── ColumnChecker
│   ├── TypeChecker
│   └── StructureValidator
├── QualityValidator
│   ├── CompletenessChecker
│   ├── UniquenessChecker
│   ├── RangeValidator
│   └── ConsistencyChecker
├── StatisticalValidator
│   ├── DistributionChecker
│   ├── OutlierDetector
│   └── DriftDetector
└── ReportGenerator
    ├── HTMLReporter
    └── MetricsExporter
```

**Great Expectations Suite Structure**:

```yaml
expectations:
  # Schema expectations
  - expect_table_columns_to_match_ordered_list
  - expect_column_values_to_be_of_type

  # Completeness expectations
  - expect_column_values_to_not_be_null
  - expect_table_row_count_to_be_between

  # Value expectations
  - expect_column_values_to_be_between
  - expect_column_values_to_be_in_set

  # Statistical expectations
  - expect_column_mean_to_be_between
  - expect_column_stdev_to_be_between
  - expect_column_kl_divergence_to_be_less_than
```

**Design Decisions**:
- **Fail-fast approach**: Block pipeline on critical failures
- **Detailed reporting**: Generate HTML reports for manual review
- **Historical tracking**: Compare current data to historical baselines
- **Configurable thresholds**: Allow tuning of validation rules
- **Integration with MLflow**: Log validation results as artifacts

### 3.3 Feature Engineering Layer

**Purpose**: Transform raw data into model-ready features.

**Architecture**:

```python
FeatureEngineering
├── FeatureGenerator
│   ├── BasicTransformers
│   │   ├── Normalizer
│   │   ├── OneHotEncoder
│   │   └── MissingValueHandler
│   ├── DerivedFeatures
│   │   ├── ServiceCounter
│   │   ├── ChargeCalculator
│   │   └── TenureGrouper
│   ├── TimeBasedFeatures
│   │   ├── DaysSinceCalculator
│   │   ├── TrendAnalyzer
│   │   └── SeasonalityExtractor
│   └── AggregationFeatures
│       ├── RollingAggregator
│       ├── WindowFunctions
│       └── CohortComparator
├── FeatureValidator
│   ├── TypeChecker
│   ├── RangeValidator
│   └── DistributionChecker
├── FeatureStore
│   ├── FeatureWriter
│   ├── FeatureReader
│   └── VersionManager
└── FeatureMetadata
    ├── LineageTracker
    ├── DocumentationGenerator
    └── StatisticsCollector
```

**Feature Store Schema**:

```sql
-- Feature definitions
CREATE TABLE feature_definitions (
    feature_id UUID PRIMARY KEY,
    feature_name VARCHAR(255) UNIQUE,
    feature_type VARCHAR(50),
    description TEXT,
    creation_logic TEXT,
    created_at TIMESTAMP,
    version INTEGER
);

-- Feature values (point-in-time)
CREATE TABLE feature_values (
    customer_id VARCHAR(255),
    feature_id UUID,
    feature_value JSONB,
    valid_from TIMESTAMP,
    valid_to TIMESTAMP,
    created_at TIMESTAMP,
    PRIMARY KEY (customer_id, feature_id, valid_from)
);

-- Feature statistics
CREATE TABLE feature_statistics (
    feature_id UUID,
    date DATE,
    mean FLOAT,
    std FLOAT,
    min FLOAT,
    max FLOAT,
    missing_rate FLOAT,
    PRIMARY KEY (feature_id, date)
);
```

**Design Decisions**:
- **Versioned features**: Track feature evolution over time
- **Point-in-time correctness**: Avoid data leakage with temporal consistency
- **Feature reuse**: Shared features between training and serving
- **Automated documentation**: Generate feature catalog from code
- **Scalable storage**: Partition features by customer and time

### 3.4 Model Training Layer

**Purpose**: Train, evaluate, and optimize ML models.

**Architecture**:

```python
ModelTraining
├── DataLoader
│   ├── TrainingDataset
│   ├── ValidationDataset
│   └── TestDataset
├── ModelFactory
│   ├── LogisticRegressionModel
│   ├── RandomForestModel
│   ├── XGBoostModel
│   └── LightGBMModel
├── HyperparameterOptimizer
│   ├── OptunaOptimizer
│   ├── SearchSpace
│   └── ObjectiveFunction
├── ModelEvaluator
│   ├── MetricsCalculator
│   ├── CurveGenerator
│   └── FeatureImportanceAnalyzer
├── ExperimentTracker
│   ├── MLflowLogger
│   ├── ArtifactSaver
│   └── RunManager
└── ModelRegistry
    ├── ModelVersioner
    ├── StageManager
    └── MetadataStore
```

**MLflow Tracking Structure**:

```
MLflow
├── Experiments
│   ├── churn-prediction-baseline
│   ├── churn-prediction-rf
│   ├── churn-prediction-xgboost
│   └── churn-prediction-ensemble
├── Runs
│   ├── run_id
│   │   ├── params/
│   │   │   ├── model_type
│   │   │   ├── hyperparameters
│   │   │   └── feature_version
│   │   ├── metrics/
│   │   │   ├── accuracy
│   │   │   ├── auc_roc
│   │   │   ├── f1_score
│   │   │   └── training_time
│   │   └── artifacts/
│   │       ├── model.pkl
│   │       ├── feature_importance.png
│   │       ├── confusion_matrix.png
│   │       └── validation_report.html
└── Models
    ├── churn-predictor
    │   ├── version-1 (None)
    │   ├── version-2 (Staging)
    │   └── version-3 (Production)
```

**Training Pipeline Flow**:

```
1. Load training data
   ├── Retrieve features from feature store
   ├── Split into train/val/test
   └── Create data loaders

2. Initialize model
   ├── Select model type
   ├── Set initial hyperparameters
   └── Configure training settings

3. Hyperparameter optimization
   ├── Define search space
   ├── Run Optuna trials (100+ iterations)
   ├── Track each trial in MLflow
   └── Select best parameters

4. Train final model
   ├── Use best hyperparameters
   ├── Train on full training set
   ├── Log progress metrics
   └── Save checkpoints

5. Evaluate model
   ├── Calculate metrics on test set
   ├── Generate evaluation plots
   ├── Analyze feature importance
   └── Create evaluation report

6. Register model
   ├── Save model artifacts
   ├── Register in MLflow registry
   ├── Tag with metadata
   └── Set stage to None
```

**Design Decisions**:
- **Experiment tracking**: Every run logged to MLflow for reproducibility
- **Hyperparameter optimization**: Automated tuning with Optuna
- **Cross-validation**: Stratified k-fold to ensure robust evaluation
- **Model comparison**: Easy comparison of different algorithms
- **Artifact management**: Centralized storage of models and plots

### 3.5 Model Serving Layer

**Purpose**: Provide predictions via API and batch processes.

**API Architecture**:

```python
ModelServing
├── APIServer (FastAPI)
│   ├── Routers
│   │   ├── PredictionRouter
│   │   ├── HealthRouter
│   │   └── MetricsRouter
│   ├── Middleware
│   │   ├── AuthenticationMiddleware
│   │   ├── RateLimitingMiddleware
│   │   └── LoggingMiddleware
│   ├── Models (Pydantic)
│   │   ├── PredictionRequest
│   │   ├── PredictionResponse
│   │   └── BatchRequest
│   └── Dependencies
│       ├── ModelLoader
│       └── FeatureService
├── ModelLoader
│   ├── MLflowLoader
│   ├── ModelCache
│   └── VersionManager
├── FeatureService
│   ├── FeatureRetriever
│   ├── FeatureValidator
│   └── FeatureCache
├── PredictionService
│   ├── Predictor
│   ├── PostProcessor
│   └── ConfidenceCalculator
└── BatchPredictor
    ├── DataLoader
    ├── ParallelProcessor
    └── ResultWriter
```

**API Endpoints**:

```python
# Single prediction
POST /predict
{
    "customer_id": "C12345",
    "features": {
        "age": 45,
        "tenure_months": 24,
        "monthly_charges": 79.99,
        # ... other features
    }
}

Response:
{
    "customer_id": "C12345",
    "churn_probability": 0.73,
    "prediction": "churn",
    "confidence": "high",
    "model_version": "v3",
    "timestamp": "2025-10-26T10:30:00Z"
}

# Batch prediction
POST /predict/batch
{
    "customers": [
        {"customer_id": "C1", "features": {...}},
        {"customer_id": "C2", "features": {...}}
    ]
}

# Health check
GET /health
{
    "status": "healthy",
    "model_loaded": true,
    "model_version": "v3",
    "uptime_seconds": 3600
}

# Metrics
GET /metrics
# Prometheus format metrics
```

**Design Decisions**:
- **FastAPI framework**: Automatic validation, async support, OpenAPI docs
- **Model caching**: Load model once, reuse for predictions
- **Feature caching**: Cache frequently used features (Redis)
- **Request validation**: Pydantic models ensure data quality
- **Rate limiting**: Prevent API abuse
- **Graceful degradation**: Return partial results on failures

### 3.6 Monitoring Layer

**Purpose**: Detect drift and monitor system health.

**Architecture**:

```python
Monitoring
├── DriftDetection
│   ├── DataDriftDetector
│   │   ├── KSTest (numerical)
│   │   ├── ChiSquareTest (categorical)
│   │   └── PSICalculator
│   ├── ModelDriftDetector
│   │   ├── PredictionDistributionMonitor
│   │   ├── ConfidenceAnalyzer
│   │   └── PerformanceMonitor
│   └── DriftReporter
│       ├── AlertGenerator
│       └── DashboardUpdater
├── PerformanceMonitoring
│   ├── MetricsCollector
│   │   ├── LatencyMetrics
│   │   ├── ThroughputMetrics
│   │   └── ErrorMetrics
│   ├── ResourceMonitoring
│   │   ├── CPUMonitor
│   │   ├── MemoryMonitor
│   │   └── DiskMonitor
│   └── PrometheusExporter
├── LoggingSystem
│   ├── StructuredLogger
│   ├── LogAggregator
│   └── LogAnalyzer
└── AlertingSystem
    ├── AlertManager
    ├── NotificationService
    └── EscalationPolicy
```

**Drift Detection Workflow**:

```
1. Collect baseline data
   ├── Store feature distributions from training
   ├── Calculate reference statistics
   └── Save to drift baseline store

2. Monitor production data
   ├── Collect features from predictions
   ├── Aggregate over time windows (hourly/daily)
   └── Store in monitoring database

3. Detect drift
   ├── Compare current vs. baseline distributions
   ├── Run statistical tests
   ├── Calculate drift scores
   └── Identify drifted features

4. Generate alerts
   ├── Check drift thresholds
   ├── Create alert if threshold exceeded
   ├── Send notifications
   └── Log drift event

5. Trigger actions
   ├── Flag for review
   ├── Trigger model retraining
   └── Update dashboards
```

**Prometheus Metrics**:

```python
# API metrics
api_requests_total = Counter('api_requests_total', 'Total API requests')
api_request_duration = Histogram('api_request_duration_seconds', 'Request duration')
api_errors_total = Counter('api_errors_total', 'Total API errors')

# Prediction metrics
predictions_total = Counter('predictions_total', 'Total predictions')
prediction_churn_rate = Gauge('prediction_churn_rate', 'Current churn prediction rate')
prediction_confidence = Histogram('prediction_confidence', 'Prediction confidence distribution')

# Model metrics
model_load_time = Gauge('model_load_time_seconds', 'Model loading time')
model_inference_time = Histogram('model_inference_time_seconds', 'Model inference time')

# Drift metrics
feature_drift_score = Gauge('feature_drift_score', 'Drift score by feature', ['feature_name'])
drift_alerts_total = Counter('drift_alerts_total', 'Total drift alerts')

# Resource metrics
cpu_usage = Gauge('cpu_usage_percent', 'CPU usage percentage')
memory_usage = Gauge('memory_usage_bytes', 'Memory usage in bytes')
```

**Design Decisions**:
- **Statistical rigor**: Multiple tests for robust drift detection
- **Automated alerting**: Proactive notification of issues
- **Comprehensive metrics**: Track all aspects of system health
- **Historical tracking**: Store metrics for trend analysis
- **Actionable insights**: Link monitoring to remediation

## 4. Orchestration Architecture

### 4.1 Airflow DAG Design

**Training Pipeline DAG**:

```python
with DAG('training_pipeline', schedule='@daily') as dag:

    # Data tasks
    ingest_data = PythonOperator(task_id='ingest_data')
    validate_data = PythonOperator(task_id='validate_data')

    # Feature tasks
    engineer_features = PythonOperator(task_id='engineer_features')
    validate_features = PythonOperator(task_id='validate_features')

    # Model tasks
    train_model = PythonOperator(task_id='train_model')
    evaluate_model = PythonOperator(task_id='evaluate_model')

    # Deployment tasks
    register_model = PythonOperator(task_id='register_model')
    promote_to_staging = PythonOperator(task_id='promote_to_staging')

    # Notification
    notify_completion = PythonOperator(task_id='notify_completion')

    # Dependencies
    ingest_data >> validate_data >> engineer_features >> validate_features
    validate_features >> train_model >> evaluate_model
    evaluate_model >> register_model >> promote_to_staging >> notify_completion
```

**Design Decisions**:
- **Daily training**: Regular model updates with fresh data
- **Task isolation**: Each task is idempotent and independently retryable
- **Conditional logic**: Skip downstream tasks on validation failures
- **Parallel execution**: Run independent tasks concurrently
- **Error handling**: Automatic retries with exponential backoff

## 5. Infrastructure Architecture

### 5.1 Kubernetes Deployment

```yaml
# Deployment Architecture
┌─────────────────────────────────────────┐
│         Kubernetes Cluster              │
│                                         │
│  ┌────────────────────────────────┐   │
│  │     Ingress Controller         │   │
│  │  (Load Balancing & Routing)    │   │
│  └────────┬───────────────────────┘   │
│           │                             │
│  ┌────────▼───────────────────────┐   │
│  │    API Service (ClusterIP)     │   │
│  └────────┬───────────────────────┘   │
│           │                             │
│  ┌────────▼───────────────────────┐   │
│  │   API Deployment (2-10 pods)   │   │
│  │  - Model serving containers     │   │
│  │  - Resource limits set          │   │
│  │  - Health checks configured     │   │
│  │  - HPA enabled                  │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   ConfigMaps & Secrets          │   │
│  │  - Application config           │   │
│  │  - Database credentials         │   │
│  │  - MLflow server URL            │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   PersistentVolumes             │   │
│  │  - Model storage                │   │
│  │  - Cache storage                │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**Resource Allocation**:

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "2000m"

autoscaling:
  minReplicas: 2
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
```

### 5.2 Local Development (Docker Compose)

```yaml
services:
  postgres:
    - Port: 5432
    - Volume: postgres_data
    - Health check enabled

  mlflow:
    - Port: 5000
    - Depends on: postgres
    - Volume: mlflow_artifacts

  airflow-webserver:
    - Port: 8080
    - Depends on: postgres, redis

  airflow-scheduler:
    - Depends on: postgres, redis

  api:
    - Port: 8000
    - Depends on: mlflow, postgres

  prometheus:
    - Port: 9090
    - Volume: prometheus_data

  grafana:
    - Port: 3000
    - Depends on: prometheus
```

## 6. Data Flow Diagrams

### 6.1 Training Flow

```
[Raw Data] → [Ingestion] → [Validation] → [Feature Engineering]
                                                    ↓
[Model Registry] ← [Model Registration] ← [Training] ← [Feature Store]
        ↓
[Staging] → [Validation] → [Production]
```

### 6.2 Inference Flow

```
[API Request] → [Feature Retrieval] → [Model Prediction] → [Response]
                        ↑                      ↓
                [Feature Store]        [Monitoring]
```

### 6.3 Monitoring Flow

```
[Predictions] → [Data Collection] → [Drift Detection] → [Alert/Action]
                                            ↓
                                    [Dashboard Update]
```

## 7. Design Decisions & Rationale

### 7.1 Technology Choices

| Decision | Rationale |
|----------|-----------|
| **Great Expectations** | Industry standard for data validation, extensive expectation library |
| **MLflow** | Unified platform for experiment tracking and model registry |
| **Optuna** | Efficient Bayesian optimization, better than grid search |
| **FastAPI** | Modern, fast, automatic validation and documentation |
| **Airflow** | Robust orchestration, good for complex DAGs |
| **Prometheus/Grafana** | De facto standard for monitoring in Kubernetes |
| **PostgreSQL** | Reliable, ACID compliant, good for feature store |
| **Kubernetes** | Industry standard for container orchestration |

### 7.2 Architectural Patterns

**Microservices Architecture**:
- Each component is independently deployable
- Loose coupling via APIs
- Scalable components independently

**Event-Driven Architecture**:
- Kafka for real-time data ingestion
- Asynchronous processing where possible
- Decoupled producers and consumers

**Layered Architecture**:
- Clear separation of concerns
- Each layer has specific responsibility
- Well-defined interfaces between layers

### 7.3 Scalability Considerations

1. **Horizontal Scaling**
   - API pods auto-scale based on load
   - Batch processing partitioned across workers
   - Database read replicas for query scaling

2. **Caching Strategy**
   - Redis for feature caching
   - Model loaded once per pod
   - API response caching for repeated requests

3. **Data Partitioning**
   - Feature store partitioned by customer ID
   - Time-based partitioning for historical data
   - Separate storage for hot and cold data

### 7.4 Security Design

1. **Authentication & Authorization**
   - API key authentication for API access
   - Role-based access control (RBAC)
   - Service accounts for inter-service communication

2. **Data Protection**
   - Encryption at rest (database, storage)
   - Encryption in transit (TLS)
   - PII data masking in logs

3. **Secret Management**
   - Kubernetes secrets for credentials
   - Environment variable injection
   - No secrets in code or containers

## 8. Future Enhancements

1. **Advanced Features**
   - Real-time feature computation
   - Online learning capabilities
   - Multi-model ensembles

2. **Infrastructure**
   - Multi-region deployment
   - Blue-green deployments
   - Canary releases

3. **Monitoring**
   - Explainability monitoring (SHAP values)
   - Fairness metrics tracking
   - Automated model retraining triggers

4. **Data**
   - Streaming feature engineering
   - Feature discovery automation
   - Automated feature selection
