"""GDPR-style data subject endpoints (delete, export, explain)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SubjectRequest:
    subject_id: str
    request_type: str          # delete | export | explain
    actor: str


class GDPRHandler:
    def __init__(self, feature_store, audit_chain):
        self.feature_store = feature_store
        self.audit = audit_chain

    def handle(self, req: SubjectRequest) -> dict:
        if req.request_type == "delete":
            n = self.feature_store.delete_subject(req.subject_id)
            self.audit.append("gdpr.delete", req.actor,
                              {"subject_id": req.subject_id, "rows_deleted": n})
            return {"deleted_rows": n}

        if req.request_type == "export":
            rows = self.feature_store.export_subject(req.subject_id)
            self.audit.append("gdpr.export", req.actor,
                              {"subject_id": req.subject_id, "rows_returned": len(rows)})
            return {"rows": rows}

        if req.request_type == "explain":
            # In a real system: load model, run SHAP, return per-feature attributions
            self.audit.append("gdpr.explain", req.actor, {"subject_id": req.subject_id})
            return {"explanation": "feature attributions (SHAP) returned"}

        raise ValueError(f"unknown request_type: {req.request_type}")
