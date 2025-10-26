# Module 05: Experimentation and A/B Testing

**Role**: MLOps Engineer (Level 2.5B)
**Duration**: 30 hours
**Prerequisites**:
- Completed Module 04: Data Quality
- Statistics (hypothesis testing, confidence intervals)
- Probability theory basics
- Understanding of experimental design
- Python scientific computing (scipy, statsmodels)

## Module Overview

This module teaches you how to design, execute, and analyze ML experiments using A/B testing, multi-armed bandits, and other experimental frameworks. You'll learn to make statistically rigorous decisions about model deployments and optimizations.

## Learning Objectives

By the end of this module, you will be able to:

1. **Design** statistically rigorous A/B tests for ML models
2. **Calculate** required sample sizes and test duration
3. **Implement** multi-armed bandit algorithms
4. **Analyze** experiment results with proper statistical tests
5. **Build** progressive rollout automation
6. **Configure** traffic splitting with Istio
7. **Detect** and handle confounding variables
8. **Make** data-driven deployment decisions

## Topics Covered

### 1. Experimentation Fundamentals (5 hours)
- Why A/B testing for ML is different
- Experimental design principles
- Randomization and control groups
- Statistical power and significance
- Common pitfalls and biases

### 2. A/B Testing Framework (7 hours)
- Hypothesis formulation
- Sample size calculation
- Test duration planning
- Statistical tests (t-test, chi-square, Mann-Whitney)
- Multiple testing correction
- Sequential testing

### 3. Multi-Armed Bandits (6 hours)
- Exploration vs exploitation
- Epsilon-greedy algorithms
- Thompson sampling
- Upper Confidence Bound (UCB)
- Contextual bandits
- When to use bandits vs A/B tests

### 4. Progressive Rollout (5 hours)
- Canary analysis
- Staged rollout strategies
- Automated decision-making
- Risk mitigation
- Rollback automation

### 5. Traffic Management (4 hours)
- Traffic splitting with Istio
- Session stickiness
- Geographic routing
- Load balancing considerations
- Infrastructure requirements

### 6. Experiment Analysis (3 hours)
- Statistical significance vs practical significance
- Confidence intervals
- Effect size calculation
- Segment analysis
- Reporting and visualization

## Files in This Module

- `lecture-notes.md` - Comprehensive 5,500-word lecture
- `exercises/` - 8 experimentation exercises
- `resources.md` - Experimentation frameworks and tools
- `quizzes/quiz-05-experimentation.md` - 30-question assessment

## Exercises

1. **Exercise 01**: Design A/B Test Experiment (90 min)
2. **Exercise 02**: Calculate Sample Sizes (60 min)
3. **Exercise 03**: Implement Statistical Tests (90 min)
4. **Exercise 04**: Build Multi-Armed Bandit (120 min)
5. **Exercise 05**: Configure Istio Traffic Splitting (90 min)
6. **Exercise 06**: Implement Progressive Rollout (120 min)
7. **Exercise 07**: Analyze Experiment Results (90 min)
8. **Exercise 08**: Build Complete Experiment Framework (180 min)

**Total Exercise Time**: 14 hours

## Key Takeaways

- ✅ A/B testing provides statistical rigor for decisions
- ✅ Sample size calculation prevents underpowered tests
- ✅ Multi-armed bandits minimize opportunity cost
- ✅ Progressive rollout reduces deployment risk
- ✅ Proper analysis prevents false conclusions
- ✅ Automation enables continuous experimentation
- ✅ Statistical vs practical significance matters

## Project Connection

This module directly supports **Project 04: Automated Retraining & A/B Testing** where you'll build:
- Statistical A/B testing framework
- Multi-armed bandit implementation
- Progressive rollout (10% → 25% → 50% → 100%)
- Istio traffic management
- Automated decision engine
- Experiment tracking and analysis

## Assessment

- **Quiz**: 30 questions on experimentation and testing (45 minutes)
- **Passing Score**: 80% (24/30 questions)
- **Practical**: Design and analyze A/B test (Exercise 08)

## Real-World Context

**Industry Applications**:
- **Netflix**: A/B tests for recommendation algorithms
- **Booking.com**: 1000+ experiments running concurrently
- **Microsoft**: Multi-armed bandits for Bing ranking
- **LinkedIn**: Progressive rollouts for model updates

**Common Tools**:
- **Frameworks**: Optimizely, LaunchDarkly, GrowthBook
- **Analysis**: scipy, statsmodels, causal-inference
- **Traffic**: Istio, Envoy, NGINX
- **Tracking**: Mixpanel, Amplitude, custom solutions

## Next Module

**Module 06: Automation and Orchestration** - Learn to build automated ML workflows

---

**Estimated Completion Time**: 30 hours (16 hours content + 14 hours exercises)
