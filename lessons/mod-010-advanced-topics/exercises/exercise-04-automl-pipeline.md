## Exercise 4: AutoML Pipeline (90 minutes)

**Objective**: Build an automated machine learning pipeline with hyperparameter optimization, architecture search, and model selection.

### Background

AutoML automates:
- Hyperparameter tuning
- Feature engineering
- Model selection
- Architecture search
- Ensemble creation

### Tasks

1. **Implement hyperparameter optimization**:
   - Use Optuna for optimization
   - Define search space
   - Implement pruning
   - Track experiments

2. **Build AutoML pipeline**:
   - Automated preprocessing
   - Model selection
   - Feature selection
   - Ensemble methods

3. **Create neural architecture search**:
   - Define search space
   - Implement search strategy
   - Evaluate candidates
   - Select best architecture

4. **Add experiment tracking**:
   - Log all trials
   - Visualize results
   - Compare models
   - Export best model

### Starter Code

```python
# automl_pipeline.py
"""
AutoML pipeline with Optuna for hyperparameter optimization.
"""

import optuna
from optuna.pruners import MedianPruner
from optuna.samplers import TPESampler
import mlflow
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime

class AutoMLPipeline:
    """
    Automated ML pipeline with hyperparameter optimization.

    TODO: Implement complete AutoML system
    """

    def __init__(
        self,
        task: str = "classification",  # "classification" or "regression"
        metric: str = "accuracy",
        n_trials: int = 100,
        timeout: int = 3600,  # seconds
        mlflow_tracking_uri: str = "http://localhost:5000"
    ):
        """
        Initialize AutoML pipeline.

        Args:
            task: ML task type
            metric: Optimization metric
            n_trials: Number of optimization trials
            timeout: Optimization timeout in seconds
            mlflow_tracking_uri: MLflow tracking server URI

        TODO: Set up AutoML configuration
        """
        self.task = task
        self.metric = metric
        self.n_trials = n_trials
        self.timeout = timeout

        # TODO: Set up MLflow
        # mlflow.set_tracking_uri(mlflow_tracking_uri)
        # mlflow.set_experiment("automl_optimization")

        # TODO: Initialize study
        # self.study = None
        # self.best_model = None
        # self.best_params = None

        logging.info(f"AutoML pipeline initialized for {task} task")

    def create_objective(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray
    ):
        """
        Create Optuna objective function.

        TODO: Implement objective function
        - Suggest hyperparameters
        - Train model
        - Evaluate performance
        - Return metric
        """
        def objective(trial: optuna.Trial) -> float:
            """
            Objective function for optimization.

            TODO: Implement objective
            """
            # TODO: Start MLflow run
            with mlflow.start_run(nested=True):
                # TODO: Suggest model type
                # model_name = trial.suggest_categorical(
                #     'model',
                #     ['random_forest', 'gradient_boosting', 'svm']
                # )

                # TODO: Suggest hyperparameters based on model
                # if model_name == 'random_forest':
                #     params = {
                #         'n_estimators': trial.suggest_int('n_estimators', 50, 500),
                #         'max_depth': trial.suggest_int('max_depth', 3, 20),
                #         'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
                #         'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
                #         'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2']),
                #         'random_state': 42
                #     }
                #     model = RandomForestClassifier(**params)

                # elif model_name == 'gradient_boosting':
                #     params = {
                #         'n_estimators': trial.suggest_int('n_estimators', 50, 300),
                #         'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
                #         'max_depth': trial.suggest_int('max_depth', 3, 10),
                #         'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
                #         'subsample': trial.suggest_float('subsample', 0.6, 1.0),
                #         'random_state': 42
                #     }
                #     model = GradientBoostingClassifier(**params)

                # elif model_name == 'svm':
                #     params = {
                #         'C': trial.suggest_float('C', 0.1, 100, log=True),
                #         'kernel': trial.suggest_categorical('kernel', ['rbf', 'poly']),
                #         'gamma': trial.suggest_categorical('gamma', ['scale', 'auto']),
                #         'random_state': 42
                #     }
                #     model = SVC(**params)

                # TODO: Suggest preprocessing
                # use_scaling = trial.suggest_categorical('use_scaling', [True, False])
                # if use_scaling:
                #     scaler = StandardScaler()
                #     X_train_processed = scaler.fit_transform(X_train)
                #     X_val_processed = scaler.transform(X_val)
                # else:
                #     X_train_processed = X_train
                #     X_val_processed = X_val

                # TODO: Feature selection
                # n_features = trial.suggest_int('n_features', 10, X_train.shape[1])
                # selector = SelectKBest(f_classif, k=n_features)
                # X_train_processed = selector.fit_transform(X_train_processed, y_train)
                # X_val_processed = selector.transform(X_val_processed)

                # TODO: Train model
                # model.fit(X_train_processed, y_train)

                # TODO: Evaluate
                # y_pred = model.predict(X_val_processed)
                # score = accuracy_score(y_val, y_pred)

                # TODO: Log parameters and metrics to MLflow
                # mlflow.log_params(params)
                # mlflow.log_param('model_type', model_name)
                # mlflow.log_metric('accuracy', score)

                # TODO: Pruning - report intermediate value
                # trial.report(score, step=1)

                # if trial.should_prune():
                #     raise optuna.TrialPruned()

                # return score

                pass

        return objective

    def optimize(
        self,
        X: np.ndarray,
        y: np.ndarray,
        test_size: float = 0.2
    ) -> Dict:
        """
        Run AutoML optimization.

        TODO: Implement optimization loop
        - Split data
        - Create study
        - Run optimization
        - Return best model and params
        """
        # TODO: Split data
        # X_train, X_val, y_train, y_val = train_test_split(
        #     X, y, test_size=test_size, random_state=42, stratify=y
        # )

        # TODO: Create objective
        # objective = self.create_objective(X_train, y_train, X_val, y_val)

        # TODO: Create study with pruning
        # sampler = TPESampler(seed=42)
        # pruner = MedianPruner(n_startup_trials=5, n_warmup_steps=10)

        # self.study = optuna.create_study(
        #     direction='maximize',
        #     sampler=sampler,
        #     pruner=pruner,
        #     study_name=f"automl_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        # )

        # TODO: Run optimization
        # logging.info(f"Starting optimization with {self.n_trials} trials")

        # with mlflow.start_run(run_name="automl_optimization"):
        #     self.study.optimize(
        #         objective,
        #         n_trials=self.n_trials,
        #         timeout=self.timeout,
        #         show_progress_bar=True
        #     )

        #     # TODO: Get best trial
        #     best_trial = self.study.best_trial
        #     self.best_params = best_trial.params

        #     # TODO: Log best params to MLflow
        #     mlflow.log_params(self.best_params)
        #     mlflow.log_metric('best_score', best_trial.value)

        #     # TODO: Train final model with best params
        #     self.best_model = self._train_best_model(X_train, y_train)

        #     # TODO: Evaluate on validation set
        #     val_score = self._evaluate_model(self.best_model, X_val, y_val)
        #     mlflow.log_metric('val_score', val_score)

        #     # TODO: Log model
        #     mlflow.sklearn.log_model(self.best_model, "best_model")

        # TODO: Return results
        # return {
        #     'best_params': self.best_params,
        #     'best_score': best_trial.value,
        #     'n_trials': len(self.study.trials),
        #     'study': self.study
        # }

        pass

    def _train_best_model(self, X: np.ndarray, y: np.ndarray):
        """
        Train model with best parameters.

        TODO: Recreate best model and train
        """
        # TODO: Extract model type and params
        # model_name = self.best_params['model']

        # TODO: Create model with best params
        # TODO: Apply preprocessing if specified
        # TODO: Train model

        pass

    def _evaluate_model(self, model, X: np.ndarray, y: np.ndarray) -> float:
        """Evaluate model on data."""
        # predictions = model.predict(X)
        # if self.metric == 'accuracy':
        #     from sklearn.metrics import accuracy_score
        #     return accuracy_score(y, predictions)
        # TODO: Add other metrics
        pass

    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance from best model.

        TODO: Extract and return feature importances
        """
        if self.best_model is None:
            raise ValueError("No model trained yet")

        # TODO: Get feature importance
        # if hasattr(self.best_model, 'feature_importances_'):
        #     importances = self.best_model.feature_importances_
        #
        #     return pd.DataFrame({
        #         'feature': range(len(importances)),
        #         'importance': importances
        #     }).sort_values('importance', ascending=False)

        pass

    def plot_optimization_history(self):
        """
        Visualize optimization history.

        TODO: Create visualization of trials
        """
        if self.study is None:
            raise ValueError("No study available")

        # TODO: Plot optimization history
        # import matplotlib.pyplot as plt
        # from optuna.visualization import plot_optimization_history, plot_param_importances

        # fig1 = plot_optimization_history(self.study)
        # fig1.show()

        # fig2 = plot_param_importances(self.study)
        # fig2.show()

        pass


# Neural Architecture Search
class NeuralArchitectureSearch:
    """
    Neural Architecture Search with Optuna.

    TODO: Implement NAS
    """

    def __init__(self, input_shape: Tuple, num_classes: int):
        """Initialize NAS."""
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.best_model = None

    def create_model(self, trial: optuna.Trial):
        """
        Create model based on trial suggestions.

        TODO: Implement architecture search space
        - Number of layers
        - Layer types
        - Activation functions
        - Regularization
        """
        import tensorflow as tf

        # TODO: Create sequential model
        # model = tf.keras.Sequential()
        # model.add(tf.keras.layers.Input(shape=self.input_shape))

        # TODO: Suggest number of layers
        # n_layers = trial.suggest_int('n_layers', 1, 5)

        # for i in range(n_layers):
        #     # TODO: Suggest layer type
        #     layer_type = trial.suggest_categorical(f'layer_{i}_type', ['dense', 'conv'])
        #
        #     if layer_type == 'dense':
        #         # TODO: Suggest units
        #         n_units = trial.suggest_int(f'layer_{i}_units', 32, 512, log=True)
        #         model.add(tf.keras.layers.Dense(n_units))
        #
        #     # TODO: Suggest activation
        #     activation = trial.suggest_categorical(f'layer_{i}_activation', ['relu', 'tanh'])
        #     model.add(tf.keras.layers.Activation(activation))
        #
        #     # TODO: Suggest dropout
        #     dropout = trial.suggest_float(f'layer_{i}_dropout', 0.0, 0.5)
        #     if dropout > 0:
        #         model.add(tf.keras.layers.Dropout(dropout))

        # TODO: Output layer
        # model.add(tf.keras.layers.Dense(self.num_classes, activation='softmax'))

        # TODO: Suggest optimizer and learning rate
        # learning_rate = trial.suggest_float('learning_rate', 1e-5, 1e-1, log=True)
        # optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

        # model.compile(
        #     optimizer=optimizer,
        #     loss='sparse_categorical_crossentropy',
        #     metrics=['accuracy']
        # )

        # return model

        pass

    def search(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        n_trials: int = 50
    ):
        """
        Run architecture search.

        TODO: Implement NAS optimization
        """
        def objective(trial):
            # TODO: Create model
            # model = self.create_model(trial)

            # TODO: Train model
            # history = model.fit(
            #     X_train, y_train,
            #     validation_data=(X_val, y_val),
            #     epochs=10,
            #     batch_size=32,
            #     verbose=0
            # )

            # TODO: Return validation accuracy
            # return history.history['val_accuracy'][-1]

            pass

        # TODO: Create and run study
        # study = optuna.create_study(direction='maximize')
        # study.optimize(objective, n_trials=n_trials)

        # TODO: Train best model
        # self.best_model = self.create_model(study.best_trial)

        pass


# Example usage
if __name__ == "__main__":
    # TODO: Load data
    # from sklearn.datasets import load_digits
    # X, y = load_digits(return_X_y=True)

    # TODO: Run AutoML
    # automl = AutoMLPipeline(
    #     task="classification",
    #     metric="accuracy",
    #     n_trials=50,
    #     timeout=1800
    # )

    # results = automl.optimize(X, y)
    # print(f"Best score: {results['best_score']:.4f}")
    # print(f"Best params: {results['best_params']}")

    # TODO: Visualize
    # automl.plot_optimization_history()

    pass
```

### Success Criteria

- [ ] Optuna optimization runs successfully
- [ ] Multiple models and hyperparameters explored
- [ ] Pruning reduces unnecessary trials
- [ ] Best model identified and logged to MLflow
- [ ] Performance improved over baseline
- [ ] Visualization of optimization process
- [ ] NAS finds optimal architecture

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Search Space**: Define broad initial space, narrow based on results
2. **Pruning**: Use MedianPruner to stop unpromising trials early
3. **Parallel**: Run with `n_jobs=-1` for parallel optimization
4. **Sampling**: TPESampler generally works best
5. **MLflow**: Log every trial for complete experiment tracking
6. **Ensembles**: Combine top-k models for better performance

</details>

---
