## Exercise 3: Model Card Generation & Documentation (75 minutes)

**Objective**: Create comprehensive model cards following industry standards for ML model documentation.

### Background

Model cards provide transparent documentation of ML models including:
- Model details and architecture
- Intended use and limitations
- Training data and evaluation metrics
- Fairness analysis
- Ethical considerations

### Tasks

1. **Implement model card generator**
2. **Document model details and performance**
3. **Include fairness and bias analysis**
4. **Add ethical considerations**
5. **Generate HTML/Markdown reports**

### Starter Code

```python
# src/governance/model_card.py
"""Model card generation for ML model documentation."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import markdown
from jinja2 import Template


@dataclass
class ModelDetails:
    """Basic model information."""
    name: str
    version: str
    model_type: str
    model_architecture: str
    training_date: datetime
    developer: str
    contact: str
    license: str = "Proprietary"
    repository: Optional[str] = None
    paper: Optional[str] = None


@dataclass
class IntendedUse:
    """Intended use and limitations."""
    primary_uses: List[str]
    primary_users: List[str]
    out_of_scope_uses: List[str]
    limitations: List[str]
    warnings: List[str] = field(default_factory=list)


@dataclass
class TrainingData:
    """Training data information."""
    dataset_name: str
    dataset_size: int
    dataset_description: str
    data_sources: List[str]
    preprocessing: List[str]
    train_test_split: Dict[str, float]
    data_collection_period: str
    known_biases: List[str] = field(default_factory=list)


@dataclass
class PerformanceMetrics:
    """Model performance metrics."""
    overall_metrics: Dict[str, float]
    performance_by_group: Optional[Dict[str, Dict[str, float]]] = None
    test_set_size: Optional[int] = None
    confidence_intervals: Optional[Dict[str, tuple]] = None


@dataclass
class FairnessAnalysis:
    """Fairness and bias analysis."""
    protected_attributes: List[str]
    fairness_metrics: Dict[str, float]
    disparate_impact_ratio: Dict[str, float]
    bias_mitigation_applied: List[str]
    residual_bias: str
    ongoing_monitoring: str


@dataclass
class EthicalConsiderations:
    """Ethical considerations and risks."""
    risks: List[str]
    mitigation_strategies: List[str]
    use_cases_to_avoid: List[str]
    stakeholder_impact: Dict[str, str]
    fairness_tradeoffs: str


@dataclass
class ModelCard:
    """Complete model card."""
    model_details: ModelDetails
    intended_use: IntendedUse
    training_data: TrainingData
    performance_metrics: PerformanceMetrics
    fairness_analysis: FairnessAnalysis
    ethical_considerations: EthicalConsiderations
    additional_info: Optional[Dict[str, Any]] = None


class ModelCardGenerator:
    """Generate model cards for ML models."""

    def __init__(self):
        """Initialize model card generator."""
        self.card = None

    def create_model_card(
        self,
        model_details: ModelDetails,
        intended_use: IntendedUse,
        training_data: TrainingData,
        performance_metrics: PerformanceMetrics,
        fairness_analysis: FairnessAnalysis,
        ethical_considerations: EthicalConsiderations
    ) -> ModelCard:
        """
        Create complete model card.

        Args:
            model_details: Model information
            intended_use: Use cases and limitations
            training_data: Training data details
            performance_metrics: Performance metrics
            fairness_analysis: Fairness analysis
            ethical_considerations: Ethical considerations

        Returns:
            Complete ModelCard object
        """
        # TODO: Create ModelCard object
        # self.card = ModelCard(...)
        # return self.card
        pass

    def generate_markdown(self, card: ModelCard) -> str:
        """
        Generate Markdown representation of model card.

        Args:
            card: ModelCard object

        Returns:
            Markdown string
        """
        # TODO: Generate Markdown following this structure:
        markdown_content = """
# Model Card: {model_name}

## Model Details
- **Name:** {model_name}
- **Version:** {version}
- **Type:** {model_type}
- **Architecture:** {architecture}
- **Developer:** {developer}
- **Training Date:** {training_date}
- **License:** {license}

## Intended Use

### Primary Uses
{primary_uses}

### Primary Users
{primary_users}

### Out-of-Scope Uses
{out_of_scope}

### Limitations
{limitations}

## Training Data

### Dataset
- **Name:** {dataset_name}
- **Size:** {dataset_size:,} samples
- **Description:** {dataset_description}

### Data Sources
{data_sources}

### Preprocessing
{preprocessing}

## Performance Metrics

### Overall Performance
{overall_metrics}

### Performance by Group
{performance_by_group}

## Fairness Analysis

### Protected Attributes
{protected_attributes}

### Fairness Metrics
{fairness_metrics}

### Disparate Impact Analysis
{disparate_impact}

### Bias Mitigation
{bias_mitigation}

## Ethical Considerations

### Risks
{risks}

### Mitigation Strategies
{mitigation_strategies}

### Use Cases to Avoid
{use_cases_to_avoid}

## Additional Information
{additional_info}

---

*Generated: {generation_date}*
"""

        # TODO: Fill in template with card data
        # TODO: Return formatted markdown
        pass

    def generate_html(self, card: ModelCard) -> str:
        """
        Generate HTML representation of model card.

        Args:
            card: ModelCard object

        Returns:
            HTML string
        """
        # TODO: Generate HTML with styling
        # Option 1: Convert markdown to HTML
        # Option 2: Use Jinja2 HTML template
        # TODO: Include CSS for nice formatting
        # TODO: Add interactive elements (collapsible sections)
        pass

    def generate_json(self, card: ModelCard) -> str:
        """
        Generate JSON representation of model card.

        Args:
            card: ModelCard object

        Returns:
            JSON string
        """
        # TODO: Convert ModelCard to dictionary
        # TODO: Serialize to JSON
        # TODO: Return JSON string
        pass

    def save_model_card(
        self,
        card: ModelCard,
        output_path: str,
        format: str = 'markdown'
    ):
        """
        Save model card to file.

        Args:
            card: ModelCard object
            output_path: Output file path
            format: Output format ('markdown', 'html', 'json')
        """
        # TODO: Generate content in requested format
        # TODO: Write to file
        pass

    def validate_model_card(self, card: ModelCard) -> List[str]:
        """
        Validate model card completeness.

        Args:
            card: ModelCard object

        Returns:
            List of validation warnings/errors
        """
        issues = []

        # TODO: Check required fields are present
        # - Model name, version, type
        # - At least one intended use
        # - At least one limitation
        # - Training data information
        # - Performance metrics
        # - Fairness analysis

        # TODO: Check for completeness
        # - Are all sections filled in?
        # - Are there placeholder values?
        # - Are fairness metrics included?

        # TODO: Return list of issues
        return issues
```

### Example Usage

```python
# scripts/create_model_card.py
"""Example script to create model card."""

from src.governance.model_card import (
    ModelCardGenerator,
    ModelDetails,
    IntendedUse,
    TrainingData,
    PerformanceMetrics,
    FairnessAnalysis,
    EthicalConsiderations
)
from datetime import datetime


def main():
    """Create example model card for loan approval model."""

    # TODO: Define model details
    model_details = ModelDetails(
        name="Loan Approval Model",
        version="1.2.0",
        model_type="Binary Classification",
        model_architecture="Gradient Boosted Trees (XGBoost)",
        training_date=datetime(2024, 10, 15),
        developer="ML Team - Financial Services Division",
        contact="ml-team@company.com",
        license="Proprietary",
        repository="https://github.com/company/loan-model"
    )

    # TODO: Define intended use
    intended_use = IntendedUse(
        primary_uses=[
            "Automated loan approval decisions for personal loans under $50,000",
            "Risk assessment for loan applications",
            "Prioritization of applications for manual review"
        ],
        primary_users=[
            "Loan officers",
            "Risk assessment teams",
            "Automated lending platform"
        ],
        out_of_scope_uses=[
            "Mortgage or business loan approvals",
            "Loans over $50,000",
            "Decisions without human oversight",
            "Use in jurisdictions with different lending regulations"
        ],
        limitations=[
            "Model performance degrades for applicants with thin credit files",
            "May not generalize to economic conditions outside training period",
            "Requires quarterly retraining to maintain performance",
            "Not suitable for first-time borrowers without credit history"
        ],
        warnings=[
            "Must be used in compliance with fair lending regulations",
            "Human review required for declined applications",
            "Monitor for fairness violations in production"
        ]
    )

    # TODO: Define training data
    training_data = TrainingData(
        dataset_name="Historical Loan Applications 2020-2024",
        dataset_size=150000,
        dataset_description="Historical loan applications with outcomes (approved/denied) and repayment data",
        data_sources=[
            "Internal loan application database",
            "Credit bureau data",
            "Income verification systems"
        ],
        preprocessing=[
            "Removal of personally identifiable information",
            "Feature engineering: debt-to-income ratio, credit utilization",
            "Handling missing values: median imputation for numerical, mode for categorical",
            "Outlier capping at 99th percentile for continuous features"
        ],
        train_test_split={
            "train": 0.7,
            "validation": 0.15,
            "test": 0.15
        },
        data_collection_period="January 2020 - June 2024",
        known_biases=[
            "Historical bias: Lower approval rates for minority groups due to systemic factors",
            "Geographic bias: Underrepresentation of rural applicants"
        ]
    )

    # TODO: Define performance metrics
    performance_metrics = PerformanceMetrics(
        overall_metrics={
            "accuracy": 0.87,
            "precision": 0.84,
            "recall": 0.82,
            "f1_score": 0.83,
            "auc_roc": 0.91
        },
        performance_by_group={
            "gender": {
                "male": {"accuracy": 0.88, "precision": 0.85},
                "female": {"accuracy": 0.86, "precision": 0.83}
            },
            "race": {
                "white": {"accuracy": 0.88, "precision": 0.86},
                "black": {"accuracy": 0.85, "precision": 0.81},
                "hispanic": {"accuracy": 0.86, "precision": 0.82}
            }
        },
        test_set_size=22500,
        confidence_intervals={
            "accuracy": (0.85, 0.89),
            "precision": (0.82, 0.86)
        }
    )

    # TODO: Define fairness analysis
    fairness_analysis = FairnessAnalysis(
        protected_attributes=["gender", "race", "age"],
        fairness_metrics={
            "demographic_parity_difference": 0.05,
            "equalized_odds_difference": 0.08,
            "equal_opportunity_difference": 0.06
        },
        disparate_impact_ratio={
            "gender": 0.92,
            "race": 0.85,
            "age": 0.88
        },
        bias_mitigation_applied=[
            "Reweighing of training samples",
            "Post-processing threshold optimization",
            "Regular fairness audits"
        ],
        residual_bias="Minor disparate impact detected for race (DI ratio: 0.85). Ongoing monitoring required.",
        ongoing_monitoring="Monthly fairness audits, quarterly model retraining with fairness constraints"
    )

    # TODO: Define ethical considerations
    ethical_considerations = EthicalConsiderations(
        risks=[
            "Potential for discriminatory outcomes if fairness monitoring lapses",
            "Over-reliance on model could reduce human judgment in edge cases",
            "Privacy risk if model features inadvertently expose sensitive information",
            "Economic harm to applicants if model errors lead to unfair denials"
        ],
        mitigation_strategies=[
            "Mandatory human review for all denials",
            "Regular fairness audits by independent team",
            "Adverse action explanations for all denied applications",
            "Appeals process with human adjudication",
            "Quarterly model retraining with updated fairness constraints"
        ],
        use_cases_to_avoid=[
            "Fully automated decisions without human oversight",
            "Use on protected classes without fairness validation",
            "Deployment without adverse action explanation capability"
        ],
        stakeholder_impact={
            "applicants": "Direct impact on loan access and financial opportunities",
            "loan_officers": "Tool to support but not replace decision-making",
            "company": "Regulatory compliance and reputation risk",
            "regulators": "Fair lending compliance oversight"
        },
        fairness_tradeoffs="Slight reduction in overall accuracy (2%) in exchange for improved fairness across demographic groups"
    )

    # TODO: Create model card
    generator = ModelCardGenerator()
    card = generator.create_model_card(
        model_details=model_details,
        intended_use=intended_use,
        training_data=training_data,
        performance_metrics=performance_metrics,
        fairness_analysis=fairness_analysis,
        ethical_considerations=ethical_considerations
    )

    # TODO: Validate model card
    issues = generator.validate_model_card(card)
    if issues:
        print("Model card validation issues:")
        for issue in issues:
            print(f"  - {issue}")

    # TODO: Generate and save in multiple formats
    generator.save_model_card(card, "model_card.md", format="markdown")
    generator.save_model_card(card, "model_card.html", format="html")
    generator.save_model_card(card, "model_card.json", format="json")

    print("Model card generated successfully!")


if __name__ == "__main__":
    main()
```

### Success Criteria

- [ ] Model card includes all required sections
- [ ] Markdown generation produces well-formatted output
- [ ] HTML generation includes styling
- [ ] JSON export is valid and complete
- [ ] Validation detects missing fields
- [ ] Card follows industry best practices
- [ ] Generated cards are human-readable

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Markdown Generation**: Use f-strings or templates
2. **HTML Generation**: Convert markdown or use Jinja2 templates
3. **JSON Serialization**: Use `dataclasses.asdict()` and `json.dumps()`
4. **Validation**: Check for None values and empty lists
5. **Follow Standards**: Reference Google's Model Cards paper and examples

</details>

---
