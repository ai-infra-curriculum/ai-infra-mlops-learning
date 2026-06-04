import numpy as np

from src.fairness import assess, threshold_per_group


def test_disparate_impact_perfect_parity():
    y_true = np.array([1, 0, 1, 0, 1, 0, 1, 0])
    y_pred = np.array([1, 0, 1, 0, 1, 0, 1, 0])
    sensitive = np.array(["a", "b", "a", "b", "a", "b", "a", "b"])
    r = assess(y_true, y_pred, sensitive)
    assert r.disparate_impact == 1.0
    assert r.passes_four_fifths_rule


def test_disparate_impact_violation():
    y_true = np.array([1, 1, 1, 1, 1, 1, 1, 1])
    y_pred = np.array([1, 1, 1, 1, 0, 0, 0, 0])     # group b never selected
    sensitive = np.array(["a", "a", "a", "a", "b", "b", "b", "b"])
    r = assess(y_true, y_pred, sensitive)
    assert r.disparate_impact == 0.0
    assert not r.passes_four_fifths_rule


def test_threshold_per_group_balances_selection():
    proba = np.array([0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2])
    sensitive = np.array(["a"] * 4 + ["b"] * 4)
    preds = threshold_per_group(proba, sensitive, target_selection_rate=0.5)
    # Each group should have ~2 positives
    assert preds[sensitive == "a"].sum() == 2
    assert preds[sensitive == "b"].sum() == 2
