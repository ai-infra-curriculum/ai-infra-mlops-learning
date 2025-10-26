# Module 06: Automation & Orchestration - Quiz

## Instructions

- **Total Questions**: 30
- **Time Limit**: 45 minutes
- **Passing Score**: 75% (23/30 correct)
- **Question Types**: Multiple choice, multiple select, code analysis, DAG analysis

---

## Section 1: Apache Airflow Fundamentals (Questions 1-8)

### Question 1
What is the primary purpose of Apache Airflow in MLOps?

A) To train machine learning models faster
B) To orchestrate and schedule complex workflows with dependencies
C) To deploy models to production
D) To store training data

<details>
<summary>Answer</summary>

**B) To orchestrate and schedule complex workflows with dependencies**

**Explanation**: Apache Airflow is a workflow orchestration platform that:
- Defines workflows as Directed Acyclic Graphs (DAGs)
- Schedules task execution
- Manages dependencies between tasks
- Monitors workflow execution
- Handles retries and failure recovery

In MLOps, Airflow orchestrates end-to-end ML pipelines including data ingestion, preprocessing, training, evaluation, and deployment.

</details>

---

### Question 2
What is a DAG in Apache Airflow?

A) Data Aggregation Group
B) Directed Acyclic Graph - a collection of tasks with defined dependencies
C) Daily Automated Generator
D) Database Access Gateway

<details>
<summary>Answer</summary>

**B) Directed Acyclic Graph - a collection of tasks with defined dependencies**

**Explanation**: A DAG is:
- **Directed**: Tasks flow in specific direction (upstream → downstream)
- **Acyclic**: No circular dependencies (prevents infinite loops)
- **Graph**: Nodes (tasks) connected by edges (dependencies)

Example DAG structure:
```
fetch_data → preprocess → train_model → evaluate → deploy
                                      ↓
                                  log_metrics
```

DAGs ensure tasks execute in correct order and enable parallel execution where possible.

</details>

---

### Question 3
Analyze this Airflow task definition:

```python
train_model = PythonOperator(
    task_id='train_model',
    python_callable=train_function,
    retries=3,
    retry_delay=timedelta(minutes=5),
    execution_timeout=timedelta(hours=2),
)
```

What happens if `train_function` fails after 30 minutes?

A) Task fails immediately
B) Task retries immediately 3 times
C) Task waits 5 minutes then retries (up to 3 times)
D) Task runs for 2 hours then fails

<details>
<summary>Answer</summary>

**C) Task waits 5 minutes then retries (up to 3 times)**

**Explanation**: Task retry behavior:
- `retries=3`: Task will retry up to 3 times after initial failure
- `retry_delay=timedelta(minutes=5)`: Waits 5 minutes between retries
- `execution_timeout=timedelta(hours=2)`: Task fails if single execution exceeds 2 hours

Timeline for failure at 30 minutes:
1. Attempt 1: Fails at 30 min
2. Wait 5 min
3. Attempt 2: Retry (if fails, wait 5 min)
4. Attempt 3: Retry (if fails, wait 5 min)
5. Attempt 4: Final retry
6. If all fail: Task marked as failed

The `execution_timeout` applies to each individual attempt, not total time.

</details>

---

### Question 4
**[Multiple Select]** Which of the following are valid Airflow executors? (Select all that apply)

A) SequentialExecutor
B) LocalExecutor
C) CeleryExecutor
D) KubernetesExecutor
E) MLflowExecutor
F) SparkExecutor

<details>
<summary>Answer</summary>

**A, B, C, D**

**Explanation**:
- **A) SequentialExecutor**: ✓ Default, runs one task at a time, single-threaded
- **B) LocalExecutor**: ✓ Runs tasks in parallel using multiprocessing
- **C) CeleryExecutor**: ✓ Distributed execution using Celery task queue
- **D) KubernetesExecutor**: ✓ Each task runs in a separate Kubernetes pod
- **E) MLflowExecutor**: ✗ Not an Airflow executor
- **F) SparkExecutor**: ✗ Not a built-in executor (though you can run Spark jobs via operators)

Choosing executor:
- Development: SequentialExecutor or LocalExecutor
- Production: CeleryExecutor or KubernetesExecutor for scalability

</details>

---

### Question 5
What is XCom in Airflow, and when should it be used?

A) External Communication protocol for APIs
B) Cross-communication mechanism for passing small amounts of data between tasks
C) A type of database connector
D) Airflow's configuration file format

<details>
<summary>Answer</summary>

**B) Cross-communication mechanism for passing small amounts of data between tasks**

**Explanation**: XCom (Cross-Communication):
- Allows tasks to exchange messages/data
- Stored in Airflow metadata database
- Pushed by upstream task, pulled by downstream task

Usage:
```python
# Push data
def task1(**context):
    context['task_instance'].xcom_push(key='data_path', value='/tmp/data.csv')

# Pull data
def task2(**context):
    path = context['task_instance'].xcom_pull(task_ids='task1', key='data_path')
```

**Important limitations**:
- Only for small data (< 48KB recommended)
- For large data: Use shared storage (S3, NFS) and pass paths via XCom
- Not for streaming data

**When to use**:
- Passing file paths
- Sharing configuration
- Communicating run IDs
- Conditional task execution

</details>

---

### Question 6
What is the difference between `schedule_interval='@daily'` and `schedule_interval=timedelta(days=1)` in Airflow?

A) They are identical
B) `@daily` runs at midnight UTC; `timedelta(days=1)` runs 24 hours after previous run
C) `@daily` is faster
D) `timedelta` only works with SequentialExecutor

<details>
<summary>Answer</summary>

**B) `@daily` runs at midnight UTC; `timedelta(days=1)` runs 24 hours after previous run**

**Explanation**:

**Cron-based (`@daily`)**:
- Runs at specific time (midnight UTC for `@daily`)
- Aligned to calendar
- Equivalent to `cron: 0 0 * * *`
- Example: Always runs at 00:00 UTC

**Timedelta-based (`timedelta(days=1)`)**:
- Runs relative to previous execution
- 24 hours after last `execution_date`
- Not aligned to calendar

**Example scenario**:
- DAG `start_date`: 2024-01-01 14:00 UTC
- `@daily`: Runs 2024-01-02 00:00, 2024-01-03 00:00, ...
- `timedelta(days=1)`: Runs 2024-01-02 14:00, 2024-01-03 14:00, ...

**Best practice for ML**:
- Use `@daily` for daily batch jobs (consistent timing)
- Use `timedelta` for continuous processing

</details>

---

### Question 7
Analyze this DAG dependency definition:

```python
task1 >> [task2, task3] >> task4
task2 >> task5
```

In what order can tasks execute?

A) task1 → task2 → task3 → task4 → task5 (sequential only)
B) task1 → (task2 and task3 in parallel) → task4; task2 → task5
C) All tasks run in parallel
D) Invalid syntax - will error

<details>
<summary>Answer</summary>

**B) task1 → (task2 and task3 in parallel) → task4; task2 → task5**

**Explanation**: Dependency graph:
```
       task1
      /     \
   task2   task3
    / \      /
 task5 task4
```

Execution order:
1. **task1** runs first
2. **task2** and **task3** run in parallel (both depend only on task1)
3. **task5** runs after task2 completes
4. **task4** runs after BOTH task2 AND task3 complete
5. **task5** can run before task4 if task2 finishes before task3

Key points:
- `>>` defines dependencies (left must complete before right)
- `[task2, task3]` creates fan-out (parallel execution)
- Tasks run in parallel when dependencies allow
- `task4` has implicit AND condition (waits for all upstream)

</details>

---

### Question 8
What is the purpose of `catchup=False` in a DAG definition?

A) Prevents catching exceptions
B) Prevents Airflow from running missed scheduled runs between start_date and current date
C) Disables error logging
D) Skips data validation

<details>
<summary>Answer</summary>

**B) Prevents Airflow from running missed scheduled runs between start_date and current date**

**Explanation**: Catchup behavior:

**`catchup=True` (default)**:
- Backfills all missed runs since `start_date`
- Example: DAG with `start_date=2024-01-01`, deployed on 2024-01-10
  - Airflow creates runs for: Jan 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
  - All execute (can overwhelm system)

**`catchup=False`**:
- Only schedules runs from activation forward
- Skips historical runs
- Same example: Only creates run for Jan 10

**When to use**:
- `catchup=True`: When historical data processing is needed (e.g., reprocessing data after bug fix)
- `catchup=False`: For most ML training pipelines (only train on recent data)

**Best practice for ML**:
```python
dag = DAG(
    'ml_training',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,  # Don't backfill old training runs
)
```

</details>

---

## Section 2: Kubeflow Pipelines (Questions 9-14)

### Question 9
What is the main advantage of Kubeflow Pipelines over Airflow for ML workflows?

A) Kubeflow is always faster
B) Kubeflow provides container-native execution with strong typing and artifact lineage
C) Kubeflow is easier to install
D) Kubeflow doesn't require Kubernetes

<details>
<summary>Answer</summary>

**B) Kubeflow provides container-native execution with strong typing and artifact lineage**

**Explanation**: Kubeflow Pipelines advantages:

**Container-Native**:
- Every component runs in isolated container
- Reproducible environments
- Easy dependency management

**Strong Typing**:
```python
def train(
    dataset: Input[Dataset],
    model: Output[Model],
    n_estimators: int = 100
) -> float:
```
- Type-checked inputs/outputs
- Prevents type mismatches at compile time

**Artifact Lineage**:
- Automatic tracking of data/model artifacts
- Versioning built-in
- Visualize artifact flow

**ML-Specific**:
- Designed for ML workflows
- Native integration with ML frameworks
- Metadata tracking

**Airflow strengths**:
- More mature ecosystem
- Better for heterogeneous workflows (ML + ETL + reporting)
- Richer operator library
- Easier debugging

**Use Kubeflow when**: Pure ML workflows, strong reproducibility needs, Kubernetes infrastructure
**Use Airflow when**: Mixed workflows, existing Airflow infrastructure, more operational flexibility

</details>

---

### Question 10
In Kubeflow Pipelines, what does the `@dsl.component` decorator do?

A) Deploys a component to production
B) Converts a Python function into a reusable, containerized pipeline component
C) Schedules component execution
D) Validates component inputs

<details>
<summary>Answer</summary>

**B) Converts a Python function into a reusable, containerized pipeline component**

**Explanation**: `@dsl.component` creates lightweight components:

```python
@dsl.component(
    packages_to_install=['pandas==2.0.0', 'scikit-learn==1.3.0'],
    base_image='python:3.10-slim'
)
def preprocess_data(
    input_data: Input[Dataset],
    output_data: Output[Dataset],
    scaler_type: str = 'standard'
):
    import pandas as pd
    from sklearn.preprocessing import StandardScaler
    # Component logic here
```

**What happens**:
1. Function wrapped into container specification
2. Dependencies installed at runtime
3. Inputs/outputs typed and validated
4. Component reusable across pipelines

**Benefits**:
- No Dockerfile needed (for simple components)
- Dependency isolation
- Type safety
- Automatic serialization/deserialization

**Alternative**: `@dsl.container_component` for custom Docker images with more control

</details>

---

### Question 11
Analyze this Kubeflow pipeline component:

```python
@dsl.component
def train_model(
    dataset: Input[Dataset],
    model: Output[Model],
    metrics: Output[Metrics],
) -> float:
    # Training code
    accuracy = 0.92
    metrics.log_metric('accuracy', accuracy)
    return accuracy
```

How does the component communicate its results?

A) Only via return value
B) Only via Output[Metrics]
C) Both via return value and Output parameters
D) Results are not communicated

<details>
<summary>Answer</summary>

**C) Both via return value and Output parameters**

**Explanation**: Kubeflow components have multiple output mechanisms:

**1. Return values**:
```python
return accuracy  # Simple scalar values
```
- Passed to downstream components
- Accessible via component outputs

**2. Output parameters** (`Output[Dataset]`, `Output[Model]`, `Output[Metrics]`):
```python
metrics.log_metric('accuracy', accuracy)  # Logged to Kubeflow UI
model.path  # Artifact stored persistently
```
- Artifacts stored in object storage
- Metadata tracked in Kubeflow metadata store
- Visible in Kubeflow UI

**Usage in pipeline**:
```python
train_task = train_model(dataset=load_task.outputs['dataset'])
accuracy = train_task.outputs['Output']  # Return value
model_artifact = train_task.outputs['model']  # Output[Model]
```

**Best practices**:
- Use return values for scalar metrics/decisions
- Use Output[Model] for model artifacts
- Use Output[Metrics] for UI visualization
- Use Output[Dataset] for intermediate datasets

</details>

---

### Question 12
What is the purpose of `Input[Dataset]` and `Output[Dataset]` type hints in Kubeflow?

A) They are optional documentation
B) They enable type checking, artifact tracking, and automatic serialization
C) They only work with specific data formats
D) They are deprecated

<details>
<summary>Answer</summary>

**B) They enable type checking, artifact tracking, and automatic serialization**

**Explanation**: Typed inputs/outputs provide:

**Type Safety**:
- Compile-time validation
- Prevents incompatible connections
```python
# This would fail at compile time:
train_model(dataset=string_value)  # Error: expected Dataset, got str
```

**Artifact Tracking**:
- Automatic versioning
- Lineage tracking (which artifact produced which)
- Stored in persistent storage (S3, GCS)

**Automatic Serialization**:
- Data automatically saved/loaded
```python
# Component 1
output_dataset.path  # '/path/to/artifact'
df.to_csv(output_dataset.path)

# Component 2 (automatic loading)
df = pd.read_csv(input_dataset.path)
```

**Available types**:
- `Dataset`: Tabular data
- `Model`: ML models
- `Metrics`: Evaluation metrics
- `Artifact`: Generic artifacts
- `HTML`, `Markdown`: Visualization

**Example**:
```python
@dsl.component
def process(
    raw_data: Input[Dataset],      # Input artifact
    processed_data: Output[Dataset], # Output artifact
    num_rows: int                    # Simple parameter
) -> int:                            # Simple return value
    # Kubeflow handles artifact paths automatically
    df = pd.read_csv(raw_data.path)
    # ... processing ...
    df.to_csv(processed_data.path)
    return len(df)
```

</details>

---

### Question 13
**[Multiple Select]** Which statements about Kubeflow Pipelines are TRUE? (Select all that apply)

A) Each pipeline component runs in its own container
B) Pipelines must be compiled before execution
C) Kubeflow requires Kubernetes
D) Kubeflow can only run Python code
E) Kubeflow automatically tracks artifact lineage
F) Kubeflow pipelines cannot be scheduled

<details>
<summary>Answer</summary>

**A, B, C, E**

**Explanation**:
- **A**: ✓ Container-native execution, each component isolated
- **B**: ✓ Pipelines compiled to YAML/JSON spec before submission
  ```python
  compiler.Compiler().compile(pipeline_func, 'pipeline.yaml')
  ```
- **C**: ✓ Kubeflow Pipelines requires Kubernetes (runs as K8s pods)
- **D**: ✗ Supports any language via container components (Python, R, Go, etc.)
  ```python
  @dsl.container_component
  def r_component():
      return dsl.ContainerSpec(
          image='r-base:4.0',
          command=['Rscript', 'script.R']
      )
  ```
- **E**: ✓ Automatic artifact lineage tracking via metadata store
- **F**: ✗ Can be scheduled via:
  - Recurring runs in Kubeflow UI
  - External schedulers (Airflow can trigger Kubeflow)
  - Kubernetes CronJobs

</details>

---

### Question 14
How do you set resource requirements (CPU, memory, GPU) for a Kubeflow pipeline component?

A) Resource requirements are fixed per cluster
B) Use `.set_cpu_limit()`, `.set_memory_limit()`, `.set_gpu_limit()` on task
C) Modify Kubernetes cluster settings
D) Resources cannot be customized

<details>
<summary>Answer</summary>

**B) Use `.set_cpu_limit()`, `.set_memory_limit()`, `.set_gpu_limit()` on task**

**Explanation**: Resource configuration:

```python
@dsl.pipeline(name='Resource Demo')
def pipeline():
    # Lightweight preprocessing
    preprocess_task = preprocess_data()
    preprocess_task.set_cpu_limit('1')
    preprocess_task.set_memory_limit('2G')
    preprocess_task.set_cpu_request('500m')
    preprocess_task.set_memory_request('1G')

    # Heavy training job
    train_task = train_model()
    train_task.set_cpu_limit('8')
    train_task.set_memory_limit('32G')
    train_task.set_gpu_limit('2')  # Request 2 GPUs

    # Set accelerator type
    train_task.set_accelerator_type('nvidia.com/gpu')
```

**Key concepts**:
- **Requests**: Minimum guaranteed resources
- **Limits**: Maximum allowed resources
- **GPU**: Requires GPU-enabled Kubernetes nodes

**Best practices**:
- Set requests lower than limits for flexibility
- Match resource needs to avoid waste
- Use GPU only for components that need it
- Monitor actual usage and adjust

**Resource units**:
- CPU: Cores (e.g., '2' = 2 cores, '500m' = 0.5 cores)
- Memory: '1G', '512M', '2Gi' (binary), '2G' (decimal)
- GPU: Integer count

</details>

---

## Section 3: Error Handling & Retry Logic (Questions 15-20)

### Question 15
What is exponential backoff in retry logic, and why is it important?

A) Retrying immediately after each failure
B) Increasing delay between retries (e.g., 1s, 2s, 4s, 8s) to avoid overwhelming systems
C) Retrying a decreasing number of times
D) Only retrying exponential functions

<details>
<summary>Answer</summary>

**B) Increasing delay between retries (e.g., 1s, 2s, 4s, 8s) to avoid overwhelming systems**

**Explanation**: Exponential backoff pattern:

**Problem with immediate retries**:
- System overload during outages
- "Thundering herd" problem
- Rate limit violations
- No time for recovery

**Exponential backoff solution**:
```python
delay = initial_delay * (backoff_factor ** attempt)
# Attempt 0: 1s
# Attempt 1: 2s
# Attempt 2: 4s
# Attempt 3: 8s
```

**Implementation with jitter**:
```python
import random
import time

def retry_with_backoff(func, max_retries=5, initial_delay=1, backoff_factor=2):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise

            delay = initial_delay * (backoff_factor ** attempt)
            jitter = random.uniform(0, delay * 0.1)  # Add 10% jitter
            sleep_time = delay + jitter

            print(f"Retry {attempt + 1}/{max_retries} after {sleep_time:.2f}s")
            time.sleep(sleep_time)
```

**Why jitter**:
- Prevents synchronized retries
- Spreads load over time
- Reduces collision probability

**When to use**:
- External API calls
- Database connections
- Network operations
- Rate-limited services

**Airflow configuration**:
```python
default_args = {
    'retries': 5,
    'retry_delay': timedelta(seconds=30),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(minutes=10),
}
```

</details>

---

### Question 16
What is a Circuit Breaker pattern, and when should it be used in ML pipelines?

A) A safety mechanism for electrical circuits
B) A pattern that prevents repeated calls to failing services by "opening" after threshold
C) A way to break infinite loops
D) A database transaction mechanism

<details>
<summary>Answer</summary>

**B) A pattern that prevents repeated calls to failing services by "opening" after threshold**

**Explanation**: Circuit breaker pattern protects systems from cascading failures:

**States**:
1. **CLOSED** (normal operation):
   - All requests pass through
   - Failures tracked

2. **OPEN** (service failing):
   - Requests immediately fail without calling service
   - Prevents resource waste
   - Entered after failure threshold exceeded

3. **HALF_OPEN** (recovery testing):
   - Allow limited requests through
   - Test if service recovered
   - Close if successful, reopen if failed

**Implementation**:
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = None
        self.state = 'CLOSED'

    def call(self, func):
        if self.state == 'OPEN':
            if self._should_attempt_reset():
                self.state = 'HALF_OPEN'
            else:
                raise Exception("Circuit breaker OPEN")

        try:
            result = func()
            if self.state == 'HALF_OPEN':
                self._reset()  # Close circuit
            return result
        except Exception as e:
            self._record_failure()
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
            raise

# Usage in ML pipeline
breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=60)

def fetch_data_from_api():
    return breaker.call(lambda: requests.get('https://api.example.com/data'))
```

**When to use in ML pipelines**:
- External data sources (APIs, databases)
- Model serving endpoints
- Feature stores
- Third-party ML services (e.g., OpenAI API)

**Benefits**:
- Fail fast instead of waiting for timeouts
- Prevent resource exhaustion
- Automatic recovery detection
- Graceful degradation

</details>

---

### Question 17
Analyze this error handling code:

```python
def train_model(**context):
    try:
        model = train()
        save_model(model)
    except MemoryError:
        # Reduce batch size and retry
        model = train(batch_size=32)
        save_model(model)
    except ModelNotConvergingError:
        # Skip this training run
        raise AirflowSkipException("Model did not converge")
    except Exception as e:
        # Log and fail
        logging.error(f"Training failed: {e}")
        raise
```

What happens if training fails with MemoryError?

A) Task fails immediately
B) Task reduces batch size and retries once (within same task execution)
C) Task skips
D) Task retries 3 times with same parameters

<details>
<summary>Answer</summary>

**B) Task reduces batch size and retries once (within same task execution)**

**Explanation**: Exception handling flow:

**MemoryError**:
```python
except MemoryError:
    model = train(batch_size=32)  # Retry with smaller batch
    save_model(model)
```
- Caught and handled within task
- Retries ONCE with reduced batch size
- If second attempt succeeds, task succeeds
- If second attempt fails, exception propagates to outer `except Exception`

**ModelNotConvergingError**:
```python
except ModelNotConvergingError:
    raise AirflowSkipException("Model did not converge")
```
- Task marked as "skipped" (not failed)
- Downstream tasks with `trigger_rule='all_success'` won't run
- Downstream tasks with `trigger_rule='none_failed'` will run

**Other Exceptions**:
```python
except Exception as e:
    logging.error(f"Training failed: {e}")
    raise
```
- Logged and re-raised
- Task marked as failed
- Airflow retry mechanism kicks in (if configured)

**Better approach** - distinguish retryable vs non-retryable:
```python
from airflow.exceptions import AirflowException

class RetryableTrainingError(AirflowException):
    pass

def train_model(**context):
    try:
        model = train()
    except MemoryError:
        raise RetryableTrainingError("OOM - reduce batch size")
    except ModelNotConvergingError:
        raise AirflowSkipException("Non-convergence")
    except ValidationError:
        raise AirflowException("Invalid data - won't retry")
```

</details>

---

### Question 18
**[Multiple Select]** Which scenarios should trigger automatic retry in an ML pipeline? (Select all that apply)

A) Database connection timeout
B) Data validation failure (schema mismatch)
C) HTTP 503 Service Unavailable from API
D) Model accuracy below threshold
E) Network timeout
F) Division by zero in feature calculation

<details>
<summary>Answer</summary>

**A, C, E**

**Explanation**:

**Should retry (transient errors)**:
- **A) Database timeout**: ✓ Temporary connectivity issue, likely to succeed on retry
- **C) HTTP 503**: ✓ Service temporarily unavailable, may recover
- **E) Network timeout**: ✓ Transient network issue

**Should NOT retry (permanent errors)**:
- **B) Schema mismatch**: ✗ Data pipeline issue, retrying won't fix
  - **Action**: Alert data team, skip or fail pipeline
- **D) Low accuracy**: ✗ Model quality issue, not a failure
  - **Action**: Decision logic, not retry
- **F) Division by zero**: ✗ Code or data bug, retrying won't help
  - **Action**: Fix code or data quality checks

**Classification of errors**:

**Transient (retry)**:
- Network failures
- Timeouts
- Rate limiting (429)
- Service unavailable (503)
- Resource temporarily unavailable
- Deadlocks

**Permanent (don't retry)**:
- Validation errors (400 Bad Request)
- Authentication failures (401, 403)
- Not found (404)
- Data quality issues
- Code bugs
- Configuration errors

**Implementation**:
```python
from requests.exceptions import Timeout, ConnectionError

RETRYABLE_EXCEPTIONS = (
    Timeout,
    ConnectionError,
    TemporaryDatabaseError,
)

@retry_with_backoff(exceptions=RETRYABLE_EXCEPTIONS)
def fetch_data():
    response = requests.get(url, timeout=30)
    if response.status_code == 503:
        raise TemporaryServiceError("Service unavailable")
    if response.status_code == 400:
        raise PermanentError("Bad request - won't retry")
    return response.json()
```

</details>

---

### Question 19
What is the purpose of the `trigger_rule` parameter in Airflow tasks?

A) To trigger external webhooks
B) To define when a task should run based on upstream task states
C) To schedule task execution time
D) To set retry conditions

<details>
<summary>Answer</summary>

**B) To define when a task should run based on upstream task states**

**Explanation**: Trigger rules determine task execution logic:

**Common trigger rules**:

**1. `all_success` (default)**:
```python
task = PythonOperator(
    task_id='process_data',
    trigger_rule='all_success'  # All upstream tasks must succeed
)
```
- Runs only if ALL upstream tasks succeeded
- Most common for sequential pipelines

**2. `all_failed`**:
```python
alert_task = EmailOperator(
    task_id='send_failure_alert',
    trigger_rule='all_failed'  # All upstream tasks failed
)
```
- Runs only if ALL upstream tasks failed
- Use for failure-specific logic

**3. `one_failed`**:
```python
cleanup_task = PythonOperator(
    task_id='cleanup',
    trigger_rule='one_failed'  # At least one upstream failed
)
```
- Runs if ANY upstream task failed
- Use for cleanup after failures

**4. `none_failed`**:
```python
report_task = PythonOperator(
    task_id='generate_report',
    trigger_rule='none_failed'  # No upstream failures
)
```
- Runs if no upstream tasks failed
- Upstream tasks can be success or skipped
- Use after branching (where some tasks skip)

**5. `all_done`**:
```python
final_task = PythonOperator(
    task_id='finalize',
    trigger_rule='all_done'  # All upstream completed
)
```
- Runs when all upstream tasks finished (success, failed, or skipped)
- Use for final cleanup/logging

**Example with branching**:
```python
check_quality >> [good_quality_branch, bad_quality_branch]
[good_quality_branch, bad_quality_branch] >> report_task

# report_task needs trigger_rule='none_failed'
# because one branch will skip
```

**Other rules**:
- `none_skipped`: All succeeded, none skipped
- `one_success`: At least one succeeded
- `dummy`: Always runs

</details>

---

### Question 20
How should you handle data quality failures in an ML pipeline?

A) Always retry automatically
B) Fail the pipeline immediately without investigation
C) Log the issue, alert the data team, and either skip or fail based on severity
D) Ignore and continue with bad data

<details>
<summary>Answer</summary>

**C) Log the issue, alert the data team, and either skip or fail based on severity**

**Explanation**: Data quality failure handling strategy:

**Step 1: Detect and classify**:
```python
class DataQualityIssue:
    CRITICAL = 'critical'    # Pipeline must fail
    WARNING = 'warning'      # Can continue with degraded performance
    INFO = 'info'           # Monitor but not blocking

def validate_data(df):
    issues = []

    # Critical: Schema mismatch
    if not validate_schema(df):
        issues.append((DataQualityIssue.CRITICAL, "Schema mismatch"))

    # Warning: High missing values
    missing_pct = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
    if missing_pct > 0.3:
        issues.append((DataQualityIssue.WARNING, f"Missing values: {missing_pct:.1%}"))

    # Info: Slight distribution drift
    if detect_minor_drift(df):
        issues.append((DataQualityIssue.INFO, "Minor drift detected"))

    return issues
```

**Step 2: Handle based on severity**:
```python
def process_data(**context):
    df = load_data()
    issues = validate_data(df)

    critical_issues = [i for i in issues if i[0] == DataQualityIssue.CRITICAL]
    warning_issues = [i for i in issues if i[0] == DataQualityIssue.WARNING]

    if critical_issues:
        # Fail pipeline
        send_alert(f"CRITICAL data quality issues: {critical_issues}")
        raise DataQualityException(f"Cannot proceed: {critical_issues}")

    if warning_issues:
        # Continue but alert
        send_alert(f"WARNING data quality issues: {warning_issues}")
        context['task_instance'].xcom_push(key='data_quality_warnings', value=warning_issues)
        # Continue with degraded data

    return df
```

**Step 3: Logging and alerting**:
```python
def send_data_quality_alert(issues):
    alert_message = {
        'timestamp': datetime.now(),
        'pipeline': 'ml_training',
        'issues': issues,
        'action_required': 'yes' if any(i[0] == 'critical' for i in issues) else 'no'
    }

    # Log to monitoring system
    log_to_prometheus(alert_message)

    # Send to data team
    send_slack_message(channel='#data-quality', message=alert_message)

    # Create Jira ticket for critical issues
    if any(i[0] == 'critical' for i in issues):
        create_jira_ticket(summary="Critical data quality issue", description=issues)
```

**Best practices**:
1. **Never silently ignore** data quality issues
2. **Classify severity** - not all issues are equal
3. **Alert appropriate team** - data team, not just ML team
4. **Track over time** - log to monitoring system
5. **Decide gracefully** - skip training vs fail vs continue with warning
6. **Document expectations** - what's acceptable data quality?

**Example decision tree**:
- Schema mismatch → FAIL (critical)
- 50%+ missing values → FAIL (critical)
- 10-30% missing values → WARN and CONTINUE (warning)
- <10% missing values → LOG (info)
- No recent data → SKIP training (warning)

</details>

---

## Section 4: MLflow Integration (Questions 21-25)

### Question 21
How should you track experiment runs in an orchestrated pipeline?

A) Each pipeline run creates one MLflow experiment
B) Each task creates a separate MLflow experiment
C) Create a parent MLflow run for the pipeline, with nested runs for each component
D) MLflow tracking is not compatible with orchestration

<details>
<summary>Answer</summary>

**C) Create a parent MLflow run for the pipeline, with nested runs for each component**

**Explanation**: Hierarchical run tracking provides best organization:

**Parent run (pipeline level)**:
```python
def initialize_pipeline(**context):
    mlflow.set_experiment("ml_training_pipeline")

    # Start parent run
    with mlflow.start_run(run_name=f"pipeline_{context['ds']}") as parent_run:
        parent_run_id = parent_run.info.run_id

        # Log pipeline metadata
        mlflow.log_params({
            'pipeline_id': context['dag'].dag_id,
            'execution_date': context['ds'],
            'triggered_by': context.get('dag_run').external_trigger
        })

        # Store parent run ID for child runs
        context['task_instance'].xcom_push(key='parent_run_id', value=parent_run_id)

        return parent_run_id
```

**Child runs (task level)**:
```python
def train_model(**context):
    ti = context['task_instance']
    parent_run_id = ti.xcom_pull(task_ids='initialize_pipeline', key='parent_run_id')

    # Create nested run
    with mlflow.start_run(run_id=parent_run_id):
        with mlflow.start_run(run_name="training_task", nested=True):
            # Log training parameters and metrics
            mlflow.log_params({'n_estimators': 100, 'max_depth': 10})

            model = train()
            accuracy = evaluate(model)

            mlflow.log_metric('accuracy', accuracy)
            mlflow.sklearn.log_model(model, "model")
```

**Benefits**:
- **Hierarchy**: Easily see all components of a pipeline run
- **Traceability**: Link models to specific pipeline executions
- **Comparison**: Compare entire pipeline runs
- **Debugging**: Identify which component failed

**MLflow UI view**:
```
Pipeline Run 2024-01-15
├── Training Task (nested)
│   ├── Parameters: n_estimators=100, max_depth=10
│   ├── Metrics: accuracy=0.92
│   └── Artifacts: model/
├── Evaluation Task (nested)
│   └── Metrics: test_accuracy=0.91
└── Model Registration Task (nested)
    └── Tags: model_version=3
```

**Alternative** (separate runs with tags):
```python
# Less organized but simpler
with mlflow.start_run():
    mlflow.set_tags({
        'pipeline_id': dag_id,
        'execution_date': ds,
        'task': 'training'
    })
```

</details>

---

### Question 22
What is the correct way to retrieve and compare model metrics from previous pipeline runs?

A) Manually check MLflow UI
B) Use MLflow Search API to query and compare runs programmatically
C) Store metrics in a separate database
D) Metrics cannot be compared automatically

<details>
<summary>Answer</summary>

**B) Use MLflow Search API to query and compare runs programmatically**

**Explanation**: Programmatic run comparison:

**Search for runs**:
```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Get experiment by name
experiment = mlflow.get_experiment_by_name("ml_training_pipeline")

# Search runs with filters
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    filter_string="params.model_type = 'random_forest' AND metrics.accuracy > 0.85",
    order_by=["metrics.accuracy DESC"],
    max_results=10
)

for run in runs:
    print(f"Run ID: {run.info.run_id}")
    print(f"Accuracy: {run.data.metrics['accuracy']}")
    print(f"Date: {run.info.start_time}")
```

**Compare current with production**:
```python
def compare_with_production(current_run_id, model_name):
    client = MlflowClient()

    # Get current run metrics
    current_run = client.get_run(current_run_id)
    current_accuracy = current_run.data.metrics.get('accuracy', 0)

    # Get production model
    prod_versions = client.get_latest_versions(
        name=model_name,
        stages=["Production"]
    )

    if not prod_versions:
        return {"improvement": float('inf'), "should_promote": True}

    # Get production run metrics
    prod_run = client.get_run(prod_versions[0].run_id)
    prod_accuracy = prod_run.data.metrics.get('accuracy', 0)

    # Calculate improvement
    improvement = ((current_accuracy - prod_accuracy) / prod_accuracy) * 100

    return {
        "current_accuracy": current_accuracy,
        "production_accuracy": prod_accuracy,
        "improvement_pct": improvement,
        "should_promote": improvement > 2.0  # 2% threshold
    }
```

**Automated decision making**:
```python
def decide_model_promotion(**context):
    ti = context['task_instance']
    current_run_id = ti.xcom_pull(task_ids='train_model', key='run_id')

    comparison = compare_with_production(current_run_id, "production_model")

    if comparison['should_promote']:
        logging.info(
            f"Promoting model: {comparison['improvement_pct']:.2f}% improvement"
        )
        return 'promote_model'
    else:
        logging.info(
            f"Not promoting: only {comparison['improvement_pct']:.2f}% improvement"
        )
        return 'skip_promotion'
```

**Advanced: Pandas DataFrame for analysis**:
```python
import pandas as pd

def get_run_history(experiment_name, last_n=30):
    client = MlflowClient()
    experiment = mlflow.get_experiment_by_name(experiment_name)

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time DESC"],
        max_results=last_n
    )

    # Convert to DataFrame
    data = []
    for run in runs:
        data.append({
            'run_id': run.info.run_id,
            'start_time': pd.to_datetime(run.info.start_time, unit='ms'),
            'accuracy': run.data.metrics.get('accuracy'),
            'f1_score': run.data.metrics.get('f1_score'),
            'n_estimators': run.data.params.get('n_estimators'),
            'max_depth': run.data.params.get('max_depth'),
        })

    df = pd.DataFrame(data)

    # Analyze trends
    accuracy_trend = df['accuracy'].rolling(window=5).mean()
    print(f"Recent average accuracy: {accuracy_trend.iloc[-1]:.4f}")

    return df
```

**Benefits**:
- Automated decision making
- Trend analysis
- Performance regression detection
- Historical comparison

</details>

---

### Question 23
Analyze this model promotion logic:

```python
def promote_model(**context):
    ti = context['task_instance']
    new_accuracy = ti.xcom_pull(task_ids='evaluate', key='accuracy')

    # Get current production model
    client = MlflowClient()
    prod_models = client.get_latest_versions("classifier", stages=["Production"])

    if prod_models:
        prod_run_id = prod_models[0].run_id
        prod_run = client.get_run(prod_run_id)
        prod_accuracy = prod_run.data.metrics['accuracy']

        if new_accuracy > prod_accuracy:
            # Promote new model
            register_and_promote(model_uri, "classifier")
    else:
        # No production model, promote
        register_and_promote(model_uri, "classifier")
```

What potential issue exists with this promotion logic?

A) It doesn't check if the model exists
B) It promotes based on any improvement, even tiny ones (no minimum threshold)
C) It doesn't handle errors
D) It uses the wrong MLflow client

<details>
<summary>Answer</summary>

**B) It promotes based on any improvement, even tiny ones (no minimum threshold)**

**Explanation**: The code promotes if `new_accuracy > prod_accuracy`, which means:
- 0.001% improvement triggers promotion
- Statistical noise could cause unnecessary promotions
- No consideration of variance or confidence intervals

**Problems**:
1. **Over-promotion**: Frequent, unnecessary model updates
2. **Deployment risk**: Each deployment has risk; not worth it for tiny gains
3. **No statistical significance**: Improvement might be random chance
4. **Operational cost**: Model deployment is expensive (testing, rollout, monitoring)

**Improved version**:
```python
def promote_model(**context):
    ti = context['task_instance']
    new_accuracy = ti.xcom_pull(task_ids='evaluate', key='accuracy')

    # Configuration
    MIN_IMPROVEMENT_PCT = 2.0  # Require 2% improvement
    ABSOLUTE_THRESHOLD = 0.85  # Minimum acceptable accuracy

    client = MlflowClient()
    prod_models = client.get_latest_versions("classifier", stages=["Production"])

    # Check absolute threshold
    if new_accuracy < ABSOLUTE_THRESHOLD:
        logging.warning(
            f"Model accuracy {new_accuracy:.4f} below threshold {ABSOLUTE_THRESHOLD}"
        )
        raise AirflowSkipException("Model does not meet minimum requirements")

    if prod_models:
        prod_run_id = prod_models[0].run_id
        prod_run = client.get_run(prod_run_id)
        prod_accuracy = prod_run.data.metrics['accuracy']

        # Calculate relative improvement
        improvement_pct = ((new_accuracy - prod_accuracy) / prod_accuracy) * 100

        logging.info(
            f"New: {new_accuracy:.4f}, Prod: {prod_accuracy:.4f}, "
            f"Improvement: {improvement_pct:.2f}%"
        )

        if improvement_pct >= MIN_IMPROVEMENT_PCT:
            logging.info("Promoting model - significant improvement detected")
            register_and_promote(model_uri, "classifier")
        else:
            logging.info(
                f"Not promoting - improvement {improvement_pct:.2f}% "
                f"< threshold {MIN_IMPROVEMENT_PCT}%"
            )
            raise AirflowSkipException("Insufficient improvement")
    else:
        logging.info("No production model - promoting first model")
        register_and_promote(model_uri, "classifier")
```

**Additional improvements**:
1. **Multi-metric comparison**:
   ```python
   # Consider multiple metrics
   metrics = ['accuracy', 'precision', 'recall', 'f1']
   improvements = []
   for metric in metrics:
       new_val = new_run.metrics[metric]
       prod_val = prod_run.metrics[metric]
       improvements.append((new_val - prod_val) / prod_val * 100)

   avg_improvement = np.mean(improvements)
   ```

2. **Statistical testing**:
   ```python
   # Use confidence intervals
   from scipy import stats

   # Compare with statistical significance
   t_stat, p_value = stats.ttest_ind(new_scores, prod_scores)
   if p_value < 0.05 and avg_improvement > threshold:
       promote()
   ```

3. **Business impact consideration**:
   ```python
   # Estimate business value
   improvement_value = estimate_revenue_impact(improvement_pct)
   deployment_cost = 10000  # USD

   if improvement_value > deployment_cost:
       promote()
   ```

</details>

---

### Question 24
**[Multiple Select]** What should be logged to MLflow in an automated training pipeline? (Select all that apply)

A) Hyperparameters
B) Training and validation metrics
C) Model artifacts
D) Training data (entire dataset)
E) Environment dependencies (requirements.txt)
F) Git commit hash
G) Execution logs

<details>
<summary>Answer</summary>

**A, B, C, E, F, G**

**Explanation**:

**Should log**:

**A) Hyperparameters**: ✓
```python
mlflow.log_params({
    'n_estimators': 100,
    'max_depth': 10,
    'learning_rate': 0.01
})
```
- Essential for reproducibility
- Enables hyperparameter analysis

**B) Metrics**: ✓
```python
mlflow.log_metrics({
    'train_accuracy': 0.95,
    'val_accuracy': 0.92,
    'test_accuracy': 0.91
})
```
- Track performance
- Compare models

**C) Model artifacts**: ✓
```python
mlflow.sklearn.log_model(model, "model")
mlflow.log_artifact("confusion_matrix.png")
```
- Model deployment
- Reproducibility

**E) Environment dependencies**: ✓
```python
mlflow.log_artifact("requirements.txt")
mlflow.log_dict(conda_env, "conda.yaml")
```
- Reproducible environments
- Dependency tracking

**F) Git commit hash**: ✓
```python
import subprocess
commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
mlflow.set_tag('git_commit', commit_hash)
mlflow.set_tag('git_branch', 'main')
```
- Code version tracking
- Reproducibility

**G) Execution logs**: ✓
```python
with open('training.log', 'w') as f:
    # Log training output
    pass
mlflow.log_artifact('training.log')
```
- Debugging
- Audit trail

**Should NOT log**:

**D) Training data**: ✗
- Too large for MLflow
- Use data versioning tools (DVC, Delta Lake)
- Log data reference instead:
```python
mlflow.log_param('data_version', 'v2.3.1')
mlflow.log_param('data_path', 's3://bucket/data/train_20240115.csv')
mlflow.log_param('data_hash', 'sha256:abc123...')
```

**Complete example**:
```python
def train_with_tracking(**context):
    # Get git info
    git_commit = get_git_commit()
    git_branch = get_git_branch()

    with mlflow.start_run():
        # Log code version
        mlflow.set_tags({
            'git_commit': git_commit,
            'git_branch': git_branch,
            'pipeline_id': context['dag'].dag_id,
            'execution_date': context['ds']
        })

        # Log hyperparameters
        params = {'n_estimators': 100, 'max_depth': 10}
        mlflow.log_params(params)

        # Log data reference
        mlflow.log_params({
            'data_version': 'v2.3.1',
            'data_path': 's3://bucket/data.csv',
            'data_samples': 100000
        })

        # Train model
        model = train(params)

        # Log metrics
        metrics = evaluate(model)
        mlflow.log_metrics(metrics)

        # Log model
        mlflow.sklearn.log_model(
            model,
            "model",
            conda_env={
                'dependencies': [
                    'python=3.10',
                    'scikit-learn==1.3.0',
                    'pandas==2.0.0'
                ]
            }
        )

        # Log artifacts
        mlflow.log_artifact('confusion_matrix.png')
        mlflow.log_artifact('feature_importance.png')
        mlflow.log_artifact('requirements.txt')
```

</details>

---

### Question 25
How should you handle MLflow tracking when a pipeline task fails and retries?

A) Each retry creates a new MLflow run
B) Resume the same MLflow run across retries
C) Don't log failed attempts to MLflow
D) Log all attempts including failures with appropriate tags

<details>
<summary>Answer</summary>

**D) Log all attempts including failures with appropriate tags**

**Explanation**: Comprehensive tracking of all attempts provides valuable insights:

**Implementation**:
```python
def train_model_with_retry_tracking(**context):
    ti = context['task_instance']
    attempt_number = ti.try_number  # Current attempt (1, 2, 3, ...)

    mlflow.set_experiment("ml_training_pipeline")

    run_name = f"train_{context['ds']}_attempt_{attempt_number}"

    with mlflow.start_run(run_name=run_name) as run:
        # Tag with attempt information
        mlflow.set_tags({
            'attempt_number': attempt_number,
            'task_id': ti.task_id,
            'dag_id': context['dag'].dag_id,
            'execution_date': context['ds'],
            'is_retry': attempt_number > 1
        })

        try:
            # Training logic
            model = train()
            metrics = evaluate(model)

            # Log success
            mlflow.log_metrics(metrics)
            mlflow.sklearn.log_model(model, "model")
            mlflow.set_tag('status', 'success')

            # Store successful run ID
            ti.xcom_push(key='successful_run_id', value=run.info.run_id)

            return metrics

        except Exception as e:
            # Log failure details
            mlflow.set_tag('status', 'failed')
            mlflow.set_tag('error_type', type(e).__name__)
            mlflow.log_param('error_message', str(e))

            # Log partial results if any
            if 'metrics' in locals():
                mlflow.log_metrics(metrics)

            # Re-raise for Airflow retry logic
            raise
```

**Benefits of logging all attempts**:

1. **Debugging**:
   - See what failed and when
   - Identify patterns (always fails on 1st attempt?)
   - Understand error frequency

2. **Performance analysis**:
   - Compare metrics across attempts
   - Detect non-determinism
   - Identify if retries improve results

3. **Cost tracking**:
   - Count total compute used (including retries)
   - Optimize retry strategy

4. **Audit trail**:
   - Complete history
   - Compliance requirements

**Alternative: Single run with attempt tracking**:
```python
def train_model_single_run(**context):
    ti = context['task_instance']
    attempt = ti.try_number

    # Use consistent run ID across retries (stored in XCom)
    if attempt == 1:
        # First attempt: create new run
        active_run = mlflow.start_run()
        run_id = active_run.info.run_id
        ti.xcom_push(key='mlflow_run_id', value=run_id)
    else:
        # Retry: resume existing run
        run_id = ti.xcom_pull(key='mlflow_run_id')
        active_run = mlflow.start_run(run_id=run_id)

    with active_run:
        # Log attempt-specific metrics
        mlflow.log_metric(f'attempt_{attempt}_duration', duration)
        mlflow.log_param(f'attempt_{attempt}_timestamp', datetime.now())

        try:
            # Training
            model = train()
            mlflow.log_metric('final_accuracy', accuracy)
            mlflow.set_tag('successful_attempt', attempt)
        except Exception as e:
            mlflow.log_param(f'attempt_{attempt}_error', str(e))
            raise
```

**Query failed runs for analysis**:
```python
# Find runs that failed and were retried
failed_runs = client.search_runs(
    experiment_ids=[exp_id],
    filter_string="tags.status = 'failed' AND tags.is_retry = 'True'"
)

print(f"Found {len(failed_runs)} failed retry attempts")

# Analyze common failure patterns
for run in failed_runs:
    print(f"Error: {run.data.params.get('error_message')}")
```

</details>

---

## Section 5: Best Practices & Production (Questions 26-30)

### Question 26
What is the recommended strategy for scheduling ML training pipelines in production?

A) Run training on every new data point
B) Fixed schedule (daily/weekly) regardless of performance
C) Event-driven + scheduled with performance-based triggers
D) Manual triggering only

<details>
<summary>Answer</summary>

**C) Event-driven + scheduled with performance-based triggers**

**Explanation**: Multi-trigger approach combines reliability with efficiency:

**1. Scheduled baseline** (weekly/monthly):
```python
dag = DAG(
    'ml_training',
    schedule_interval='@weekly',  # Baseline: weekly training
    catchup=False
)
```
- Ensures regular model updates
- Captures slow-moving drift
- Predictable resource usage

**2. Event-driven triggers** (data-based):
```python
# Trigger when new labeled data available
data_sensor = ExternalTaskSensor(
    task_id='wait_for_new_data',
    external_dag_id='data_labeling_pipeline',
    external_task_id='export_labels',
    mode='reschedule'
)

# Trigger when data volume threshold met
def check_data_volume(**context):
    new_samples = count_new_samples_since_last_training()
    threshold = 10000

    if new_samples >= threshold:
        return 'trigger_training'
    else:
        return 'skip_training'

check_volume = BranchPythonOperator(
    task_id='check_data_volume',
    python_callable=check_data_volume
)
```

**3. Performance-based triggers** (drift/degradation):
```python
# Separate monitoring DAG triggers training
monitoring_dag = DAG(
    'model_monitoring',
    schedule_interval='@daily'
)

def check_model_performance(**context):
    current_accuracy = get_production_accuracy()
    drift_score = calculate_drift()

    # Trigger training if performance drops or drift detected
    if current_accuracy < 0.85 or drift_score > 0.3:
        trigger_dag_run(
            dag_id='ml_training',
            execution_date=context['execution_date'],
            conf={'trigger_reason': 'performance_degradation'}
        )
```

**Complete strategy**:
```python
# Primary training DAG
training_dag = DAG(
    'ml_training',
    schedule_interval='@weekly',  # Baseline
    catchup=False
)

# Multiple trigger conditions
def should_train(**context):
    """Determine if training should proceed."""

    # Check if triggered by monitoring
    if context['dag_run'].conf.get('trigger_reason') == 'performance_degradation':
        return True

    # Check data volume
    new_samples = count_new_labeled_samples()
    if new_samples >= 10000:
        logging.info(f"Training triggered: {new_samples} new samples")
        return True

    # Check time since last successful training
    days_since_training = get_days_since_last_training()
    if days_since_training >= 30:  # Force retraining after 1 month
        logging.info(f"Training triggered: {days_since_training} days since last training")
        return True

    # Check drift
    drift_score = calculate_drift()
    if drift_score > 0.3:
        logging.info(f"Training triggered: drift score {drift_score}")
        return True

    return False

with training_dag:
    check_should_train = BranchPythonOperator(
        task_id='check_should_train',
        python_callable=should_train
    )

    train_task = PythonOperator(task_id='train_model', ...)
    skip_task = DummyOperator(task_id='skip_training')

    check_should_train >> [train_task, skip_task]
```

**Anti-patterns**:
- **Too frequent**: Training on every data point (expensive, unnecessary)
- **Too rigid**: Only scheduled, ignoring performance issues
- **Too reactive**: Only event-driven, may miss gradual drift
- **Manual only**: Requires human intervention, not scalable

**Resource considerations**:
```python
# Rate limiting to prevent resource exhaustion
def can_start_training(**context):
    # Check if another training is running
    if is_training_already_running():
        raise AirflowSkipException("Training already in progress")

    # Check resource availability
    if not check_gpu_availability():
        raise AirflowSkipException("No GPUs available")

    return True
```

</details>

---

### Question 27
**[Multiple Select]** What should be included in a production ML pipeline? (Select all that apply)

A) Automated data quality validation
B) Model performance monitoring
C) Automated rollback on failure
D) Manual approval gates for production deployment
E) Comprehensive logging and alerting
F) Cost tracking and optimization

<details>
<summary>Answer</summary>

**A, B, C, D, E, F** (All of them)

**Explanation**: Production-grade ML pipelines require comprehensive safety and observability:

**A) Data quality validation**: ✓
```python
validate_data = PythonOperator(
    task_id='validate_data_quality',
    python_callable=validate_schema_and_quality
)
# Fail early if data is bad
```
- Schema validation
- Distribution checks
- Missing value detection
- Outlier detection

**B) Model performance monitoring**: ✓
```python
monitor_model = PythonOperator(
    task_id='monitor_production_model',
    python_callable=check_production_metrics
)
# Track accuracy, latency, drift
```
- Real-time accuracy tracking
- Drift detection
- Latency monitoring
- A/B test analysis

**C) Automated rollback**: ✓
```python
def deploy_with_rollback(**context):
    try:
        deploy_new_model()

        # Monitor for 1 hour
        if check_metrics_degraded():
            rollback_to_previous_model()
            raise AirflowException("Metrics degraded - rolled back")
    except Exception as e:
        rollback_to_previous_model()
        raise
```
- Automatic rollback on errors
- Performance-based rollback
- Preserves last known good state

**D) Manual approval gates**: ✓
```python
from airflow.sensors.external_task import ExternalTaskSensor

approval_gate = ExternalTaskSensor(
    task_id='wait_for_approval',
    external_dag_id='approval_workflow',
    mode='reschedule'
)
# Human approval before production
```
- Human verification
- Risk mitigation
- Compliance requirements

**E) Comprehensive logging/alerting**: ✓
```python
def train_with_logging(**context):
    logger = setup_structured_logging()

    try:
        model = train()
        logger.info("Training succeeded", extra={
            'accuracy': accuracy,
            'duration': duration
        })
    except Exception as e:
        logger.error("Training failed", extra={
            'error': str(e),
            'stack_trace': traceback.format_exc()
        })
        send_alert(severity='HIGH', message=f"Training failed: {e}")
        raise
```
- Structured logging
- Error alerts
- Performance metrics
- Audit trails

**F) Cost tracking**: ✓
```python
def track_training_cost(**context):
    start_time = context['task_instance'].start_date
    end_time = datetime.now()

    # Calculate compute cost
    gpu_hours = (end_time - start_time).total_seconds() / 3600
    cost_per_gpu_hour = 2.50
    total_cost = gpu_hours * cost_per_gpu_hour

    # Log to monitoring
    mlflow.log_metric('training_cost_usd', total_cost)
    log_to_cost_tracking(
        pipeline='ml_training',
        cost=total_cost,
        date=context['ds']
    )
```
- Compute cost tracking
- Resource optimization
- Budget alerts

**Complete production pipeline structure**:
```python
with dag:
    # 1. Data validation
    validate = validate_data_quality()

    # 2. Training with tracking
    train = train_model_with_mlflow()

    # 3. Evaluation
    evaluate = evaluate_model()

    # 4. Performance check (automated gate)
    check_perf = check_performance_threshold()

    # 5. Cost analysis
    analyze_cost = calculate_training_cost()

    # 6. Staging deployment
    deploy_staging = deploy_to_staging()

    # 7. Integration tests
    test_staging = run_integration_tests()

    # 8. Manual approval (human gate)
    approval = wait_for_approval()

    # 9. Production deployment with canary
    deploy_prod = canary_deploy_to_production()

    # 10. Monitor and auto-rollback
    monitor = monitor_and_rollback()

    # 11. Cleanup
    cleanup = cleanup_resources()

    validate >> train >> evaluate >> check_perf
    [check_perf, analyze_cost] >> deploy_staging >> test_staging
    test_staging >> approval >> deploy_prod >> monitor >> cleanup
```

</details>

---

### Question 28
How should you handle pipeline versioning and reproducibility?

A) Versioning is not necessary
B) Only version the final model
C) Version code, data, environment, and pipeline configuration
D) Use timestamps only

<details>
<summary>Answer</summary>

**C) Version code, data, environment, and pipeline configuration**

**Explanation**: Comprehensive versioning ensures reproducibility:

**1. Code versioning** (Git):
```python
import subprocess

def get_git_info():
    commit = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD']
    ).decode('ascii').strip()

    branch = subprocess.check_output(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
    ).decode('ascii').strip()

    # Check for uncommitted changes
    status = subprocess.check_output(
        ['git', 'status', '--porcelain']
    ).decode('ascii')

    dirty = len(status) > 0

    return {
        'git_commit': commit,
        'git_branch': branch,
        'git_dirty': dirty  # Warn if uncommitted changes
    }

# Log to MLflow
git_info = get_git_info()
mlflow.log_params(git_info)

if git_info['git_dirty']:
    logging.warning("Uncommitted changes detected - not fully reproducible!")
```

**2. Data versioning** (DVC, Delta Lake):
```python
# Using DVC
def get_data_version():
    # Data tracked with DVC
    data_dvc_file = 'data/train.csv.dvc'

    with open(data_dvc_file) as f:
        dvc_info = yaml.safe_load(f)

    return {
        'data_md5': dvc_info['md5'],
        'data_size': dvc_info['size'],
        'data_path': dvc_info['path']
    }

# Log to MLflow
data_info = get_data_version()
mlflow.log_params(data_info)

# Alternative: Data versioning with timestamps/hashes
data_version = f"v_{datetime.now().strftime('%Y%m%d')}_{data_hash[:8]}"
mlflow.log_param('data_version', data_version)
```

**3. Environment versioning**:
```python
# Conda environment
conda_env = {
    'name': 'ml_training',
    'channels': ['conda-forge', 'defaults'],
    'dependencies': [
        'python=3.10.8',
        'scikit-learn==1.3.0',
        'pandas==2.0.0',
        'numpy==1.24.0',
        {
            'pip': [
                'mlflow==2.9.0',
                'evidently==0.4.0'
            ]
        }
    ]
}

# Log environment
mlflow.log_dict(conda_env, 'conda_env.yaml')

# Also log pip freeze
import subprocess
pip_freeze = subprocess.check_output(['pip', 'freeze']).decode('utf-8')
mlflow.log_text(pip_freeze, 'requirements.txt')
```

**4. Pipeline configuration versioning**:
```python
# Store pipeline configuration
pipeline_config = {
    'version': '2.1.0',
    'dag_id': 'ml_training_v2',
    'hyperparameters': {
        'n_estimators': 100,
        'max_depth': 10,
        'learning_rate': 0.01
    },
    'preprocessing': {
        'scaler': 'standard',
        'encoding': 'onehot',
        'handle_missing': 'mean'
    },
    'training': {
        'cross_validation_folds': 5,
        'test_size': 0.2,
        'random_seed': 42
    }
}

# Log configuration
mlflow.log_dict(pipeline_config, 'pipeline_config.json')

# Version Airflow DAG
mlflow.log_param('dag_version', '2.1.0')
mlflow.log_param('dag_file_hash', calculate_file_hash('dags/ml_training.py'))
```

**5. Complete reproducibility package**:
```python
def create_reproducibility_package(**context):
    """Create complete package for reproducing this run."""

    run_id = mlflow.active_run().info.run_id

    package = {
        # Code
        'git_commit': get_git_commit(),
        'git_repo': 'https://github.com/company/ml-pipeline',

        # Data
        'data_version': get_data_version(),
        'data_location': 's3://bucket/data/train_20240115.csv',

        # Environment
        'python_version': '3.10.8',
        'conda_env': conda_env,
        'docker_image': 'ml-training:v2.1.0',

        # Pipeline
        'pipeline_version': '2.1.0',
        'airflow_dag_id': context['dag'].dag_id,
        'execution_date': context['ds'],

        # Model
        'mlflow_run_id': run_id,
        'model_uri': f'runs:/{run_id}/model',

        # Configuration
        'hyperparameters': pipeline_config['hyperparameters'],
        'random_seed': 42
    }

    # Save reproducibility package
    mlflow.log_dict(package, 'reproducibility.json')

    # Generate reproduction script
    reproduction_script = f"""
    # Reproduce this training run

    # 1. Clone code
    git clone {package['git_repo']}
    git checkout {package['git_commit']}

    # 2. Set up environment
    conda env create -f conda_env.yaml
    conda activate ml_training

    # 3. Download data
    dvc pull data/train.csv

    # 4. Run training
    python train.py --config reproducibility.json

    # Expected output:
    # Model: {package['model_uri']}
    # MLflow run: {package['mlflow_run_id']}
    """

    mlflow.log_text(reproduction_script, 'REPRODUCE.md')
```

**Benefits**:
- Full reproducibility
- Debugging capability
- Compliance and auditing
- Experiment comparison
- Rollback capability

**Validation**:
```python
def validate_reproducibility(original_run_id):
    """Test if run can be reproduced."""

    # Load original reproducibility package
    client = MlflowClient()
    original_run = client.get_run(original_run_id)

    # Download and execute reproduction script
    # Compare results

    # Check if results match within tolerance
    original_accuracy = original_run.data.metrics['accuracy']
    reproduced_accuracy = reproduced_run.data.metrics['accuracy']

    assert abs(original_accuracy - reproduced_accuracy) < 0.001, \
        "Reproduction accuracy differs significantly"
```

</details>

---

### Question 29
What is the purpose of a "dry run" mode in ML pipelines, and how should it be implemented?

A) Dry run is not useful for ML pipelines
B) Dry run validates pipeline logic without executing expensive operations
C) Dry run only checks syntax
D) Dry run is the same as running with test data

<details>
<summary>Answer</summary>

**B) Dry run validates pipeline logic without executing expensive operations**

**Explanation**: Dry run mode enables safe pipeline validation:

**Implementation**:
```python
# Airflow Variable for dry run mode
DRY_RUN = Variable.get("dry_run_mode", default_var="false") == "true"

def train_model(**context):
    """Train model with dry run support."""

    if DRY_RUN:
        logging.info("DRY RUN: Skipping actual training")

        # Validate inputs
        data_path = context['task_instance'].xcom_pull(key='data_path')
        assert data_path is not None, "Data path not found"
        assert os.path.exists(data_path), f"Data file not found: {data_path}"

        # Validate configuration
        hyperparameters = context['dag_run'].conf.get('hyperparameters', {})
        validate_hyperparameters(hyperparameters)

        # Return mock results
        mock_metrics = {
            'accuracy': 0.85,
            'f1_score': 0.83,
            'training_time': 10.0
        }

        context['task_instance'].xcom_push(key='metrics', value=mock_metrics)
        logging.info(f"DRY RUN: Would train with params: {hyperparameters}")
        logging.info(f"DRY RUN: Mock metrics: {mock_metrics}")

        return mock_metrics

    else:
        # Actual training
        logging.info("PRODUCTION MODE: Running actual training")
        model = train_actual_model(**hyperparameters)
        metrics = evaluate_model(model)
        return metrics
```

**Comprehensive dry run implementation**:
```python
class DryRunContext:
    """Context manager for dry run mode."""

    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.operations_skipped = []

    def skip_operation(self, operation_name: str, mock_result: Any = None):
        """Skip an expensive operation in dry run mode."""
        if self.enabled:
            self.operations_skipped.append(operation_name)
            logging.info(f"DRY RUN: Skipping {operation_name}")
            return mock_result
        return None

    def log_summary(self):
        """Log dry run summary."""
        if self.enabled:
            logging.info("=" * 50)
            logging.info("DRY RUN SUMMARY")
            logging.info(f"Operations skipped: {len(self.operations_skipped)}")
            for op in self.operations_skipped:
                logging.info(f"  - {op}")
            logging.info("=" * 50)

# Usage in tasks
def data_processing_task(**context):
    dry_run = DryRunContext(enabled=DRY_RUN)

    # Expensive data download
    mock_data_path = "/tmp/mock_data.csv"
    if result := dry_run.skip_operation("download_data", mock_data_path):
        data_path = result
    else:
        data_path = download_large_dataset()

    # Expensive preprocessing
    if result := dry_run.skip_operation("preprocess_data", pd.DataFrame({'col': [1, 2, 3]})):
        processed_data = result
    else:
        processed_data = expensive_preprocessing(data_path)

    # Expensive feature engineering
    if result := dry_run.skip_operation("feature_engineering"):
        features = pd.DataFrame({'feature1': [1, 2, 3]})
    else:
        features = compute_complex_features(processed_data)

    dry_run.log_summary()
    return features
```

**Pipeline-level dry run control**:
```python
def create_ml_pipeline_dag(dry_run: bool = False):
    """Create DAG with optional dry run mode."""

    dag = DAG(
        'ml_pipeline',
        default_args=default_args,
        schedule_interval='@daily',
        params={
            'dry_run': Param(dry_run, type='boolean', description='Enable dry run mode')
        }
    )

    with dag:
        def fetch_data_task(**context):
            dry_run = context['params']['dry_run']

            if dry_run:
                # Validate API connection only
                response = requests.head('https://api.example.com/data')
                assert response.status_code == 200
                return "/tmp/mock_data.csv"
            else:
                # Actual data fetch
                return download_data()

        # ... other tasks with dry run support

    return dag

# Create both dry run and production DAGs
dry_run_dag = create_ml_pipeline_dag(dry_run=True)
production_dag = create_ml_pipeline_dag(dry_run=False)
```

**Use cases**:
1. **Pipeline development**: Test logic without expensive operations
2. **Pre-deployment validation**: Ensure pipeline will work before running
3. **Configuration testing**: Validate hyperparameters, paths, connections
4. **CI/CD integration**: Fast pipeline tests in CI
5. **Debugging**: Isolate issues without long waits

**What to validate in dry run**:
- ✓ DAG structure and dependencies
- ✓ Task configuration
- ✓ Data paths exist
- ✓ API connections work
- ✓ XCom data passing
- ✓ Conditional logic
- ✗ Actual model training
- ✗ Large data downloads
- ✗ Expensive computations

**Testing dry run**:
```bash
# Test with dry run
airflow dags test ml_pipeline 2024-01-15 --dry-run

# Test with parameters
airflow dags trigger ml_pipeline --conf '{"dry_run": true}'
```

</details>

---

### Question 30
Analyze this pipeline design. What improvements would you recommend?

```python
dag = DAG('ml_pipeline', schedule_interval='@daily')

with dag:
    data = PythonOperator(task_id='get_data', python_callable=fetch_data)
    train = PythonOperator(task_id='train', python_callable=train_model)
    deploy = PythonOperator(task_id='deploy', python_callable=deploy_model)

    data >> train >> deploy
```

A) No improvements needed
B) Add error handling, validation, monitoring, conditional deployment, and retries
C) Just add retries
D) Just add monitoring

<details>
<summary>Answer</summary>

**B) Add error handling, validation, monitoring, conditional deployment, and retries**

**Explanation**: The pipeline is overly simplistic. Production improvements:

**Improved version**:
```python
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.email import EmailOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta

# Error handling and retry configuration
default_args = {
    'owner': 'ml-team',
    'depends_on_past': False,
    'email': ['ml-team@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(hours=1),
    'execution_timeout': timedelta(hours=4),
}

dag = DAG(
    'ml_pipeline_production',
    default_args=default_args,
    description='Production ML pipeline with best practices',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['ml', 'production'],
)

with dag:
    # 1. Start marker
    start = DummyOperator(task_id='start')

    # 2. Data fetching with retries
    fetch_data = PythonOperator(
        task_id='fetch_data',
        python_callable=fetch_data_with_retry,
        provide_context=True,
    )

    # 3. Data quality validation (NEW)
    validate_data = PythonOperator(
        task_id='validate_data_quality',
        python_callable=validate_data_quality,
        provide_context=True,
    )

    # 4. Preprocessing (NEW)
    preprocess = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data,
        provide_context=True,
    )

    # 5. Training with MLflow tracking (IMPROVED)
    train = PythonOperator(
        task_id='train_model',
        python_callable=train_model_with_mlflow,
        provide_context=True,
    )

    # 6. Model evaluation (NEW)
    evaluate = PythonOperator(
        task_id='evaluate_model',
        python_callable=evaluate_model,
        provide_context=True,
    )

    # 7. Performance check (NEW)
    check_performance = BranchPythonOperator(
        task_id='check_performance',
        python_callable=check_performance_threshold,
        provide_context=True,
    )

    # 8. Model registration (NEW)
    register = PythonOperator(
        task_id='register_model',
        python_callable=register_to_mlflow,
        provide_context=True,
    )

    # 9. Skip deployment branch (NEW)
    skip_deploy = DummyOperator(task_id='skip_deployment')

    # 10. Staging deployment (NEW)
    deploy_staging = PythonOperator(
        task_id='deploy_to_staging',
        python_callable=deploy_to_staging,
        provide_context=True,
    )

    # 11. Integration tests (NEW)
    test_staging = PythonOperator(
        task_id='test_staging_deployment',
        python_callable=run_integration_tests,
        provide_context=True,
    )

    # 12. Production deployment (IMPROVED)
    deploy_prod = PythonOperator(
        task_id='deploy_to_production',
        python_callable=deploy_to_production_with_rollback,
        provide_context=True,
    )

    # 13. Post-deployment monitoring (NEW)
    monitor = PythonOperator(
        task_id='monitor_deployment',
        python_callable=monitor_new_deployment,
        provide_context=True,
    )

    # 14. Success notification (NEW)
    notify_success = EmailOperator(
        task_id='notify_success',
        to='ml-team@example.com',
        subject='ML Pipeline Success - {{ ds }}',
        html_content='''
            <h3>Pipeline completed successfully</h3>
            <p>Execution date: {{ ds }}</p>
            <p>Check MLflow for metrics</p>
        ''',
        trigger_rule=TriggerRule.ALL_SUCCESS,
    )

    # 15. Failure cleanup (NEW)
    cleanup_failure = PythonOperator(
        task_id='cleanup_on_failure',
        python_callable=cleanup_resources,
        provide_context=True,
        trigger_rule=TriggerRule.ONE_FAILED,
    )

    # 16. End marker
    end = DummyOperator(
        task_id='end',
        trigger_rule=TriggerRule.NONE_FAILED,
    )

    # Dependencies
    start >> fetch_data >> validate_data >> preprocess
    preprocess >> train >> evaluate >> check_performance

    # Branching based on performance
    check_performance >> register >> deploy_staging
    check_performance >> skip_deploy

    # Deployment path
    deploy_staging >> test_staging >> deploy_prod >> monitor

    # Final notifications
    [monitor, skip_deploy] >> notify_success >> end

    # Failure handling
    [fetch_data, validate_data, preprocess, train,
     evaluate, deploy_staging, deploy_prod] >> cleanup_failure >> end
```

**Key improvements**:

**1. Error handling**:
- Retries with exponential backoff
- Execution timeout
- Email on failure
- Cleanup on failure

**2. Data validation**:
- Quality checks before training
- Schema validation
- Volume checks

**3. Performance gating**:
- Conditional deployment
- Performance threshold checks
- Comparison with production

**4. Staging environment**:
- Test before production
- Integration tests
- Safe deployment path

**5. Monitoring**:
- Post-deployment checks
- Rollback capability
- Success/failure notifications

**6. MLflow integration**:
- Experiment tracking
- Model registry
- Artifact storage

**7. Trigger rules**:
- `NONE_FAILED` for end task
- `ONE_FAILED` for cleanup
- `ALL_SUCCESS` for success notification

**Issues with original**:
- ❌ No error handling
- ❌ No data validation
- ❌ No performance checks
- ❌ Direct to production (risky)
- ❌ No monitoring
- ❌ No cleanup on failure
- ❌ No notifications
- ❌ No MLflow tracking
- ❌ No retries configured
- ❌ Simple linear flow

</details>

---

## Scoring Guide

| Score | Grade | Feedback |
|-------|-------|----------|
| 28-30 | A+ | Excellent! Deep understanding of automation & orchestration |
| 25-27 | A | Great job! Strong grasp of pipeline concepts |
| 23-24 | B | Good. Review missed topics |
| 20-22 | C | Passing. Revisit key orchestration concepts |
| < 20 | F | Please review lecture notes and retry |

---

## Answer Key Summary

1. B | 2. B | 3. C | 4. A,B,C,D | 5. B
6. B | 7. B | 8. B | 9. B | 10. B
11. C | 12. B | 13. A,B,C,E | 14. B | 15. B
16. B | 17. B | 18. A,C,E | 19. B | 20. C
21. C | 22. B | 23. B | 24. A,B,C,E,F,G | 25. D
26. C | 27. A,B,C,D,E,F | 28. C | 29. B | 30. B

---

## Next Steps

- Review any missed questions
- Complete hands-on exercises
- Build your own ML pipeline
- Deploy to production environment
- Explore additional resources in lecture notes

Good luck!
