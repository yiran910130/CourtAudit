from __future__ import annotations
from collections import Counter
from typing import Any

DEFAULT_REQUIRED = ("record_id", "source_id", "text")


def validate_records(records: list[dict[str, Any]], required: tuple[str, ...] = DEFAULT_REQUIRED) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    ids: list[str] = []
    for idx, rec in enumerate(records):
        missing = [k for k in required if k not in rec or rec[k] in (None, "")]
        if missing:
            errors.append({"row": idx, "code": "MISSING_REQUIRED", "fields": missing})
        rid = rec.get("record_id")
        if rid not in (None, ""):
            ids.append(str(rid))
        text = rec.get("text")
        if text is not None and not isinstance(text, str):
            errors.append({"row": idx, "code": "TEXT_NOT_STRING"})
    dup_ids = [k for k, v in Counter(ids).items() if v > 1]
    if dup_ids:
        errors.append({"code": "DUPLICATE_RECORD_ID", "record_ids": sorted(dup_ids)})
    return {
        "n_records": len(records),
        "required_fields": list(required),
        "valid": not errors,
        "n_errors": len(errors),
        "errors": errors,
    }
