from __future__ import annotations
import re
from collections import defaultdict
from typing import Any


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", text.lower(), flags=re.UNICODE)).strip()


def audit_leakage(records: list[dict[str, Any]], split_field: str = "split", group_field: str = "source_id") -> dict[str, Any]:
    text_splits: dict[str, set[str]] = defaultdict(set)
    text_records: dict[str, list[str]] = defaultdict(list)
    group_splits: dict[str, set[str]] = defaultdict(set)
    for i, rec in enumerate(records):
        rid = str(rec.get("record_id", i))
        split = str(rec.get(split_field, "UNSPECIFIED"))
        text = rec.get("text")
        if isinstance(text, str):
            norm = normalize_text(text)
            text_splits[norm].add(split)
            text_records[norm].append(rid)
        group = rec.get(group_field)
        if group not in (None, ""):
            group_splits[str(group)].add(split)
    duplicate_cross_split = [
        {"record_ids": text_records[t], "splits": sorted(splits), "normalized_text": t}
        for t, splits in text_splits.items() if len(splits) > 1
    ]
    group_cross_split = [
        {group_field: g, "splits": sorted(splits)} for g, splits in group_splits.items() if len(splits) > 1
    ]
    return {
        "n_records": len(records),
        "split_field": split_field,
        "group_field": group_field,
        "n_cross_split_text_duplicates": len(duplicate_cross_split),
        "cross_split_text_duplicates": duplicate_cross_split,
        "n_cross_split_groups": len(group_cross_split),
        "cross_split_groups": group_cross_split,
        "pass": not duplicate_cross_split and not group_cross_split,
    }
