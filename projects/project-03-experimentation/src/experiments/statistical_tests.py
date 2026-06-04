"""
Statistical Testing Library

Implements frequentist hypothesis tests for A/B testing including:
- Two-sample t-tests
- Proportion tests (z-tests)
- Chi-square tests
- Mann-Whitney U tests
- Multiple comparison corrections
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Optional, List
import numpy as np
from enum import Enum


class TestType(Enum):
    """Types of statistical tests"""
    T_TEST = "t_test"
    PROPORTION_TEST = "proportion_test"
    CHI_SQUARE = "chi_square"
    MANN_WHITNEY = "mann_whitney"


class AlternativeHypothesis(Enum):
    """Alternative hypothesis types"""
    TWO_SIDED = "two_sided"
    GREATER = "greater"
    LESS = "less"


@dataclass
class TestResult:
    """Result from a statistical test"""
    test_type: TestType
    statistic: float
    p_value: float
    degrees_of_freedom: Optional[float]
    confidence_interval: Tuple[float, float]
    effect_size: float
    significant: bool
    alpha: float

    # TODO: Add interpretation text
    # TODO: Add visualization methods
    # TODO: Add export to dict/JSON


class StatisticalTest(ABC):
    """
    Abstract base class for statistical tests

    All statistical tests should inherit from this class and
    implement the required methods.
    """

    @abstractmethod
    def run(
        self,
        control_data: np.ndarray,
        treatment_data: np.ndarray,
        alpha: float = 0.05,
        alternative: AlternativeHypothesis = AlternativeHypothesis.TWO_SIDED
    ) -> TestResult:
        """
        Run the statistical test

        Args:
            control_data: Observations from control group
            treatment_data: Observations from treatment group
            alpha: Significance level
            alternative: Type of alternative hypothesis

        Returns:
            Test result

        TODO: Implement in subclass
        """
        pass

    @abstractmethod
    def compute_confidence_interval(
        self,
        data: np.ndarray,
        confidence: float = 0.95
    ) -> Tuple[float, float]:
        """
        Compute confidence interval

        Args:
            data: Sample data
            confidence: Confidence level (e.g., 0.95 for 95%)

        Returns:
            Lower and upper bounds of confidence interval

        TODO: Implement in subclass
        """
        pass

    def validate_input(
        self,
        control_data: np.ndarray,
        treatment_data: np.ndarray
    ) -> None:
        """
        Validate input data

        Args:
            control_data: Control group data
            treatment_data: Treatment group data

        Raises:
            ValueError: If data is invalid

        TODO: Check for empty arrays
        TODO: Check for NaN/inf values
        TODO: Check minimum sample size
        TODO: Check data type compatibility
        """
        raise NotImplementedError("Input validation not yet implemented")


class TTest(StatisticalTest):
    """
    Two-sample t-test

    Tests whether two independent samples have different means.
    Supports both equal and unequal variance (Welch's t-test).
    """

    def __init__(self, equal_var: bool = False):
        """
        Initialize t-test

        Args:
            equal_var: Assume equal variance (Student's t-test) or not (Welch's)

        TODO: Store configuration
        """
        self.equal_var = equal_var

    def run(
        self,
        control_data: np.ndarray,
        treatment_data: np.ndarray,
        alpha: float = 0.05,
        alternative: AlternativeHypothesis = AlternativeHypothesis.TWO_SIDED
    ) -> TestResult:
        """
        Run two-sample t-test

        TODO: Validate input data
        TODO: Calculate sample statistics (mean, variance, n)
        TODO: Compute t-statistic
        TODO: Calculate degrees of freedom (Welch-Satterthwaite if unequal var)
        TODO: Compute p-value from t-distribution
        TODO: Calculate confidence interval for difference in means
        TODO: Compute effect size (Cohen's d)
        TODO: Determine significance
        TODO: Return TestResult
        """
        raise NotImplementedError("T-test not yet implemented")

    def compute_confidence_interval(
        self,
        data: np.ndarray,
        confidence: float = 0.95
    ) -> Tuple[float, float]:
        """
        Compute confidence interval for mean

        TODO: Calculate sample mean and standard error
        TODO: Get critical value from t-distribution
        TODO: Compute margin of error
        TODO: Return (lower, upper) bounds
        """
        raise NotImplementedError("CI computation not yet implemented")

    def compute_effect_size(
        self,
        control_data: np.ndarray,
        treatment_data: np.ndarray
    ) -> float:
        """
        Compute Cohen's d effect size

        Cohen's d = (mean_treatment - mean_control) / pooled_std

        TODO: Calculate means
        TODO: Calculate pooled standard deviation
        TODO: Compute and return Cohen's d
        """
        raise NotImplementedError("Effect size computation not yet implemented")

    def compute_degrees_of_freedom(
        self,
        n1: int,
        n2: int,
        var1: float,
        var2: float
    ) -> float:
        """
        Compute degrees of freedom

        Uses Welch-Satterthwaite equation for unequal variances,
        or n1 + n2 - 2 for equal variances.

        TODO: Implement Welch-Satterthwaite formula
        TODO: Handle equal variance case
        """
        raise NotImplementedError("DF computation not yet implemented")


class ProportionTest(StatisticalTest):
    """
    Two-sample proportion test (z-test)

    Tests whether two proportions are significantly different.
    Commonly used for conversion rate testing.
    """

    def run(
        self,
        control_data: np.ndarray,
        treatment_data: np.ndarray,
        alpha: float = 0.05,
        alternative: AlternativeHypothesis = AlternativeHypothesis.TWO_SIDED
    ) -> TestResult:
        """
        Run two-proportion z-test

        Args:
            control_data: Binary array (0/1) for control
            treatment_data: Binary array (0/1) for treatment
            alpha: Significance level
            alternative: Type of alternative hypothesis

        Returns:
            Test result

        TODO: Validate data is binary (0/1)
        TODO: Calculate proportions and sample sizes
        TODO: Compute pooled proportion
        TODO: Calculate standard error
        TODO: Compute z-statistic
        TODO: Calculate p-value from normal distribution
        TODO: Compute confidence interval for difference
        TODO: Calculate effect size (relative lift)
        TODO: Return TestResult
        """
        raise NotImplementedError("Proportion test not yet implemented")

    def compute_confidence_interval(
        self,
        data: np.ndarray,
        confidence: float = 0.95
    ) -> Tuple[float, float]:
        """
        Compute confidence interval for proportion

        Uses normal approximation or Wilson score interval

        TODO: Calculate sample proportion
        TODO: Choose method (normal approximation vs Wilson)
        TODO: Compute interval bounds
        TODO: Return (lower, upper)
        """
        raise NotImplementedError("Proportion CI not yet implemented")

    def compute_pooled_proportion(
        self,
        successes1: int,
        n1: int,
        successes2: int,
        n2: int
    ) -> float:
        """
        Compute pooled proportion for null hypothesis

        pooled_p = (successes1 + successes2) / (n1 + n2)

        TODO: Implement pooled proportion calculation
        """
        raise NotImplementedError("Pooled proportion not yet implemented")

    def compute_relative_lift(
        self,
        control_proportion: float,
        treatment_proportion: float
    ) -> float:
        """
        Compute relative lift (effect size for proportions)

        relative_lift = (treatment - control) / control

        TODO: Calculate and return relative lift
        TODO: Handle zero control proportion case
        """
        raise NotImplementedError("Relative lift not yet implemented")


class ChiSquareTest(StatisticalTest):
    """
    Chi-square test of independence

    Tests whether two categorical variables are independent.
    """

    def run(
        self,
        control_data: np.ndarray,
        treatment_data: np.ndarray,
        alpha: float = 0.05,
        alternative: AlternativeHypothesis = AlternativeHypothesis.TWO_SIDED
    ) -> TestResult:
        """
        Run chi-square test

        TODO: Create contingency table
        TODO: Calculate expected frequencies
        TODO: Compute chi-square statistic
        TODO: Calculate degrees of freedom
        TODO: Compute p-value
        TODO: Calculate effect size (Cramér's V)
        TODO: Return TestResult
        """
        raise NotImplementedError("Chi-square test not yet implemented")

    def compute_confidence_interval(
        self,
        data: np.ndarray,
        confidence: float = 0.95
    ) -> Tuple[float, float]:
        """
        Confidence intervals not directly applicable to chi-square

        TODO: Consider alternatives (e.g., CI for proportions)
        """
        raise NotImplementedError("CI not applicable for chi-square")

    def compute_cramers_v(self, chi2: float, n: int, min_dim: int) -> float:
        """
        Compute Cramér's V effect size

        V = sqrt(chi2 / (n * (min_dim - 1)))

        TODO: Implement Cramér's V calculation
        """
        raise NotImplementedError("Cramér's V not yet implemented")


class MannWhitneyU(StatisticalTest):
    """
    Mann-Whitney U test (Wilcoxon rank-sum test)

    Non-parametric test for comparing two independent samples.
    Alternative to t-test when normality assumption is violated.
    """

    def run(
        self,
        control_data: np.ndarray,
        treatment_data: np.ndarray,
        alpha: float = 0.05,
        alternative: AlternativeHypothesis = AlternativeHypothesis.TWO_SIDED
    ) -> TestResult:
        """
        Run Mann-Whitney U test

        TODO: Combine and rank all observations
        TODO: Calculate rank sums
        TODO: Compute U statistic
        TODO: Calculate p-value (normal approximation for large n)
        TODO: Calculate effect size (rank-biserial correlation)
        TODO: Return TestResult
        """
        raise NotImplementedError("Mann-Whitney U test not yet implemented")

    def compute_confidence_interval(
        self,
        data: np.ndarray,
        confidence: float = 0.95
    ) -> Tuple[float, float]:
        """
        Compute confidence interval for median

        TODO: Use bootstrap or exact method
        TODO: Return (lower, upper) bounds
        """
        raise NotImplementedError("Median CI not yet implemented")


class MultipleTestingCorrection:
    """
    Methods for controlling Type I error in multiple testing
    """

    @staticmethod
    def bonferroni(p_values: List[float], alpha: float = 0.05) -> List[bool]:
        """
        Bonferroni correction for multiple comparisons

        Adjusted alpha = alpha / n_tests

        Args:
            p_values: List of p-values from tests
            alpha: Family-wise error rate

        Returns:
            List of booleans indicating significance

        TODO: Calculate adjusted alpha
        TODO: Compare each p-value to adjusted alpha
        TODO: Return significance decisions
        """
        raise NotImplementedError("Bonferroni correction not yet implemented")

    @staticmethod
    def benjamini_hochberg(
        p_values: List[float],
        alpha: float = 0.05
    ) -> List[bool]:
        """
        Benjamini-Hochberg FDR control

        Controls false discovery rate instead of family-wise error rate.

        Args:
            p_values: List of p-values from tests
            alpha: False discovery rate

        Returns:
            List of booleans indicating significance

        TODO: Sort p-values
        TODO: Calculate BH critical values
        TODO: Find largest i where p(i) <= (i/m) * alpha
        TODO: Reject all hypotheses up to i
        TODO: Return significance decisions
        """
        raise NotImplementedError("BH procedure not yet implemented")

    @staticmethod
    def holm_bonferroni(
        p_values: List[float],
        alpha: float = 0.05
    ) -> List[bool]:
        """
        Holm-Bonferroni sequential correction

        More powerful than standard Bonferroni.

        Args:
            p_values: List of p-values from tests
            alpha: Family-wise error rate

        Returns:
            List of booleans indicating significance

        TODO: Sort p-values
        TODO: Test sequentially with adjusted alphas
        TODO: Stop at first non-rejection
        TODO: Return significance decisions
        """
        raise NotImplementedError("Holm-Bonferroni not yet implemented")


class PowerAnalysis:
    """
    Statistical power and sample size calculations
    """

    @staticmethod
    def calculate_sample_size_ttest(
        effect_size: float,
        alpha: float = 0.05,
        power: float = 0.80,
        alternative: AlternativeHypothesis = AlternativeHypothesis.TWO_SIDED
    ) -> int:
        """
        Calculate required sample size for t-test

        Args:
            effect_size: Cohen's d
            alpha: Significance level
            power: Desired statistical power
            alternative: Type of test

        Returns:
            Required sample size per group

        TODO: Get critical values from distributions
        TODO: Use power formula to solve for n
        TODO: Round up to nearest integer
        TODO: Add safety margin
        """
        raise NotImplementedError("Sample size calculation not yet implemented")

    @staticmethod
    def calculate_sample_size_proportion(
        p1: float,
        p2: float,
        alpha: float = 0.05,
        power: float = 0.80,
        alternative: AlternativeHypothesis = AlternativeHypothesis.TWO_SIDED
    ) -> int:
        """
        Calculate required sample size for proportion test

        Args:
            p1: Control proportion
            p2: Treatment proportion
            alpha: Significance level
            power: Desired statistical power
            alternative: Type of test

        Returns:
            Required sample size per group

        TODO: Calculate pooled proportion
        TODO: Calculate effect size
        TODO: Use power formula
        TODO: Return sample size
        """
        raise NotImplementedError("Proportion sample size not yet implemented")

    @staticmethod
    def calculate_power(
        n: int,
        effect_size: float,
        alpha: float = 0.05,
        alternative: AlternativeHypothesis = AlternativeHypothesis.TWO_SIDED
    ) -> float:
        """
        Calculate statistical power given sample size

        Args:
            n: Sample size per group
            effect_size: Effect size (Cohen's d or similar)
            alpha: Significance level
            alternative: Type of test

        Returns:
            Statistical power (0 to 1)

        TODO: Calculate non-centrality parameter
        TODO: Get critical values
        TODO: Calculate power from distributions
        TODO: Return power
        """
        raise NotImplementedError("Power calculation not yet implemented")

    @staticmethod
    def calculate_minimum_detectable_effect(
        n: int,
        alpha: float = 0.05,
        power: float = 0.80,
        alternative: AlternativeHypothesis = AlternativeHypothesis.TWO_SIDED
    ) -> float:
        """
        Calculate minimum detectable effect size

        Args:
            n: Sample size per group
            alpha: Significance level
            power: Desired statistical power
            alternative: Type of test

        Returns:
            Minimum detectable effect size

        TODO: Get critical values
        TODO: Solve power equation for effect size
        TODO: Return MDE
        """
        raise NotImplementedError("MDE calculation not yet implemented")


# TODO: Add sequential testing support
# TODO: Add CUSUM test for change detection
# TODO: Add variance reduction techniques (CUPED)
# TODO: Add stratified analysis
# TODO: Add subgroup analysis with interaction tests
# TODO: Add bootstrap methods for non-parametric inference
# TODO: Add permutation tests
# TODO: Add meta-analysis methods for combining experiments
