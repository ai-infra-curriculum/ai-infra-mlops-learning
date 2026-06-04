"""Tamper-evident append-only audit log via hash chaining."""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class AuditEvent:
    seq: int
    ts: float
    event_type: str
    actor: str
    payload: dict
    prev_hash: str
    this_hash: str


def _hash(event: dict) -> str:
    canonical = json.dumps(event, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(canonical).hexdigest()


class AuditChain:
    """In-memory hash chain. Persist to DB by writing each event to a table."""

    def __init__(self):
        self._events: list[AuditEvent] = []

    def append(self, event_type: str, actor: str, payload: dict) -> AuditEvent:
        seq = len(self._events)
        prev_hash = self._events[-1].this_hash if self._events else "0" * 64
        body = {
            "seq": seq, "ts": time.time(), "event_type": event_type,
            "actor": actor, "payload": payload, "prev_hash": prev_hash,
        }
        body["this_hash"] = _hash(body)
        ev = AuditEvent(**body)
        self._events.append(ev)
        return ev

    def verify(self) -> tuple[bool, int | None]:
        """Return (ok, first_broken_seq). Walks the chain re-computing hashes."""
        prev_hash = "0" * 64
        for ev in self._events:
            body = asdict(ev)
            stored = body.pop("this_hash")
            if body["prev_hash"] != prev_hash:
                return False, ev.seq
            if _hash(body) != stored:
                return False, ev.seq
            prev_hash = stored
        return True, None

    def events(self) -> list[AuditEvent]:
        return list(self._events)
