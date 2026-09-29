from __future__ import annotations
import csv, statistics, time, tracemalloc
from pathlib import Path
from courtaudit.schema import validate_records
from courtaudit.provenance import audit_record_hashes
from courtaudit.leakage import audit_leakage

SIZES = [100, 1000, 5000, 20000]
REPEATS = 10


def build_records(n: int):
    return [
        {
            "record_id": f"r{i:06d}",
            "source_id": f"source{i:06d}",
            "text": f"Synthetic institutional-language record number {i} with stable content.",
            "split": ("train" if i % 5 < 3 else "dev" if i % 5 == 3 else "test"),
        }
        for i in range(n)
    ]


def q(values, p):
    s=sorted(values)
    if not s: return None
    pos=(len(s)-1)*p
    lo=int(pos); hi=min(lo+1,len(s)-1); frac=pos-lo
    return s[lo]*(1-frac)+s[hi]*frac


def main(out_path: str = "benchmarks/scaling_results.csv"):
    rows=[]
    for n in SIZES:
        records=build_records(n)
        times=[]; peaks=[]
        for _ in range(REPEATS):
            tracemalloc.start()
            t0=time.perf_counter()
            validate_records(records)
            audit_record_hashes(records)
            audit_leakage(records)
            elapsed=(time.perf_counter()-t0)*1000
            _,peak=tracemalloc.get_traced_memory()
            tracemalloc.stop()
            times.append(elapsed); peaks.append(peak/1024/1024)
        rows.append({
            "n_records": n,
            "repeats": REPEATS,
            "median_ms": round(statistics.median(times),3),
            "iqr_ms": round(q(times,.75)-q(times,.25),3),
            "median_peak_mib": round(statistics.median(peaks),3),
            "iqr_peak_mib": round(q(peaks,.75)-q(peaks,.25),3),
        })
    p=Path(out_path); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    return rows

if __name__ == "__main__":
    print(main())
