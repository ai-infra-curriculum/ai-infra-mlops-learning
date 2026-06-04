"""
Base Bandit Interface

Abstract base class and common functionality for all bandit algorithms.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional
import numpy as np


@dataclass
class BanditResult:
    """Result from a bandit experiment"""
    best_arm: str
    arm_selection_counts: Dict[str, int]
    estimated_means: Dict[str, float]
    cumulative_reward: float
    cumulative_regret: float
    total_rounds: int

    # TODO: Add confidence intervals for arm means
    # TODO: Add visualization methods
    # TODO: Add serialization


class Bandit(ABC):
    """
    Abstract base class for multi-armed bandit algorithms

    All bandit implementations should inherit from this class
    and implement the required methods.
    """

    def __init__(self, arms: List[str]):
        """
        Initialize bandit

        Args:
            arms: List of arm identifiers

        TODO: Validate arms list
        TODO: Initialize common state
        """
        self.arms = arms
        self.n_arms = len(arms)
        self.arm_to_idx = {arm: idx for idx, arm in enumerate(arms)}

        # Tracking
        self.pulls = np.zeros(self.n_arms, dtype=int)
        self.rewards = [[] for _ in range(self.n_arms)]
        self.cumulative_reward = 0.0
        self.total_rounds = 0

    @abstractmethod
    def select_arm(self, context: Optional[np.ndarray] = None) -> str:
        """
        Select which arm to pull next

        Args:
            context: Optional context vector for contextual bandits

        Returns:
            Selected arm identifier

        TODO: Implement in subclass
        """
        pass

    @abstractmethod
    def update(
        self,
        arm: str,
        reward: float,
        context: Optional[np.ndarray] = None
    ) -> None:
        """
        Update bandit state after observing reward

        Args:
            arm: Arm that was pulled
            reward: Observed reward
            context: Optional context vector

        TODO: Implement in subclass
        """
        pass

    def pull(
        self,
        arm: str,
        reward: float,
        context: Optional[np.ndarray] = None
    ) -> None:
        """
        Record an arm pull and update state

        Args:
            arm: Arm identifier
            reward: Observed reward
            context: Optional context

        TODO: Validate arm exists
        TODO: Update tracking variables
        TODO: Call update method
        """
        idx = self.arm_to_idx[arm]
        self.pulls[idx] += 1
        self.rewards[idx].append(reward)
        self.cumulative_reward += reward
        self.total_rounds += 1
        self.update(arm, reward, context)

    def get_best_arm(self) -> str:
        """
        Get the current best arm based on estimated means

        Returns:
            Arm identifier with highest estimated mean

        TODO: Calculate mean for each arm
        TODO: Return arm with highest mean
        TODO: Handle ties
        """
        raise NotImplementedError("Get best arm not yet implemented")

    def get_estimated_means(self) -> Dict[str, float]:
        """
        Get estimated mean reward for each arm

        Returns:
            Dictionary of arm -> estimated mean

        TODO: Calculate empirical mean for each arm
        TODO: Handle arms with no pulls
        TODO: Return dictionary
        """
        raise NotImplementedError("Estimated means not yet implemented")

    def get_selection_counts(self) -> Dict[str, int]:
        """
        Get number of times each arm was selected

        Returns:
            Dictionary of arm -> count

        TODO: Convert pulls array to dictionary
        TODO: Return counts
        """
        return {arm: int(self.pulls[idx]) for arm, idx in self.arm_to_idx.items()}

    def compute_regret(self, optimal_arm_mean: float) -> float:
        """
        Calculate cumulative regret

        Regret = (optimal_arm_mean * T) - cumulative_reward

        Args:
            optimal_arm_mean: Mean reward of best arm

        Returns:
            Cumulative regret

        TODO: Calculate regret
        TODO: Update tracking
        TODO: Return regret
        """
        return (optimal_arm_mean * self.total_rounds) - self.cumulative_reward

    def get_result(self, optimal_arm_mean: Optional[float] = None) -> BanditResult:
        """
        Get comprehensive result summary

        Args:
            optimal_arm_mean: Mean of optimal arm for regret calculation

        Returns:
            BanditResult object

        TODO: Calculate all metrics
        TODO: Identify best arm
        TODO: Return BanditResult
        """
        raise NotImplementedError("Get result not yet implemented")

    def reset(self) -> None:
        """
        Reset bandit state

        TODO: Reset all tracking variables
        TODO: Reset algorithm-specific state
        """
        self.pulls = np.zeros(self.n_arms, dtype=int)
        self.rewards = [[] for _ in range(self.n_arms)]
        self.cumulative_reward = 0.0
        self.total_rounds = 0


class BanditSimulator:
    """
    Simulator for evaluating bandit algorithms
    """

    def __init__(
        self,
        bandit: Bandit,
        arm_distributions: Dict[str, callable]
    ):
        """
        Initialize simulator

        Args:
            bandit: Bandit algorithm to evaluate
            arm_distributions: Dictionary of arm -> reward distribution function

        TODO: Validate arms match
        TODO: Store configuration
        """
        self.bandit = bandit
        self.arm_distributions = arm_distributions

        # TODO: Calculate optimal arm
        self.optimal_arm = None
        self.optimal_mean = None

    def run(
        self,
        n_rounds: int,
        track_every: int = 100
    ) -> BanditResult:
        """
        Run simulation for n rounds

        Args:
            n_rounds: Number of rounds to simulate
            track_every: Record metrics every N rounds

        Returns:
            Final bandit result

        TODO: Loop for n_rounds
        TODO: Select arm
        TODO: Sample reward from distribution
        TODO: Update bandit
        TODO: Track metrics periodically
        TODO: Return final result
        """
        raise NotImplementedError("Simulation not yet implemented")

    def compare_algorithms(
        self,
        bandits: List[Bandit],
        n_rounds: int,
        n_replications: int = 100
    ) -> Dict[str, BanditResult]:
        """
        Compare multiple bandit algorithms

        Args:
            bandits: List of bandit algorithms
            n_rounds: Rounds per replication
            n_replications: Number of replications

        Returns:
            Dictionary of algorithm -> aggregated results

        TODO: Run each algorithm multiple times
        TODO: Aggregate results
        TODO: Calculate confidence intervals
        TODO: Return comparison
        """
        raise NotImplementedError("Algorithm comparison not yet implemented")


class BanditVisualizer:
    """
    Visualization utilities for bandit experiments
    """

    @staticmethod
    def plot_regret(results: List[BanditResult], labels: List[str]):
        """
        Plot cumulative regret over time

        Args:
            results: List of bandit results
            labels: Labels for each result

        TODO: Create time series plot
        TODO: Show regret for each algorithm
        TODO: Add confidence bands if available
        TODO: Return plot
        """
        raise NotImplementedError("Regret plotting not yet implemented")

    @staticmethod
    def plot_arm_selection(result: BanditResult):
        """
        Plot arm selection distribution

        Args:
            result: Bandit result to visualize

        TODO: Create bar chart or pie chart
        TODO: Show selection percentage for each arm
        TODO: Highlight best arm
        TODO: Return plot
        """
        raise NotImplementedError("Arm selection plotting not yet implemented")

    @staticmethod
    def plot_estimated_means(
        result: BanditResult,
        true_means: Optional[Dict[str, float]] = None
    ):
        """
        Plot estimated vs true arm means

        Args:
            result: Bandit result
            true_means: Optional true arm means for comparison

        TODO: Create comparison plot
        TODO: Show estimated means with error bars
        TODO: Overlay true means if provided
        TODO: Return plot
        """
        raise NotImplementedError("Mean estimation plotting not yet implemented")


# TODO: Add Thompson Sampling with Gaussian rewards
# TODO: Add batched bandits (select K arms simultaneously)
# TODO: Add adversarial bandits (Exp3)
# TODO: Add dueling bandits
# TODO: Add restless bandits
# TODO: Add sleeping bandits (arms not always available)
# TODO: Add bandit with delayed feedback
# TODO: Add combinatorial bandits
