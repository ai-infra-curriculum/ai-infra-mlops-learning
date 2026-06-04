# Architecture - ML Experimentation Platform

## System Overview

The ML Experimentation Platform is a distributed system designed to enable safe, statistically rigorous experimentation with machine learning models in production environments. The platform combines classical A/B testing with modern online learning techniques and automated progressive deployment strategies.

## Design Principles

### 1. Statistical Rigor
- All decisions backed by statistical evidence
- Multiple testing correction to control error rates
- Clear separation of frequentist and Bayesian approaches
- Transparent uncertainty quantification

### 2. Production Safety
- Progressive rollout to minimize blast radius
- Automated rollback on metric degradation
- Shadow deployments for validation
- Comprehensive monitoring and alerting

### 3. Reproducibility
- Complete experiment tracking in MLflow
- Configuration-as-code for all experiments
- Version control for models and code
- Immutable experiment records

### 4. Modularity
- Pluggable statistical test implementations
- Extensible bandit algorithm framework
- Configurable deployment strategies
- Integration with external systems via adapters

### 5. Developer Experience
- Simple configuration via YAML
- Intuitive Python APIs
- Comprehensive documentation
- Rich visualization and reporting

## High-Level Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │   CLI    │  │   API    │  │ Dashboard│  │   Airflow    │  │
│  │   Tool   │  │ Endpoints│  │   (Web)  │  │      UI      │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘  │
└───────┼─────────────┼─────────────┼────────────────┼──────────┘
        │             │             │                │
        └─────────────┴─────────────┴────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────────┐
│                     Application Layer                          │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              Experiment Orchestration                     │ │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │ │
│  │  │  Experiment │  │    Bandit    │  │    Rollout     │  │ │
│  │  │   Manager   │  │  Controller  │  │   Controller   │  │ │
│  │  └─────────────┘  └──────────────┘  └────────────────┘  │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              Statistical & ML Components                  │ │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │ │
│  │  │ Statistical │  │   Multi-Armed│  │     Metric     │  │ │
│  │  │   Tests     │  │    Bandits   │  │   Aggregator   │  │ │
│  │  └─────────────┘  └──────────────┘  └────────────────┘  │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                 Integration Layer                         │ │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │ │
│  │  │   MLflow    │  │    Istio     │  │   Airflow      │  │ │
│  │  │  Adapter    │  │   Adapter    │  │   Adapter      │  │ │
│  │  └─────────────┘  └──────────────┘  └────────────────┘  │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────────┐
│                      Infrastructure Layer                      │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │  PostgreSQL │  │    Redis     │  │   Kubernetes +     │   │
│  │  (Metadata) │  │   (Cache)    │  │       Istio        │   │
│  └─────────────┘  └──────────────┘  └────────────────────┘   │
│                                                                 │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │   MLflow    │  │   Airflow    │  │  Prometheus +      │   │
│  │   Server    │  │   Server     │  │     Grafana        │   │
│  └─────────────┘  └──────────────┘  └────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Experiment Management

#### Experiment Manager
**Responsibility**: Central coordinator for experiment lifecycle

**Key Functions**:
- Create and configure experiments
- Manage experiment state transitions
- Coordinate between components
- Enforce experiment isolation

**State Machine**:
```
CREATED → VALIDATED → RUNNING → ANALYZING → COMPLETED
                         ↓
                    STOPPED/FAILED
```

**Data Model**:
```python
class Experiment:
    id: UUID
    name: str
    type: ExperimentType  # AB_TEST, BANDIT, ROLLOUT
    config: ExperimentConfig
    state: ExperimentState
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    metrics: Dict[str, MetricConfig]
    arms: List[Arm]  # Variants being tested
    assignment_policy: AssignmentPolicy
```

#### Assignment Service
**Responsibility**: Determine which variant a user receives

**Design**:
- Deterministic hash-based assignment for A/B tests
- Dynamic allocation for bandits
- Support for stratified randomization
- Handle assignment consistency

**Implementation**:
```python
class AssignmentService:
    def assign(
        self,
        experiment_id: str,
        user_id: str,
        context: Optional[Dict] = None
    ) -> Assignment:
        """
        Returns the assigned arm for a user.
        Uses consistent hashing for A/B tests,
        bandit algorithm for online learning.
        """
        pass
```

### 2. Statistical Testing Framework

#### Architecture
```
┌─────────────────────────────────────────┐
│         Statistical Test API            │
│  (Abstract base class for all tests)    │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴────────┬──────────────┐
       │                │              │
┌──────▼──────┐  ┌──────▼──────┐  ┌───▼─────────┐
│ Frequentist │  │  Bayesian   │  │ Sequential  │
│    Tests    │  │    Tests    │  │    Tests    │
└─────────────┘  └─────────────┘  └─────────────┘
```

#### Frequentist Tests
**Implementation Classes**:
- `TTest`: Two-sample t-test for continuous metrics
- `ProportionTest`: Z-test for conversion rates
- `ChiSquareTest`: Chi-square test for categorical data
- `MannWhitneyU`: Non-parametric alternative to t-test

**Interface**:
```python
class StatisticalTest(ABC):
    @abstractmethod
    def run(
        self,
        control_data: np.ndarray,
        treatment_data: np.ndarray,
        alpha: float = 0.05
    ) -> TestResult:
        pass

    @abstractmethod
    def compute_confidence_interval(
        self,
        data: np.ndarray,
        confidence: float = 0.95
    ) -> Tuple[float, float]:
        pass
```

#### Bayesian Tests
**Implementation**:
- Prior specification (informative vs. non-informative)
- Conjugate prior updates
- MCMC for non-conjugate priors
- Credible interval computation
- Probability of superiority

**Beta-Binomial Model** (for conversion rates):
```python
class BayesianProportionTest:
    def __init__(self, alpha_prior=1, beta_prior=1):
        self.alpha_prior = alpha_prior
        self.beta_prior = beta_prior

    def update_posterior(self, successes: int, trials: int):
        """Update Beta posterior with new data"""
        return Beta(
            alpha=self.alpha_prior + successes,
            beta=self.beta_prior + (trials - successes)
        )

    def probability_b_better_than_a(
        self,
        posterior_a: Beta,
        posterior_b: Beta
    ) -> float:
        """Monte Carlo estimation of P(B > A)"""
        samples_a = posterior_a.sample(10000)
        samples_b = posterior_b.sample(10000)
        return np.mean(samples_b > samples_a)
```

#### Sequential Testing
**Methods**:
- Sequential Probability Ratio Test (SPRT)
- Group sequential designs
- Always-valid inference

**Benefits**:
- Early stopping for winners/losers
- Reduced sample size requirements
- Continuous monitoring

### 3. Multi-Armed Bandit Framework

#### Base Architecture
```python
class Bandit(ABC):
    """Abstract base class for bandit algorithms"""

    @abstractmethod
    def select_arm(self, context: Optional[np.ndarray] = None) -> int:
        """Select which arm to pull next"""
        pass

    @abstractmethod
    def update(self, arm: int, reward: float, context: Optional[np.ndarray] = None):
        """Update beliefs after observing reward"""
        pass

    def compute_regret(self, optimal_arm_mean: float) -> float:
        """Calculate cumulative regret"""
        pass
```

#### Thompson Sampling
**Algorithm**:
1. Sample from posterior distribution for each arm
2. Select arm with highest sample
3. Observe reward
4. Update posterior with Bayesian update

**Implementation**:
```python
class ThompsonSampling(Bandit):
    def __init__(self, n_arms: int, prior: str = "beta"):
        self.n_arms = n_arms
        if prior == "beta":
            # Beta(1,1) uniform prior
            self.alpha = np.ones(n_arms)
            self.beta = np.ones(n_arms)

    def select_arm(self, context=None) -> int:
        # Sample from posterior
        theta_samples = np.random.beta(self.alpha, self.beta)
        return np.argmax(theta_samples)

    def update(self, arm: int, reward: float, context=None):
        # Bayesian update
        self.alpha[arm] += reward
        self.beta[arm] += (1 - reward)
```

#### Upper Confidence Bound (UCB)
**Algorithm**:
Select arm with highest upper confidence bound:
```
UCB(arm) = mean_reward(arm) + sqrt(2 * ln(t) / n_pulls(arm))
```

**Properties**:
- Optimistic in the face of uncertainty
- Logarithmic regret bounds
- No prior required

#### Contextual Bandits
**LinUCB Algorithm**:
```python
class LinUCB(Bandit):
    """Linear contextual bandit with UCB"""

    def __init__(self, n_arms: int, d: int, alpha: float = 1.0):
        self.n_arms = n_arms
        self.d = d  # Context dimension
        self.alpha = alpha  # Exploration parameter

        # Initialize for each arm
        self.A = [np.identity(d) for _ in range(n_arms)]  # Design matrix
        self.b = [np.zeros(d) for _ in range(n_arms)]     # Response vector

    def select_arm(self, context: np.ndarray) -> int:
        ucb_values = []
        for arm in range(self.n_arms):
            A_inv = np.linalg.inv(self.A[arm])
            theta = A_inv @ self.b[arm]  # Estimate

            # UCB calculation
            ucb = theta @ context + self.alpha * np.sqrt(
                context @ A_inv @ context
            )
            ucb_values.append(ucb)

        return np.argmax(ucb_values)
```

### 4. Progressive Rollout System

#### Rollout Controller
**State Machine**:
```
INITIALIZED → VALIDATING → STAGE_1 → STAGE_2 → ... → COMPLETED
                  ↓
             ROLLING_BACK → ROLLED_BACK
```

**Stage Configuration**:
```yaml
rollout:
  strategy: canary
  stages:
    - name: stage_1
      traffic_percentage: 5
      duration: 1h
      success_criteria:
        - metric: error_rate
          operator: <
          threshold: 0.01
        - metric: p95_latency
          operator: <
          threshold: 500ms
    - name: stage_2
      traffic_percentage: 25
      duration: 2h
      success_criteria:
        # ... similar criteria
```

#### Istio Traffic Management
**VirtualService Generation**:
```python
class IstioManager:
    def create_traffic_split(
        self,
        service_name: str,
        canary_weight: int,
        stable_weight: int
    ) -> VirtualService:
        """Generate Istio VirtualService for weighted routing"""
        return {
            "apiVersion": "networking.istio.io/v1beta1",
            "kind": "VirtualService",
            "metadata": {"name": f"{service_name}-vs"},
            "spec": {
                "hosts": [service_name],
                "http": [{
                    "route": [
                        {
                            "destination": {
                                "host": service_name,
                                "subset": "canary"
                            },
                            "weight": canary_weight
                        },
                        {
                            "destination": {
                                "host": service_name,
                                "subset": "stable"
                            },
                            "weight": stable_weight
                        }
                    ]
                }]
            }
        }
```

#### Metrics Monitor
**Responsibilities**:
- Query Prometheus for service metrics
- Compare against baseline and thresholds
- Detect anomalies and degradations
- Trigger rollback when necessary

**Implementation**:
```python
class MetricsMonitor:
    def check_stage_health(
        self,
        stage: RolloutStage,
        metrics: Dict[str, float]
    ) -> Tuple[bool, Optional[str]]:
        """
        Returns (is_healthy, failure_reason)
        """
        for criterion in stage.success_criteria:
            metric_value = metrics.get(criterion.metric)
            if not self._check_threshold(
                metric_value,
                criterion.operator,
                criterion.threshold
            ):
                return False, f"{criterion.metric} threshold violated"
        return True, None
```

### 5. MLflow Integration

#### Tracking Architecture
```python
class MLflowTracker:
    def __init__(self, tracking_uri: str):
        mlflow.set_tracking_uri(tracking_uri)
        self.client = mlflow.tracking.MlflowClient()

    def start_experiment(self, experiment_name: str) -> str:
        """Create or get existing MLflow experiment"""
        try:
            experiment = self.client.create_experiment(experiment_name)
        except:
            experiment = self.client.get_experiment_by_name(experiment_name)
        return experiment.experiment_id

    def log_arm_metrics(
        self,
        run_id: str,
        arm: str,
        metrics: Dict[str, float],
        step: int
    ):
        """Log metrics for a specific arm"""
        for metric_name, value in metrics.items():
            self.client.log_metric(
                run_id,
                f"{arm}/{metric_name}",
                value,
                step=step
            )

    def log_test_results(self, run_id: str, results: TestResult):
        """Log statistical test results"""
        self.client.log_params(run_id, {
            "test_type": results.test_type,
            "alpha": results.alpha,
        })
        self.client.log_metrics(run_id, {
            "p_value": results.p_value,
            "test_statistic": results.statistic,
            "effect_size": results.effect_size,
        })
```

### 6. Airflow Orchestration

#### DAG Structure for A/B Test
```python
@dag(
    dag_id='ab_test_experiment',
    schedule_interval=None,
    catchup=False,
    tags=['experimentation', 'ab_test']
)
def ab_test_dag():

    @task
    def initialize_experiment(config: dict) -> str:
        """Create experiment in system"""
        experiment = ExperimentManager.create(config)
        return experiment.id

    @task
    def collect_metrics(experiment_id: str):
        """Gather metrics from production"""
        metrics = MetricsCollector.collect(experiment_id)
        return metrics

    @task
    def run_statistical_test(experiment_id: str, metrics: dict):
        """Perform hypothesis testing"""
        test = StatisticalTestFactory.create(experiment_id)
        results = test.run(metrics)
        return results

    @task
    def generate_report(experiment_id: str, results: dict):
        """Create experiment report"""
        report = ReportGenerator.generate(experiment_id, results)
        report.send_notifications()

    # Define task dependencies
    exp_id = initialize_experiment(config)
    metrics = collect_metrics(exp_id)
    results = run_statistical_test(exp_id, metrics)
    generate_report(exp_id, results)

ab_test = ab_test_dag()
```

#### Progressive Rollout DAG
```python
@dag(
    dag_id='progressive_rollout',
    schedule_interval='@hourly',  # Check every hour
    tags=['experimentation', 'rollout']
)
def progressive_rollout_dag():

    @task.sensor
    def wait_for_stage_completion(stage: RolloutStage):
        """Wait for stage duration to elapse"""
        return time.time() >= stage.start_time + stage.duration

    @task
    def check_stage_metrics(stage: RolloutStage) -> bool:
        """Validate metrics meet success criteria"""
        monitor = MetricsMonitor()
        is_healthy, reason = monitor.check_stage_health(stage)

        if not is_healthy:
            raise AirflowException(f"Stage unhealthy: {reason}")

        return True

    @task.branch
    def decide_next_action(stage_healthy: bool, is_final_stage: bool):
        """Decide whether to progress, complete, or rollback"""
        if not stage_healthy:
            return 'rollback'
        elif is_final_stage:
            return 'complete_rollout'
        else:
            return 'progress_to_next_stage'

    # ... task orchestration
```

### 7. Reporting System

#### Dashboard Architecture
- **Real-time updates** via WebSocket connections
- **Plotly Dash** for interactive visualizations
- **Responsive design** for mobile/desktop

#### Report Generator
```python
class ReportGenerator:
    def generate_ab_test_report(
        self,
        experiment: Experiment,
        results: TestResult
    ) -> Report:
        """Generate comprehensive A/B test report"""

        report = Report(experiment.name)

        # Executive summary
        report.add_section(
            "Executive Summary",
            self._create_summary(results)
        )

        # Statistical details
        report.add_section(
            "Statistical Analysis",
            self._create_statistical_section(results)
        )

        # Visualizations
        report.add_plot(
            "Metric Comparison",
            self._create_comparison_plot(experiment)
        )

        report.add_plot(
            "Confidence Intervals",
            self._create_confidence_interval_plot(results)
        )

        # Recommendations
        report.add_section(
            "Recommendations",
            self._create_recommendations(results)
        )

        return report
```

## Data Flow

### A/B Test Workflow
```
1. User creates experiment via API/CLI
   ↓
2. Experiment Manager validates configuration
   ↓
3. Assignment Service starts routing traffic
   ↓
4. Users interact with assigned variants
   ↓
5. Metrics logged to database
   ↓
6. Airflow DAG triggers statistical analysis
   ↓
7. Results logged to MLflow
   ↓
8. Report generated and distributed
   ↓
9. Decision made (rollout/reject/continue)
```

### Bandit Workflow
```
1. Initialize bandit with arms and priors
   ↓
2. For each incoming request:
   a. Bandit algorithm selects arm
   b. User receives selected variant
   c. Observe reward (conversion, revenue, etc.)
   d. Update bandit posterior/estimates
   ↓
3. Periodic evaluation:
   a. Compute regret
   b. Check convergence
   c. Log to MLflow
   ↓
4. Convergence reached:
   a. Select best arm
   b. Generate report
   c. Full rollout to winner
```

### Progressive Rollout Workflow
```
1. Deploy new model version (canary)
   ↓
2. Istio routes small % traffic to canary
   ↓
3. Monitor metrics for duration
   ↓
4. Metrics healthy?
   Yes → Increase traffic % → Repeat from step 2
   No → Trigger rollback → Route 100% to stable
   ↓
5. All stages passed:
   → Promote canary to stable
   → Complete rollout
```

## Technology Stack

### Core Application
- **Python 3.9+**: Primary language
- **FastAPI**: REST API framework
- **Pydantic**: Data validation
- **SQLAlchemy**: ORM for database
- **Alembic**: Database migrations

### Statistical Computing
- **NumPy**: Numerical computations
- **SciPy**: Statistical tests
- **PyMC3**: Bayesian inference (optional)
- **statsmodels**: Advanced statistical methods

### ML Infrastructure
- **MLflow**: Experiment tracking
- **Apache Airflow**: Workflow orchestration
- **Kubernetes**: Container orchestration
- **Istio**: Service mesh

### Data Storage
- **PostgreSQL**: Metadata and experiment state
- **Redis**: Caching and fast assignment lookups
- **S3/MinIO**: Artifact storage

### Monitoring & Observability
- **Prometheus**: Metrics collection
- **Grafana**: Dashboards
- **OpenTelemetry**: Distributed tracing
- **ELK Stack**: Log aggregation

### Frontend
- **Plotly Dash**: Interactive dashboards
- **React**: Custom UI components (optional)

## Deployment Architecture

### Kubernetes Resources
```
Namespace: experimentation

Deployments:
- experiment-api (3 replicas)
- assignment-service (5 replicas)
- metrics-collector (2 replicas)
- report-generator (1 replica)

StatefulSets:
- postgresql (1 replica)
- redis (1 replica)

Services:
- experiment-api-svc (ClusterIP)
- assignment-service-svc (ClusterIP)
- postgres-svc (ClusterIP)
- redis-svc (ClusterIP)

Ingress:
- experiment-api-ingress (HTTPS)
- dashboard-ingress (HTTPS)
```

### Istio Configuration
```yaml
# DestinationRule for subset definitions
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: ml-model-dr
spec:
  host: ml-model-service
  subsets:
  - name: stable
    labels:
      version: v1
  - name: canary
    labels:
      version: v2
```

## Security Considerations

### Authentication & Authorization
- JWT tokens for API access
- Role-based access control (RBAC)
- Service-to-service mTLS via Istio

### Data Protection
- Encryption at rest (database)
- Encryption in transit (TLS)
- PII anonymization in metrics

### Audit Logging
- All experiment modifications logged
- User actions tracked
- Compliance with data regulations

## Scalability Considerations

### Horizontal Scaling
- Stateless API services (scale pods)
- Read replicas for PostgreSQL
- Redis cluster for high availability

### Performance Optimization
- Assignment caching in Redis
- Batch metric aggregation
- Async processing for non-critical path
- Database indexing on query patterns

### Cost Optimization
- Auto-scaling based on load
- Spot instances for Airflow workers
- Data retention policies

## Disaster Recovery

### Backup Strategy
- Daily PostgreSQL backups
- MLflow artifact replication
- Configuration backup in git

### Recovery Procedures
- Database restore from backup
- Experiment state recovery
- Graceful degradation modes

## Future Enhancements

1. **Advanced Algorithms**
   - Contextual bandits with deep learning
   - Causal inference methods
   - Multi-objective optimization

2. **Platform Features**
   - Multi-tenancy support
   - Custom metric plugins
   - Integration marketplace

3. **Automation**
   - Auto-tuning of experiment parameters
   - Anomaly detection with ML
   - Predictive experiment duration

4. **Observability**
   - Cost attribution per experiment
   - Carbon footprint tracking
   - Advanced debugging tools
