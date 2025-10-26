# Module 04: Data Quality & Validation - Quiz

## Instructions

- **Total Questions**: 28
- **Time Limit**: 40 minutes
- **Passing Score**: 75% (21/28 correct)
- **Question Types**: Multiple choice, multiple select, code analysis

---

## Section 1: Pydantic Schema Validation (Questions 1-6)

### Question 1
What is the primary purpose of using Pydantic for data validation in ML pipelines?

A) To visualize data distributions
B) To enforce type safety and data validation at runtime
C) To train machine learning models
D) To generate synthetic data

<details>
<summary>Answer</summary>

**B) To enforce type safety and data validation at runtime**

**Explanation**: Pydantic provides runtime type checking and validation for Python data structures. It ensures that incoming data conforms to expected schemas before it reaches your ML models, catching data quality issues early. Pydantic schemas define:
- Field types (int, float, str, etc.)
- Validation rules (ranges, patterns, custom logic)
- Required vs. optional fields
- Default values

This prevents invalid data from corrupting model training or predictions.

</details>

---

### Question 2
Examine this Pydantic schema:

```python
class CustomerSchema(BaseModel):
    age: int = Field(..., ge=18, le=100)
    income: float = Field(..., gt=0)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
```

What happens if you try to validate `{"age": 17, "income": 50000, "email": "valid@example.com"}`?

A) Validation passes
B) ValidationError for age only
C) ValidationError for all fields
D) ValidationError for email only

<details>
<summary>Answer</summary>

**B) ValidationError for age only**

**Explanation**: The age field has constraints `ge=18` (greater than or equal to 18) and `le=100`. The value 17 violates the `ge=18` constraint, so validation fails for age. The other fields are valid:
- `income: 50000` satisfies `gt=0` (greater than 0)
- `email: "valid@example.com"` matches the regex pattern

Pydantic will raise a ValidationError specifically identifying the age field as invalid.

</details>

---

### Question 3
**[Multiple Select]** Which of the following are valid Pydantic validators? (Select all that apply)

A) `@validator('field_name')` - validates a specific field
B) `@root_validator` - validates across multiple fields
C) `@property_validator` - validates object properties
D) Custom validation in `__init__` method
E) `Field(..., regex=r'pattern')` - validates string patterns

<details>
<summary>Answer</summary>

**A, B, E**

**Explanation**:
- **A**: `@validator` decorator validates individual fields with custom logic
- **B**: `@root_validator` validates relationships between multiple fields
- **C**: INCORRECT - Not a Pydantic validator type
- **D**: INCORRECT - Pydantic uses declarative validators, not `__init__` logic
- **E**: `Field()` with `regex` parameter validates string patterns

Example:
```python
class Schema(BaseModel):
    price: float
    discount: float

    @validator('discount')
    def discount_valid(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Discount must be 0-100')
        return v

    @root_validator
    def discounted_price_positive(cls, values):
        price = values.get('price')
        discount = values.get('discount')
        if price * (1 - discount/100) <= 0:
            raise ValueError('Discounted price must be positive')
        return values
```

</details>

---

### Question 4
What is the purpose of schema evolution and migration in production ML systems?

A) To train models faster
B) To handle changes in data structure over time without breaking systems
C) To compress data
D) To visualize model performance

<details>
<summary>Answer</summary>

**B) To handle changes in data structure over time without breaking systems**

**Explanation**: Schema evolution allows systems to handle changes in data structure gracefully:

**Common scenarios**:
- Adding new fields (e.g., adding `phone_number` field)
- Renaming fields (e.g., `total_spend` → `total_charges`)
- Changing field types (e.g., `int` → `float`)
- Splitting fields (e.g., `name` → `first_name`, `last_name`)

**Migration pattern**:
```python
def migrate_v1_to_v2(data: dict) -> dict:
    """Migrate from schema v1 to v2."""
    return {
        **data,
        'new_field': data.get('old_field', default_value),
        # Transform old structure to new
    }
```

Without proper schema management, data structure changes break production pipelines and require expensive system downtime.

</details>

---

### Question 5
In Pydantic, what does `Field(..., gt=0, le=1000)` mean?

A) Value must be greater than 0 or less than/equal to 1000
B) Value must be greater than 0 AND less than/equal to 1000
C) Value must be exactly 0 or 1000
D) Value must be between 0 and 1000 inclusive

<details>
<summary>Answer</summary>

**B) Value must be greater than 0 AND less than/equal to 1000**

**Explanation**: The constraints are combined with AND logic:
- `gt=0`: greater than 0 (exclusive: 0 is invalid)
- `le=1000`: less than or equal to 1000 (inclusive: 1000 is valid)

Valid range: 0 < value ≤ 1000

**Common constraint abbreviations**:
- `gt`: greater than (>)
- `ge`: greater than or equal to (≥)
- `lt`: less than (<)
- `le`: less than or equal to (≤)

Example valid values: 0.1, 1, 500, 999.99, 1000
Example invalid values: 0, -5, 1000.01, 2000

</details>

---

### Question 6
Why is it important to use `validate_assignment = True` in Pydantic Config?

A) It improves performance
B) It validates data when fields are modified after object creation
C) It generates automatic documentation
D) It enables async validation

<details>
<summary>Answer</summary>

**B) It validates data when fields are modified after object creation**

**Explanation**: By default, Pydantic only validates data during object initialization. With `validate_assignment = True`, validation also runs when you modify fields:

```python
class CustomerSchema(BaseModel):
    age: int = Field(..., ge=18)

    class Config:
        validate_assignment = True

# Without validate_assignment:
customer = CustomerSchema(age=25)
customer.age = 10  # No error! Validation skipped

# With validate_assignment:
customer = CustomerSchema(age=25)
customer.age = 10  # ValidationError! Age must be >= 18
```

This is critical in ML pipelines where data might be modified during preprocessing or feature engineering. It ensures data integrity throughout the pipeline, not just at entry points.

</details>

---

## Section 2: Great Expectations (Questions 7-12)

### Question 7
What is the primary purpose of Great Expectations in a data pipeline?

A) To train machine learning models
B) To define, test, and document data quality expectations
C) To visualize data
D) To compress datasets

<details>
<summary>Answer</summary>

**B) To define, test, and document data quality expectations**

**Explanation**: Great Expectations is a framework for:

1. **Defining Expectations**: Declarative data quality rules
   - "Column X should have no null values"
   - "Column Y should be between 0 and 100"
   - "Column Z should match regex pattern"

2. **Testing**: Automated validation against expectations
   - Run on every data batch
   - Catch quality issues before they affect models

3. **Documenting**: Auto-generated Data Docs
   - HTML documentation of expectations
   - Validation results with visualizations
   - Shareable with stakeholders

Great Expectations acts as a testing framework for data, similar to how pytest tests code. It catches data quality issues early, preventing bad data from reaching ML models.

</details>

---

### Question 8
Examine this Great Expectations code:

```python
validator.expect_column_values_to_be_between(
    column="price",
    min_value=0,
    max_value=10000,
    mostly=0.95
)
```

What does `mostly=0.95` mean?

A) 95% of values must be between 0 and 10000 for expectation to pass
B) Values must be exactly 95% of the max
C) The expectation is 95% confident
D) Sample 95% of rows for validation

<details>
<summary>Answer</summary>

**A) 95% of values must be between 0 and 10000 for expectation to pass**

**Explanation**: The `mostly` parameter allows for some tolerance in expectations:

- `mostly=0.95`: At least 95% of values must satisfy the expectation
- Allows for 5% outliers or edge cases
- Makes expectations more realistic for messy real-world data

**Without `mostly`** (default `mostly=1.0`):
- 100% of values must satisfy the expectation
- One outlier fails the entire validation
- Too strict for production data

**Example**:
```
Dataset: [10, 20, 30, ..., 99000]  # 100 values, one is 99000
Without mostly: FAIL (99000 > 10000)
With mostly=0.95: PASS (99 of 100 values valid = 99%)
```

This is useful for handling occasional data collection errors or legitimate outliers without failing the entire pipeline.

</details>

---

### Question 9
What is a Great Expectations checkpoint?

A) A save point in model training
B) A configuration that bundles validation runs and actions
C) A database snapshot
D) A git commit

<details>
<summary>Answer</summary>

**B) A configuration that bundles validation runs and actions**

**Explanation**: A checkpoint in Great Expectations bundles:

1. **Validation Configuration**:
   - Which data to validate
   - Which expectation suites to use
   - Batch configuration

2. **Actions**:
   - Store validation results
   - Update Data Docs
   - Send notifications (Slack, email)
   - Fail pipelines on validation errors

**Example**:
```python
checkpoint_config = {
    "name": "daily_data_check",
    "validations": [
        {
            "batch_request": {...},
            "expectation_suite_name": "customer_suite"
        }
    ],
    "action_list": [
        {"action": {"class_name": "StoreValidationResultAction"}},
        {"action": {"class_name": "UpdateDataDocsAction"}},
        {"action": {"class_name": "SlackNotificationAction"}}
    ]
}
```

Checkpoints enable automated, repeatable data quality validation in production pipelines.

</details>

---

### Question 10
**[Multiple Select]** Which of the following are valid Great Expectations expectation types? (Select all that apply)

A) `expect_column_to_exist`
B) `expect_column_values_to_not_be_null`
C) `expect_column_values_to_match_regex`
D) `expect_model_accuracy_above_threshold`
E) `expect_table_row_count_to_be_between`
F) `expect_column_mean_to_be_between`

<details>
<summary>Answer</summary>

**A, B, C, E, F**

**Explanation**:
- **A**: Schema expectation - validates column existence
- **B**: Completeness expectation - validates no nulls
- **C**: Pattern expectation - validates string format
- **D**: INCORRECT - Great Expectations validates data, not model metrics
- **E**: Table-level expectation - validates row count
- **F**: Statistical expectation - validates mean value

**Great Expectations categories**:
1. **Schema**: `expect_column_to_exist`, `expect_column_values_to_be_of_type`
2. **Completeness**: `expect_column_values_to_not_be_null`
3. **Validity**: `expect_column_values_to_be_between`, `expect_column_values_to_be_in_set`
4. **Pattern**: `expect_column_values_to_match_regex`
5. **Statistical**: `expect_column_mean_to_be_between`, `expect_column_stdev_to_be_between`
6. **Uniqueness**: `expect_column_values_to_be_unique`

</details>

---

### Question 11
What is the purpose of Data Docs in Great Expectations?

A) To train documentation models
B) To auto-generate HTML documentation of expectations and validation results
C) To compress data
D) To visualize model architecture

<details>
<summary>Answer</summary>

**B) To auto-generate HTML documentation of expectations and validation results**

**Explanation**: Data Docs provide:

1. **Expectation Documentation**:
   - What expectations are defined
   - Why they exist (business context)
   - Which data they apply to

2. **Validation Results**:
   - Pass/fail status
   - Visualizations of data distributions
   - Details of failures
   - Historical trends

3. **Shareable Reports**:
   - HTML format viewable in browser
   - Can be hosted on S3, GitHub Pages
   - Accessible to non-technical stakeholders

**Benefits**:
- Data quality transparency
- Stakeholder communication
- Debugging validation failures
- Onboarding new team members

Data Docs turn implicit data quality assumptions into explicit, testable, documented requirements.

</details>

---

### Question 12
How would you create a custom Great Expectations expectation for validating phone numbers?

A) Use `expect_column_values_to_match_regex` with phone regex
B) Extend `ColumnMapExpectation` class
C) Write a custom validator function
D) Both A and B are valid approaches

<details>
<summary>Answer</summary>

**D) Both A and B are valid approaches**

**Explanation**:

**Approach A - Use built-in regex expectation**:
```python
validator.expect_column_values_to_match_regex(
    column="phone",
    regex=r'^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$'
)
```
✅ Quick and simple
❌ Less reusable

**Approach B - Create custom expectation**:
```python
from great_expectations.expectations.expectation import ColumnMapExpectation

class ExpectColumnValuesToBeValidPhoneNumber(ColumnMapExpectation):
    """Expect column values to be valid US phone numbers."""

    map_metric = "column_values.phone_valid"

    @classmethod
    def _validate_phone(cls, value):
        # Custom validation logic
        pattern = r'^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$'
        return bool(re.match(pattern, value))
```
✅ Reusable across projects
✅ Can have complex logic
✅ Better documentation

For one-time use, use A. For reusable validation, use B.

</details>

---

## Section 3: Statistical Validation (Questions 13-18)

### Question 13
What is the Kolmogorov-Smirnov (KS) test used for in data quality validation?

A) To test if two samples come from the same distribution
B) To calculate mean and standard deviation
C) To detect outliers
D) To compress data

<details>
<summary>Answer</summary>

**A) To test if two samples come from the same distribution**

**Explanation**: The KS test compares distributions:

**Use case**: Detect data drift
```python
from scipy.stats import ks_2samp

# Reference data (training)
ref_data = training_df['feature'].values

# New data (production)
new_data = production_df['feature'].values

# Perform KS test
statistic, p_value = ks_2samp(ref_data, new_data)

if p_value < 0.05:
    print("⚠️ Distribution has changed significantly!")
else:
    print("✅ Distribution is consistent")
```

**Interpretation**:
- **p_value < 0.05**: Distributions are significantly different (drift detected)
- **p_value ≥ 0.05**: Distributions are statistically similar (no drift)

**Why it matters**:
- ML models trained on one distribution may fail on different distributions
- KS test provides early warning of data drift
- Triggers model retraining or investigation

</details>

---

### Question 14
Which outlier detection method assumes data follows a Gaussian distribution?

A) Isolation Forest
B) IQR (Interquartile Range) method
C) Elliptic Envelope
D) Local Outlier Factor

<details>
<summary>Answer</summary>

**C) Elliptic Envelope**

**Explanation**:

**Elliptic Envelope** (Robust Covariance):
- Assumes data is Gaussian (normal distribution)
- Fits an ellipse around the data
- Points outside ellipse are outliers
- Uses Mahalanobis distance

```python
from sklearn.covariance import EllipticEnvelope

detector = EllipticEnvelope(contamination=0.1)
outliers = detector.fit_predict(data)  # -1 for outliers
```

**Other methods**:
- **Isolation Forest** (A): No distribution assumption, works on any data
- **IQR method** (B): No distribution assumption, uses quartiles
- **Local Outlier Factor** (D): No distribution assumption, density-based

**When to use each**:
- **Gaussian data**: Elliptic Envelope (most accurate)
- **Non-Gaussian data**: Isolation Forest, LOF
- **Univariate data**: IQR method (simple and robust)

</details>

---

### Question 15
What does the IQR (Interquartile Range) outlier detection method identify as outliers?

A) Values more than 3 standard deviations from mean
B) Values below Q1 - 1.5×IQR or above Q3 + 1.5×IQR
C) Values in the top and bottom 5%
D) All values below the median

<details>
<summary>Answer</summary>

**B) Values below Q1 - 1.5×IQR or above Q3 + 1.5×IQR**

**Explanation**: The IQR method:

1. **Calculate quartiles**:
   - Q1 (25th percentile)
   - Q3 (75th percentile)
   - IQR = Q3 - Q1

2. **Define outlier bounds**:
   - Lower bound = Q1 - 1.5 × IQR
   - Upper bound = Q3 + 1.5 × IQR

3. **Identify outliers**:
   - Values < lower bound
   - Values > upper bound

**Example**:
```
Data: [10, 12, 15, 18, 20, 22, 25, 28, 30, 100]
Q1 = 15, Q3 = 28, IQR = 13
Lower bound = 15 - 1.5×13 = -4.5
Upper bound = 28 + 1.5×13 = 47.5
Outliers: [100]  (> 47.5)
```

**Advantages**:
- Robust to extreme outliers
- Doesn't assume normal distribution
- Simple to interpret
- Used in box plots

**1.5 multiplier**: Can be adjusted (2.0 for stricter, 1.0 for looser)

</details>

---

### Question 16
**[Multiple Select]** Which statistical properties should you monitor to detect data drift? (Select all that apply)

A) Mean
B) Standard deviation
C) Distribution shape (skewness, kurtosis)
D) File size
E) Correlation structure
F) Missing value rate

<details>
<summary>Answer</summary>

**A, B, C, E, F**

**Explanation**:

**Monitoring for drift**:

1. **Mean (A)**:
   - Detects shift in central tendency
   - Example: Average age increases from 35 to 45

2. **Standard deviation (B)**:
   - Detects change in variability
   - Example: Income spread increases (more inequality)

3. **Distribution shape (C)**:
   - Skewness: Detects asymmetry changes
   - Kurtosis: Detects tail thickness changes
   - Example: Price distribution becomes right-skewed

4. **File size (D)**: INCORRECT - Not a statistical property of data content

5. **Correlation structure (E)**:
   - Detects relationship changes between features
   - Example: Temperature-sales correlation weakens

6. **Missing value rate (F)**:
   - Detects data quality degradation
   - Example: Missing rate increases from 2% to 15%

**Comprehensive drift monitoring**:
```python
drift_metrics = {
    'mean': new_data.mean() - ref_data.mean(),
    'std': new_data.std() - ref_data.std(),
    'skew': new_data.skew() - ref_data.skew(),
    'missing_rate': new_data.isna().mean() - ref_data.isna().mean(),
    'correlation_change': abs(new_corr - ref_corr).max()
}
```

</details>

---

### Question 17
What is the purpose of comparing correlation structure between training and production data?

A) To detect feature engineering bugs
B) To detect if relationships between features have changed
C) To reduce dimensionality
D) To improve model accuracy

<details>
<summary>Answer</summary>

**B) To detect if relationships between features have changed**

**Explanation**: Correlation structure validation catches:

**1. Distribution drift in relationships**:
```
Training: bedrooms ↔ price correlation = 0.75
Production: bedrooms ↔ price correlation = 0.35
⚠️ Relationship has weakened!
```

**2. Feature engineering bugs**:
```
Training: feature_A ↔ feature_B correlation = 0.05
Production: feature_A ↔ feature_B correlation = 0.98
⚠️ Features became highly correlated (bug?)
```

**3. Data collection changes**:
```
Training: income ↔ credit_score correlation = 0.65
Production: income ↔ credit_score correlation = -0.10
⚠️ Data source may have changed
```

**Implementation**:
```python
def validate_correlation_structure(ref_data, new_data, threshold=0.3):
    ref_corr = ref_data.corr()
    new_corr = new_data.corr()
    diff = abs(ref_corr - new_corr)

    significant_changes = diff[diff > threshold]

    if len(significant_changes) > 0:
        alert("Correlation structure has changed!")
```

**Why it matters**: ML models learn from feature relationships. If relationships change, model predictions become unreliable.

</details>

---

### Question 18
In statistical validation, what does a p-value < 0.05 typically indicate?

A) The null hypothesis is true
B) The result is statistically significant (reject null hypothesis)
C) The data is of high quality
D) The model is accurate

<details>
<summary>Answer</summary>

**B) The result is statistically significant (reject null hypothesis)**

**Explanation**: P-value interpretation in data quality:

**Context: Testing for distribution drift**
```python
statistic, p_value = ks_2samp(training_data, production_data)
```

**Null hypothesis (H0)**: The distributions are the same
**Alternative hypothesis (H1)**: The distributions are different

**P-value interpretation**:
- **p < 0.05**: Reject H0 → Distributions ARE different (drift detected!)
- **p ≥ 0.05**: Fail to reject H0 → Distributions appear the same (no drift)

**Example**:
```
Training data: mean=100, std=15
Production data: mean=120, std=15

KS test: p_value = 0.002

Interpretation:
p < 0.05 → Significant difference
→ Distribution has drifted
→ Investigate and potentially retrain model
```

**Common mistake**: p < 0.05 does NOT mean the data is "good" or "bad". It means there's a statistically significant difference from the reference distribution.

**Threshold choice**:
- 0.05: Standard (5% false positive rate)
- 0.01: Stricter (1% false positive rate)
- 0.10: Looser (10% false positive rate)

</details>

---

## Section 4: Data Profiling (Questions 19-23)

### Question 19
What is the purpose of data profiling in ML pipelines?

A) To train models faster
B) To automatically generate comprehensive statistical summaries of datasets
C) To compress data
D) To visualize model architecture

<details>
<summary>Answer</summary>

**B) To automatically generate comprehensive statistical summaries of datasets**

**Explanation**: Data profiling provides:

**1. Statistical summaries**:
- Min, max, mean, median, std
- Percentiles (25th, 50th, 75th)
- Skewness, kurtosis

**2. Data quality metrics**:
- Missing value counts/percentages
- Duplicate row detection
- Outlier identification
- Cardinality (unique values)

**3. Data type information**:
- Inferred types (int, float, string, date)
- Type mismatches
- Constant columns

**4. Relationships**:
- Correlation matrix
- Feature interactions

**Use cases**:
```python
profiler = DataProfiler()
profile = profiler.profile_dataset(df)

# Outputs:
# - 15 columns analyzed
# - 3 columns with >20% missing values
# - 2 highly correlated features (r>0.95)
# - 1 constant column (remove?)
# - Price outliers detected (IQR method)
```

**Benefits**:
- Understand data before modeling
- Detect quality issues early
- Guide feature engineering
- Document datasets for stakeholders

</details>

---

### Question 20
Which of the following indicates high cardinality in a categorical feature?

A) Feature has 2-5 unique values
B) Feature has unique values close to the number of rows
C) Feature has no missing values
D) Feature is normally distributed

<details>
<summary>Answer</summary>

**B) Feature has unique values close to the number of rows**

**Explanation**: Cardinality = number of unique values

**Low cardinality** (2-20 unique values):
```
gender: ['Male', 'Female', 'Other']  # 3 unique values
→ Good for categorical encoding
→ Use one-hot encoding
```

**Medium cardinality** (20-100 unique values):
```
state: ['CA', 'NY', 'TX', ..., 'WY']  # 50 unique values
→ Consider target encoding or embeddings
```

**High cardinality** (100s-1000s of unique values):
```
user_id: ['USER001', 'USER002', ..., 'USER9999']  # 9999 unique values
→ ⚠️ Problem for one-hot encoding (creates too many columns)
→ Don't use directly as categorical feature
→ Consider: hashing, embeddings, or remove
```

**Detecting high cardinality**:
```python
def detect_high_cardinality(series, threshold=100):
    n_unique = series.nunique()
    cardinality_ratio = n_unique / len(series)

    return {
        'is_high_cardinality': n_unique > threshold,
        'unique_count': n_unique,
        'cardinality_ratio': cardinality_ratio,
        'likely_id_column': cardinality_ratio > 0.95
    }
```

**Red flag**: If cardinality ratio > 0.95, column is likely an ID (not a useful feature).

</details>

---

### Question 21
Examine this data profile output:

```
Column: customer_id
Unique values: 10000 / 10000 (100%)
Missing: 0 (0%)
Type: string
```

What does this profile suggest?

A) This is a good feature for the model
B) This column is likely a unique identifier, not a useful feature
C) This column has poor data quality
D) This column should be one-hot encoded

<details>
<summary>Answer</summary>

**B) This column is likely a unique identifier, not a useful feature**

**Explanation**: Profile analysis:

**Indicators of ID column**:
- ✅ 100% unique values (10000/10000)
- ✅ 0% missing (IDs are rarely missing)
- ✅ String type
- ✅ Name contains "id"

**Why not useful for ML**:
```python
# Model can't generalize from unique values
# Each customer_id appears exactly once in training
# New customer_ids in production are never seen before
# → Model learns nothing useful
```

**What to do**:
```python
# ❌ Don't use directly
X = df[['customer_id', 'age', 'income']]

# ✅ Drop ID columns
X = df.drop(['customer_id'], axis=1)

# ✅ Or use for joining/tracking only
df['customer_id']  # Keep for tracking, not for model
```

**Exception**: If using ID for entity embeddings:
```python
# Learn embedding for each customer_id
# Useful in deep learning with many samples per ID
```

**Red flags in profiling**:
- Cardinality ratio > 95%: Likely ID
- Constant column: Remove (no variation)
- Very high missing rate (>50%): Consider removing

</details>

---

### Question 22
What is the purpose of comparing training, validation, and production dataset profiles?

A) To train models faster
B) To detect data drift, distribution shifts, and data collection bugs
C) To compress datasets
D) To generate synthetic data

<details>
<summary>Answer</summary>

**B) To detect data drift, distribution shifts, and data collection bugs**

**Explanation**: Profile comparison reveals:

**1. Distribution shifts**:
```
Training:    age mean=35, std=12
Validation:  age mean=35, std=12  ✅ Consistent
Production:  age mean=52, std=8   ⚠️ Shift detected!
```

**2. Data collection bugs**:
```
Training:    income range: $20k-$200k
Validation:  income range: $22k-$190k  ✅ Similar
Production:  income range: $0-$0       ⚠️ Bug! All zeros
```

**3. Schema changes**:
```
Training:    15 columns
Validation:  15 columns  ✅ Match
Production:  14 columns  ⚠️ Missing column!
```

**4. Data quality degradation**:
```
Training:    missing rate: 2%
Validation:  missing rate: 3%   ✅ Acceptable
Production:  missing rate: 25%  ⚠️ Quality issue!
```

**Implementation**:
```python
def compare_profiles(train_profile, prod_profile):
    issues = []

    # Check schema
    if train_profile.n_columns != prod_profile.n_columns:
        issues.append("Column count mismatch")

    # Check distributions
    for col in train_profile.columns:
        train_mean = train_profile[col].mean
        prod_mean = prod_profile[col].mean

        if abs(train_mean - prod_mean) > 0.2 * train_mean:
            issues.append(f"{col}: Mean shifted by >20%")

    return issues
```

**Actions on detection**:
- Alert data engineering team
- Investigate data pipeline
- Hold back production predictions
- Retrain model if drift confirmed

</details>

---

### Question 23
**[Multiple Select]** Which of the following are red flags in a data profile? (Select all that apply)

A) Column with 100% unique values
B) Column with 0% missing values
C) Constant column (same value for all rows)
D) Numerical column with mean=50, std=10
E) Categorical column with 10,000 unique categories
F) Duplicate rows exceeding 10%

<details>
<summary>Answer</summary>

**A, C, E, F**

**Explanation**:

**Red flags**:

**A) 100% unique values**:
- Likely an ID column
- Not useful for ML models
- Action: Remove from features

**B) 0% missing values**: ✅ Good! (Not a red flag)

**C) Constant column**:
```
all_values = ['premium', 'premium', 'premium', ...]
→ No variance, no information
→ Action: Remove
```

**D) Normal statistics**: ✅ Good! (Not a red flag)

**E) 10,000 unique categories**:
- High cardinality problem
- One-hot encoding creates 10,000 columns
- Action: Use target encoding, embeddings, or remove

**F) >10% duplicate rows**:
```
10,000 rows → 1,000+ duplicates
→ Data collection bug?
→ Or legitimate repeated measurements?
→ Action: Investigate and deduplicate
```

**Other red flags**:
- Missing rate > 50%
- Negative values in positive-only columns (e.g., price)
- Dates in the future
- Extreme outliers (>10 std from mean)

</details>

---

## Section 5: Best Practices (Questions 24-28)

### Question 24
In a production ML pipeline, when should data quality validation occur?

A) Only during model training
B) Only before making predictions
C) At every stage: ingestion, preprocessing, training, and inference
D) Never, it's too expensive

<details>
<summary>Answer</summary>

**C) At every stage: ingestion, preprocessing, training, and inference**

**Explanation**: Multi-layer data quality defense:

**1. Data Ingestion** (Raw data):
```python
# Validate as data enters system
if not validate_schema(raw_data):
    reject_batch()
    alert_data_team()
```

**2. Preprocessing**:
```python
# Validate after transformations
preprocessed = preprocess(raw_data)
if not validate_distributions(preprocessed):
    investigate_preprocessing_bug()
```

**3. Training**:
```python
# Validate training data quality
if quality_score(train_data) < 80:
    alert("Low quality training data")
    halt_training()
```

**4. Inference** (Production):
```python
# Validate each prediction request
if not validate_input(request_data):
    return error(422, "Invalid input")

# Validate prediction output
if not validate_prediction(output):
    log_anomaly()
```

**Why multi-layer**:
- Catch issues early (cheaper to fix)
- Prevent error propagation
- Isolate failure points
- Maintain data lineage

**Cost vs. benefit**: Validation cost << Cost of bad predictions

</details>

---

### Question 25
What is the recommended approach for handling data that fails quality validation in production?

A) Always reject it immediately
B) Use a fallback/default value
C) Depends on severity: reject critical failures, flag warnings
D) Ignore validation errors

<details>
<summary>Answer</summary>

**C) Depends on severity: reject critical failures, flag warnings**

**Explanation**: Tiered response strategy:

**Critical failures** (REJECT):
```python
# Schema violations
if not isinstance(age, int):
    return Error(422, "Invalid data type")

# Business logic violations
if price < 0:
    return Error(422, "Price cannot be negative")

# Missing required fields
if user_id is None:
    return Error(422, "user_id required")
```

**Warnings** (FLAG but allow):
```python
# Statistical anomalies
if is_outlier(value):
    log_warning("Outlier detected")
    prediction = model.predict(value)  # Still predict
    add_confidence_penalty(prediction)
    return prediction

# Minor drift
if distribution_changed(value):
    trigger_retraining_evaluation()
    return model.predict(value)  # Still serve
```

**Implementation**:
```python
class ValidationResponse:
    REJECT = "reject"      # Don't process
    WARN = "warn"          # Process with warning
    ACCEPT = "accept"      # Process normally

def validate(data):
    if critical_failure(data):
        return ValidationResponse.REJECT
    elif warning_level_issue(data):
        return ValidationResponse.WARN
    else:
        return ValidationResponse.ACCEPT
```

**Response actions**:
- **REJECT**: Return error to user, log incident
- **WARN**: Process but log, monitor, investigate
- **ACCEPT**: Process normally

**Define thresholds** based on business impact:
- Healthcare: Strict (reject more)
- Recommendations: Lenient (warn more)

</details>

---

### Question 26
Examine this data quality pipeline:

```python
# Validate incoming data
valid_df, errors = validate_schema(df)

# If any errors, fail pipeline
if len(errors) > 0:
    raise ValidationError("Schema validation failed")

# Continue with valid data only
train_model(valid_df)
```

What is the problem with this approach?

A) It's too strict
B) It silently drops invalid rows without logging or analysis
C) It should use Great Expectations instead
D) There is no problem

<details>
<summary>Answer</summary>

**B) It silently drops invalid rows without logging or analysis**

**Explanation**: Problems with silent failure:

**❌ Bad practice**:
```python
valid_df, errors = validate_schema(df)
# Errors discarded! No visibility into:
# - How many rows failed?
# - Which validation rules failed?
# - Is this a one-time issue or systematic problem?

train_model(valid_df)  # Train on subset
```

**✅ Good practice**:
```python
valid_df, errors = validate_schema(df)

# 1. Log errors
logger.error(f"{len(errors)} rows failed validation")
for error in errors[:10]:  # Log first 10
    logger.error(f"Row {error['index']}: {error['message']}")

# 2. Calculate error rate
error_rate = len(errors) / len(df)

# 3. Take action based on threshold
if error_rate > 0.10:  # >10% failure
    alert_data_team()
    raise ValidationError(f"High validation failure rate: {error_rate:.1%}")
elif error_rate > 0.01:  # 1-10% failure
    log_warning(f"Moderate validation failures: {error_rate:.1%}")

# 4. Store errors for analysis
save_validation_errors(errors, timestamp=now())

# 5. Continue with valid data
train_model(valid_df)
```

**Why logging matters**:
- Detect systematic data issues
- Track data quality over time
- Debug pipeline problems
- Provide audit trail

**Never silently fail** - always log, monitor, and alert.

</details>

---

### Question 27
**[Multiple Select]** Which metrics should be tracked in a data quality monitoring dashboard? (Select all that apply)

A) Validation pass rate over time
B) Number of outliers detected
C) Model training time
D) Distribution drift scores
E) Missing value rates
F) Data freshness (time since last update)

<details>
<summary>Answer</summary>

**A, B, D, E, F**

**Explanation**:

**Data quality dashboard metrics**:

**A) Validation pass rate**:
```
Daily validation: [95%, 96%, 93%, 87%, 75%]
→ Declining trend! Investigate
```

**B) Outliers detected**:
```
Outlier rate: [2%, 2%, 3%, 15%]
→ Spike detected! Check data source
```

**C) Model training time**: Related to infrastructure, not data quality

**D) Distribution drift scores**:
```
KS statistic over time: [0.02, 0.03, 0.15, 0.35]
→ Increasing drift! Consider retraining
```

**E) Missing value rates**:
```
Missing rate by column:
- age: 2% → 2% (stable)
- income: 5% → 25% (⚠️ degradation!)
```

**F) Data freshness**:
```
Last data update: 2 hours ago
Expected: hourly
→ ⚠️ Data pipeline delay
```

**Dashboard implementation**:
```python
metrics = {
    'timestamp': now(),
    'validation_pass_rate': 0.95,
    'outlier_rate': 0.03,
    'drift_score': 0.08,
    'missing_rate': 0.05,
    'data_age_hours': 1.5
}

# Track over time
dashboard.log_metrics(metrics)

# Alert on thresholds
if metrics['validation_pass_rate'] < 0.90:
    alert("Validation pass rate dropped below 90%")
```

**Visualization**:
- Time series charts for trends
- Distribution comparisons
- Heatmaps for correlation changes
- Alerts for threshold violations

</details>

---

### Question 28
Why is it important to separate data quality checks into "critical" and "warning" levels?

A) To reduce computational cost
B) To avoid blocking production systems on minor issues while catching severe problems
C) To improve model accuracy
D) To compress data

<details>
<summary>Answer</summary>

**B) To avoid blocking production systems on minor issues while catching severe problems**

**Explanation**: Severity-based validation strategy:

**Critical checks** (Block production):
```python
CRITICAL_CHECKS = [
    # Schema violations
    "required_fields_present",
    "correct_data_types",

    # Business logic
    "price_not_negative",
    "age_within_valid_range",

    # Model requirements
    "no_null_in_model_features",
    "feature_count_matches_model"
]

if any_critical_check_fails():
    return Error(422)  # Block request
```

**Warning checks** (Log but allow):
```python
WARNING_CHECKS = [
    # Statistical anomalies
    "outlier_detected",
    "slight_distribution_drift",

    # Data quality concerns
    "high_missing_rate_in_optional_field",
    "unusual_correlation_pattern",

    # Performance monitoring
    "prediction_confidence_low"
]

if warning_check_fails():
    log_warning()      # Log for monitoring
    return prediction  # Still serve
```

**Benefits**:

1. **Availability**:
   - System stays online for minor issues
   - Avoid false-positive outages

2. **Safety**:
   - Critical issues still blocked
   - Prevent bad predictions

3. **Monitoring**:
   - Warnings signal degradation
   - Early warning system

4. **Balance**:
```
Too strict: ❌ Frequent outages, poor availability
Too lenient: ❌ Bad data reaches model
Just right: ✅ Block critical, warn minor
```

**Example categorization**:
```python
@dataclass
class ValidationRule:
    name: str
    check_fn: Callable
    severity: Literal["critical", "warning"]

rules = [
    ValidationRule("price_positive", lambda x: x['price'] > 0, "critical"),
    ValidationRule("price_reasonable", lambda x: x['price'] < 1000000, "warning"),
]
```

This enables **graceful degradation** - system operates with reduced confidence instead of hard failure.

</details>

---

## Scoring Guide

| Score | Grade | Feedback |
|-------|-------|----------|
| 26-28 | A+ | Excellent! You have mastered data quality validation |
| 23-25 | A | Great job! Strong understanding of data quality |
| 21-22 | B | Good. Review missed topics |
| 18-20 | C | Passing. Revisit key concepts |
| < 18 | F | Please review lecture notes and retry |

---

## Answer Key Summary

1. B | 2. B | 3. A,B,E | 4. B | 5. B
6. B | 7. B | 8. A | 9. B | 10. A,B,C,E,F
11. B | 12. D | 13. A | 14. C | 15. B
16. A,B,C,E,F | 17. B | 18. B | 19. B | 20. B
21. B | 22. B | 23. A,C,E,F | 24. C | 25. C
26. B | 27. A,B,D,E,F | 28. B

---

## Next Steps

- Review any missed questions
- Revisit corresponding lecture sections
- Complete hands-on exercises
- Implement data quality validation in your projects
- Practice with real-world datasets

**Good luck!**
