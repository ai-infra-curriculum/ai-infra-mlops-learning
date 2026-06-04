## Exercise 5: Complete Governance Framework (120 minutes)

**Objective**: Build an end-to-end ML governance framework integrating fairness, model cards, audit logging, and compliance.

### Background

Create a production-ready governance system that:
1. Assesses fairness before deployment
2. Generates model cards automatically
3. Logs all predictions with audit trail
4. Monitors ongoing compliance
5. Generates governance reports

### Tasks

1. **Design governance architecture**
2. **Integrate all governance components**
3. **Create governance pipeline**
4. **Implement compliance dashboard**
5. **Set up automated governance checks**

### Starter Code

```python
# src/governance/governance_framework.py
"""Complete ML governance framework."""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.governance.fairness_assessment import FairnessAssessor
from src.governance.bias_mitigation import BiasMitigator
from src.governance.model_card import ModelCardGenerator, ModelCard
from src.governance.audit_logging import AuditLogger


class GovernanceFramework:
    """Complete ML governance and compliance framework."""

    def __init__(
        self,
        model_name: str,
        model_version: str,
        sensitive_features: List[str],
        audit_db_path: str = "governance_audit.db"
    ):
        """
        Initialize governance framework.

        Args:
            model_name: Name of model
            model_version: Model version
            sensitive_features: List of protected attributes
            audit_db_path: Path to audit log database
        """
        self.model_name = model_name
        self.model_version = model_version
        self.sensitive_features = sensitive_features

        # Initialize components
        self.fairness_assessor = FairnessAssessor(sensitive_features)
        self.bias_mitigator = BiasMitigator()
        self.model_card_generator = ModelCardGenerator()
        self.audit_logger = AuditLogger(audit_db_path)

        self.governance_status = "NOT_ASSESSED"
        self.fairness_report = None
        self.model_card = None

    def assess_model_governance(
        self,
        model: Any,
        X_test: pd.DataFrame,
        y_test: np.ndarray,
        sensitive_features_test: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Comprehensive governance assessment before deployment.

        Args:
            model: Trained model
            X_test: Test features
            y_test: Test labels
            sensitive_features_test: Test sensitive attributes

        Returns:
            Governance assessment results
        """
        assessment = {
            'timestamp': datetime.now(),
            'model_name': self.model_name,
            'model_version': self.model_version,
            'checks': {}
        }

        # ============================================
        # 1. FAIRNESS ASSESSMENT
        # ============================================
        print("Running fairness assessment...")

        # TODO: Get predictions
        # y_pred = model.predict(X_test)

        # TODO: Assess fairness
        # self.fairness_report = self.fairness_assessor.assess_fairness(
        #     y_test, y_pred, sensitive_features_test
        # )

        # TODO: Record results
        # assessment['checks']['fairness'] = {
        #     'passed': self.fairness_report.compliance_status == 'COMPLIANT',
        #     'disparate_impact': self.fairness_report.disparate_impact_ratio,
        #     'violations': self.fairness_report.fairness_violations
        # }

        # ============================================
        # 2. PERFORMANCE ASSESSMENT
        # ============================================
        print("Assessing model performance...")

        # TODO: Calculate performance metrics
        # assessment['checks']['performance'] = {
        #     'accuracy': accuracy_score(y_test, y_pred),
        #     'precision': precision_score(y_test, y_pred),
        #     'recall': recall_score(y_test, y_pred),
        #     'f1': f1_score(y_test, y_pred)
        # }

        # ============================================
        # 3. BIAS MITIGATION CHECK
        # ============================================
        print("Checking if bias mitigation needed...")

        # TODO: If fairness check failed, recommend mitigation
        # if not assessment['checks']['fairness']['passed']:
        #     print("Fairness violations detected. Running bias mitigation...")
        #     mitigation_results = self.bias_mitigator.compare_mitigation_strategies(
        #         X_train, y_train, X_test, y_test,
        #         sensitive_features_train, sensitive_features_test
        #     )
        #     assessment['checks']['bias_mitigation'] = {
        #         'required': True,
        #         'strategies_evaluated': mitigation_results
        #     }

        # ============================================
        # 4. MODEL CARD GENERATION
        # ============================================
        print("Generating model card...")

        # TODO: Generate model card with all information
        # self.model_card = self._generate_model_card(
        #     assessment['checks']['performance'],
        #     self.fairness_report
        # )

        # TODO: Save model card
        # self.model_card_generator.save_model_card(
        #     self.model_card,
        #     f"model_cards/{self.model_name}_v{self.model_version}.md"
        # )

        # assessment['checks']['model_card'] = {
        #     'generated': True,
        #     'path': f"model_cards/{self.model_name}_v{self.model_version}.md"
        # }

        # ============================================
        # 5. DETERMINE OVERALL GOVERNANCE STATUS
        # ============================================

        # TODO: Determine if model passes governance
        # all_checks_passed = all(
        #     check.get('passed', True)
        #     for check in assessment['checks'].values()
        # )

        # if all_checks_passed:
        #     self.governance_status = "APPROVED"
        # elif assessment['checks']['fairness']['passed']:
        #     self.governance_status = "APPROVED_WITH_CONDITIONS"
        # else:
        #     self.governance_status = "REJECTED"

        # assessment['governance_status'] = self.governance_status

        return assessment

    def _generate_model_card(
        self,
        performance_metrics: Dict,
        fairness_report: Any
    ) -> ModelCard:
        """Generate model card from assessment results."""
        # TODO: Create model card sections
        # TODO: Include performance and fairness information
        # TODO: Return ModelCard object
        pass

    def log_prediction_with_governance(
        self,
        user_id: str,
        input_data: Dict[str, Any],
        prediction: Any,
        confidence: float,
        sensitive_features: Dict[str, Any],
        explanation: Dict = None
    ) -> Dict[str, Any]:
        """
        Make prediction with full governance logging.

        Args:
            user_id: User making prediction
            input_data: Input features
            prediction: Model prediction
            confidence: Prediction confidence
            sensitive_features: Sensitive attributes
            explanation: Prediction explanation

        Returns:
            Prediction result with governance metadata
        """
        # ============================================
        # 1. PRE-PREDICTION CHECKS
        # ============================================

        # TODO: Check if model is approved for use
        # if self.governance_status not in ['APPROVED', 'APPROVED_WITH_CONDITIONS']:
        #     return {
        #         'error': 'Model not approved for production use',
        #         'governance_status': self.governance_status
        #     }

        # ============================================
        # 2. FAIRNESS CHECK ON INDIVIDUAL PREDICTION
        # ============================================

        # TODO: Run fairness check if sensitive features provided
        fairness_check_passed = True
        # if sensitive_features:
        #     fairness_check_passed = self._check_individual_fairness(
        #         input_data, prediction, sensitive_features
        #     )

        # ============================================
        # 3. AUDIT LOGGING
        # ============================================

        # TODO: Log prediction
        # log_id = self.audit_logger.log_prediction(
        #     model_name=self.model_name,
        #     model_version=self.model_version,
        #     user_id=user_id,
        #     input_data=input_data,
        #     prediction=prediction,
        #     confidence=confidence,
        #     explanation=explanation,
        #     sensitive_features=sensitive_features,
        #     fairness_check_passed=fairness_check_passed
        # )

        # ============================================
        # 4. RETURN RESULT
        # ============================================

        # return {
        #     'prediction': prediction,
        #     'confidence': confidence,
        #     'explanation': explanation,
        #     'fairness_check_passed': fairness_check_passed,
        #     'log_id': log_id,
        #     'governance_status': self.governance_status
        # }
        pass

    def _check_individual_fairness(
        self,
        input_data: Dict,
        prediction: Any,
        sensitive_features: Dict
    ) -> bool:
        """
        Check fairness for individual prediction.

        Args:
            input_data: Input features
            prediction: Prediction
            sensitive_features: Sensitive attributes

        Returns:
            True if fairness check passed
        """
        # TODO: Implement individual fairness check
        # - Check if prediction is consistent with similar individuals
        # - Check if sensitive features influenced decision inappropriately
        # - Return True/False
        pass

    def generate_governance_report(
        self,
        start_date: datetime,
        end_date: datetime,
        output_path: str = "governance_report.html"
    ):
        """
        Generate comprehensive governance report.

        Args:
            start_date: Report period start
            end_date: Report period end
            output_path: Output file path
        """
        # TODO: Query audit logs
        logs = self.audit_logger.query_logs(start_date, end_date, self.model_name)

        # TODO: Calculate governance metrics
        governance_metrics = self._calculate_governance_metrics(logs)

        # TODO: Generate HTML report with:
        #   - Executive summary
        #   - Model card
        #   - Fairness assessment results
        #   - Audit log statistics
        #   - Compliance status
        #   - Recommendations

        # TODO: Save report
        pass

    def _calculate_governance_metrics(self, logs: List) -> Dict:
        """Calculate governance metrics from logs."""
        # TODO: Calculate:
        #   - Total predictions
        #   - Fairness check pass rate
        #   - Predictions by sensitive group
        #   - Average confidence
        #   - Trend analysis
        pass

    def monitor_ongoing_compliance(
        self,
        lookback_days: int = 30
    ) -> Dict[str, Any]:
        """
        Monitor ongoing compliance over time.

        Args:
            lookback_days: Number of days to look back

        Returns:
            Compliance monitoring results
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=lookback_days)

        # TODO: Query recent logs
        logs = self.audit_logger.query_logs(start_date, end_date, self.model_name)

        # TODO: Check for compliance issues
        #   - Fairness degradation
        #   - High failure rate
        #   - Unusual patterns
        #   - Bias drift

        # TODO: Generate alerts if issues detected

        # TODO: Return monitoring results
        pass

    def verify_governance_integrity(self) -> Dict[str, Any]:
        """
        Verify integrity of governance system.

        Returns:
            Integrity check results
        """
        results = {
            'timestamp': datetime.now(),
            'checks': {}
        }

        # TODO: 1. Verify audit log integrity
        # is_valid, issues = self.audit_logger.verify_log_integrity()
        # results['checks']['audit_log_integrity'] = {
        #     'passed': is_valid,
        #     'issues': issues
        # }

        # TODO: 2. Verify model card exists and is valid
        # if self.model_card:
        #     validation_issues = self.model_card_generator.validate_model_card(
        #         self.model_card
        #     )
        #     results['checks']['model_card_validity'] = {
        #         'passed': len(validation_issues) == 0,
        #         'issues': validation_issues
        #     }

        # TODO: 3. Check governance status is current
        # results['checks']['governance_status'] = {
        #     'status': self.governance_status,
        #     'last_assessment': 'timestamp of last assessment'
        # }

        # TODO: Return results
        return results
```

### Deployment Example

```python
# scripts/deploy_with_governance.py
"""Deploy model with governance framework."""

import joblib
from src.governance.governance_framework import GovernanceFramework


def deploy_model_with_governance():
    """Deploy model with full governance."""

    # TODO: Load trained model
    model = joblib.load("models/loan_approval_model.pkl")

    # TODO: Load test data
    X_test = pd.read_csv("data/X_test.csv")
    y_test = pd.read_csv("data/y_test.csv").values.ravel()
    sensitive_features = pd.read_csv("data/sensitive_features_test.csv")

    # TODO: Initialize governance framework
    governance = GovernanceFramework(
        model_name="loan_approval_model",
        model_version="1.2.0",
        sensitive_features=['gender', 'race', 'age']
    )

    # TODO: Assess governance before deployment
    assessment = governance.assess_model_governance(
        model, X_test, y_test, sensitive_features
    )

    print(f"\nGovernance Status: {assessment['governance_status']}")

    # TODO: Only deploy if approved
    if assessment['governance_status'] in ['APPROVED', 'APPROVED_WITH_CONDITIONS']:
        print("Model approved for deployment!")

        # TODO: Save model with governance metadata
        deployment_package = {
            'model': model,
            'governance': governance,
            'assessment': assessment
        }
        joblib.dump(deployment_package, "deployed_models/loan_model_v1.2.0.pkl")

        print("Model deployed with governance framework.")
    else:
        print("Model REJECTED for deployment due to governance violations.")
        print("Violations:", assessment['checks']['fairness']['violations'])


if __name__ == "__main__":
    deploy_model_with_governance()
```

### Success Criteria

- [ ] Complete governance framework integrates all components
- [ ] Pre-deployment assessment works correctly
- [ ] Predictions logged with full governance
- [ ] Governance reports generated
- [ ] Ongoing compliance monitoring functions
- [ ] Integrity verification works
- [ ] Framework ready for production use

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Integration**: Use composition to combine governance components
2. **Assessment Pipeline**: Run checks in sequence, collect results
3. **Approval Logic**: Define clear criteria for approval/rejection
4. **Monitoring**: Track metrics over time windows
5. **Reporting**: Combine data from all components into unified report
6. **Production Ready**: Handle errors gracefully, log all operations

</details>

---

## Bonus Challenges

### Challenge 1: GDPR Compliance Module

Implement GDPR-compliant features:
- Right to explanation
- Right to be forgotten
- Data minimization
- Consent tracking

### Challenge 2: Model Risk Management

Implement model risk tier classification:
- Risk assessment based on use case
- Different governance requirements by tier
- Approval workflows

### Challenge 3: Fairness Drift Detection

Implement fairness monitoring over time:
- Detect fairness degradation
- Trigger retraining when fairness drifts
- Adaptive fairness thresholds

---

## Additional Resources

- **Fairlearn**: [Documentation](https://fairlearn.org/)
- **Model Cards**: [Google Research Paper](https://arxiv.org/abs/1810.03993)
- **EU AI Act**: [Regulatory Framework](https://artificialintelligenceact.eu/)
- **NIST AI Risk Management**: [Framework](https://www.nist.gov/itl/ai-risk-management-framework)

---

## Submission Guidelines

For each exercise, submit:
1. **Code**: All implementation files
2. **Model Cards**: Generated documentation
3. **Audit Logs**: Example audit trails
4. **Reports**: Governance and fairness reports
5. **Documentation**: Governance framework guide

**Estimated Total Time**: 6-9 hours
**Difficulty**: Intermediate to Advanced

Good luck!
