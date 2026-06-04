# Getting Started Guide

## Prerequisites

### Required Software

1. **Python 3.9+**
   ```bash
   python --version  # Should be 3.9 or higher
   ```

2. **Docker & Docker Compose**
   ```bash
   docker --version  # Should be 20.10+
   docker-compose --version  # Should be 1.29+
   ```

3. **kubectl** (for Kubernetes deployment)
   ```bash
   kubectl version --client  # Should be 1.24+
   ```

4. **Git**
   ```bash
   git --version
   ```

### Optional Tools

- **make**: For using Makefile commands
- **Minikube** or **kind**: For local Kubernetes testing
- **AWS CLI**: If using AWS services

### System Requirements

- **RAM**: Minimum 8GB, recommended 16GB
- **Disk Space**: Minimum 20GB free
- **CPU**: Minimum 4 cores recommended

## Quick Start (Local Development)

### 1. Clone and Setup

```bash
# Navigate to project directory
cd /path/to/project-01-ml-pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
nano .env  # or your preferred editor
```

**Required environment variables**:
```bash
# Database
POSTGRES_USER=mlops
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=churn_prediction
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# MLflow
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_ARTIFACT_ROOT=./mlruns

# Airflow
AIRFLOW_HOME=/path/to/project/airflow
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://mlops:password@localhost:5432/airflow

# API
API_HOST=0.0.0.0
API_PORT=8000
MODEL_VERSION=latest

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
```

### 3. Start Services with Docker Compose

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

**Services started**:
- PostgreSQL (port 5432)
- MLflow Server (port 5000)
- Airflow Webserver (port 8080)
- Airflow Scheduler
- Redis (port 6379)
- Prometheus (port 9090)
- Grafana (port 3000)

### 4. Initialize Databases

```bash
# Initialize Airflow database
make airflow-init

# Initialize application database
make db-init
```

### 5. Verify Installation

```bash
# Run health checks
make health-check

# Run tests
make test
```

## Detailed Setup Instructions

### Database Setup

#### 1. PostgreSQL Initialization

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U mlops -d churn_prediction

# Create necessary schemas
CREATE SCHEMA IF NOT EXISTS features;
CREATE SCHEMA IF NOT EXISTS predictions;
CREATE SCHEMA IF NOT EXISTS monitoring;

# Create tables (or run migration script)
\i scripts/init_db.sql
```

#### 2. Sample Data Loading

```bash
# Download sample dataset
make download-sample-data

# Load sample data
python scripts/load_sample_data.py
```

### MLflow Setup

#### 1. Access MLflow UI

Open browser: http://localhost:5000

#### 2. Create Experiments

```bash
# Create experiments via CLI
mlflow experiments create --experiment-name churn-prediction-baseline
mlflow experiments create --experiment-name churn-prediction-xgboost
mlflow experiments create --experiment-name churn-prediction-ensemble
```

Or use the Python API:

```python
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.create_experiment("churn-prediction-baseline")
```

### Airflow Setup

#### 1. Access Airflow UI

Open browser: http://localhost:8080

Default credentials:
- Username: `admin`
- Password: `admin` (change this!)

#### 2. Configure Connections

Go to Admin > Connections and add:

**PostgreSQL Connection**:
- Conn Id: `postgres_default`
- Conn Type: `Postgres`
- Host: `postgres`
- Schema: `churn_prediction`
- Login: `mlops`
- Password: `your_password`
- Port: `5432`

**MLflow Connection**:
- Conn Id: `mlflow_default`
- Conn Type: `HTTP`
- Host: `http://mlflow`
- Port: `5000`

#### 3. Enable DAGs

In Airflow UI, enable the following DAGs:
- `training_pipeline`
- `batch_prediction_pipeline`
- `monitoring_pipeline`

### Monitoring Setup

#### 1. Access Grafana

Open browser: http://localhost:3000

Default credentials:
- Username: `admin`
- Password: `admin` (change on first login)

#### 2. Add Prometheus Data Source

1. Go to Configuration > Data Sources
2. Click "Add data source"
3. Select "Prometheus"
4. URL: `http://prometheus:9090`
5. Click "Save & Test"

#### 3. Import Dashboards

```bash
# Import pre-built dashboards
make import-dashboards
```

Or manually import from `dashboards/` directory.

## Development Workflow

### 1. Data Pipeline Development

```bash
# Run data ingestion
python src/data/ingestion.py

# Run data validation
python src/data/validation.py

# Check validation reports
open great_expectations/uncommitted/data_docs/local_site/index.html
```

### 2. Feature Engineering

```bash
# Generate features
python src/features/engineering.py --input data/raw --output data/processed

# Validate features
python src/features/engineering.py --validate

# Inspect feature store
python scripts/inspect_features.py
```

### 3. Model Training

```bash
# Train baseline model
python src/models/train.py --model logistic

# Train with hyperparameter tuning
python src/models/train.py --model xgboost --optimize --trials 100

# View results in MLflow
open http://localhost:5000
```

### 4. Model Evaluation

```bash
# Evaluate model
python src/models/evaluate.py --model-uri models:/churn-predictor/latest

# Generate evaluation report
python src/models/evaluate.py --model-uri models:/churn-predictor/latest --report
```

### 5. Model Serving

```bash
# Start API server
make serve

# Or manually
uvicorn src.api.serve:app --host 0.0.0.0 --port 8000 --reload

# Test API
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @sample_requests/single_prediction.json

# View API documentation
open http://localhost:8000/docs
```

### 6. Running Tests

```bash
# Run all tests
make test

# Run specific test types
make test-unit
make test-integration
make test-e2e

# Run with coverage
make test-coverage

# View coverage report
open htmlcov/index.html
```

### 7. Code Quality Checks

```bash
# Format code
make format

# Lint code
make lint

# Type checking
make type-check

# Security scanning
make security-check

# Run all checks
make check-all
```

## Makefile Commands

The project includes a Makefile with helpful commands:

```bash
# Setup and installation
make install          # Install dependencies
make install-dev      # Install dev dependencies
make setup            # Complete setup (install + init)

# Development
make train            # Run training pipeline
make serve            # Start API server
make airflow-start    # Start Airflow services
make airflow-stop     # Stop Airflow services

# Testing
make test             # Run all tests
make test-unit        # Run unit tests
make test-integration # Run integration tests
make test-e2e         # Run end-to-end tests
make test-coverage    # Run tests with coverage

# Code quality
make format           # Format code with black
make lint             # Lint with flake8
make type-check       # Type check with mypy
make security-check   # Security scan with bandit

# Docker
make docker-build     # Build Docker images
make docker-up        # Start Docker services
make docker-down      # Stop Docker services
make docker-logs      # View Docker logs

# Database
make db-init          # Initialize database
make db-migrate       # Run migrations
make db-reset         # Reset database

# Cleanup
make clean            # Remove generated files
make clean-pyc        # Remove Python cache files
make clean-test       # Remove test artifacts
```

## Running the Complete Pipeline

### Option 1: Using Airflow (Recommended)

1. Ensure Airflow is running:
   ```bash
   docker-compose up -d airflow-webserver airflow-scheduler
   ```

2. Trigger the training pipeline:
   - Go to http://localhost:8080
   - Find `training_pipeline` DAG
   - Click "Trigger DAG"
   - Monitor progress in the Graph View

### Option 2: Using Make Commands

```bash
# Run complete training pipeline
make pipeline-train

# Run batch prediction
make pipeline-predict

# Run monitoring
make pipeline-monitor
```

### Option 3: Manual Execution

```bash
# Step 1: Ingest data
python src/data/ingestion.py --source csv --path data/raw/customers.csv

# Step 2: Validate data
python src/data/validation.py --input data/staging/customers.parquet

# Step 3: Engineer features
python src/features/engineering.py --input data/staging --output data/processed

# Step 4: Train model
python src/models/train.py --config config/training_config.yaml

# Step 5: Evaluate model
python src/models/evaluate.py --run-id <mlflow_run_id>

# Step 6: Register model
python scripts/register_model.py --run-id <mlflow_run_id>
```

## Kubernetes Deployment

### Prerequisites

```bash
# Start Minikube (for local testing)
minikube start --cpus 4 --memory 8192

# Or use kind
kind create cluster --config infrastructure/kubernetes/kind-config.yaml
```

### Deploy to Kubernetes

```bash
# Build and push images
make docker-build
make docker-push

# Apply Kubernetes manifests
kubectl apply -f infrastructure/kubernetes/

# Check deployment status
kubectl get pods
kubectl get services

# Access API service
kubectl port-forward service/api-service 8000:80

# View logs
kubectl logs -f deployment/api-deployment
```

### Monitoring in Kubernetes

```bash
# Deploy Prometheus
kubectl apply -f infrastructure/kubernetes/monitoring/prometheus.yaml

# Deploy Grafana
kubectl apply -f infrastructure/kubernetes/monitoring/grafana.yaml

# Access Grafana
kubectl port-forward service/grafana 3000:80
```

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

```bash
# Find process using port
lsof -i :8000  # Replace 8000 with your port

# Kill process
kill -9 <PID>

# Or use different port
docker-compose down
# Edit docker-compose.yml to change port
docker-compose up -d
```

#### 2. Database Connection Errors

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres

# Verify connection
docker-compose exec postgres psql -U mlops -d churn_prediction -c "SELECT 1;"
```

#### 3. MLflow Tracking Issues

```bash
# Check MLflow server is running
curl http://localhost:5000/health

# Restart MLflow
docker-compose restart mlflow

# Check artifact storage
ls -la mlruns/
```

#### 4. Airflow DAG Import Errors

```bash
# Check Airflow logs
docker-compose logs airflow-scheduler

# Test DAG
python airflow/dags/training_pipeline.py

# Refresh DAGs
docker-compose exec airflow-webserver airflow dags list-import-errors
```

#### 5. Docker Compose Issues

```bash
# Rebuild images
docker-compose build --no-cache

# Remove volumes and restart
docker-compose down -v
docker-compose up -d

# Check resource usage
docker stats
```

### Getting Help

1. **Check logs**: Always start with checking logs
   ```bash
   docker-compose logs -f <service-name>
   ```

2. **Run health checks**: Use built-in health checks
   ```bash
   make health-check
   ```

3. **Verify environment**: Ensure all environment variables are set
   ```bash
   python scripts/verify_environment.py
   ```

4. **Check documentation**: Review the documentation files
   - README.md
   - REQUIREMENTS.md
   - ARCHITECTURE.md

5. **Run in debug mode**: Enable debug logging
   ```bash
   export LOG_LEVEL=DEBUG
   python src/api/serve.py
   ```

## Next Steps

Once you have everything running:

1. **Review the architecture**: Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. **Understand requirements**: Review [REQUIREMENTS.md](REQUIREMENTS.md)
3. **Run sample pipeline**: Execute the training pipeline
4. **Make predictions**: Test the API with sample data
5. **Monitor system**: Check Grafana dashboards
6. **Read the code**: Review stub files and TODO comments
7. **Start implementing**: Begin with data ingestion

## Development Best Practices

1. **Version Control**
   - Commit frequently with descriptive messages
   - Create feature branches
   - Use pull requests for code review

2. **Testing**
   - Write tests before implementation (TDD)
   - Aim for >80% code coverage
   - Run tests before committing

3. **Code Quality**
   - Follow PEP 8 style guide
   - Add docstrings to all functions
   - Use type hints
   - Keep functions small and focused

4. **Experiment Tracking**
   - Log all experiments to MLflow
   - Use descriptive experiment names
   - Tag runs with metadata
   - Document significant findings

5. **Documentation**
   - Update docs as you implement
   - Add inline comments for complex logic
   - Keep README up to date
   - Document API changes

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [MLflow Quickstart](https://mlflow.org/docs/latest/quickstart.html)
- [Airflow Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html)
- [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/)
- [Great Expectations Getting Started](https://docs.greatexpectations.io/docs/tutorials/getting_started/tutorial_overview)

## Support

For issues or questions:
1. Check this guide
2. Review documentation
3. Check GitHub issues
4. Contact instructors
