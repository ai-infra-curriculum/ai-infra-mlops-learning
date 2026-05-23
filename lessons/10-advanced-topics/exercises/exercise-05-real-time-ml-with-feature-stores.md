## Exercise 5: Real-time ML with Feature Stores (120 minutes)

**Objective**: Build a real-time ML system with Feast feature store for online serving and feature management.

### Background

Real-time ML requires:
- Low-latency feature serving
- Consistent features (training/serving)
- Feature versioning and monitoring
- Online and offline feature stores
- Point-in-time correct features

### Tasks

1. **Set up Feast feature store**:
   - Install and configure Feast
   - Define feature views
   - Set up online/offline stores
   - Implement materialization

2. **Create feature pipelines**:
   - Define data sources
   - Create feature transformations
   - Implement feature validation
   - Set up feature monitoring

3. **Build online serving**:
   - Deploy online feature store
   - Implement feature retrieval API
   - Add caching layer
   - Optimize for latency

4. **Integrate with ML pipeline**:
   - Training with offline features
   - Serving with online features
   - Feature drift detection
   - Automated retraining triggers

### Starter Code

```python
# feast_feature_store.py
"""
Real-time ML with Feast feature store.
"""

from feast import FeatureStore, Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64, String
from feast.on_demand_feature_view import on_demand_feature_view
from feast.value_type import ValueType
from datetime import timedelta, datetime
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
import redis

# Feature definitions
class FeatureDefinitions:
    """
    Define features for the feature store.

    TODO: Implement feature definitions
    """

    @staticmethod
    def create_user_entity() -> Entity:
        """
        Create user entity.

        TODO: Define user entity
        """
        # return Entity(
        #     name="user",
        #     join_keys=["user_id"],
        #     description="User entity"
        # )
        pass

    @staticmethod
    def create_user_features(data_source: FileSource) -> FeatureView:
        """
        Create user feature view.

        TODO: Define user features
        - Age
        - Account age
        - Transaction count
        - Average transaction amount
        """
        # return FeatureView(
        #     name="user_features",
        #     entities=["user"],
        #     ttl=timedelta(days=1),
        #     schema=[
        #         Field(name="age", dtype=Int64),
        #         Field(name="account_age_days", dtype=Int64),
        #         Field(name="transaction_count_30d", dtype=Int64),
        #         Field(name="avg_transaction_amount_30d", dtype=Float32),
        #         Field(name="is_premium", dtype=Int64),
        #     ],
        #     source=data_source,
        # )
        pass

    @staticmethod
    def create_transaction_features(data_source: FileSource) -> FeatureView:
        """
        Create transaction feature view.

        TODO: Define transaction features
        """
        # return FeatureView(
        #     name="transaction_features",
        #     entities=["user"],
        #     ttl=timedelta(hours=1),
        #     schema=[
        #         Field(name="transaction_amount", dtype=Float32),
        #         Field(name="merchant_category", dtype=String),
        #         Field(name="transaction_hour", dtype=Int64),
        #         Field(name="is_international", dtype=Int64),
        #     ],
        #     source=data_source,
        # )
        pass

    @staticmethod
    @on_demand_feature_view(
        sources=[],  # TODO: Add source feature views
        schema=[
            Field(name="transaction_to_avg_ratio", dtype=Float32),
            Field(name="is_high_value", dtype=Int64),
        ]
    )
    def derived_features(features_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create on-demand derived features.

        TODO: Implement feature transformations
        - Transaction to average ratio
        - High value transaction flag
        - Risk score
        """
        # df = pd.DataFrame()

        # TODO: Calculate derived features
        # df["transaction_to_avg_ratio"] = (
        #     features_df["transaction_amount"] /
        #     features_df["avg_transaction_amount_30d"]
        # )

        # df["is_high_value"] = (
        #     features_df["transaction_amount"] > 1000
        # ).astype(int)

        # return df

        pass


class FeastFeatureStore:
    """
    Wrapper for Feast feature store operations.

    TODO: Implement feature store management
    """

    def __init__(self, repo_path: str = "./feature_repo"):
        """
        Initialize feature store.

        Args:
            repo_path: Path to Feast repository

        TODO: Initialize Feast store
        """
        self.repo_path = repo_path
        # self.store = FeatureStore(repo_path=repo_path)

        logging.info(f"Feature store initialized at {repo_path}")

    def setup_feature_store(self):
        """
        Set up feature store with initial configuration.

        TODO: Implement setup
        - Create entities
        - Define feature views
        - Configure online/offline stores
        - Apply configuration
        """
        # TODO: Create data sources
        # user_source = FileSource(
        #     path="data/user_features.parquet",
        #     timestamp_field="event_timestamp",
        # )

        # transaction_source = FileSource(
        #     path="data/transaction_features.parquet",
        #     timestamp_field="event_timestamp",
        # )

        # TODO: Create entities and feature views
        # user_entity = FeatureDefinitions.create_user_entity()
        # user_fv = FeatureDefinitions.create_user_features(user_source)
        # transaction_fv = FeatureDefinitions.create_transaction_features(transaction_source)

        # TODO: Apply to store
        # self.store.apply([user_entity, user_fv, transaction_fv])

        logging.info("Feature store setup complete")

    def materialize_features(
        self,
        start_date: datetime,
        end_date: datetime
    ):
        """
        Materialize features to online store.

        TODO: Implement materialization
        - Load features from offline store
        - Push to online store (Redis)
        - Verify materialization
        """
        # TODO: Materialize features
        # self.store.materialize(
        #     start_date=start_date,
        #     end_date=end_date
        # )

        # logging.info(f"Materialized features from {start_date} to {end_date}")

        pass

    def get_online_features(
        self,
        entity_rows: List[Dict],
        features: List[str]
    ) -> pd.DataFrame:
        """
        Get features for online serving.

        TODO: Implement online feature retrieval
        - Fetch from online store
        - Handle missing features
        - Return as DataFrame
        """
        # TODO: Get features
        # feature_vector = self.store.get_online_features(
        #     features=features,
        #     entity_rows=entity_rows
        # )

        # TODO: Convert to DataFrame
        # return feature_vector.to_df()

        pass

    def get_historical_features(
        self,
        entity_df: pd.DataFrame,
        features: List[str]
    ) -> pd.DataFrame:
        """
        Get historical features for training.

        TODO: Implement offline feature retrieval
        - Perform point-in-time join
        - Return training dataset
        """
        # TODO: Get historical features
        # training_df = self.store.get_historical_features(
        #     entity_df=entity_df,
        #     features=features
        # ).to_df()

        # return training_df

        pass

    def validate_features(
        self,
        feature_df: pd.DataFrame,
        feature_names: List[str]
    ) -> Dict:
        """
        Validate feature quality.

        TODO: Implement feature validation
        - Check for nulls
        - Validate distributions
        - Detect outliers
        - Check freshness
        """
        validation_results = {}

        for feature in feature_names:
            if feature not in feature_df.columns:
                validation_results[feature] = {"status": "missing"}
                continue

            # TODO: Calculate validation metrics
            # null_pct = feature_df[feature].isnull().mean()
            # validation_results[feature] = {
            #     "status": "valid" if null_pct < 0.1 else "invalid",
            #     "null_percentage": null_pct,
            #     "mean": feature_df[feature].mean() if pd.api.types.is_numeric_dtype(feature_df[feature]) else None,
            #     "std": feature_df[feature].std() if pd.api.types.is_numeric_dtype(feature_df[feature]) else None
            # }

        return validation_results


class RealtimeMLPipeline:
    """
    Real-time ML pipeline with feature store.

    TODO: Implement end-to-end real-time ML
    """

    def __init__(
        self,
        feature_store: FeastFeatureStore,
        model_path: Optional[str] = None
    ):
        """Initialize pipeline."""
        self.feature_store = feature_store
        self.model = None

        # TODO: Load model if provided
        # if model_path:
        #     import joblib
        #     self.model = joblib.load(model_path)

    def train(
        self,
        entity_df: pd.DataFrame,
        features: List[str],
        target_column: str
    ):
        """
        Train model using historical features.

        TODO: Implement training with feature store
        - Get historical features
        - Prepare training data
        - Train model
        - Log to MLflow
        """
        logging.info("Starting training with historical features")

        # TODO: Get historical features
        # training_df = self.feature_store.get_historical_features(
        #     entity_df=entity_df,
        #     features=features
        # )

        # TODO: Prepare X, y
        # feature_columns = [f.split(':')[1] for f in features]
        # X = training_df[feature_columns]
        # y = training_df[target_column]

        # TODO: Train model
        # from sklearn.ensemble import RandomForestClassifier
        # self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        # self.model.fit(X, y)

        # TODO: Validate features
        # validation_results = self.feature_store.validate_features(
        #     training_df,
        #     feature_columns
        # )
        # logging.info(f"Feature validation: {validation_results}")

        logging.info("Training complete")

    def predict(
        self,
        user_ids: List[int],
        features: List[str]
    ) -> np.ndarray:
        """
        Make real-time predictions.

        TODO: Implement online prediction
        - Get online features
        - Make predictions
        - Log prediction latency
        """
        if self.model is None:
            raise ValueError("Model not trained or loaded")

        import time
        start = time.time()

        # TODO: Prepare entity rows
        # entity_rows = [{"user_id": user_id} for user_id in user_ids]

        # TODO: Get online features
        # feature_df = self.feature_store.get_online_features(
        #     entity_rows=entity_rows,
        #     features=features
        # )

        # TODO: Make predictions
        # feature_columns = [f.split(':')[1] for f in features]
        # X = feature_df[feature_columns]
        # predictions = self.model.predict(X)

        latency = time.time() - start
        logging.info(f"Prediction latency: {latency*1000:.2f}ms for {len(user_ids)} users")

        # return predictions

        pass

    def monitor_feature_drift(
        self,
        current_features: pd.DataFrame,
        reference_features: pd.DataFrame,
        feature_names: List[str]
    ) -> Dict:
        """
        Monitor feature drift.

        TODO: Implement drift detection
        - Calculate distribution differences
        - Detect statistical drift
        - Alert on significant drift
        """
        from scipy import stats

        drift_results = {}

        for feature in feature_names:
            # TODO: Calculate KS statistic
            # ks_stat, p_value = stats.ks_2samp(
            #     reference_features[feature],
            #     current_features[feature]
            # )

            # drift_results[feature] = {
            #     'ks_statistic': ks_stat,
            #     'p_value': p_value,
            #     'drift_detected': p_value < 0.05
            # }

            pass

        return drift_results


# FastAPI serving endpoint
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Real-time ML API")

# Global instances
feature_store: Optional[FeastFeatureStore] = None
ml_pipeline: Optional[RealtimeMLPipeline] = None

class PredictionRequest(BaseModel):
    user_ids: List[int]

class PredictionResponse(BaseModel):
    predictions: List[float]
    latency_ms: float

@app.on_event("startup")
async def startup():
    """Initialize feature store and model on startup."""
    global feature_store, ml_pipeline

    # TODO: Initialize feature store
    # feature_store = FeastFeatureStore(repo_path="./feature_repo")
    # ml_pipeline = RealtimeMLPipeline(
    #     feature_store=feature_store,
    #     model_path="./model.pkl"
    # )

    logging.info("Real-time ML API started")

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Make real-time predictions.

    TODO: Implement prediction endpoint
    """
    import time
    start = time.time()

    try:
        # TODO: Get features and predict
        # features = [
        #     "user_features:age",
        #     "user_features:transaction_count_30d",
        #     "user_features:avg_transaction_amount_30d"
        # ]

        # predictions = ml_pipeline.predict(
        #     user_ids=request.user_ids,
        #     features=features
        # )

        latency = (time.time() - start) * 1000

        # return PredictionResponse(
        #     predictions=predictions.tolist(),
        #     latency_ms=latency
        # )

        pass

    except Exception as e:
        logging.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy"}


if __name__ == "__main__":
    # TODO: Example usage

    # 1. Setup feature store
    # fs = FeastFeatureStore(repo_path="./feature_repo")
    # fs.setup_feature_store()

    # 2. Materialize features
    # fs.materialize_features(
    #     start_date=datetime(2024, 1, 1),
    #     end_date=datetime(2024, 1, 31)
    # )

    # 3. Train model
    # entity_df = pd.DataFrame({
    #     'user_id': [1, 2, 3, 4, 5],
    #     'event_timestamp': [datetime.now()] * 5,
    #     'fraud_label': [0, 0, 1, 0, 1]
    # })

    # pipeline = RealtimeMLPipeline(feature_store=fs)
    # pipeline.train(
    #     entity_df=entity_df,
    #     features=["user_features:age", "user_features:transaction_count_30d"],
    #     target_column="fraud_label"
    # )

    # 4. Make predictions
    # predictions = pipeline.predict(
    #     user_ids=[1, 2, 3],
    #     features=["user_features:age", "user_features:transaction_count_30d"]
    # )

    pass
```

```yaml
# feature_store.yaml
# Feast feature store configuration

project: realtime_ml
registry: data/registry.db
provider: local
online_store:
  type: redis
  connection_string: "localhost:6379"
offline_store:
  type: file
```

### Success Criteria

- [ ] Feast feature store is configured correctly
- [ ] Features are materialized to online store
- [ ] Online feature retrieval is under 50ms
- [ ] Historical features support point-in-time joins
- [ ] Training and serving use same features
- [ ] Feature drift is detected
- [ ] Real-time predictions work end-to-end

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Online Store**: Use Redis for low-latency feature serving
2. **Offline Store**: Use Parquet files or data warehouse
3. **Materialization**: Schedule regular materialization jobs
4. **Features**: Define features with proper TTL
5. **Monitoring**: Track feature freshness and drift
6. **Caching**: Add caching layer for frequently accessed features

</details>

---

## Submission Guidelines

For each exercise, submit:
1. **Code**: All implementation files with TODOs completed
2. **Documentation**: Architecture decisions and design choices
3. **Benchmarks**: Performance metrics and comparisons
4. **Screenshots**: Successful runs and visualizations
5. **Reflection**: Challenges faced and lessons learned

**Estimated Total Time**: 7.5 hours
**Difficulty**: Advanced

Good luck!
