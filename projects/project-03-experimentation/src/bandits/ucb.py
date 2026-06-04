"""
Upper Confidence Bound (UCB) Algorithms
"""

import numpy as np
from typing import List, Optional
from .base import Bandit


class UCB1(Bandit):
    """
    UCB1 Algorithm (Auer et al., 2002)

    Selects arm with highest upper confidence bound:
    UCB(arm) = mean_reward + sqrt(2 * ln(t) / n_arm)
    """

    def __init__(self, arms: List[str], c: float = 2.0):
        """
        Initialize UCB1

        Args:
            arms: List of arm identifiers
            c: Exploration parameter (default sqrt(2))

        TODO: Call parent constructor
        TODO: Store exploration parameter
        """
        super().__init__(arms)
        self.c = c

    def select_arm(self, context: Optional[np.ndarray] = None) -> str:
        """
        Select arm with highest UCB

        TODO: For each arm, calculate UCB
        TODO: Return arm with max UCB
        TODO: Use optimistic initialization for unpulled arms
        """
        raise NotImplementedError("UCB1 selection not yet implemented")

    def update(
        self,
        arm: str,
        reward: float,
        context: Optional[np.ndarray] = None
    ) -> None:
        """Update is handled in parent pull() method"""
        pass

    def _ucb_value(self, arm_idx: int) -> float:
        """
        Calculate UCB value for an arm

        TODO: Get empirical mean
        TODO: Calculate exploration bonus
        TODO: Return UCB value
        """
        raise NotImplementedError("UCB calculation not yet implemented")


class UCB1Tuned(Bandit):
    """
    UCB1-Tuned variant with tighter bounds
    """

    def __init__(self, arms: List[str]):
        super().__init__(arms)
        # TODO: Track variance estimates

    def select_arm(self, context: Optional[np.ndarray] = None) -> str:
        """
        Select using variance-aware UCB

        TODO: Calculate UCB with variance term
        TODO: Return best arm
        """
        raise NotImplementedError("UCB1-Tuned not yet implemented")

    def update(
        self,
        arm: str,
        reward: float,
        context: Optional[np.ndarray] = None
    ) -> None:
        """TODO: Update variance estimates"""
        pass


# TODO: Add UCB-V (variance-based UCB)
# TODO: Add KL-UCB
# TODO: Add Bayes-UCB
