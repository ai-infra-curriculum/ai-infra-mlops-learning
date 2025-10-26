# Module 04: Data Quality & Validation - Exercises

## Overview

This exercise set provides hands-on practice with data quality and validation, covering:
- Pydantic schema validation and type safety
- Great Expectations framework for data testing
- Statistical validation and distribution testing
- Data profiling and anomaly detection
- Production data quality pipelines

**Time Estimate**: 6-9 hours total

---

## Exercise 1: Pydantic Schema Validation (75 minutes)

**Objective**: Implement comprehensive schema validation using Pydantic for ML datasets.

### Background

You're building a customer churn prediction model. Raw data comes from multiple sources with inconsistent formats, missing values, and invalid entries. You need to:
- Define strict schemas with type safety
- Validate data before training
- Handle schema evolution
- Log validation errors for analysis

### Tasks

1. **Create Pydantic schemas** for customer data
2. **Implement custom validators** for business logic
3. **Build schema version manager** to handle evolution
4. **Create validation pipeline** with error reporting
5. **Integrate with pandas DataFrames**

### Starter Code

```python
# schemas.py
"""Pydantic schemas for customer churn data validation."""

from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, Literal
from datetime import datetime, date
from enum import Enum
import re


class SubscriptionTier(str, Enum):
    """Valid subscription tiers."""
    BASIC = 'basic'
    PREMIUM = 'premium'
    ENTERPRISE = 'enterprise'


class CustomerDataSchema(BaseModel):
    """Schema for customer churn prediction data."""

    # Customer identifiers
    customer_id: str = Field(..., regex=r'^CUST-\d{8}$')

    # Demographics
    age: int = Field(..., ge=18, le=100)
    country: str = Field(..., min_length=2, max_length=2)  # ISO country code
    account_created_date: date

    # Subscription details
    subscription_tier: SubscriptionTier
    monthly_charges: float = Field(..., gt=0, le=10000)
    total_charges: float = Field(..., ge=0)
    contract_months: int = Field(..., ge=1, le=36)

    # Usage metrics
    monthly_usage_gb: float = Field(..., ge=0)
    support_tickets: int = Field(..., ge=0)
    login_frequency_days: float = Field(..., ge=0, le=30)

    # Features
    has_multiple_devices: bool
    has_payment_issues: bool

    # Target (optional for prediction)
    churned: Optional[bool] = None

    @validator('account_created_date')
    def account_date_not_future(cls, v):
        """Account creation date must be in the past."""
        # TODO: Implement validation
        # - Check that date is not in the future
        # - Check that date is not too old (e.g., before 2000)
        pass

    @validator('monthly_charges')
    def monthly_charges_reasonable_for_tier(cls, v, values):
        """Validate monthly charges match subscription tier."""
        # TODO: Implement validation
        # - BASIC: $10-50
        # - PREMIUM: $50-200
        # - ENTERPRISE: $200-1000
        pass

    @root_validator
    def total_charges_consistent_with_monthly(cls, values):
        """Total charges should align with monthly charges and contract length."""
        # TODO: Implement validation
        # - Calculate expected total: monthly_charges * contract_months
        # - Allow some variance (±20%) for discounts/promotions
        # - Raise ValueError if inconsistent
        pass

    @validator('login_frequency_days')
    def login_frequency_logical(cls, v, values):
        """Login frequency should be logical for subscription tier."""
        # TODO: Implement validation
        # - Enterprise users should login more frequently
        # - Churned users might have low login frequency
        pass

    class Config:
        validate_assignment = True
        use_enum_values = True


def validate_dataframe(
    df: pd.DataFrame,
    schema: BaseModel,
    strict: bool = False
) -> tuple[pd.DataFrame, list]:
    """
    Validate entire DataFrame against Pydantic schema.

    Args:
        df: Input DataFrame
        schema: Pydantic schema class
        strict: If True, raise exception on any validation error

    Returns:
        Tuple of (valid_dataframe, errors_list)
    """
    # TODO: Implement DataFrame validation
    # - Iterate through rows
    # - Validate each row against schema
    # - Collect valid rows and errors
    # - Create DataFrame from valid rows
    # - If strict=True and errors exist, raise exception
    pass


def generate_validation_report(errors: list) -> dict:
    """
    Generate detailed validation error report.

    Args:
        errors: List of validation errors

    Returns:
        Dictionary with error statistics and details
    """
    # TODO: Implement error reporting
    # - Count errors by type
    # - Identify most common validation failures
    # - Calculate error rate by column
    # - Return comprehensive report
    pass
```

```python
# schema_evolution.py
"""Handle schema evolution and migrations."""

from typing import Dict, Any, Callable
import json
from pathlib import Path


class SchemaVersionManager:
    """Manage schema versions and migrations."""

    def __init__(self, schema_dir: str = './schemas'):
        self.schema_dir = Path(schema_dir)
        self.schema_dir.mkdir(exist_ok=True)
        self.schemas: Dict[str, BaseModel] = {}
        self.migrations: Dict[tuple, Callable] = {}

    def register_schema(self, version: str, schema: BaseModel):
        """
        Register a schema version.

        Args:
            version: Version string (e.g., 'v1', 'v2')
            schema: Pydantic schema class
        """
        # TODO: Register schema
        # - Store in self.schemas
        # - Save schema JSON schema to file
        pass

    def register_migration(
        self,
        from_version: str,
        to_version: str,
        migration_func: Callable
    ):
        """
        Register a migration function.

        Args:
            from_version: Source version
            to_version: Target version
            migration_func: Function that transforms data
        """
        # TODO: Register migration function
        pass

    def migrate_data(
        self,
        data: Dict[str, Any],
        from_version: str,
        to_version: str
    ) -> Dict[str, Any]:
        """
        Migrate data between schema versions.

        Args:
            data: Data dict in source version format
            from_version: Source version
            to_version: Target version

        Returns:
            Migrated data dict
        """
        # TODO: Implement migration
        # - Look up migration function
        # - Apply migration
        # - Validate against target schema
        # - Return migrated data
        pass

    def detect_version(self, data: Dict[str, Any]) -> Optional[str]:
        """
        Detect which schema version the data matches.

        Args:
            data: Data dictionary

        Returns:
            Detected version or None
        """
        # TODO: Try validating against each schema
        # - Return version of first successful validation
        # - Return None if no match
        pass


# Example migration functions
def migrate_v1_to_v2(data: dict) -> dict:
    """
    Migrate from v1 to v2.

    Changes:
    - Rename 'total_spend' to 'total_charges'
    - Add 'has_payment_issues' field (default False)
    """
    # TODO: Implement migration
    pass


def migrate_v2_to_v3(data: dict) -> dict:
    """
    Migrate from v2 to v3.

    Changes:
    - Split 'usage' into 'monthly_usage_gb' and 'login_frequency_days'
    - Add 'subscription_tier' enum field
    """
    # TODO: Implement migration
    pass
```

### Validation Tests

```python
# tests/test_schema_validation.py
"""Tests for Pydantic schema validation."""

import pytest
import pandas as pd
from datetime import date, timedelta
from schemas import CustomerDataSchema, validate_dataframe, SubscriptionTier


class TestCustomerDataSchema:
    """Test suite for customer data schema."""

    def test_valid_customer_data(self):
        """Test that valid data passes validation."""
        valid_data = {
            'customer_id': 'CUST-12345678',
            'age': 35,
            'country': 'US',
            'account_created_date': date(2022, 1, 15),
            'subscription_tier': 'premium',
            'monthly_charges': 99.99,
            'total_charges': 1199.88,
            'contract_months': 12,
            'monthly_usage_gb': 150.5,
            'support_tickets': 2,
            'login_frequency_days': 15.5,
            'has_multiple_devices': True,
            'has_payment_issues': False,
            'churned': False
        }

        # TODO: Validate data
        # TODO: Assert validation succeeds
        pass

    def test_invalid_customer_id_format(self):
        """Test that invalid customer ID format fails."""
        # TODO: Create data with invalid customer_id
        # TODO: Assert ValidationError is raised
        pass

    def test_age_out_of_range(self):
        """Test that age outside valid range fails."""
        # TODO: Test age < 18
        # TODO: Test age > 100
        pass

    def test_future_account_date_rejected(self):
        """Test that future account creation date is rejected."""
        # TODO: Create data with future date
        # TODO: Assert validation fails
        pass

    def test_monthly_charges_tier_mismatch(self):
        """Test that monthly charges must match subscription tier."""
        # TODO: Test BASIC tier with ENTERPRISE pricing
        # TODO: Assert validation fails
        pass

    def test_total_charges_inconsistent(self):
        """Test that inconsistent total charges fail validation."""
        # TODO: Create data where total_charges doesn't match monthly * months
        # TODO: Assert validation fails
        pass


class TestDataFrameValidation:
    """Test suite for DataFrame validation."""

    def test_validate_clean_dataframe(self, sample_clean_data):
        """Test validation of clean DataFrame."""
        # TODO: Create clean DataFrame
        # TODO: Validate
        # TODO: Assert all rows valid, no errors
        pass

    def test_validate_mixed_dataframe(self, sample_mixed_data):
        """Test validation of DataFrame with some invalid rows."""
        # TODO: Create DataFrame with mix of valid/invalid rows
        # TODO: Validate
        # TODO: Assert correct number of valid rows
        # TODO: Assert errors captured
        pass

    def test_strict_mode_raises_on_errors(self, sample_invalid_data):
        """Test that strict mode raises exception on validation errors."""
        # TODO: Create invalid DataFrame
        # TODO: Call validate_dataframe with strict=True
        # TODO: Assert exception is raised
        pass


@pytest.fixture
def sample_clean_data():
    """Generate clean sample data."""
    return pd.DataFrame({
        'customer_id': [f'CUST-{i:08d}' for i in range(100)],
        'age': [25, 35, 45, 55, 65] * 20,
        # TODO: Add all required fields
    })

# Run with: pytest tests/test_schema_validation.py -v
```

### Success Criteria

- [ ] Pydantic schemas validate all data types correctly
- [ ] Custom validators enforce business logic
- [ ] Schema evolution manager handles migrations
- [ ] DataFrame validation processes entire datasets
- [ ] Validation errors are captured and reported
- [ ] Tests cover edge cases and invalid data
- [ ] Validation runs in under 1 second for 10k rows

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Regex Validation**: Use `Field(..., regex=r'pattern')` for string format validation
2. **Date Validation**: Compare dates with `datetime.now().date()` in validator
3. **Cross-field Validation**: Use `@root_validator` to access multiple fields
4. **Enum Values**: Use `SubscriptionTier.PREMIUM.value` to compare string values
5. **DataFrame Iteration**: Use `df.iterrows()` but consider vectorization for large datasets
6. **Error Collection**: Store errors as `{'row_index': idx, 'error': str(e), 'field': field}`

</details>

---

## Exercise 2: Great Expectations Suite (90 minutes)

**Objective**: Build comprehensive data quality test suite using Great Expectations framework.

### Background

Your ML pipeline processes daily data feeds. You need automated data quality checks that:
- Validate schema compliance
- Check statistical properties
- Detect anomalies
- Generate HTML reports
- Integrate with CI/CD

### Tasks

1. **Set up Great Expectations project**
2. **Create expectation suite** with 20+ expectations
3. **Implement custom expectations** for business logic
4. **Create checkpoint** for automated validation
5. **Generate and customize data docs**

### Starter Code

```python
# setup_great_expectations.py
"""Initialize and configure Great Expectations."""

import great_expectations as gx
from great_expectations.core.batch import BatchRequest
from great_expectations.checkpoint import SimpleCheckpoint


def initialize_ge_project(project_root: str = './') -> gx.DataContext:
    """
    Initialize Great Expectations project.

    Args:
        project_root: Root directory for GE project

    Returns:
        Initialized DataContext
    """
    # TODO: Initialize GE context
    # context = gx.get_context()
    # TODO: Return context
    pass


def create_datasource(context: gx.DataContext, data_dir: str) -> dict:
    """
    Create pandas datasource for CSV files.

    Args:
        context: GE DataContext
        data_dir: Directory containing data files

    Returns:
        Datasource configuration
    """
    datasource_config = {
        "name": "customer_datasource",
        "class_name": "Datasource",
        "execution_engine": {
            "class_name": "PandasExecutionEngine"
        },
        "data_connectors": {
            # TODO: Configure data connector
            # - Use InferredAssetFilesystemDataConnector
            # - Set base_directory to data_dir
            # - Configure regex pattern for CSV files
        }
    }

    # TODO: Add datasource to context
    # context.add_datasource(**datasource_config)

    return datasource_config


def create_expectation_suite(
    context: gx.DataContext,
    suite_name: str,
    datasource_name: str,
    data_asset_name: str
) -> gx.core.ExpectationSuite:
    """
    Create comprehensive expectation suite.

    Args:
        context: GE DataContext
        suite_name: Name for the expectation suite
        datasource_name: Name of datasource
        data_asset_name: Name of data asset

    Returns:
        Created expectation suite
    """
    # TODO: Create expectation suite
    suite = context.create_expectation_suite(
        expectation_suite_name=suite_name,
        overwrite_existing=True
    )

    # TODO: Get validator
    validator = context.get_validator(
        batch_request=BatchRequest(
            datasource_name=datasource_name,
            data_connector_name="default_inferred_data_connector_name",
            data_asset_name=data_asset_name
        ),
        expectation_suite_name=suite_name
    )

    # ============================================
    # COMPLETENESS EXPECTATIONS
    # ============================================

    # TODO: Add expectations for required columns
    # validator.expect_column_to_exist("customer_id")
    # validator.expect_column_values_to_not_be_null("customer_id")
    # TODO: Add for all critical columns

    # ============================================
    # TYPE EXPECTATIONS
    # ============================================

    # TODO: Add type expectations
    # validator.expect_column_values_to_be_of_type("age", "int64")
    # validator.expect_column_values_to_be_of_type("monthly_charges", "float64")

    # ============================================
    # RANGE EXPECTATIONS
    # ============================================

    # TODO: Add range validations
    # validator.expect_column_values_to_be_between("age", min_value=18, max_value=100)
    # validator.expect_column_values_to_be_between(
    #     "monthly_charges",
    #     min_value=0,
    #     max_value=10000
    # )

    # ============================================
    # SET MEMBERSHIP EXPECTATIONS
    # ============================================

    # TODO: Add set expectations for categorical columns
    # validator.expect_column_values_to_be_in_set(
    #     "subscription_tier",
    #     value_set=['basic', 'premium', 'enterprise']
    # )
    # validator.expect_column_values_to_be_in_set(
    #     "country",
    #     value_set=['US', 'UK', 'CA', 'AU', 'DE', 'FR']
    # )

    # ============================================
    # UNIQUENESS EXPECTATIONS
    # ============================================

    # TODO: Add uniqueness checks
    # validator.expect_column_values_to_be_unique("customer_id")

    # ============================================
    # PATTERN EXPECTATIONS
    # ============================================

    # TODO: Add regex pattern expectations
    # validator.expect_column_values_to_match_regex(
    #     "customer_id",
    #     regex=r'^CUST-\d{8}$'
    # )

    # ============================================
    # STATISTICAL EXPECTATIONS
    # ============================================

    # TODO: Add statistical expectations
    # validator.expect_column_mean_to_be_between(
    #     "monthly_charges",
    #     min_value=50,
    #     max_value=200
    # )
    # validator.expect_column_stdev_to_be_between(
    #     "age",
    #     min_value=10,
    #     max_value=30
    # )
    # validator.expect_column_quantile_values_to_be_between(
    #     "total_charges",
    #     quantile_ranges={
    #         "quantiles": [0.25, 0.5, 0.75],
    #         "value_ranges": [[100, 500], [500, 1500], [1500, 5000]]
    #     }
    # )

    # ============================================
    # MULTI-COLUMN EXPECTATIONS
    # ============================================

    # TODO: Add multi-column expectations
    # validator.expect_column_pair_values_to_be_in_set(
    #     column_A="subscription_tier",
    #     column_B="monthly_charges",
    #     value_pairs_set=[
    #         ("basic", 29.99),
    #         ("premium", 99.99),
    #         ("enterprise", 299.99)
    #     ],
    #     mostly=0.9  # Allow 10% variance for promotions
    # )

    # TODO: Save suite
    validator.save_expectation_suite(discard_failed_expectations=False)

    return suite
```

```python
# custom_expectations.py
"""Custom Great Expectations for business logic."""

from great_expectations.execution_engine import PandasExecutionEngine
from great_expectations.expectations.expectation import ColumnMapExpectation
from great_expectations.expectations.metrics import (
    ColumnMapMetricProvider,
    column_condition_partial
)


class ColumnValuesCustomerIDValid(ColumnMapMetricProvider):
    """Metric for validating customer ID format and checksum."""

    condition_metric_name = "column_values.customer_id_valid"

    @column_condition_partial(engine=PandasExecutionEngine)
    def _pandas(cls, column, **kwargs):
        """Validate customer ID format and checksum."""
        # TODO: Implement customer ID validation
        # - Check format: CUST-########
        # - Validate checksum digit
        # - Return boolean series
        pass


class ExpectColumnValuesToBeValidCustomerID(ColumnMapExpectation):
    """Expect customer IDs to be valid format with checksum."""

    map_metric = "column_values.customer_id_valid"
    success_keys = ("mostly",)

    default_kwarg_values = {
        "mostly": 1.0,
        "result_format": "BASIC"
    }


class ExpectTotalChargesConsistentWithMonthly(ColumnMapExpectation):
    """Expect total charges to be consistent with monthly charges."""

    # TODO: Implement custom expectation
    # - Calculate expected total: monthly_charges * contract_months
    # - Allow variance for promotions (±20%)
    # - Return validation result
    pass
```

```python
# checkpoint_runner.py
"""Create and run Great Expectations checkpoints."""

import great_expectations as gx
from pathlib import Path


def create_checkpoint(
    context: gx.DataContext,
    checkpoint_name: str,
    suite_name: str,
    datasource_name: str,
    data_asset_name: str
) -> dict:
    """
    Create validation checkpoint.

    Args:
        context: GE DataContext
        checkpoint_name: Name for checkpoint
        suite_name: Expectation suite name
        datasource_name: Datasource name
        data_asset_name: Data asset name

    Returns:
        Checkpoint configuration
    """
    checkpoint_config = {
        "name": checkpoint_name,
        "config_version": 1.0,
        "class_name": "SimpleCheckpoint",
        "run_name_template": "%Y%m%d-%H%M%S-" + data_asset_name,
        "validations": [
            {
                "batch_request": {
                    "datasource_name": datasource_name,
                    "data_connector_name": "default_inferred_data_connector_name",
                    "data_asset_name": data_asset_name
                },
                "expectation_suite_name": suite_name
            }
        ],
        "action_list": [
            # TODO: Add actions
            # - StoreValidationResultAction
            # - StoreEvaluationParametersAction
            # - UpdateDataDocsAction
            # - SlackNotificationAction (optional)
        ]
    }

    # TODO: Add checkpoint to context
    context.add_checkpoint(**checkpoint_config)

    return checkpoint_config


def run_validation(
    context: gx.DataContext,
    checkpoint_name: str
) -> dict:
    """
    Run validation checkpoint.

    Args:
        context: GE DataContext
        checkpoint_name: Name of checkpoint to run

    Returns:
        Validation results
    """
    # TODO: Run checkpoint
    results = context.run_checkpoint(checkpoint_name=checkpoint_name)

    # TODO: Process results
    success = results["success"]

    # TODO: Extract failed expectations
    failed_expectations = []
    if not success:
        # TODO: Parse validation results
        # TODO: Collect failed expectations
        pass

    return {
        "success": success,
        "failed_expectations": failed_expectations,
        "results": results
    }


def generate_validation_report(results: dict) -> str:
    """
    Generate human-readable validation report.

    Args:
        results: Validation results from run_validation

    Returns:
        Formatted report string
    """
    # TODO: Create formatted report
    # - Overall status
    # - Number of expectations passed/failed
    # - Details of failures
    # - Link to data docs
    pass
```

### Integration Script

```python
# run_data_quality_checks.py
"""Main script to run data quality validation."""

import argparse
from pathlib import Path
from setup_great_expectations import (
    initialize_ge_project,
    create_datasource,
    create_expectation_suite
)
from checkpoint_runner import create_checkpoint, run_validation, generate_validation_report


def main():
    """Run complete data quality validation pipeline."""

    # TODO: Parse command line arguments
    # - data_dir: Directory with data files
    # - data_file: Specific file to validate
    # - suite_name: Expectation suite name

    # TODO: Initialize GE
    context = initialize_ge_project()

    # TODO: Create datasource
    create_datasource(context, data_dir)

    # TODO: Create expectation suite (if not exists)
    create_expectation_suite(
        context,
        suite_name="customer_churn_suite",
        datasource_name="customer_datasource",
        data_asset_name="customer_data"
    )

    # TODO: Create checkpoint
    create_checkpoint(
        context,
        checkpoint_name="customer_validation",
        suite_name="customer_churn_suite",
        datasource_name="customer_datasource",
        data_asset_name="customer_data"
    )

    # TODO: Run validation
    results = run_validation(context, "customer_validation")

    # TODO: Generate and print report
    report = generate_validation_report(results)
    print(report)

    # TODO: Exit with appropriate code
    # exit(0 if results["success"] else 1)


if __name__ == '__main__':
    main()
```

### Validation Tests

```python
# tests/test_great_expectations.py
"""Tests for Great Expectations integration."""

import pytest
import great_expectations as gx
import pandas as pd
from setup_great_expectations import create_expectation_suite


def test_expectation_suite_creation(ge_context):
    """Test that expectation suite is created with all expectations."""
    # TODO: Create suite
    # TODO: Assert suite exists
    # TODO: Assert expected number of expectations
    pass


def test_validation_passes_on_clean_data(ge_context, clean_data_file):
    """Test that validation passes on clean data."""
    # TODO: Run validation on clean data
    # TODO: Assert success=True
    pass


def test_validation_fails_on_dirty_data(ge_context, dirty_data_file):
    """Test that validation catches data quality issues."""
    # TODO: Run validation on dirty data
    # TODO: Assert success=False
    # TODO: Assert specific expectations failed
    pass


@pytest.fixture
def ge_context():
    """Create test GE context."""
    # TODO: Initialize test context
    # TODO: Return context
    pass

# Run with: pytest tests/test_great_expectations.py -v
```

### Success Criteria

- [ ] Great Expectations project initialized
- [ ] Expectation suite with 20+ expectations created
- [ ] Custom expectations implemented and working
- [ ] Checkpoint runs successfully
- [ ] Data docs generated and accessible
- [ ] Validation fails on invalid data
- [ ] Validation passes on clean data
- [ ] Integration with CI/CD ready

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Initialization**: Use `great_expectations init` or `gx.get_context()`
2. **Datasource**: Use `InferredAssetFilesystemDataConnector` for CSV files
3. **Custom Expectations**: Extend `ColumnMapExpectation` for row-level checks
4. **Batch Request**: Specify datasource, connector, and asset names
5. **Actions**: Add `UpdateDataDocsAction` to generate reports automatically
6. **CI/CD**: Run checkpoint in GitHub Actions, fail build on validation errors

</details>

---

## Exercise 3: Statistical Data Quality Checks (75 minutes)

**Objective**: Implement statistical validation to detect data drift and anomalies.

### Background

Production data distributions can shift over time (data drift). You need to:
- Compare new data against reference distributions
- Detect outliers using multiple methods
- Validate correlation structure
- Alert on significant changes

### Tasks

1. **Build statistical validator** with reference data
2. **Implement distribution testing** (KS test, Chi-square)
3. **Create multi-method outlier detection**
4. **Validate correlation structure**
5. **Generate drift detection reports**

### Starter Code

```python
# statistical_validator.py
"""Statistical validation for data quality."""

from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of statistical validation check."""
    check_name: str
    passed: bool
    statistic: float
    threshold: float
    details: dict


class StatisticalValidator:
    """Statistical validation against reference data."""

    def __init__(self, reference_data: pd.DataFrame):
        """
        Initialize validator with reference data.

        Args:
            reference_data: Clean training/validation data as reference
        """
        self.reference_data = reference_data
        self.stats = self._compute_reference_stats()
        self.correlations = self._compute_correlations()

    def _compute_reference_stats(self) -> Dict[str, Dict]:
        """Compute statistical properties of reference data."""
        stats_dict = {}

        for col in self.reference_data.select_dtypes(include=[np.number]).columns:
            # TODO: Compute statistics for each numerical column
            # - mean, std, min, max
            # - quantiles (0.01, 0.25, 0.5, 0.75, 0.99)
            # - skewness, kurtosis
            # - Store in stats_dict[col]
            pass

        return stats_dict

    def _compute_correlations(self) -> pd.DataFrame:
        """Compute correlation matrix of reference data."""
        # TODO: Calculate and return correlation matrix
        pass

    def validate_distribution(
        self,
        data: pd.DataFrame,
        column: str,
        test: str = 'ks',
        p_threshold: float = 0.05
    ) -> ValidationResult:
        """
        Test if distribution matches reference.

        Args:
            data: New data to validate
            column: Column name
            test: Statistical test ('ks' or 'chi2')
            p_threshold: P-value threshold for significance

        Returns:
            ValidationResult with test outcome
        """
        ref_values = self.reference_data[column].dropna()
        new_values = data[column].dropna()

        if test == 'ks':
            # TODO: Perform Kolmogorov-Smirnov test
            # statistic, p_value = stats.ks_2samp(ref_values, new_values)
            pass
        elif test == 'chi2':
            # TODO: Perform Chi-square test
            # - Bin data
            # - Compare distributions
            pass
        else:
            raise ValueError(f"Unknown test: {test}")

        # TODO: Create and return ValidationResult
        pass

    def validate_range(
        self,
        data: pd.DataFrame,
        column: str,
        method: str = 'iqr',
        **kwargs
    ) -> ValidationResult:
        """
        Validate that values are within expected range.

        Args:
            data: Data to validate
            column: Column name
            method: Method ('iqr', 'zscore', 'quantile')
            **kwargs: Method-specific parameters

        Returns:
            ValidationResult with outlier information
        """
        values = data[column]
        ref_stats = self.stats[column]

        if method == 'iqr':
            # TODO: IQR method
            # multiplier = kwargs.get('multiplier', 1.5)
            # Q1, Q3 = ref_stats['q25'], ref_stats['q75']
            # IQR = Q3 - Q1
            # lower = Q1 - multiplier * IQR
            # upper = Q3 + multiplier * IQR
            # outliers = (values < lower) | (values > upper)
            pass

        elif method == 'zscore':
            # TODO: Z-score method
            # threshold = kwargs.get('threshold', 3.0)
            # z_scores = np.abs((values - ref_stats['mean']) / ref_stats['std'])
            # outliers = z_scores > threshold
            pass

        elif method == 'quantile':
            # TODO: Quantile method
            # lower_q = kwargs.get('lower_quantile', 0.01)
            # upper_q = kwargs.get('upper_quantile', 0.99)
            # lower = ref_stats[f'q{int(lower_q*100):02d}']
            # upper = ref_stats[f'q{int(upper_q*100):02d}']
            # outliers = (values < lower) | (values > upper)
            pass

        # TODO: Create and return ValidationResult
        pass

    def validate_correlation_structure(
        self,
        data: pd.DataFrame,
        threshold: float = 0.3
    ) -> ValidationResult:
        """
        Validate that correlation structure hasn't changed.

        Args:
            data: New data
            threshold: Maximum allowed correlation change

        Returns:
            ValidationResult with correlation drift information
        """
        # TODO: Compute correlation matrix for new data
        new_corr = data[self.correlations.columns].corr()

        # TODO: Calculate correlation difference
        corr_diff = np.abs(self.correlations - new_corr)

        # TODO: Find largest changes
        # Get upper triangle to avoid duplicates
        mask = np.triu(np.ones_like(corr_diff, dtype=bool), k=1)
        significant_changes = []

        # TODO: Identify significant changes
        # for i, j in zip(*np.where((corr_diff > threshold) & mask)):
        #     significant_changes.append({
        #         'features': (corr_diff.index[i], corr_diff.columns[j]),
        #         'ref_correlation': self.correlations.iloc[i, j],
        #         'new_correlation': new_corr.iloc[i, j],
        #         'change': corr_diff.iloc[i, j]
        #     })

        # TODO: Create and return ValidationResult
        pass

    def validate_all(
        self,
        data: pd.DataFrame,
        config: dict = None
    ) -> List[ValidationResult]:
        """
        Run all statistical validations.

        Args:
            data: Data to validate
            config: Configuration for validation checks

        Returns:
            List of ValidationResults
        """
        # TODO: Use default config if not provided
        if config is None:
            config = {
                'distribution_tests': ['ks'],
                'range_methods': ['iqr', 'zscore'],
                'check_correlations': True
            }

        results = []

        # TODO: Run distribution tests for numerical columns
        # TODO: Run range validations
        # TODO: Run correlation validation

        return results


class OutlierDetector:
    """Multivariate outlier detection."""

    @staticmethod
    def detect_isolation_forest(
        data: pd.DataFrame,
        contamination: float = 0.1,
        random_state: int = 42
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect outliers using Isolation Forest.

        Args:
            data: Input data
            contamination: Expected proportion of outliers
            random_state: Random seed

        Returns:
            Tuple of (outlier_labels, outlier_scores)
        """
        # TODO: Fit Isolation Forest
        # TODO: Predict outliers (-1 for outliers, 1 for inliers)
        # TODO: Get anomaly scores
        # TODO: Return labels and scores
        pass

    @staticmethod
    def detect_elliptic_envelope(
        data: pd.DataFrame,
        contamination: float = 0.1
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect outliers using Elliptic Envelope (assumes Gaussian).

        Args:
            data: Input data
            contamination: Expected proportion of outliers

        Returns:
            Tuple of (outlier_labels, outlier_scores)
        """
        # TODO: Fit Elliptic Envelope
        # TODO: Predict outliers
        # TODO: Get Mahalanobis distances
        # TODO: Return labels and scores
        pass

    @staticmethod
    def detect_lof(
        data: pd.DataFrame,
        n_neighbors: int = 20,
        contamination: float = 0.1
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect outliers using Local Outlier Factor.

        Args:
            data: Input data
            n_neighbors: Number of neighbors
            contamination: Expected proportion of outliers

        Returns:
            Tuple of (outlier_labels, outlier_scores)
        """
        from sklearn.neighbors import LocalOutlierFactor

        # TODO: Fit LOF
        # TODO: Predict outliers
        # TODO: Get LOF scores
        # TODO: Return labels and scores
        pass

    @staticmethod
    def ensemble_detection(
        data: pd.DataFrame,
        methods: List[str] = None,
        voting: str = 'majority'
    ) -> np.ndarray:
        """
        Ensemble outlier detection using multiple methods.

        Args:
            data: Input data
            methods: List of methods to use
            voting: 'majority' or 'unanimous'

        Returns:
            Array of outlier labels
        """
        if methods is None:
            methods = ['isolation_forest', 'elliptic_envelope', 'lof']

        # TODO: Run each detection method
        # TODO: Combine results based on voting strategy
        # TODO: Return ensemble outlier labels
        pass
```

```python
# drift_detector.py
"""Detect data drift over time."""

import pandas as pd
import numpy as np
from typing import Dict, List
import matplotlib.pyplot as plt
import seaborn as sns


class DataDriftDetector:
    """Monitor and detect data drift."""

    def __init__(self, reference_data: pd.DataFrame):
        self.reference_data = reference_data
        self.validator = StatisticalValidator(reference_data)
        self.drift_history = []

    def detect_drift(
        self,
        new_data: pd.DataFrame,
        timestamp: str = None
    ) -> Dict:
        """
        Detect drift in new data batch.

        Args:
            new_data: New data batch
            timestamp: Timestamp for this batch

        Returns:
            Drift detection results
        """
        # TODO: Run statistical validations
        results = self.validator.validate_all(new_data)

        # TODO: Identify drifted features
        drifted_features = [
            r for r in results
            if not r.passed and r.check_name.startswith('distribution')
        ]

        # TODO: Calculate drift score
        drift_score = len(drifted_features) / len(results)

        # TODO: Create drift report
        drift_report = {
            'timestamp': timestamp or pd.Timestamp.now(),
            'drift_score': drift_score,
            'drifted_features': [r.details.get('column') for r in drifted_features],
            'validation_results': results
        }

        # TODO: Store in history
        self.drift_history.append(drift_report)

        return drift_report

    def plot_drift_over_time(self, save_path: str = None):
        """
        Plot drift score over time.

        Args:
            save_path: Optional path to save plot
        """
        # TODO: Extract timestamps and drift scores
        # TODO: Create time series plot
        # TODO: Add threshold line
        # TODO: Save or show plot
        pass

    def generate_drift_report(self) -> str:
        """Generate human-readable drift report."""
        # TODO: Create formatted report
        # - Current drift status
        # - Trend over time
        # - Most frequently drifted features
        # - Recommendations
        pass
```

### Validation Tests

```python
# tests/test_statistical_validation.py
"""Tests for statistical validation."""

import pytest
import pandas as pd
import numpy as np
from statistical_validator import StatisticalValidator, OutlierDetector


def test_distribution_validation_no_drift(reference_data):
    """Test that same distribution passes validation."""
    validator = StatisticalValidator(reference_data)

    # TODO: Create data from same distribution
    # TODO: Validate distribution
    # TODO: Assert passed=True
    pass


def test_distribution_validation_detects_drift(reference_data):
    """Test that shifted distribution fails validation."""
    validator = StatisticalValidator(reference_data)

    # TODO: Create data with shifted distribution
    # TODO: Validate distribution
    # TODO: Assert passed=False
    pass


def test_outlier_detection_isolation_forest():
    """Test Isolation Forest outlier detection."""
    # TODO: Create data with known outliers
    # TODO: Run detection
    # TODO: Assert outliers are detected
    pass


@pytest.fixture
def reference_data():
    """Generate reference data."""
    np.random.seed(42)
    return pd.DataFrame({
        'feature1': np.random.normal(100, 15, 1000),
        'feature2': np.random.exponential(2, 1000),
        'feature3': np.random.uniform(0, 100, 1000)
    })

# Run with: pytest tests/test_statistical_validation.py -v
```

### Success Criteria

- [ ] Statistical validator computes reference statistics
- [ ] Distribution tests (KS, Chi-square) work correctly
- [ ] Multiple outlier detection methods implemented
- [ ] Correlation structure validation works
- [ ] Drift detector identifies shifted distributions
- [ ] Ensemble outlier detection combines methods
- [ ] Tests pass for various scenarios

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **KS Test**: Use `scipy.stats.ks_2samp()` for continuous distributions
2. **IQR Method**: `Q1 - 1.5*IQR` to `Q3 + 1.5*IQR` for outlier bounds
3. **Isolation Forest**: Set `contamination` based on expected outlier rate
4. **Correlation**: Use `pandas.DataFrame.corr()` for correlation matrix
5. **Ensemble**: Combine multiple methods with voting (2/3 methods agree)
6. **Performance**: Use vectorized operations instead of loops

</details>

---

## Exercise 4: Data Profiling & Anomaly Detection (90 minutes)

**Objective**: Build automated data profiling and anomaly detection system.

### Background

You need to automatically profile datasets to:
- Generate comprehensive data reports
- Detect anomalies in production data
- Compare datasets (train vs. test vs. production)
- Create data quality dashboards

### Tasks

1. **Implement comprehensive data profiler**
2. **Create anomaly detection pipeline**
3. **Build dataset comparison tool**
4. **Generate HTML profiling reports**
5. **Create real-time monitoring dashboard**

### Starter Code

```python
# data_profiler.py
"""Comprehensive data profiling for ML datasets."""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import json
from pathlib import Path


@dataclass
class ColumnProfile:
    """Profile for a single column."""
    name: str
    dtype: str
    count: int
    missing_count: int
    missing_percentage: float
    unique_count: int
    unique_percentage: float

    # For numerical columns
    mean: Optional[float] = None
    std: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    q25: Optional[float] = None
    median: Optional[float] = None
    q75: Optional[float] = None
    skewness: Optional[float] = None
    kurtosis: Optional[float] = None

    # For categorical columns
    mode: Optional[str] = None
    mode_frequency: Optional[int] = None
    top_values: Optional[Dict] = None

    # Data quality flags
    has_outliers: bool = False
    has_high_cardinality: bool = False
    is_constant: bool = False
    is_unique_id: bool = False


@dataclass
class DatasetProfile:
    """Complete dataset profile."""
    name: str
    n_rows: int
    n_columns: int
    memory_usage_mb: float
    duplicate_rows: int
    column_profiles: List[ColumnProfile]
    correlations: Optional[Dict] = None
    warnings: List[str] = None


class DataProfiler:
    """Generate comprehensive data profiles."""

    def __init__(self, high_cardinality_threshold: int = 100):
        self.high_cardinality_threshold = high_cardinality_threshold

    def profile_column(
        self,
        series: pd.Series,
        detect_outliers: bool = True
    ) -> ColumnProfile:
        """
        Profile a single column.

        Args:
            series: Pandas Series to profile
            detect_outliers: Whether to detect outliers

        Returns:
            ColumnProfile with statistics
        """
        # TODO: Implement column profiling
        # - Basic stats (count, missing, unique)
        # - Type-specific stats (numerical vs categorical)
        # - Outlier detection
        # - Quality flags
        pass

    def profile_dataset(
        self,
        df: pd.DataFrame,
        name: str = "dataset",
        compute_correlations: bool = True
    ) -> DatasetProfile:
        """
        Profile entire dataset.

        Args:
            df: DataFrame to profile
            name: Dataset name
            compute_correlations: Whether to compute correlation matrix

        Returns:
            DatasetProfile
        """
        # TODO: Implement dataset profiling
        # - Overall statistics
        # - Profile each column
        # - Compute correlations
        # - Generate warnings
        pass

    def detect_data_quality_issues(
        self,
        profile: DatasetProfile
    ) -> List[str]:
        """
        Detect data quality issues from profile.

        Args:
            profile: Dataset profile

        Returns:
            List of data quality warnings
        """
        warnings = []

        # TODO: Check for issues
        # - High missing rate (>20%)
        # - High duplicate rate (>5%)
        # - Constant columns
        # - High cardinality categoricals
        # - Highly correlated features (>0.95)
        # - Columns with all unique values (potential IDs)
        # - Imbalanced target variable

        return warnings

    def compare_profiles(
        self,
        profile1: DatasetProfile,
        profile2: DatasetProfile
    ) -> Dict:
        """
        Compare two dataset profiles.

        Args:
            profile1: First dataset profile
            profile2: Second dataset profile

        Returns:
            Comparison report
        """
        # TODO: Compare profiles
        # - Schema differences
        # - Statistical differences
        # - Distribution changes
        # - Return detailed comparison
        pass

    def export_profile(
        self,
        profile: DatasetProfile,
        output_path: str,
        format: str = 'json'
    ):
        """
        Export profile to file.

        Args:
            profile: Dataset profile
            output_path: Output file path
            format: Export format ('json', 'html', 'markdown')
        """
        # TODO: Export profile
        if format == 'json':
            # TODO: Export as JSON
            pass
        elif format == 'html':
            # TODO: Generate HTML report
            pass
        elif format == 'markdown':
            # TODO: Generate Markdown report
            pass
```

```python
# anomaly_detector.py
"""Production anomaly detection system."""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


class ProductionAnomalyDetector:
    """Real-time anomaly detection for production data."""

    def __init__(
        self,
        reference_data: pd.DataFrame,
        contamination: float = 0.05
    ):
        """
        Initialize anomaly detector.

        Args:
            reference_data: Clean reference data for training
            contamination: Expected anomaly rate
        """
        self.reference_data = reference_data
        self.contamination = contamination
        self.scaler = StandardScaler()
        self.detector = None
        self._train_detector()

    def _train_detector(self):
        """Train anomaly detection model on reference data."""
        # TODO: Prepare data
        # - Select numerical features
        # - Handle missing values
        # - Scale features

        # TODO: Train Isolation Forest
        # self.detector = IsolationForest(
        #     contamination=self.contamination,
        #     random_state=42
        # )
        # self.detector.fit(scaled_data)
        pass

    def detect_anomalies(
        self,
        data: pd.DataFrame,
        return_scores: bool = True
    ) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Detect anomalies in new data.

        Args:
            data: New data to check
            return_scores: Whether to return anomaly scores

        Returns:
            Tuple of (anomaly_labels, anomaly_scores)
        """
        # TODO: Preprocess data
        # TODO: Predict anomalies
        # TODO: Return labels and optionally scores
        pass

    def detect_point_anomaly(
        self,
        data_point: Dict
    ) -> Dict:
        """
        Detect if single data point is anomalous.

        Args:
            data_point: Dictionary with feature values

        Returns:
            Detection result with details
        """
        # TODO: Convert to DataFrame
        # TODO: Detect anomaly
        # TODO: Return detailed result
        pass

    def get_anomaly_explanation(
        self,
        data_point: Dict,
        top_n: int = 5
    ) -> List[Dict]:
        """
        Explain why a point is anomalous.

        Args:
            data_point: Anomalous data point
            top_n: Number of top contributing features

        Returns:
            List of feature contributions
        """
        # TODO: Calculate feature contributions
        # - Compare to reference statistics
        # - Identify most unusual features
        # - Return ranked explanations
        pass


class AnomalyMonitor:
    """Monitor anomalies over time."""

    def __init__(self, detector: ProductionAnomalyDetector):
        self.detector = detector
        self.anomaly_history = []

    def log_batch(
        self,
        batch_data: pd.DataFrame,
        timestamp: str = None
    ) -> Dict:
        """
        Process and log a batch of data.

        Args:
            batch_data: Batch to process
            timestamp: Batch timestamp

        Returns:
            Batch anomaly report
        """
        # TODO: Detect anomalies in batch
        # TODO: Calculate metrics
        # TODO: Log to history
        # TODO: Return report
        pass

    def get_anomaly_rate_over_time(self) -> pd.DataFrame:
        """Get time series of anomaly rates."""
        # TODO: Extract anomaly rates from history
        # TODO: Return as DataFrame
        pass

    def alert_if_threshold_exceeded(
        self,
        threshold: float = 0.10
    ) -> Optional[str]:
        """
        Check if recent anomaly rate exceeds threshold.

        Args:
            threshold: Anomaly rate threshold

        Returns:
            Alert message if threshold exceeded
        """
        # TODO: Calculate recent anomaly rate
        # TODO: Compare to threshold
        # TODO: Return alert if exceeded
        pass
```

```python
# comparison_report.py
"""Generate dataset comparison reports."""

import pandas as pd
from data_profiler import DataProfiler, DatasetProfile


def compare_train_test_production(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    production_df: pd.DataFrame
) -> str:
    """
    Compare training, test, and production datasets.

    Args:
        train_df: Training data
        test_df: Test data
        production_df: Production data

    Returns:
        Formatted comparison report
    """
    profiler = DataProfiler()

    # TODO: Profile each dataset
    train_profile = profiler.profile_dataset(train_df, "training")
    test_profile = profiler.profile_dataset(test_df, "test")
    prod_profile = profiler.profile_dataset(production_df, "production")

    # TODO: Compare profiles
    train_test_comparison = profiler.compare_profiles(train_profile, test_profile)
    train_prod_comparison = profiler.compare_profiles(train_profile, prod_profile)

    # TODO: Generate report
    # - Schema differences
    # - Distribution differences
    # - Data quality differences
    # - Recommendations

    # TODO: Return formatted report
    pass
```

### Success Criteria

- [ ] Data profiler generates complete column profiles
- [ ] Dataset-level statistics computed correctly
- [ ] Anomaly detector trained on reference data
- [ ] Real-time anomaly detection works
- [ ] Profile comparison identifies differences
- [ ] HTML reports generated
- [ ] Monitoring tracks anomalies over time

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Profiling**: Use `df.describe()`, `df.dtypes`, `df.memory_usage()` for basics
2. **Categorical Stats**: Use `value_counts()` for mode and top values
3. **Outlier Detection**: Use IQR method or Isolation Forest
4. **Correlations**: Use `df.corr()` but only for numerical columns
5. **HTML Export**: Use Jinja2 templates or pandas `to_html()`
6. **Anomaly Explanation**: Calculate z-scores for each feature

</details>

---

## Exercise 5: End-to-End Data Quality Pipeline (120 minutes)

**Objective**: Build a complete production-ready data quality pipeline integrating all components.

### Background

Create an end-to-end data quality system that:
1. Validates incoming data with Pydantic schemas
2. Runs Great Expectations test suite
3. Performs statistical validation
4. Detects anomalies
5. Generates quality reports
6. Blocks low-quality data from reaching models
7. Integrates with CI/CD

### Components

This exercise integrates everything from Exercises 1-4.

### Starter Code

```python
# data_quality_pipeline.py
"""Complete end-to-end data quality pipeline."""

from typing import Dict, Tuple
import pandas as pd
from dataclasses import dataclass
import logging

from schemas import CustomerDataSchema, validate_dataframe
from statistical_validator import StatisticalValidator
from anomaly_detector import ProductionAnomalyDetector
from data_profiler import DataProfiler


@dataclass
class QualityReport:
    """Complete data quality report."""
    passed: bool
    schema_validation_passed: bool
    statistical_validation_passed: bool
    ge_validation_passed: bool
    anomaly_rate: float
    quality_score: float
    errors: List[str]
    warnings: List[str]
    details: Dict


class DataQualityPipeline:
    """End-to-end data quality validation pipeline."""

    def __init__(
        self,
        reference_data: pd.DataFrame,
        ge_context=None,
        checkpoint_name: str = None
    ):
        """
        Initialize pipeline with reference data.

        Args:
            reference_data: Clean reference dataset
            ge_context: Great Expectations context
            checkpoint_name: GE checkpoint name
        """
        # TODO: Initialize all validators
        self.schema = CustomerDataSchema
        self.stat_validator = StatisticalValidator(reference_data)
        self.anomaly_detector = ProductionAnomalyDetector(reference_data)
        self.profiler = DataProfiler()
        self.ge_context = ge_context
        self.checkpoint_name = checkpoint_name

        # TODO: Configure logging
        self.logger = logging.getLogger(__name__)

    def validate(
        self,
        data: pd.DataFrame,
        strict: bool = False
    ) -> QualityReport:
        """
        Run complete validation pipeline.

        Args:
            data: Data to validate
            strict: If True, fail on any validation error

        Returns:
            QualityReport with results
        """
        errors = []
        warnings = []

        # ============================================
        # STEP 1: Schema Validation
        # ============================================
        self.logger.info("Running schema validation...")

        # TODO: Validate DataFrame with Pydantic schema
        # valid_df, schema_errors = validate_dataframe(data, self.schema)
        # schema_passed = len(schema_errors) == 0

        # TODO: Log schema validation results
        # if schema_errors:
        #     errors.extend([f"Schema: {e['error']}" for e in schema_errors[:10]])

        # ============================================
        # STEP 2: Statistical Validation
        # ============================================
        self.logger.info("Running statistical validation...")

        # TODO: Run statistical validations
        # stat_results = self.stat_validator.validate_all(valid_df)
        # stat_passed = all(r.passed for r in stat_results)

        # TODO: Collect statistical warnings
        # for result in stat_results:
        #     if not result.passed:
        #         warnings.append(f"Statistical: {result.check_name} failed")

        # ============================================
        # STEP 3: Great Expectations Validation
        # ============================================
        self.logger.info("Running Great Expectations...")

        ge_passed = True
        # TODO: Run GE checkpoint if configured
        # if self.ge_context and self.checkpoint_name:
        #     ge_results = self.ge_context.run_checkpoint(self.checkpoint_name)
        #     ge_passed = ge_results["success"]

        # ============================================
        # STEP 4: Anomaly Detection
        # ============================================
        self.logger.info("Running anomaly detection...")

        # TODO: Detect anomalies
        # anomaly_labels, anomaly_scores = self.anomaly_detector.detect_anomalies(valid_df)
        # anomaly_rate = (anomaly_labels == -1).sum() / len(anomaly_labels)

        # TODO: Check anomaly threshold
        # if anomaly_rate > 0.15:
        #     warnings.append(f"High anomaly rate: {anomaly_rate:.1%}")

        # ============================================
        # STEP 5: Data Profiling
        # ============================================
        self.logger.info("Generating data profile...")

        # TODO: Profile data
        # profile = self.profiler.profile_dataset(valid_df)
        # profile_warnings = self.profiler.detect_data_quality_issues(profile)
        # warnings.extend(profile_warnings)

        # ============================================
        # STEP 6: Calculate Quality Score
        # ============================================

        # TODO: Calculate weighted quality score
        # quality_score = self._calculate_quality_score(
        #     schema_passed=schema_passed,
        #     stat_passed=stat_passed,
        #     ge_passed=ge_passed,
        #     anomaly_rate=anomaly_rate
        # )

        # ============================================
        # STEP 7: Determine Overall Pass/Fail
        # ============================================

        # TODO: Determine if data passes quality checks
        # passed = (
        #     schema_passed and
        #     stat_passed and
        #     ge_passed and
        #     anomaly_rate < 0.20 and
        #     quality_score >= 75
        # )

        # TODO: In strict mode, fail on any error
        # if strict and (errors or not passed):
        #     passed = False

        # ============================================
        # STEP 8: Generate Report
        # ============================================

        # TODO: Create QualityReport
        # report = QualityReport(
        #     passed=passed,
        #     schema_validation_passed=schema_passed,
        #     statistical_validation_passed=stat_passed,
        #     ge_validation_passed=ge_passed,
        #     anomaly_rate=anomaly_rate,
        #     quality_score=quality_score,
        #     errors=errors,
        #     warnings=warnings,
        #     details={...}
        # )

        # TODO: Log summary
        self.logger.info(f"Quality validation complete. Status: {'PASS' if passed else 'FAIL'}")
        self.logger.info(f"Quality score: {quality_score:.1f}/100")

        return report

    def _calculate_quality_score(
        self,
        schema_passed: bool,
        stat_passed: bool,
        ge_passed: bool,
        anomaly_rate: float
    ) -> float:
        """Calculate weighted quality score."""
        # TODO: Implement scoring
        # - Schema: 30 points (pass/fail)
        # - Statistical: 30 points (pass/fail)
        # - GE: 25 points (pass/fail)
        # - Anomaly rate: 15 points (based on rate)
        pass

    def generate_html_report(
        self,
        report: QualityReport,
        output_path: str
    ):
        """Generate HTML quality report."""
        # TODO: Create HTML report
        # - Overall status
        # - Validation results
        # - Errors and warnings
        # - Quality score visualization
        # - Recommendations
        pass
```

```python
# fastapi_integration.py
"""FastAPI integration for real-time validation."""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Initialize pipeline
# TODO: Load reference data
# TODO: Initialize DataQualityPipeline

class PredictionRequest(BaseModel):
    """Request for prediction with validation."""
    data: Dict


@app.post("/predict")
async def predict_with_validation(
    request: PredictionRequest,
    background_tasks: BackgroundTasks
):
    """Make prediction with data quality validation."""

    try:
        # TODO: Convert to DataFrame
        # TODO: Run validation pipeline
        # TODO: If validation fails, return error
        # TODO: If passes, make prediction
        # TODO: Log quality metrics in background
        pass

    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.get("/quality/stats")
async def get_quality_stats():
    """Get data quality statistics."""
    # TODO: Return quality metrics from monitoring
    pass
```

```python
# ci_cd_integration.py
"""CI/CD integration script."""

import sys
import argparse
from pathlib import Path


def run_quality_checks(data_path: str, strict: bool = True) -> int:
    """
    Run data quality checks in CI/CD pipeline.

    Args:
        data_path: Path to data file
        strict: Strict validation mode

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # TODO: Load data
    # TODO: Load reference data
    # TODO: Initialize pipeline
    # TODO: Run validation
    # TODO: Print report
    # TODO: Save report artifacts
    # TODO: Return appropriate exit code
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True)
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()

    exit_code = run_quality_checks(args.data, args.strict)
    sys.exit(exit_code)
```

### GitHub Actions Workflow

```yaml
# .github/workflows/data-quality.yml
name: Data Quality Checks

on:
  pull_request:
    paths:
      - 'data/**'
  push:
    branches: [main]

jobs:
  quality-checks:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run data quality validation
        run: |
          python ci_cd_integration.py --data data/new_batch.csv --strict

      - name: Upload quality report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: quality-report
          path: reports/quality_report.html
```

### Success Criteria

- [ ] Complete pipeline validates data through all stages
- [ ] Quality score calculated correctly
- [ ] HTML reports generated
- [ ] FastAPI integration works
- [ ] CI/CD integration fails build on quality issues
- [ ] Monitoring tracks quality over time
- [ ] Pipeline handles errors gracefully
- [ ] Performance acceptable (< 5 sec for 10k rows)

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Error Handling**: Use try-except blocks around each validation stage
2. **Logging**: Use logging module with appropriate levels (INFO, WARNING, ERROR)
3. **Quality Score**: Weight critical checks higher than warnings
4. **FastAPI**: Use BackgroundTasks for async logging
5. **CI/CD**: Exit with code 1 on failure, 0 on success
6. **HTML Reports**: Use Jinja2 templates or simple HTML formatting
7. **Performance**: Process in batches for large datasets

</details>

---

## Bonus Challenges

### Challenge 1: Automated Schema Inference

Build a system that automatically infers Pydantic schemas from data:
- Detect column types
- Infer validation rules from data distributions
- Generate schema code

### Challenge 2: Real-Time Quality Dashboard

Create a Streamlit dashboard that:
- Shows quality metrics in real-time
- Displays drift trends
- Alerts on quality degradation
- Allows drill-down into specific issues

### Challenge 3: Quality-Based Model Retraining

Implement a system that triggers model retraining when:
- Data quality score drops below threshold
- Significant drift detected
- Anomaly rate exceeds limit

---

## Submission Guidelines

For each exercise, submit:
1. **Code**: All implementation files
2. **Reports**: Generated data quality reports
3. **Tests**: Passing test suite
4. **Documentation**: Explanation of validation strategy
5. **Reflection**: Data quality insights and lessons learned

**Estimated Total Time**: 6-9 hours
**Difficulty**: Intermediate to Advanced

Good luck!
