"""Fairness metrics for binary classifiers."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class FairnessReport:
    demographic_parity_diff: float
    equal_opportunity_diff: float
    disparate_impact: float
    accuracy_by_group: dict[str, float]
    selection_rate_by_group: dict[str, float]
    passes_four_fifths_rule: bool


def demographic_parity_diff(y_pred: np.ndarray, sensitive: np.ndarray) -> float:
    """max(rate) - min(rate) across groups. 0 = perfect parity."""
    rates = pd.Series(y_pred).groupby(pd.Series(sensitive)).mean()
    return float(rates.max() - rates.min())


def equal_opportunity_diff(y_true: np.ndarray, y_pred: np.ndarray,
                            sensitive: np.ndarray) -> float:
    """Difference in TPR across groups. 0 = equal opportunity."""
    df = pd.DataFrame({"y_true": y_true, "y_pred": y_pred, "g": sensitive})
    tpr = df[df.y_true == 1].groupby("g").apply(lambda x: (x.y_pred == 1).mean())
    return float(tpr.max() - tpr.min()) if len(tpr) > 1 else 0.0


def disparate_impact(y_pred: np.ndarray, sensitive: np.ndarray) -> float:
    """min(rate) / max(rate). >= 0.8 satisfies the four-fifths rule."""
    rates = pd.Series(y_pred).groupby(pd.Series(sensitive)).mean()
    return float(rates.min() / rates.max()) if rates.max() > 0 else 0.0


def assess(y_true: np.ndarray, y_pred: np.ndarray,
            sensitive: np.ndarray) -> FairnessReport:
    """Compute all fairness metrics for the given predictions + protected attribute."""
    di = disparate_impact(y_pred, sensitive)
    df = pd.DataFrame({"y_true": y_true, "y_pred": y_pred, "g": sensitive})
    acc_by_g = df.groupby("g").apply(lambda x: (x.y_pred == x.y_true).mean()).to_dict()
    rate_by_g = df.groupby("g")["y_pred"].mean().to_dict()
    return FairnessReport(
        demographic_parity_diff=demographic_parity_diff(y_pred, sensitive),
        equal_opportunity_diff=equal_opportunity_diff(y_true, y_pred, sensitive),
        disparate_impact=di,
        accuracy_by_group={str(k): float(v) for k, v in acc_by_g.items()},
        selection_rate_by_group={str(k): float(v) for k, v in rate_by_g.items()},
        passes_four_fifths_rule=di >= 0.8,
    )
