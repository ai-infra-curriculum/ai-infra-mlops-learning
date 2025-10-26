# Project 3: ML Experimentation Platform

A comprehensive A/B testing and progressive rollout platform for machine learning models with multi-armed bandit algorithms, statistical testing, and automated experiment tracking.

## Overview

This project implements an end-to-end experimentation platform that enables:
- **A/B Testing**: Rigorous statistical testing framework for model comparison
- **Multi-Armed Bandits**: Dynamic allocation strategies (Thompson Sampling, UCB)
- **Progressive Rollouts**: Automated canary deployments with Istio traffic management
- **Experiment Tracking**: Integration with MLflow for comprehensive experiment logging
- **Orchestration**: Airflow-based workflow management for complex experiments
- **Automated Reporting**: Real-time dashboards and statistical analysis reports

## Use Case Scenario

**Problem**: A recommendation system team needs to safely test new model versions in production while:
- Minimizing exposure to potentially worse models
- Gathering statistically significant results quickly
- Automating rollout decisions based on performance metrics
- Tracking all experiments with reproducibility
- Supporting multiple concurrent experiments

**Solution**: This platform provides automated experimentation infrastructure that dynamically allocates traffic, monitors performance metrics, and makes rollout decisions based on statistical evidence.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Experimentation Platform                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐     ┌──────────────┐    ┌──────────────┐ │
│  │   A/B Test   │     │ Multi-Armed  │    │  Progressive │ │
│  │  Framework   │────▶│   Bandits    │───▶│   Rollout    │ │
│  └──────────────┘     └──────────────┘    └──────────────┘ │
│         │                     │                    │         │
│         └─────────────────────┴────────────────────┘         │
│                              │                                │
│                    ┌─────────▼─────────┐                     │
│                    │  Experiment       │                     │
│                    │  Tracking (MLflow)│                     │
│                    └─────────┬─────────┘                     │
│                              │                                │
│         ┌────────────────────┴────────────────────┐          │
│         │                                          │          │
│  ┌──────▼──────┐                          ┌───────▼──────┐  │
│  │   Airflow   │                          │  Reporting   │  │
│  │Orchestration│                          │  & Analytics │  │
│  └─────────────┘                          └──────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Istio Service    │
                    │  Mesh (Traffic    │
                    │  Splitting)       │
                    └───────────────────┘
```

## Key Features

### 1. Statistical Testing Framework
- Frequentist hypothesis testing (t-tests, chi-square)
- Bayesian A/B testing with credible intervals
- Sequential testing for early stopping
- Multiple comparison corrections (Bonferroni, FDR)
- Power analysis and sample size estimation

### 2. Multi-Armed Bandit Algorithms
- **Thompson Sampling**: Bayesian approach for exploration/exploitation
- **Upper Confidence Bound (UCB)**: Optimistic allocation strategy
- **Epsilon-Greedy**: Simple baseline with configurable exploration
- Contextual bandits with linear models
- Performance tracking and regret analysis

### 3. Progressive Rollout Automation
- Canary deployment with configurable stages
- Automated traffic shifting based on metrics
- Integration with Istio for fine-grained traffic control
- Rollback mechanisms on metric degradation
- Blue-green deployment support

### 4. Experiment Tracking
- MLflow integration for experiment logging
- Metric tracking (accuracy, latency, business KPIs)
- Model artifact versioning
- Experiment comparison and visualization
- Reproducibility through comprehensive logging

### 5. Airflow Orchestration
- DAG templates for common experiment patterns
- Scheduled experiment execution
- Multi-stage experiment workflows
- Integration with monitoring and alerting
- Automated report generation

### 6. Reporting & Analytics
- Real-time experiment dashboards
- Statistical significance monitoring
- Confidence interval visualization
- Automated email/Slack notifications
- Exportable experiment reports

## Project Structure

```
project-3-experimentation/
├── README.md                 # This file
├── REQUIREMENTS.md          # Detailed requirements and acceptance criteria
├── ARCHITECTURE.md          # System design and technical decisions
├── GETTING_STARTED.md       # Quick start guide
├── VALIDATION.md            # Testing and validation checklist
├── pyproject.toml           # Project dependencies and configuration
├── Makefile                 # Common development tasks
├── .env.example             # Environment variable template
│
├── src/
│   ├── experiments/         # A/B testing framework
│   │   ├── ab_test.py      # Core A/B testing implementation
│   │   ├── statistical_tests.py  # Statistical test library
│   │   ├── bayesian_tests.py     # Bayesian testing methods
│   │   └── sequential_tests.py   # Sequential analysis
│   │
│   ├── bandits/            # Multi-armed bandit algorithms
│   │   ├── base.py        # Base bandit interface
│   │   ├── thompson_sampling.py  # Thompson sampling implementation
│   │   ├── ucb.py         # UCB algorithms
│   │   ├── epsilon_greedy.py     # Epsilon-greedy
│   │   └── contextual.py  # Contextual bandit variants
│   │
│   ├── rollout/           # Progressive rollout automation
│   │   ├── canary.py     # Canary deployment controller
│   │   ├── istio_manager.py      # Istio traffic management
│   │   ├── metrics_monitor.py    # Metrics monitoring
│   │   └── rollback.py   # Automated rollback logic
│   │
│   ├── tracking/          # Experiment tracking
│   │   ├── mlflow_tracker.py     # MLflow integration
│   │   ├── metrics_logger.py     # Metrics logging
│   │   └── artifact_manager.py   # Artifact management
│   │
│   ├── reporting/         # Reporting and analytics
│   │   ├── dashboard.py  # Dashboard generation
│   │   ├── report_generator.py   # Report creation
│   │   ├── visualizations.py     # Plotting utilities
│   │   └── notifications.py      # Alert notifications
│   │
│   └── common/            # Shared utilities
│       ├── config.py     # Configuration management
│       ├── logging.py    # Logging setup
│       └── utils.py      # Common utilities
│
├── config/
│   ├── istio/            # Istio configurations
│   │   ├── virtual_service.yaml
│   │   ├── destination_rule.yaml
│   │   └── traffic_policy.yaml
│   │
│   ├── mlflow/           # MLflow configuration
│   │   └── tracking_config.yaml
│   │
│   └── airflow/          # Airflow DAGs and config
│       ├── dags/
│       │   ├── ab_test_dag.py
│       │   ├── bandit_optimization_dag.py
│       │   └── progressive_rollout_dag.py
│       └── airflow.cfg
│
├── tests/
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── e2e/             # End-to-end tests
│
├── scripts/              # Utility scripts
│   ├── setup_mlflow.sh
│   ├── deploy_istio_config.sh
│   └── run_experiment.py
│
├── docs/                 # Additional documentation
│   ├── api/             # API documentation
│   ├── tutorials/       # Step-by-step tutorials
│   └── guides/          # How-to guides
│
├── examples/            # Example experiments
│   ├── simple_ab_test.py
│   ├── bandit_example.py
│   └── canary_rollout.py
│
└── notebooks/           # Jupyter notebooks
    ├── statistical_analysis.ipynb
    └── experiment_results.ipynb
```

## Getting Started

See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed setup instructions.

Quick start:
```bash
# Install dependencies
pip install -e .

# Set up infrastructure
make setup-infrastructure

# Run example A/B test
python examples/simple_ab_test.py

# View results in MLflow
mlflow ui
```

## Key Learning Objectives

1. **Statistical Rigor**: Understanding statistical testing, p-values, confidence intervals
2. **Online Learning**: Implementing and comparing bandit algorithms
3. **Production Safety**: Progressive rollouts and automated rollback mechanisms
4. **Service Mesh**: Using Istio for traffic management
5. **Experiment Management**: MLflow for tracking and reproducibility
6. **Workflow Orchestration**: Airflow for complex experiment workflows
7. **Decision Automation**: Automated decision-making based on statistical evidence

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Kubernetes cluster (Minikube or cloud provider)
- Istio installed on cluster
- Basic understanding of statistics and probability
- Familiarity with A/B testing concepts

## Technologies Used

- **Python**: Core implementation language
- **SciPy/NumPy**: Statistical computations
- **MLflow**: Experiment tracking and model registry
- **Apache Airflow**: Workflow orchestration
- **Istio**: Service mesh for traffic management
- **Kubernetes**: Container orchestration
- **Plotly/Matplotlib**: Visualization
- **FastAPI**: API endpoints for experiment control
- **PostgreSQL**: Metadata storage
- **Prometheus/Grafana**: Metrics and monitoring

## Documentation

- [REQUIREMENTS.md](REQUIREMENTS.md) - Detailed requirements and acceptance criteria
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design and technical architecture
- [GETTING_STARTED.md](GETTING_STARTED.md) - Setup and quick start guide
- [VALIDATION.md](VALIDATION.md) - Testing and validation procedures

## Development Workflow

1. **Design Experiment**: Define hypothesis, metrics, and success criteria
2. **Configure Test**: Set up A/B test or bandit experiment
3. **Deploy Models**: Deploy model variants to Kubernetes
4. **Start Experiment**: Launch experiment with Airflow DAG
5. **Monitor Progress**: Track metrics in real-time dashboards
6. **Analyze Results**: Statistical analysis and significance testing
7. **Make Decision**: Automated or manual rollout decision
8. **Progressive Rollout**: Gradual traffic shifting to winner
9. **Generate Report**: Comprehensive experiment report

## Common Experiment Patterns

### Pattern 1: Simple A/B Test
```python
from src.experiments import ABTest

test = ABTest(
    name="model_v2_test",
    control_model="model_v1",
    treatment_model="model_v2",
    metric="click_through_rate",
    sample_size=10000
)
test.run()
results = test.analyze()
```

### Pattern 2: Multi-Armed Bandit
```python
from src.bandits import ThompsonSampling

bandit = ThompsonSampling(
    arms=["model_a", "model_b", "model_c"],
    metric="conversion_rate"
)
bandit.run(duration_hours=24)
winner = bandit.get_best_arm()
```

### Pattern 3: Progressive Rollout
```python
from src.rollout import CanaryDeployment

canary = CanaryDeployment(
    new_model="model_v3",
    stages=[10, 25, 50, 100],  # Traffic percentages
    metric_threshold=0.95,
    auto_promote=True
)
canary.start()
```

## Testing

```bash
# Run all tests
make test

# Run specific test suite
pytest tests/unit/test_statistical_tests.py

# Run with coverage
make test-coverage

# Validate experiment configurations
make validate
```

## Contributing

This is a learning project. Focus areas for extension:
- Additional bandit algorithms (Exp3, UCB variants)
- Advanced statistical tests (CUSUM, SPRT)
- Multi-objective optimization
- Causal inference methods
- Integration with more ML platforms

## License

Educational use only - part of AI Infrastructure Learning Path

## References

- "A/B Testing: The Most Powerful Way to Turn Clicks Into Customers" - Dan Siroker
- "Bandit Algorithms for Website Optimization" - John Myles White
- Istio Documentation: https://istio.io/latest/docs/
- MLflow Documentation: https://mlflow.org/docs/latest/
- Apache Airflow Documentation: https://airflow.apache.org/docs/

## Next Steps

After completing this project, you'll be ready for:
- Advanced online learning techniques
- Causal inference methods
- Multi-objective optimization
- Large-scale experimentation platforms
