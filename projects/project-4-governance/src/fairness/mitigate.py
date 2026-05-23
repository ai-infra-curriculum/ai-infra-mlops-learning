"""Bias mitigation via threshold adjustment + fairlearn reductions."""
from __future__ import annotations

import numpy as np


def threshold_per_group(y_pred_proba: np.ndarray, sensitive: np.ndarray,
                        target_selection_rate: float = 0.3) -> np.ndarray:
    """Pick per-group thresholds so each group has the same selection rate."""
    out = np.zeros_like(y_pred_proba, dtype=int)
    for g in np.unique(sensitive):
        mask = sensitive == g
        # Choose threshold so target_selection_rate of this group is positive
        thresh = np.quantile(y_pred_proba[mask], 1 - target_selection_rate)
        out[mask] = (y_pred_proba[mask] >= thresh).astype(int)
    return out


def reweight(X, y, sensitive):
    """Sample weights so under-represented (group, label) combos count more."""
    import pandas as pd
    df = pd.DataFrame({"y": y, "g": sensitive})
    counts = df.groupby(["g", "y"]).size()
    weights = (1.0 / counts).reindex(list(zip(sensitive, y))).to_numpy()
    return weights / weights.mean()
