# Module 07: ML Governance and Compliance - Lecture Notes

**Duration**: 14.5 hours
**Level**: MLOps Engineer (2.5B)
**Last Updated**: October 2025

---

## Table of Contents

1. [ML Governance Fundamentals](#1-ml-governance-fundamentals)
2. [Model Approval Workflows](#2-model-approval-workflows)
3. [Fairness and Bias Detection](#3-fairness-and-bias-detection)
4. [Model Documentation](#4-model-documentation)
5. [Audit and Compliance](#5-audit-and-compliance)
6. [Governance Automation](#6-governance-automation)
7. [Summary and Best Practices](#7-summary-and-best-practices)

---

## 1. ML Governance Fundamentals

### 1.1 Why Governance Matters

**Real-World Incident - Amazon Hiring AI (2018)**:
- ML model trained on historical hiring data
- Learned to penalize resumes mentioning "women's" (e.g., "women's chess club")
- Systematically discriminated against female candidates
- **Cost**: Reputational damage, project cancellation
- **Root Cause**: No fairness validation, no bias testing, no governance process

**Regulatory Landscape (2025)**:
- **EU AI Act**: High-risk AI systems require compliance
- **GDPR**: Right to explanation for automated decisions (up to €20M fines)
- **CCPA**: Consumer privacy rights ($7,500 per violation)
- **NIST AI Framework**: Risk management standards
- **Industry Standards**: ISO/IEC 42001 (AI management systems)

### 1.2 Governance vs Compliance

**Governance** = Internal policies and processes
- Model approval workflows
- Fairness requirements
- Documentation standards
- Risk management

**Compliance** = External legal requirements
- GDPR, CCPA, AI Act
- Industry regulations (HIPAA for healthcare, PCI-DSS for payments)
- Audit requirements
- Data protection laws

---

## 2. Model Approval Workflows

### 2.1 Multi-Stage Approval System

```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import mlflow

class ApprovalStage(Enum):
    """Approval stages for model deployment."""
    TECHNICAL_REVIEW = "technical_review"
    FAIRNESS_ASSESSMENT = "fairness_assessment"
    BUSINESS_VALIDATION = "business_validation"
    COMPLIANCE_CHECK = "compliance_check"
    FINAL_APPROVAL = "final_approval"

class ApprovalStatus(Enum):
    """Status of approval."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REQUIRES_CHANGES = "requires_changes"

@dataclass
class ApprovalDecision:
    """Individual approval decision."""
    stage: ApprovalStage
    status: ApprovalStatus
    approver: str
    timestamp: datetime
    comments: str
    checklist_results: dict

class ModelApprovalWorkflow:
    """Multi-stage approval workflow for ML models."""

    def __init__(self, model_uri: str, model_metadata: dict):
        self.model_uri = model_uri
        self.model_metadata = model_metadata
        self.approvals: List[ApprovalDecision] = []
        self.current_stage = ApprovalStage.TECHNICAL_REVIEW

    def submit_approval(
        self,
        stage: ApprovalStage,
        approver: str,
        status: ApprovalStatus,
        checklist_results: dict,
        comments: str = ""
    ):
        """Submit approval decision for a stage."""

        decision = ApprovalDecision(
            stage=stage,
            status=status,
            approver=approver,
            timestamp=datetime.now(),
            comments=comments,
            checklist_results=checklist_results
        )

        self.approvals.append(decision)

        # Log to MLflow
        mlflow.log_dict(
            {
                'stage': stage.value,
                'status': status.value,
                'approver': approver,
                'timestamp': str(decision.timestamp),
                'comments': comments
            },
            f"approvals/{stage.value}_{decision.timestamp.isoformat()}.json"
        )

        # Update current stage
        if status == ApprovalStatus.APPROVED:
            self._advance_stage()
        elif status == ApprovalStatus.REJECTED:
            self.current_stage = None  # Workflow terminated

    def _advance_stage(self):
        """Move to next approval stage."""
        stages = list(ApprovalStage)
        current_idx = stages.index(self.current_stage)

        if current_idx < len(stages) - 1:
            self.current_stage = stages[current_idx + 1]
        else:
            self.current_stage = None  # All approvals complete

    def is_fully_approved(self) -> bool:
        """Check if model has passed all approval stages."""
        required_stages = set(ApprovalStage)
        approved_stages = {
            approval.stage for approval in self.approvals
            if approval.status == ApprovalStatus.APPROVED
        }

        return required_stages == approved_stages

    def get_approval_summary(self) -> dict:
        """Get summary of approval status."""
        return {
            'model_uri': self.model_uri,
            'current_stage': self.current_stage.value if self.current_stage else 'complete',
            'fully_approved': self.is_fully_approved(),
            'approvals': [
                {
                    'stage': a.stage.value,
                    'status': a.status.value,
                    'approver': a.approver,
                    'timestamp': a.timestamp.isoformat()
                }
                for a in self.approvals
            ]
        }

# Technical review checklist
def technical_review_checklist(model_uri: str) -> dict:
    """Technical review checklist."""
    import mlflow

    model = mlflow.pyfunc.load_model(model_uri)
    run = mlflow.get_run(model.metadata.run_id)

    checks = {}

    # 1. Model performance meets threshold
    accuracy = run.data.metrics.get('accuracy', 0)
    checks['accuracy_threshold'] = accuracy >= 0.85

    # 2. Training data size sufficient
    training_samples = run.data.params.get('training_samples', 0)
    checks['sufficient_data'] = int(training_samples) >= 10000

    # 3. Model complexity reasonable
    checks['model_complexity'] = True  # Check model size, inference time

    # 4. All required metrics logged
    required_metrics = ['accuracy', 'precision', 'recall', 'f1_score']
    checks['metrics_logged'] = all(m in run.data.metrics for m in required_metrics)

    # 5. Model artifacts present
    checks['artifacts_present'] = len(run.info.artifact_uri) > 0

    # 6. Code version tracked
    checks['code_versioned'] = 'git_commit' in run.data.tags

    return {
        'all_passed': all(checks.values()),
        'checks': checks
    }

# Usage example
workflow = ModelApprovalWorkflow(
    model_uri="models:/credit-model/staging",
    model_metadata={'version': '2.3', 'created_by': 'ml-team'}
)

# Technical review
tech_results = technical_review_checklist("models:/credit-model/staging")
workflow.submit_approval(
    stage=ApprovalStage.TECHNICAL_REVIEW,
    approver="senior-ml-engineer@company.com",
    status=ApprovalStatus.APPROVED if tech_results['all_passed'] else ApprovalStatus.REQUIRES_CHANGES,
    checklist_results=tech_results,
    comments="All technical requirements met"
)

# Fairness assessment (next section)
# Business validation
# Compliance check
# Final approval

# Check if ready for production
if workflow.is_fully_approved():
    print("✅ Model approved for production deployment")
    # Promote to production
    client = mlflow.MlflowClient()
    client.transition_model_version_stage(
        name="credit-model",
        version="2.3",
        stage="Production"
    )
else:
    print(f"⏸️ Currently at stage: {workflow.current_stage}")
```

---

## 3. Fairness and Bias Detection

### 3.1 Fairness Metrics with Fairlearn

```python
import pandas as pd
import numpy as np
from fairlearn.metrics import (
    demographic_parity_difference,
    demographic_parity_ratio,
    equalized_odds_difference,
    MetricFrame
)
from sklearn.metrics import accuracy_score, precision_score, recall_score

class FairnessAssessment:
    """Comprehensive fairness assessment for ML models."""

    def __init__(
        self,
        sensitive_features: List[str],
        fairness_thresholds: dict = None
    ):
        self.sensitive_features = sensitive_features
        self.fairness_thresholds = fairness_thresholds or {
            'demographic_parity_diff': 0.1,
            'equalized_odds_diff': 0.1,
            'accuracy_parity': 0.05
        }

    def evaluate_fairness(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        sensitive_features_df: pd.DataFrame
    ) -> dict:
        """
        Evaluate fairness across multiple metrics and sensitive features.

        Args:
            y_true: True labels
            y_pred: Predicted labels
            sensitive_features_df: DataFrame with sensitive features

        Returns:
            Comprehensive fairness report
        """
        report = {
            'overall_metrics': self._calculate_overall_metrics(y_true, y_pred),
            'fairness_by_feature': {},
            'violations': [],
            'fairness_score': 0.0
        }

        for feature in self.sensitive_features:
            feature_report = self._evaluate_feature_fairness(
                y_true,
                y_pred,
                sensitive_features_df[feature]
            )

            report['fairness_by_feature'][feature] = feature_report

            # Check for violations
            if feature_report['demographic_parity_diff'] > self.fairness_thresholds['demographic_parity_diff']:
                report['violations'].append({
                    'feature': feature,
                    'metric': 'demographic_parity',
                    'value': feature_report['demographic_parity_diff'],
                    'threshold': self.fairness_thresholds['demographic_parity_diff']
                })

            if feature_report['equalized_odds_diff'] > self.fairness_thresholds['equalized_odds_diff']:
                report['violations'].append({
                    'feature': feature,
                    'metric': 'equalized_odds',
                    'value': feature_report['equalized_odds_diff'],
                    'threshold': self.fairness_thresholds['equalized_odds_diff']
                })

        # Calculate overall fairness score (0-100)
        report['fairness_score'] = self._calculate_fairness_score(report)

        return report

    def _calculate_overall_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> dict:
        """Calculate overall model metrics."""
        return {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted')
        }

    def _evaluate_feature_fairness(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        sensitive_feature: pd.Series
    ) -> dict:
        """Evaluate fairness for a single sensitive feature."""

        # Demographic parity
        dp_diff = demographic_parity_difference(
            y_true, y_pred, sensitive_features=sensitive_feature
        )
        dp_ratio = demographic_parity_ratio(
            y_true, y_pred, sensitive_features=sensitive_feature
        )

        # Equalized odds
        eo_diff = equalized_odds_difference(
            y_true, y_pred, sensitive_features=sensitive_feature
        )

        # Per-group metrics
        metric_frame = MetricFrame(
            metrics={
                'accuracy': accuracy_score,
                'precision': lambda y_t, y_p: precision_score(y_t, y_p, average='binary'),
                'recall': lambda y_t, y_p: recall_score(y_t, y_p, average='binary')
            },
            y_true=y_true,
            y_pred=y_pred,
            sensitive_features=sensitive_feature
        )

        return {
            'demographic_parity_diff': abs(dp_diff),
            'demographic_parity_ratio': dp_ratio,
            'equalized_odds_diff': abs(eo_diff),
            'group_metrics': metric_frame.by_group.to_dict(),
            'metric_differences': {
                metric: metric_frame.difference(method='between_groups')[metric]
                for metric in ['accuracy', 'precision', 'recall']
            }
        }

    def _calculate_fairness_score(self, report: dict) -> float:
        """Calculate overall fairness score (0-100)."""
        if not report['violations']:
            return 100.0

        # Penalize based on number and severity of violations
        penalty = 0
        for violation in report['violations']:
            severity = violation['value'] / violation['threshold']
            penalty += min(severity * 10, 25)  # Max 25 points per violation

        return max(0.0, 100.0 - penalty)

    def generate_fairness_report(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        sensitive_features_df: pd.DataFrame,
        save_path: str = None
    ) -> str:
        """Generate human-readable fairness report."""

        results = self.evaluate_fairness(y_true, y_pred, sensitive_features_df)

        report_lines = [
            "=" * 60,
            "FAIRNESS ASSESSMENT REPORT",
            "=" * 60,
            "",
            f"Overall Fairness Score: {results['fairness_score']:.1f}/100",
            "",
            "Overall Model Performance:",
            f"  Accuracy:  {results['overall_metrics']['accuracy']:.3f}",
            f"  Precision: {results['overall_metrics']['precision']:.3f}",
            f"  Recall:    {results['overall_metrics']['recall']:.3f}",
            "",
            "Fairness by Sensitive Feature:",
            ""
        ]

        for feature, metrics in results['fairness_by_feature'].items():
            report_lines.extend([
                f"  {feature.upper()}:",
                f"    Demographic Parity Difference: {metrics['demographic_parity_diff']:.3f}",
                f"    Equalized Odds Difference:     {metrics['equalized_odds_diff']:.3f}",
                ""
            ])

        if results['violations']:
            report_lines.extend([
                "⚠️  FAIRNESS VIOLATIONS DETECTED:",
                ""
            ])
            for violation in results['violations']:
                report_lines.append(
                    f"  • {violation['feature']} - {violation['metric']}: "
                    f"{violation['value']:.3f} (threshold: {violation['threshold']:.3f})"
                )
        else:
            report_lines.append("✅ No fairness violations detected")

        report_text = "\n".join(report_lines)

        if save_path:
            with open(save_path, 'w') as f:
                f.write(report_text)

        return report_text

# Usage example
fairness_assessor = FairnessAssessment(
    sensitive_features=['gender', 'race', 'age_group'],
    fairness_thresholds={
        'demographic_parity_diff': 0.1,
        'equalized_odds_diff': 0.1,
        'accuracy_parity': 0.05
    }
)

# Evaluate model
fairness_report = fairness_assessor.generate_fairness_report(
    y_true=test_labels,
    y_pred=predictions,
    sensitive_features_df=test_data[['gender', 'race', 'age_group']],
    save_path='fairness_report.txt'
)

print(fairness_report)
```

### 3.2 Bias Mitigation Strategies

```python
from fairlearn.reductions import ExponentiatedGradient, DemographicParity
from sklearn.ensemble import RandomForestClassifier

class BiasMitigationPipeline:
    """Pipeline for detecting and mitigating bias."""

    def __init__(self, base_estimator, mitigation_method='reweighting'):
        self.base_estimator = base_estimator
        self.mitigation_method = mitigation_method
        self.mitigated_model = None

    def fit(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        sensitive_features: pd.DataFrame
    ):
        """Train model with bias mitigation."""

        if self.mitigation_method == 'exponentiated_gradient':
            # Use Fairlearn's ExponentiatedGradient
            mitigator = ExponentiatedGradient(
                self.base_estimator,
                constraints=DemographicParity()
            )

            mitigator.fit(X, y, sensitive_features=sensitive_features)
            self.mitigated_model = mitigator

        elif self.mitigation_method == 'reweighting':
            # Reweight samples to balance sensitive groups
            from sklearn.utils.class_weight import compute_sample_weight

            # Compute weights for demographic parity
            sample_weights = compute_sample_weight(
                class_weight='balanced',
                y=sensitive_features.iloc[:, 0]
            )

            self.base_estimator.fit(X, y, sample_weight=sample_weights)
            self.mitigated_model = self.base_estimator

        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions with mitigated model."""
        return self.mitigated_model.predict(X)

# Compare original vs mitigated model
original_model = RandomForestClassifier()
original_model.fit(X_train, y_train)

mitigated_pipeline = BiasMitigationPipeline(
    RandomForestClassifier(),
    mitigation_method='exponentiated_gradient'
)
mitigated_pipeline.fit(X_train, y_train, sensitive_features_train)

# Evaluate both
original_fairness = fairness_assessor.evaluate_fairness(
    y_test, original_model.predict(X_test), sensitive_features_test
)

mitigated_fairness = fairness_assessor.evaluate_fairness(
    y_test, mitigated_pipeline.predict(X_test), sensitive_features_test
)

print(f"Original Fairness Score: {original_fairness['fairness_score']:.1f}")
print(f"Mitigated Fairness Score: {mitigated_fairness['fairness_score']:.1f}")
```

---

## 4. Model Documentation

### 4.1 Automated Model Card Generation

```python
from dataclasses import dataclass, asdict
from typing import List, Dict
import json

@dataclass
class ModelCard:
    """Model card following https://arxiv.org/abs/1810.03993."""

    # Model details
    model_name: str
    model_version: str
    model_type: str
    training_date: str
    developers: List[str]
    contact: str

    # Intended use
    intended_use: str
    intended_users: List[str]
    out_of_scope_uses: List[str]

    # Training data
    training_data_description: str
    training_data_size: int
    data_preprocessing: List[str]

    # Evaluation data
    evaluation_data_description: str
    evaluation_data_size: int

    # Performance metrics
    overall_performance: Dict[str, float]
    performance_by_group: Dict[str, Dict[str, float]]

    # Fairness metrics
    fairness_assessment: Dict[str, any]

    # Ethical considerations
    ethical_considerations: List[str]
    known_limitations: List[str]
    potential_biases: List[str]

    # Technical specifications
    model_architecture: str
    hyperparameters: Dict[str, any]
    compute_requirements: str

    def to_markdown(self) -> str:
        """Generate markdown model card."""

        md = f"""# Model Card: {self.model_name}

## Model Details

**Version:** {self.model_version}
**Type:** {self.model_type}
**Training Date:** {self.training_date}
**Developers:** {', '.join(self.developers)}
**Contact:** {self.contact}

## Intended Use

**Primary Use:** {self.intended_use}

**Intended Users:**
{self._list_to_md(self.intended_users)}

**Out of Scope Uses:**
{self._list_to_md(self.out_of_scope_uses)}

## Training Data

{self.training_data_description}

**Size:** {self.training_data_size:,} samples

**Preprocessing:**
{self._list_to_md(self.data_preprocessing)}

## Evaluation

**Evaluation Data:** {self.evaluation_data_description}
**Size:** {self.evaluation_data_size:,} samples

### Overall Performance

{self._dict_to_md_table(self.overall_performance)}

### Performance by Group

{self._nested_dict_to_md(self.performance_by_group)}

## Fairness Assessment

**Fairness Score:** {self.fairness_assessment.get('fairness_score', 'N/A')}/100

**Violations:**
{self._list_to_md([f"{v['feature']} - {v['metric']}: {v['value']:.3f}" for v in self.fairness_assessment.get('violations', [])])}

## Ethical Considerations

{self._list_to_md(self.ethical_considerations)}

## Limitations

{self._list_to_md(self.known_limitations)}

## Potential Biases

{self._list_to_md(self.potential_biases)}

## Technical Specifications

**Architecture:** {self.model_architecture}

**Hyperparameters:**
```json
{json.dumps(self.hyperparameters, indent=2)}
```

**Compute Requirements:** {self.compute_requirements}

---

*This model card was generated automatically following the Model Cards for Model Reporting framework.*
"""
        return md

    def _list_to_md(self, items: List[str]) -> str:
        """Convert list to markdown bullet points."""
        return '\n'.join(f"- {item}" for item in items) if items else "- None"

    def _dict_to_md_table(self, d: Dict[str, float]) -> str:
        """Convert dict to markdown table."""
        rows = [f"| {k} | {v:.4f} |" for k, v in d.items()]
        return "| Metric | Value |\n|--------|-------|\n" + '\n'.join(rows)

    def _nested_dict_to_md(self, d: Dict[str, Dict[str, float]]) -> str:
        """Convert nested dict to markdown."""
        result = []
        for group, metrics in d.items():
            result.append(f"\n**{group}:**\n")
            result.append(self._dict_to_md_table(metrics))
        return '\n'.join(result)

    def save(self, filepath: str):
        """Save model card."""
        # Save as JSON
        with open(f"{filepath}.json", 'w') as f:
            json.dump(asdict(self), f, indent=2)

        # Save as Markdown
        with open(f"{filepath}.md", 'w') as f:
            f.write(self.to_markdown())

# Usage
model_card = ModelCard(
    model_name="Credit Risk Predictor",
    model_version="2.3.0",
    model_type="Random Forest Classifier",
    training_date="2025-10-25",
    developers=["ML Team", "Risk Analytics"],
    contact="ml-ops@company.com",
    intended_use="Predict credit default risk for loan applications",
    intended_users=["Loan Officers", "Risk Analysts"],
    out_of_scope_uses=["Criminal justice", "Employment decisions"],
    training_data_description="Historical loan applications from 2020-2024",
    training_data_size=500000,
    data_preprocessing=[
        "Missing value imputation",
        "Feature scaling (StandardScaler)",
        "Categorical encoding (one-hot)"
    ],
    evaluation_data_description="Hold-out test set from 2024",
    evaluation_data_size=50000,
    overall_performance={
        'accuracy': 0.87,
        'precision': 0.84,
        'recall': 0.82,
        'f1_score': 0.83,
        'auc_roc': 0.91
    },
    performance_by_group={
        'gender_male': {'accuracy': 0.88, 'precision': 0.85},
        'gender_female': {'accuracy': 0.86, 'precision': 0.83}
    },
    fairness_assessment=fairness_results,
    ethical_considerations=[
        "Model may perpetuate historical lending biases",
        "Requires human review for all denials",
        "Regular fairness audits required"
    ],
    known_limitations=[
        "Performance degrades for thin credit files",
        "Not validated for self-employed applicants",
        "Requires retraining quarterly"
    ],
    potential_biases=[
        "Training data over-represents urban applicants",
        "Historical data reflects past discriminatory practices"
    ],
    model_architecture="Random Forest with 100 trees",
    hyperparameters={
        'n_estimators': 100,
        'max_depth': 10,
        'min_samples_split': 5
    },
    compute_requirements="CPU: 4 cores, RAM: 8GB, Inference: <100ms"
)

model_card.save('model_cards/credit_risk_v2_3_0')
```

---

## 5. Audit and Compliance

### 5.1 Tamper-Proof Audit Logging

```python
import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any

class AuditLog:
    """Immutable audit log using Merkle tree."""

    def __init__(self):
        self.entries: List[Dict[str, Any]] = []
        self.hashes: List[str] = []

    def log_event(
        self,
        event_type: str,
        user: str,
        action: str,
        details: dict,
        model_version: str = None
    ):
        """Log an auditable event."""

        entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'user': user,
            'action': action,
            'details': details,
            'model_version': model_version,
            'previous_hash': self.hashes[-1] if self.hashes else '0' * 64
        }

        # Calculate hash (includes previous hash for chain integrity)
        entry_json = json.dumps(entry, sort_keys=True)
        entry_hash = hashlib.sha256(entry_json.encode()).hexdigest()

        entry['hash'] = entry_hash

        self.entries.append(entry)
        self.hashes.append(entry_hash)

        # Persist to database
        self._persist_entry(entry)

    def verify_integrity(self) -> bool:
        """Verify audit log has not been tampered with."""

        for i, entry in enumerate(self.entries):
            # Recalculate hash
            entry_copy = entry.copy()
            stored_hash = entry_copy.pop('hash')

            recalculated_hash = hashlib.sha256(
                json.dumps(entry_copy, sort_keys=True).encode()
            ).hexdigest()

            if stored_hash != recalculated_hash:
                print(f"⚠️ Tampering detected at entry {i}")
                return False

            # Verify chain
            if i > 0 and entry['previous_hash'] != self.entries[i-1]['hash']:
                print(f"⚠️ Chain broken at entry {i}")
                return False

        return True

    def _persist_entry(self, entry: dict):
        """Persist entry to database."""
        # In production: write to PostgreSQL, S3, or blockchain
        pass

    def query_events(
        self,
        event_type: str = None,
        user: str = None,
        start_date: datetime = None,
        end_date: datetime = None
    ) -> List[dict]:
        """Query audit log entries."""

        results = self.entries

        if event_type:
            results = [e for e in results if e['event_type'] == event_type]

        if user:
            results = [e for e in results if e['user'] == user]

        if start_date:
            results = [
                e for e in results
                if datetime.fromisoformat(e['timestamp']) >= start_date
            ]

        if end_date:
            results = [
                e for e in results
                if datetime.fromisoformat(e['timestamp']) <= end_date
            ]

        return results

# Global audit logger
audit_logger = AuditLog()

# Log various events
audit_logger.log_event(
    event_type='model_training',
    user='ml-engineer@company.com',
    action='train_model',
    details={
        'model_type': 'RandomForest',
        'training_samples': 100000,
        'accuracy': 0.87
    },
    model_version='2.3.0'
)

audit_logger.log_event(
    event_type='model_approval',
    user='compliance-officer@company.com',
    action='approve_deployment',
    details={
        'approval_stage': 'compliance_check',
        'fairness_score': 95.0,
        'risk_level': 'low'
    },
    model_version='2.3.0'
)

audit_logger.log_event(
    event_type='model_prediction',
    user='api-service',
    action='batch_predict',
    details={
        'num_predictions': 5000,
        'avg_confidence': 0.82
    },
    model_version='2.3.0'
)

# Verify integrity
if audit_logger.verify_integrity():
    print("✅ Audit log integrity verified")
else:
    print("⚠️ Audit log has been tampered with!")

# Query specific events
approval_events = audit_logger.query_events(event_type='model_approval')
print(f"Found {len(approval_events)} approval events")
```

### 5.2 GDPR Compliance Implementation

```python
class GDPRCompliance:
    """GDPR compliance for ML systems."""

    def __init__(self, model_uri: str, data_storage):
        self.model_uri = model_uri
        self.data_storage = data_storage

    def handle_right_to_explanation(
        self,
        user_id: str,
        prediction_id: str
    ) -> dict:
        """
        GDPR Article 22: Right to explanation for automated decisions.

        Args:
            user_id: User requesting explanation
            prediction_id: ID of prediction to explain

        Returns:
            Human-readable explanation
        """
        import shap
        import mlflow

        # Load model and prediction data
        model = mlflow.pyfunc.load_model(self.model_uri)
        prediction_data = self.data_storage.get_prediction(prediction_id)

        # Verify user owns this prediction
        if prediction_data['user_id'] != user_id:
            raise PermissionError("User not authorized")

        # Generate SHAP explanation
        explainer = shap.TreeExplainer(model._model_impl.python_model)
        shap_values = explainer.shap_values(prediction_data['features'])

        # Create human-readable explanation
        explanation = self._format_explanation(
            shap_values,
            prediction_data['features'],
            prediction_data['prediction']
        )

        # Log explanation request (audit trail)
        audit_logger.log_event(
            event_type='gdpr_explanation',
            user=user_id,
            action='request_explanation',
            details={'prediction_id': prediction_id}
        )

        return explanation

    def handle_right_to_erasure(self, user_id: str):
        """
        GDPR Article 17: Right to be forgotten.

        Args:
            user_id: User requesting data deletion
        """
        # 1. Delete user data from training sets
        self.data_storage.delete_user_data(user_id)

        # 2. Mark user in deletion log
        self.data_storage.mark_user_deleted(user_id)

        # 3. Trigger model retraining without user's data
        self._trigger_retraining_without_user(user_id)

        # 4. Delete predictions involving user
        self.data_storage.delete_user_predictions(user_id)

        # 5. Log erasure (required for compliance)
        audit_logger.log_event(
            event_type='gdpr_erasure',
            user='system',
            action='delete_user_data',
            details={'user_id': user_id, 'timestamp': datetime.now().isoformat()}
        )

    def _format_explanation(
        self,
        shap_values: np.ndarray,
        features: dict,
        prediction: float
    ) -> str:
        """Format SHAP values into human-readable text."""

        # Get top contributing features
        feature_importance = sorted(
            zip(features.keys(), shap_values[0]),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:5]

        explanation = f"Decision: {'Approved' if prediction > 0.5 else 'Denied'}\n\n"
        explanation += "Top factors influencing this decision:\n\n"

        for feature, importance in feature_importance:
            direction = "increased" if importance > 0 else "decreased"
            explanation += f"- {feature}: {direction} likelihood by {abs(importance):.2%}\n"

        return explanation

    def _trigger_retraining_without_user(self, user_id: str):
        """Trigger retraining excluding deleted user's data."""
        from airflow.api.client.local_client import Client

        client = Client(None, None)
        client.trigger_dag(
            dag_id='retrain_without_user',
            conf={'excluded_user': user_id}
        )
```

---

## 6. Governance Automation

### 6.1 Automated Compliance Checking

```python
class AutomatedGovernanceChecks:
    """Automated governance and compliance checks."""

    def __init__(self):
        self.checks = []

    def run_all_checks(
        self,
        model_uri: str,
        test_data: pd.DataFrame,
        sensitive_features: pd.DataFrame
    ) -> dict:
        """Run all governance checks."""

        results = {
            'timestamp': datetime.now().isoformat(),
            'model_uri': model_uri,
            'checks': {},
            'overall_pass': True
        }

        # 1. Fairness check
        fairness_result = self._check_fairness(
            model_uri, test_data, sensitive_features
        )
        results['checks']['fairness'] = fairness_result
        if not fairness_result['passed']:
            results['overall_pass'] = False

        # 2. Performance check
        performance_result = self._check_performance(model_uri, test_data)
        results['checks']['performance'] = performance_result
        if not performance_result['passed']:
            results['overall_pass'] = False

        # 3. Documentation check
        doc_result = self._check_documentation(model_uri)
        results['checks']['documentation'] = doc_result
        if not doc_result['passed']:
            results['overall_pass'] = False

        # 4. Audit trail check
        audit_result = self._check_audit_trail(model_uri)
        results['checks']['audit_trail'] = audit_result
        if not audit_result['passed']:
            results['overall_pass'] = False

        return results

    def _check_fairness(
        self,
        model_uri: str,
        test_data: pd.DataFrame,
        sensitive_features: pd.DataFrame
    ) -> dict:
        """Check fairness requirements."""
        # Load model and make predictions
        import mlflow
        model = mlflow.pyfunc.load_model(model_uri)
        predictions = model.predict(test_data.drop('label', axis=1))

        # Run fairness assessment
        assessor = FairnessAssessment(['gender', 'race', 'age_group'])
        fairness_report = assessor.evaluate_fairness(
            test_data['label'],
            predictions,
            sensitive_features
        )

        return {
            'passed': fairness_report['fairness_score'] >= 80.0,
            'score': fairness_report['fairness_score'],
            'violations': fairness_report['violations']
        }

    def _check_performance(self, model_uri: str, test_data: pd.DataFrame) -> dict:
        """Check performance meets requirements."""
        import mlflow
        from sklearn.metrics import accuracy_score

        model = mlflow.pyfunc.load_model(model_uri)
        predictions = model.predict(test_data.drop('label', axis=1))

        accuracy = accuracy_score(test_data['label'], predictions)

        return {
            'passed': accuracy >= 0.85,
            'accuracy': accuracy,
            'threshold': 0.85
        }

    def _check_documentation(self, model_uri: str) -> dict:
        """Check model card exists and is complete."""
        import mlflow

        run = mlflow.get_run(model_uri.split('/')[-1])

        # Check required documentation
        required_tags = [
            'model_card_url',
            'training_date',
            'data_source',
            'intended_use'
        ]

        missing_tags = [tag for tag in required_tags if tag not in run.data.tags]

        return {
            'passed': len(missing_tags) == 0,
            'missing_documentation': missing_tags
        }

    def _check_audit_trail(self, model_uri: str) -> dict:
        """Check complete audit trail exists."""

        # Query audit log for this model
        model_version = model_uri.split('/')[-1]
        events = audit_logger.query_events(model_version=model_version)

        required_events = ['model_training', 'model_approval', 'fairness_assessment']
        logged_event_types = set(e['event_type'] for e in events)

        missing_events = [e for e in required_events if e not in logged_event_types]

        return {
            'passed': len(missing_events) == 0,
            'missing_events': missing_events,
            'total_events': len(events)
        }

# Integrate into CI/CD
governance = AutomatedGovernanceChecks()

compliance_results = governance.run_all_checks(
    model_uri="models:/credit-model/staging",
    test_data=test_df,
    sensitive_features=test_df[['gender', 'race', 'age_group']]
)

if compliance_results['overall_pass']:
    print("✅ All governance checks passed - approved for production")
else:
    print("❌ Governance checks failed:")
    for check_name, check_result in compliance_results['checks'].items():
        if not check_result['passed']:
            print(f"  - {check_name}: {check_result}")

    raise Exception("Governance requirements not met")
```

---

## 7. Summary and Best Practices

### Key Takeaways

1. **Governance is Mandatory**: Not optional in regulated industries
2. **Automate Checks**: Integrate into CI/CD pipelines
3. **Document Everything**: Model cards, audit logs, fairness reports
4. **Measure Fairness**: Multiple metrics across sensitive features
5. **Tamper-Proof Logs**: Use cryptographic hashing for audit trails
6. **GDPR Compliance**: Right to explanation and erasure

### Best Practices

- **Multi-Stage Approvals**: Technical, fairness, business, compliance
- **Regular Audits**: Quarterly fairness assessments
- **Version Control**: Track all governance artifacts
- **Transparency**: Make model cards publicly available
- **Continuous Monitoring**: Track fairness in production
- **Human Oversight**: Critical decisions require human review

---

**Total Words**: ~5,400 words

**Next Module**: Module 08 - Production Operations
