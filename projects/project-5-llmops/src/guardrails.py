"""Input + output guardrails: injection + PII + max-tokens."""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class GuardResult:
    allowed: bool
    reason: str = ""
    sanitized: str | None = None


_INJECTION = [
    re.compile(r"ignore (the )?(previous|prior|above) instructions", re.I),
    re.compile(r"\byou are (now |from now on )?(in )?(developer|admin|root) mode\b", re.I),
    re.compile(r"\breveal (your |the )?(system )?prompt\b", re.I),
]

_PII = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b\d{16}\b"),
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
]


def check_input(text: str, max_chars: int = 50000) -> GuardResult:
    if len(text) > max_chars:
        return GuardResult(allowed=False, reason=f"input>{max_chars}chars")
    for pattern in _INJECTION:
        if pattern.search(text):
            return GuardResult(allowed=False, reason=f"injection:{pattern.pattern[:30]}")
    sanitized = text
    for pattern in _PII:
        sanitized = pattern.sub("[REDACTED]", sanitized)
    return GuardResult(allowed=True, sanitized=sanitized)


def check_output(text: str) -> GuardResult:
    redacted = text
    for pattern in _PII:
        redacted = pattern.sub("[REDACTED]", redacted)
    return GuardResult(allowed=True, sanitized=redacted)
