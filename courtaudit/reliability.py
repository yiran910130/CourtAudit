from __future__ import annotations
from collections import Counter, defaultdict
from typing import Any


def percent_agreement(pairs: list[tuple[str, str]]) -> float | None:
    if not pairs:
        return None
    return sum(a == b for a, b in pairs) / len(pairs)


def cohens_kappa(pairs: list[tuple[str, str]]) -> float | None:
    if not pairs:
        return None
    po = percent_agreement(pairs)
    a = Counter(x for x, _ in pairs)
    b = Counter(y for _, y in pairs)
    labels = set(a) | set(b)
    n = len(pairs)
    pe = sum((a[l] / n) * (b[l] / n) for l in labels)
    if pe == 1:
        return 1.0 if po == 1 else None
    return (po - pe) / (1 - pe)


def krippendorff_alpha_nominal(item_labels: dict[str, list[str]]) -> float | None:
    usable = {k: v for k, v in item_labels.items() if len(v) >= 2}
    if not usable:
        return None
    do_num = 0.0
    do_den = 0.0
    pooled = Counter()
    for labels in usable.values():
        pooled.update(labels)
        n = len(labels)
        disagree = sum(1 for i in range(n) for j in range(i + 1, n) if labels[i] != labels[j])
        pairs = n * (n - 1) / 2
        do_num += disagree
        do_den += pairs
    do = do_num / do_den if do_den else 0.0
    N = sum(pooled.values())
    if N < 2:
        return None
    same = sum(c * (c - 1) for c in pooled.values())
    pe_same = same / (N * (N - 1))
    de = 1 - pe_same
    if de == 0:
        return 1.0 if do == 0 else None
    return 1 - do / de


def audit_annotations(rows: list[dict[str, str]], item_field: str = "item_id", coder_field: str = "coder_id", label_field: str = "label") -> dict[str, Any]:
    by_item: dict[str, list[tuple[str, str]]] = defaultdict(list)
    coders = set()
    for row in rows:
        item, coder, label = row.get(item_field), row.get(coder_field), row.get(label_field)
        if item and coder and label != "":
            by_item[item].append((coder, label))
            coders.add(coder)
    coder_list = sorted(coders)
    paired = []
    if len(coder_list) == 2:
        c1, c2 = coder_list
        for item, vals in by_item.items():
            d = dict(vals)
            if c1 in d and c2 in d:
                paired.append((d[c1], d[c2]))
    labels_only = {item: [label for _, label in vals] for item, vals in by_item.items()}
    return {
        "n_rows": len(rows),
        "n_items": len(by_item),
        "n_coders": len(coder_list),
        "coders": coder_list,
        "pairwise_percent_agreement": percent_agreement(paired),
        "cohens_kappa_two_coders": cohens_kappa(paired),
        "krippendorff_alpha_nominal": krippendorff_alpha_nominal(labels_only),
    }
