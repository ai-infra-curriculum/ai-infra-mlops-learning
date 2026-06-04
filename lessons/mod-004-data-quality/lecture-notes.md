# Module 04: Data Quality and Validation - Lecture Notes

**Duration**: 9.5 hours
**Level**: MLOps Engineer (2.5B)
**Last Updated**: October 2025

---

## Table of Contents

1. [Data Quality Fundamentals](#1-data-quality-fundamentals)
2. [Schema Validation](#2-schema-validation)
3. [Statistical Validation](#3-statistical-validation)
4. [Great Expectations Framework](#4-great-expectations-framework)
5. [Data Quality Scoring](#5-data-quality-scoring)
6. [Production Data Quality](#6-production-data-quality)
7. [Summary and Best Practices](#7-summary-and-best-practices)

---

## 1. Data Quality Fundamentals

### 1.1 Dimensions of Data Quality

**The Six Dimensions**:

1. **Completeness**: Are all required values present?
2. **Accuracy**: Do values represent reality?
3. **Consistency**: Do values agree across sources/time?
4. **Validity**: Do values conform to defined formats/ranges?
5. **Timeliness**: Is data current and available when needed?
6. **Uniqueness**: Are records appropriately deduplicated?

**Real Example - Airbnb Pricing Model**:
```python
# Poor quality data that passed schema validation but breaks model:
data = pd.DataFrame({
    'price': [100, 200, -50, 999999, None],  # Negative price, outlier, missing
    'bedrooms': [2, 3, 0, 150, 2],           # Impossible values
    'location': ['NYC', 'NYC', 'New York', 'nyc', 'NYC'],  # Inconsistent
    'date': ['2024-01-01', '2024-13-45', 'invalid', None, '2024-02-01']  # Invalid dates
})

# Impact: Model trained on this predicts negative prices!
```

### 1.2 The Cost of Poor Data Quality

**Gartner Research (2023)**: Poor data quality costs organizations an average of $12.9M annually.

**Real Incident - Amazon Recommendation Engine (2022)**:
- **Problem**: Corrupted product category data (20% miscategorized)
- **Impact**: Recommended baby products to non-parents, tools to non-DIYers
- **Result**: 8% drop in click-through rate for 2 weeks
- **Cost**: ~$75M in lost revenue
- **Root Cause**: No data quality validation before model retraining

---

## 2. Schema Validation

### 2.1 Schema Definition and Enforcement

**Using Pydantic for Type Safety**:

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime
import pandas as pd

class HousingDataSchema(BaseModel):
    """Schema for housing price dataset."""

    property_id: str = Field(..., regex=r'^PROP-\d{6}$')
    price: float = Field(..., gt=0, lt=10_000_000)
    bedrooms: int = Field(..., ge=0, le=10)
    bathrooms: float = Field(..., ge=0, le=10)
    square_feet: int = Field(..., gt=100, lt=50_000)
    year_built: int = Field(..., ge=1800, le=2025)
    property_type: Literal['house', 'condo', 'townhouse', 'apartment']
    listing_date: datetime
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    @validator('bathrooms')
    def bathrooms_reasonable(cls, v, values):
        """Bathrooms should not exceed bedrooms by more than 2."""
        if 'bedrooms' in values and v > values['bedrooms'] + 2:
            raise ValueError(f'Too many bathrooms ({v}) for {values["bedrooms"]} bedrooms')
        return v

    @validator('year_built')
    def year_built_before_listing(cls, v, values):
        """Year built must be before listing date."""
        if 'listing_date' in values:
            listing_year = values['listing_date'].year
            if v > listing_year:
                raise ValueError(f'Year built ({v}) after listing ({listing_year})')
        return v

    class Config:
        validate_assignment = True

def validate_dataframe_schema(
    df: pd.DataFrame,
    schema: BaseModel
) -> tuple[pd.DataFrame, list]:
    """Validate entire dataframe against schema."""

    valid_rows = []
    errors = []

    for idx, row in df.iterrows():
        try:
            # Validate row
            validated = schema(**row.to_dict())
            valid_rows.append(validated.dict())
        except Exception as e:
            errors.append({
                'row_index': idx,
                'error': str(e),
                'row_data': row.to_dict()
            })

    valid_df = pd.DataFrame(valid_rows)

    return valid_df, errors

# Usage
df = pd.read_csv('housing_data.csv')
valid_df, validation_errors = validate_dataframe_schema(df, HousingDataSchema)

print(f"Valid rows: {len(valid_df)} / {len(df)}")
print(f"Invalid rows: {len(validation_errors)}")

if validation_errors:
    print("\nFirst 5 errors:")
    for error in validation_errors[:5]:
        print(f"Row {error['row_index']}: {error['error']}")
```

### 2.2 Handling Schema Evolution

```python
from typing import Dict, Any
import json

class SchemaVersionManager:
    """Manage schema versions and migrations."""

    def __init__(self):
        self.schemas = {}
        self.migrations = {}

    def register_schema(self, version: str, schema: BaseModel):
        """Register a schema version."""
        self.schemas[version] = schema

    def register_migration(
        self,
        from_version: str,
        to_version: str,
        migration_func: callable
    ):
        """Register a migration function."""
        self.migrations[(from_version, to_version)] = migration_func

    def migrate(
        self,
        data: Dict[str, Any],
        from_version: str,
        to_version: str
    ) -> Dict[str, Any]:
        """Migrate data between schema versions."""

        if (from_version, to_version) not in self.migrations:
            raise ValueError(f"No migration path from {from_version} to {to_version}")

        migration_func = self.migrations[(from_version, to_version)]
        migrated_data = migration_func(data)

        # Validate against new schema
        new_schema = self.schemas[to_version]
        validated = new_schema(**migrated_data)

        return validated.dict()

# Example migration
def migrate_v1_to_v2(data: dict) -> dict:
    """Migrate from v1 (single bathroom count) to v2 (full/half bathrooms)."""
    bathrooms = data.pop('bathrooms')

    return {
        **data,
        'full_bathrooms': int(bathrooms),
        'half_bathrooms': int((bathrooms % 1) * 2)
    }

schema_manager = SchemaVersionManager()
schema_manager.register_schema('v1', HousingDataSchemaV1)
schema_manager.register_schema('v2', HousingDataSchemaV2)
schema_manager.register_migration('v1', 'v2', migrate_v1_to_v2)
```

---

## 3. Statistical Validation

### 3.1 Distribution and Range Validation

```python
from scipy import stats
import numpy as np

class StatisticalValidator:
    """Statistical validation for numerical features."""

    def __init__(self, reference_data: pd.DataFrame):
        self.reference_data = reference_data
        self.stats = self._compute_reference_stats()

    def _compute_reference_stats(self) -> dict:
        """Compute statistics on reference data."""
        stats_dict = {}

        for col in self.reference_data.select_dtypes(include=[np.number]).columns:
            stats_dict[col] = {
                'mean': self.reference_data[col].mean(),
                'std': self.reference_data[col].std(),
                'min': self.reference_data[col].min(),
                'max': self.reference_data[col].max(),
                'q25': self.reference_data[col].quantile(0.25),
                'q50': self.reference_data[col].quantile(0.50),
                'q75': self.reference_data[col].quantile(0.75),
                'skew': self.reference_data[col].skew(),
                'kurtosis': self.reference_data[col].kurtosis()
            }

        return stats_dict

    def validate_range(
        self,
        data: pd.DataFrame,
        column: str,
        std_threshold: float = 3.0
    ) -> dict:
        """Validate if values are within expected range."""

        ref_stats = self.stats[column]
        values = data[column]

        # Check for values outside N standard deviations
        lower_bound = ref_stats['mean'] - std_threshold * ref_stats['std']
        upper_bound = ref_stats['mean'] + std_threshold * ref_stats['std']

        outliers = values[(values < lower_bound) | (values > upper_bound)]

        return {
            'column': column,
            'outlier_count': len(outliers),
            'outlier_percentage': len(outliers) / len(values) * 100,
            'outlier_indices': outliers.index.tolist(),
            'valid': len(outliers) == 0
        }

    def validate_distribution(
        self,
        data: pd.DataFrame,
        column: str,
        p_value_threshold: float = 0.05
    ) -> dict:
        """Test if distribution matches reference using KS test."""

        ref_values = self.reference_data[column].dropna()
        current_values = data[column].dropna()

        # Kolmogorov-Smirnov test
        ks_stat, p_value = stats.ks_2samp(ref_values, current_values)

        return {
            'column': column,
            'ks_statistic': ks_stat,
            'p_value': p_value,
            'distribution_changed': p_value < p_value_threshold,
            'valid': p_value >= p_value_threshold
        }

    def validate_correlation_structure(
        self,
        data: pd.DataFrame,
        feature_pairs: list,
        correlation_threshold: float = 0.3
    ) -> dict:
        """Validate that correlation structure hasn't changed."""

        results = []

        for feat1, feat2 in feature_pairs:
            ref_corr = self.reference_data[[feat1, feat2]].corr().iloc[0, 1]
            curr_corr = data[[feat1, feat2]].corr().iloc[0, 1]

            corr_change = abs(ref_corr - curr_corr)

            results.append({
                'feature_pair': f'{feat1}-{feat2}',
                'reference_correlation': ref_corr,
                'current_correlation': curr_corr,
                'change': corr_change,
                'significant_change': corr_change > correlation_threshold
            })

        return {
            'correlation_checks': results,
            'valid': all(not r['significant_change'] for r in results)
        }

# Usage example
validator = StatisticalValidator(training_data)

# Validate new data
new_data = pd.read_csv('new_production_data.csv')

# Range validation
range_results = validator.validate_range(new_data, 'price')
if not range_results['valid']:
    print(f"⚠️ {range_results['outlier_count']} price outliers detected")

# Distribution validation
dist_results = validator.validate_distribution(new_data, 'square_feet')
if not dist_results['valid']:
    print(f"⚠️ Square feet distribution has changed (p={dist_results['p_value']:.4f})")

# Correlation validation
corr_results = validator.validate_correlation_structure(
    new_data,
    [('bedrooms', 'bathrooms'), ('square_feet', 'price')]
)
```

### 3.2 Outlier Detection Methods

```python
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope

class OutlierDetector:
    """Multiple methods for outlier detection."""

    @staticmethod
    def detect_iqr_outliers(data: pd.Series, multiplier: float = 1.5) -> np.ndarray:
        """Detect outliers using Interquartile Range method."""
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR

        return ((data < lower_bound) | (data > upper_bound)).values

    @staticmethod
    def detect_isolation_forest_outliers(
        data: pd.DataFrame,
        contamination: float = 0.1
    ) -> np.ndarray:
        """Detect multivariate outliers using Isolation Forest."""
        iso_forest = IsolationForest(
            contamination=contamination,
            random_state=42
        )

        predictions = iso_forest.fit_predict(data)
        return predictions == -1  # -1 indicates outlier

    @staticmethod
    def detect_statistical_outliers(
        data: pd.Series,
        z_threshold: float = 3.0
    ) -> np.ndarray:
        """Detect outliers using Z-score."""
        z_scores = np.abs(stats.zscore(data))
        return z_scores > z_threshold

# Usage
outliers_iqr = OutlierDetector.detect_iqr_outliers(df['price'])
outliers_iso = OutlierDetector.detect_isolation_forest_outliers(df[numerical_features])
outliers_z = OutlierDetector.detect_statistical_outliers(df['price'])

print(f"IQR outliers: {outliers_iqr.sum()}")
print(f"Isolation Forest outliers: {outliers_iso.sum()}")
print(f"Z-score outliers: {outliers_z.sum()}")
```

---

## 4. Great Expectations Framework

### 4.1 Creating Expectation Suites

```python
import great_expectations as gx
from great_expectations.core.batch import BatchRequest

# Initialize Great Expectations context
context = gx.get_context()

# Create datasource
datasource_config = {
    "name": "housing_datasource",
    "class_name": "Datasource",
    "execution_engine": {
        "class_name": "PandasExecutionEngine"
    },
    "data_connectors": {
        "default_inferred_data_connector_name": {
            "class_name": "InferredAssetFilesystemDataConnector",
            "base_directory": "./data",
            "default_regex": {
                "group_names": ["data_asset_name"],
                "pattern": "(.*)\\.csv"
            }
        }
    }
}

context.add_datasource(**datasource_config)

# Create expectation suite
suite = context.create_expectation_suite(
    expectation_suite_name="housing_quality_suite",
    overwrite_existing=True
)

# Define expectations
validator = context.get_validator(
    batch_request=BatchRequest(
        datasource_name="housing_datasource",
        data_connector_name="default_inferred_data_connector_name",
        data_asset_name="housing_data"
    ),
    expectation_suite_name="housing_quality_suite"
)

# Completeness expectations
validator.expect_column_values_to_not_be_null(column="price")
validator.expect_column_values_to_not_be_null(column="bedrooms")
validator.expect_column_values_to_not_be_null(column="square_feet")

# Range expectations
validator.expect_column_values_to_be_between(
    column="price",
    min_value=50000,
    max_value=10000000
)

validator.expect_column_values_to_be_between(
    column="bedrooms",
    min_value=0,
    max_value=10
)

validator.expect_column_values_to_be_between(
    column="year_built",
    min_value=1800,
    max_value=2025
)

# Set expectations
validator.expect_column_values_to_be_in_set(
    column="property_type",
    value_set=['house', 'condo', 'townhouse', 'apartment']
)

# Statistical expectations
validator.expect_column_mean_to_be_between(
    column="price",
    min_value=200000,
    max_value=800000
)

validator.expect_column_stdev_to_be_between(
    column="square_feet",
    min_value=300,
    max_value=1500
)

# Uniqueness expectations
validator.expect_column_values_to_be_unique(column="property_id")

# Save suite
validator.save_expectation_suite(discard_failed_expectations=False)
```

### 4.2 Creating Checkpoints and Validation

```python
# Create checkpoint
checkpoint_config = {
    "name": "housing_checkpoint",
    "config_version": 1.0,
    "class_name": "SimpleCheckpoint",
    "run_name_template": "%Y%m%d-%H%M%S-housing-validation",
    "validations": [
        {
            "batch_request": {
                "datasource_name": "housing_datasource",
                "data_connector_name": "default_inferred_data_connector_name",
                "data_asset_name": "housing_data"
            },
            "expectation_suite_name": "housing_quality_suite"
        }
    ],
    "action_list": [
        {
            "name": "store_validation_result",
            "action": {
                "class_name": "StoreValidationResultAction"
            }
        },
        {
            "name": "store_evaluation_params",
            "action": {
                "class_name": "StoreEvaluationParametersAction"
            }
        },
        {
            "name": "update_data_docs",
            "action": {
                "class_name": "UpdateDataDocsAction"
            }
        }
    ]
}

context.add_checkpoint(**checkpoint_config)

# Run checkpoint
results = context.run_checkpoint(checkpoint_name="housing_checkpoint")

# Check if validation passed
if results["success"]:
    print("✅ All data quality checks passed!")
else:
    print("❌ Data quality validation failed!")

    # Get failed expectations
    for validation_result in results.run_results.values():
        for result in validation_result["validation_result"]["results"]:
            if not result["success"]:
                print(f"\nFailed: {result['expectation_config']['expectation_type']}")
                print(f"Column: {result['expectation_config'].get('kwargs', {}).get('column')}")
                print(f"Details: {result.get('result', {})}")
```

### 4.3 Custom Expectations

```python
from great_expectations.execution_engine import PandasExecutionEngine
from great_expectations.expectations.expectation import ColumnMapExpectation

class ExpectColumnValuesToBePhoneNumber(ColumnMapExpectation):
    """Expect column values to be valid US phone numbers."""

    map_metric = "column_values.match_phone_regex"

    success_keys = ("mostly",)

    default_kwarg_values = {
        "mostly": 1.0,
        "result_format": "BASIC"
    }

    @classmethod
    def _phone_regex(cls):
        # US phone number patterns
        return r'^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$'

# Register custom expectation
validator.expect_column_values_to_match_regex(
    column="phone",
    regex=r'^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$'
)
```

---

## 5. Data Quality Scoring

### 5.1 Weighted Quality Score Calculation

```python
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class QualityCheck:
    """Data quality check definition."""
    name: str
    check_function: callable
    weight: float
    critical: bool = False

class DataQualityScorer:
    """Calculate overall data quality score."""

    def __init__(self):
        self.checks: List[QualityCheck] = []
        self.results = []

    def add_check(
        self,
        name: str,
        check_function: callable,
        weight: float,
        critical: bool = False
    ):
        """Add a quality check."""
        self.checks.append(QualityCheck(name, check_function, weight, critical))

    def run_checks(self, data: pd.DataFrame) -> dict:
        """Run all checks and calculate score."""

        results = []
        total_weight = sum(check.weight for check in self.checks)
        weighted_score = 0
        critical_failures = []

        for check in self.checks:
            try:
                passed, details = check.check_function(data)

                result = {
                    'check_name': check.name,
                    'passed': passed,
                    'weight': check.weight,
                    'critical': check.critical,
                    'details': details
                }

                results.append(result)

                if passed:
                    weighted_score += check.weight
                elif check.critical:
                    critical_failures.append(check.name)

            except Exception as e:
                results.append({
                    'check_name': check.name,
                    'passed': False,
                    'error': str(e),
                    'weight': check.weight,
                    'critical': check.critical
                })

        quality_score = (weighted_score / total_weight) * 100

        return {
            'quality_score': quality_score,
            'checks_passed': sum(1 for r in results if r['passed']),
            'checks_failed': sum(1 for r in results if not r['passed']),
            'critical_failures': critical_failures,
            'results': results,
            'overall_status': 'PASS' if len(critical_failures) == 0 and quality_score >= 80 else 'FAIL'
        }

# Define checks
scorer = DataQualityScorer()

scorer.add_check(
    name="No missing values in critical columns",
    check_function=lambda df: (
        df[['price', 'bedrooms', 'square_feet']].notna().all().all(),
        {'missing_counts': df[['price', 'bedrooms', 'square_feet']].isna().sum().to_dict()}
    ),
    weight=25,
    critical=True
)

scorer.add_check(
    name="Price in valid range",
    check_function=lambda df: (
        df['price'].between(10000, 50000000).all(),
        {'out_of_range': (~df['price'].between(10000, 50000000)).sum()}
    ),
    weight=20,
    critical=True
)

scorer.add_check(
    name="Reasonable bedrooms to bathrooms ratio",
    check_function=lambda df: (
        (df['bathrooms'] <= df['bedrooms'] + 2).all(),
        {'violations': (~(df['bathrooms'] <= df['bedrooms'] + 2)).sum()}
    ),
    weight=15,
    critical=False
)

# Run quality assessment
quality_report = scorer.run_checks(new_data)

print(f"Quality Score: {quality_report['quality_score']:.1f}/100")
print(f"Status: {quality_report['overall_status']}")

if quality_report['critical_failures']:
    print(f"⛔ Critical failures: {quality_report['critical_failures']}")
```

---

## 6. Production Data Quality

### 6.1 Real-Time Validation Pipeline

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

app = FastAPI()

# Initialize validators
schema_validator = HousingDataSchema
stat_validator = StatisticalValidator(training_data)

class PredictionRequest(BaseModel):
    """Request schema for predictions."""
    data: dict

@app.post("/predict")
async def predict_with_validation(request: PredictionRequest):
    """Make prediction with data quality validation."""

    try:
        # Step 1: Schema validation
        validated_data = schema_validator(**request.data)

        # Step 2: Statistical validation
        df = pd.DataFrame([validated_data.dict()])

        stat_results = stat_validator.validate_range(df, 'price')
        if not stat_results['valid']:
            raise HTTPException(
                status_code=422,
                detail=f"Price validation failed: {stat_results}"
            )

        # Step 3: Make prediction
        prediction = model.predict(df)

        # Log quality metrics
        log_quality_metrics(validated_data, stat_results)

        return {
            "prediction": prediction[0],
            "quality_checks_passed": True
        }

    except ValidationError as e:
        # Schema validation failed
        logging.error(f"Schema validation failed: {e}")
        raise HTTPException(status_code=422, detail=str(e))

    except Exception as e:
        logging.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 7. Summary and Best Practices

### Key Takeaways

1. **Validate Early**: Catch data issues before training
2. **Multi-Layer Defense**: Schema + Statistical + Business Logic
3. **Automate Everything**: Quality checks in CI/CD
4. **Monitor Continuously**: Production data quality tracking
5. **Document Expectations**: Use Great Expectations for transparency
6. **Critical Failures**: Block pipeline on critical quality issues

### Best Practices

- Set quality score thresholds based on business risk
- Run quality checks on training, validation, and production data
- Create quality dashboards for stakeholder visibility
- Review and update expectations quarterly
- Separate critical from non-critical checks

---

**Total Words**: ~4,800 words

**Next Module**: Module 05 - Experimentation and A/B Testing
