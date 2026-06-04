"""
Thompson Sampling

Bayesian approach to multi-armed bandits using posterior sampling.
"""

import numpy as np
from typing import List, Optional
from .base import Bandit


class ThompsonSampling(Bandit):
    """
    Thompson Sampling for Bernoulli bandits

    Uses Beta-Bernoulli conjugate prior.
    Samples from posterior and selects arm with highest sample.
    """

    def __init__(
        self,
        arms: List[str],
        alpha_prior: float = 1.0,
        beta_prior: float = 1.0
    ):
        """
        Initialize Thompson Sampling

        Args:
            arms: List of arm identifiers
            alpha_prior: Prior alpha parameter (Beta distribution)
            beta_prior: Prior beta parameter (Beta distribution)

        TODO: Call parent constructor
        TODO: Initialize Beta parameters for each arm
        """
        super().__init__(arms)
        self.alpha = np.ones(self.n_arms) * alpha_prior
        self.beta = np.ones(self.n_arms) * beta_prior

    def select_arm(self, context: Optional[np.ndarray] = None) -> str:
        """
        Select arm by sampling from posterior

        Returns:
            Selected arm identifier

        TODO: Sample from Beta(alpha, beta) for each arm
        TODO: Return arm with highest sample
        """
        raise NotImplementedError("Thompson Sampling selection not yet implemented")

    def update(
        self,
        arm: str,
        reward: float,
        context: Optional[np.ndarray] = None
    ) -> None:
        """
        Update posterior with observed reward

        Args:
            arm: Pulled arm
            reward: Observed reward (0 or 1)

        TODO: Get arm index
        TODO: Update alpha if reward = 1
        TODO: Update beta if reward = 0
        """
        raise NotImplementedError("Thompson Sampling update not yet implemented")

    def get_posterior_params(self) -> dict:
        """
        Get current posterior parameters

        Returns:
            Dictionary with alpha and beta arrays

        TODO: Return current alpha and beta values
        """
        return {"alpha": self.alpha.copy(), "beta": self.beta.copy()}


class GaussianThompsonSampling(Bandit):
    """
    Thompson Sampling for Gaussian rewards

    Uses Normal-Gamma conjugate prior (simplified to known variance).
    """

    def __init__(
        self,
        arms: List[str],
        mu_prior: float = 0.0,
        sigma_prior: float = 1.0,
        sigma_known: float = 1.0
    ):
        """
        Initialize Gaussian Thompson Sampling

        Args:
            arms: List of arm identifiers
            mu_prior: Prior mean
            sigma_prior: Prior standard deviation
            sigma_known: Known reward standard deviation

        TODO: Call parent constructor
        TODO: Initialize Normal parameters
        """
        super().__init__(arms)
        # TODO: Initialize parameters

    def select_arm(self, context: Optional[np.ndarray] = None) -> str:
        """
        Select arm by sampling from Normal posterior

        TODO: Sample from Normal(mu, sigma) for each arm
        TODO: Return arm with highest sample
        """
        raise NotImplementedError("Gaussian TS selection not yet implemented")

    def update(
        self,
        arm: str,
        reward: float,
        context: Optional[np.ndarray] = None
    ) -> None:
        """
        Update Normal posterior

        TODO: Update mean and variance using Bayesian update
        """
        raise NotImplementedError("Gaussian TS update not yet implemented")


# TODO: Add Thompson Sampling for Poisson rewards
# TODO: Add Thompson Sampling with unknown variance
# TODO: Add optimistic Thompson Sampling
# TODO: Add Thompson Sampling with time-varying rewards
