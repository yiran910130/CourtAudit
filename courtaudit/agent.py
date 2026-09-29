from __future__ import annotations
from typing import Any

REQUIRED = ("request_id", "response_text", "completion_status")


def audit_agent_outputs(records: list[dict[str, Any]]) -> dict[str, Any]:
    issues = []
    for i, rec in enumerate(records):
        rid = rec.get("request_id", i)
        missing = [k for k in REQUIRED if k not in rec]
        if missing:
            issues.append({"request_id": rid, "code": "MISSING_AGENT_FIELD", "fields": missing})
        if rec.get("completion_status") != "complete":
            issues.append({"request_id": rid, "code": "INCOMPLETE_RESPONSE", "value": rec.get("completion_status")})
        if rec.get("direct_model_inference") is False:
            issues.append({"request_id": rid, "code": "NON_DIRECT_INFERENCE"})
        if rec.get("web_search_used") is True:
            issues.append({"request_id": rid, "code": "WEB_SEARCH_USED"})
        if rec.get("external_sources_used") is True:
            issues.append({"request_id": rid, "code": "EXTERNAL_SOURCE_USED"})
        text = rec.get("response_text")
        if isinstance(text, str) and not text.strip():
            issues.append({"request_id": rid, "code": "EMPTY_RESPONSE"})
    return {"n_records": len(records), "n_issues": len(issues), "pass": not issues, "issues": issues}
