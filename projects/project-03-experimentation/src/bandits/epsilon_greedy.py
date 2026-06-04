"""
Epsilon-Greedy Bandit Algorithm
"""

import numpy as np
from typing import List, Optional, Callable
from .base import Bandit


class EpsilonGreedy(Bandit):
    """
    Epsilon-Greedy Algorithm

    With probability epsilon: explore (random arm)
    With probability 1-epsilon: exploit (best arm)
    """

    def __init__(
        self,
        arms: List[str],
        epsilon: float = 0.1,
        decay: Optional[Callable] = None
    ):
        """
        Initialize Epsilon-Greedy

        Args:
            arms: List of arm identifiers
            epsilon: Exploration probability
            decay: Optional decay function for epsilon

        TODO: Call parent constructor
        TODO: Store epsilon and decay function
        """
        super().__init__(arms)
        self.epsilon_init = epsilon
        self.epsilon = epsilon
        self.decay = decay

    def select_arm(self, context: Optional[np.ndarray] = None) -> str:
        """
        Select arm using epsilon-greedy strategy

        TODO: Generate random number
        TODO: If < epsilon, select random arm
        TODO: Else select arm with highest mean
        TODO: Update epsilon if decay function provided
        """
        raise NotImplementedError("Epsilon-greedy selection not yet implemented")

    def update(
        self,
        arm: str,
        reward: float,
        context: Optional[np.ndarray] = None
    ) -> None:
        """Update handled in parent pull()"""
        pass

    def _update_epsilon(self):
        """
        Update epsilon using decay function

        TODO: Apply decay function if provided
        """
        if self.decay:
            self.epsilon = self.decay(self.total_rounds, self.epsilon_init)


# Common decay schedules
def linear_decay(t: int, epsilon_0: float, decay_rate: float = 0.001) -> float:
    """TODO: Implement linear decay"""
    raise NotImplementedError()


def exponential_decay(t: int, epsilon_0: float, decay_rate: float = 0.001) -> float:
    """TODO: Implement exponential decay"""
    raise NotImplementedError()


# TODO: Add optimistic initialization variant
# TODO: Add epsilon-decreasing
