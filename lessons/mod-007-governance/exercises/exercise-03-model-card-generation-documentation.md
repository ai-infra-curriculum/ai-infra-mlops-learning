## Exercise 3: Model Card Generation & Documentation (75 minutes)

**Objective**: Build a model card generator that produces complete, standards-aligned ML model documentation in Markdown, HTML, and JSON, with completeness validation.

### Background

A model card is the canonical artifact for transparent model documentation — required by most ML
governance frameworks and a near-universal expectation in regulated industries. Following the
"Model Cards for Model Reporting" pattern (Mitchell et al., 2019) and the Hugging Face card schema,
a good card answers:

- **What is this model?** Architecture, version, owner, license.
- **What is it for — and not for?** Intended uses, out-of-scope uses, limitations.
- **What was it trained on?** Dataset provenance, preprocessing, known biases.
- **How well does it work?** Overall metrics *and* metrics sliced by group.
- **Is it fair?** Protected attributes, fairness metrics, disparate impact, mitigation.
- **What could go wrong?** Risks, mitigations, stakeholder impact, fairness trade-offs.

The card is only useful if it is generated from the same metadata your evaluation pipeline already
produces — a hand-written card drifts immediately. In this exercise you build the generator so the
card is a deterministic render of structured inputs, and you add validation so an incomplete card
fails CI rather than shipping with `TODO` sections.

### Tasks

1. **Model the card** with typed dataclasses (provided).
2. **Implement `create_model_card`** to assemble the typed sections into a `ModelCard`.
3. **Implement `generate_markdown`** to render a complete, readable Markdown card.
4. **Implement `generate_html`** by converting the Markdown and wrapping it in styled HTML.
5. **Implement `generate_json`** with `dataclasses.asdict` so the card is machine-readable.
6. **Implement `validate_model_card`** to flag missing or placeholder sections.
7. **Implement `save_model_card`** to write any format to disk.

### Starter Code

The dataclasses define the card schema. Every generator method below is fully implemented — use
them as the reference and adapt the rendered sections to your organization's template.

```python
# src/governance/model_card.py
"""Model card generation for ML model documentation."""

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import markdown


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
    performance_by_group: Optional[Dict[str, Dict[str, Dict[str, float]]]] = None
    test_set_size: Optional[int] = None
    confidence_intervals: Optional[Dict[str, Tuple[float, float]]] = None


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


def _bullets(items: List[str]) -> str:
    """Render a list as Markdown bullets, or an explicit '_None specified_' if empty."""
    if not items:
        return "_None specified_"
    return "\n".join(f"- {item}" for item in items)


def _metric_table(metrics: Dict[str, float]) -> str:
    """Render a flat metric dict as a Markdown table."""
    if not metrics:
        return "_No metrics reported_"
    rows = ["| Metric | Value |", "| --- | --- |"]
    rows += [f"| {name} | {value:.4f} |" for name, value in metrics.items()]
    return "\n".join(rows)


class ModelCardGenerator:
    """Generate model cards for ML models."""

    REQUIRED_SECTIONS = (
        "model_details",
        "intended_use",
        "training_data",
        "performance_metrics",
        "fairness_analysis",
        "ethical_considerations",
    )

    def create_model_card(
        self,
        model_details: ModelDetails,
        intended_use: IntendedUse,
        training_data: TrainingData,
        performance_metrics: PerformanceMetrics,
        fairness_analysis: FairnessAnalysis,
        ethical_considerations: EthicalConsiderations,
        additional_info: Optional[Dict[str, Any]] = None,
    ) -> ModelCard:
        """Assemble the typed sections into a complete ModelCard."""
        return ModelCard(
            model_details=model_details,
            intended_use=intended_use,
            training_data=training_data,
            performance_metrics=performance_metrics,
            fairness_analysis=fairness_analysis,
            ethical_considerations=ethical_considerations,
            additional_info=additional_info,
        )

    def generate_markdown(self, card: ModelCard) -> str:
        """Render the card as Markdown."""
        d = card.model_details
        use = card.intended_use
        data = card.training_data
        perf = card.performance_metrics
        fair = card.fairness_analysis
        ethics = card.ethical_considerations

        sections = [
            f"# Model Card: {d.name}",
            "",
            "## Model Details",
            "",
            f"- **Name:** {d.name}",
            f"- **Version:** {d.version}",
            f"- **Type:** {d.model_type}",
            f"- **Architecture:** {d.model_architecture}",
            f"- **Developer:** {d.developer}",
            f"- **Contact:** {d.contact}",
            f"- **Training Date:** {d.training_date.strftime('%Y-%m-%d')}",
            f"- **License:** {d.license}",
        ]
        if d.repository:
            sections.append(f"- **Repository:** {d.repository}")
        if d.paper:
            sections.append(f"- **Paper:** {d.paper}")

        sections += [
            "",
            "## Intended Use",
            "",
            "### Primary Uses",
            "",
            _bullets(use.primary_uses),
            "",
            "### Primary Users",
            "",
            _bullets(use.primary_users),
            "",
            "### Out-of-Scope Uses",
            "",
            _bullets(use.out_of_scope_uses),
            "",
            "### Limitations",
            "",
            _bullets(use.limitations),
            "",
            "### Warnings",
            "",
            _bullets(use.warnings),
            "",
            "## Training Data",
            "",
            f"- **Dataset:** {data.dataset_name}",
            f"- **Size:** {data.dataset_size:,} samples",
            f"- **Description:** {data.dataset_description}",
            f"- **Collection Period:** {data.data_collection_period}",
            "",
            "### Data Sources",
            "",
            _bullets(data.data_sources),
            "",
            "### Preprocessing",
            "",
            _bullets(data.preprocessing),
            "",
            "### Train/Test Split",
            "",
            _bullets([f"{name}: {ratio:.0%}" for name, ratio in data.train_test_split.items()]),
            "",
            "### Known Biases",
            "",
            _bullets(data.known_biases),
            "",
            "## Performance Metrics",
            "",
            "### Overall Performance",
            "",
            _metric_table(perf.overall_metrics),
            "",
        ]

        if perf.test_set_size:
            sections += [f"**Test set size:** {perf.test_set_size:,} samples", ""]

        if perf.confidence_intervals:
            ci_rows = ["| Metric | 95% CI |", "| --- | --- |"]
            ci_rows += [
                f"| {name} | ({low:.4f}, {high:.4f}) |"
                for name, (low, high) in perf.confidence_intervals.items()
            ]
            sections += ["### Confidence Intervals", "", "\n".join(ci_rows), ""]

        if perf.performance_by_group:
            sections += ["### Performance by Group", ""]
            for attribute, groups in perf.performance_by_group.items():
                sections.append(f"**{attribute}**")
                sections.append("")
                for group_name, group_metrics in groups.items():
                    rendered = ", ".join(f"{k}: {v:.4f}" for k, v in group_metrics.items())
                    sections.append(f"- {group_name}: {rendered}")
                sections.append("")

        sections += [
            "## Fairness Analysis",
            "",
            "### Protected Attributes",
            "",
            _bullets(fair.protected_attributes),
            "",
            "### Fairness Metrics",
            "",
            _metric_table(fair.fairness_metrics),
            "",
            "### Disparate Impact Ratio",
            "",
            _metric_table(fair.disparate_impact_ratio),
            "",
            "### Bias Mitigation Applied",
            "",
            _bullets(fair.bias_mitigation_applied),
            "",
            f"**Residual bias:** {fair.residual_bias}",
            "",
            f"**Ongoing monitoring:** {fair.ongoing_monitoring}",
            "",
            "## Ethical Considerations",
            "",
            "### Risks",
            "",
            _bullets(ethics.risks),
            "",
            "### Mitigation Strategies",
            "",
            _bullets(ethics.mitigation_strategies),
            "",
            "### Use Cases to Avoid",
            "",
            _bullets(ethics.use_cases_to_avoid),
            "",
            "### Stakeholder Impact",
            "",
            _bullets([f"**{who}:** {impact}" for who, impact in ethics.stakeholder_impact.items()]),
            "",
            f"**Fairness trade-offs:** {ethics.fairness_tradeoffs}",
            "",
        ]

        if card.additional_info:
            sections += ["## Additional Information", ""]
            sections += [f"- **{k}:** {v}" for k, v in card.additional_info.items()]
            sections.append("")

        sections += ["---", "", f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"]
        return "\n".join(sections)

    def generate_html(self, card: ModelCard) -> str:
        """Render the card as styled, standalone HTML."""
        body = markdown.markdown(
            self.generate_markdown(card), extensions=["tables", "fenced_code"]
        )
        css = """
        body { font-family: -apple-system, Segoe UI, Roboto, sans-serif;
               max-width: 880px; margin: 2rem auto; padding: 0 1rem; line-height: 1.6; }
        h1 { border-bottom: 3px solid #2563eb; padding-bottom: .3rem; }
        h2 { margin-top: 2rem; color: #1e3a8a; }
        table { border-collapse: collapse; width: 100%; margin: .5rem 0; }
        th, td { border: 1px solid #cbd5e1; padding: .4rem .6rem; text-align: left; }
        th { background: #eff6ff; }
        code { background: #f1f5f9; padding: .1rem .3rem; border-radius: 3px; }
        """
        return (
            "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
            f"<meta charset=\"utf-8\">\n<title>Model Card: {card.model_details.name}</title>\n"
            f"<style>{css}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n"
        )

    def generate_json(self, card: ModelCard) -> str:
        """Serialize the card to JSON (datetimes rendered as ISO strings)."""
        return json.dumps(asdict(card), indent=2, default=str)

    def save_model_card(self, card: ModelCard, output_path: str, fmt: str = "markdown") -> None:
        """Generate the card in ``fmt`` and write it to ``output_path``."""
        renderers = {
            "markdown": self.generate_markdown,
            "html": self.generate_html,
            "json": self.generate_json,
        }
        if fmt not in renderers:
            raise ValueError(f"Unsupported format: {fmt}. Choose one of {list(renderers)}.")
        with open(output_path, "w", encoding="utf-8") as handle:
            handle.write(renderers[fmt](card))

    def validate_model_card(self, card: ModelCard) -> List[str]:
        """
        Validate completeness. Returns a list of human-readable issues
        (empty list means the card passes).
        """
        issues: List[str] = []

        if not card.model_details.name:
            issues.append("model_details.name is empty")
        if not card.model_details.version:
            issues.append("model_details.version is empty")

        if not card.intended_use.primary_uses:
            issues.append("intended_use.primary_uses must list at least one use")
        if not card.intended_use.limitations:
            issues.append("intended_use.limitations must list at least one limitation")
        if not card.intended_use.out_of_scope_uses:
            issues.append("intended_use.out_of_scope_uses must list at least one entry")

        if card.training_data.dataset_size <= 0:
            issues.append("training_data.dataset_size must be positive")
        if not card.training_data.data_sources:
            issues.append("training_data.data_sources must list at least one source")

        if not card.performance_metrics.overall_metrics:
            issues.append("performance_metrics.overall_metrics is empty")

        if not card.fairness_analysis.protected_attributes:
            issues.append("fairness_analysis.protected_attributes is empty")
        if not card.fairness_analysis.fairness_metrics:
            issues.append("fairness_analysis.fairness_metrics is empty")

        if not card.ethical_considerations.risks:
            issues.append("ethical_considerations.risks must list at least one risk")

        # Catch lingering placeholder text in free-form fields.
        placeholder_tokens = ("todo", "tbd", "fixme", "xxx", "<placeholder>")
        for label, text in (
            ("fairness_analysis.residual_bias", card.fairness_analysis.residual_bias),
            ("ethical_considerations.fairness_tradeoffs", card.ethical_considerations.fairness_tradeoffs),
        ):
            if text and any(token in text.lower() for token in placeholder_tokens):
                issues.append(f"{label} contains placeholder text: {text!r}")

        return issues
```

### Example Usage

This script builds a card for a loan-approval model, validates it, and writes all three formats.

```python
# scripts/create_model_card.py
"""Build, validate, and export a model card."""

from datetime import datetime

from src.governance.model_card import (
    EthicalConsiderations,
    FairnessAnalysis,
    IntendedUse,
    ModelCardGenerator,
    ModelDetails,
    PerformanceMetrics,
    TrainingData,
)


def build_card():
    generator = ModelCardGenerator()
    return generator, generator.create_model_card(
        model_details=ModelDetails(
            name="Loan Approval Model",
            version="1.2.0",
            model_type="Binary Classification",
            model_architecture="Gradient Boosted Trees (XGBoost)",
            training_date=datetime(2024, 10, 15),
            developer="ML Team - Financial Services Division",
            contact="ml-team@company.com",
            license="Proprietary",
            repository="https://github.com/company/loan-model",
        ),
        intended_use=IntendedUse(
            primary_uses=[
                "Automated approval decisions for personal loans under $50,000",
                "Risk assessment for loan applications",
                "Prioritization of applications for manual review",
            ],
            primary_users=["Loan officers", "Risk assessment teams", "Lending platform"],
            out_of_scope_uses=[
                "Mortgage or business loan approvals",
                "Loans over $50,000",
                "Decisions without human oversight",
            ],
            limitations=[
                "Performance degrades for applicants with thin credit files",
                "May not generalize beyond the training economic period",
                "Requires quarterly retraining to maintain performance",
            ],
            warnings=[
                "Must be used in compliance with fair lending regulations",
                "Human review required for declined applications",
            ],
        ),
        training_data=TrainingData(
            dataset_name="Historical Loan Applications 2020-2024",
            dataset_size=150_000,
            dataset_description="Historical applications with approval and repayment outcomes",
            data_sources=["Internal loan database", "Credit bureau data", "Income verification"],
            preprocessing=[
                "PII removal",
                "Feature engineering: debt-to-income ratio, credit utilization",
                "Median/mode imputation for missing values",
                "Outlier capping at the 99th percentile",
            ],
            train_test_split={"train": 0.7, "validation": 0.15, "test": 0.15},
            data_collection_period="January 2020 - June 2024",
            known_biases=[
                "Historical bias: lower approval rates for minority groups",
                "Geographic bias: underrepresentation of rural applicants",
            ],
        ),
        performance_metrics=PerformanceMetrics(
            overall_metrics={
                "accuracy": 0.87, "precision": 0.84, "recall": 0.82,
                "f1_score": 0.83, "auc_roc": 0.91,
            },
            performance_by_group={
                "gender": {
                    "male": {"accuracy": 0.88, "precision": 0.85},
                    "female": {"accuracy": 0.86, "precision": 0.83},
                },
            },
            test_set_size=22_500,
            confidence_intervals={"accuracy": (0.85, 0.89), "precision": (0.82, 0.86)},
        ),
        fairness_analysis=FairnessAnalysis(
            protected_attributes=["gender", "race", "age"],
            fairness_metrics={
                "demographic_parity_difference": 0.05,
                "equalized_odds_difference": 0.08,
                "equal_opportunity_difference": 0.06,
            },
            disparate_impact_ratio={"gender": 0.92, "race": 0.85, "age": 0.88},
            bias_mitigation_applied=[
                "Reweighing of training samples",
                "Post-processing threshold optimization",
            ],
            residual_bias="Minor disparate impact for race (DI ratio 0.85); ongoing monitoring.",
            ongoing_monitoring="Monthly fairness audits, quarterly retraining with constraints.",
        ),
        ethical_considerations=EthicalConsiderations(
            risks=[
                "Discriminatory outcomes if fairness monitoring lapses",
                "Over-reliance reduces human judgment in edge cases",
            ],
            mitigation_strategies=[
                "Mandatory human review for all denials",
                "Adverse-action explanations for declined applications",
            ],
            use_cases_to_avoid=["Fully automated decisions without human oversight"],
            stakeholder_impact={
                "applicants": "Direct impact on loan access and financial opportunity",
                "company": "Regulatory compliance and reputation risk",
            },
            fairness_tradeoffs="~2% accuracy reduction in exchange for improved group fairness.",
        ),
    )


def main():
    generator, card = build_card()

    issues = generator.validate_model_card(card)
    if issues:
        print("Validation issues:")
        for issue in issues:
            print(f"  - {issue}")
        raise SystemExit(1)

    generator.save_model_card(card, "model_card.md", fmt="markdown")
    generator.save_model_card(card, "model_card.html", fmt="html")
    generator.save_model_card(card, "model_card.json", fmt="json")
    print("Model card generated in markdown, html, and json.")


if __name__ == "__main__":
    main()
```

### Validation Tests

```python
# tests/test_model_card.py
"""Tests for the model card generator."""

import json
from datetime import datetime

import pytest

from src.governance.model_card import (
    EthicalConsiderations,
    FairnessAnalysis,
    IntendedUse,
    ModelCardGenerator,
    ModelDetails,
    PerformanceMetrics,
    TrainingData,
)


@pytest.fixture
def card():
    gen = ModelCardGenerator()
    return gen.create_model_card(
        model_details=ModelDetails(
            name="Test Model", version="1.0.0", model_type="Classification",
            model_architecture="XGBoost", training_date=datetime(2024, 1, 1),
            developer="ML Team", contact="ml@test.com",
        ),
        intended_use=IntendedUse(
            primary_uses=["Risk scoring"], primary_users=["Analysts"],
            out_of_scope_uses=["Medical diagnosis"], limitations=["Thin-file degradation"],
        ),
        training_data=TrainingData(
            dataset_name="Test", dataset_size=1000, dataset_description="Synthetic",
            data_sources=["Internal"], preprocessing=["Scaling"],
            train_test_split={"train": 0.8, "test": 0.2}, data_collection_period="2024",
        ),
        performance_metrics=PerformanceMetrics(overall_metrics={"accuracy": 0.9}),
        fairness_analysis=FairnessAnalysis(
            protected_attributes=["gender"], fairness_metrics={"dpd": 0.03},
            disparate_impact_ratio={"gender": 0.95}, bias_mitigation_applied=["Reweighing"],
            residual_bias="Negligible.", ongoing_monitoring="Monthly audits.",
        ),
        ethical_considerations=EthicalConsiderations(
            risks=["Disparate impact"], mitigation_strategies=["Human review"],
            use_cases_to_avoid=["Autonomous denials"], stakeholder_impact={"users": "High"},
            fairness_tradeoffs="Minor accuracy cost.",
        ),
    )


def test_valid_card_has_no_issues(card):
    assert ModelCardGenerator().validate_model_card(card) == []


def test_markdown_contains_required_headings(card):
    md = ModelCardGenerator().generate_markdown(card)
    for heading in ("# Model Card:", "## Intended Use", "## Fairness Analysis"):
        assert heading in md


def test_json_is_valid_and_roundtrips(card):
    payload = json.loads(ModelCardGenerator().generate_json(card))
    assert payload["model_details"]["name"] == "Test Model"


def test_validation_flags_missing_limitations(card):
    card.intended_use.limitations = []
    issues = ModelCardGenerator().validate_model_card(card)
    assert any("limitations" in issue for issue in issues)


def test_validation_flags_placeholder_text(card):
    card.fairness_analysis.residual_bias = "TODO: fill in"
    issues = ModelCardGenerator().validate_model_card(card)
    assert any("placeholder" in issue for issue in issues)

# Run with: pytest tests/test_model_card.py -v
```

### Success Criteria

- [ ] `create_model_card` assembles all six required sections
- [ ] Markdown output includes every section with correct headings
- [ ] HTML output is valid, standalone, and styled
- [ ] JSON output is valid and round-trips through `json.loads`
- [ ] `validate_model_card` flags missing required fields *and* placeholder text
- [ ] `save_model_card` writes all three formats to disk
- [ ] All tests pass

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Render from structure**: keep the card a pure function of its dataclasses so it never drifts.
2. **Markdown tables** need a header separator row (`| --- | --- |`) and the `tables` extension when
   converting to HTML via `python-markdown`.
3. **JSON serialization**: `dataclasses.asdict()` handles nesting; pass `default=str` to `json.dumps`
   so `datetime` fields serialize cleanly.
4. **Validation as a gate**: run `validate_model_card` in CI and fail the build on any issue — this is
   what stops half-finished cards from shipping.
5. **Placeholder detection**: scan free-form fields for `todo`/`tbd`/`fixme` so a card with empty
   prose is rejected even when the field is technically non-empty.
6. **Standards**: align section names with the Hugging Face card schema so cards publish cleanly to a
   model registry or hub.

</details>

---
