"""Prometheus metrics for the LLMOps gateway."""
from prometheus_client import Counter, Histogram, Gauge


TTFT = Histogram(
    "llm_time_to_first_token_seconds",
    "Time from request received to first token streamed",
    ["model"],
    buckets=(0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0),
)

TOKENS_TOTAL = Counter(
    "llm_tokens_total",
    "Total tokens generated, split by direction",
    ["model", "direction"],
)

COST_USD_TOTAL = Counter(
    "llm_cost_usd_total",
    "Cumulative inferred USD spend",
    ["model"],
)

CACHE = Counter(
    "llm_cache_events_total",
    "Semantic cache events",
    ["outcome"],  # hit | miss
)

GUARD_BLOCKS = Counter(
    "llm_guard_blocks_total",
    "Requests blocked by guardrails",
    ["rule"],
)

REQUEST_LATENCY = Histogram(
    "llm_request_latency_seconds",
    "Total request handling latency",
    ["endpoint", "outcome"],
)

ACTIVE_REQUESTS = Gauge("llm_active_requests", "In-flight LLM requests")
