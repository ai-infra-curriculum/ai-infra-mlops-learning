## Exercise 4: Audit Logging & Compliance Tracking (90 minutes)

**Objective**: Implement tamper-proof audit logging for ML model predictions and decisions.

### Background

Regulatory compliance requires complete audit trails of model predictions, including:
- Who made predictions
- What inputs were used
- What outputs were generated
- When predictions occurred
- Why decisions were made (explanations)

### Tasks

1. **Implement tamper-proof audit logging**
2. **Log predictions with full context**
3. **Generate audit reports**
4. **Implement compliance checks**
5. **Create audit trail query system**

### Starter Code

```python
# src/governance/audit_logging.py
"""Tamper-proof audit logging for ML models."""

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import sqlite3
from pathlib import Path


@dataclass
class PredictionLog:
    """Single prediction audit log entry."""
    log_id: str
    timestamp: datetime
    model_name: str
    model_version: str
    user_id: str
    input_data: Dict[str, Any]
    prediction: Any
    confidence: float
    explanation: Optional[Dict] = None
    sensitive_features: Optional[Dict] = None
    fairness_check_passed: bool = True
    previous_hash: str = ""
    current_hash: str = ""


class AuditLogger:
    """Tamper-proof audit logging system."""

    def __init__(self, db_path: str = "audit_log.db"):
        """
        Initialize audit logger.

        Args:
            db_path: Path to SQLite database for audit logs
        """
        self.db_path = Path(db_path)
        self._initialize_database()
        self.previous_hash = self._get_last_hash()

    def _initialize_database(self):
        """Create audit log database if it doesn't exist."""
        # TODO: Create SQLite database with audit_logs table
        # Columns:
        #   - log_id (PRIMARY KEY)
        #   - timestamp
        #   - model_name
        #   - model_version
        #   - user_id
        #   - input_data (JSON)
        #   - prediction (JSON)
        #   - confidence
        #   - explanation (JSON)
        #   - sensitive_features (JSON)
        #   - fairness_check_passed
        #   - previous_hash
        #   - current_hash
        pass

    def _calculate_hash(self, log_entry: PredictionLog) -> str:
        """
        Calculate cryptographic hash of log entry.

        Args:
            log_entry: Prediction log entry

        Returns:
            SHA-256 hash string
        """
        # TODO: Create hash of log entry
        # Include all fields except current_hash
        # Concatenate with previous_hash to create chain
        # Use SHA-256 for cryptographic security

        # Example:
        # data_string = json.dumps({
        #     'log_id': log_entry.log_id,
        #     'timestamp': log_entry.timestamp.isoformat(),
        #     ...
        #     'previous_hash': log_entry.previous_hash
        # }, sort_keys=True)
        # hash_value = hashlib.sha256(data_string.encode()).hexdigest()
        # return hash_value
        pass

    def log_prediction(
        self,
        model_name: str,
        model_version: str,
        user_id: str,
        input_data: Dict[str, Any],
        prediction: Any,
        confidence: float,
        explanation: Optional[Dict] = None,
        sensitive_features: Optional[Dict] = None,
        fairness_check_passed: bool = True
    ) -> str:
        """
        Log a model prediction.

        Args:
            model_name: Name of the model
            model_version: Version of the model
            user_id: User making the prediction
            input_data: Input features
            prediction: Model prediction
            confidence: Prediction confidence score
            explanation: Explanation of prediction (optional)
            sensitive_features: Sensitive attributes (optional)
            fairness_check_passed: Whether fairness check passed

        Returns:
            Log ID
        """
        # TODO: Generate unique log ID
        # log_id = f"{model_name}_{datetime.now().timestamp()}"

        # TODO: Create PredictionLog entry
        # log_entry = PredictionLog(
        #     log_id=log_id,
        #     timestamp=datetime.now(),
        #     model_name=model_name,
        #     model_version=model_version,
        #     user_id=user_id,
        #     input_data=input_data,
        #     prediction=prediction,
        #     confidence=confidence,
        #     explanation=explanation,
        #     sensitive_features=sensitive_features,
        #     fairness_check_passed=fairness_check_passed,
        #     previous_hash=self.previous_hash
        # )

        # TODO: Calculate hash
        # log_entry.current_hash = self._calculate_hash(log_entry)

        # TODO: Store in database
        # self._store_log(log_entry)

        # TODO: Update previous_hash for next log
        # self.previous_hash = log_entry.current_hash

        # TODO: Return log_id
        pass

    def _store_log(self, log_entry: PredictionLog):
        """
        Store log entry in database.

        Args:
            log_entry: Prediction log to store
        """
        # TODO: Connect to database
        # TODO: Insert log entry
        # TODO: Commit transaction
        pass

    def _get_last_hash(self) -> str:
        """
        Get hash of last log entry.

        Returns:
            Last hash or empty string if no logs
        """
        # TODO: Query database for last log entry
        # TODO: Return current_hash or "" if no entries
        pass

    def verify_log_integrity(self) -> tuple[bool, List[str]]:
        """
        Verify integrity of entire audit log.

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        # TODO: Query all log entries in order
        # TODO: Verify hash chain:
        #   - For each entry:
        #     - Recalculate hash
        #     - Compare to stored hash
        #     - Verify previous_hash matches previous entry's current_hash
        #   - If any mismatch, add to issues list

        # TODO: Return (len(issues) == 0, issues)
        pass

    def query_logs(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        model_name: Optional[str] = None,
        user_id: Optional[str] = None,
        fairness_check_failed: bool = False
    ) -> List[PredictionLog]:
        """
        Query audit logs with filters.

        Args:
            start_date: Filter logs after this date
            end_date: Filter logs before this date
            model_name: Filter by model name
            user_id: Filter by user ID
            fairness_check_failed: If True, return only failed fairness checks

        Returns:
            List of matching prediction logs
        """
        # TODO: Build SQL query with WHERE clauses based on filters
        # TODO: Execute query
        # TODO: Convert results to PredictionLog objects
        # TODO: Return list
        pass

    def generate_audit_report(
        self,
        start_date: datetime,
        end_date: datetime,
        output_path: str = "audit_report.html"
    ):
        """
        Generate compliance audit report.

        Args:
            start_date: Report start date
            end_date: Report end date
            output_path: Path to save report
        """
        # TODO: Query logs for date range
        logs = self.query_logs(start_date=start_date, end_date=end_date)

        # TODO: Calculate statistics
        #   - Total predictions
        #   - Predictions by model
        #   - Predictions by user
        #   - Fairness check failures
        #   - Average confidence
        #   - Sensitive feature usage

        # TODO: Generate HTML report with:
        #   - Summary statistics
        #   - Fairness violations
        #   - Model usage
        #   - User activity
        #   - Compliance status

        # TODO: Save report
        pass

    def export_logs(
        self,
        output_path: str,
        format: str = 'json',
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ):
        """
        Export audit logs for compliance.

        Args:
            output_path: Output file path
            format: Export format ('json', 'csv')
            start_date: Optional start date filter
            end_date: Optional end date filter
        """
        # TODO: Query logs with filters
        # TODO: Convert to requested format
        # TODO: Write to file
        pass
```

### Validation Tests

```python
# tests/test_audit_logging.py
"""Tests for audit logging."""

import pytest
from datetime import datetime, timedelta
from src.governance.audit_logging import AuditLogger, PredictionLog


@pytest.fixture
def audit_logger(tmp_path):
    """Create temporary audit logger."""
    db_path = tmp_path / "test_audit.db"
    return AuditLogger(str(db_path))


def test_audit_logger_initialization(audit_logger):
    """Test that audit logger initializes."""
    # TODO: Assert database created
    # TODO: Assert previous_hash is empty initially
    pass


def test_log_prediction(audit_logger):
    """Test logging a prediction."""
    log_id = audit_logger.log_prediction(
        model_name="loan_model",
        model_version="1.0",
        user_id="user123",
        input_data={"age": 35, "income": 50000},
        prediction="approved",
        confidence=0.85
    )

    # TODO: Assert log_id returned
    # TODO: Assert log stored in database
    # TODO: Assert hash calculated
    pass


def test_hash_chain_integrity(audit_logger):
    """Test that hash chain maintains integrity."""
    # TODO: Log multiple predictions
    # TODO: Verify hash chain integrity
    # TODO: Assert verification passes
    pass


def test_tamper_detection(audit_logger):
    """Test that tampering is detected."""
    # TODO: Log prediction
    # TODO: Manually modify database entry
    # TODO: Run verify_log_integrity()
    # TODO: Assert tampering detected
    pass


def test_query_logs_with_filters(audit_logger):
    """Test querying logs with filters."""
    # TODO: Log multiple predictions with different attributes
    # TODO: Query with model_name filter
    # TODO: Assert correct logs returned
    # TODO: Query with date filter
    # TODO: Assert correct logs returned
    pass


def test_fairness_check_logging(audit_logger):
    """Test logging fairness check results."""
    # TODO: Log prediction with fairness_check_passed=False
    # TODO: Query for failed fairness checks
    # TODO: Assert failed check is returned
    pass


# Run with: pytest tests/test_audit_logging.py -v
```

### Success Criteria

- [ ] Audit logs stored in tamper-proof manner
- [ ] Hash chain maintains integrity
- [ ] Tampering is detected
- [ ] Logs queryable with multiple filters
- [ ] Audit reports generated correctly
- [ ] Export functionality works
- [ ] Tests verify all functionality

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Hash Chain**: Each entry's hash includes previous entry's hash
   ```python
   data = {**log_data, 'previous_hash': previous_hash}
   current_hash = hashlib.sha256(json.dumps(data).encode()).hexdigest()
   ```

2. **Tamper Detection**: Recalculate hashes and compare to stored values
3. **SQLite**: Use `sqlite3` module for database operations
4. **JSON Storage**: Store complex fields as JSON strings in SQLite
5. **Verification**: Check hash chain in order from oldest to newest

</details>

---
