# Getting Started — Project 5: LLMOps Production System

This guide takes you from a freshly cloned repo to a working LLMOps stack you can hit with `curl`. Plan for **2-3 hours** the first time, plus model download time (which depends on your bandwidth — typically 15-90 minutes).

If you only want to read about the system before building it, start with [README.md](README.md) and [ARCHITECTURE.md](ARCHITECTURE.md). This file is for getting your hands dirty.

---

## What you'll have at the end

- vLLM serving an LLM on your GPU (or a mock backend on CPU).
- ChromaDB holding embeddings for a small RAG corpus.
- A FastAPI gateway in front exposing `/completions`, `/rag`, `/admin`.
- Prometheus scraping metrics, Grafana showing them.
- Redis enforcing rate limits.
- A smoke test that proves end-to-end works.

---

## 1. Prerequisites

### Hardware

| Tier | What you can run |
|---|---|
| CPU-only (mock or tiny GGUF model) | Smoke tests, RAG without real generation, full observability |
| 1× consumer GPU (RTX 3090/4090, 24 GB) | TinyLlama 1.1B, Llama-2 7B AWQ-quantized, Mistral 7B AWQ |
| 1× A10/A100 (24-80 GB) | Llama-2 7B fp16, Mistral 7B fp16, Mixtral 8×7B AWQ |
| Multi-GPU (2× A100+) | 70B-class models with tensor parallelism |

The bare minimum to do the full exercise meaningfully is the consumer-GPU tier. Without a GPU, use `MODEL_BACKEND=mock` and you'll still exercise the entire control plane.

### Software

- **OS**: Linux (Ubuntu 22.04 strongly preferred). macOS works only for mock backend. Windows via WSL2.
- **Python**: 3.11.x (3.12 has incompatibilities with several vLLM extras as of 2026-05).
- **Docker**: 24.0+ with Compose v2 plugin.
- **CUDA**: 12.1 or 12.4 (matches the torch wheels in `requirements.txt`).
- **NVIDIA Container Toolkit**: for GPU access from containers.
- **kubectl + helm + kind**: only if you also do the Kubernetes path.

Verify:

```bash
python --version           # 3.11.x
docker --version           # 24+
docker compose version     # v2+
nvidia-smi                 # GPU present, driver loaded
docker run --rm --gpus all nvidia/cuda:12.4.0-base-ubuntu22.04 nvidia-smi  # GPU visible in container
```

If `nvidia-smi` works on the host but not in the container, install the NVIDIA Container Toolkit (see Orientation Exercise 02 [docs/setup-linux.md Section 3](../../../ai-infra-junior-engineer-solutions/modules/mod-000-orientation/exercise-02-dev-environment/docs/setup-linux.md#3-docker-engine-not-docker-desktop)).

### Accounts / credentials

- **Hugging Face account**: required for gated models like Llama-2. Create at https://huggingface.co/join, accept the Llama-2 license at https://huggingface.co/meta-llama/Llama-2-7b-chat-hf, then `huggingface-cli login` with a read token.
- **OpenAI / Anthropic API key**: not required. The project is self-hosted by default. Only needed for the "compare with hosted models" notebook.

---

## 2. Clone and base setup

```bash
cd ~/code
git clone <your-fork-url> ai-infra-mlops-learning
cd ai-infra-mlops-learning/projects/project-05-llmops

# Create the venv with the exact Python you want
pyenv local 3.11.9
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip wheel
```

---

## 3. Install dependencies

There are three install paths depending on what you'll run.

### 3a. CPU / mock-only (no GPU)

Fastest. Skips vLLM and torch CUDA wheels.

```bash
LLMOPS_INSTALL_PROFILE=cpu pip install -r requirements.txt
```

### 3b. GPU (vLLM + flash-attn)

```bash
pip install -r requirements.txt
# vLLM pulls a CUDA-matched torch. If you have an older driver:
# pip install torch==2.3.1+cu121 --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements-dev.txt    # tests + linters
```

### 3c. Dev (everything)

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
pre-commit install
```

Verify the imports the rest of the project relies on:

```bash
python - <<'EOF'
import importlib, sys
for name in ("fastapi", "uvicorn", "pydantic", "chromadb", "langchain", "redis", "prometheus_client"):
    try:
        importlib.import_module(name); print(f"  ok  {name}")
    except Exception as e:
        print(f"  FAIL {name}: {e}", file=sys.stderr); sys.exit(1)
try:
    import vllm; print(f"  ok  vllm {vllm.__version__}")
except Exception:
    print("  warn vllm not installed (fine for CPU profile)")
EOF
```

---

## 4. Configure the environment

```bash
cp .env.example .env
```

Open `.env` and set, at minimum:

```bash
# Backend selection
MODEL_BACKEND=vllm                  # or 'mock' for no GPU
MODEL_NAME=TinyLlama/TinyLlama-1.1B-Chat-v1.0    # safe first choice
MAX_MODEL_LEN=2048
GPU_MEMORY_UTILIZATION=0.85

# Embeddings (used for RAG)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Storage
CHROMA_PERSIST_DIR=./data/chroma
PROMPT_REGISTRY_DIR=./prompts

# Auth / rate limiting
API_KEYS=dev-key-please-rotate
RATE_LIMIT_RPM=60
REDIS_URL=redis://localhost:6379/0

# Cost tracking
GPU_COST_PER_HOUR=1.0
INPUT_TOKEN_COST_PER_1K=0.0001
OUTPUT_TOKEN_COST_PER_1K=0.0002

# Observability
PROMETHEUS_MULTIPROC_DIR=/tmp/prom_multiproc
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
LOG_LEVEL=INFO
```

Important: `API_KEYS` is comma-separated. **Rotate dev-key-please-rotate before exposing the service to anyone else.**

---

## 5. Pre-download the model (recommended)

vLLM will fetch the model on first request, but doing it now means your first health check isn't 90 minutes long.

```bash
huggingface-cli login                                  # only needed for gated models
huggingface-cli download TinyLlama/TinyLlama-1.1B-Chat-v1.0
huggingface-cli download sentence-transformers/all-MiniLM-L6-v2
```

The download cache lives in `~/.cache/huggingface/hub` and is shared across all your projects, so this is a one-time cost per model.

---

## 6. Start the stack (Docker Compose path)

```bash
docker compose up -d
docker compose ps
```

You should see:

| Service | Healthy when |
|---|---|
| `vllm` | `/health` returns 200 (60-120s after start) |
| `api` | `/health` returns 200 (5-10s after vllm) |
| `chromadb` | port 8001 responds to `/api/v1/heartbeat` |
| `redis` | `redis-cli -p 6379 ping` returns PONG |
| `prometheus` | port 9090 web UI loads |
| `grafana` | port 3000 web UI loads (admin/admin) |

Tail logs while it spins up:

```bash
docker compose logs -f vllm api
```

Common first-run output you want to see in vllm logs:

```
INFO ... Loading model weights took XX seconds
INFO ... Engine started, ready for requests
```

Common first-run output you want to NOT see:

- `CUDA out of memory` — drop `GPU_MEMORY_UTILIZATION` or pick a smaller model.
- `Connection refused` between services — `docker compose down && docker compose up -d` to recreate the network.

---

## 7. Smoke test

### 7a. Basic completion

```bash
curl -sS http://localhost:8000/v1/completions \
  -H "Authorization: Bearer dev-key-please-rotate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Briefly: what is LLMOps?",
    "max_tokens": 80,
    "temperature": 0.2
  }' | jq .
```

Expected: a JSON envelope with `choices[0].text` containing one or two sentences.

### 7b. RAG ingestion + retrieval

```bash
# Ingest a corpus
curl -sS http://localhost:8000/v1/rag/ingest \
  -H "Authorization: Bearer dev-key-please-rotate" \
  -F "files=@./data/samples/llmops-intro.md" \
  -F "files=@./data/samples/vllm-faq.md" \
  -F "collection=getting-started" | jq .

# Ask a question grounded in that corpus
curl -sS http://localhost:8000/v1/rag/query \
  -H "Authorization: Bearer dev-key-please-rotate" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does vLLM batch requests?",
    "collection": "getting-started",
    "top_k": 4
  }' | jq .
```

Expected: an `answer` field plus a `sources` array with at least one snippet from `vllm-faq.md`.

### 7c. Observability

- Open Prometheus: http://localhost:9090 — query `llmops_request_duration_seconds_count` and you should see your requests from the previous steps.
- Open Grafana: http://localhost:3000 (admin/admin) -> Dashboards -> "LLMOps Overview".
- Open Swagger: http://localhost:8000/docs.

### 7d. Cost endpoint

```bash
curl -sS http://localhost:8000/v1/admin/cost \
  -H "Authorization: Bearer dev-key-please-rotate" | jq .
```

You should see per-request cost calculated from your `INPUT_TOKEN_COST_PER_1K` / `OUTPUT_TOKEN_COST_PER_1K` settings.

---

## 8. First end-to-end run — `make smoke`

The repo provides a one-shot test that exercises everything:

```bash
make smoke
```

What it does:

1. Pings every service health endpoint.
2. Sends 10 completion requests at concurrency 2.
3. Ingests three sample documents.
4. Runs 5 RAG queries.
5. Asserts P95 latency under `SMOKE_P95_MS` (default 8000 — generous for first runs).
6. Asserts cost accounting incremented.
7. Tails recent Grafana panel data to confirm metrics flowed.

Expected exit code 0. Output saved to `./reports/smoke-<timestamp>.json`.

---

## 9. Run locally (no Docker)

Useful for fast iteration on the API or RAG code without rebuilding images.

```bash
# Terminal 1 — start dependencies only
docker compose up -d chromadb redis prometheus grafana

# Terminal 2 — vLLM (or mock)
export MODEL_BACKEND=mock          # easiest path while iterating
python -m src.llm.vllm_server      # binds 8001

# Terminal 3 — API
uvicorn src.api.main:app --reload --port 8000
```

Hit `http://localhost:8000/docs` as before.

---

## 10. Run the test suite

```bash
pytest -q                                 # unit
pytest tests/integration -q               # integration (requires services up)
pytest --cov=src --cov-report=term-missing
```

Target coverage on this project: **80% lines, 70% branches**. CI fails below.

Common pre-test fixture errors:

- `redis.exceptions.ConnectionError` — start Redis (`docker compose up -d redis`).
- `chromadb.errors.NoIndexException` — clear `./data/chroma` and re-run; the test bootstraps a fresh collection.

---

## 11. Next steps

Once the smoke test passes, work through the project in this order:

1. **Notebook 01 — LLM Serving Demo**: explore vLLM's PagedAttention behavior, batch size tuning, streaming.
2. **Notebook 02 — RAG Pipeline**: try semantic vs sliding-window chunking, swap embeddings, reranker on/off.
3. **Notebook 03 — Prompt Engineering**: use the A/B harness on two prompt variants for the same task.
4. **Notebook 04 — Performance Analysis**: run `scripts/benchmark.py` at different concurrencies.
5. **Notebook 05 — Cost Analysis**: walk through the cost optimization recommendations.

Then:

- Deploy to a local Kind cluster: `kubectl apply -k infrastructure/kubernetes/overlays/dev/`.
- Run the validation checklist: [VALIDATION.md](VALIDATION.md).
- Diagnose problems: [docs/troubleshooting.md](docs/troubleshooting.md).

---

## Troubleshooting quick links

- vLLM won't start / CUDA OOM → [docs/troubleshooting.md #2](docs/troubleshooting.md#2-cuda-out-of-memory-on-vllm-startup)
- Slow first request → [docs/troubleshooting.md #5](docs/troubleshooting.md#5-first-request-takes-tens-of-seconds)
- ChromaDB collection corrupted → [docs/troubleshooting.md #9](docs/troubleshooting.md#9-chromadb-collection-corruption)
- RAG returns irrelevant chunks → [docs/troubleshooting.md #11](docs/troubleshooting.md#11-rag-returns-irrelevant-chunks)
- Prompt eval drift between deploys → [docs/troubleshooting.md #14](docs/troubleshooting.md#14-prompt-evaluation-drift-after-deploy)
- Rate limiter returns 429 in normal traffic → [docs/troubleshooting.md #16](docs/troubleshooting.md#16-rate-limiter-returns-429-in-normal-traffic)

If you hit something not listed, capture (a) the request that triggered it, (b) the relevant container logs, and (c) `docker compose ps` output, then open a discussion thread.
