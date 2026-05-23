## Exercise 1: A/B Testing Framework (90 minutes)

**Objective**: Implement a complete A/B testing framework for ML model comparison with proper experiment design and tracking.

### Background

You need to A/B test a new ML model against the current production model. Your framework should:
- Assign users to treatment groups randomly
- Track model predictions and outcomes
- Calculate statistical significance
- Support multiple concurrent experiments
- Ensure consistent user experience (sticky assignment)

### Tasks

1. **Implement experiment assignment logic**:
   - Random assignment with configurable split ratios
   - Consistent hashing for sticky assignments
   - Support for multiple concurrent experiments
   - Exclusion/inclusion criteria

2. **Create tracking infrastructure**:
   - Log experiment assignments
   - Track predictions and outcomes
   - Store results for analysis
   - Support delayed conversion tracking

3. **Build analysis pipeline**:
   - Calculate conversion rates
   - Compute confidence intervals
   - Test statistical significance
   - Generate experiment reports

4. **Implement experiment configuration**:
   - YAML-based experiment definitions
   - Version control for experiments
   - Experiment lifecycle management

### Starter Code

```python
# ab_testing/experiment.py
"""A/B testing framework for ML models."""

import hashlib
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json

class ExperimentStatus(Enum):
    """Experiment lifecycle status."""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class VariantType(Enum):
    """Type of experiment variant."""
    CONTROL = "control"
    TREATMENT = "treatment"

@dataclass
class Variant:
    """Represents a variant in an A/B test."""

    id: str
    name: str
    variant_type: VariantType
    traffic_percentage: float
    model_uri: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate variant configuration."""
        if not 0 <= self.traffic_percentage <= 100:
            raise ValueError(f"Traffic percentage must be 0-100, got {self.traffic_percentage}")

@dataclass
class Experiment:
    """Represents an A/B experiment."""

    id: str
    name: str
    description: str
    variants: List[Variant]
    status: ExperimentStatus = ExperimentStatus.DRAFT
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    sample_size_target: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate experiment configuration."""
        # TODO: Validate total traffic allocation equals 100%
        total_traffic = sum(v.traffic_percentage for v in self.variants)
        if abs(total_traffic - 100.0) > 0.01:
            raise ValueError(f"Total traffic must equal 100%, got {total_traffic}")

        # TODO: Ensure exactly one control variant
        control_count = sum(1 for v in self.variants if v.variant_type == VariantType.CONTROL)
        if control_count != 1:
            raise ValueError(f"Must have exactly one control variant, got {control_count}")


class ExperimentAssigner:
    """Handles user assignment to experiment variants."""

    def __init__(self, seed: int = 42):
        """
        Initialize experiment assigner.

        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        random.seed(seed)

    def assign_variant(
        self,
        user_id: str,
        experiment: Experiment,
        use_consistent_hashing: bool = True
    ) -> Variant:
        """
        Assign user to experiment variant.

        Args:
            user_id: Unique user identifier
            experiment: Experiment configuration
            use_consistent_hashing: Use consistent hashing for sticky assignments

        Returns:
            Assigned variant
        """
        if use_consistent_hashing:
            # TODO: Implement consistent hashing
            # - Create hash from user_id + experiment_id
            # - Use hash to deterministically assign variant
            # - Ensures same user always gets same variant
            hash_str = f"{user_id}:{experiment.id}:{self.seed}"
            hash_value = int(hashlib.md5(hash_str.encode()).hexdigest(), 16)
            percentage = (hash_value % 10000) / 100.0  # 0-100 range

            # TODO: Assign based on traffic allocation
            cumulative = 0.0
            for variant in experiment.variants:
                cumulative += variant.traffic_percentage
                if percentage < cumulative:
                    return variant

            return experiment.variants[-1]  # Fallback
        else:
            # TODO: Implement random assignment (non-sticky)
            rand_value = random.random() * 100
            cumulative = 0.0
            for variant in experiment.variants:
                cumulative += variant.traffic_percentage
                if rand_value < cumulative:
                    return variant
            return experiment.variants[-1]

    def is_eligible(
        self,
        user_id: str,
        experiment: Experiment,
        user_attributes: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Check if user is eligible for experiment.

        Args:
            user_id: Unique user identifier
            experiment: Experiment configuration
            user_attributes: User attributes for filtering

        Returns:
            True if user is eligible
        """
        # TODO: Implement eligibility checks
        # - Check experiment status is ACTIVE
        # - Check experiment date range
        # - Apply inclusion/exclusion criteria from metadata
        # - Check user attributes against targeting rules

        if experiment.status != ExperimentStatus.ACTIVE:
            return False

        if experiment.start_date and datetime.now() < experiment.start_date:
            return False

        if experiment.end_date and datetime.now() > experiment.end_date:
            return False

        # TODO: Add more sophisticated filtering

        return True


class ExperimentTracker:
    """Tracks experiment events and outcomes."""

    def __init__(self, storage_backend: str = "local"):
        """
        Initialize experiment tracker.

        Args:
            storage_backend: Storage backend ('local', 'postgres', 'bigquery')
        """
        self.storage_backend = storage_backend
        self.events = []  # In-memory storage for local backend

    def track_assignment(
        self,
        user_id: str,
        experiment_id: str,
        variant_id: str,
        timestamp: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Track experiment assignment.

        Args:
            user_id: User identifier
            experiment_id: Experiment identifier
            variant_id: Assigned variant identifier
            timestamp: Assignment timestamp (default: now)
            metadata: Additional metadata
        """
        # TODO: Create assignment event
        event = {
            'event_type': 'assignment',
            'user_id': user_id,
            'experiment_id': experiment_id,
            'variant_id': variant_id,
            'timestamp': timestamp or datetime.now(),
            'metadata': metadata or {}
        }

        # TODO: Store event
        self._store_event(event)

    def track_prediction(
        self,
        user_id: str,
        experiment_id: str,
        variant_id: str,
        prediction: Any,
        features: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Track model prediction.

        Args:
            user_id: User identifier
            experiment_id: Experiment identifier
            variant_id: Variant identifier
            prediction: Model prediction
            features: Input features
            timestamp: Prediction timestamp
        """
        # TODO: Create prediction event
        event = {
            'event_type': 'prediction',
            'user_id': user_id,
            'experiment_id': experiment_id,
            'variant_id': variant_id,
            'prediction': prediction,
            'features': features,
            'timestamp': timestamp or datetime.now()
        }

        self._store_event(event)

    def track_outcome(
        self,
        user_id: str,
        experiment_id: str,
        variant_id: str,
        outcome: Any,
        metric_name: str = "conversion",
        timestamp: Optional[datetime] = None
    ):
        """
        Track experiment outcome.

        Args:
            user_id: User identifier
            experiment_id: Experiment identifier
            variant_id: Variant identifier
            outcome: Outcome value (e.g., True for conversion)
            metric_name: Name of the metric
            timestamp: Outcome timestamp
        """
        # TODO: Create outcome event
        event = {
            'event_type': 'outcome',
            'user_id': user_id,
            'experiment_id': experiment_id,
            'variant_id': variant_id,
            'metric_name': metric_name,
            'outcome': outcome,
            'timestamp': timestamp or datetime.now()
        }

        self._store_event(event)

    def _store_event(self, event: Dict[str, Any]):
        """Store event to backend."""
        if self.storage_backend == 'local':
            self.events.append(event)
        elif self.storage_backend == 'postgres':
            # TODO: Implement PostgreSQL storage
            pass
        elif self.storage_backend == 'bigquery':
            # TODO: Implement BigQuery storage
            pass

    def get_experiment_data(self, experiment_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all events for an experiment.

        Args:
            experiment_id: Experiment identifier

        Returns:
            List of events
        """
        # TODO: Filter events by experiment_id
        if self.storage_backend == 'local':
            return [e for e in self.events if e.get('experiment_id') == experiment_id]
        else:
            # TODO: Query from database
            pass
```

```python
# ab_testing/config.py
"""Experiment configuration management."""

import yaml
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from ab_testing.experiment import Experiment, Variant, ExperimentStatus, VariantType

class ExperimentConfig:
    """Manages experiment configurations from YAML files."""

    def __init__(self, config_dir: str = "./experiments"):
        """
        Initialize experiment config manager.

        Args:
            config_dir: Directory containing experiment YAML files
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True, parents=True)

    def load_experiment(self, experiment_id: str) -> Experiment:
        """
        Load experiment from YAML file.

        Args:
            experiment_id: Experiment identifier

        Returns:
            Experiment object
        """
        # TODO: Load YAML file
        config_file = self.config_dir / f"{experiment_id}.yaml"

        if not config_file.exists():
            raise FileNotFoundError(f"Experiment config not found: {config_file}")

        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        # TODO: Parse variants
        variants = [
            Variant(
                id=v['id'],
                name=v['name'],
                variant_type=VariantType(v['type']),
                traffic_percentage=v['traffic_percentage'],
                model_uri=v['model_uri'],
                metadata=v.get('metadata', {})
            )
            for v in config['variants']
        ]

        # TODO: Create experiment
        experiment = Experiment(
            id=config['id'],
            name=config['name'],
            description=config['description'],
            variants=variants,
            status=ExperimentStatus(config.get('status', 'draft')),
            start_date=self._parse_datetime(config.get('start_date')),
            end_date=self._parse_datetime(config.get('end_date')),
            sample_size_target=config.get('sample_size_target'),
            metadata=config.get('metadata', {})
        )

        return experiment

    def save_experiment(self, experiment: Experiment):
        """
        Save experiment to YAML file.

        Args:
            experiment: Experiment to save
        """
        # TODO: Convert experiment to dict
        config = {
            'id': experiment.id,
            'name': experiment.name,
            'description': experiment.description,
            'status': experiment.status.value,
            'variants': [
                {
                    'id': v.id,
                    'name': v.name,
                    'type': v.variant_type.value,
                    'traffic_percentage': v.traffic_percentage,
                    'model_uri': v.model_uri,
                    'metadata': v.metadata
                }
                for v in experiment.variants
            ],
            'start_date': experiment.start_date.isoformat() if experiment.start_date else None,
            'end_date': experiment.end_date.isoformat() if experiment.end_date else None,
            'sample_size_target': experiment.sample_size_target,
            'metadata': experiment.metadata
        }

        # TODO: Write to YAML file
        config_file = self.config_dir / f"{experiment.id}.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    def _parse_datetime(self, dt_str: Optional[str]) -> Optional[datetime]:
        """Parse datetime string."""
        if dt_str is None:
            return None
        return datetime.fromisoformat(dt_str)
```

```yaml
# experiments/model_v2_ab_test.yaml
# Example experiment configuration

id: model_v2_ab_test
name: "Model V2 vs V1 A/B Test"
description: "Testing new recommendation model v2 against production v1"
status: active
start_date: "2025-10-25T00:00:00"
end_date: "2025-11-08T23:59:59"
sample_size_target: 100000

variants:
  - id: control
    name: "Model V1 (Control)"
    type: control
    traffic_percentage: 50.0
    model_uri: "models:/recommendation_model/production"
    metadata:
      model_version: "1.2.3"
      algorithm: "collaborative_filtering"

  - id: treatment
    name: "Model V2 (Treatment)"
    type: treatment
    traffic_percentage: 50.0
    model_uri: "models:/recommendation_model/staging"
    metadata:
      model_version: "2.0.0"
      algorithm: "neural_collaborative_filtering"

metadata:
  owner: "ml-team@company.com"
  metrics:
    - click_through_rate
    - conversion_rate
    - revenue_per_user
  minimum_detectable_effect: 0.02
  significance_level: 0.05
  statistical_power: 0.80
```

### Validation Tests

```python
# tests/test_ab_testing.py
"""Tests for A/B testing framework."""

import pytest
from ab_testing.experiment import (
    Experiment, Variant, ExperimentAssigner, ExperimentTracker,
    ExperimentStatus, VariantType
)

@pytest.fixture
def sample_experiment():
    """Create sample experiment for testing."""
    variants = [
        Variant(
            id="control",
            name="Control",
            variant_type=VariantType.CONTROL,
            traffic_percentage=50.0,
            model_uri="models:/test/1"
        ),
        Variant(
            id="treatment",
            name="Treatment",
            variant_type=VariantType.TREATMENT,
            traffic_percentage=50.0,
            model_uri="models:/test/2"
        )
    ]

    return Experiment(
        id="test_exp",
        name="Test Experiment",
        description="Test",
        variants=variants,
        status=ExperimentStatus.ACTIVE
    )

def test_experiment_creation(sample_experiment):
    """Test that experiments are created correctly."""
    assert sample_experiment.id == "test_exp"
    assert len(sample_experiment.variants) == 2
    # TODO: Add more assertions

def test_traffic_allocation_validation():
    """Test that traffic allocation must equal 100%."""
    # TODO: Test that creating experiment with traffic != 100% raises error
    pass

def test_consistent_assignment(sample_experiment):
    """Test that users are assigned consistently."""
    assigner = ExperimentAssigner(seed=42)

    user_id = "user123"
    variant1 = assigner.assign_variant(user_id, sample_experiment)
    variant2 = assigner.assign_variant(user_id, sample_experiment)

    # TODO: Assert same user gets same variant
    assert variant1.id == variant2.id

def test_traffic_distribution(sample_experiment):
    """Test that traffic is distributed according to percentages."""
    assigner = ExperimentAssigner(seed=42)

    # TODO: Assign 10000 users
    # TODO: Count assignments to each variant
    # TODO: Assert distribution is approximately 50/50
    pass

def test_event_tracking():
    """Test that events are tracked correctly."""
    tracker = ExperimentTracker(storage_backend='local')

    # TODO: Track assignment
    tracker.track_assignment("user1", "exp1", "control")

    # TODO: Track prediction
    tracker.track_prediction("user1", "exp1", "control", prediction=0.8)

    # TODO: Track outcome
    tracker.track_outcome("user1", "exp1", "control", outcome=True)

    # TODO: Retrieve events
    events = tracker.get_experiment_data("exp1")

    # TODO: Assert correct number of events
    assert len(events) == 3

# Run with: pytest tests/test_ab_testing.py -v
```

### Success Criteria

- [ ] Experiment configuration loads from YAML
- [ ] Users are assigned consistently (sticky)
- [ ] Traffic distribution matches configuration
- [ ] All events (assignment, prediction, outcome) are tracked
- [ ] Experiments can be activated/paused/archived
- [ ] Multiple concurrent experiments are supported
- [ ] Tests pass

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Consistent Hashing**: Use MD5 hash of `user_id + experiment_id + seed` modulo 10000
2. **Traffic Allocation**: Sort variants by cumulative percentage, assign based on hash range
3. **Storage**: Start with in-memory list, then implement database storage
4. **Eligibility**: Check experiment status, date range, and user attributes
5. **Validation**: Use `__post_init__` in dataclasses for automatic validation
6. **Config**: Use YAML for human-readable experiment definitions

</details>

---
