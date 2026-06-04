from src.cost import count_tokens, estimate_cost


def test_count_tokens_nonzero():
    assert count_tokens("hello world") > 0


def test_estimate_cost():
    cost = estimate_cost(prompt_tokens=1000, completion_tokens=500,
                          cost_per_1k_input=0.001, cost_per_1k_output=0.002)
    assert cost == 0.001 * 1 + 0.002 * 0.5
