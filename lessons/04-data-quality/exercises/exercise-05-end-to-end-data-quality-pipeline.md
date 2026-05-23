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
