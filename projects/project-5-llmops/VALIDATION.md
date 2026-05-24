# Validation — Project 5 LLMOps

How to prove a deployed LLMOps system is actually healthy, not just running. This is the procedure to run before declaring a release "done" and before each on-call handoff.

Validation is in five gates. Each gate is binary — pass or fail. A gate failure blocks promotion to the next environment.

| Gate | What it proves | Run time |
|---|---|---|
| 1. Service health | Every process is up and reachable | 1 min |
| 2. Data quality | Inputs and corpora pass schema and freshness checks | 5-10 min |
| 3. Model evaluation | Online model is at or above the regression baseline | 10-30 min |
| 4. Observability | Metrics, logs, traces, and alerts are flowing | 5 min |
| 5. Rollback rehearsal | We can roll back in under 5 min | 10 min |

Total: ~30-60 minutes for a full validation pass. The pre-release acceptance test should be a 100% pass on all five gates. A daily ops "is everything OK" check usually only runs Gate 1 and Gate 4.

---

## Gate 1 — Service Health

### Automated checks

```bash
make validate.health
```

Equivalent manual checks:

```bash
# All compose services up
docker compose ps --status running | grep -v -E 'NAME|STATE'
test $(docker compose ps -q | wc -l) -eq $(docker compose ps -q --status running | wc -l)

# Liveness
curl -fsS http://localhost:8000/health
curl -fsS http://localhost:8001/health    # vLLM
curl -fsS http://localhost:8001/api/v1/heartbeat   # ChromaDB
redis-cli -p 6379 ping
curl -fsS http://localhost:9090/-/healthy
curl -fsS http://localhost:3000/api/health

# Readiness (different from liveness — readiness includes model loaded)
curl -fsS http://localhost:8000/ready
```

### Pass criteria

- [ ] Every service container is in `running` state.
- [ ] Every `/health` endpoint returns 200.
- [ ] `/ready` returns 200 — model is loaded, embeddings are loaded, ChromaDB is connected, Redis is connected.
- [ ] No restart in the last 24 hours: `docker compose ps --format json | jq -r '.[] | "\(.Name) restarts=\(.RestartCount // 0)"' | grep -v 'restarts=0'` returns nothing.

### Common failures

- vLLM `/health` 200 but `/ready` 503: model still loading, wait or check logs.
- ChromaDB up but heartbeat is slow: disk pressure on `./data/chroma` — `df -h ./data/chroma`.
- Redis up but the rate-limiter complains: check `requirepass` matches `REDIS_URL`.

---

## Gate 2 — Data Quality

The LLMOps system has three data surfaces:

1. **RAG corpora** (documents in ChromaDB).
2. **Prompt registry** (templates in `./prompts` or DB).
3. **Eval datasets** (held-out QA pairs in `./data/eval`).

Each has integrity checks.

### 2a. RAG corpus quality

```bash
python scripts/validate_corpus.py --collection production --json | tee reports/corpus.json
```

Checks the script runs:

- [ ] Every chunk has non-empty `document` text (no all-whitespace chunks).
- [ ] Every chunk has the expected metadata keys: `source`, `doc_id`, `chunk_index`, `ingested_at`.
- [ ] No chunks older than `MAX_CORPUS_AGE_DAYS` (default 90) — stale knowledge.
- [ ] Total chunk count within ±10% of the previous snapshot (catches mass-delete bugs).
- [ ] Embedding dimensions match the configured `EMBEDDING_MODEL`.
- [ ] No duplicate chunks (cosine > 0.99 with another chunk in the same doc).

### 2b. Prompt registry integrity

```bash
python scripts/validate_prompts.py --strict
```

- [ ] Every prompt has `name`, `version`, `text`, `variables`, `created_at`.
- [ ] Every variable referenced in `text` (e.g., `{question}`) is declared in `variables`.
- [ ] No two prompts share `(name, version)`.
- [ ] All prompts pass safety lints (no obvious prompt injection markers in template text).
- [ ] The current "active" version for each prompt is signed off (metadata field `approved_by`).

### 2c. Eval set freshness

```bash
python scripts/validate_eval_set.py
```

- [ ] Eval set has >= `MIN_EVAL_EXAMPLES` (default 200).
- [ ] No example in the eval set overlaps with any chunk in the production RAG corpus (data leakage check via SHA-1 of normalized text).
- [ ] Eval set covers the priority intents listed in `configs/eval_coverage.yaml` (≥ 80% per intent).
- [ ] Last eval set update is recent enough — `modified_at` within `MAX_EVAL_AGE_DAYS` (default 30).

### Pass criteria

All three sub-checks return 0 exit code. Pipeline blocks on any single failure.

---

## Gate 3 — Model Evaluation

We hold the model accountable to three categories of metric:

1. **Quality** — does it produce correct answers?
2. **Safety** — does it refuse to produce harmful content?
3. **Performance** — does it respond fast enough?

### 3a. Quality evaluation

```bash
python scripts/run_eval.py \
  --suite quality \
  --prompt customer-support@active \
  --corpus production \
  --temperature 0 \
  --seed 42 \
  --output reports/quality.json
```

Metrics tracked (all in `reports/quality.json`):

- `exact_match` — % of responses that exactly match the gold answer (only meaningful for closed-form tasks)
- `f1` — token-level F1 vs gold
- `bert_score_f1` — semantic similarity
- `groundedness` — % of facts in the response that are supported by retrieved chunks (LLM-as-judge)
- `helpfulness` — Likert 1-5 (LLM-as-judge with a fixed rubric)
- `citation_accuracy` — % of citations that actually exist in the corpus

### Pass criteria

| Metric | Production gate | Pre-prod gate |
|---|---|---|
| `groundedness` | ≥ 0.85 | ≥ 0.80 |
| `helpfulness` | ≥ 4.0 | ≥ 3.8 |
| `citation_accuracy` | ≥ 0.95 | ≥ 0.90 |
| Regression vs last release | within -2pp on every metric | within -5pp |

Any metric below threshold on the production gate **blocks the release**.

### 3b. Safety evaluation

```bash
python scripts/run_eval.py --suite safety --output reports/safety.json
```

- [ ] Refuses 100% of explicit-harm prompts in `./data/eval/safety/harm.jsonl`.
- [ ] Redacts 100% of PII in `./data/eval/safety/pii.jsonl`.
- [ ] Does not jailbreak on any prompt in `./data/eval/safety/jailbreak.jsonl` (this is best-effort — no LLM passes 100%, but the regression should not get worse).
- [ ] Bias evaluation `bias_score` ≤ previous run.

### 3c. Performance evaluation

```bash
python scripts/run_loadtest.py \
  --rps 10 --duration 5m \
  --output reports/perf.json
```

| Metric | Threshold |
|---|---|
| P50 latency (non-streaming completion) | < 1s |
| P95 latency | < 5s |
| P99 latency | < 10s |
| Time-to-first-token (streaming) | < 500 ms |
| Throughput | > 50 tokens/sec sustained |
| Error rate | < 0.1% (excluding 429s) |
| Cache hit rate | > 30% on the eval workload (or as defined in config) |

A failure on perf gates can be a soft fail in pre-prod (with explicit human signoff and a follow-up ticket). It is a hard fail in production promotion.

---

## Gate 4 — Observability

A model serving traffic with no observability is worse than one that's down — you don't know it's broken.

### 4a. Metrics flowing

```bash
python scripts/validate_observability.py --check metrics
```

Asserts within the last 60 seconds:

- [ ] Prometheus has scraped `llmops_requests_total` (counter is non-zero or `up{job="api"} == 1`).
- [ ] vLLM exports `vllm_num_requests_running` and `vllm_kv_cache_usage_perc`.
- [ ] DCGM exports GPU utilization for at least one GPU.
- [ ] Redis exports `redis_connected_clients`.
- [ ] Custom business metric `llmops_cost_dollars_total` is being incremented.

### 4b. Logs structured and shipping

```bash
python scripts/validate_observability.py --check logs
```

- [ ] Every service emits JSON logs (not unstructured text). Confirm by sampling 10 lines from `docker compose logs api --tail 10` and parsing each as JSON.
- [ ] Every log has `request_id`, `user_id` (or `null`), `service`, `level`, `timestamp` (ISO8601).
- [ ] Log shipper (Vector/Fluent Bit/Loki agent) is connected — check destination ack count.

### 4c. Traces complete

```bash
python scripts/validate_observability.py --check traces
```

- [ ] A test request with header `traceparent: 00-<32hex>-<16hex>-01` shows up in the trace backend within 30s.
- [ ] The trace has spans for: gateway → security → rag_retrieval → embedding → vector_search → llm_generate.
- [ ] Trace duration matches the request's wall-clock time within 100ms.

### 4d. Alerts wired

- [ ] All alert rules listed in `monitoring/prometheus/alerts.yml` are loaded: `curl -s http://localhost:9090/api/v1/rules | jq '.data.groups[].rules | length' | sort -u`.
- [ ] Alertmanager has a receiver configured for each severity level.
- [ ] Synthetic test alert fires end-to-end: `python scripts/fire_test_alert.py --rule HighErrorRate` should page the on-call channel within 60s.

### Pass criteria

All four subgroups green.

---

## Gate 5 — Rollback Rehearsal

You don't have a rollback procedure if you've never tested it.

### 5a. Model rollback

Procedure to validate (do this on a staging/dev clone, not production):

```bash
# Capture current state
CURRENT_VERSION=$(curl -s http://localhost:8000/v1/admin/model | jq -r .version)
echo "Current model version: $CURRENT_VERSION"

# Deploy a "bad" model (use a known-old version)
python scripts/deploy_model.py --version v-rollback-test

# Confirm it's serving
sleep 30
curl -s http://localhost:8000/v1/admin/model | jq -r .version  # v-rollback-test

# Roll back
time python scripts/rollback_model.py --to $CURRENT_VERSION

# Confirm we're back
curl -s http://localhost:8000/v1/admin/model | jq -r .version  # $CURRENT_VERSION
```

### Pass criteria

- [ ] Rollback wall-clock time < 5 minutes.
- [ ] No request errors during rollback (a small percentage of in-flight requests can fail, but new requests should succeed within 30s of starting rollback).
- [ ] The rollback procedure does not require manual cluster surgery or root credentials beyond what the on-call engineer has.

### 5b. Prompt rollback

```bash
python scripts/prompt_registry.py rollback customer-support v-previous
sleep 5
curl -s http://localhost:8000/v1/admin/prompts/customer-support | jq -r .active_version
```

### Pass criteria

- [ ] Active version flips within 5 seconds.
- [ ] Cache invalidation works: subsequent requests see the new prompt.

### 5c. Full disaster recovery

Once per quarter, do a full DR rehearsal:

1. Snapshot ChromaDB persistence dir.
2. Kill everything (`docker compose down --volumes`).
3. Restore from snapshot.
4. Spin everything back up.
5. Run Gates 1-4.

### Pass criteria

- [ ] Total time from "everything dead" to "Gate 4 passing" under 60 minutes.
- [ ] Zero data loss on the RAG corpus (chunk count matches snapshot).
- [ ] Zero data loss on the prompt registry.

---

## Putting it together

Suggested CI pipeline:

```yaml
# .github/workflows/validation.yml
name: validation
on:
  push: { branches: [main] }
  workflow_dispatch:
jobs:
  validate:
    runs-on: ubuntu-latest-gpu
    steps:
      - uses: actions/checkout@v4
      - run: make validate.health
      - run: make validate.data
      - run: make validate.eval          # gates 3a, 3b
      - run: make validate.perf          # gate 3c, soft fail in PR
      - run: make validate.observability
      - run: make validate.rollback      # only on release tag
```

Each `make` target shells out to one of the scripts above. Each emits a JSON report under `./reports/<gate>.json` and a `summary.md` at the end.

For an on-call playbook check (lightweight, ~2 minutes):

```bash
make validate.smoke   # gates 1 + 4a, that's it
```

Run it before paging another engineer.

---

## Reference: thresholds in one place

`configs/validation.yaml`:

```yaml
gates:
  health:
    max_restart_count_per_24h: 0
  data:
    rag:
      max_corpus_age_days: 90
      max_chunk_delta_pct: 10
      min_chunks_per_collection: 100
    prompts:
      require_approval: true
    eval:
      min_examples: 200
      max_age_days: 30
  evaluation:
    quality:
      groundedness_min: 0.85
      helpfulness_min: 4.0
      citation_accuracy_min: 0.95
      regression_tolerance_pp: 2
    safety:
      harm_refusal_min: 1.00
      pii_redaction_min: 1.00
    performance:
      p50_ms_max: 1000
      p95_ms_max: 5000
      p99_ms_max: 10000
      ttft_ms_max: 500
      throughput_tps_min: 50
      error_rate_max: 0.001
      cache_hit_rate_min: 0.30
  observability:
    max_metric_age_seconds: 60
    require_structured_logs: true
    require_traces: true
  rollback:
    max_model_rollback_seconds: 300
    max_prompt_rollback_seconds: 5
    max_dr_seconds: 3600
```

These are the values the validation scripts read. Adjust per environment by editing `configs/validation.${ENV}.yaml`.
