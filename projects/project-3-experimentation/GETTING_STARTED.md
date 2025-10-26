# Getting Started - ML Experimentation Platform

This guide will help you set up and run your first experiments with the ML Experimentation Platform.

## Prerequisites

Before starting, ensure you have:

### Required Software
- Python 3.9 or higher
- Docker and Docker Compose
- kubectl (Kubernetes CLI)
- Minikube or access to a Kubernetes cluster
- Git
- make (GNU Make)

### Recommended Tools
- Helm (for Kubernetes package management)
- k9s (Kubernetes CLI UI)
- Postman or curl (for API testing)

### Knowledge Prerequisites
- Basic understanding of A/B testing concepts
- Familiarity with Python
- Basic Docker knowledge
- Understanding of Kubernetes basics
- Basic statistics knowledge

## Installation

### Step 1: Clone the Repository

```bash
cd /home/claude/ai-infrastructure-project/repositories/learning/ai-infra-mlops-learning/projects
git clone <repository-url> project-3-experimentation
cd project-3-experimentation
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### Step 3: Install Dependencies

```bash
# Install project in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"

# Verify installation
python -c "from src.experiments import ABTest; print('Installation successful!')"
```

### Step 4: Set Up Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
nano .env
```

Required environment variables:
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/experimentation

# Redis
REDIS_URL=redis://localhost:6379/0

# MLflow
MLFLOW_TRACKING_URI=http://localhost:5000

# Kubernetes
KUBECONFIG=/path/to/kubeconfig

# Istio
ISTIO_NAMESPACE=istio-system
```

### Step 5: Start Infrastructure Services

```bash
# Start PostgreSQL, Redis, and MLflow using Docker Compose
docker-compose up -d

# Verify services are running
docker-compose ps

# Check logs if needed
docker-compose logs -f mlflow
```

### Step 6: Initialize Database

```bash
# Run database migrations
alembic upgrade head

# Verify database is ready
python scripts/check_database.py
```

### Step 7: Set Up Kubernetes Cluster (Optional)

If you want to use the progressive rollout features:

```bash
# Start Minikube (if using local cluster)
minikube start --memory=4096 --cpus=2

# Install Istio
./scripts/install_istio.sh

# Verify Istio installation
kubectl get pods -n istio-system

# Deploy sample application
kubectl apply -f examples/k8s/sample-deployment.yaml
```

## Quick Start Examples

### Example 1: Simple A/B Test

Let's run a basic A/B test comparing two models:

```python
# examples/simple_ab_test.py
from src.experiments import ABTest, ExperimentConfig
from src.experiments.statistical_tests import TTest

# Define experiment configuration
config = ExperimentConfig(
    name="model_v2_ab_test",
    metric="conversion_rate",
    arms=["model_v1", "model_v2"],
    traffic_split=[0.5, 0.5],
    sample_size=10000,
    alpha=0.05
)

# Create A/B test
ab_test = ABTest(config)

# Start the experiment
ab_test.start()

# Simulate collecting data (in production, this happens automatically)
# For demo, we'll use synthetic data
import numpy as np

control_conversions = np.random.binomial(1, 0.10, 5000)  # 10% baseline
treatment_conversions = np.random.binomial(1, 0.12, 5000)  # 12% treatment

# Log observations
for conversion in control_conversions:
    ab_test.log_observation("model_v1", conversion)

for conversion in treatment_conversions:
    ab_test.log_observation("model_v2", conversion)

# Run statistical analysis
results = ab_test.analyze()

# Print results
print(f"Test Result: {results.conclusion}")
print(f"P-value: {results.p_value:.4f}")
print(f"Effect Size: {results.effect_size:.4f}")
print(f"Confidence Interval: {results.confidence_interval}")

# View in MLflow UI
print(f"View results at: {results.mlflow_url}")
```

Run the example:
```bash
python examples/simple_ab_test.py
```

View results in MLflow:
```bash
# Open MLflow UI
mlflow ui

# Navigate to http://localhost:5000
```

### Example 2: Multi-Armed Bandit

Run an online learning experiment with Thompson Sampling:

```python
# examples/bandit_example.py
from src.bandits import ThompsonSampling

# Create bandit with 3 arms
bandit = ThompsonSampling(
    arms=["model_a", "model_b", "model_c"],
    prior_alpha=1.0,  # Uniform prior
    prior_beta=1.0
)

# Simulate online traffic
n_rounds = 1000

for i in range(n_rounds):
    # Select which arm to use
    selected_arm = bandit.select_arm()

    # Simulate reward (in production, this is real user feedback)
    true_probabilities = {
        "model_a": 0.08,
        "model_b": 0.10,
        "model_c": 0.12
    }
    reward = np.random.binomial(1, true_probabilities[selected_arm])

    # Update bandit
    bandit.update(selected_arm, reward)

    # Print progress every 100 rounds
    if (i + 1) % 100 == 0:
        print(f"Round {i + 1}:")
        print(f"  Arm selection: {bandit.get_selection_counts()}")
        print(f"  Estimated means: {bandit.get_estimated_means()}")

# Final results
print("\nFinal Results:")
print(f"Best arm: {bandit.get_best_arm()}")
print(f"Cumulative regret: {bandit.compute_regret(0.12):.2f}")
```

Run the example:
```bash
python examples/bandit_example.py
```

### Example 3: Progressive Rollout

Deploy a new model with automated canary deployment:

```python
# examples/canary_rollout.py
from src.rollout import CanaryDeployment, RolloutConfig

# Define rollout configuration
config = RolloutConfig(
    name="model_v3_rollout",
    service_name="recommendation-service",
    namespace="production",
    canary_version="v3",
    stable_version="v2",
    stages=[
        {
            "name": "stage_1",
            "traffic_percentage": 5,
            "duration_minutes": 30,
            "success_criteria": [
                {"metric": "error_rate", "threshold": 0.01, "operator": "<"},
                {"metric": "p95_latency_ms", "threshold": 500, "operator": "<"}
            ]
        },
        {
            "name": "stage_2",
            "traffic_percentage": 25,
            "duration_minutes": 60,
            "success_criteria": [
                {"metric": "error_rate", "threshold": 0.01, "operator": "<"},
                {"metric": "p95_latency_ms", "threshold": 500, "operator": "<"}
            ]
        },
        {
            "name": "stage_3",
            "traffic_percentage": 50,
            "duration_minutes": 120,
            "success_criteria": [
                {"metric": "error_rate", "threshold": 0.01, "operator": "<"}
            ]
        }
    ],
    auto_promote=True,
    auto_rollback=True
)

# Create canary deployment
canary = CanaryDeployment(config)

# Start rollout
canary.start()

# Monitor progress
while canary.is_active():
    status = canary.get_status()
    print(f"Stage: {status.current_stage}")
    print(f"Traffic to canary: {status.canary_traffic_percentage}%")
    print(f"Health: {status.health_status}")
    time.sleep(60)  # Check every minute

# Get final result
result = canary.get_result()
print(f"Rollout completed: {result.success}")
if not result.success:
    print(f"Rollback reason: {result.rollback_reason}")
```

Run the example:
```bash
python examples/canary_rollout.py
```

## Working with Airflow

### Starting Airflow

```bash
# Initialize Airflow database
airflow db init

# Create admin user
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

# Start Airflow webserver
airflow webserver --port 8080 &

# Start Airflow scheduler
airflow scheduler &

# Access UI at http://localhost:8080
```

### Triggering an Experiment DAG

```bash
# List available DAGs
airflow dags list

# Trigger A/B test DAG
airflow dags trigger ab_test_experiment \
    --conf '{"experiment_name": "my_test", "sample_size": 10000}'

# Monitor DAG run
airflow dags list-runs -d ab_test_experiment

# View task logs
airflow tasks logs ab_test_experiment run_statistical_test <execution_date>
```

### Creating a Custom Experiment DAG

```python
# config/airflow/dags/my_custom_experiment.py
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id='my_custom_experiment',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['custom', 'experimentation']
)
def my_experiment_dag():

    @task
    def setup_experiment():
        # Your setup logic
        return {"experiment_id": "exp_123"}

    @task
    def run_experiment(config):
        # Your experiment logic
        from src.experiments import ABTest
        # ... implementation
        pass

    @task
    def analyze_results(experiment_id):
        # Your analysis logic
        pass

    config = setup_experiment()
    run_experiment(config)
    analyze_results(config['experiment_id'])

dag = my_experiment_dag()
```

## Configuration

### Experiment Configuration File

Create YAML configuration files for reproducible experiments:

```yaml
# config/experiments/my_ab_test.yaml
name: recommendation_model_test
type: ab_test
description: Testing new recommendation algorithm

arms:
  - name: control
    model_version: v1.2.3
    traffic_percentage: 50
  - name: treatment
    model_version: v2.0.0
    traffic_percentage: 50

metrics:
  primary:
    name: click_through_rate
    type: proportion
  secondary:
    - name: conversion_rate
      type: proportion
    - name: revenue_per_user
      type: continuous

statistical_test:
  type: frequentist
  method: proportion_test
  alpha: 0.05
  power: 0.80
  minimum_detectable_effect: 0.02

sample_size:
  per_arm: 10000
  total: 20000

duration:
  max_days: 14
  early_stopping: true

randomization:
  unit: user_id
  stratification:
    - user_segment
    - device_type
```

Load and run:
```python
from src.experiments import ExperimentConfig, ABTest

config = ExperimentConfig.from_yaml("config/experiments/my_ab_test.yaml")
experiment = ABTest(config)
experiment.start()
```

## Monitoring and Debugging

### View Experiment Status

```python
from src.experiments import ExperimentManager

manager = ExperimentManager()

# List all experiments
experiments = manager.list_experiments()
for exp in experiments:
    print(f"{exp.name}: {exp.state} ({exp.created_at})")

# Get specific experiment
experiment = manager.get_experiment("exp_123")
print(f"Status: {experiment.state}")
print(f"Observations: {experiment.total_observations}")

# View metrics
metrics = experiment.get_current_metrics()
for arm, values in metrics.items():
    print(f"{arm}: {values}")
```

### Access Logs

```bash
# Application logs
tail -f logs/experimentation.log

# Airflow logs
tail -f logs/airflow/scheduler.log

# Docker logs
docker-compose logs -f mlflow
```

### Prometheus Metrics

Access metrics at http://localhost:9090

Key metrics to monitor:
- `experiment_assignments_total`: Total assignments per experiment
- `experiment_observations_total`: Total observations logged
- `experiment_analysis_duration_seconds`: Time to run analysis
- `bandit_regret`: Cumulative regret for bandit experiments

### Grafana Dashboards

Access dashboards at http://localhost:3000

Pre-built dashboards:
- Experiment Overview
- A/B Test Performance
- Bandit Performance
- Rollout Progress

## Common Tasks

### Running Tests

```bash
# Run all tests
make test

# Run unit tests only
pytest tests/unit/

# Run with coverage
make test-coverage

# Run specific test file
pytest tests/unit/test_statistical_tests.py -v

# Run tests matching pattern
pytest -k "thompson" -v
```

### Code Quality Checks

```bash
# Format code
make format

# Lint code
make lint

# Type checking
make type-check

# All quality checks
make quality
```

### Database Management

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history
```

## Troubleshooting

### Issue: MLflow Server Not Starting

```bash
# Check if port 5000 is in use
lsof -i :5000

# Kill process if needed
kill -9 <PID>

# Restart MLflow
docker-compose restart mlflow
```

### Issue: Database Connection Error

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Test connection
psql postgresql://user:password@localhost:5432/experimentation -c "SELECT 1"

# Reset database
docker-compose down -v
docker-compose up -d
alembic upgrade head
```

### Issue: Kubernetes Deployment Fails

```bash
# Check pod status
kubectl get pods -n experimentation

# View pod logs
kubectl logs <pod-name> -n experimentation

# Describe pod for events
kubectl describe pod <pod-name> -n experimentation

# Check Istio injection
kubectl get namespace experimentation -o yaml | grep istio-injection
```

### Issue: Statistical Test Fails

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run test with detailed output
from src.experiments.statistical_tests import TTest

test = TTest()
result = test.run(control_data, treatment_data, debug=True)
```

## Next Steps

Now that you have the platform running:

1. **Learn the Concepts**: Read through [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system design

2. **Explore Examples**: Try all examples in the `examples/` directory

3. **Run Notebooks**: Work through Jupyter notebooks in `notebooks/` for deeper analysis

4. **Customize**: Modify configurations for your use case

5. **Advanced Features**:
   - Implement custom bandit algorithms
   - Create custom statistical tests
   - Build custom Airflow DAGs
   - Add new metrics and visualizations

6. **Production Deployment**: When ready, see deployment guides in `docs/deployment/`

## Getting Help

- Check documentation in `docs/`
- Review code examples in `examples/`
- Search issues on GitHub
- Consult [VALIDATION.md](VALIDATION.md) for testing procedures

## Best Practices

1. **Always use configuration files** for reproducibility
2. **Log everything to MLflow** for experiment tracking
3. **Set appropriate sample sizes** using power analysis
4. **Monitor metrics continuously** during rollouts
5. **Use version control** for configurations and code
6. **Test thoroughly** before production deployment
7. **Document your experiments** with clear hypotheses
8. **Validate statistical assumptions** before analysis

## Resources

- MLflow Documentation: https://mlflow.org/docs/
- Airflow Documentation: https://airflow.apache.org/docs/
- Istio Documentation: https://istio.io/latest/docs/
- Statistical Testing Guide: See `docs/statistics_guide.md`
- Bandit Algorithms: See `docs/bandit_guide.md`

Happy Experimenting!
