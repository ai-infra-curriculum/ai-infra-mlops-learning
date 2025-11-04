# Module 02: Experiment Tracking & MLflow

---

## ⚠️ AI-Generated Content Disclaimer

> **Important Notice**: The content in this repository has been generated with AI assistance and is currently undergoing human review and verification. While we strive for accuracy, **the content may contain errors, inaccuracies, or outdated information**. 
>
> **Status**: 🔄 Verification in progress
>
> Please use this content as a learning resource with appropriate caution. We recommend:
> - Cross-referencing with official documentation
> - Testing all code examples in a safe environment
> - Reporting any errors or inaccuracies via GitHub issues
>
> We appreciate your understanding as we work to ensure content quality and accuracy.

---


**Role**: MLOps Engineer (Level 2.5B)
**Duration**: 20 hours
**Prerequisites**:
- Completed Module 01: CI/CD Foundations
- Strong Python programming skills
- Basic understanding of machine learning workflows
- Familiarity with ML model training and evaluation

## Module Overview

This module teaches you how to systematically track machine learning experiments using MLflow. You'll learn to record parameters, metrics, and artifacts; manage model versions through a registry; compare experiments; and integrate tracking into your ML workflows.

## Learning Objectives

By the end of this module, you will be able to:

1. **Explain** why experiment tracking is essential for ML projects
2. **Set up** MLflow tracking server with proper backend and artifact storage
3. **Track** experiments comprehensively (parameters, metrics, artifacts, models)
4. **Use** the MLflow Model Registry for versioning and lifecycle management
5. **Package** ML code using MLflow Projects for reproducibility
6. **Deploy** models using MLflow Models to various platforms
7. **Integrate** MLflow with hyperparameter optimization frameworks (Optuna, Ray Tune)
8. **Compare** experiments and identify best models
9. **Apply** best practices for production-grade experiment tracking

## Topics Covered

### 1. Introduction to Experiment Tracking (2 hours)
- Why experiment tracking matters
- What to track in ML experiments
- Industry tools and adoption
- The experiment tracking lifecycle

### 2. MLflow Fundamentals (2 hours)
- MLflow architecture and components
- Installation and setup
- Backend store vs artifact store
- MLflow UI overview

### 3. MLflow Tracking API (3 hours)
- Starting and managing runs
- Logging parameters, metrics, and artifacts
- Logging models with different flavors
- Tags and metadata
- Nested runs for hyperparameter tuning
- Querying and searching runs

### 4. Model Registry (2.5 hours)
- Registering models
- Managing model versions
- Stage transitions (Staging → Production)
- Loading models from registry
- Best practices for model registry

### 5. MLflow Projects (1.5 hours)
- Creating MLproject files
- Conda and Docker environments
- Running projects locally and remotely
- Parameterizable ML code

### 6. MLflow Models (1.5 hours)
- Model flavors (sklearn, PyTorch, TensorFlow, etc.)
- Custom Python function models
- Model signatures
- Model serving locally and in production

### 7. Hyperparameter Optimization (2 hours)
- Integration with Optuna
- Integration with Ray Tune
- Grid search with MLflow tracking
- Nested runs for tuning experiments

### 8. Advanced MLflow Features (1.5 hours)
- MLflow plugins
- System metrics logging
- Autologging
- MLflow Recipes/Pipelines
- Comparing runs visually

### 9. Alternative Tools (1 hour)
- Weights & Biases (W&B)
- Neptune.ai
- TensorBoard
- Tool comparison and recommendations

### 10. Best Practices (1.5 hours)
- Experiment organization strategies
- What and when to track
- Production-ready tracking template
- Performance optimization

### 11. Integration with ML Pipelines (1 hour)
- MLflow with Airflow
- MLflow with Kubeflow
- MLflow with other orchestration tools

### 12. Summary and Resources (0.5 hours)
- Key concepts review
- Common pitfalls
- Additional resources

## Files in This Module

- `lecture-notes.md` - Comprehensive 12,300-word lecture covering all topics
- `exercises.md` - 5 hands-on exercises (7-9 hours total)
- `quiz.md` - 30-question assessment
- `README.md` - This file

## Exercises

1. **Exercise 01**: MLflow Tracking Fundamentals (75 min)
   - Set up MLflow tracking server
   - Implement comprehensive tracking in training script
   - Compare multiple runs
   - Identify best performing model

2. **Exercise 02**: Model Registry & Lifecycle Management (90 min)
   - Register models from training runs
   - Manage model versions
   - Implement stage transitions
   - Load and serve models from registry

3. **Exercise 03**: Hyperparameter Optimization with Tracking (90 min)
   - Integrate MLflow with Optuna
   - Track hyperparameter search experiments
   - Visualize optimization progress
   - Select and register best model

4. **Exercise 04**: Advanced MLflow Features (60 min)
   - Create MLflow Project with conda environment
   - Implement custom pyfunc model
   - Enable autologging
   - Create parallel coordinates visualization

5. **Exercise 05**: End-to-End MLflow Pipeline (120 min)
   - Build complete training pipeline with tracking
   - Implement model registry automation
   - Create model serving endpoint
   - Monitor model performance

**Total Exercise Time**: 7.5 hours

## Key Takeaways

After completing this module, you should understand:

- ✅ Experiment tracking is essential for reproducibility and collaboration
- ✅ MLflow provides end-to-end ML lifecycle management
- ✅ Track parameters, metrics, artifacts, and models systematically
- ✅ Model Registry enables version control and lifecycle management
- ✅ MLflow integrates with major ML frameworks and tools
- ✅ Proper organization and naming conventions are critical
- ✅ Production deployments require centralized tracking servers

## Assessment

- **Quiz**: 30 questions covering all module topics (40 minutes)
- **Passing Score**: 80% (24/30 questions)
- **Practical Assessment**: Complete Exercise 05 with working end-to-end pipeline

## Real-World Context

**Industry Applications**:
- **Uber**: Uses MLflow to track experiments across 1,000+ ML models
- **Airbnb**: Tracks 100,000+ ML experiments annually with MLflow
- **Databricks**: Reports 90% reduction in time searching for experiments
- **Netflix**: Extensive experimentation for recommendation systems

**Common Use Cases**:
- Hyperparameter tuning experiments
- Model comparison and selection
- A/B testing of models
- Model versioning for production
- Reproducibility audits
- Team collaboration

**MLflow Adoption**:
- 60% of ML teams use MLflow (2024)
- Open-source leader in experiment tracking
- Used by Fortune 500 companies and startups
- Active community and ecosystem

## Project Connection

This module directly supports:
- **Project 01: ML CI/CD Pipeline** - Track experiments in automated pipelines
- **Project 02: Monitoring Dashboard** - Log models to registry for monitoring
- **Project 03: Experimentation** - Track A/B testing experiments
- **All Projects** - Systematic experiment tracking for all ML work

## Prerequisites Review

Before starting this module, ensure you have:
- [x] Python 3.9+ installed
- [x] pip and virtualenv installed
- [x] PostgreSQL or SQLite available (for backend store)
- [x] S3/GCS or local storage (for artifacts)
- [x] Completed Module 01: CI/CD Foundations
- [x] Basic ML knowledge (training, evaluation)

## Time Allocation

- **Lectures**: 12.5 hours (reading lecture notes and studying concepts)
- **Exercises**: 7.5 hours (hands-on practice)
- **Total**: 20 hours

**Recommended Study Schedule**:
- Week 1: Topics 1-4 (Introduction, Fundamentals, Tracking API, Model Registry)
- Week 2: Topics 5-8 (Projects, Models, Hyperparameter Optimization, Advanced Features)
- Week 3: Topics 9-12 (Alternative Tools, Best Practices, Integration, Summary)
- Week 4: Complete all exercises and assessment

## Next Module

**Module 03: Model Monitoring** - Learn to monitor ML models in production, detect drift, track performance, and trigger retraining automatically.

## Additional Resources

### Official Documentation
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [MLflow GitHub Repository](https://github.com/mlflow/mlflow)
- [MLflow API Reference](https://mlflow.org/docs/latest/python_api/index.html)
- [MLflow Examples](https://github.com/mlflow/mlflow/tree/master/examples)

### Tutorials
- [MLflow Tutorial](https://mlflow.org/docs/latest/tutorials-and-examples/tutorial.html)
- [Databricks MLflow Guide](https://docs.databricks.com/mlflow/index.html)
- [AWS MLflow on SageMaker](https://aws.amazon.com/blogs/machine-learning/managing-your-machine-learning-lifecycle-with-mlflow-and-amazon-sagemaker/)
- [GCP MLflow Integration](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)

### Books
- "Practical MLOps" by Noah Gift and Alfredo Deza
- "Building Machine Learning Powered Applications" by Emmanuel Ameisen
- "Machine Learning Engineering" by Andriy Burkov

### Online Courses
- [MLOps Specialization (Coursera)](https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops)
- [Full Stack Deep Learning](https://fullstackdeeplearning.com/)
- [Made With ML - MLOps](https://madewithml.com/)
- [Databricks Academy - MLflow](https://www.databricks.com/learn/training/mlflow-workshops)

### Community
- [MLflow Slack](https://mlflow.org/slack)
- [MLflow Mailing List](https://groups.google.com/g/mlflow-users)
- [Stack Overflow - MLflow](https://stackoverflow.com/questions/tagged/mlflow)
- [GitHub Discussions](https://github.com/mlflow/mlflow/discussions)

### Comparison Resources
- [MLflow vs W&B Comparison](https://www.sicara.fr/blog-technique/mlflow-vs-weights-and-biases)
- [Experiment Tracking Tools Comparison](https://neptune.ai/blog/best-ml-experiment-tracking-tools)
- [MLOps Tools Landscape](https://ml-ops.org/content/state-of-mlops)

## Getting Help

- **Stuck on setup?** Review the MLflow installation guide in lecture notes section 2.3
- **Tracking issues?** Check the Tracking API reference in section 3
- **Registry confusion?** Review Model Registry section 4
- **Technical problems?** Post in MLflow Slack or Stack Overflow
- **Need examples?** Check MLflow GitHub examples directory

## Success Checklist

Before moving to the next module, ensure you can:
- [ ] Set up MLflow tracking server with PostgreSQL backend
- [ ] Track experiments with parameters, metrics, and artifacts
- [ ] Log models and create model signatures
- [ ] Register models in the Model Registry
- [ ] Transition models between stages (Staging → Production)
- [ ] Load models from registry for inference
- [ ] Integrate MLflow with hyperparameter optimization
- [ ] Compare experiments using MLflow UI
- [ ] Query runs programmatically using search_runs
- [ ] Apply best practices for production tracking

## Installation Quick Start

```bash
# Install MLflow
pip install mlflow

# Install with extras (database support, cloud storage)
pip install mlflow[extras]

# Start local tracking server
mlflow ui

# Start production tracking server
mlflow server \
  --backend-store-uri postgresql://user:pass@localhost/mlflow \
  --default-artifact-root s3://my-bucket/mlflow \
  --host 0.0.0.0 \
  --port 5000
```

## Quick Reference

**Basic Tracking**:
```python
import mlflow

mlflow.set_experiment("my-experiment")

with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.001)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.sklearn.log_model(model, "model")
```

**Model Registry**:
```python
# Register model
mlflow.register_model("runs:/run-id/model", "my-model")

# Transition to production
client.transition_model_version_stage(
    name="my-model",
    version=3,
    stage="Production"
)

# Load model
model = mlflow.pyfunc.load_model("models:/my-model/Production")
```

---

**Estimated Completion Time**: 20 hours (12.5 hours content + 7.5 hours exercises)

**Difficulty**: Intermediate (assumes Module 01 completion and ML basics)

**Importance**: ⭐⭐⭐⭐⭐ (Critical for reproducible ML and team collaboration)

Ready to master experiment tracking? Start with `lecture-notes.md` and work through each section systematically. Happy tracking! 📊
