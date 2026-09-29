from __future__ import annotations
from typing import Any


def audit_binary_predictions(rows: list[dict[str, str]], true_field: str = "y_true", pred_field: str = "y_pred", confidence_field: str = "confidence", bins: int = 10) -> dict[str, Any]:
    parsed = []
    for row in rows:
        try:
            y = int(row[true_field])
            yp = int(row[pred_field])
            c = float(row[confidence_field])
        except (KeyError, TypeError, ValueError):
            continue
        if y not in (0, 1) or yp not in (0, 1) or not 0 <= c <= 1:
            continue
        p1 = c if yp == 1 else 1 - c
        parsed.append((y, yp, c, p1))
    n = len(parsed)
    if not n:
        return {"n": 0, "error": "No valid binary prediction rows"}
    accuracy = sum(y == yp for y, yp, _, _ in parsed) / n
    brier = sum((p1 - y) ** 2 for y, _, _, p1 in parsed) / n
    ece = 0.0
    details = []
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        bucket = [(y, yp, c) for y, yp, c, _ in parsed if lo <= c < hi or (b == bins - 1 and c == 1.0)]
        if not bucket:
            continue
        acc = sum(y == yp for y, yp, _ in bucket) / len(bucket)
        conf = sum(c for _, _, c in bucket) / len(bucket)
        ece += (len(bucket) / n) * abs(acc - conf)
        details.append({"bin": b, "n": len(bucket), "accuracy": acc, "mean_confidence": conf})
    return {"n": n, "accuracy": accuracy, "brier_score": brier, "ece": ece, "bins": bins, "bin_details": details}
