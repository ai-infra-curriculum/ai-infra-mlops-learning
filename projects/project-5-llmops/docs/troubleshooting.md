# LLMOps Troubleshooting

Project-5-specific failures and their fixes. For dev-environment basics (Docker permissions, Python issues, etc.) see the orientation exercise's [troubleshooting guide](../../../../ai-infra-junior-engineer-solutions/modules/mod-000-orientation/exercise-02-dev-environment/docs/troubleshooting.md).

Each entry: **symptom → why it happens → the actual fix**.

## Index

1. [vLLM server crashes immediately on launch with `RuntimeError: Found no NVIDIA driver`](#1-vllm-no-nvidia-driver)
2. [CUDA out of memory on vLLM startup](#2-cuda-out-of-memory-on-vllm-startup)
3. [Mid-generation OOM: throughput collapses after N concurrent requests](#3-mid-generation-oom)
4. [vLLM loads the model but `/health` never goes green](#4-vllm-health-stays-red)
5. [First request takes tens of seconds](#5-first-request-takes-tens-of-seconds)
6. [Token-per-second far below benchmark numbers](#6-low-tokens-per-second)
7. [Model registry conflicts on deploy](#7-model-registry-conflicts)
8. [Retraining / fine-tune loop stuck in failed → retry cycle](#8-retraining-loop-instability)
9. [ChromaDB collection corruption](#9-chromadb-collection-corruption)
10. [Vector index dimension mismatch](#10-vector-index-dimension-mismatch)
11. [RAG returns irrelevant chunks](#11-rag-returns-irrelevant-chunks)
12. [RAG returns duplicates / near-duplicates](#12-rag-returns-duplicates)
13. [Embeddings inference is the bottleneck, not the LLM](#13-embeddings-bottleneck)
14. [Prompt evaluation drift after deploy](#14-prompt-evaluation-drift-after-deploy)
15. [A/B test results flip between runs](#15-ab-test-results-flip)
16. [Rate limiter returns 429 in normal traffic](#16-rate-limiter-returns-429-in-normal-traffic)
17. [PII redactor over-redacts or misses obvious PII](#17-pii-redactor-over-or-under)
18. [Cost numbers don't reconcile with cloud bill](#18-cost-numbers-don-t-reconcile)
19. [Prometheus metrics gap during high load](#19-prometheus-metrics-gap)
20. [Streaming responses cut off / disconnect](#20-streaming-cuts-off)

---

## 1. vLLM no NVIDIA driver

**Symptom**: `docker compose logs vllm` shows `RuntimeError: Found no NVIDIA driver on your system. Please check that you have an NVIDIA GPU and installed a driver.`

**Cause**: The vLLM container can't see the host GPU. Either the NVIDIA Container Toolkit isn't installed, the compose service is missing `deploy.resources.reservations.devices`, or you booted the container before the driver was loaded after a host reboot.

**Fix**:

1. On the host: `nvidia-smi` must work.
2. `docker run --rm --gpus all nvidia/cuda:12.4.0-base-ubuntu22.04 nvidia-smi` must work.
3. In `docker-compose.yaml` the vllm service needs:
   ```yaml
   deploy:
     resources:
       reservations:
         devices:
           - driver: nvidia
             count: all
             capabilities: [gpu]
   ```
4. `docker compose down && docker compose up -d vllm`.

If 2 fails, install nvidia-container-toolkit and restart Docker — see [setup-linux.md Section 3](../../../../ai-infra-junior-engineer-solutions/modules/mod-000-orientation/exercise-02-dev-environment/docs/setup-linux.md#3-docker-engine-not-docker-desktop).

---

## 2. CUDA out of memory on vLLM startup

**Symptom**: vLLM dies during model load with `torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate X GiB (GPU 0; Y GiB total capacity)`.

**Causes & fixes**, in priority order:

1. **Model is bigger than the GPU.** Pick a smaller one or a quantized variant. Llama-2 7B fp16 ≈ 14 GB. AWQ-quantized ≈ 7 GB.
2. **Another process is holding the GPU.** `nvidia-smi` will show it. Kill or restart: `sudo fuser -k /dev/nvidia*`.
3. **`GPU_MEMORY_UTILIZATION` too high.** Drop from `0.90` to `0.80`. vLLM reserves this fraction for weights + KV cache + activations.
4. **`MAX_MODEL_LEN` too long.** Long context = bigger KV cache. Drop from `8192` to `4096`.
5. **`--tensor-parallel-size` mismatched with GPU count.** TP must divide num_attention_heads.

If after all of the above you still OOM on a 24 GB consumer card with a 7B model, the issue is usually #3 + #4 together.

---

## 3. Mid-generation OOM

**Symptom**: vLLM serves a few requests fine, then under load throws `OOM during decode` and starts dropping requests. Throughput tanks.

**Cause**: PagedAttention KV cache is full. New requests can't get blocks until older ones finish.

**Fix**:

- Lower `max_num_seqs` (default 256 — try 128).
- Lower `max_num_batched_tokens` (default 2048 — try 1024).
- Increase `swap_space` (in GB) — vLLM swaps cold KV cache to CPU RAM. Set to 4-16 GB.
- Reject long prompts at the gateway. Add Pydantic validation on `len(prompt) <= MAX_PROMPT_TOKENS`.

The right combination depends on your model and traffic shape — instrument `vllm_kv_cache_usage_perc` and tune by hand.

---

## 4. vLLM health stays red

**Symptom**: Logs show "Engine started, ready for requests" but `/health` keeps returning 503 from the API gateway.

**Cause**: The API gateway is probing the vLLM container by container name, but DNS hasn't resolved yet, or the gateway's health check timeout is shorter than vLLM's startup.

**Fix**:

1. From inside the api container: `docker compose exec api curl -v http://vllm:8001/health`. If this works, the gateway code has a bug — check `src/api/health.py` to ensure it dials `vllm:8001`, not `localhost:8001`.
2. In `docker-compose.yaml`, add `depends_on` with `condition: service_healthy`:
   ```yaml
   api:
     depends_on:
       vllm:
         condition: service_healthy
   vllm:
     healthcheck:
       test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
       interval: 10s
       timeout: 5s
       retries: 30
       start_period: 120s
   ```

`start_period: 120s` is crucial — it gives vLLM time to load the model before health checks count.

---

## 5. First request takes tens of seconds

**Symptom**: First request after deploy takes 30-90 seconds. Subsequent identical requests are sub-second.

**Cause**: vLLM lazily JIT-compiles CUDA kernels for your specific (batch_size, seq_len) combination on first encounter. Same for `flash-attn`.

**Fix**:

- Pre-warm on startup: `scripts/warmup.py` sends 5-10 requests across the batch sizes you expect. Run as the last step in your readiness probe so traffic only starts when warmup finishes.
- For predictable latency, set `enforce_eager=True` on the LLM engine — skips compilation but loses 10-20% throughput. Worth it for short-burst APIs, not for sustained workloads.
- If using `torch.compile` anywhere in the pipeline, the first call rebuilds the graph. Move to background warmup.

---

## 6. Low tokens per second

**Symptom**: You're getting 80 tok/s where a benchmark blog promised 300.

**Diagnostic checklist**:

1. **GPU utilization**. `nvidia-smi dmon -s u` while requests are flowing. If sub-70%, you're CPU- or network-bound, not GPU-bound.
2. **Batch size**. vLLM's continuous batching only helps when concurrent requests overlap. With 1 client, you'll see single-stream throughput, period.
3. **Tensor parallelism**. TP > 1 with NVLink: linear speedup. TP > 1 on PCIe: degrades.
4. **Quantization tradeoff**. AWQ/GPTQ saves memory but adds dequantization overhead. fp16 is faster than AWQ on the same card if it fits.
5. **Tokenizer overhead**. Long prompts where the tokenizer call dominates — pre-tokenize at the gateway.
6. **flash-attn missing**. `pip list | grep flash-attn`. Without it, vLLM falls back to xformers which is 1.5-2× slower for long sequences.

Standard tuning order: confirm flash-attn → enable continuous batching → tune `max_num_seqs` → raise concurrency on the client.

---

## 7. Model registry conflicts

**Symptom**: Deploying a new model artifact fails with `ConflictError: model 'mistral-7b-instruct' version v3 already exists`. Or two regions disagree about which version is "latest".

**Cause**: The registry uses the artifact hash as identity, but you have a race where two CI jobs registered the same logical version with different content.

**Fix**:

1. Resolve conflict by content hash. Use the SHA-256 from `scripts/register_model.py --print-hash <artifact>` as the source of truth.
2. If two hashes claim the same name+version, fail loud and require a human to pick.
3. Add a CI lock: only one `register_model` job per (model_name, version) can run at a time. Use Redis SETNX with a 10-min TTL, or use Argo Workflows' `synchronization`.

To recover a corrupted registry entry:

```bash
python scripts/registry_admin.py inspect mistral-7b-instruct
python scripts/registry_admin.py delete mistral-7b-instruct --version v3 --confirm
python scripts/registry_admin.py register mistral-7b-instruct --version v3 --artifact ./artifacts/mistral-7b-v3.tar.gz
```

Never delete a model version that's actively pinned by a deployment. Check `kubectl get llm-deployments -A -o yaml | grep -A2 modelRef` first.

---

## 8. Retraining loop instability

**Symptom**: The continuous fine-tuning job (`src/training/loop.py`) starts, runs for 30-60 min, fails with `LossExploded` or `NaN encountered`, restarts via cron, fails again. Wastes GPU-hours and never produces a checkpoint.

**Causes** (multiple, usually together):

1. **Learning rate too high** for the dataset size. Continuous fine-tunes often inherit the original training LR which assumed millions of examples.
2. **Bad data slipping in.** Empty prompts, duplicated rows, leaked test data with the wrong label.
3. **Gradient clipping disabled.**
4. **Mixed precision overflow** without loss scaling.

**Fix sequence**:

1. **Stop the cron.** Don't keep wasting compute.
2. Run one epoch in `--dry-run` mode that prints per-batch loss and gradient norm.
3. Set `max_grad_norm: 1.0` in the trainer config. Mandatory.
4. Drop LR to 1/10 of the original. For SFT on a 7B base, `2e-5` is a safe default.
5. Add input validation in the data loader: skip examples where prompt or completion is empty or > MAX_LEN.
6. Enable gradient scaling for fp16, or switch to bf16 (no scaling needed).
7. Add an early-stopping guard: `if loss > 10x running_avg: abort`. Better to kill a bad run early than burn 6 hours.

---

## 9. ChromaDB collection corruption

**Symptom**: Queries against an existing collection return `NoIndexException` or `Cannot read index file: invalid hnsw header`. Process restarts don't help.

**Cause**: ChromaDB's HNSW index file got partially written — usually because the container OOM'd or the host rebooted mid-write. Chroma does not journal HNSW files.

**Fix** (data loss is acceptable here because embeddings are re-derivable):

```bash
# Stop chromadb
docker compose stop chromadb

# Inspect what's there
ls -la ./data/chroma/

# Remove the corrupt collection
COLL="getting-started"
rm -rf ./data/chroma/$COLL

docker compose up -d chromadb

# Re-ingest from source
python scripts/load_documents.py --source ./data/samples --collection $COLL
```

**Prevention** (you should do this anyway):

- Run periodic `scripts/chroma_backup.py` snapshots to S3/GCS. The script tars the persist dir into a versioned object.
- Add a startup integrity check: `python -m src.rag.vector_store check-all` returns non-zero exit if any HNSW file is bad. Hook it into the readiness probe.
- For production, consider Qdrant or Weaviate — both have write-ahead logs and survive crashes more gracefully.

---

## 10. Vector index dimension mismatch

**Symptom**: Ingestion succeeds, query fails with `Dimension mismatch: expected 384, got 768`.

**Cause**: You switched `EMBEDDING_MODEL` (e.g., from `all-MiniLM-L6-v2` (384) to `bge-base` (768)) without re-indexing.

**Fix**:

1. Pick the model you want.
2. Delete the affected collection (Chroma cannot retrofit dimensions).
3. Re-ingest. Same data, new embeddings.
4. **Lock the embedding model in code**: ChromaDB collections carry a metadata field `embedding_model`. Refuse to write into a collection whose metadata doesn't match the runtime config:
   ```python
   if coll.metadata.get("embedding_model") != settings.EMBEDDING_MODEL:
       raise EmbeddingModelMismatch(...)
   ```

If you must support migrating: maintain both collections (`docs_v1` 384-dim, `docs_v2` 768-dim) and route reads to v2 once it's caught up, then drop v1.

---

## 11. RAG returns irrelevant chunks

**Symptom**: Query that should hit a known document returns top-K chunks from totally different sources.

**Diagnostic order**:

1. **Tokenizer / language**. Chinese, code, math — many embedding models tank on these. Try `bge-m3` or `e5-multilingual`.
2. **Chunking too large**. 2000-char chunks are nearly random for cosine similarity. Drop to 300-500 with 50 overlap.
3. **Chunking too small**. < 100 chars and you're embedding header words. Combine with parent-page metadata.
4. **No metadata filtering**. Add filters: `collection.query(filter={"source": "docs/llmops"})`.
5. **No reranker**. Vector search gives you a coarse top-50; rerank with a cross-encoder to top-5. We ship `BAAI/bge-reranker-large` in `src/rag/reranker.py`.
6. **Query is too short**. "vllm batching" returns junk. Use query expansion: have the LLM rewrite the query into 3 variants and embed all three.
7. **Domain mismatch**. General embeddings don't know your jargon. Fine-tune embeddings on your domain (see Notebook 02 Section 7) or use a sparse + dense hybrid.

Run `scripts/rag_eval.py --corpus ./data/eval --queries ./data/eval-queries.jsonl` to get NDCG@10 — that tells you objectively whether changes are helping.

---

## 12. RAG returns duplicates

**Symptom**: Top-K chunks all say the same thing in slightly different words.

**Cause**: Adjacent overlapping chunks from the same document score similarly.

**Fix**:

- Use **MMR** (Maximal Marginal Relevance) instead of straight similarity. We expose `--retriever=mmr` in `src/rag/retriever.py`.
- Or post-filter: group by `metadata.doc_id`, keep top-1 per document, return top-K documents.
- Or use a reranker after the initial search and dedupe by `near-identical: cosine > 0.95`.

---

## 13. Embeddings bottleneck

**Symptom**: P95 latency on `/v1/rag/query` is 800ms with 80% of that in `embed_query`. The LLM is fast.

**Cause**: You're calling SentenceTransformer once per query, on CPU.

**Fix**:

- Run the embedding model on GPU: `EMBEDDING_DEVICE=cuda:0`. 10-30× speedup.
- Cache query embeddings in Redis with a hash key: identical queries return cached vectors instantly.
- Batch concurrent queries with a 5-10 ms window — turns N forward passes into one.
- Switch to a smaller model: `bge-small-en-v1.5` (33M params) is plenty for most retrieval and runs at ~1ms/query on a modern CPU.

---

## 14. Prompt evaluation drift after deploy

**Symptom**: You changed a prompt template, the LLM responses look fine in dev, but the eval harness in prod reports a 12% drop on the regression set.

**Causes**:

1. **Whitespace / token changes**. A leading newline you added has measurable effect on Llama-class models. Pin via `prompt_text.strip()` or version-snapshot the exact byte sequence.
2. **Variable interpolation order changed**. You moved `{context}` from before to after `{question}`. For many models, position-in-prompt matters.
3. **Eval set drift**, not prompt drift. Did the eval corpus change? Diff the SHA: `git log -p evals/regression-set.jsonl`.
4. **Sampling parameters not pinned to the eval**. Different temperature or top_p across runs makes results stochastic.

**Fix process**:

```bash
# Roll back the prompt
python scripts/prompt_registry.py rollback customer-support v7

# Compare prompts byte-by-byte
python scripts/prompt_registry.py diff customer-support v7 v8

# Re-run eval at fixed temperature=0, seed=42
python scripts/run_eval.py --prompt customer-support@v8 --temperature 0 --seed 42
```

Prevention: all prompts in version control. CI runs the eval suite on every prompt PR. PR fails if regression > 2%. A/B in production only after CI passes.

---

## 15. A/B test results flip

**Symptom**: Variant B wins by 8% on Tuesday, variant A wins by 5% on Friday. You can't ship either.

**Causes**:

1. **Sample size too small for the effect size.** 200 requests per arm is rarely enough. Use a power calculator: for 5% effect, alpha=0.05, you need ~1500/arm.
2. **Non-stationary traffic.** Tuesday is enterprise users, Friday is consumers. Stratify by user segment.
3. **Different model versions across days.** vLLM autoscaler killed and respawned with a different image tag. Pin the image SHA in the deployment.
4. **Outlier dragging the mean.** One 30-second response skews mean latency. Report P50 and P95 separately, not mean.

**Fix**:

- Compute the result properly: bootstrapped 95% CIs on the metric, not just the point estimate.
- Use `src/prompts/ab_testing.py:run_sequential_test` which stops when the CI excludes 0, not at a fixed N.
- Log which model SHA served each request. If the deploy changed mid-experiment, throw out the run.

---

## 16. Rate limiter returns 429 in normal traffic

**Symptom**: Your `RATE_LIMIT_RPM=60` setting is firing 429s even when one user sends 30 req/min.

**Causes**:

1. **Rate limiter keyed by IP, multiple users behind one NAT.** Switch the key to API key or user ID, not IP. `src/security/rate_limiter.py:RateLimiter(key_fn=lambda req: req.headers["x-api-key"])`.
2. **Token bucket bucket size = 1.** Bursts get punished immediately. Set `burst = max(rpm/4, 10)`.
3. **Redis clock skew.** If the limiter compares timestamps and your Redis container drifted, you get nondeterministic firing. Use Redis `TIME` command or pass `now_ts` explicitly.
4. **The 429 isn't from you — it's from upstream.** Check the response headers for `x-ratelimit-source`. Hugging Face Inference Endpoints sometimes 429 the model load itself.

---

## 17. PII redactor over or under

**Over-redacts**: "John works at GitHub" becomes "[NAME] works at [ORG]" and downstream consumers can't understand the response.

**Under-redacts**: Real emails leak through.

**Fix**:

- We use Presidio (`src/security/pii_detector.py`). Tune the confidence threshold per entity type:
  ```python
  redactor = Redactor(
      thresholds={"EMAIL_ADDRESS": 0.8, "PERSON": 0.95, "ORG": 0.95},
  )
  ```
- Add allowlist patterns: don't redact your own product name, your support address, common public companies.
- For under-redaction: add custom regex recognizers for your domain (employee IDs, internal URLs).
- Always log the redacted spans (not their content) so you can audit false positives.

Validate with `tests/security/test_pii_redactor.py` which has 50 hand-curated examples.

---

## 18. Cost numbers don't reconcile

**Symptom**: The system reports $230/day. The cloud bill shows $410/day.

**Causes**:

1. **You only charge for foreground requests.** Background jobs (embedding pre-compute, eval runs) burn GPU time too. Tag them with `cost_category=background` and include in totals.
2. **GPU idle time isn't free.** If your spot A10 runs 24h but only serves traffic 8h, the bill still says 24h. Compute `actual_gpu_hours = (now - boot_time)` not request-time.
3. **Egress.** Streaming responses across regions add CloudFront / data transfer charges you didn't model.
4. **Persistent disk + snapshots.** Multi-TB Chroma volumes accrue daily. Snapshots are billed separately.
5. **Token prices wrong.** You set `OUTPUT_TOKEN_COST_PER_1K=0.0002` but your actual marginal cost per output token (cost-of-GPU-second / tokens-per-second) is higher.

**Fix** — write a reconciliation report that subtracts what you tracked from what the bill says, broken out by category. Iterate. Don't claim "cost optimization" if your numbers are off by 40%.

---

## 19. Prometheus metrics gap

**Symptom**: Grafana shows a flat line / "No data" for the LLM request rate panel during peak load.

**Causes**:

1. **The API was OOM-killed and restarted.** Counter resets to 0. Use `rate()` or `increase()` in queries, not raw counters.
2. **Prometheus scrape interval too long.** Default 30s but your traffic spikes are 10s. Drop to 5s for the API job.
3. **`PROMETHEUS_MULTIPROC_DIR` not writable.** If you run uvicorn with multiple workers, every worker needs the shared dir. Bind a tmpfs and `chmod 1777` it.
4. **OpenTelemetry collector queue overflowed.** Check `otelcol` logs for `queue is full`. Bump `sending_queue.queue_size` or scale otelcol replicas.

---

## 20. Streaming cuts off

**Symptom**: SSE streaming responses end mid-token. Client sees half a sentence.

**Causes**:

1. **Reverse proxy buffers SSE.** NGINX must have `proxy_buffering off` and `X-Accel-Buffering: no` header set on the response.
2. **Timeout shorter than generation.** Cloudflare default is 100s. For a 500-token response at 50 tok/s, you're cutting it close. Bump proxy timeouts to 300s for streaming routes.
3. **vLLM aborted the request.** Look for `request_id=... aborted` in vllm logs. Usually because the client disconnected and the engine cleaned up — confirm with `enable_keep_alive` and TCP keepalives on the client.
4. **JSON instead of SSE.** Some clients try to parse the whole stream as one JSON. Use a real SSE library (`eventsource` in JS, `httpx-sse` in Python).

---

## When to escalate

If you've tried the relevant section and the issue persists for over an hour, capture:

- The full request/response.
- `docker compose ps` output.
- The last 200 lines of the relevant service logs.
- `nvidia-smi` output if GPU-related.
- The output of `python scripts/diagnose.py` (which checks all of the above automatically).

Open an issue in the curriculum repo with that bundle. Don't paste screenshots of terminal text — paste the text.
