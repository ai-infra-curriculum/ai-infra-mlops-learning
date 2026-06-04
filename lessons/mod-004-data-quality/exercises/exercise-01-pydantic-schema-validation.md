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
