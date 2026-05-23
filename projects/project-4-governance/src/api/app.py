"""Governance API: fairness reports, model cards, audit log, GDPR endpoints."""
from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import UTC, datetime

import numpy as np
from fastapi import FastAPI, HTTPException
from prometheus_client import make_asgi_app
from pydantic import BaseModel

from src.audit import AuditChain
from src.fairness import assess
from src.model_cards import CardData, render


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.audit = AuditChain()
    yield


app = FastAPI(title="ml-governance", lifespan=lifespan)
app.mount("/metrics", make_asgi_app())


class FairnessReq(BaseModel):
    y_true: list[int]
    y_pred: list[int]
    sensitive: list[str]


class ModelCardReq(BaseModel):
    model_name: str
    version: str
    intended_use: str
    out_of_scope: str = ""
    data_source: str
    data_window: str
    data_rows: int
    algorithm: str
    hyperparameters: str
    compute: str
    primary_metric_name: str
    primary_metric_value: float
    slice_metrics: dict
    sensitive_attribute: str
    disparate_impact: float
    passes_fairness: bool


@app.get("/health")
def health(): return {"status": "ok"}


@app.post("/v1/fairness")
def fairness(req: FairnessReq):
    report = assess(np.array(req.y_true), np.array(req.y_pred), np.array(req.sensitive))
    app.state.audit.append("fairness.assess", "api",
                           {"sample_size": len(req.y_true),
                             "disparate_impact": report.disparate_impact})
    return report


@app.post("/v1/model-cards")
def make_card(req: ModelCardReq):
    card = CardData(
        eng_lead="", ds_lead="", known_biases="", eng_approval="pending",
        compliance_approval="pending", ds_approval="pending",
        timestamp=datetime.now(UTC).isoformat(),
        **req.dict(),
    )
    text = render(card)
    app.state.audit.append("modelcard.create", "api",
                           {"model_name": req.model_name, "version": req.version})
    return {"model_card": text}


@app.get("/v1/audit")
def audit_log():
    return {"events": [e.__dict__ for e in app.state.audit.events()]}


@app.get("/v1/audit/verify")
def audit_verify():
    ok, broken = app.state.audit.verify()
    return {"valid": ok, "first_broken_seq": broken}
