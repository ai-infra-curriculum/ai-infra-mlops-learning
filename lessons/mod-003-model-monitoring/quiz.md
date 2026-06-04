# Module 03: Model Monitoring - Quiz

## Instructions

- **Total Questions**: 28
- **Time Limit**: 40 minutes
- **Passing Score**: 75% (21/28 correct)
- **Question Types**: Multiple choice, multiple select, code analysis

---

## Section 1: Drift Detection Fundamentals (Questions 1-7)

### Question 1
What is the primary difference between data drift and concept drift?

A) Data drift is faster than concept drift
B) Data drift is a change in feature distributions; concept drift is a change in the relationship between features and target
C) Data drift only affects categorical features
D) There is no difference

<details>
<summary>Answer</summary>

**B) Data drift is a change in feature distributions; concept drift is a change in the relationship between features and target**

**Explanation**:
- **Data Drift (Covariate Shift)**: The distribution of input features P(X) changes, but P(Y|X) remains the same
- **Concept Drift**: The relationship P(Y|X) changes - same inputs produce different outputs over time
- Example Data Drift: Customer age distribution shifts from 25-35 to 45-55
- Example Concept Drift: Economic conditions change, so same customer profile has different default probability

</details>

---

### Question 2
What does the Kolmogorov-Smirnov (KS) test measure?

A) The mean difference between two distributions
B) The maximum distance between cumulative distribution functions of two samples
C) The correlation between features
D) The variance ratio between datasets

<details>
<summary>Answer</summary>

**B) The maximum distance between cumulative distribution functions of two samples**

**Explanation**: The KS test is a non-parametric test that measures:
- Maximum vertical distance between two empirical CDFs
- Returns KS statistic (0 to 1) and p-value
- P-value < threshold indicates distributions are significantly different
- Works well for continuous numerical features
- Sensitive to both location and shape differences

Formula: `D = max|F1(x) - F2(x)|` where F1, F2 are CDFs

</details>

---

### Question 3
**[Multiple Select]** Which scenarios indicate data drift that requires action? (Select all that apply)

A) Feature mean shifted by 0.01%
B) KS test p-value = 0.001 (threshold = 0.05) for critical feature
C) PSI = 0.25 for multiple features
D) All features have identical distributions to training data
E) 40% of features show PSI > 0.2

<details>
<summary>Answer</summary>

**B, C, E**

**Explanation**:
- **A**: INCORRECT - 0.01% shift is negligible and within normal variation
- **B**: CORRECT - p-value < 0.05 indicates significant distribution difference
- **C**: CORRECT - PSI > 0.2 indicates significant population shift
- **D**: INCORRECT - Identical distributions mean no drift, no action needed
- **E**: CORRECT - 40% of features drifting is severe, likely indicates data pipeline issues

Action thresholds:
- PSI < 0.1: No action
- PSI 0.1-0.2: Investigate
- PSI > 0.2: Take action

</details>

---

### Question 4
When should you retrain a model due to drift?

A) Immediately upon detecting any drift
B) When drift causes measurable performance degradation
C) Every week regardless of drift
D) Never - models should be static

<details>
<summary>Answer</summary>

**B) When drift causes measurable performance degradation**

**Explanation**: Not all drift requires retraining:
- **Statistical drift ≠ Performance drift**: Distributions can change without affecting model performance
- Monitor both drift metrics AND model performance
- Retrain when:
  - Performance drops below threshold (e.g., accuracy < 85%)
  - Drift is severe AND performance impacted
  - Business metrics are affected
- Avoid unnecessary retraining (expensive, risky)
- Establish clear retraining triggers based on business impact

</details>

---

### Question 5
Analyze this PSI calculation output:

```python
PSI Results:
  age: 0.08
  income: 0.15
  credit_score: 0.35
  employment_duration: 0.05
```

What action should be taken?

A) No action needed - all features are stable
B) Investigate credit_score feature immediately
C) Retrain model on all features
D) Ignore PSI values and rely only on accuracy

<details>
<summary>Answer</summary>

**B) Investigate credit_score feature immediately**

**Explanation**: PSI interpretation:
- **age (0.08)**: < 0.1, no significant change
- **income (0.15)**: 0.1-0.2, moderate change, monitor
- **credit_score (0.35)**: > 0.2, significant shift, **requires investigation**
- **employment_duration (0.05)**: < 0.1, stable

Actions for credit_score:
1. Check data pipeline for bugs
2. Verify data source changes
3. Analyze business context (e.g., policy changes)
4. Assess impact on model performance
5. Consider feature-specific retraining or removal

</details>

---

### Question 6
Why is it important to monitor both univariate and multivariate drift?

A) Univariate drift is always sufficient
B) Multivariate drift can detect feature interaction changes that univariate methods miss
C) Multivariate drift is easier to compute
D) Regulatory requirements

<details>
<summary>Answer</summary>

**B) Multivariate drift can detect feature interaction changes that univariate methods miss**

**Explanation**:
- **Univariate**: Tests each feature independently (KS test, PSI)
  - Pros: Simple, interpretable
  - Cons: Misses correlation changes
- **Multivariate**: Tests joint distribution (Chi-square, Mahalanobis distance)
  - Pros: Detects interaction changes
  - Cons: More complex, harder to interpret

Example: Two features individually stable but their correlation changed dramatically - only multivariate detection catches this.

Best practice: Use both approaches complementarily.

</details>

---

### Question 7
What is the null hypothesis in the KS test for drift detection?

A) The two distributions are different
B) The two distributions come from the same underlying distribution
C) The means are equal
D) The variances are equal

<details>
<summary>Answer</summary>

**B) The two distributions come from the same underlying distribution**

**Explanation**: KS test hypothesis:
- **H0 (null)**: Samples come from the same distribution (no drift)
- **H1 (alternative)**: Samples come from different distributions (drift detected)
- Low p-value (< 0.05): Reject H0, conclude drift exists
- High p-value (≥ 0.05): Fail to reject H0, no evidence of drift

Important: P-value is probability of observing data if H0 is true.

</details>

---

## Section 2: PSI and Statistical Methods (Questions 8-13)

### Question 8
How is PSI (Population Stability Index) calculated?

A) `PSI = Σ (current% - reference%) * log(current% / reference%)`
B) `PSI = |mean_current - mean_reference| / std_reference`
C) `PSI = max|CDF_current - CDF_reference|`
D) `PSI = correlation(current, reference)`

<details>
<summary>Answer</summary>

**A) `PSI = Σ (current% - reference%) * log(current% / reference%)`**

**Explanation**: PSI formula:
```
PSI = Σ (p_current - p_reference) * ln(p_current / p_reference)
```

Where:
- p_current = percentage of current data in bin i
- p_reference = percentage of reference data in bin i
- Sum over all bins (typically 10 bins)

Steps:
1. Create bins from reference data (quantile or uniform)
2. Calculate percentage in each bin for both datasets
3. Apply formula
4. Sum across bins

Edge case: Add small epsilon (1e-10) to avoid log(0)

</details>

---

### Question 9
Why do we typically use 10 bins for PSI calculation?

A) It's a regulatory requirement
B) It balances granularity and statistical stability
C) More bins always give better results
D) It's the mathematical maximum

<details>
<summary>Answer</summary>

**B) It balances granularity and statistical stability**

**Explanation**:
- **Too few bins (< 5)**: Loss of information, may miss subtle drift
- **Too many bins (> 20)**: Sparse bins, unstable estimates, noise sensitivity
- **10 bins**: Industry standard, good compromise
  - Each bin has ~10% of reference data
  - Sufficient granularity
  - Stable estimates

Adjust based on data volume:
- Large datasets (>100K): Can use 20 bins
- Small datasets (<1K): Use 5-7 bins

</details>

---

### Question 10
Analyze this code snippet:

```python
def calculate_psi(reference, current, bins=10):
    breakpoints = np.percentile(reference, np.linspace(0, 100, bins + 1))
    ref_percents = np.histogram(reference, breakpoints)[0] / len(reference)
    cur_percents = np.histogram(current, breakpoints)[0] / len(current)
    psi = np.sum((cur_percents - ref_percents) * np.log(cur_percents / ref_percents))
    return psi
```

What problem does this code have?

A) Bins should be uniform, not quantile-based
B) The PSI formula is incorrect
C) Division by zero / log(0) errors when percentages are 0
D) Using wrong numpy functions

<details>
<summary>Answer</summary>

**C) Division by zero / log(0) errors when percentages are 0**

**Explanation**: The code has critical bug:
- When a bin has 0 samples: `cur_percents[i] = 0`
- `np.log(0)` = `-inf`, causes NaN in result
- Also division by zero if computing `cur / ref`

**Fix**: Add small epsilon
```python
epsilon = 1e-10
cur_percents = np.maximum(cur_percents, epsilon)
ref_percents = np.maximum(ref_percents, epsilon)
```

This ensures numerical stability without significantly affecting PSI value.

</details>

---

### Question 11
When comparing PSI and KS test for drift detection, which statement is TRUE?

A) PSI is always better than KS test
B) KS test provides p-values for statistical significance; PSI provides a stability index
C) They always give the same results
D) PSI only works for categorical features

<details>
<summary>Answer</summary>

**B) KS test provides p-values for statistical significance; PSI provides a stability index**

**Explanation**:

**KS Test**:
- Statistical hypothesis test
- Returns p-value (significance)
- Non-parametric
- Sensitive to shape and location
- Best for: Statistical validation

**PSI**:
- Descriptive stability metric
- Returns index value (interpretable thresholds)
- Based on binning
- Industry-standard interpretation
- Best for: Business monitoring

**Use both**: KS test for statistical rigor, PSI for business communication.

</details>

---

### Question 12
**[Multiple Select]** Which factors can cause false positive drift detections? (Select all that apply)

A) Very large sample sizes making tiny differences statistically significant
B) Seasonal patterns in data
C) Bug in data collection
D) Appropriate choice of significance threshold
E) Multiple testing without correction

<details>
<summary>Answer</summary>

**A, B, E**

**Explanation**:
- **A**: CORRECT - With huge datasets (millions), even negligible differences become "statistically significant"
- **B**: CORRECT - Seasonal patterns look like drift but are expected variation (compare same season year-over-year)
- **C**: INCORRECT - This is actual drift/data quality issue, not false positive
- **D**: INCORRECT - Appropriate threshold reduces false positives
- **E**: CORRECT - Testing 100 features at α=0.05, expect 5 false positives. Use Bonferroni correction.

Solutions:
- Use effect size thresholds, not just p-values
- Account for seasonality in baseline
- Apply multiple testing correction

</details>

---

### Question 13
What is the recommended approach for monitoring high-cardinality categorical features?

A) Use PSI on all categories
B) Group rare categories and monitor top categories + "Other" bucket
C) Ignore categorical features
D) Convert to numerical encoding and use KS test

<details>
<summary>Answer</summary>

**B) Group rare categories and monitor top categories + "Other" bucket**

**Explanation**: High-cardinality challenges:
- 1000s of categories (e.g., product IDs, zip codes)
- Sparse data in each category
- Unstable drift estimates

**Best practices**:
1. Keep top-K categories (e.g., top 20 covering 80% of data)
2. Group remaining as "Other" or "Rare"
3. Monitor distribution of top categories
4. Track proportion in "Other" bucket
5. Consider embeddings for very high cardinality

Alternative: Chi-square test for categorical drift

</details>

---

## Section 3: Evidently AI and Tools (Questions 14-19)

### Question 14
What is the primary advantage of using Evidently AI over custom drift detection code?

A) It's always faster
B) It provides production-ready reports, tests, and dashboards with minimal code
C) It only works with Python
D) It doesn't require reference data

<details>
<summary>Answer</summary>

**B) It provides production-ready reports, tests, and dashboards with minimal code**

**Explanation**: Evidently AI benefits:
- Pre-built reports (drift, quality, performance)
- Interactive HTML dashboards
- Test suites with pass/fail
- Standardized metrics
- Minimal code required
- Easy integration

Example:
```python
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=ref, current_data=cur)
report.save_html('report.html')  # Interactive dashboard
```

vs. Custom: 100s of lines for equivalent functionality

</details>

---

### Question 15
In Evidently, what is the difference between a Report and a TestSuite?

A) Reports are faster than TestSuites
B) Reports provide detailed metrics and visualizations; TestSuites provide pass/fail assertions
C) TestSuites are deprecated
D) No difference

<details>
<summary>Answer</summary>

**B) Reports provide detailed metrics and visualizations; TestSuites provide pass/fail assertions**

**Explanation**:

**Report**:
- Descriptive analytics
- Rich visualizations
- Metric values
- For exploration and debugging

**TestSuite**:
- Pass/fail results
- Threshold-based assertions
- For CI/CD pipelines
- Automated decision making

Example:
```python
# Report - explore drift
report = Report(metrics=[DataDriftPreset()])
report.run(reference, current)

# TestSuite - automated testing
tests = TestSuite(tests=[
    TestShareOfDriftedColumns(lt=0.3)  # < 30% drifted
])
tests.run(reference, current)
assert tests.as_dict()['summary']['all_passed']
```

</details>

---

### Question 16
Analyze this Evidently configuration:

```python
column_mapping = ColumnMapping(
    target='is_fraud',
    prediction='fraud_prediction',
    numerical_features=['amount', 'age'],
    categorical_features=['merchant_category']
)
```

What is this configuration used for?

A) Training a model
B) Telling Evidently which columns are which types for proper analysis
C) Creating new features
D) Data cleaning

<details>
<summary>Answer</summary>

**B) Telling Evidently which columns are which types for proper analysis**

**Explanation**: ColumnMapping informs Evidently about:
- Which column is the target variable
- Which column contains predictions
- Which features are numerical (use KS test, mean/std)
- Which features are categorical (use chi-square, unique values)

This enables Evidently to:
- Choose appropriate statistical tests
- Generate correct visualizations
- Calculate relevant metrics
- Provide accurate drift detection

Without mapping, Evidently must infer types, potentially incorrectly.

</details>

---

### Question 17
**[Multiple Select]** Which metrics can Evidently AI monitor out-of-the-box? (Select all that apply)

A) Data drift per feature
B) Model performance (accuracy, precision, recall)
C) Data quality (missing values, duplicates)
D) Infrastructure costs
E) Prediction distribution drift

<details>
<summary>Answer</summary>

**A, B, C, E**

**Explanation**:
- **A**: ✓ DataDriftPreset provides per-feature drift metrics
- **B**: ✓ ClassificationPreset, RegressionPreset provide performance metrics
- **C**: ✓ DataQualityPreset provides quality checks
- **D**: ✗ Infrastructure monitoring is outside Evidently's scope (use Prometheus)
- **E**: ✓ Can detect drift in prediction distributions

Evidently focuses on ML-specific monitoring, not infrastructure.

</details>

---

### Question 18
How can you extract drift metrics from an Evidently report for automated alerting?

A) Reports are only visual, metrics cannot be extracted
B) Use `report.as_dict()` to get JSON representation of all metrics
C) Parse the HTML file
D) Re-calculate manually

<details>
<summary>Answer</summary>

**B) Use `report.as_dict()` to get JSON representation of all metrics**

**Explanation**: Programmatic access:

```python
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data, current_data)

# Extract as dictionary
metrics = report.as_dict()

# Access specific metrics
drift_score = metrics['metrics'][0]['result']['drift_score']
drifted_features = metrics['metrics'][0]['result']['number_of_drifted_columns']

# Use for alerting
if drift_score > 0.5:
    send_alert("High drift detected")
```

This enables integration with alerting systems (PagerDuty, Slack).

</details>

---

### Question 19
What is the purpose of the `reference_data` parameter in Evidently?

A) It's optional and not important
B) It represents the training data distribution as a baseline for comparison
C) It's the data to be tested
D) It stores test results

<details>
<summary>Answer</summary>

**B) It represents the training data distribution as a baseline for comparison**

**Explanation**: Reference data:
- Typically training data or initial production data
- Represents "known good" distribution
- Baseline for drift detection
- Should be representative and stable

Current data compared against reference:
- If distributions differ significantly → drift detected
- Reference should be updated periodically (e.g., after retraining)

Best practice: Store reference data with model version for reproducibility.

</details>

---

## Section 4: Monitoring Strategy (Questions 20-24)

### Question 20
What is the appropriate monitoring frequency for a high-traffic prediction API (1000s requests/second)?

A) Once per year
B) Once per month
C) Real-time per request
D) Batched hourly or daily

<details>
<summary>Answer</summary>

**D) Batched hourly or daily**

**Explanation**: Monitoring frequency tradeoffs:

**Too Frequent (per-request)**:
- Extremely expensive computationally
- Noisy signals (individual requests vary)
- Not statistically meaningful

**Too Infrequent (monthly)**:
- Slow to detect issues
- Large impact before detection

**Optimal (hourly/daily batches)**:
- Statistically significant sample size
- Timely detection (hours, not weeks)
- Reasonable computational cost
- Allows for time-of-day patterns

For 1000 req/s:
- Hourly batch = 3.6M samples (excellent for statistical tests)
- Daily batch = 86.4M samples

</details>

---

### Question 21
Which metrics should be monitored in production beyond just drift detection?

A) Only model accuracy
B) Drift, model performance, data quality, system health (latency, throughput)
C) Only infrastructure metrics
D) Only business KPIs

<details>
<summary>Answer</summary>

**B) Drift, model performance, data quality, system health (latency, throughput)**

**Explanation**: Comprehensive monitoring pyramid:

1. **System Health** (bottom layer):
   - Latency (p50, p95, p99)
   - Throughput (requests/second)
   - Error rate
   - Resource utilization (CPU, memory)

2. **Data Quality**:
   - Missing values
   - Schema validation
   - Range checks
   - Consistency

3. **Drift Detection**:
   - Feature drift (KS, PSI)
   - Prediction drift
   - Concept drift

4. **Model Performance** (when labels available):
   - Accuracy, precision, recall
   - Confusion matrix
   - Calibration

5. **Business Metrics** (top layer):
   - Revenue impact
   - User satisfaction
   - A/B test metrics

All layers are essential for production ML.

</details>

---

### Question 22
**[Multiple Select]** What should trigger a model retraining? (Select all that apply)

A) Every Monday regardless of performance
B) Model performance drops below acceptable threshold
C) Significant data drift that impacts performance
D) New labeled data becomes available with different distribution
E) A single outlier prediction

<details>
<summary>Answer</summary>

**B, C, D**

**Explanation**:
- **A**: INCORRECT - Calendar-based retraining ignores actual need, wasteful
- **B**: CORRECT - Performance degradation is primary trigger
- **C**: CORRECT - Drift causing performance impact requires retraining
- **D**: CORRECT - New data distribution with labels enables better model
- **E**: INCORRECT - Single outlier is noise, not systematic issue

**Retraining triggers**:
1. Performance-based: Accuracy < threshold for N consecutive days
2. Drift-based: PSI > 0.2 AND performance drops
3. Time-based: Every X months as fallback (e.g., quarterly)
4. Data-based: Sufficient new labeled data accumulated

Use combination of triggers with business context.

</details>

---

### Question 23
How should you handle seasonal patterns when monitoring for drift?

A) Ignore seasonality
B) Compare current data to same period in previous year(s), not to training data
C) Remove all seasonal features
D) Use only KS test

<details>
<summary>Answer</summary>

**B) Compare current data to same period in previous year(s), not to training data**

**Explanation**: Seasonality handling:

**Problem**: Training data from January, production data from December → drift detected, but it's expected seasonality

**Solutions**:
1. **Seasonal Baselines**: Compare December 2024 to December 2023
2. **Deseasonalization**: Remove seasonal component before drift testing
3. **Multiple References**: Maintain reference data for each season
4. **Time-aware Models**: Include time features in model

Example:
```python
# Instead of:
compare(training_data, current_data)  # ❌ Ignores seasonality

# Do:
compare(last_december_data, current_december_data)  # ✓
```

Critical for retail, finance, weather-dependent models.

</details>

---

### Question 24
What is the recommended approach for monitoring in a multi-model system?

A) Monitor only the final ensemble output
B) Monitor each model independently plus the ensemble
C) No monitoring needed for ensembles
D) Only monitor the best-performing model

<details>
<summary>Answer</summary>

**B) Monitor each model independently plus the ensemble**

**Explanation**: Multi-model monitoring:

**Monitor Each Component**:
- Individual model drift
- Individual model performance
- Detect which model is degrading

**Monitor Ensemble**:
- Overall system performance
- Ensemble prediction distribution
- Agreement/disagreement between models

**Benefits**:
- Isolate issues to specific models
- Understand ensemble behavior
- Replace degraded model without affecting ensemble
- Detect if ensemble weighting should change

Example: Fraud detection ensemble of 3 models
- Monitor each model's recall, precision
- Monitor ensemble metrics
- If Model B drifts, retrain just Model B

</details>

---

## Section 5: Alerting and Response (Questions 25-28)

### Question 25
What is alert fatigue, and how can it be prevented in ML monitoring?

A) Alerts getting tired from being triggered
B) Teams ignoring alerts due to too many false positives or low-priority alerts
C) Alerts becoming less accurate over time
D) Alerts requiring too much energy to send

<details>
<summary>Answer</summary>

**B) Teams ignoring alerts due to too many false positives or low-priority alerts**

**Explanation**: Alert fatigue prevention:

**Causes**:
- Too many alerts (low threshold)
- False positives (poor thresholds)
- Alerts for non-actionable issues
- No alert prioritization

**Prevention strategies**:
1. **Appropriate Thresholds**: Base on business impact, not just statistical significance
2. **Alert Prioritization**: INFO, WARNING, CRITICAL levels
3. **Aggregation**: Group related alerts, suppress duplicates
4. **Actionability**: Every alert must have clear action
5. **SLO-based**: Alert on SLO violations, not every metric deviation
6. **Feedback Loop**: Tune thresholds based on alert outcomes

Example: Instead of alerting on every feature with PSI > 0.1, alert when:
- PSI > 0.2 for critical features OR
- 30%+ features have PSI > 0.15 OR
- Model performance drops > 5%

</details>

---

### Question 26
What severity level should be assigned to a drift alert where PSI = 0.15 but model performance is stable?

A) CRITICAL - requires immediate action
B) WARNING - monitor but no immediate action
C) INFO - just logging
D) Don't alert at all

<details>
<summary>Answer</summary>

**B) WARNING - monitor but no immediate action**

**Explanation**: Severity guidelines:

**CRITICAL** (page on-call):
- Model performance degraded significantly
- System downtime
- Data quality issues affecting predictions
- PSI > 0.5 (severe drift)

**WARNING** (notify team):
- PSI 0.1-0.2 (moderate drift)
- Performance stable but drift present
- Investigate during business hours
- Monitor more frequently

**INFO** (log only):
- PSI < 0.1
- Normal variation
- FYI for team

PSI = 0.15 + stable performance → WARNING:
- Not urgent (performance OK)
- But worth investigating (might lead to future issues)
- Proactive monitoring

</details>

---

### Question 27
Analyze this alerting configuration:

```python
alert_rules = [
    AlertRule("drift", "psi", threshold=0.2, action="email"),
    AlertRule("performance", "accuracy", threshold=0.85, action="page"),
    AlertRule("latency", "p95_ms", threshold=100, action="email")
]
```

Which rule should likely have the highest priority?

A) drift
B) performance
C) latency
D) All equal priority

<details>
<summary>Answer</summary>

**B) performance**

**Explanation**: Priority rationale:

**Performance (accuracy < 0.85)**: HIGHEST
- Direct business impact
- Users getting wrong predictions NOW
- Action: "page" (appropriate for critical)
- Requires immediate investigation/rollback

**Latency (p95 > 100ms)**: MEDIUM-HIGH
- User experience impact
- SLA violation
- Action: "email" (appropriate)
- Needs attention soon

**Drift (PSI > 0.2)**: MEDIUM
- Leading indicator
- May not impact performance yet
- Action: "email" (appropriate)
- Investigate during business hours

Priority order: performance > latency > drift

Configure alerting to reflect this priority hierarchy.

</details>

---

### Question 28
What should be included in an ML monitoring alert runbook?

A) Just the error message
B) Alert description, impact assessment, investigation steps, mitigation actions, escalation path
C) Only who to contact
D) Monitoring dashboard link only

<details>
<summary>Answer</summary>

**B) Alert description, impact assessment, investigation steps, mitigation actions, escalation path**

**Explanation**: Comprehensive runbook:

**1. Alert Description**:
- What triggered the alert
- Threshold values
- Current metric values

**2. Impact Assessment**:
- Business impact (user-facing? revenue impact?)
- Urgency level
- Affected services/features

**3. Investigation Steps**:
```
1. Check monitoring dashboard
2. Query last N predictions
3. Compare to reference distribution
4. Check data pipeline logs
5. Verify data sources
```

**4. Mitigation Actions**:
- Immediate: Rollback to previous model
- Short-term: Increase monitoring frequency
- Long-term: Retrain model

**5. Escalation Path**:
- Primary: ML Engineer on-call
- Secondary: ML Team Lead
- If > 2 hours: Engineering Manager

Runbooks reduce MTTR (Mean Time To Resolution).

</details>

---

## Scoring Guide

| Score | Grade | Feedback |
|-------|-------|----------|
| 26-28 | A+ | Excellent! Deep understanding of model monitoring |
| 23-25 | A | Great job! Strong grasp of monitoring concepts |
| 21-22 | B | Good. Review missed topics |
| 18-20 | C | Passing. Revisit key monitoring concepts |
| < 18 | F | Please review lecture notes and retry |

---

## Answer Key Summary

1. B | 2. B | 3. B,C,E | 4. B | 5. B
6. B | 7. B | 8. A | 9. B | 10. C
11. B | 12. A,B,E | 13. B | 14. B | 15. B
16. B | 17. A,B,C,E | 18. B | 19. B | 20. D
21. B | 22. B,C,D | 23. B | 24. B | 25. B
26. B | 27. B | 28. B

---

## Next Steps

- Review any missed questions
- Complete hands-on exercises
- Set up monitoring for a real model
- Practice with Evidently AI
- Explore additional resources in `resources.md`

Good luck!
