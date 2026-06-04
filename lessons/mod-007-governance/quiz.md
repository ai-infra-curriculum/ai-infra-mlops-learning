# Module 07: ML Governance & Compliance - Quiz

## Instructions

- **Total Questions**: 30
- **Time Limit**: 45 minutes
- **Passing Score**: 75% (23/30 correct)
- **Question Types**: Multiple choice, multiple select, code analysis

---

## Section 1: Fairness Metrics & Assessment (Questions 1-6)

### Question 1
What is demographic parity in the context of fairness in ML?

A) Equal accuracy across all demographic groups
B) Equal positive prediction rate across all demographic groups
C) Equal false positive rate across all demographic groups
D) Equal sample size across all demographic groups

<details>
<summary>Answer</summary>

**B) Equal positive prediction rate across all demographic groups**

**Explanation**: Demographic parity (also called statistical parity) requires:
- The probability of positive prediction is equal across protected groups
- Formula: `P(Ŷ=1|A=a) = P(Ŷ=1|A=b)` for all groups a, b
- Example: In loan approval, 30% approval rate for all demographic groups

**Measurement**:
```python
# Demographic Parity Ratio
ratio = min(P(Ŷ=1|A=a), P(Ŷ=1|A=b)) / max(P(Ŷ=1|A=a), P(Ŷ=1|A=b))
# Typically require ratio ≥ 0.8 (80% rule)
```

**Limitations**:
- Doesn't consider actual qualifications or ground truth
- May conflict with accuracy if base rates differ
- Can be "gamed" by predicting positive equally for unqualified candidates

**Use case**: When equal opportunity/access is the goal, regardless of base rates.

</details>

---

### Question 2
What is the "80% rule" (four-fifths rule) in fairness assessment?

A) Models must be 80% accurate
B) The selection rate for any protected group should be at least 80% of the highest selection rate
C) Training data must be 80% balanced
D) 80% of predictions should be correct

<details>
<summary>Answer</summary>

**B) The selection rate for any protected group should be at least 80% of the highest selection rate**

**Explanation**: The 80% rule is a legal standard from employment law:

**Formula**:
```
Adverse Impact Ratio = (Selection Rate for Protected Group) / (Selection Rate for Highest Group)

Pass if: Adverse Impact Ratio ≥ 0.8
```

**Example**:
```
Loan approvals:
  Group A: 40% approval rate
  Group B: 30% approval rate

Adverse Impact Ratio = 30% / 40% = 0.75 < 0.8 → FAIL (potential discrimination)
```

**Origin**: EEOC Uniform Guidelines on Employee Selection Procedures (1978)

**Practical application**:
- Used in hiring, lending, and other high-stakes decisions
- Not a safe harbor (failing doesn't automatically mean discrimination)
- Passing doesn't guarantee legal compliance
- Should be one of multiple fairness checks

**In Python (Fairlearn)**:
```python
from fairlearn.metrics import demographic_parity_ratio
ratio = demographic_parity_ratio(y_true, y_pred, sensitive_features=gender)
# ratio ≥ 0.8 passes 80% rule
```

</details>

---

### Question 3
What is equalized odds in fairness?

A) Equal accuracy across groups
B) Equal true positive rate AND equal false positive rate across groups
C) Equal sample sizes across groups
D) Equal prediction rates across groups

<details>
<summary>Answer</summary>

**B) Equal true positive rate AND equal false positive rate across groups**

**Explanation**: Equalized odds requires:

**Both conditions must hold**:
1. Equal TPR: `P(Ŷ=1|Y=1,A=a) = P(Ŷ=1|Y=1,A=b)` (equal sensitivity)
2. Equal FPR: `P(Ŷ=1|Y=0,A=a) = P(Ŷ=1|Y=0,A=b)` (equal false alarm rate)

**Example - Criminal Risk Assessment**:
```
Group A: TPR=0.70, FPR=0.20
Group B: TPR=0.70, FPR=0.35  ← FAIL (FPR not equal)

Equalized odds requires:
  Group A: TPR=0.70, FPR=0.20
  Group B: TPR=0.70, FPR=0.20  ✓
```

**Why it matters**:
- Ensures model errors are distributed equally
- Important when false positives AND false negatives have serious consequences
- Example: In criminal justice, want equal error rates across races

**Measurement**:
```python
from fairlearn.metrics import equalized_odds_difference
diff = equalized_odds_difference(y_true, y_pred, sensitive_features=race)
# diff ≈ 0 indicates equalized odds
# Typically require diff < 0.1
```

**vs Demographic Parity**: Equalized odds considers ground truth labels; demographic parity doesn't.

</details>

---

### Question 4
**[Multiple Select]** Which of the following scenarios demonstrate potential fairness issues? (Select all that apply)

A) A hiring model has 90% accuracy for men and 89% accuracy for women
B) A loan model approves 40% of Group A and 25% of Group B (adverse impact ratio = 0.625)
C) A fraud detection model has FPR=0.05 for all demographic groups but TPR=0.80 for Group A and TPR=0.60 for Group B
D) A model trained on perfectly balanced demographic groups
E) A recidivism prediction model has equal accuracy but different false positive rates across races

<details>
<summary>Answer</summary>

**B, C, E**

**Explanation**:
- **A**: INCORRECT - 1% accuracy difference is minimal and likely acceptable
  - Small differences are expected due to sampling variation
  - No clear fairness violation

- **B**: CORRECT - Adverse impact ratio 0.625 < 0.8 (fails 80% rule)
  - 62.5% means Group B gets approved at only 62.5% the rate of Group A
  - Suggests potential discrimination
  - Requires investigation

- **C**: CORRECT - Violates equalized odds (equal opportunity)
  - TPR differs significantly: 0.80 vs 0.60
  - Group B has 25% lower chance of being correctly identified as fraud
  - Unfair burden on Group B

- **D**: INCORRECT - Balanced training data is good practice
  - Helps prevent bias from representation disparities
  - Not a fairness issue

- **E**: CORRECT - Different FPR violates equalized odds
  - Even with equal accuracy, error distribution matters
  - One group suffers more false accusations
  - Critical in criminal justice, lending, hiring

**Key insight**: Accuracy alone is insufficient - must examine error rates and selection rates across groups.

</details>

---

### Question 5
Analyze this fairness metrics output:

```python
MetricFrame:
                      overall  group_a  group_b
accuracy                 0.85     0.88     0.82
selection_rate           0.40     0.50     0.30
true_positive_rate       0.75     0.80     0.65
false_positive_rate      0.15     0.10     0.25
```

What fairness violations are present?

A) No violations - metrics are acceptable
B) Demographic parity violation only
C) Equalized odds violation only
D) Both demographic parity and equalized odds violations

<details>
<summary>Answer</summary>

**D) Both demographic parity and equalized odds violations**

**Explanation**: Let's analyze each fairness criterion:

**1. Demographic Parity**:
```
Selection rates: 50% (group_a) vs 30% (group_b)
Ratio = 30% / 50% = 0.6 < 0.8 → FAIL
```
Group B selected at only 60% the rate of Group A (violates 80% rule)

**2. Equalized Odds**:
```
TPR: 0.80 (group_a) vs 0.65 (group_b)
  → Difference = 0.15 (significant)

FPR: 0.10 (group_a) vs 0.25 (group_b)
  → Difference = 0.15 (significant)
```
Both TPR and FPR differ substantially → FAIL

**Summary of issues**:
- Group A: Higher selection (50% vs 30%)
- Group A: Higher TPR (80% vs 65%) - better at identifying true positives
- Group A: Lower FPR (10% vs 25%) - fewer false accusations
- Group B: Disadvantaged on all metrics

**Recommendations**:
1. Investigate root causes (biased features, imbalanced training data)
2. Apply bias mitigation (reweighting, threshold optimization)
3. Consider if base rates legitimately differ between groups
4. May need to retrain with fairness constraints

</details>

---

### Question 6
What is the fundamental trade-off between fairness and accuracy?

A) There is no trade-off
B) Imposing fairness constraints may reduce overall accuracy but improve fairness across groups
C) Fairness always improves accuracy
D) Accuracy always improves fairness

<details>
<summary>Answer</summary>

**B) Imposing fairness constraints may reduce overall accuracy but improve fairness across groups**

**Explanation**: The fairness-accuracy trade-off is a fundamental challenge:

**Why the trade-off exists**:
1. **Different base rates**: If groups have genuinely different outcome rates, achieving demographic parity requires sacrificing accuracy
2. **Optimal thresholds differ**: Different groups may need different decision thresholds for optimal accuracy
3. **Constrained optimization**: Adding fairness constraints restricts the model's optimization space

**Example - Loan Default Prediction**:
```
Unconstrained model:
  Overall accuracy: 85%
  Demographic parity ratio: 0.65 (FAIL)

Fairness-constrained model:
  Overall accuracy: 82% (↓3%)
  Demographic parity ratio: 0.85 (PASS)
```

**Quantifying the trade-off**:
```python
# Pareto frontier of fairness vs accuracy
for threshold_a, threshold_b in threshold_pairs:
    accuracy = compute_accuracy(y_true, y_pred)
    fairness = demographic_parity_ratio(y_true, y_pred, sensitive_features)
    # Plot shows accuracy↓ as fairness↑
```

**Practical considerations**:
- Trade-off is often small (1-3% accuracy loss)
- Fairness benefits may outweigh small accuracy loss
- Some fairness methods (pre-processing) minimize trade-off
- Legal/ethical requirements may mandate fairness despite accuracy loss

**Exception**: If original model had biased training data, fairness interventions can IMPROVE both fairness and true accuracy on unbiased test data.

</details>

---

## Section 2: Bias Mitigation Strategies (Questions 7-12)

### Question 7
What are the three stages where bias mitigation can be applied in ML pipelines?

A) Training, validation, testing
B) Pre-processing, in-processing, post-processing
C) Data collection, feature engineering, deployment
D) Development, staging, production

<details>
<summary>Answer</summary>

**B) Pre-processing, in-processing, post-processing**

**Explanation**: Bias mitigation taxonomy:

**1. Pre-processing** (before training):
- Modify training data to reduce bias
- Techniques: Reweighting, resampling, label correction
- Example: Increase weight of underrepresented group samples
- Advantage: Model-agnostic, works with any algorithm
- Disadvantage: May discard information

**2. In-processing** (during training):
- Add fairness constraints to model optimization
- Techniques: Fairness-aware loss functions, adversarial debiasing
- Example: Penalize demographic parity violations in loss function
- Advantage: Directly optimizes for fairness
- Disadvantage: Requires custom training, algorithm-specific

**3. Post-processing** (after training):
- Adjust predictions or thresholds to achieve fairness
- Techniques: Threshold optimization, calibration
- Example: Use different classification thresholds per group
- Advantage: Can be applied to any trained model
- Disadvantage: May seem like "masking" rather than fixing root cause

**Choosing an approach**:
- Pre-processing: When you can retrain and want model-agnostic solution
- In-processing: When you control training and want integrated fairness
- Post-processing: When working with existing/third-party models

**Fairlearn supports all three**:
```python
from fairlearn.preprocessing import CorrelationRemover  # Pre
from fairlearn.reductions import ExponentiatedGradient   # In
from fairlearn.postprocessing import ThresholdOptimizer  # Post
```

</details>

---

### Question 8
How does reweighting work as a bias mitigation technique?

A) Removing biased features
B) Assigning higher weights to underrepresented or disadvantaged samples during training
C) Adjusting model predictions after training
D) Retraining the model multiple times

<details>
<summary>Answer</summary>

**B) Assigning higher weights to underrepresented or disadvantaged samples during training**

**Explanation**: Reweighting balances the effective contribution of different groups:

**Intuition**: If Group B is underrepresented or has worse outcomes, increase the importance of correctly predicting Group B samples.

**Weight calculation**:
```python
def calculate_fairness_weights(y, sensitive_feature):
    """Calculate sample weights to achieve demographic parity."""
    weights = []
    for y_val in [0, 1]:
        for group in unique_groups:
            # Inverse of (group proportion × outcome proportion)
            p_group = (sensitive_feature == group).mean()
            p_outcome = (y == y_val).mean()
            weight = 1.0 / (p_group * p_outcome)
            weights[(sensitive_feature == group) & (y == y_val)] = weight
    return weights / weights.mean()  # Normalize
```

**Example**:
```
Original dataset:
  Group A: 800 samples (400 positive, 400 negative)
  Group B: 200 samples (50 positive, 150 negative)

Reweighted:
  Group A samples: weight = 1.0
  Group B positive: weight = 4.0 (upweight rare group+outcome)
  Group B negative: weight = 1.33

Effect: Model treats Group B samples as more important
```

**Implementation**:
```python
from sklearn.linear_model import LogisticRegression

weights = calculate_fairness_weights(y_train, sensitive_features)
model = LogisticRegression()
model.fit(X_train, y_train, sample_weight=weights)
```

**Advantages**:
- Simple, model-agnostic
- Works with any sklearn-compatible algorithm
- Preserves all data (no removal)

**Disadvantages**:
- May increase variance (overweighting small groups)
- Doesn't guarantee specific fairness criteria
- Can interact poorly with class imbalance

</details>

---

### Question 9
What is the Exponentiated Gradient (EG) algorithm in Fairlearn?

A) A gradient descent variant for faster training
B) An in-processing algorithm that reduces a fairness-aware model to a sequence of cost-sensitive classification problems
C) A post-processing threshold adjustment method
D) A data augmentation technique

<details>
<summary>Answer</summary>

**B) An in-processing algorithm that reduces a fairness-aware model to a sequence of cost-sensitive classification problems**

**Explanation**: Exponentiated Gradient is a powerful reduction-based approach:

**Key idea**: Convert constrained fairness problem to a series of standard ML problems:
1. Define fairness constraint (e.g., demographic parity)
2. Iteratively train models with different cost weights
3. Combine models to satisfy constraint

**Algorithm**:
```python
from fairlearn.reductions import ExponentiatedGradient, DemographicParity

# Define fairness constraint
constraint = DemographicParity()

# Define base estimator
estimator = LogisticRegression()

# Train fairness-aware model
mitigator = ExponentiatedGradient(
    estimator=estimator,
    constraints=constraint,
    eps=0.01  # Fairness tolerance
)
mitigator.fit(X_train, y_train, sensitive_features=sensitive_features)

# Predict (internally uses ensemble of models)
y_pred = mitigator.predict(X_test)
```

**How it works**:
1. Start with uniform cost weights for all groups
2. Train a model with current weights
3. Evaluate fairness constraint violations
4. Update weights exponentially based on violations (hence "Exponentiated")
5. Repeat until fairness constraint satisfied

**Supported constraints**:
- `DemographicParity`: Equal positive rates
- `EqualizedOdds`: Equal TPR and FPR
- `TruePositiveRateParity`: Equal TPR only
- `FalsePositiveRateParity`: Equal FPR only
- `ErrorRateParity`: Equal error rates

**Advantages**:
- Theoretical guarantees on fairness
- Handles multiple fairness constraints
- Generally small accuracy loss

**Disadvantages**:
- Slower training (multiple models)
- More complex to interpret
- Requires fairness constraint specification upfront

</details>

---

### Question 10
**[Multiple Select]** Which techniques are effective for mitigating bias in ML models? (Select all that apply)

A) Removing all demographic features from the model
B) Reweighting training samples to balance group representation
C) Using different classification thresholds for different groups (post-processing)
D) Ignoring fairness metrics and focusing only on accuracy
E) Training with fairness-aware loss functions
F) Collecting more diverse training data

<details>
<summary>Answer</summary>

**B, C, E, F**

**Explanation**:
- **A**: INCORRECT - "Fairness through unawareness" doesn't work
  - Proxy features (ZIP code → race) still encode protected attributes
  - Model can learn bias from correlated features
  - May violate equal opportunity laws that allow using protected attributes for fairness
  - **Exception**: In some jurisdictions, using protected attributes is illegal; but removing alone is insufficient

- **B**: CORRECT - Reweighting is effective pre-processing
  - Balances influence of different groups
  - Reduces impact of representation bias
  - Model-agnostic

- **C**: CORRECT - Threshold optimization is effective post-processing
  - Adjust decision boundary per group
  - Can achieve equalized odds or demographic parity
  - Example: Group A threshold=0.5, Group B threshold=0.3

- **D**: INCORRECT - Ignoring fairness causes harm
  - Legal/ethical issues
  - Perpetuates discrimination
  - Business risk (reputation, lawsuits)

- **E**: CORRECT - In-processing with fairness-aware objectives
  - Add fairness penalty to loss function
  - Example: `Loss = Accuracy_Loss + λ × Fairness_Penalty`
  - Directly optimizes fairness-accuracy trade-off

- **F**: CORRECT - Data collection is foundational
  - More diverse data reduces representation bias
  - Captures broader range of scenarios
  - Improves generalization and fairness
  - Prevention better than cure

**Best practice**: Combine multiple techniques (diverse data + in-processing + post-processing validation).

</details>

---

### Question 11
Analyze this bias mitigation code:

```python
from fairlearn.postprocessing import ThresholdOptimizer
from fairlearn.metrics import equalized_odds_difference

# Train base model
base_model = LogisticRegression()
base_model.fit(X_train, y_train)

# Post-process for fairness
mitigator = ThresholdOptimizer(
    estimator=base_model,
    constraints='equalized_odds',
    predict_method='predict_proba'
)
mitigator.fit(X_train, y_train, sensitive_features=gender)

# Evaluate
y_pred = mitigator.predict(X_test, sensitive_features=gender_test)
fairness_diff = equalized_odds_difference(y_test, y_pred, sensitive_features=gender_test)
```

What does this code do?

A) Trains a new model with fairness constraints
B) Adjusts decision thresholds per group to achieve equalized odds on the training data
C) Removes gender from features
D) Reweights training samples

<details>
<summary>Answer</summary>

**B) Adjusts decision thresholds per group to achieve equalized odds on the training data**

**Explanation**: This is post-processing threshold optimization:

**Step-by-step**:

1. **Train base model** (standard, no fairness):
```python
base_model.fit(X_train, y_train)
# Learns probability estimates P(Y=1|X)
```

2. **Post-process with ThresholdOptimizer**:
```python
mitigator = ThresholdOptimizer(
    estimator=base_model,          # Use base model's probabilities
    constraints='equalized_odds',   # Fairness goal
    predict_method='predict_proba'  # Needs probabilities, not binary
)
mitigator.fit(X_train, y_train, sensitive_features=gender)
```

**What fit() does**:
- Evaluates base model on training data
- For each group (male/female), finds optimal threshold that achieves:
  - Equal TPR across groups
  - Equal FPR across groups
- Stores group-specific thresholds: `{male: 0.45, female: 0.38}`

3. **Predict with group-specific thresholds**:
```python
y_pred = mitigator.predict(X_test, sensitive_features=gender_test)
# For males: predict 1 if P(Y=1) > 0.45
# For females: predict 1 if P(Y=1) > 0.38
```

**Advantages**:
- Works with any pre-trained model
- No retraining required
- Directly optimizes fairness constraint

**Disadvantages**:
- Requires sensitive features at prediction time
- May appear as "different treatment" (can be controversial)
- Can reduce accuracy

**When to use**: When you have an existing model and need to quickly impose fairness without retraining.

</details>

---

### Question 12
What is the purpose of disparate impact analysis?

A) To measure model accuracy
B) To identify if a model has significantly different outcomes for different demographic groups
C) To optimize hyperparameters
D) To detect data drift

<details>
<summary>Answer</summary>

**B) To identify if a model has significantly different outcomes for different demographic groups**

**Explanation**: Disparate impact is a legal concept for detecting discrimination:

**Definition**: When a facially neutral policy or model disproportionately affects a protected group.

**Legal context**:
- From employment law (Griggs v. Duke Power Co., 1971)
- Applied to lending (ECOA), hiring (Title VII), housing (Fair Housing Act)
- Even unintentional discrimination is illegal if disparate impact exists

**Measurement**:
```python
def disparate_impact_ratio(y_pred, sensitive_features):
    """Calculate disparate impact ratio."""
    groups = np.unique(sensitive_features)
    selection_rates = []

    for group in groups:
        group_mask = (sensitive_features == group)
        selection_rate = y_pred[group_mask].mean()
        selection_rates.append(selection_rate)

    # Ratio of lowest to highest selection rate
    return min(selection_rates) / max(selection_rates)

# Interpretation
ratio = disparate_impact_ratio(y_pred, race)
if ratio < 0.8:
    print("Potential disparate impact (fails 80% rule)")
```

**Example - Credit Card Approval**:
```
Approval rates:
  White applicants: 60%
  Black applicants: 45%

Disparate Impact Ratio = 45% / 60% = 0.75 < 0.8
→ Potential disparate impact
→ Company must justify business necessity
→ Or modify model to reduce impact
```

**Defenses**:
1. **Business necessity**: Practice is essential for business operations
2. **Job-related**: For employment, requirements related to job performance
3. **Less discriminatory alternative**: No alternative practice with less impact

**In ML**:
- Regularly audit models for disparate impact
- Document disparate impact analysis
- Implement mitigation if violations found
- Track over time (drift can cause new violations)

**Tools**:
```python
from fairlearn.metrics import MetricFrame, selection_rate

metric_frame = MetricFrame(
    metrics=selection_rate,
    y_true=y_true,
    y_pred=y_pred,
    sensitive_features=protected_attribute
)
print(metric_frame.by_group)  # Selection rates per group
print(metric_frame.difference())  # Max - min
print(metric_frame.ratio())  # Min / max (disparate impact ratio)
```

</details>

---

## Section 3: Model Cards & Documentation (Questions 13-18)

### Question 13
What is a Model Card in ML?

A) A playing card used for model selection
B) A structured document that provides transparency about a model's purpose, performance, limitations, and fairness characteristics
C) A credit card for paying for ML services
D) A business card for ML engineers

<details>
<summary>Answer</summary>

**B) A structured document that provides transparency about a model's purpose, performance, limitations, and fairness characteristics**

**Explanation**: Model Cards (introduced by Google in 2019) are standardized documentation:

**Purpose**: Increase transparency and accountability in ML systems

**Key sections**:

1. **Model Details**:
   - Developer, version, type (e.g., Logistic Regression, BERT)
   - Training date, framework, license
   - Paper/reference

2. **Intended Use**:
   - Primary intended uses
   - Primary intended users
   - Out-of-scope uses

3. **Factors**:
   - Relevant factors (demographics, domains)
   - Evaluation factors (what groups were tested)

4. **Metrics**:
   - Performance metrics (accuracy, F1, AUC)
   - Decision thresholds
   - Confidence intervals

5. **Evaluation Data**:
   - Datasets used
   - Preprocessing
   - Distribution statistics

6. **Training Data**:
   - Datasets used (if public)
   - Preprocessing details

7. **Quantitative Analysis**:
   - Performance by subgroup
   - Fairness metrics
   - Intersectional analysis

8. **Ethical Considerations**:
   - Known biases
   - Potential harms
   - Mitigation strategies

9. **Caveats and Recommendations**:
   - Known limitations
   - Recommended use cases
   - Not recommended uses

**Example excerpt**:
```markdown
## Model Card: Credit Scoring Model v2.3

### Model Details
- Developed by: Financial ML Team
- Model type: XGBoost Classifier
- Version: 2.3
- Date: 2024-10-15

### Intended Use
- **Primary use**: Credit risk assessment for consumer loans
- **Primary users**: Credit analysts, automated lending systems
- **Out-of-scope**: Not for employment screening, not for loans > $100k

### Performance
- Overall AUC: 0.85 (95% CI: 0.84-0.86)
- Demographic Parity Ratio: 0.83 (male vs female)
- Equalized Odds Difference: 0.07
```

**Benefits**:
- Helps users understand model capabilities and limitations
- Facilitates informed decision-making
- Supports responsible AI practices
- Enables accountability
- Required for some regulations (EU AI Act)

</details>

---

### Question 14
**[Multiple Select]** What information should be included in a model card? (Select all that apply)

A) Model performance metrics overall and by demographic subgroups
B) Intended use cases and out-of-scope applications
C) Developer personal contact information
D) Known limitations and biases
E) Secret proprietary algorithms
F) Training data characteristics and preprocessing steps

<details>
<summary>Answer</summary>

**A, B, D, F**

**Explanation**:
- **A**: CORRECT - Quantitative analysis section
  - Overall metrics: accuracy, precision, recall, AUC
  - Disaggregated metrics by:
    - Demographic groups (gender, race, age)
    - Geographic regions
    - Time periods
  - Fairness metrics: demographic parity, equalized odds
  - Example:
    ```
    Performance:
      Overall accuracy: 87%
      Male accuracy: 88%
      Female accuracy: 85%
      Demographic parity ratio: 0.82
    ```

- **B**: CORRECT - Intended use section
  - **Intended uses**: What the model is designed for
  - **Primary users**: Who should use it
  - **Out-of-scope**: What it should NOT be used for
  - Example:
    ```
    Intended: Resume screening for initial filtering
    Out-of-scope: Final hiring decisions without human review
    ```

- **C**: INCORRECT - Personal contact info inappropriate
  - Include organization, team name
  - Professional contact (team email, not personal)
  - Avoid individual personal information

- **D**: CORRECT - Caveats and ethical considerations
  - Known biases and sources
  - Potential harms
  - Failure modes
  - Mitigation strategies attempted
  - Example:
    ```
    Known limitations:
    - Underperforms on Spanish-language text (15% accuracy drop)
    - Training data from 2020-2022 may not reflect current trends
    - Higher false positive rate for age < 25 demographic
    ```

- **E**: INCORRECT - Don't expose trade secrets
  - Can describe general approach without revealing proprietary details
  - Balance transparency with IP protection
  - Example: "Ensemble of gradient-boosted trees" (OK) vs. exact feature engineering code (not required)

- **F**: CORRECT - Data section
  - Training data sources, size, date range
  - Preprocessing steps
  - Data distribution (class balance, demographic distribution)
  - Exclusions or filtering applied
  - Example:
    ```
    Training Data:
    - Source: Internal customer database 2020-2023
    - Size: 500K samples
    - Preprocessing: Removed duplicates, imputed missing values with median
    - Class distribution: 30% positive, 70% negative
    - Gender distribution: 55% male, 45% female
    ```

</details>

---

### Question 15
Why is documenting out-of-scope use cases important in model cards?

A) To make the documentation longer
B) To prevent misuse and set clear expectations about inappropriate applications
C) To show off knowledge
D) It's not important

<details>
<summary>Answer</summary>

**B) To prevent misuse and set clear expectations about inappropriate applications**

**Explanation**: Out-of-scope documentation protects both users and developers:

**Why it matters**:

1. **Prevents harmful misuse**:
   - Models may perform poorly or unfairly outside intended use
   - Example: Resume screening model trained for tech jobs used for medical positions
   - Prevents deployment in high-stakes scenarios without proper validation

2. **Manages expectations**:
   - Users understand limitations upfront
   - Reduces disappointment and inappropriate trust
   - Example: "Not suitable for real-time fraud detection (<100ms latency required)"

3. **Legal protection**:
   - Documents developer's intended use
   - Can be used as defense if model is misused
   - Demonstrates responsible AI practices

4. **Ethical responsibility**:
   - Models can cause harm if misapplied
   - Developers have duty to communicate appropriate use
   - Example: Face recognition model not intended for law enforcement without human review

**Examples of out-of-scope uses**:

```markdown
## Out-of-Scope Uses

### NOT intended for:
1. **Final decision-making without human review**
   - Model should augment, not replace, human judgment
   - Human must review all positive predictions

2. **Populations not represented in training data**
   - Training data: US customers age 25-65
   - Not validated for: Age < 25, age > 65, non-US customers

3. **High-stakes individual decisions**
   - Intended: Aggregate portfolio risk assessment
   - Not intended: Individual loan rejections without appeal process

4. **Real-time critical systems**
   - Average latency: 500ms
   - Not suitable for: Autonomous driving, medical emergency response

5. **Adversarial environments**
   - No adversarial training applied
   - Not robust to deliberate attacks or gaming
```

**Impact**:
- Clarifies responsibility
- Guides proper deployment
- Enables informed consent
- Reduces harm from misuse

</details>

---

### Question 16
How can model card generation be automated?

A) It cannot be automated
B) By extracting metrics, metadata, and statistics from training runs and model registries
C) By copying from other models
D) By using random text generation

<details>
<summary>Answer</summary>

**B) By extracting metrics, metadata, and statistics from training runs and model registries**

**Explanation**: Automated model card generation reduces manual effort and improves consistency:

**Automation approach**:

1. **Extract from experiment tracking** (MLflow, W&B):
```python
import mlflow

def generate_model_card_from_mlflow(run_id):
    """Generate model card from MLflow run."""
    run = mlflow.get_run(run_id)

    model_card = {
        'model_details': {
            'version': run.data.params['version'],
            'model_type': run.data.params['model_type'],
            'training_date': run.info.start_time,
            'framework': run.data.tags.get('framework', 'unknown')
        },
        'metrics': {
            'accuracy': run.data.metrics['accuracy'],
            'auc': run.data.metrics['auc'],
            'f1_score': run.data.metrics['f1']
        },
        'hyperparameters': run.data.params
    }
    return model_card
```

2. **Extract from model registry**:
```python
from mlflow.tracking import MlflowClient

client = MlflowClient()
model_version = client.get_model_version('CreditScoring', version='3')

metadata = {
    'name': model_version.name,
    'version': model_version.version,
    'stage': model_version.current_stage,
    'description': model_version.description
}
```

3. **Compute fairness metrics automatically**:
```python
from fairlearn.metrics import MetricFrame, demographic_parity_ratio

def compute_fairness_metrics(model, X_test, y_test, sensitive_features):
    """Compute fairness metrics for model card."""
    y_pred = model.predict(X_test)

    metric_frame = MetricFrame(
        metrics={
            'accuracy': accuracy_score,
            'precision': precision_score,
            'recall': recall_score
        },
        y_true=y_test,
        y_pred=y_pred,
        sensitive_features=sensitive_features
    )

    return {
        'overall': metric_frame.overall,
        'by_group': metric_frame.by_group.to_dict(),
        'demographic_parity_ratio': demographic_parity_ratio(
            y_test, y_pred, sensitive_features=sensitive_features
        )
    }
```

4. **Generate markdown template**:
```python
def generate_model_card_markdown(model_info, metrics, fairness_metrics):
    """Generate model card in markdown format."""
    template = f"""
# Model Card: {model_info['name']} v{model_info['version']}

## Model Details
- **Developed by**: {model_info['team']}
- **Model type**: {model_info['model_type']}
- **Version**: {model_info['version']}
- **Date**: {model_info['date']}

## Performance
- **Overall Accuracy**: {metrics['accuracy']:.3f}
- **AUC**: {metrics['auc']:.3f}
- **F1 Score**: {metrics['f1']:.3f}

## Fairness Metrics
- **Demographic Parity Ratio**: {fairness_metrics['demographic_parity_ratio']:.3f}

### Performance by Group
{format_table(fairness_metrics['by_group'])}
"""
    return template
```

5. **Full automation pipeline**:
```python
class ModelCardGenerator:
    def __init__(self, template_path='model_card_template.md'):
        self.template = self._load_template(template_path)

    def generate(self, model, X_test, y_test, sensitive_features, metadata):
        """Generate complete model card."""
        # Compute all metrics
        performance = self._compute_performance(model, X_test, y_test)
        fairness = self._compute_fairness(model, X_test, y_test, sensitive_features)
        feature_importance = self._compute_feature_importance(model)

        # Populate template
        card = self.template.format(
            **metadata,
            **performance,
            **fairness,
            feature_importance=feature_importance
        )

        return card

    def save(self, card, output_path='model_card.md'):
        """Save model card to file."""
        with open(output_path, 'w') as f:
            f.write(card)
```

**Tools**:
- **Model Card Toolkit** (Google): https://github.com/tensorflow/model-card-toolkit
- **Custom scripts** integrated with MLflow/W&B
- **CI/CD integration**: Generate on every model training run

**Benefits**:
- Consistent documentation across models
- Reduced manual effort
- Always up-to-date metrics
- Version-controlled with model
- Can be part of CI/CD pipeline

</details>

---

### Question 17
Analyze this model card excerpt:

```markdown
## Intended Use
**Primary use**: Automated resume screening for software engineering positions

## Performance
- Overall Accuracy: 92%

## Training Data
- Internal database of past hires (2015-2020)
```

What critical information is missing?

A) Model type
B) Disaggregated performance metrics by demographic groups
C) Developer name
D) Nothing - this is complete

<details>
<summary>Answer</summary>

**B) Disaggregated performance metrics by demographic groups**

**Explanation**: This model card has several critical gaps:

**Missing critical information**:

1. **Disaggregated metrics** (MOST CRITICAL):
```markdown
❌ Missing:
## Performance by Demographics
- Male candidates: 94% accuracy
- Female candidates: 87% accuracy
- Age <30: 91% accuracy
- Age 30-50: 93% accuracy
- Age >50: 88% accuracy

## Fairness Metrics
- Demographic Parity Ratio (gender): 0.78 (FAILS 80% rule)
- Selection Rate: Male 45%, Female 35%
```

2. **Out-of-scope uses** (CRITICAL for safety):
```markdown
❌ Missing:
## Out-of-Scope Uses
- NOT for final hiring decisions without human review
- NOT for non-software engineering positions
- NOT for candidates outside training distribution (e.g., recent graduates with different skill profiles)
```

3. **Known limitations and biases**:
```markdown
❌ Missing:
## Limitations
- Training data reflects historical hiring patterns, which may encode past biases
- Underrepresents women (15% of training data)
- Performance degrades for candidates with non-traditional backgrounds
```

4. **Ethical considerations**:
```markdown
❌ Missing:
## Ethical Considerations
- Risk of perpetuating historical gender imbalance in tech
- May disadvantage career-changers and bootcamp graduates
- Requires human oversight to prevent discriminatory outcomes
```

5. **Model details**:
```markdown
❌ Missing:
- Model type: XGBoost classifier
- Version: 2.1
- Training date: 2024-10-15
- Framework: scikit-learn 1.3
```

**Why disaggregated metrics are MOST important**:
- Overall accuracy (92%) masks disparities
- Different groups may experience very different accuracy
- Essential for fairness assessment
- Legal requirement in some contexts
- Enables informed consent from users

**Red flags in this excerpt**:
1. Training data from 2015-2020 is outdated (4+ years old)
2. "Past hires" introduces survivorship bias (only includes hired candidates, not all qualified candidates)
3. No mention of fairness validation
4. Resume screening is high-stakes (affects livelihoods)

**What this model card should trigger**:
- ⚠️ Fairness audit before deployment
- ⚠️ Diverse evaluation dataset
- ⚠️ Human-in-the-loop requirement
- ⚠️ Regular monitoring for bias

</details>

---

### Question 18
What is the relationship between model cards and regulatory compliance (e.g., EU AI Act)?

A) Model cards are unrelated to regulation
B) Model cards help satisfy transparency and documentation requirements in AI regulations
C) Model cards replace all regulatory requirements
D) Model cards are only for marketing

<details>
<summary>Answer</summary>

**B) Model cards help satisfy transparency and documentation requirements in AI regulations**

**Explanation**: Model cards increasingly align with regulatory requirements:

**EU AI Act requirements** (for high-risk AI systems):

1. **Technical documentation** (Article 11):
   - Design and development process
   - Performance metrics
   - Validation and testing
   - **Model cards satisfy**: Structured performance documentation

2. **Transparency obligations** (Article 13):
   - Inform users about AI system capabilities and limitations
   - Provide instructions for use
   - **Model cards satisfy**: Intended use, limitations, performance characteristics

3. **Accuracy, robustness, cybersecurity** (Article 15):
   - Appropriate levels of accuracy
   - Robustness in case of errors
   - **Model cards satisfy**: Documented metrics, confidence intervals, failure modes

4. **Human oversight** (Article 14):
   - Understand AI system capabilities
   - Be aware of tendency of automation bias
   - **Model cards satisfy**: Clear communication of limitations, out-of-scope uses

**Other regulations**:

**GDPR** (Right to explanation):
- Article 22: Right to explanation for automated decisions
- Model cards provide basis for explaining how decisions are made
- Not sufficient alone, but foundational documentation

**Fair Housing Act, ECOA** (US):
- Requires fair lending practices
- Model cards document fairness metrics, disparate impact analysis
- Support adverse action explanations

**Algorithmic Accountability Act** (proposed, US):
- Requires impact assessments for automated systems
- Model cards provide structured framework for assessments

**Mapping model cards to EU AI Act**:

```markdown
## Model Card Section → EU AI Act Requirement

Model Details → Technical Documentation (Art. 11)
Intended Use → Transparency Obligations (Art. 13)
Out-of-Scope → Instructions for Use (Art. 13)
Performance Metrics → Accuracy Requirements (Art. 15)
Fairness Metrics → Non-discrimination (Art. 10)
Known Limitations → Risk Management (Art. 9)
Evaluation Data → Validation Requirements (Art. 15)
```

**Benefits for compliance**:
- ✓ Demonstrates due diligence
- ✓ Provides audit trail
- ✓ Facilitates regulatory review
- ✓ Supports impact assessments
- ✓ Enables informed user consent

**Best practices**:
1. Generate model cards for all production models
2. Version control with model versions
3. Update when model is retrained or data changes
4. Include in model registry
5. Review with legal/compliance team
6. Make accessible to users and regulators

**Limitations**:
- Model cards alone don't guarantee compliance
- Need additional processes: impact assessments, monitoring, human oversight
- Should be part of broader responsible AI program

</details>

---

## Section 4: Audit Logging & Compliance Tracking (Questions 19-24)

### Question 19
What is the purpose of tamper-proof audit logs in ML systems?

A) To make logs unreadable
B) To provide an immutable record of model predictions and decisions that cannot be altered retroactively
C) To encrypt all data
D) To compress logs

<details>
<summary>Answer</summary>

**B) To provide an immutable record of model predictions and decisions that cannot be altered retroactively**

**Explanation**: Tamper-proof logs are critical for accountability and compliance:

**Why immutability matters**:

1. **Legal evidence**: Audit logs may be required in litigation
   - Example: Lending discrimination lawsuit needs proof of decisions made
   - Altered logs are inadmissible
   - Tamper-proof logs have legal standing

2. **Regulatory compliance**:
   - GDPR: Right to explanation requires records of automated decisions
   - Financial regulations: MiFID II, SOX require audit trails
   - Healthcare: HIPAA requires access logs for patient data

3. **Accountability**:
   - Prove what decisions were made and when
   - Trace decisions to specific model versions
   - Investigate incidents and complaints

4. **Forensics**:
   - Detect unauthorized changes to predictions
   - Identify system compromises
   - Root cause analysis for failures

**Implementation techniques**:

**1. Cryptographic hashing** (Merkle trees):
```python
import hashlib
import json
from datetime import datetime

class TamperProofLogger:
    def __init__(self):
        self.logs = []
        self.previous_hash = '0' * 64  # Genesis hash

    def log_prediction(self, user_id, features, prediction, model_version):
        """Log a prediction with tamper-proof hash."""
        timestamp = datetime.utcnow().isoformat()

        log_entry = {
            'timestamp': timestamp,
            'user_id': user_id,
            'features': features,
            'prediction': prediction,
            'model_version': model_version,
            'previous_hash': self.previous_hash
        }

        # Compute hash of this entry
        entry_string = json.dumps(log_entry, sort_keys=True)
        current_hash = hashlib.sha256(entry_string.encode()).hexdigest()

        log_entry['hash'] = current_hash
        self.logs.append(log_entry)
        self.previous_hash = current_hash

        return log_entry

    def verify_integrity(self):
        """Verify no logs have been tampered with."""
        previous_hash = '0' * 64

        for entry in self.logs:
            # Recompute hash
            entry_copy = entry.copy()
            stored_hash = entry_copy.pop('hash')

            entry_string = json.dumps(entry_copy, sort_keys=True)
            computed_hash = hashlib.sha256(entry_string.encode()).hexdigest()

            if computed_hash != stored_hash:
                return False, f"Tampering detected at {entry['timestamp']}"

            if entry['previous_hash'] != previous_hash:
                return False, f"Chain broken at {entry['timestamp']}"

            previous_hash = stored_hash

        return True, "Logs intact"
```

**2. Write-once storage**:
- Append-only databases
- Immutable S3 buckets (Object Lock)
- Blockchain for critical decisions

**3. Digital signatures**:
```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

def sign_log_entry(entry, private_key):
    """Digitally sign a log entry."""
    entry_bytes = json.dumps(entry, sort_keys=True).encode()

    signature = private_key.sign(
        entry_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature
```

**What to log**:
- ✓ Timestamp (UTC)
- ✓ User/entity identifier
- ✓ Input features
- ✓ Prediction/decision
- ✓ Model version
- ✓ Confidence score
- ✓ Sensitive features (if used)
- ✓ Decision rationale (feature importance)

**Benefits**:
- Legal defensibility
- Regulatory compliance
- Incident investigation
- Trust and transparency
- Deterrent against manipulation

</details>

---

### Question 20
How does a Merkle tree enhance audit log integrity?

A) By compressing logs
B) By creating a hierarchical hash structure where any tampering changes the root hash, making alterations detectable
C) By encrypting logs
D) By sorting logs alphabetically

<details>
<summary>Answer</summary>

**B) By creating a hierarchical hash structure where any tampering changes the root hash, making alterations detectable**

**Explanation**: Merkle trees (hash trees) provide efficient tamper detection:

**Structure**:
```
                Root Hash
                /        \
            H(AB)        H(CD)
            /    \      /    \
          H(A)  H(B)  H(C)  H(D)
           |     |     |     |
         Log A  Log B Log C Log D
```

**How it works**:

1. **Build tree**:
   - Hash each log entry → leaf nodes
   - Hash pairs of hashes → parent nodes
   - Continue until single root hash

2. **Verify integrity**:
   - Store root hash securely (sign it, store externally)
   - To verify: recompute tree, compare root hash
   - Any change to any log changes root hash

**Implementation**:
```python
import hashlib

class MerkleTree:
    def __init__(self, log_entries):
        """Build Merkle tree from log entries."""
        self.leaves = [self._hash(entry) for entry in log_entries]
        self.root = self._build_tree(self.leaves)

    def _hash(self, data):
        """SHA-256 hash of data."""
        if isinstance(data, str):
            data = data.encode()
        elif isinstance(data, dict):
            data = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(data).hexdigest()

    def _build_tree(self, nodes):
        """Recursively build tree from leaves to root."""
        if len(nodes) == 1:
            return nodes[0]  # Root hash

        # Pair up nodes and hash
        next_level = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i + 1] if i + 1 < len(nodes) else left  # Duplicate last if odd

            parent = self._hash(left + right)
            next_level.append(parent)

        return self._build_tree(next_level)

    def verify(self, expected_root):
        """Verify tree integrity against expected root hash."""
        return self.root == expected_root

    def get_proof(self, index):
        """Get proof path for verifying a specific log entry."""
        # Returns sibling hashes needed to recompute root
        # Enables efficient verification without full tree
        # Used in blockchain, distributed systems
        pass  # Implementation omitted for brevity
```

**Usage**:
```python
# Create logs
logs = [
    {'timestamp': '2024-10-25T10:00:00', 'user': 'user1', 'prediction': 0},
    {'timestamp': '2024-10-25T10:01:00', 'user': 'user2', 'prediction': 1},
    {'timestamp': '2024-10-25T10:02:00', 'user': 'user3', 'prediction': 1},
    {'timestamp': '2024-10-25T10:03:00', 'user': 'user4', 'prediction': 0}
]

# Build Merkle tree
tree = MerkleTree(logs)
root_hash = tree.root

# Store root hash securely (sign it, store in blockchain, write to immutable storage)
store_securely(root_hash)

# Later, verify integrity
tree_verify = MerkleTree(logs)
is_valid = tree_verify.verify(root_hash)

if not is_valid:
    print("TAMPERING DETECTED: Logs have been altered!")
else:
    print("Logs are intact and trustworthy")
```

**Advantages**:

1. **Efficient verification**:
   - Don't need to recompute all hashes
   - Proof size: O(log n) instead of O(n)

2. **Pinpoint tampering**:
   - Can identify which log was altered
   - Useful for large audit trails

3. **Distributed verification**:
   - Multiple parties can verify same root
   - Used in blockchain (Bitcoin, Ethereum)

4. **Incremental updates**:
   - Add new logs without recomputing everything
   - Only recompute path to root

**Real-world use**:
- **Git**: Commits form Merkle tree (each commit hash depends on parent)
- **Blockchain**: Transactions form Merkle tree in each block
- **Certificate Transparency**: HTTPS certificate logs
- **Audit systems**: Tamper-proof logging

**ML-specific application**:
```python
class MLAuditLog:
    def __init__(self):
        self.logs = []
        self.tree = None

    def log_prediction(self, user_id, features, prediction, model_version):
        """Log prediction and update Merkle tree."""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'features': features,
            'prediction': prediction,
            'model_version': model_version
        }

        self.logs.append(entry)
        self.tree = MerkleTree(self.logs)

        # Publish root hash (blockchain, external notary, etc.)
        self._publish_root_hash(self.tree.root)

    def verify_integrity(self):
        """Verify all logs are intact."""
        current_tree = MerkleTree(self.logs)
        published_root = self._get_published_root_hash()

        return current_tree.verify(published_root)
```

</details>

---

### Question 21
**[Multiple Select]** What information should be captured in ML audit logs for compliance? (Select all that apply)

A) Timestamp of prediction
B) Input features used
C) Model version that made the prediction
D) Developer's password
E) Prediction output and confidence score
F) Unique identifier for the subject of the prediction

<details>
<summary>Answer</summary>

**A, B, C, E, F**

**Explanation**:
- **A**: CORRECT - Timestamp (UTC) is essential
  - When was decision made?
  - Enables temporal analysis
  - Required for regulatory audits
  - Example: `2024-10-25T14:32:15.123Z`

- **B**: CORRECT - Input features
  - What information was used?
  - Enables decision reproduction
  - Supports right to explanation (GDPR)
  - May need to anonymize/pseudonymize sensitive features
  - Example:
    ```json
    {
      "age": 35,
      "income": 75000,
      "credit_score": 720,
      "employment_duration_months": 48
    }
    ```

- **C**: CORRECT - Model version
  - Which model made this decision?
  - Critical for tracing decisions to specific models
  - Enables rollback identification
  - Supports model governance
  - Example: `credit-scoring-model:v2.3.1`

- **D**: INCORRECT - NEVER log passwords or credentials
  - Security violation
  - GDPR violation
  - No legitimate audit purpose
  - Log authentication events (success/failure), not credentials

- **E**: CORRECT - Prediction and confidence
  - What was decided?
  - How confident was the model?
  - Enables quality analysis
  - Supports appeals process
  - Example:
    ```json
    {
      "prediction": "approved",
      "prediction_proba": 0.87,
      "decision_threshold": 0.5
    }
    ```

- **F**: CORRECT - Subject identifier
  - Who was affected by this decision?
  - Enables individual lookups
  - Required for GDPR right to access
  - Should be pseudonymized when possible
  - Example: `user_id: "usr_8x3k9m2"`

**Complete audit log structure**:
```python
{
  # Required fields
  "log_id": "log_20241025_143215_abc123",
  "timestamp": "2024-10-25T14:32:15.123Z",
  "subject_id": "usr_8x3k9m2",  # User/customer identifier
  "model_version": "credit-scoring:v2.3.1",
  "prediction": "approved",
  "prediction_proba": 0.87,

  # Input features
  "features": {
    "age": 35,
    "income": 75000,
    "credit_score": 720,
    "employment_duration_months": 48,
    "existing_loans": 1
  },

  # Metadata
  "model_type": "XGBoostClassifier",
  "decision_threshold": 0.5,
  "sensitive_features": {
    "gender": "female",  # If used for fairness monitoring
    "race": "asian"      # May be required for disparate impact analysis
  },

  # Explainability
  "feature_importance": {
    "credit_score": 0.35,
    "income": 0.28,
    "employment_duration": 0.20,
    "age": 0.10,
    "existing_loans": 0.07
  },

  # Provenance
  "prediction_latency_ms": 45,
  "api_version": "v1",
  "request_id": "req_xyz789",

  # Integrity
  "previous_log_hash": "a1b2c3...",
  "log_hash": "d4e5f6..."
}
```

**Compliance mapping**:
- **GDPR Article 15** (Right to access): subject_id, timestamp, features, prediction
- **GDPR Article 22** (Automated decisions): model_version, feature_importance, decision logic
- **Fair Lending Laws**: sensitive_features (for disparate impact monitoring)
- **SOX, MiFID II**: Complete audit trail, tamper-proof hashing

**Storage considerations**:
- Retention period: Check regulations (often 3-7 years)
- Encryption at rest: PII/sensitive data
- Access controls: Only authorized personnel
- Backup: Ensure logs are backed up
- Anonymization: For analytics, create anonymized copies

</details>

---

### Question 22
What is the purpose of SHA-256 hashing in audit logs?

A) To compress logs
B) To generate a unique, deterministic fingerprint of log content that changes if content is altered
C) To encrypt sensitive data
D) To sort logs

<details>
<summary>Answer</summary>

**B) To generate a unique, deterministic fingerprint of log content that changes if content is altered**

**Explanation**: SHA-256 (Secure Hash Algorithm 256-bit) provides cryptographic integrity:

**Properties**:

1. **Deterministic**: Same input always produces same hash
   ```python
   hashlib.sha256(b"hello").hexdigest()
   # Always: 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
   ```

2. **One-way**: Cannot reverse hash to get original input
   - Can't recover log content from hash
   - Protects against rainbow table attacks

3. **Avalanche effect**: Tiny change → completely different hash
   ```python
   hashlib.sha256(b"hello").hexdigest()
   # 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824

   hashlib.sha256(b"Hello").hexdigest()  # Just capitalized 'h'
   # 185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969
   # Completely different!
   ```

4. **Collision resistant**: Virtually impossible to find two inputs with same hash
   - 2^256 possible outputs (more than atoms in universe)
   - No known collisions

5. **Fixed size**: Always 256 bits (64 hex characters)
   - Regardless of input size

**Usage in audit logs**:

```python
import hashlib
import json

def hash_log_entry(log_entry):
    """Generate SHA-256 hash of log entry."""
    # Convert to canonical JSON string (sorted keys for consistency)
    log_string = json.dumps(log_entry, sort_keys=True)

    # Compute hash
    hash_object = hashlib.sha256(log_string.encode('utf-8'))
    hash_hex = hash_object.hexdigest()

    return hash_hex

# Example
log_entry = {
    'timestamp': '2024-10-25T14:32:15Z',
    'user_id': 'usr_123',
    'prediction': 'approved',
    'model_version': 'v2.3'
}

log_hash = hash_log_entry(log_entry)
# e.g., '7d8f3e4a9b2c1d0e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3'
```

**Chaining logs**:
```python
class AuditLogger:
    def __init__(self):
        self.previous_hash = '0' * 64  # Genesis

    def add_log(self, log_entry):
        """Add log with hash chain."""
        # Include previous hash in this entry
        log_entry['previous_hash'] = self.previous_hash

        # Compute this entry's hash
        current_hash = hash_log_entry(log_entry)
        log_entry['hash'] = current_hash

        # Update for next entry
        self.previous_hash = current_hash

        return log_entry
```

**Tampering detection**:
```python
def verify_log_integrity(logs):
    """Verify no logs have been tampered with."""
    previous_hash = '0' * 64

    for i, log in enumerate(logs):
        # Check previous hash link
        if log['previous_hash'] != previous_hash:
            return False, f"Chain broken at log {i}"

        # Recompute hash
        log_copy = log.copy()
        stored_hash = log_copy.pop('hash')
        computed_hash = hash_log_entry(log_copy)

        # Compare
        if computed_hash != stored_hash:
            return False, f"Tampering detected at log {i}"

        previous_hash = stored_hash

    return True, "All logs verified"
```

**Example tampering detection**:
```python
logs = [
    {'timestamp': '10:00', 'user': 'A', 'prediction': 0, 'previous_hash': '0'*64, 'hash': 'abc...'},
    {'timestamp': '10:01', 'user': 'B', 'prediction': 1, 'previous_hash': 'abc...', 'hash': 'def...'},
    {'timestamp': '10:02', 'user': 'C', 'prediction': 1, 'previous_hash': 'def...', 'hash': 'ghi...'}
]

# Attacker changes log[1] prediction from 1 to 0
logs[1]['prediction'] = 0  # Tamper!

# Verification will fail
is_valid, message = verify_log_integrity(logs)
# Returns: (False, "Tampering detected at log 1")
# Because recomputed hash ≠ stored hash
```

**Not encryption**:
- SHA-256 does NOT encrypt (data is still readable)
- Use encryption (AES) for confidentiality
- Use hashing (SHA-256) for integrity

**Best practices**:
- Hash entire log entry (all fields)
- Include timestamp in hash (prevent replay)
- Use sorted JSON for determinism
- Chain hashes (current depends on previous)
- Store root hash externally (blockchain, notary)

</details>

---

### Question 23
Analyze this audit logging code:

```python
class AuditLogger:
    def __init__(self):
        self.logs = []

    def log_prediction(self, user_id, features, prediction):
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'features': features,
            'prediction': prediction
        }
        self.logs.append(entry)

    def modify_log(self, index, new_prediction):
        """Allow modifying past predictions."""
        self.logs[index]['prediction'] = new_prediction
```

What is the main problem with this implementation?

A) It's too slow
B) It allows tampering with audit logs through the modify_log method
C) It doesn't use JSON
D) It's missing timestamps

<details>
<summary>Answer</summary>

**B) It allows tampering with audit logs through the modify_log method**

**Explanation**: This implementation violates fundamental audit log principles:

**Critical flaws**:

1. **Mutable logs** (MOST CRITICAL):
```python
def modify_log(self, index, new_prediction):
    self.logs[index]['prediction'] = new_prediction
    # ❌ ALLOWS RETROACTIVE CHANGES
    # ❌ Destroys audit trail integrity
    # ❌ Legal evidence is compromised
```

**Why this is dangerous**:
- Hides mistakes or misconduct
- No record of original decision
- Violates regulatory requirements (SOX, GDPR, etc.)
- Inadmissible as legal evidence
- Enables covering up discrimination

2. **No integrity protection**:
   - No hashing
   - No tamper detection
   - No way to verify logs haven't been altered

3. **No immutability enforcement**:
   - Data structure (list) is mutable
   - No cryptographic protection

**Proper implementation**:

```python
import hashlib
import json
from datetime import datetime

class TamperProofAuditLogger:
    def __init__(self):
        self.logs = []
        self.previous_hash = '0' * 64

    def log_prediction(self, user_id, features, prediction, model_version):
        """Log prediction immutably."""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'features': features,
            'prediction': prediction,
            'model_version': model_version,
            'previous_hash': self.previous_hash
        }

        # Compute hash
        entry_string = json.dumps(entry, sort_keys=True)
        current_hash = hashlib.sha256(entry_string.encode()).hexdigest()
        entry['hash'] = current_hash

        # Append (don't allow modification)
        self.logs.append(entry)
        self.previous_hash = current_hash

        return entry

    def correct_prediction(self, original_log_id, new_prediction, reason):
        """
        Correct a prediction by adding a NEW correction log.
        ✓ Original log remains unchanged
        ✓ Correction is logged with reason
        ✓ Full audit trail preserved
        """
        correction_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': 'correction',
            'original_log_id': original_log_id,
            'corrected_prediction': new_prediction,
            'reason': reason,
            'corrected_by': get_current_user(),  # Track who made correction
            'previous_hash': self.previous_hash
        }

        # Hash and append
        entry_string = json.dumps(correction_entry, sort_keys=True)
        current_hash = hashlib.sha256(entry_string.encode()).hexdigest()
        correction_entry['hash'] = current_hash

        self.logs.append(correction_entry)
        self.previous_hash = current_hash

        return correction_entry

    def verify_integrity(self):
        """Verify no logs have been tampered with."""
        previous_hash = '0' * 64

        for entry in self.logs:
            # Recompute hash
            entry_copy = entry.copy()
            stored_hash = entry_copy.pop('hash')

            entry_string = json.dumps(entry_copy, sort_keys=True)
            computed_hash = hashlib.sha256(entry_string.encode()).hexdigest()

            # Verify hash matches
            if computed_hash != stored_hash:
                return False, f"Tampering detected at {entry['timestamp']}"

            # Verify chain
            if entry['previous_hash'] != previous_hash:
                return False, f"Chain broken at {entry['timestamp']}"

            previous_hash = stored_hash

        return True, "Logs intact"

    # ❌ NO modify_log() method - by design!
```

**Key differences**:

| Flawed Implementation | Proper Implementation |
|----------------------|----------------------|
| ❌ `modify_log()` allows changes | ✓ No modification methods |
| ❌ No hashing | ✓ SHA-256 hash chain |
| ❌ No tamper detection | ✓ `verify_integrity()` |
| ❌ Can alter history | ✓ Append-only, corrections logged separately |

**Correction pattern**:
```python
# Original log
log1 = logger.log_prediction('usr_123', {...}, 'approved', 'v2.3')

# Later, realize prediction was wrong
# ❌ Don't: logger.modify_log(0, 'denied')
# ✓ Do: Log correction
correction = logger.correct_prediction(
    original_log_id=log1['hash'],
    new_prediction='denied',
    reason='Manual review found error in credit score calculation'
)

# Now audit trail shows:
# 1. Original prediction: approved
# 2. Correction: denied (with reason and who made it)
# ✓ Complete transparency
```

**Additional protections**:
- Append-only storage (S3 Object Lock, blockchain)
- Cryptographic signatures
- External verification (publish hashes to blockchain)
- Access controls (only authorized users can log)

</details>

---

### Question 24
What is GDPR's "Right to Explanation" and how does it relate to ML audit logs?

A) Users have the right to understand why an automated decision was made about them
B) Users must explain their data to companies
C) Companies must explain their business model
D) Models must be interpretable

<details>
<summary>Answer</summary>

**A) Users have the right to understand why an automated decision was made about them**

**Explanation**: GDPR Article 22 provides rights regarding automated decision-making:

**GDPR Article 22**:
> The data subject shall have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her.

**Right to Explanation** (Recital 71):
- Right to obtain explanation of decision reached after assessment
- Right to contest the decision
- Right to express point of view

**What this means for ML systems**:

1. **When it applies**:
   - Decision is **solely automated** (no meaningful human review)
   - Decision has **legal or similarly significant effects**
   - Examples:
     - ✓ Loan rejection
     - ✓ Insurance pricing
     - ✓ Job application rejection
     - ✓ Credit score determination
     - ✗ Product recommendations (not significant)
     - ✗ Movie suggestions (not significant)

2. **What must be explained**:
   - Logic involved in the decision
   - Significance and consequences
   - How data was used

**How audit logs support right to explanation**:

```python
class ExplainableAuditLogger:
    def log_prediction(self, user_id, features, prediction, model_version, explainability):
        """Log prediction with explainability data."""
        entry = {
            # Standard fields
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'prediction': prediction,
            'model_version': model_version,

            # For right to explanation
            'features_used': features,
            'feature_importance': explainability['feature_importance'],
            'decision_rule': explainability['decision_rule'],
            'similar_cases': explainability['similar_cases'],

            # For contestation
            'human_review_available': True,
            'appeal_process': 'email support@company.com',
        }

        # Log with tamper-proof hash
        return self._log_immutably(entry)

    def generate_explanation(self, log_id):
        """Generate human-readable explanation from log."""
        log = self.get_log(log_id)

        explanation = f"""
Decision Explanation for User {log['user_id']}
Date: {log['timestamp']}

DECISION: {log['prediction']}

WHY THIS DECISION WAS MADE:
Your application was processed by our automated system (version {log['model_version']}).

KEY FACTORS:
"""
        # Add top features
        for feature, importance in sorted(
            log['feature_importance'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]:
            explanation += f"- {feature}: {importance:.1%} influence\n"

        explanation += f"""

YOUR DATA:
{format_features(log['features_used'])}

YOUR RIGHTS:
- You can request human review of this decision
- You can provide additional information for reconsideration
- Contact: {log['appeal_process']}
"""
        return explanation
```

**Example explanation generated from audit log**:

```
Decision Explanation for User usr_8x3k9m2
Date: 2024-10-25T14:32:15Z

DECISION: DENIED

WHY THIS DECISION WAS MADE:
Your loan application was processed by our automated system (version credit-scoring:v2.3.1).

KEY FACTORS that influenced this decision:
- Credit Score (720): 35% influence
  → Score is below our threshold (750) for this loan amount
- Debt-to-Income Ratio (0.45): 28% influence
  → Ratio exceeds our maximum (0.40)
- Employment Duration (8 months): 20% influence
  → Duration is shorter than our requirement (12 months)
- Income ($45,000): 10% influence
  → Income is below recommended level for this loan amount
- Existing Loans (3): 7% influence
  → Number of existing obligations considered

YOUR DATA USED:
- Age: 28
- Income: $45,000/year
- Credit Score: 720
- Debt-to-Income Ratio: 0.45
- Employment Duration: 8 months
- Existing Loans: 3
- Loan Amount Requested: $50,000

YOUR RIGHTS UNDER GDPR:
- You have the right to request human review of this automated decision
- You can provide additional information or documentation for reconsideration
- You can contest this decision
- You can request deletion of your data (subject to legal retention requirements)

TO APPEAL:
Email: appeals@bank.com
Phone: +1-555-0123
Reference ID: log_20241025_143215_abc123
```

**Technical requirements**:

1. **Store explainability data**:
```python
explainability = {
    'feature_importance': model.feature_importances_,
    'shap_values': shap_explainer.shap_values(features),
    'decision_threshold': 0.5,
    'prediction_proba': y_proba
}
```

2. **Enable individual lookups**:
```python
def get_user_decisions(user_id, start_date, end_date):
    """Retrieve all decisions for a user (GDPR access request)."""
    return [
        log for log in self.logs
        if log['user_id'] == user_id
        and start_date <= log['timestamp'] <= end_date
    ]
```

3. **Support data deletion** (Right to Erasure):
```python
def anonymize_user_data(user_id):
    """
    Anonymize user data while preserving audit trail.
    Note: Some logs may need to be retained for legal reasons.
    """
    for log in self.logs:
        if log['user_id'] == user_id:
            # Pseudonymize instead of delete (preserve audit trail)
            log['user_id'] = hash_user_id(user_id)
            log['features'] = anonymize_features(log['features'])
```

**Best practices**:
- Generate explanations automatically from logs
- Store sufficient detail for meaningful explanations
- Train customer service on explanation process
- Provide human review option
- Document explanation methodology in model cards
- Test explanations with non-technical users

</details>

---

## Section 5: GDPR & Regulatory Compliance (Questions 25-30)

### Question 25
What is GDPR's principle of "data minimization" and how does it apply to ML training data?

A) Minimize file sizes
B) Collect and use only the data necessary for the specified purpose
C) Use as little training data as possible
D) Minimize the number of models

<details>
<summary>Answer</summary>

**B) Collect and use only the data necessary for the specified purpose**

**Explanation**: Data minimization is a core GDPR principle (Article 5(1)(c)):

**Principle**: Personal data shall be adequate, relevant, and **limited to what is necessary** in relation to the purposes for which they are processed.

**Implications for ML**:

1. **Feature selection**:
```python
# ❌ Bad: Collect everything "just in case"
features = [
    'age', 'income', 'credit_score',
    'social_security_number',  # ❌ Not necessary for prediction
    'medical_history',  # ❌ Irrelevant to loan default
    'browsing_history',  # ❌ Excessive
    'full_transaction_history'  # ❌ Can use aggregated stats instead
]

# ✓ Good: Only necessary features
features = [
    'age',
    'income',
    'credit_score',
    'employment_duration',
    'debt_to_income_ratio'
]
```

2. **Purpose limitation**:
- Data collected for one purpose can't be used for unrelated purpose
- Example: Health data collected for insurance can't be used for marketing

3. **Retention limitation**:
```python
# Delete training data after model is deployed
def cleanup_old_training_data():
    """Remove training data older than retention period."""
    retention_days = 90  # Or as required by policy

    for dataset in training_datasets:
        if (datetime.now() - dataset.created_at).days > retention_days:
            if not dataset.required_for_compliance:
                dataset.delete()  # Or anonymize
```

4. **Aggregation over raw data**:
```python
# ❌ Store all transactions
user_data = {
    'transactions': [
        {'date': '2024-01-01', 'amount': 50.00, 'merchant': 'Store A'},
        {'date': '2024-01-02', 'amount': 120.00, 'merchant': 'Store B'},
        # ... thousands of transactions
    ]
}

# ✓ Store aggregated features (sufficient for model)
user_features = {
    'avg_monthly_spend': 1200.00,
    'max_transaction_amount': 500.00,
    'transaction_frequency': 3.5,  # per week
    'unique_merchants': 12
}
# Raw transactions can be deleted
```

**Practical application**:

**Step 1: Justify each feature**:
```markdown
| Feature | Purpose | Justification | Keep? |
|---------|---------|---------------|-------|
| age | Risk assessment | Correlates with default rate | ✓ |
| credit_score | Risk assessment | Primary predictor of default | ✓ |
| SSN | Identification | Not used in model, only for linking records | ✗ Replace with pseudonym |
| full_name | Identification | Not used in model | ✗ Remove |
| medical_history | ??? | No clear purpose for loan default prediction | ✗ Remove |
```

**Step 2: Implement technical measures**:
```python
class DataMinimizer:
    """Enforce data minimization in ML pipelines."""

    def __init__(self, allowed_features):
        self.allowed_features = set(allowed_features)

    def filter_features(self, data):
        """Remove unnecessary features."""
        return data[list(self.allowed_features)]

    def pseudonymize_identifiers(self, data, id_columns):
        """Replace direct identifiers with pseudonyms."""
        for col in id_columns:
            if col in data.columns:
                data[col] = data[col].apply(self._hash_identifier)
        return data

    def _hash_identifier(self, identifier):
        """Hash identifier for pseudonymization."""
        return hashlib.sha256(str(identifier).encode()).hexdigest()[:16]

# Usage
minimizer = DataMinimizer(allowed_features=['age', 'income', 'credit_score'])
clean_data = minimizer.filter_features(raw_data)
clean_data = minimizer.pseudonymize_identifiers(clean_data, id_columns=['ssn', 'name'])
```

**Benefits**:
- ✓ Reduced privacy risk
- ✓ Simpler models (fewer features)
- ✓ Lower storage costs
- ✓ Faster training
- ✓ GDPR compliance

**Common violations**:
- ❌ "Collect everything, we might need it later"
- ❌ Using customer data for purposes not disclosed
- ❌ Keeping training data indefinitely
- ❌ Including sensitive attributes without justification

</details>

---

### Question 26
**[Multiple Select]** Which of the following are GDPR rights that impact ML systems? (Select all that apply)

A) Right to access (obtain copy of personal data)
B) Right to free ML models
C) Right to rectification (correction of inaccurate data)
D) Right to erasure ("right to be forgotten")
E) Right to restrict processing
F) Right to data portability

<details>
<summary>Answer</summary>

**A, C, D, E, F**

**Explanation**:
- **A**: CORRECT - Right to Access (Article 15)
  - Individuals can request copy of their personal data
  - Must provide information on automated decision-making logic
  - **ML impact**:
    - Must be able to retrieve training samples for a user
    - Must explain what data was used to train model
    - Must provide predictions made about the user
  ```python
  def access_request(user_id):
      """Respond to GDPR access request."""
      return {
          'training_data': get_user_training_samples(user_id),
          'predictions': get_user_predictions(user_id),
          'features_used': get_features_for_user(user_id),
          'models_applied': get_models_used_on_user(user_id)
      }
  ```

- **B**: INCORRECT - No right to free ML models
  - GDPR doesn't require free services
  - Companies can charge for products/services

- **C**: CORRECT - Right to Rectification (Article 16)
  - Users can correct inaccurate personal data
  - **ML impact**:
    - Must update training data if user corrects information
    - May need to retrain model with corrected data
    - Must track data lineage to identify affected models
  ```python
  def rectify_data(user_id, corrected_data):
      """Handle data rectification request."""
      # Update in database
      update_user_data(user_id, corrected_data)

      # Check if data was used in training
      affected_models = find_models_trained_on_user(user_id)

      # Consider retraining or at minimum log the correction
      for model in affected_models:
          log_data_correction(model, user_id, corrected_data)
          # May trigger model retrain if significant
  ```

- **D**: CORRECT - Right to Erasure / Right to be Forgotten (Article 17)
  - Users can request deletion of their personal data
  - **ML impact**:
    - Must delete user's training data
    - May need to retrain model without user's data
    - Can retain anonymized/aggregated data
    - Exceptions: Legal obligations, public interest
  ```python
  def erase_user_data(user_id):
      """Handle right to erasure request."""
      # Delete raw data
      delete_user_records(user_id)

      # For training data in models:
      # Option 1: Retrain without this user (expensive)
      # Option 2: Mark as deleted, retrain on next cycle
      # Option 3: Anonymize (if truly anonymized, GDPR doesn't apply)

      mark_for_exclusion_in_next_retrain(user_id)

      # Delete predictions
      delete_user_predictions(user_id)

      # Keep audit logs (may be legally required)
      # but anonymize user identifier
      anonymize_audit_logs(user_id)
  ```

- **E**: CORRECT - Right to Restriction of Processing (Article 18)
  - Users can request to limit how data is processed
  - **ML impact**:
    - Must stop using user's data for model training
    - May still store data, but not process it
    - Must flag user's data as restricted
  ```python
  def restrict_processing(user_id):
      """Handle restriction of processing request."""
      # Flag user as restricted
      set_processing_restriction(user_id, restricted=True)

      # Don't include in new training runs
      # Don't make automated decisions
      # Can store data but not use it
  ```

- **F**: CORRECT - Right to Data Portability (Article 20)
  - Users can receive their data in machine-readable format
  - Users can transfer data to another controller
  - **ML impact**:
    - Must export user's data in structured format (CSV, JSON)
    - Include features, predictions, model versions used
  ```python
  def export_user_data(user_id):
      """Export user data in portable format."""
      user_data = {
          'personal_info': get_user_info(user_id),
          'features_used': get_features(user_id),
          'predictions': [
              {
                  'timestamp': pred.timestamp,
                  'model_version': pred.model_version,
                  'prediction': pred.value,
                  'features_used': pred.features
              }
              for pred in get_predictions(user_id)
          ]
      }

      # Export as JSON (machine-readable)
      return json.dumps(user_data, indent=2)
  ```

**Implementation summary**:
```python
class GDPRCompliantMLSystem:
    """ML system with GDPR compliance."""

    def handle_access_request(self, user_id):
        """Article 15: Right to access."""
        return self._export_all_user_data(user_id)

    def handle_rectification(self, user_id, corrections):
        """Article 16: Right to rectification."""
        self._update_data(user_id, corrections)
        self._flag_for_retrain()

    def handle_erasure(self, user_id):
        """Article 17: Right to erasure."""
        if self._can_erase(user_id):
            self._delete_user_data(user_id)
            self._anonymize_logs(user_id)
            return True
        return False  # Legal obligation to retain

    def handle_restriction(self, user_id):
        """Article 18: Right to restriction."""
        self._set_processing_flag(user_id, restricted=True)

    def handle_portability(self, user_id):
        """Article 20: Right to data portability."""
        return self._export_structured_data(user_id)
```

</details>

---

### Question 27
What is "Privacy by Design" in the context of ML systems?

A) Designing private buildings
B) Integrating privacy and data protection principles into ML system design from the start, not as an afterthought
C) Using encrypted designs
D) Hiding model architectures

<details>
<summary>Answer</summary>

**B) Integrating privacy and data protection principles into ML system design from the start, not as an afterthought**

**Explanation**: Privacy by Design is a GDPR requirement (Article 25):

**Core principles** (7 Foundational Principles by Ann Cavoukian):

1. **Proactive not Reactive; Preventative not Remedial**
   - Anticipate privacy issues before they occur
   - Example: Design data pipelines with pseudonymization from start

2. **Privacy as the Default Setting**
   - Maximum privacy protection by default
   - Users don't need to take action
   - Example: Opt-in for data collection, not opt-out

3. **Privacy Embedded into Design**
   - Privacy integral to system, not bolt-on
   - Example: Differential privacy in model training algorithm

4. **Full Functionality - Positive-Sum, not Zero-Sum**
   - Privacy AND functionality (not trade-off)
   - Example: Federated learning enables model training without centralizing data

5. **End-to-End Security**
   - Lifecycle protection (collection → deletion)
   - Example: Encryption at rest and in transit

6. **Visibility and Transparency**
   - Operations remain visible and transparent
   - Example: Model cards, explainability, audit logs

7. **Respect for User Privacy**
   - User-centric design
   - Example: Clear consent, easy opt-out

**ML-specific Privacy by Design**:

**1. Data Collection**:
```python
# ❌ Collect first, ask questions later
def collect_all_data(user):
    return {
        'name': user.name,
        'ssn': user.ssn,
        'full_browsing_history': user.get_all_browsing(),
        'all_purchases': user.get_all_purchases(),
        # Collect everything!
    }

# ✓ Privacy by Design: Collect only what's needed
def collect_minimal_data(user, purpose='credit_scoring'):
    if purpose == 'credit_scoring':
        return {
            'user_id': hash(user.id),  # Pseudonymized
            'age_range': user.age // 10 * 10,  # Generalized (30-39, not 34)
            'income_bracket': categorize_income(user.income),
            'credit_score': user.credit_score
        }
    # Different purposes collect different data
```

**2. Model Training**:
```python
# ✓ Differential Privacy
from diffprivlib.models import LogisticRegression

model = LogisticRegression(epsilon=1.0)  # Privacy budget
model.fit(X_train, y_train)
# Adds noise to prevent individual inference
```

**3. Data Storage**:
```python
# ✓ Encryption by default
def store_training_data(data, purpose, retention_days=90):
    """Store with privacy controls."""
    encrypted_data = encrypt(data)  # At-rest encryption

    metadata = {
        'purpose': purpose,
        'retention_until': datetime.now() + timedelta(days=retention_days),
        'encryption_key_id': key_id,
        'anonymized': True
    }

    save(encrypted_data, metadata)
    schedule_deletion(retention_until)  # Auto-delete
```

**4. Access Controls**:
```python
# ✓ Role-based access
class DataAccess:
    def __init__(self):
        self.permissions = {
            'ml_engineer': ['read_aggregated_data', 'train_model'],
            'data_scientist': ['read_anonymized_data', 'analyze'],
            'admin': ['read_raw_data'],  # Minimal access to PII
            'auditor': ['read_logs', 'verify_compliance']
        }

    def can_access(self, role, operation, data_type):
        if data_type == 'pii' and operation == 'read':
            # Strict controls on PII
            return role in ['admin'] and self.log_access(role, operation)
        return operation in self.permissions.get(role, [])
```

**5. Feature Engineering**:
```python
# ✓ Privacy-preserving transformations
def engineer_features(raw_data):
    """Transform data to reduce privacy risk."""
    features = {}

    # Generalization
    features['age_group'] = raw_data['age'] // 10 * 10  # 25 → 20-29

    # Aggregation
    features['avg_transaction'] = raw_data['transactions'].mean()
    # Don't keep individual transactions

    # Suppression
    if raw_data['is_rare_condition']:
        # Suppress rare values to prevent re-identification
        features['is_rare_condition'] = None

    # k-anonymity: Ensure each combination appears ≥ k times
    return ensure_k_anonymity(features, k=5)
```

**6. Model Deployment**:
```python
# ✓ Privacy controls in inference
def predict(features, user_consent):
    """Make prediction with privacy checks."""
    # Verify consent
    if not user_consent.allows('automated_decision'):
        return require_human_review()

    # Make prediction
    prediction = model.predict(features)

    # Log with privacy protections
    audit_log.log(
        user_id=hash(user_id),  # Pseudonymized
        prediction=prediction,
        retention_days=90  # Auto-delete logs
    )

    return prediction
```

**7. Monitoring**:
```python
# ✓ Privacy-preserving analytics
def monitor_model_performance():
    """Monitor without exposing individual data."""
    # Use aggregated metrics
    metrics = {
        'overall_accuracy': compute_accuracy(y_true, y_pred),
        'accuracy_by_age_group': group_accuracy(y_true, y_pred, age_groups),
        # Don't report individual predictions
    }

    # Differential privacy for monitoring
    noisy_metrics = add_laplace_noise(metrics, epsilon=1.0)

    return noisy_metrics
```

**Privacy by Design Checklist**:
- [ ] Data minimization: Collect only necessary features
- [ ] Pseudonymization: Hash identifiers
- [ ] Encryption: At rest and in transit
- [ ] Access controls: Role-based permissions
- [ ] Retention limits: Auto-delete after retention period
- [ ] Anonymization: Aggregate, generalize, suppress
- [ ] Consent management: Track and enforce user consent
- [ ] Differential privacy: Add noise to prevent inference
- [ ] Audit logging: Track all data access
- [ ] Privacy impact assessment: Document privacy risks
- [ ] User rights: Support access, rectification, erasure
- [ ] Transparency: Model cards, explanations

**Tools**:
- **Differential Privacy**: Google's DP library, IBM's diffprivlib
- **Federated Learning**: TensorFlow Federated, PySyft
- **Anonymization**: ARX, sdcMicro
- **Encryption**: AWS KMS, HashiCorp Vault

</details>

---

### Question 28
What is the difference between anonymization and pseudonymization under GDPR?

A) They are the same thing
B) Anonymization removes all identifying information making re-identification impossible; pseudonymization replaces identifiers with pseudonyms but re-identification is possible with additional information
C) Anonymization is faster
D) Pseudonymization is not allowed under GDPR

<details>
<summary>Answer</summary>

**B) Anonymization removes all identifying information making re-identification impossible; pseudonymization replaces identifiers with pseudonyms but re-identification is possible with additional information**

**Explanation**: This is a critical distinction for GDPR compliance:

**Anonymization**:
- **Definition**: Processing personal data such that it can **no longer** be attributed to a specific individual without disproportionate effort
- **GDPR status**: Anonymized data is **NOT** personal data → GDPR doesn't apply
- **Irreversible**: Cannot be re-identified, even with additional information
- **Examples**:
  - Aggregated statistics (average age of customers: 35)
  - k-anonymity with suppression (age 34 → age 30-39, shared by 1000+ people)
  - Differential privacy with high noise

**Pseudonymization**:
- **Definition**: Processing where identifiers are replaced with pseudonyms, but re-identification is **possible** with additional information kept separately
- **GDPR status**: Still **IS** personal data → GDPR applies
- **Reversible**: Can be re-identified with the mapping key
- **Examples**:
  - Hashing user IDs (user_123 → 7d8f3e...)
  - Tokenization (SSN → token)
  - Encryption (can be decrypted with key)

**Comparison**:

| Aspect | Anonymization | Pseudonymization |
|--------|---------------|------------------|
| **GDPR applies?** | NO (not personal data) | YES (still personal data) |
| **Reversible?** | NO | YES (with additional info) |
| **Re-identification** | Impossible (or extremely difficult) | Possible with mapping key |
| **Use case** | Public datasets, research | Internal processing, security |
| **Example** | "Average age: 35" | "User A7F3 age: 35" |
| **Data utility** | Lower (less granular) | Higher (preserves granularity) |
| **Privacy protection** | Highest | Moderate |

**Examples**:

**Anonymization**:
```python
def anonymize_dataset(data):
    """Truly anonymize data (GDPR no longer applies)."""
    # Aggregation - no individual records
    anonymized = {
        'total_users': len(data),
        'average_age': data['age'].mean(),
        'age_distribution': {
            '18-25': (data['age'] < 26).sum(),
            '26-35': ((data['age'] >= 26) & (data['age'] < 36)).sum(),
            '36-50': ((data['age'] >= 36) & (data['age'] < 51)).sum(),
            '50+': (data['age'] >= 51).sum()
        },
        'average_income': data['income'].mean(),
        'approval_rate': (data['approved'] == True).mean()
    }
    # ✓ No way to identify individuals
    # ✓ GDPR doesn't apply
    return anonymized

# Or: k-anonymity with generalization
def k_anonymize(data, k=5):
    """Ensure each record is indistinguishable from k-1 others."""
    # Generalize age: 34 → 30-39
    data['age_group'] = (data['age'] // 10) * 10

    # Generalize location: exact address → ZIP code
    data['location'] = data['address'].apply(extract_zip_code)

    # Suppress rare values
    for col in data.columns:
        value_counts = data[col].value_counts()
        rare_values = value_counts[value_counts < k].index
        data.loc[data[col].isin(rare_values), col] = 'SUPPRESSED'

    # Remove direct identifiers
    data = data.drop(['name', 'ssn', 'email'], axis=1)

    return data  # Each record shared by ≥ k people
```

**Pseudonymization**:
```python
import hashlib
import secrets

class Pseudonymizer:
    """Pseudonymize identifiers (GDPR still applies)."""

    def __init__(self):
        self.mapping = {}  # Store mapping securely
        self.salt = secrets.token_bytes(16)

    def pseudonymize(self, identifier):
        """Replace identifier with pseudonym."""
        # Hash identifier (deterministic)
        pseudonym = hashlib.sha256(
            str(identifier).encode() + self.salt
        ).hexdigest()[:16]

        # Store mapping (keep separately, access-controlled)
        self.mapping[pseudonym] = identifier

        return pseudonym

    def de_pseudonymize(self, pseudonym):
        """Reverse pseudonymization (requires mapping)."""
        if pseudonym in self.mapping:
            return self.mapping[pseudonym]
        return None

# Usage
pseudonymizer = Pseudonymizer()

# Pseudonymize dataset
data['user_id'] = data['user_id'].apply(pseudonymizer.pseudonymize)
data['email'] = data['email'].apply(pseudonymizer.pseudonymize)

# Data still contains individual records
# Can still train granular models
# But identifiers are protected

# Later, can de-pseudonymize if needed (e.g., GDPR access request)
original_user_id = pseudonymizer.de_pseudonymize('7d8f3e4a9b2c1d0e')
```

**When to use each**:

**Use Anonymization when**:
- Publishing datasets publicly
- Sharing with third parties
- Research purposes
- Don't need individual-level data
- Want to avoid GDPR obligations

**Use Pseudonymization when**:
- Internal processing
- Need individual-level granularity for ML
- May need to re-identify (e.g., for GDPR requests)
- Want security-in-depth
- GDPR compliance required anyway

**GDPR encourages pseudonymization** (Article 25, Recital 78):
> Pseudonymization is a useful technique to reduce risks to data subjects while allowing controllers to derive meaningful analytics

**Important**: Pseudonymization alone doesn't make you GDPR-compliant (still personal data), but it's a good security practice and can reduce compliance burden.

**Risk: Re-identification**:
Even "anonymized" data can sometimes be re-identified:
```python
# Example: "Anonymous" data
anonymous_data = {
    'age': 34,
    'zip_code': '02138',  # Cambridge, MA
    'gender': 'female',
    'disease': 'diabetes'
}

# Re-identification risk:
# - Only a few 34-year-old females in ZIP 02138
# - Cross-reference with voter registration (public data)
# - Can uniquely identify individual

# Solution: More aggressive anonymization
safer_data = {
    'age_range': '30-39',
    'region': 'Massachusetts',  # Not ZIP
    'gender': 'female',
    'disease': 'diabetes'
}
```

**Best practice**: Always perform re-identification risk assessment before claiming data is anonymized.

</details>

---

### Question 29
Analyze this compliance scenario:

Your ML system was trained on customer data collected in 2022. It's now 2024, and a customer requests deletion of their data (Right to Erasure). The model is still in production. What should you do?

A) Ignore the request - model is already trained
B) Delete the customer's raw data but keep the model unchanged
C) Delete the customer's data and retrain the model without it, or document why erasure is not possible (legal obligation to retain)
D) Delete the entire model

<details>
<summary>Answer</summary>

**C) Delete the customer's data and retrain the model without it, or document why erasure is not possible (legal obligation to retain)**

**Explanation**: Right to Erasure is complex for ML systems:

**GDPR Article 17 - Right to Erasure**:
Data must be erased when:
1. No longer necessary for original purpose
2. User withdraws consent
3. User objects to processing
4. Data was unlawfully processed

**Exceptions** (can refuse erasure):
1. Legal obligation to retain data
2. Public interest / official authority
3. Establishment, exercise, or defense of legal claims
4. Archiving in public interest

**Step-by-step response**:

**Step 1: Assess if erasure can be refused**:
```python
def can_refuse_erasure(user_id, purpose):
    """Determine if erasure can be legally refused."""
    reasons_to_retain = []

    # Check legal obligations
    if has_legal_retention_requirement(user_id, purpose):
        # e.g., Anti-money laundering (5 years), SOX (7 years)
        reasons_to_retain.append('Legal retention requirement')

    # Check pending legal claims
    if has_pending_litigation(user_id):
        reasons_to_retain.append('Legal claim defense')

    # Check public interest
    if is_public_interest_research(purpose):
        reasons_to_retain.append('Scientific research')

    if reasons_to_retain:
        return False, reasons_to_retain  # Cannot erase
    else:
        return True, []  # Must erase
```

**Step 2: If erasure required, delete data**:
```python
def process_erasure_request(user_id):
    """Handle right to erasure request."""
    # 1. Delete from active databases
    delete_user_from_database(user_id)

    # 2. Delete from backups (or document retention policy)
    schedule_backup_deletion(user_id)  # May take backup cycle to complete

    # 3. Identify affected models
    affected_models = find_models_trained_on_user(user_id)

    # 4. Handle model training data
    for model in affected_models:
        # Option A: Remove from training set and retrain
        if model.can_retrain():
            remove_from_training_data(model, user_id)
            schedule_retrain(model)

        # Option B: Mark for exclusion in next retrain cycle
        else:
            mark_for_exclusion(model, user_id)
            log_erasure_pending(model, user_id)

    # 5. Delete predictions about user
    delete_user_predictions(user_id)

    # 6. Anonymize audit logs
    # May keep logs for compliance, but anonymize user identifier
    anonymize_audit_logs(user_id)

    # 7. Document the erasure
    log_erasure_action(user_id, timestamp=datetime.now())

    return {
        'status': 'completed',
        'data_deleted': True,
        'models_affected': affected_models,
        'retrain_scheduled': True,
        'logs_anonymized': True
    }
```

**Step 3: Communicate to user**:
```python
def generate_erasure_confirmation(user_id):
    """Generate confirmation message for user."""
    return f"""
Dear Customer,

Your data erasure request has been processed.

ACTIONS TAKEN:
✓ Personal data deleted from our systems
✓ Predictions about you deleted
✓ Scheduled for removal from backup systems (within 30 days)
✓ ML models will be retrained without your data (next cycle: {next_retrain_date})
✓ Audit logs anonymized (we retain anonymized logs for compliance)

IMPORTANT NOTES:
- Some data may be retained for legal obligations (e.g., transaction records required for tax compliance for 7 years)
- Anonymized aggregate statistics (which cannot identify you) may be retained

If you have questions, please contact: privacy@company.com

Confirmation ID: {confirmation_id}
Date: {datetime.now().isoformat()}
"""
```

**Handling model retraining**:

**Option 1: Immediate retrain** (best for compliance):
```python
def immediate_retrain(model_id, excluded_user_id):
    """Retrain model without specific user's data."""
    # Load training data
    training_data = load_training_data(model_id)

    # Remove user's data
    training_data = training_data[training_data['user_id'] != excluded_user_id]

    # Retrain
    new_model = train_model(training_data)

    # Deploy
    deploy_model(new_model, replace=model_id)

    log_retrain_for_erasure(model_id, excluded_user_id)
```

**Option 2: Scheduled retrain** (more practical):
```python
class ModelErasureManager:
    """Manage erasure requests for models."""

    def __init__(self):
        self.exclusion_list = set()
        self.retrain_schedule = {}

    def add_erasure_request(self, model_id, user_id):
        """Add user to exclusion list."""
        self.exclusion_list.add((model_id, user_id))

        # Schedule retrain if not already scheduled
        if model_id not in self.retrain_schedule:
            # Next monthly retrain cycle
            self.retrain_schedule[model_id] = get_next_retrain_date()

        return self.retrain_schedule[model_id]

    def retrain_with_exclusions(self, model_id):
        """Retrain model excluding erased users."""
        excluded_users = [
            user_id for (mid, user_id) in self.exclusion_list
            if mid == model_id
        ]

        training_data = load_training_data(model_id)
        training_data = training_data[~training_data['user_id'].isin(excluded_users)]

        new_model = train_model(training_data)
        deploy_model(new_model)

        # Clear exclusion list for this model
        self.exclusion_list = {
            (mid, uid) for (mid, uid) in self.exclusion_list
            if mid != model_id
        }
```

**Option 3: Differential Privacy** (alternative approach):
```python
# If model trained with differential privacy, can argue:
# - Individual's contribution is already obscured by noise
# - Removing individual wouldn't materially change model
# - Less clear legally, consult GDPR experts

# But still should:
# - Delete raw training data
# - Delete predictions
# - Document DP approach in privacy policy
```

**Documentation**:
```python
erasure_log = {
    'request_id': 'erasure_20241025_user123',
    'user_id': 'user_123',
    'request_date': '2024-10-25',
    'completion_date': '2024-10-26',
    'actions_taken': [
        'Deleted user records from database',
        'Deleted user predictions',
        'Removed from training data for models: [model_v1, model_v2]',
        'Scheduled model retrain for 2024-11-01',
        'Anonymized audit logs'
    ],
    'data_retained': [
        'Transaction records (legal requirement: AML, 5 years)'
    ],
    'retention_justification': 'Anti-Money Laundering regulations require 5-year retention'
}
```

**Best practices**:
- ✓ Respond within 30 days (GDPR requirement)
- ✓ Document all actions taken
- ✓ Communicate clearly to user
- ✓ Retrain models or schedule retrain
- ✓ Keep anonymized logs for compliance
- ✓ Document any data retained with justification
- ✓ Implement automated erasure pipelines

</details>

---

### Question 30
**[Multiple Select]** What are best practices for GDPR-compliant ML systems? (Select all that apply)

A) Conduct Data Protection Impact Assessments (DPIAs) for high-risk ML systems
B) Implement Privacy by Design from the start
C) Document all processing activities in a Record of Processing Activities (ROPA)
D) Never use personal data for ML
E) Appoint a Data Protection Officer (DPO) if required
F) Provide clear, specific consent mechanisms
G) Regularly audit models for bias and fairness

<details>
<summary>Answer</summary>

**A, B, C, E, F, G**

**Explanation**:
- **A**: CORRECT - Data Protection Impact Assessment (DPIA)
  - **Required** for high-risk processing (GDPR Article 35)
  - High-risk includes:
    - Automated decision-making with legal/significant effects
    - Large-scale processing of sensitive data
    - Systematic monitoring
  - **ML systems often qualify** (automated decisions, profiling)
  ```markdown
  ## DPIA for Credit Scoring ML Model

  ### Processing Description
  - Purpose: Automated credit risk assessment
  - Data: Financial history, employment, demographics
  - Technology: XGBoost classifier
  - Scope: 100,000+ applicants/year

  ### Necessity and Proportionality
  - Legitimate interest: Risk management
  - Data minimization: Only relevant features
  - Alternatives considered: Human-only review (slower, less consistent)

  ### Risks to Rights and Freedoms
  - Risk 1: Discriminatory outcomes (HIGH)
    - Mitigation: Fairness metrics, bias testing, human review
  - Risk 2: Inaccurate data leading to wrongful denial (MEDIUM)
    - Mitigation: Data validation, appeals process
  - Risk 3: Data breach exposure of financial data (HIGH)
    - Mitigation: Encryption, access controls, monitoring

  ### Consultation
  - DPO reviewed: Approved with mitigations
  - Supervisory authority: Notified (high-risk)

  ### Conclusion
  - Risks acceptable with mitigations
  - Monitoring plan: Quarterly fairness audits
  ```

- **B**: CORRECT - Privacy by Design
  - Integrate privacy from system design phase
  - See Question 27 for detailed explanation
  - Examples:
    - Pseudonymization in data pipeline
    - Differential privacy in training
    - Auto-deletion of old data
    - Minimal data collection

- **C**: CORRECT - Record of Processing Activities (ROPA)
  - **Required** for organizations with 250+ employees (Article 30)
  - Documents all data processing
  ```markdown
  ## ROPA Entry: ML-Based Credit Scoring

  - **Purpose**: Automated credit risk assessment for loan applications
  - **Legal basis**: Legitimate interest (risk management)
  - **Data categories**:
    - Identity: Name, date of birth, address
    - Financial: Income, credit score, existing loans
    - Employment: Job title, employer, duration
  - **Data subjects**: Loan applicants (age 18+)
  - **Recipients**: Internal credit team, external credit bureaus
  - **Transfers**: None outside EU
  - **Retention**: 7 years (financial regulation requirement)
  - **Security measures**: Encryption at rest, access controls, audit logging
  - **DPO contact**: dpo@company.com
  ```

- **D**: INCORRECT - Can use personal data with proper legal basis
  - GDPR doesn't prohibit personal data use
  - Requires:
    - Legal basis (consent, contract, legitimate interest, etc.)
    - Transparency
    - User rights
    - Security measures
  - Many ML applications legitimately use personal data

- **E**: CORRECT - Data Protection Officer (DPO)
  - **Required** if (Article 37):
    - Public authority
    - Core activities involve large-scale systematic monitoring
    - Core activities involve large-scale processing of sensitive data
  - **ML systems often trigger DPO requirement**
  - DPO responsibilities:
    - Monitor GDPR compliance
    - Advise on DPIAs
    - Cooperate with supervisory authority
    - Be contact point for data subjects

- **F**: CORRECT - Clear, specific consent
  - If using consent as legal basis (Article 7):
    - Must be freely given, specific, informed, unambiguous
    - Clear affirmative action (not pre-checked boxes)
    - Easy to withdraw
    - Separate consents for different purposes
  ```python
  # ❌ Bad consent
  consent_text = "I agree to Terms and Conditions [checkbox]"
  # Too vague, bundles everything

  # ✓ Good consent
  consent_options = {
      'necessary_processing': {
          'text': 'Process my data to evaluate loan application',
          'required': True,  # Can't opt out of primary purpose
          'legal_basis': 'Contract'
      },
      'marketing': {
          'text': 'Send me marketing emails about other products',
          'required': False,
          'legal_basis': 'Consent',
          'can_withdraw': True
      },
      'analytics': {
          'text': 'Use my data to improve models (anonymized)',
          'required': False,
          'legal_basis': 'Legitimate Interest'
      }
  }
  ```

- **G**: CORRECT - Regular bias and fairness audits
  - Not explicitly required by GDPR, but:
    - GDPR requires "fair processing" (Article 5)
    - Many regulations require bias testing (EU AI Act, NY Bias Audit Law)
    - Ethical responsibility
  ```python
  class FairnessAuditScheduler:
      """Schedule regular fairness audits."""

      def quarterly_audit(self, model):
          """Perform quarterly fairness audit."""
          report = {
              'date': datetime.now().isoformat(),
              'model_version': model.version,
              'metrics': {},
              'issues': [],
              'actions': []
          }

          # Test demographic parity
          dp_ratio = demographic_parity_ratio(y_test, y_pred, sensitive_features)
          report['metrics']['demographic_parity_ratio'] = dp_ratio
          if dp_ratio < 0.8:
              report['issues'].append('Fails 80% rule')
              report['actions'].append('Retrain with fairness constraints')

          # Test equalized odds
          eo_diff = equalized_odds_difference(y_test, y_pred, sensitive_features)
          report['metrics']['equalized_odds_diff'] = eo_diff
          if eo_diff > 0.1:
              report['issues'].append('Equalized odds violation')
              report['actions'].append('Threshold optimization')

          # Test for drift
          # Test for accuracy degradation
          # Test for proxy discrimination

          return report
  ```

**Complete GDPR compliance checklist**:

```markdown
## GDPR Compliance Checklist for ML Systems

### Legal Basis
- [ ] Identified legal basis for processing (consent, contract, legitimate interest, etc.)
- [ ] Documented legal basis in ROPA
- [ ] Obtained consent if using consent as basis
- [ ] Legitimate Interest Assessment if using legitimate interest

### Transparency
- [ ] Privacy policy explains ML processing
- [ ] Model cards document model behavior
- [ ] Users informed of automated decision-making
- [ ] Right to explanation implemented

### Data Minimization
- [ ] Collect only necessary features
- [ ] Retention policies defined and enforced
- [ ] Auto-deletion configured

### Privacy by Design
- [ ] Pseudonymization implemented
- [ ] Encryption at rest and in transit
- [ ] Access controls configured
- [ ] Privacy impact assessment completed

### User Rights
- [ ] Right to access: Can export user data
- [ ] Right to rectification: Can correct user data
- [ ] Right to erasure: Can delete user data (with retraining)
- [ ] Right to restriction: Can limit processing
- [ ] Right to data portability: Can export in machine-readable format
- [ ] Right to object: Can opt out of processing

### Security
- [ ] Encryption implemented
- [ ] Access controls configured
- [ ] Audit logging enabled
- [ ] Incident response plan documented
- [ ] Regular security testing

### Accountability
- [ ] ROPA maintained
- [ ] DPO appointed (if required)
- [ ] DPIA completed for high-risk processing
- [ ] Regular compliance audits
- [ ] Staff training on GDPR

### Fairness
- [ ] Bias testing performed
- [ ] Fairness metrics monitored
- [ ] Regular fairness audits scheduled
- [ ] Bias mitigation implemented if needed

### Documentation
- [ ] Model cards created
- [ ] Data processing documented in ROPA
- [ ] Privacy policy updated
- [ ] Consent records maintained
- [ ] Audit logs retained

### Vendor Management
- [ ] Data Processing Agreements with vendors
- [ ] Vendor GDPR compliance verified
- [ ] Data transfer mechanisms documented (if non-EU)
```

</details>

---

## Scoring Guide

| Score | Grade | Feedback |
|-------|-------|----------|
| 28-30 | A+ | Excellent! Deep understanding of ML governance and compliance |
| 25-27 | A | Great job! Strong grasp of fairness, bias mitigation, and GDPR |
| 23-24 | B | Good. Review missed topics, especially regulatory requirements |
| 20-22 | C | Passing. Revisit fairness metrics and compliance frameworks |
| < 20 | F | Please review lecture notes and retry |

---

## Answer Key Summary

**Section 1 (Fairness Metrics)**: 1.B | 2.B | 3.B | 4.B,C,E | 5.D | 6.B

**Section 2 (Bias Mitigation)**: 7.B | 8.B | 9.B | 10.B,C,E,F | 11.B | 12.B

**Section 3 (Model Cards)**: 13.B | 14.A,B,D,F | 15.B | 16.B | 17.B | 18.B

**Section 4 (Audit Logging)**: 19.B | 20.B | 21.A,B,C,E,F | 22.B | 23.B | 24.A

**Section 5 (GDPR)**: 25.B | 26.A,C,D,E,F | 27.B | 28.B | 29.C | 30.A,B,C,E,F,G

---

## Next Steps

- Review any missed questions
- Complete hands-on exercises
- Implement fairness assessments with Fairlearn
- Create model cards for your models
- Set up tamper-proof audit logging
- Review GDPR requirements for your jurisdiction
- Conduct privacy impact assessments
- Explore additional resources in `resources.md`

**Additional Resources**:
- Fairlearn Documentation: https://fairlearn.org/
- Model Cards Paper: https://arxiv.org/abs/1810.03993
- GDPR Official Text: https://gdpr-info.eu/
- EU AI Act: https://artificialintelligenceact.eu/
- Google's Responsible AI Practices: https://ai.google/responsibilities/responsible-ai-practices/

Good luck!
