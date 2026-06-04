"""
Multi-Armed Bandit Algorithms

Online learning algorithms for dynamic allocation:
- Thompson Sampling
- Upper Confidence Bound (UCB)
- Epsilon-Greedy
- Contextual bandits
"""

from .base import Bandit, BanditResult
from .thompson_sampling import ThompsonSampling
from .ucb import UCB1, UCB1Tuned
from .epsilon_greedy import EpsilonGreedy
from .contextual import LinUCB, ContextualThompsonSampling

__all__ = [
    "Bandit",
    "BanditResult",
    "ThompsonSampling",
    "UCB1",
    "UCB1Tuned",
    "EpsilonGreedy",
    "LinUCB",
    "ContextualThompsonSampling",
]
