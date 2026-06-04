# Module 05: Experimentation & A/B Testing - Quiz

## Instructions

- **Total Questions**: 28
- **Time Limit**: 40 minutes
- **Passing Score**: 75% (21/28 correct)
- **Question Types**: Multiple choice, multiple select, code analysis

---

## Section 1: A/B Testing Fundamentals (Questions 1-6)

### Question 1
What is the primary purpose of A/B testing in ML systems?

A) To test code for bugs
B) To compare performance of two or more model versions with statistical rigor
C) To increase model accuracy
D) To reduce infrastructure costs

<details>
<summary>Answer</summary>

**B) To compare performance of two or more model versions with statistical rigor**

**Explanation**: A/B testing allows you to:
- Compare a new model (treatment) against the current model (control)
- Measure impact on real users and business metrics
- Use statistical methods to determine if differences are significant
- Make data-driven decisions about model deployment
- Minimize risk by testing incrementally

Example: Testing whether a new recommendation model increases click-through rate compared to the production model.

</details>

---

### Question 2
What is "random assignment" in A/B testing, and why is it important?

A) Randomly selecting features for the model
B) Randomly assigning users to control or treatment groups to eliminate selection bias
C) Randomly shuffling training data
D) Using random seeds in model training

<details>
<summary>Answer</summary>

**B) Randomly assigning users to control or treatment groups to eliminate selection bias**

**Explanation**: Random assignment ensures:
- Each user has equal probability of being in control or treatment
- Groups are statistically equivalent at the start
- Differences in outcomes can be attributed to the treatment, not pre-existing differences
- Selection bias is eliminated

**Selection bias example**: If you assign early morning users to treatment and afternoon users to control, behavior differences might be due to time of day, not the model.

Random assignment makes groups comparable and results valid.

</details>

---

### Question 3
What is a "consistent" or "sticky" assignment in A/B testing?

A) Users randomly reassigned on each visit
B) The same user always gets the same treatment variant across sessions
C) All users get the same treatment
D) Assignment based on user location

<details>
<summary>Answer</summary>

**B) The same user always gets the same treatment variant across sessions**

**Explanation**: Sticky assignment ensures:
- User experience is consistent (user doesn't see different models on different visits)
- Metrics are calculated correctly (same users contribute to same variant)
- Typically implemented with consistent hashing: `hash(user_id + experiment_id) % 100`

**Why it matters**: Without sticky assignment:
- User confusion (recommendations change randomly)
- Metrics contamination (user counted in both control and treatment)
- Invalid statistical assumptions

Implementation: Hash user ID to deterministically assign variant.

</details>

---

### Question 4
**[Multiple Select]** Which of the following are valid business metrics for evaluating an ML model A/B test? (Select all that apply)

A) Click-through rate (CTR)
B) Model training time
C) Conversion rate
D) Revenue per user
E) Code complexity
F) User engagement (time on site)

<details>
<summary>Answer</summary>

**A, C, D, F**

**Explanation**:
- **A**: CTR directly measures user interaction with recommendations
- **B**: INCORRECT - Training time is a development metric, not business metric
- **C**: Conversion rate measures business outcomes (purchases, sign-ups)
- **D**: Revenue is the ultimate business metric
- **E**: INCORRECT - Code complexity is an engineering metric
- **F**: Engagement measures user experience and value

**Business metrics** should be:
- Measurable in production
- Tied to business objectives
- Observable within reasonable time frame
- Actionable (can guide decisions)

</details>

---

### Question 5
What sample size per variant would you need to detect a 10% relative improvement in conversion rate from 5% baseline with 80% power and 95% confidence?

A) ~100
B) ~1,000
C) ~6,200
D) ~100,000

<details>
<summary>Answer</summary>

**C) ~6,200**

**Explanation**: Sample size calculation:
- Baseline rate: p1 = 0.05
- Treatment rate: p2 = 0.05 × 1.10 = 0.055 (10% relative improvement)
- Significance level: α = 0.05 (95% confidence)
- Power: β = 0.80

Formula: `n = (Z_α/2 + Z_β)² × (p1(1-p1) + p2(1-p2)) / (p2 - p1)²`

Where:
- Z_α/2 = 1.96 (for α = 0.05)
- Z_β = 0.84 (for power = 0.80)

Result: n ≈ 6,200 per variant

**Key insight**: Detecting small improvements requires large samples. A 10% relative lift on a 5% baseline is only 0.5% absolute difference, requiring substantial data.

</details>

---

### Question 6
Analyze this A/B test result:

```
Control: 100/1000 conversions (10%)
Treatment: 115/1000 conversions (11.5%)
P-value: 0.08
```

What decision should you make at α = 0.05?

A) Roll out treatment - it shows improvement
B) Do not roll out - result is not statistically significant
C) Immediately stop the test
D) Run the test longer to collect more data

<details>
<summary>Answer</summary>

**B or D are both reasonable**

**Best answer: D) Run the test longer to collect more data**

**Explanation**:
- P-value = 0.08 > α = 0.05, so **not statistically significant**
- Treatment shows 15% relative improvement (promising signal)
- With more data, this could become significant

**Options**:
1. **Don't roll out yet** (B) - Correct from strict statistical perspective
2. **Continue testing** (D) - Best practice to reach significance
3. **Not A** - Don't roll out non-significant results
4. **Not C** - No reason to stop early

**Recommendation**: Continue collecting data. Calculate required sample size:
- For 15% relative lift at 10% baseline
- Likely need ~3,000-4,000 per variant for 80% power
- Current sample is underpowered

</details>

---

## Section 2: Statistical Methods (Questions 7-12)

### Question 7
What is a Type I error in A/B testing?

A) Concluding there's no difference when there actually is (false negative)
B) Concluding there is a difference when there actually isn't (false positive)
C) A coding bug in the test
D) Assigning users incorrectly

<details>
<summary>Answer</summary>

**B) Concluding there is a difference when there actually isn't (false positive)**

**Explanation**: Statistical errors:
- **Type I Error (α)**: False positive - detecting effect that doesn't exist
  - "Crying wolf" - saying treatment is better when it's not
  - Controlled by significance level α (typically 0.05 = 5% false positive rate)
  - Consequence: Roll out model that doesn't actually improve metrics

- **Type II Error (β)**: False negative - missing real effect
  - Saying treatment is no better when it actually is
  - Controlled by statistical power (1 - β, typically 0.80)
  - Consequence: Don't roll out model that would improve metrics

**Balance**: Lowering α (more stringent) increases β (less power). Choose based on risk tolerance.

</details>

---

### Question 8
Why is it problematic to repeatedly check A/B test results and stop as soon as p-value < 0.05?

A) It wastes time
B) It increases false positive rate (Type I error) due to multiple testing
C) It's too conservative
D) There's no problem with this approach

<details>
<summary>Answer</summary>

**B) It increases false positive rate (Type I error) due to multiple testing**

**Explanation**: This is called "peeking" or "optional stopping":

**Problem**:
- Each peek is a hypothesis test
- If you peek 20 times, probability of seeing p < 0.05 by chance is much higher than 5%
- Actual α can inflate to 20-30% instead of 5%

**Example**:
- No real effect exists
- You peek every day for 20 days
- By chance, you'll likely see p < 0.05 at some point
- You incorrectly conclude there's an effect

**Solutions**:
1. **Pre-commit** to sample size and only test once
2. **Sequential testing** with alpha spending (O'Brien-Fleming, Haybittle-Peto)
3. **Bonferroni correction**: Divide α by number of looks

**Best practice**: Calculate required sample size upfront, run test to completion, analyze once.

</details>

---

### Question 9
What is the purpose of calculating a confidence interval in addition to a p-value?

A) To make the report longer
B) To estimate the range of plausible effect sizes, providing more context than just significance
C) To increase sample size requirements
D) Confidence intervals are obsolete

<details>
<summary>Answer</summary>

**B) To estimate the range of plausible effect sizes, providing more context than just significance**

**Explanation**: P-value tells you IF there's an effect, confidence interval tells you HOW MUCH.

**Example**:
```
P-value: 0.01 (significant at α = 0.05)
Confidence interval for lift: [0.1%, 15%]
```

**Insights from CI**:
- Effect is somewhere between 0.1% and 15%
- Wide interval suggests uncertainty about true effect size
- Even lower bound (0.1%) might not be practically significant
- Helps assess business value, not just statistical significance

**Statistical vs Practical Significance**:
- P-value < 0.05: Statistically significant
- CI includes business-relevant effect sizes: Practically significant
- Need both for good decisions

</details>

---

### Question 10
Analyze this code for a Z-test:

```python
def z_test(conv_a, n_a, conv_b, n_b):
    p_a = conv_a / n_a
    p_b = conv_b / n_b
    p_pooled = (conv_a + conv_b) / (n_a + n_b)
    se = (p_pooled * (1 - p_pooled) * (1/n_a + 1/n_b)) ** 0.5
    z = (p_b - p_a) / se
    p_value = 2 * (1 - norm.cdf(abs(z)))
    return p_value
```

Is this implementation correct for a two-tailed test?

A) Yes, this is correct
B) No, should use t-test instead
C) No, pooled proportion formula is wrong
D) No, should be one-tailed test

<details>
<summary>Answer</summary>

**A) Yes, this is correct**

**Explanation**: This implements a proper two-tailed Z-test for proportions:

1. **Calculate proportions**: p_a and p_b ✓
2. **Pooled proportion**: Assumes null hypothesis (no difference) ✓
   - `p_pooled = (successes_a + successes_b) / (n_a + n_b)`
3. **Standard error**: ✓
   - `SE = sqrt(p_pooled * (1 - p_pooled) * (1/n_a + 1/n_b))`
4. **Z-statistic**: Difference divided by standard error ✓
5. **Two-tailed p-value**: `2 * P(Z > |z|)` ✓

**Two-tailed**: Tests if treatment is different (better OR worse) from control
**One-tailed**: Tests if treatment is only better (or only worse)

**When to use**:
- Two-tailed: Default, tests for any difference
- One-tailed: When you only care about one direction (rare)

</details>

---

### Question 11
**[Multiple Select]** Which factors increase the required sample size for an A/B test? (Select all that apply)

A) Smaller minimum detectable effect
B) Higher baseline conversion rate
C) Higher desired statistical power
D) Lower significance level (more stringent)
E) More variance in the metric

<details>
<summary>Answer</summary>

**A, C, D, E**

**Explanation**:
- **A**: CORRECT - Detecting 5% lift requires more samples than detecting 20% lift
- **B**: INCORRECT - Higher baseline typically reduces required sample size (more signal)
- **C**: CORRECT - 90% power requires more samples than 80% power
- **D**: CORRECT - α = 0.01 requires more samples than α = 0.05
- **E**: CORRECT - More variance requires more samples to detect signal

**Sample size formula**: `n ∝ (Z_α + Z_β)² × σ² / δ²`

Where:
- Increases with: smaller δ (effect size), larger Z_α (stringent α), larger Z_β (higher power), larger σ² (variance)

**Practical implications**:
- Detecting small improvements requires large samples
- Lower conversion rates need more samples
- High-variance metrics (revenue) need more samples than binary metrics (clicks)

</details>

---

### Question 12
What is the purpose of a "minimum detectable effect" (MDE) in experiment design?

A) The smallest effect we can measure with infinite data
B) The smallest effect we consider worth detecting, used to calculate required sample size
C) The maximum allowed effect size
D) The average effect size observed

<details>
<summary>Answer</summary>

**B) The smallest effect we consider worth detecting, used to calculate required sample size**

**Explanation**: MDE is a business-driven parameter:

**Definition**: Smallest improvement that would justify deploying the new model

**Example**:
- Current CTR: 10%
- MDE: 10% relative improvement (1% absolute)
- We want to detect if new model achieves ≥ 11% CTR

**Why it matters**:
- Smaller MDE → larger sample size required
- Determines experiment duration
- Balances statistical rigor with business needs

**Setting MDE**:
1. **Business perspective**: What improvement justifies deployment cost/risk?
2. **Statistical perspective**: What can we realistically detect given time/traffic constraints?

**Trade-off**: Setting MDE too small requires impractically large samples. Setting too large misses valuable small improvements.

**Typical values**:
- High-traffic systems: 2-5% relative improvement
- Low-traffic systems: 10-20% relative improvement

</details>

---

## Section 3: Multi-Armed Bandits (Questions 13-18)

### Question 13
What is the key difference between A/B testing and multi-armed bandits (MAB)?

A) A/B tests are faster than bandits
B) A/B tests fix traffic allocation; bandits dynamically allocate more traffic to better variants
C) Bandits require more variants
D) A/B tests are more accurate

<details>
<summary>Answer</summary>

**B) A/B tests fix traffic allocation; bandits dynamically allocate more traffic to better variants**

**Explanation**:

**A/B Testing**:
- Fixed allocation (e.g., 50/50 split)
- Equal traffic to all variants for entire test
- Minimize bias, maximize statistical power
- "Exploration" throughout test

**Multi-Armed Bandits**:
- Dynamic allocation based on observed performance
- More traffic to better-performing variants
- Balances exploration (trying all variants) and exploitation (using best variant)
- Minimizes regret (lost value from using suboptimal variant)

**Trade-off**:
- A/B test: More rigorous statistical inference, but wastes traffic on worse variant
- Bandit: Better performance during test, but harder to calculate statistical significance

**When to use**:
- A/B test: Final decision on model deployment, need clear significance
- Bandit: Ongoing optimization, content recommendation, many variants

</details>

---

### Question 14
What does "regret" mean in the context of multi-armed bandits?

A) Feeling bad about the experiment
B) The cumulative difference between the reward obtained and the reward of always choosing the best arm
C) The error rate of the model
D) The statistical p-value

<details>
<summary>Answer</summary>

**B) The cumulative difference between the reward obtained and the reward of always choosing the best arm**

**Explanation**: Regret quantifies opportunity cost:

**Formula**: `Regret = Σ(R_optimal - R_chosen)`

Where:
- R_optimal: Reward from best arm
- R_chosen: Reward from arm actually chosen

**Example**:
```
True conversion rates:
  Arm A: 10%
  Arm B: 12%  (optimal)
  Arm C: 8%

If you pull: A, A, B, C, B
Regret = (12-10) + (12-10) + (12-12) + (12-8) + (12-12) = 8%
```

**Goal**: Minimize regret by:
1. Quickly identifying best arm (exploration)
2. Pulling it more often (exploitation)

**Bandit algorithms** differ in regret bounds:
- ε-greedy: O(n)
- UCB: O(log n)
- Thompson Sampling: O(log n)

Lower regret = better algorithm.

</details>

---

### Question 15
How does the ε-greedy algorithm work?

A) Always selects the best arm
B) With probability ε, explores (random arm); with probability 1-ε, exploits (best arm)
C) Selects arms based on confidence bounds
D) Uses Bayesian updating

<details>
<summary>Answer</summary>

**B) With probability ε, explores (random arm); with probability 1-ε, exploits (best arm)**

**Explanation**: ε-greedy is simplest bandit algorithm:

**Algorithm**:
```python
if random() < epsilon:
    # Explore: choose random arm
    arm = random_choice(arms)
else:
    # Exploit: choose best arm so far
    arm = argmax(arm.mean_reward for arm in arms)
```

**Parameter ε** (epsilon):
- ε = 0.1: 10% exploration, 90% exploitation
- Higher ε: More exploration, slower convergence, lower regret if arms change
- Lower ε: More exploitation, faster convergence, higher regret if wrong arm chosen early

**Variants**:
- **ε-decreasing**: Start high (explore), decrease over time (exploit)
  - `ε_t = max(ε_min, ε_0 * decay^t)`
- **ε-first**: Explore for first N trials, then exploit

**Pros**: Simple, effective
**Cons**: Arbitrary ε, explores randomly (not intelligently)

</details>

---

### Question 16
What is the Upper Confidence Bound (UCB) algorithm's key principle?

A) Choose arm with highest observed reward
B) Choose arm with highest upper confidence bound (optimism in the face of uncertainty)
C) Choose arms proportionally to their rewards
D) Always explore randomly

<details>
<summary>Answer</summary>

**B) Choose arm with highest upper confidence bound (optimism in the face of uncertainty)**

**Explanation**: UCB selects arm with highest optimistic estimate:

**Formula (UCB1)**:
```
UCB_i = mean_reward_i + c * sqrt(ln(total_pulls) / pulls_i)
```

Where:
- `mean_reward_i`: Average reward from arm i
- `c`: Exploration constant (typically √2)
- `ln(total_pulls) / pulls_i`: Uncertainty term (higher for less-pulled arms)

**Intuition**:
- Well-explored arms: Small confidence bound, score ≈ mean reward
- Under-explored arms: Large confidence bound, optimistic score
- Automatically balances exploration and exploitation

**Example**:
```
Arm A: mean=0.10, pulls=100, UCB=0.10 + 0.05 = 0.15
Arm B: mean=0.08, pulls=10,  UCB=0.08 + 0.15 = 0.23  ← Select (optimistic)
```

**Advantages**:
- No tuning parameter (like ε)
- Theoretical regret guarantees: O(log n)
- Automatically explores uncertain arms

**Disadvantages**:
- Assumes bounded rewards [0,1]
- Can be slow to adapt to changing rewards

</details>

---

### Question 17
Analyze this Thompson Sampling update code:

```python
class ThompsonSampling:
    def __init__(self, n_arms):
        self.alpha = [1] * n_arms  # Successes + 1
        self.beta = [1] * n_arms   # Failures + 1

    def select_arm(self):
        samples = [random.betavariate(self.alpha[i], self.beta[i])
                   for i in range(len(self.alpha))]
        return argmax(samples)

    def update(self, arm, reward):
        if reward == 1:
            self.alpha[arm] += 1
        else:
            self.beta[arm] += 1
```

What distribution is this using, and why?

A) Normal distribution for continuous rewards
B) Beta distribution for modeling probability of success (Bernoulli rewards)
C) Uniform distribution for random exploration
D) Exponential distribution for time-based rewards

<details>
<summary>Answer</summary>

**B) Beta distribution for modeling probability of success (Bernoulli rewards)**

**Explanation**: Thompson Sampling uses Bayesian inference:

**Beta Distribution**:
- Models probability of binary outcome
- Parameters: α (successes), β (failures)
- Beta(1,1) = Uniform(0,1) prior (no knowledge)
- As data accumulates, distribution concentrates around true probability

**Update Rule**:
- Reward = 1 (success): Increment α
- Reward = 0 (failure): Increment β
- Posterior: Beta(α + successes, β + failures)

**Selection**:
- Sample conversion probability from each arm's Beta distribution
- Choose arm with highest sample
- Naturally explores uncertain arms (wide distribution) and exploits promising arms

**Example**:
```
Arm A: Beta(20, 80)  → mean=0.20, uncertain
Arm B: Beta(10, 5)   → mean=0.67, but very uncertain
Arm C: Beta(50, 50)  → mean=0.50, very certain

Samples: A=0.18, B=0.82, C=0.51 → Choose B (high sample despite lower observed mean)
```

**Why it works**: Automatically balances exploration (sample from uncertain distributions) and exploitation (high mean).

</details>

---

### Question 18
**[Multiple Select]** Which scenarios are good use cases for multi-armed bandits instead of traditional A/B tests? (Select all that apply)

A) Final decision on deploying a new model to production
B) Personalizing content recommendations with many variants
C) Optimizing ad creatives with frequent changes
D) Regulatory compliance testing requiring statistical rigor
E) Continuously optimizing email subject lines

<details>
<summary>Answer</summary>

**B, C, E**

**Explanation**:
- **A**: INCORRECT - Final deployment decisions need statistical rigor of A/B test
- **B**: CORRECT - Many variants, ongoing optimization, minimize regret
- **C**: CORRECT - Frequent changes, need to quickly identify best creative
- **D**: INCORRECT - Regulatory requires fixed design and significance testing
- **E**: CORRECT - Continuous optimization, new subject lines added regularly

**A/B Test - Use When**:
- Final go/no-go decision
- Need p-values and statistical significance
- Limited number of variants (2-4)
- Regulatory or compliance requirements
- One-time test

**Bandit - Use When**:
- Many variants (10+)
- Ongoing optimization
- Variants added/removed frequently
- Minimize opportunity cost during test
- Content recommendation, personalization

**Hybrid Approach**:
1. Use bandits for ongoing optimization
2. Periodically run A/B test to validate winner statistically

</details>

---

## Section 4: Progressive Rollout & Canary Deployment (Questions 19-24)

### Question 19
What is a canary deployment in the context of ML models?

A) Testing models on synthetic data
B) Gradually rolling out a new model version to a small subset of users before full deployment
C) Training models on a subset of data
D) Using birds to test model predictions

<details>
<summary>Answer</summary>

**B) Gradually rolling out a new model version to a small subset of users before full deployment**

**Explanation**: Canary deployment minimizes risk:

**Process**:
1. Deploy new model to small % of traffic (e.g., 5%)
2. Monitor metrics (latency, error rate, business KPIs)
3. If metrics are healthy, gradually increase (25% → 50% → 100%)
4. If metrics degrade, rollback immediately

**Name origin**: "Canary in a coal mine" - early warning system

**Example rollout schedule**:
```
Hour 0:  5% canary, 95% baseline
Hour 1:  25% canary, 75% baseline (if healthy)
Hour 2:  50% canary, 50% baseline (if healthy)
Hour 3:  100% canary (if healthy)
```

**Benefits**:
- Limits blast radius of bugs
- Detects issues before full rollout
- Allows quick rollback
- Validates performance on real traffic

**vs A/B test**: Canary is deployment strategy; A/B test is evaluation method. Can combine: run A/B test during canary rollout.

</details>

---

### Question 20
What Kubernetes/Istio resource controls traffic splitting for canary deployments?

A) Deployment
B) Service
C) VirtualService
D) ConfigMap

<details>
<summary>Answer</summary>

**C) VirtualService**

**Explanation**: Istio VirtualService defines traffic routing:

**Example**:
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: model-service
spec:
  hosts:
  - model-service
  http:
  - route:
    - destination:
        host: model-service
        subset: v1      # Baseline
      weight: 95        # 95% traffic
    - destination:
        host: model-service
        subset: v2      # Canary
      weight: 5         # 5% traffic
```

**Istio Components**:
- **VirtualService**: Defines routing rules and traffic splits
- **DestinationRule**: Defines subsets (versions) based on labels
- **ServiceEntry**: External services
- **Gateway**: Ingress/egress

**Traffic control**:
- Adjust weights (0-100, must sum to 100)
- Route based on headers, URI, etc.
- Implement retries, timeouts, circuit breaking

**vs Kubernetes Service**: K8s Service does simple load balancing; Istio enables advanced routing.

</details>

---

### Question 21
What metrics should you monitor during a canary deployment?

A) Only model accuracy
B) Error rate, latency, throughput, business metrics (CTR, conversion)
C) Only infrastructure metrics (CPU, memory)
D) Only cost metrics

<details>
<summary>Answer</summary>

**B) Error rate, latency, throughput, business metrics (CTR, conversion)**

**Explanation**: Comprehensive monitoring across layers:

**1. System Health** (immediate):
- Error rate: 4xx, 5xx responses
- Latency: p50, p95, p99 response time
- Throughput: Requests per second
- Resource utilization: CPU, memory

**2. Model Performance** (short-term):
- Prediction distribution drift
- Model latency (inference time)
- Input validation errors
- Feature availability

**3. Business Metrics** (medium-term):
- Click-through rate (CTR)
- Conversion rate
- Revenue per user
- User engagement

**4. User Experience** (medium-term):
- Session duration
- Bounce rate
- User complaints/support tickets

**Rollback triggers**:
- Error rate > baseline × 1.5
- p95 latency > SLA threshold
- Business metric drop > 10%

**Prometheus queries**:
```promql
# Error rate
sum(rate(http_requests_total{status=~"5.."}[5m])) /
sum(rate(http_requests_total[5m]))

# p95 latency
histogram_quantile(0.95,
  rate(http_request_duration_seconds_bucket[5m]))
```

</details>

---

### Question 22
What is the purpose of automated rollback in canary deployments?

A) To automatically update all models
B) To revert to the baseline version if canary metrics degrade below thresholds
C) To save costs
D) To speed up deployments

<details>
<summary>Answer</summary>

**B) To revert to the baseline version if canary metrics degrade below thresholds**

**Explanation**: Automated rollback minimizes incident duration:

**Rollback triggers**:
```python
def should_rollback(canary_metrics, baseline_metrics):
    # Absolute thresholds
    if canary_metrics['error_rate'] > 0.05:
        return True
    if canary_metrics['p95_latency'] > 200:  # ms
        return True

    # Relative comparison
    if canary_metrics['error_rate'] > baseline_metrics['error_rate'] * 1.5:
        return True
    if canary_metrics['conversion_rate'] < baseline_metrics['conversion_rate'] * 0.9:
        return True

    return False
```

**Rollback action**:
```yaml
# Set canary weight to 0
VirtualService:
  route:
    - destination: v1
      weight: 100
    - destination: v2
      weight: 0
```

**Benefits**:
- Fast incident response (seconds, not minutes)
- Reduces blast radius
- No human intervention needed
- Works 24/7, even outside business hours

**Best practices**:
- Define clear rollback criteria upfront
- Test rollback automation regularly
- Alert team after automatic rollback
- Require manual approval before retry

</details>

---

### Question 23
**[Multiple Select]** What are advantages of progressive rollout over immediate full deployment? (Select all that apply)

A) Faster deployment time
B) Limited blast radius if issues occur
C) Early detection of problems
D) Simpler deployment process
E) Lower risk to users
F) Ability to validate on real traffic

<details>
<summary>Answer</summary>

**B, C, E, F**

**Explanation**:
- **A**: INCORRECT - Progressive rollout is slower (by design)
- **B**: CORRECT - Only 5-10% of users affected initially
- **C**: CORRECT - Problems detected before full rollout
- **D**: INCORRECT - More complex than immediate deployment
- **E**: CORRECT - Gradual exposure minimizes risk
- **F**: CORRECT - Validates on production traffic patterns

**Risk comparison**:
```
Immediate deployment:
  Time to 100%: 5 minutes
  Blast radius: 100% of users
  Detection time: After full rollout

Progressive rollout:
  Time to 100%: 2-4 hours
  Blast radius: 5-10% initially
  Detection time: At each stage (5%, 25%, 50%)
```

**Trade-off**: Slower deployment vs. reduced risk. For ML models where impact is uncertain, progressive rollout is worth the extra time.

</details>

---

### Question 24
Analyze this canary rollout schedule:

```python
stages = [
    {'weight': 5, 'duration_minutes': 30},
    {'weight': 10, 'duration_minutes': 30},
    {'weight': 25, 'duration_minutes': 60},
    {'weight': 50, 'duration_minutes': 60},
    {'weight': 100, 'duration_minutes': 0}
]
```

What is the minimum time to complete rollout if all stages pass?

A) 30 minutes
B) 90 minutes
C) 180 minutes
D) 210 minutes

<details>
<summary>Answer</summary>

**C) 180 minutes (3 hours)**

**Explanation**: Sum of all stage durations:
- 5% for 30 min
- 10% for 30 min
- 25% for 60 min
- 50% for 60 min
- 100% (final, no wait)

Total: 30 + 30 + 60 + 60 = **180 minutes**

**Rollout strategy analysis**:
- **Conservative start**: Small steps (5%, 10%) with short duration
- **Accelerate if healthy**: Larger steps (25%, 50%) with longer monitoring
- **Total blast radius**: Even if 100% deployment fails, only exposed for short time

**Duration considerations**:
- Short duration: Faster rollout, higher risk
- Long duration: More data for validation, slower rollout
- Typical: 30-60 min per stage for well-monitored systems

**Best practice**: Duration should allow sufficient data for statistical significance in metrics comparison.

</details>

---

## Section 5: Experimentation Best Practices (Questions 25-28)

### Question 25
What is the "novelty effect" in A/B testing, and how should you handle it?

A) Users preferring new features simply because they're new
B) Testing too many new features
C) Using new statistical methods
D) Deploying during holidays

<details>
<summary>Answer</summary>

**A) Users preferring new features simply because they're new**

**Explanation**: Novelty effect causes temporary behavior changes:

**Problem**:
- Users interact more with new UI/features initially
- Effect diminishes over time (days to weeks)
- A/B test shows positive lift, but disappears post-launch

**Example**:
```
Week 1: +15% CTR (novelty)
Week 2: +8% CTR (wearing off)
Week 3: +2% CTR (true effect)
```

**Detection**:
- Monitor metrics over time
- Look for decreasing effect size
- Compare early vs. late cohorts

**Mitigation**:
1. **Run longer tests** (3-4 weeks, not 1 week)
2. **Cohort analysis**: Compare users by week
3. **Measure steady-state**: Focus on late-stage metrics
4. **Pre-announcement**: Show feature to control group first (no functionality), then test

**Related**: **Hawthorne effect** - people change behavior when observed

**Recommendation**: For UI changes, run tests for at least 2-3 weeks to see novelty wear off.

</details>

---

### Question 26
**[Multiple Select]** Which of the following can invalidate an A/B test? (Select all that apply)

A) Sample ratio mismatch (unequal group sizes when they should be equal)
B) Starting with large sample size
C) Assignment bugs causing users to switch groups
D) External events (holidays, news) affecting one group differently
E) Using multiple metrics
F) Data pipeline failures affecting only one variant

<details>
<summary>Answer</summary>

**A, C, D, F**

**Explanation**:
- **A**: CORRECT - Sample Ratio Mismatch (SRM) indicates assignment bug
  - Expected: 50/50 split
  - Observed: 60/40 split
  - Cause: Assignment logic bug, bot traffic, etc.

- **B**: INCORRECT - Large samples are good (more power)

- **C**: CORRECT - Users switching groups violates independence
  - Breaks assumption of sticky assignment
  - Contaminates both groups

- **D**: CORRECT - Confounding events
  - Example: Black Friday affects mobile users (treatment) more than desktop (control)
  - Use randomization to distribute events equally

- **E**: INCORRECT - Multiple metrics are fine (with multiple testing correction)

- **F**: CORRECT - Data quality issues
  - Feature computation fails for treatment only
  - Logging broken for one variant
  - Causes false differences

**Validation checklist**:
1. Check sample ratio matches expected
2. Verify assignment is consistent
3. Check for temporal confounders
4. Validate data quality per variant

</details>

---

### Question 27
What is "A/A testing" and why is it useful?

A) Testing two identical models to validate experiment infrastructure
B) Testing on two different datasets
C) Testing twice to increase confidence
D) Testing A against itself

<details>
<summary>Answer</summary>

**A) Testing two identical models to validate experiment infrastructure**

**Explanation**: A/A test validates experiment setup:

**Setup**: Run experiment with control and treatment **both using same model**

**Expected result**: No significant difference (p-value > 0.05)

**What it validates**:
1. **Assignment is random**: Groups are comparable
2. **Metrics calculation**: Same logic for both groups
3. **Data pipeline**: No bugs favoring one group
4. **Sample ratio**: Correct traffic split
5. **False positive rate**: ~5% tests should show p < 0.05 by chance

**Red flags**:
- Significant difference (p < 0.05): Something is broken
- Sample ratio mismatch: Assignment bug
- Consistent bias: Systematic error in one group

**Best practice**:
1. Run A/A test before first A/B test
2. Run periodically to validate infrastructure
3. Use as baseline for false positive rate

**Example finding**:
```
A/A test shows control group has 2% higher conversion
→ Investigate: Mobile users overrepresented in treatment
→ Fix: Update assignment logic to stratify by device
```

</details>

---

### Question 28
You're running an A/B test on a recommendation model. After 1 week, you have:
- Control: 1,000 conversions / 10,000 users (10%)
- Treatment: 1,080 conversions / 10,000 users (10.8%)
- P-value: 0.12

Your manager wants to roll out the treatment because it shows improvement. What should you do?

A) Roll out immediately - there's clear improvement
B) Explain that results are not statistically significant and recommend continuing the test
C) Stop the test and start over
D) Switch everyone to control

<details>
<summary>Answer</summary>

**B) Explain that results are not statistically significant and recommend continuing the test**

**Explanation**: This is a common pressure point in A/B testing:

**Statistical reasoning**:
- P-value = 0.12 > 0.05 → **Not statistically significant**
- 8% relative lift looks promising but could be random variation
- Probability this difference is random: 12%

**Communication to manager**:
```
"The treatment shows a promising 8% improvement, but we cannot
rule out random chance (12% probability).

Recommendation: Continue test for 1 more week to reach
statistical significance. With more data, we'll have confidence
in our decision.

Risk of rolling out now: 12% chance this improvement doesn't
exist, and we waste deployment effort."
```

**Sample size calculation**:
- Current: 10,000 per group
- Needed for 80% power to detect 8% lift: ~15,000 per group
- Action: Run 5 more days

**What NOT to do**:
- ❌ Roll out non-significant results (A)
- ❌ Stop test prematurely (C)
- ❌ Ignore positive signal (D)

**Compromise**: If urgent, consider progressive rollout (canary) while continuing A/B test for validation.

</details>

---

## Scoring Guide

| Score | Grade | Feedback |
|-------|-------|----------|
| 26-28 | A+ | Excellent! Deep understanding of experimentation |
| 23-25 | A | Great job! Strong grasp of A/B testing and bandits |
| 21-22 | B | Good. Review missed topics |
| 18-20 | C | Passing. Revisit key experimentation concepts |
| < 18 | F | Please review lecture notes and retry |

---

## Answer Key Summary

1. B | 2. B | 3. B | 4. A,C,D,F | 5. C
6. D | 7. B | 8. B | 9. B | 10. A
11. A,C,D,E | 12. B | 13. B | 14. B | 15. B
16. B | 17. B | 18. B,C,E | 19. B | 20. C
21. B | 22. B | 23. B,C,E,F | 24. C | 25. A
26. A,C,D,F | 27. A | 28. B

---

## Next Steps

- Review any missed questions
- Complete hands-on exercises
- Implement A/B testing framework
- Experiment with multi-armed bandits
- Set up progressive rollout pipeline
- Explore additional resources in `resources.md`

Good luck!
