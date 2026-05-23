"""LLMOps gateway. Composes: rate limit → guard → cache → RAG → LLM → cost."""
from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager

import httpx
import redis.asyncio as redis
from fastapi import Depends, FastAPI, HTTPException, Request
from prometheus_client import make_asgi_app
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.cache import ExactCache
from src.config import Settings
from src.cost import count_tokens, estimate_cost
from src.guardrails import check_input, check_output
from src.metrics import (ACTIVE_REQUESTS, CACHE, COST_USD_TOTAL, GUARD_BLOCKS,
                          REQUEST_LATENCY, TOKENS_TOTAL, TTFT)
from src.rag import DocStore


log = logging.getLogger("llmops")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    app.state.settings = settings
    app.state.http = httpx.AsyncClient(timeout=120)
    app.state.redis = await redis.from_url(settings.redis_url)
    app.state.cache = ExactCache(app.state.redis)
    try:
        app.state.docs = DocStore(settings.chroma_url, settings.chroma_collection)
    except Exception as e:
        log.warning(f"chroma unavailable: {e}; RAG disabled")
        app.state.docs = None
    yield
    await app.state.http.aclose()
    await app.state.redis.aclose()


limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="llmops-gateway", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.mount("/metrics", make_asgi_app())


class ChatReq(BaseModel):
    prompt: str
    use_rag: bool = False
    max_tokens: int = 500
    temperature: float = 0.0


def settings_dep(request: Request) -> Settings:
    return request.app.state.settings


@app.get("/health")
def health(): return {"status": "ok"}


@app.post("/v1/chat")
@limiter.limit("60/minute")
async def chat(request: Request, body: ChatReq, settings: Settings = Depends(settings_dep)):
    t0 = time.perf_counter()
    ACTIVE_REQUESTS.inc()
    try:
        # 1. Input guard
        ig = check_input(body.prompt)
        if not ig.allowed:
            GUARD_BLOCKS.labels(rule="input").inc()
            REQUEST_LATENCY.labels("chat", "blocked").observe(time.perf_counter() - t0)
            raise HTTPException(400, f"input rejected: {ig.reason}")
        prompt = ig.sanitized or body.prompt

        # 2. RAG context
        if body.use_rag and request.app.state.docs is not None:
            hits = request.app.state.docs.search(prompt, k=4)
            context = "\n\n".join(f"[{h.id}] {h.text[:500]}" for h in hits)
            prompt = f"Use these sources to answer. Cite as [id].\n\n{context}\n\nQuestion: {prompt}"

        # 3. Cache
        hit = await request.app.state.cache.get(prompt)
        if hit:
            CACHE.labels(outcome="hit").inc()
            REQUEST_LATENCY.labels("chat", "cache_hit").observe(time.perf_counter() - t0)
            return {"response": hit.response, "cached": True, "kind": hit.kind}
        CACHE.labels(outcome="miss").inc()

        # 4. LLM call
        async with request.app.state.http.stream(
            "POST",
            f"{settings.llm_backend_url}/completions",
            json={
                "model": settings.llm_model,
                "prompt": prompt,
                "max_tokens": body.max_tokens,
                "temperature": body.temperature,
            },
        ) as response:
            response.raise_for_status()
            t_first = None
            chunks: list[str] = []
            async for line in response.aiter_lines():
                if not line:
                    continue
                if t_first is None:
                    t_first = time.perf_counter()
                    TTFT.labels(model=settings.llm_model).observe(t_first - t0)
                chunks.append(line)
            full = "".join(chunks)

        # 5. Output guard
        og = check_output(full)
        response_text = og.sanitized or full

        # 6. Cost + tokens
        pt = count_tokens(prompt, settings.llm_model)
        ct = count_tokens(response_text, settings.llm_model)
        TOKENS_TOTAL.labels(model=settings.llm_model, direction="input").inc(pt)
        TOKENS_TOTAL.labels(model=settings.llm_model, direction="output").inc(ct)
        cost = estimate_cost(pt, ct, settings.cost_per_1k_input, settings.cost_per_1k_output)
        COST_USD_TOTAL.labels(model=settings.llm_model).inc(cost)

        # 7. Cache write
        await request.app.state.cache.put(prompt, response_text)

        REQUEST_LATENCY.labels("chat", "ok").observe(time.perf_counter() - t0)
        return {
            "response": response_text,
            "cached": False,
            "tokens": {"prompt": pt, "completion": ct},
            "cost_usd": round(cost, 6),
        }
    finally:
        ACTIVE_REQUESTS.dec()


class IngestReq(BaseModel):
    docs: list[dict]    # [{"id": "...", "text": "...", "metadata": {...}}]


@app.post("/v1/rag/ingest")
async def rag_ingest(req: IngestReq, request: Request):
    if request.app.state.docs is None:
        raise HTTPException(503, "RAG backend unavailable")
    from src.rag import Doc
    request.app.state.docs.add([Doc(**d) for d in req.docs])
    return {"ingested": len(req.docs)}
