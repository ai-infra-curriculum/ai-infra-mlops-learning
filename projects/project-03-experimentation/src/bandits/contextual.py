"""
Contextual Bandit Algorithms
"""

import numpy as np
from typing import List, Optional
from .base import Bandit


class LinUCB(Bandit):
    """
    Linear Upper Confidence Bound (contextual bandit)

    Models reward as linear function of context.
    """

    def __init__(
        self,
        arms: List[str],
        context_dim: int,
        alpha: float = 1.0
    ):
        """
        Initialize LinUCB

        Args:
            arms: List of arm identifiers
            context_dim: Dimension of context vector
            alpha: Exploration parameter

        TODO: Call parent constructor
        TODO: Initialize A matrices (d x d) for each arm
        TODO: Initialize b vectors (d x 1) for each arm
        """
        super().__init__(arms)
        self.d = context_dim
        self.alpha = alpha

        # TODO: Initialize parameters
        self.A = None  # [np.identity(d) for _ in range(n_arms)]
        self.b = None  # [np.zeros(d) for _ in range(n_arms)]

    def select_arm(self, context: np.ndarray) -> str:
        """
        Select arm with highest UCB given context

        Args:
            context: Context vector (d-dimensional)

        TODO: For each arm, compute theta = A^-1 * b
        TODO: Compute UCB = theta^T * context + alpha * sqrt(context^T * A^-1 * context)
        TODO: Return arm with highest UCB
        """
        raise NotImplementedError("LinUCB selection not yet implemented")

    def update(self, arm: str, reward: float, context: np.ndarray) -> None:
        """
        Update model parameters

        Args:
            arm: Pulled arm
            reward: Observed reward
            context: Context vector

        TODO: Get arm index
        TODO: Update A: A += context * context^T
        TODO: Update b: b += reward * context
        """
        raise NotImplementedError("LinUCB update not yet implemented")


class ContextualThompsonSampling(Bandit):
    """
    Thompson Sampling for contextual bandits

    Uses Bayesian linear regression.
    """

    def __init__(
        self,
        arms: List[str],
        context_dim: int,
        v: float = 1.0
    ):
        """
        Initialize Contextual Thompson Sampling

        Args:
            arms: List of arm identifiers
            context_dim: Context dimension
            v: Noise variance

        TODO: Initialize Bayesian linear regression parameters
        """
        super().__init__(arms)
        self.d = context_dim
        self.v = v
        # TODO: Initialize parameters

    def select_arm(self, context: np.ndarray) -> str:
        """
        Sample weights and select best arm

        TODO: Sample theta from posterior for each arm
        TODO: Compute expected reward for each arm
        TODO: Return arm with highest expected reward
        """
        raise NotImplementedError("Contextual TS selection not yet implemented")

    def update(self, arm: str, reward: float, context: np.ndarray) -> None:
        """
        Update posterior with observation

        TODO: Update Bayesian linear regression parameters
        """
        raise NotImplementedError("Contextual TS update not yet implemented")


# TODO: Add neural contextual bandits
# TODO: Add neural Thompson Sampling
# TODO: Add contextual UCB with kernels
