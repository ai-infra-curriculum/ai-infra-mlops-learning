"""Model card generation from training metadata."""
from __future__ import annotations

from dataclasses import dataclass

from jinja2 import Template


TEMPLATE_TEXT = """
# Model Card: {{ model_name }} v{{ version }}

## Owners
- Eng lead: {{ eng_lead }}
- DS lead: {{ ds_lead }}

## Intended use
{{ intended_use }}

## Out of scope
{{ out_of_scope }}

## Training data
- Source: {{ data_source }}
- Window: {{ data_window }}
- Row count: {{ data_rows }}
- Known biases: {{ known_biases }}

## Architecture
- Algorithm: {{ algorithm }}
- Hyperparameters: {{ hyperparameters }}
- Training compute: {{ compute }}

## Performance
- Primary metric: {{ primary_metric_name }} = {{ primary_metric_value }}
- Per-slice metrics:
{% for slice_name, value in slice_metrics.items() %}
  - {{ slice_name }}: {{ value }}
{% endfor %}

## Fairness
- Disparate impact (sensitive attribute = {{ sensitive_attribute }}): {{ disparate_impact }}
- Four-fifths rule: {{ "PASS" if passes_fairness else "FAIL" }}

## Approvals
- Eng: {{ eng_approval }}
- Compliance: {{ compliance_approval }}
- DS: {{ ds_approval }}

## Generated: {{ timestamp }}
""".strip()


@dataclass
class CardData:
    model_name: str
    version: str
    eng_lead: str
    ds_lead: str
    intended_use: str
    out_of_scope: str
    data_source: str
    data_window: str
    data_rows: int
    known_biases: str
    algorithm: str
    hyperparameters: str
    compute: str
    primary_metric_name: str
    primary_metric_value: float
    slice_metrics: dict
    sensitive_attribute: str
    disparate_impact: float
    passes_fairness: bool
    eng_approval: str
    compliance_approval: str
    ds_approval: str
    timestamp: str


def render(card: CardData) -> str:
    return Template(TEMPLATE_TEXT).render(**card.__dict__)
