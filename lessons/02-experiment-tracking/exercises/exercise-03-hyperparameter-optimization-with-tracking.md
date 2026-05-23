## Exercise 3: Hyperparameter Optimization with Tracking (90 minutes)

**Objective**: Implement hyperparameter optimization using Optuna with comprehensive MLflow tracking.

### Background

Manual hyperparameter tuning is inefficient. You need to:
- Automate hyperparameter search
- Track all trials
- Visualize optimization progress
- Select best configuration
- Reproduce results

### Tasks

1. **Implement Optuna optimization with MLflow callback**
2. **Track all trials as MLflow runs**
3. **Create parent-child run hierarchy**
4. **Implement early stopping**
5. **Visualize optimization results**

### Starter Code

```python
# hyperparameter_optimization.py
"""Hyperparameter optimization with Optuna and MLflow tracking."""

import optuna
from optuna.integration.mlflow import MLflowCallback
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification
import numpy as np
from typing import Dict, Any

class MLflowOptunaBridge:
    """Bridge between Optuna and MLflow for comprehensive tracking."""

    def __init__(self, experiment_name: str, tracking_uri: str = "http://localhost:5000"):
        """
        Initialize MLflow-Optuna bridge.

        Args:
            experiment_name: Name of MLflow experiment
            tracking_uri: MLflow tracking URI
        """
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)
        self.experiment_name = experiment_name

    def objective(self, trial: optuna.Trial, X: np.ndarray, y: np.ndarray) -> float:
        """
        Objective function for Optuna optimization.

        Args:
            trial: Optuna trial
            X: Training features
            y: Training labels

        Returns:
            Score to optimize (higher is better)
        """
        # TODO: Define hyperparameter search space
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 10, 200),
            'max_depth': trial.suggest_int('max_depth', 2, 32),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
            'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', None]),
            'bootstrap': trial.suggest_categorical('bootstrap', [True, False]),
        }

        # TODO: Create and train model
        model = RandomForestClassifier(**params, random_state=42)

        # TODO: Evaluate with cross-validation
        score = cross_val_score(model, X, y, cv=5, scoring='accuracy', n_jobs=-1).mean()

        # TODO: Log to MLflow (handled by callback, but you can log additional metrics)

        return score

    def optimize(
        self,
        X: np.ndarray,
        y: np.ndarray,
        n_trials: int = 50,
        timeout: int = 3600
    ) -> optuna.Study:
        """
        Run hyperparameter optimization.

        Args:
            X: Training features
            y: Training labels
            n_trials: Number of optimization trials
            timeout: Timeout in seconds

        Returns:
            Completed Optuna study
        """
        # TODO: Create Optuna study
        study = optuna.create_study(
            study_name=f"{self.experiment_name}_optimization",
            direction='maximize',
            sampler=optuna.samplers.TPESampler(seed=42),
            pruner=optuna.pruners.MedianPruner(n_startup_trials=5, n_warmup_steps=10)
        )

        # TODO: Create MLflow callback
        mlflc = MLflowCallback(
            tracking_uri=mlflow.get_tracking_uri(),
            metric_name="accuracy",
            create_experiment=False,
            mlflow_kwargs={"experiment_name": self.experiment_name}
        )

        # TODO: Run optimization
        with mlflow.start_run(run_name="hyperparameter_optimization") as parent_run:
            mlflow.log_param("n_trials", n_trials)
            mlflow.log_param("timeout", timeout)
            mlflow.log_param("sampler", "TPESampler")
            mlflow.log_param("pruner", "MedianPruner")

            study.optimize(
                lambda trial: self.objective(trial, X, y),
                n_trials=n_trials,
                timeout=timeout,
                callbacks=[mlflc]
            )

            # TODO: Log best results
            mlflow.log_params(study.best_params)
            mlflow.log_metric("best_accuracy", study.best_value)
            mlflow.log_metric("n_trials_completed", len(study.trials))

            # TODO: Log optimization visualizations
            # self._log_optimization_plots(study)

        return study

    def _log_optimization_plots(self, study: optuna.Study):
        """
        Create and log optimization visualizations.

        Args:
            study: Completed Optuna study
        """
        try:
            import matplotlib.pyplot as plt
            from optuna.visualization.matplotlib import (
                plot_optimization_history,
                plot_param_importances,
                plot_parallel_coordinate
            )

            # TODO: Create optimization history plot
            fig = plot_optimization_history(study)
            mlflow.log_figure(fig, "optimization_history.png")
            plt.close()

            # TODO: Create parameter importance plot
            fig = plot_param_importances(study)
            mlflow.log_figure(fig, "param_importances.png")
            plt.close()

            # TODO: Create parallel coordinate plot
            fig = plot_parallel_coordinate(study)
            mlflow.log_figure(fig, "parallel_coordinate.png")
            plt.close()

        except Exception as e:
            print(f"Failed to log optimization plots: {e}")

    def retrain_best_model(self, study: optuna.Study, X: np.ndarray, y: np.ndarray):
        """
        Retrain model with best hyperparameters and log to MLflow.

        Args:
            study: Completed Optuna study
            X: Training features
            y: Training labels
        """
        with mlflow.start_run(run_name="best_model_retrain"):
            # TODO: Log best parameters
            mlflow.log_params(study.best_params)

            # TODO: Train model with best parameters
            model = RandomForestClassifier(**study.best_params, random_state=42)
            model.fit(X, y)

            # TODO: Log model
            mlflow.sklearn.log_model(model, "model")

            # TODO: Log final metrics
            score = cross_val_score(model, X, y, cv=5, scoring='accuracy').mean()
            mlflow.log_metric("cv_accuracy", score)

            print(f"Best model retrained with CV accuracy: {score:.4f}")


# Example usage
if __name__ == '__main__':
    # Generate sample data
    X, y = make_classification(n_samples=1000, n_features=20, n_informative=15, n_redundant=5, random_state=42)

    # Run optimization
    optimizer = MLflowOptunaBridge(experiment_name="rf_optimization")
    study = optimizer.optimize(X, y, n_trials=30)

    # Print results
    print(f"Best parameters: {study.best_params}")
    print(f"Best CV accuracy: {study.best_value:.4f}")

    # Retrain best model
    optimizer.retrain_best_model(study, X, y)
```

```python
# advanced_optimization.py
"""Advanced optimization strategies with MLflow tracking."""

import optuna
import mlflow
from sklearn.model_selection import train_test_split
from typing import Callable, Dict, Any
import numpy as np

class AdvancedOptimizer:
    """Advanced optimization with multiple strategies."""

    def __init__(self, tracking_uri: str = "http://localhost:5000"):
        mlflow.set_tracking_uri(tracking_uri)

    def multi_objective_optimization(
        self,
        X: np.ndarray,
        y: np.ndarray,
        experiment_name: str = "multi_objective_opt"
    ) -> optuna.Study:
        """
        Optimize for multiple objectives (e.g., accuracy and inference time).

        Args:
            X: Training features
            y: Training labels
            experiment_name: MLflow experiment name

        Returns:
            Completed multi-objective study
        """
        mlflow.set_experiment(experiment_name)

        def objective(trial):
            # TODO: Define hyperparameters
            # TODO: Train model
            # TODO: Calculate accuracy
            # TODO: Measure inference time
            # Return tuple of (accuracy, -inference_time) for minimization
            pass

        # TODO: Create multi-objective study
        study = optuna.create_study(directions=['maximize', 'minimize'])

        # TODO: Optimize
        # TODO: Log Pareto front to MLflow

        return study

    def distributed_optimization(
        self,
        objective_fn: Callable,
        n_trials: int = 100,
        n_jobs: int = -1
    ) -> optuna.Study:
        """
        Run distributed hyperparameter optimization.

        Args:
            objective_fn: Objective function
            n_trials: Number of trials
            n_jobs: Number of parallel jobs

        Returns:
            Completed study
        """
        # TODO: Create study with storage (for distributed optimization)
        # study = optuna.create_study(
        #     study_name="distributed_opt",
        #     storage="postgresql://user:password@localhost/optuna",
        #     direction="maximize",
        #     load_if_exists=True
        # )

        # TODO: Optimize with n_jobs
        # study.optimize(objective_fn, n_trials=n_trials, n_jobs=n_jobs)

        pass
```

### Validation

Run optimization and check results:
```bash
# Run hyperparameter optimization
python hyperparameter_optimization.py

# Check MLflow UI for:
# - Parent run with optimization summary
# - Child runs for each trial
# - Optimization visualizations
# - Best parameters logged
```

### Success Criteria

- [ ] Optuna optimization runs successfully
- [ ] All trials are logged to MLflow
- [ ] Parent-child run hierarchy is created
- [ ] Best parameters are identified and logged
- [ ] Visualization plots are generated and logged
- [ ] Early stopping (pruning) works
- [ ] Best model can be retrained with logged parameters

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Callback**: Use `MLflowCallback` from `optuna.integration.mlflow`
2. **Parent Run**: Start MLflow run before `study.optimize()` to create hierarchy
3. **Pruning**: Use `MedianPruner` or `HyperbandPruner` for early stopping
4. **Visualization**: Use `optuna.visualization.matplotlib` for plots
5. **Best Params**: Access via `study.best_params` and `study.best_value`
6. **Sampler**: TPESampler is good for < 100 trials, CmaEsSampler for continuous spaces

</details>

---
