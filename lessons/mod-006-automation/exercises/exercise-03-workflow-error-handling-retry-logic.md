## Exercise 3: Workflow Error Handling & Retry Logic (75 minutes)

**Objective**: Implement robust error handling, retry logic, and failure recovery in ML pipelines.

### Background

Production pipelines must handle:
- Transient failures (network, API limits)
- Data quality issues
- Resource constraints
- Downstream service failures
- Partial failures requiring cleanup

### Tasks

1. **Implement retry logic with exponential backoff**
2. **Add error handling for different failure types**
3. **Create failure recovery mechanisms**
4. **Implement circuit breakers**
5. **Add comprehensive logging and alerting**

### Starter Code

```python
# robust_pipeline.py
"""
ML pipeline with comprehensive error handling and retry logic.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowException, AirflowSkipException
from airflow.utils.trigger_rule import TriggerRule
import logging
import time
import requests
from functools import wraps
from typing import Callable, Any
import random

# Custom exceptions
class DataQualityException(AirflowException):
    """Raised when data quality checks fail."""
    pass

class ExternalServiceException(AirflowException):
    """Raised when external service is unavailable."""
    pass

class RetryableException(AirflowException):
    """Raised for errors that should be retried."""
    pass


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    Decorator for retry logic with exponential backoff.

    TODO: Implement retry decorator
    - Catch specified exceptions
    - Retry with exponential backoff
    - Log retry attempts
    - Raise after max_retries exceeded
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay

            for attempt in range(max_retries + 1):
                try:
                    # TODO: Execute function
                    result = func(*args, **kwargs)

                    if attempt > 0:
                        logging.info(f"{func.__name__} succeeded after {attempt} retries")

                    return result

                except exceptions as e:
                    if attempt == max_retries:
                        logging.error(f"{func.__name__} failed after {max_retries} retries: {e}")
                        raise

                    # TODO: Calculate next delay with jitter
                    jitter = random.uniform(0, delay * 0.1)
                    sleep_time = delay + jitter

                    logging.warning(
                        f"{func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {e}. "
                        f"Retrying in {sleep_time:.2f}s..."
                    )

                    time.sleep(sleep_time)
                    delay *= backoff_factor

        return wrapper
    return decorator


class CircuitBreaker:
    """
    Circuit breaker pattern for external service calls.

    TODO: Implement circuit breaker
    - Track failure rate
    - Open circuit after threshold
    - Half-open state for recovery testing
    - Close circuit when recovered
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: type = Exception
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection.

        TODO: Implement circuit breaker logic
        """

        # TODO: Check if circuit is OPEN
        if self.state == 'OPEN':
            if self._should_attempt_reset():
                self.state = 'HALF_OPEN'
                logging.info("Circuit breaker entering HALF_OPEN state")
            else:
                raise ExternalServiceException(
                    f"Circuit breaker is OPEN. Service unavailable."
                )

        try:
            # TODO: Execute function
            result = func(*args, **kwargs)

            # TODO: On success in HALF_OPEN, close circuit
            if self.state == 'HALF_OPEN':
                self._reset()
                logging.info("Circuit breaker CLOSED - service recovered")

            return result

        except self.expected_exception as e:
            # TODO: Record failure
            self._record_failure()

            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
                logging.error(
                    f"Circuit breaker OPENED after {self.failure_count} failures"
                )

            raise

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt recovery."""
        # TODO: Implement timeout check
        if self.last_failure_time is None:
            return True

        return (time.time() - self.last_failure_time) >= self.recovery_timeout

    def _record_failure(self):
        """Record a failure."""
        self.failure_count += 1
        self.last_failure_time = time.time()

    def _reset(self):
        """Reset circuit breaker to closed state."""
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'


# Example usage in Airflow tasks
@retry_with_backoff(
    max_retries=3,
    initial_delay=2.0,
    backoff_factor=2.0,
    exceptions=(requests.exceptions.RequestException, RetryableException)
)
def fetch_data_with_retry(**context):
    """
    Fetch data with automatic retry on transient failures.

    TODO: Implement data fetching with error handling
    """
    logging.info("Fetching data from external API")

    # TODO: Make API request
    # response = requests.get('https://api.example.com/data', timeout=30)

    # TODO: Handle different status codes
    # if response.status_code == 429:  # Rate limited
    #     raise RetryableException("Rate limited - will retry")
    # elif response.status_code >= 500:  # Server error
    #     raise RetryableException(f"Server error {response.status_code} - will retry")
    # elif response.status_code != 200:
    #     raise AirflowException(f"Failed to fetch data: {response.status_code}")

    # TODO: Parse and validate response
    # data = response.json()
    # if not data:
    #     raise DataQualityException("Empty response received")

    # return data
    pass


def validate_data_quality(**context):
    """
    Validate data quality with specific error handling.

    TODO: Implement data quality checks
    - Check for missing values
    - Validate schema
    - Check distributions
    - Raise appropriate exceptions
    """
    ti = context['task_instance']
    data = ti.xcom_pull(task_ids='fetch_data_with_retry')

    try:
        # TODO: Validation logic
        # if data is None:
        #     raise DataQualityException("No data received")

        # TODO: Check missing values
        # missing_pct = calculate_missing_percentage(data)
        # if missing_pct > 0.3:  # 30% threshold
        #     raise DataQualityException(f"Too many missing values: {missing_pct:.1%}")

        # TODO: Schema validation
        # if not validate_schema(data):
        #     raise DataQualityException("Schema validation failed")

        logging.info("Data quality validation passed")

    except DataQualityException as e:
        # TODO: Log data quality issue
        logging.error(f"Data quality check failed: {e}")

        # TODO: Send alert
        # send_alert(f"Data quality issue: {e}")

        # Re-raise to fail task
        raise


def cleanup_on_failure(**context):
    """
    Cleanup task that runs on pipeline failure.

    TODO: Implement cleanup logic
    - Remove temporary files
    - Release resources
    - Rollback partial changes
    - Send failure notifications
    """
    logging.info("Running failure cleanup")

    # TODO: Get failed task details
    # failed_task_id = context['task_instance'].task_id
    # execution_date = context['execution_date']

    # TODO: Cleanup temporary files
    # cleanup_temp_files(execution_date)

    # TODO: Release resources
    # release_db_connections()

    # TODO: Send detailed failure notification
    # send_failure_alert(
    #     task=failed_task_id,
    #     execution_date=execution_date,
    #     error=context.get('exception')
    # )

    pass


def graceful_degradation(**context):
    """
    Implement graceful degradation when optimal path fails.

    TODO: Implement fallback logic
    - Try primary data source
    - Fall back to secondary source if primary fails
    - Use cached data as last resort
    """
    logging.info("Attempting primary data source")

    try:
        # TODO: Try primary source
        # data = fetch_from_primary_source()
        # return data
        pass

    except Exception as e:
        logging.warning(f"Primary source failed: {e}. Trying secondary source...")

        try:
            # TODO: Try secondary source
            # data = fetch_from_secondary_source()
            # logging.info("Successfully retrieved data from secondary source")
            # return data
            pass

        except Exception as e2:
            logging.error(f"Secondary source also failed: {e2}. Using cached data...")

            # TODO: Use cached data
            # data = load_cached_data()
            # if data is not None:
            #     logging.warning("Using cached data - may be stale")
            #     return data

            # If all fail, raise
            raise AirflowException("All data sources failed")


# DAG definition
default_args = {
    'owner': 'ml-team',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(minutes=30),
    'on_failure_callback': lambda context: logging.error(f"Task failed: {context['task_instance'].task_id}"),
}

dag = DAG(
    'robust_ml_pipeline',
    default_args=default_args,
    description='ML pipeline with robust error handling',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['ml', 'robust', 'production'],
)

with dag:
    # Tasks with different error handling strategies
    fetch_data = PythonOperator(
        task_id='fetch_data_with_retry',
        python_callable=fetch_data_with_retry,
        provide_context=True,
    )

    validate_data = PythonOperator(
        task_id='validate_data_quality',
        python_callable=validate_data_quality,
        provide_context=True,
    )

    graceful_task = PythonOperator(
        task_id='graceful_degradation',
        python_callable=graceful_degradation,
        provide_context=True,
    )

    cleanup = PythonOperator(
        task_id='cleanup_on_failure',
        python_callable=cleanup_on_failure,
        provide_context=True,
        trigger_rule=TriggerRule.ONE_FAILED,  # Run only if upstream failed
    )

    # Define dependencies
    fetch_data >> validate_data >> graceful_task
    [fetch_data, validate_data, graceful_task] >> cleanup
```

### Validation

Test error scenarios:
```python
# test_error_handling.py
import pytest
from unittest.mock import Mock, patch
import requests

def test_retry_with_backoff_success_after_retries():
    """Test that retry succeeds after transient failures."""
    # TODO: Implement test
    pass

def test_retry_with_backoff_max_retries_exceeded():
    """Test that function raises after max retries."""
    # TODO: Implement test
    pass

def test_circuit_breaker_opens_after_threshold():
    """Test circuit breaker opens after failure threshold."""
    # TODO: Implement test
    pass

def test_circuit_breaker_half_open_recovery():
    """Test circuit breaker recovery mechanism."""
    # TODO: Implement test
    pass
```

### Success Criteria

- [ ] Retry logic works with exponential backoff
- [ ] Circuit breaker opens/closes correctly
- [ ] Different exception types handled appropriately
- [ ] Cleanup runs on failure
- [ ] Graceful degradation works
- [ ] Comprehensive logging implemented
- [ ] Alerts sent on failures

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Retries**: Use `time.sleep()` with exponential backoff, add jitter to prevent thundering herd
2. **Circuit Breaker**: Track state (CLOSED/OPEN/HALF_OPEN), use timestamps for recovery
3. **Exception Types**: Create custom exceptions for different failure modes
4. **Cleanup**: Use `trigger_rule=TriggerRule.ONE_FAILED` for cleanup tasks
5. **Callbacks**: Use `on_failure_callback` in default_args for centralized failure handling
6. **Logging**: Use structured logging with context (task_id, execution_date)

</details>

---
