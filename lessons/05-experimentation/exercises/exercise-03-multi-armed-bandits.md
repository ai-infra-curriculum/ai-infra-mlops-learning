## Exercise 3: Multi-Armed Bandits (90 minutes)

**Objective**: Implement multi-armed bandit algorithms (ε-greedy, UCB, Thompson Sampling) for adaptive experimentation.

### Background

Traditional A/B tests waste traffic on inferior variants. Multi-armed bandits (MAB) dynamically allocate more traffic to better-performing variants while exploring alternatives.

### Tasks

1. **Implement ε-greedy algorithm**
2. **Implement Upper Confidence Bound (UCB)**
3. **Implement Thompson Sampling**
4. **Compare bandit strategies**
5. **Integrate with ML model serving**

### Starter Code

```python
# bandits/base.py
"""Base classes for multi-armed bandit algorithms."""

from abc import ABC, abstractmethod
from typing import List, Dict
import numpy as np

class Arm:
    """Represents a bandit arm (variant/model)."""

    def __init__(self, arm_id: str, model_uri: str):
        """
        Initialize arm.

        Args:
            arm_id: Unique identifier
            model_uri: Model URI for this arm
        """
        self.arm_id = arm_id
        self.model_uri = model_uri
        self.pulls = 0
        self.rewards = 0.0
        self.reward_history = []

    def update(self, reward: float):
        """
        Update arm statistics with new reward.

        Args:
            reward: Reward value (0 or 1 for binary, any float for continuous)
        """
        self.pulls += 1
        self.rewards += reward
        self.reward_history.append(reward)

    @property
    def mean_reward(self) -> float:
        """Calculate mean reward."""
        return self.rewards / self.pulls if self.pulls > 0 else 0.0


class BanditAlgorithm(ABC):
    """Abstract base class for bandit algorithms."""

    def __init__(self, arms: List[Arm]):
        """
        Initialize bandit.

        Args:
            arms: List of arms
        """
        self.arms = arms
        self.total_pulls = 0

    @abstractmethod
    def select_arm(self) -> Arm:
        """
        Select an arm to pull.

        Returns:
            Selected arm
        """
        pass

    def update(self, arm_id: str, reward: float):
        """
        Update arm with reward.

        Args:
            arm_id: Arm that was pulled
            reward: Observed reward
        """
        arm = next(a for a in self.arms if a.arm_id == arm_id)
        arm.update(reward)
        self.total_pulls += 1

    def get_stats(self) -> Dict:
        """Get current statistics."""
        return {
            arm.arm_id: {
                'pulls': arm.pulls,
                'mean_reward': arm.mean_reward,
                'total_reward': arm.rewards
            }
            for arm in self.arms
        }
```

```python
# bandits/epsilon_greedy.py
"""Epsilon-greedy bandit algorithm."""

import random
from typing import List
from bandits.base import BanditAlgorithm, Arm

class EpsilonGreedy(BanditAlgorithm):
    """Epsilon-greedy exploration strategy."""

    def __init__(self, arms: List[Arm], epsilon: float = 0.1):
        """
        Initialize epsilon-greedy bandit.

        Args:
            arms: List of arms
            epsilon: Exploration probability (0.1 = 10% explore, 90% exploit)
        """
        super().__init__(arms)
        self.epsilon = epsilon

    def select_arm(self) -> Arm:
        """
        Select arm using epsilon-greedy strategy.

        Returns:
            Selected arm
        """
        # TODO: With probability epsilon, explore (random selection)
        if random.random() < self.epsilon:
            return random.choice(self.arms)

        # TODO: Otherwise, exploit (select best arm)
        # Handle ties by random selection
        best_reward = max(arm.mean_reward for arm in self.arms)
        best_arms = [arm for arm in self.arms if arm.mean_reward == best_reward]
        return random.choice(best_arms)


class EpsilonDecreasing(BanditAlgorithm):
    """Epsilon-greedy with decreasing exploration rate."""

    def __init__(self, arms: List[Arm], epsilon_start: float = 1.0, epsilon_min: float = 0.01, decay_rate: float = 0.99):
        """
        Initialize with decaying epsilon.

        Args:
            arms: List of arms
            epsilon_start: Initial exploration rate
            epsilon_min: Minimum exploration rate
            decay_rate: Decay factor per pull
        """
        super().__init__(arms)
        self.epsilon = epsilon_start
        self.epsilon_min = epsilon_min
        self.decay_rate = decay_rate

    def select_arm(self) -> Arm:
        """Select arm with current epsilon."""
        # TODO: Implement selection
        if random.random() < self.epsilon:
            selected = random.choice(self.arms)
        else:
            best_reward = max(arm.mean_reward for arm in self.arms)
            best_arms = [arm for arm in self.arms if arm.mean_reward == best_reward]
            selected = random.choice(best_arms)

        # TODO: Decay epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon * self.decay_rate)

        return selected
```

```python
# bandits/ucb.py
"""Upper Confidence Bound (UCB) bandit algorithm."""

import math
from typing import List
from bandits.base import BanditAlgorithm, Arm

class UCB1(BanditAlgorithm):
    """UCB1 algorithm for bandit problems."""

    def __init__(self, arms: List[Arm], c: float = math.sqrt(2)):
        """
        Initialize UCB1.

        Args:
            arms: List of arms
            c: Exploration constant (default: sqrt(2))
        """
        super().__init__(arms)
        self.c = c

    def select_arm(self) -> Arm:
        """
        Select arm using UCB1 strategy.

        Returns:
            Selected arm
        """
        # TODO: If any arm hasn't been pulled, pull it
        for arm in self.arms:
            if arm.pulls == 0:
                return arm

        # TODO: Calculate UCB for each arm
        # UCB = mean_reward + c * sqrt(ln(total_pulls) / arm_pulls)
        ucb_values = []
        for arm in self.arms:
            exploration_bonus = self.c * math.sqrt(math.log(self.total_pulls) / arm.pulls)
            ucb = arm.mean_reward + exploration_bonus
            ucb_values.append((arm, ucb))

        # TODO: Select arm with highest UCB
        best_arm = max(ucb_values, key=lambda x: x[1])[0]
        return best_arm
```

```python
# bandits/thompson_sampling.py
"""Thompson Sampling bandit algorithm."""

import random
from typing import List
from bandits.base import BanditAlgorithm, Arm

class ThompsonSampling(BanditAlgorithm):
    """Thompson Sampling with Beta distribution (for binary rewards)."""

    def __init__(self, arms: List[Arm]):
        """
        Initialize Thompson Sampling.

        Args:
            arms: List of arms
        """
        super().__init__(arms)
        # Beta distribution parameters (successes, failures)
        self.alpha = {arm.arm_id: 1 for arm in arms}  # Prior: Beta(1,1) = Uniform(0,1)
        self.beta = {arm.arm_id: 1 for arm in arms}

    def select_arm(self) -> Arm:
        """
        Select arm using Thompson Sampling.

        Returns:
            Selected arm
        """
        # TODO: Sample from Beta distribution for each arm
        samples = {}
        for arm in self.arms:
            # Sample from Beta(alpha, beta)
            samples[arm.arm_id] = random.betavariate(
                self.alpha[arm.arm_id],
                self.beta[arm.arm_id]
            )

        # TODO: Select arm with highest sample
        best_arm_id = max(samples, key=samples.get)
        return next(arm for arm in self.arms if arm.arm_id == best_arm_id)

    def update(self, arm_id: str, reward: float):
        """
        Update Beta distribution parameters.

        Args:
            arm_id: Arm that was pulled
            reward: Observed reward (0 or 1 for binary)
        """
        super().update(arm_id, reward)

        # TODO: Update Beta parameters
        # If reward = 1 (success), increment alpha
        # If reward = 0 (failure), increment beta
        if reward > 0:
            self.alpha[arm_id] += 1
        else:
            self.beta[arm_id] += 1
```

```python
# bandits/simulation.py
"""Simulate and compare bandit algorithms."""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict
from bandits.base import Arm, BanditAlgorithm
from bandits.epsilon_greedy import EpsilonGreedy, EpsilonDecreasing
from bandits.ucb import UCB1
from bandits.thompson_sampling import ThompsonSampling

class BanditSimulation:
    """Simulate bandit algorithms for comparison."""

    def __init__(self, true_probabilities: List[float]):
        """
        Initialize simulation.

        Args:
            true_probabilities: True conversion probability for each arm
        """
        self.true_probabilities = true_probabilities
        self.n_arms = len(true_probabilities)

    def simulate_bandit(
        self,
        algorithm: BanditAlgorithm,
        n_iterations: int = 10000
    ) -> Dict:
        """
        Simulate bandit algorithm.

        Args:
            algorithm: Bandit algorithm to simulate
            n_iterations: Number of iterations

        Returns:
            Dictionary with simulation results
        """
        rewards = []
        regrets = []
        optimal_arm_idx = np.argmax(self.true_probabilities)
        cumulative_regret = 0

        for i in range(n_iterations):
            # TODO: Select arm
            arm = algorithm.select_arm()
            arm_idx = int(arm.arm_id.split('_')[1])

            # TODO: Simulate reward (Bernoulli trial)
            reward = 1 if np.random.random() < self.true_probabilities[arm_idx] else 0

            # TODO: Update algorithm
            algorithm.update(arm.arm_id, reward)

            # TODO: Track metrics
            rewards.append(reward)
            regret = self.true_probabilities[optimal_arm_idx] - self.true_probabilities[arm_idx]
            cumulative_regret += regret
            regrets.append(cumulative_regret)

        return {
            'rewards': rewards,
            'cumulative_rewards': np.cumsum(rewards),
            'regrets': regrets,
            'final_stats': algorithm.get_stats()
        }

    def compare_algorithms(self, n_iterations: int = 10000):
        """
        Compare multiple bandit algorithms.

        Args:
            n_iterations: Number of iterations
        """
        # TODO: Create arms
        arms_eps = [Arm(f"arm_{i}", f"model_{i}") for i in range(self.n_arms)]
        arms_ucb = [Arm(f"arm_{i}", f"model_{i}") for i in range(self.n_arms)]
        arms_ts = [Arm(f"arm_{i}", f"model_{i}") for i in range(self.n_arms)]

        # TODO: Initialize algorithms
        algorithms = {
            'Epsilon-Greedy (0.1)': EpsilonGreedy(arms_eps, epsilon=0.1),
            'UCB1': UCB1(arms_ucb),
            'Thompson Sampling': ThompsonSampling(arms_ts)
        }

        # TODO: Run simulations
        results = {}
        for name, algo in algorithms.items():
            print(f"Running {name}...")
            results[name] = self.simulate_bandit(algo, n_iterations)

        # TODO: Plot comparison
        self._plot_comparison(results, n_iterations)

        return results

    def _plot_comparison(self, results: Dict, n_iterations: int):
        """Plot algorithm comparison."""
        # TODO: Create comparison plots
        pass
```

### Validation

Test bandits with simulation:
```python
# Test with known probabilities
true_probs = [0.05, 0.08, 0.10, 0.07]  # Arm 2 is best (10%)

sim = BanditSimulation(true_probs)
results = sim.compare_algorithms(n_iterations=10000)

# Check that algorithms converge to best arm
for name, result in results.items():
    stats = result['final_stats']
    print(f"\n{name}:")
    for arm_id, arm_stats in stats.items():
        print(f"  {arm_id}: {arm_stats['pulls']} pulls, {arm_stats['mean_reward']:.3f} reward")
```

### Success Criteria

- [ ] Epsilon-greedy balances exploration and exploitation
- [ ] UCB gives optimistic estimates for under-explored arms
- [ ] Thompson Sampling converges to optimal arm
- [ ] Simulation shows bandits outperform random allocation
- [ ] Algorithms can be integrated with model serving
- [ ] Tests pass

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Epsilon-Greedy**: Simple but effective, tune epsilon based on problem
2. **UCB**: No tuning needed, automatic exploration-exploitation balance
3. **Thompson Sampling**: Best for binary rewards, use Gaussian for continuous
4. **Comparison**: Thompson Sampling often performs best in practice
5. **Convergence**: All algorithms should eventually identify best arm
6. **Regret**: Measure cumulative regret to compare efficiency

</details>

---
