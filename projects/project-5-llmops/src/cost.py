"""Per-request cost computation + token counting."""
from __future__ import annotations

import tiktoken


_enc_cache: dict[str, object] = {}


def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    if model not in _enc_cache:
        try:
            _enc_cache[model] = tiktoken.encoding_for_model(model)
        except KeyError:
            _enc_cache[model] = tiktoken.get_encoding("cl100k_base")
    return len(_enc_cache[model].encode(text))


def estimate_cost(prompt_tokens: int, completion_tokens: int,
                   cost_per_1k_input: float, cost_per_1k_output: float) -> float:
    return (prompt_tokens / 1000 * cost_per_1k_input
            + completion_tokens / 1000 * cost_per_1k_output)
