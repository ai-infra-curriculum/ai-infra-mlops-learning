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
