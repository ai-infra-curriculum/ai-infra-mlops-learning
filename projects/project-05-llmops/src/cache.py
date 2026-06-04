"""Semantic cache: hash-based first, fall back to embedding similarity."""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass

import redis.asyncio as redis


@dataclass
class CacheHit:
    response: str
    age_seconds: float
    kind: str        # exact | semantic


def _key(prompt: str) -> str:
    return "llmcache:" + hashlib.sha256(prompt.encode()).hexdigest()


class ExactCache:
    """Cheapest layer: byte-exact match."""
    def __init__(self, redis_client: redis.Redis, ttl_seconds: int = 3600):
        self.r = redis_client
        self.ttl = ttl_seconds

    async def get(self, prompt: str) -> CacheHit | None:
        raw = await self.r.get(_key(prompt))
        if not raw:
            return None
        data = json.loads(raw)
        return CacheHit(response=data["response"], age_seconds=time.time() - data["ts"], kind="exact")

    async def put(self, prompt: str, response: str):
        await self.r.setex(_key(prompt), self.ttl,
                            json.dumps({"response": response, "ts": time.time()}))
