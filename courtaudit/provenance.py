from __future__ import annotations
import hashlib
from pathlib import Path
from typing import Any
from .io import canonical_json_bytes


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def record_hash(record: dict[str, Any], exclude: tuple[str, ...] = ("record_hash",)) -> str:
    obj = {k: v for k, v in record.items() if k not in exclude}
    return sha256_bytes(canonical_json_bytes(obj))


def audit_record_hashes(records: list[dict[str, Any]]) -> dict[str, Any]:
    checked = 0
    mismatches = []
    computed = {}
    for i, rec in enumerate(records):
        rid = str(rec.get("record_id", i))
        digest = record_hash(rec)
        computed[rid] = digest
        declared = rec.get("record_hash")
        if declared:
            checked += 1
            if declared != digest:
                mismatches.append({"record_id": rid, "declared": declared, "computed": digest})
    return {
        "n_records": len(records),
        "n_declared_hashes_checked": checked,
        "n_mismatches": len(mismatches),
        "mismatches": mismatches,
        "computed_hashes": computed,
    }
