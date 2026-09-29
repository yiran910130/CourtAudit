from __future__ import annotations
import argparse, json, sys
from .agent import audit_agent_outputs
from .calibration import audit_binary_predictions
from .io import read_csv, read_jsonl
from .leakage import audit_leakage
from .provenance import audit_record_hashes
from .reliability import audit_annotations
from .report import build_report, write_report
from .schema import validate_records


def emit(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True))


def main(argv=None):
    p = argparse.ArgumentParser(prog="courtaudit", description="Audit institutional-language NLP datasets and model outputs.")
    p.add_argument("--version", action="version", version="courtaudit 0.1.0")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("validate", "provenance", "leakage"):
        s = sub.add_parser(name); s.add_argument("records")
    s = sub.add_parser("reliability"); s.add_argument("annotations")
    s = sub.add_parser("calibration"); s.add_argument("predictions"); s.add_argument("--bins", type=int, default=10)
    s = sub.add_parser("agent-audit"); s.add_argument("outputs")
    s = sub.add_parser("report")
    s.add_argument("records"); s.add_argument("--annotations"); s.add_argument("--predictions"); s.add_argument("--agent-outputs")
    s.add_argument("--out-json", default="courtaudit_report.json"); s.add_argument("--out-md", default="courtaudit_report.md"); s.add_argument("--deterministic", action="store_true")
    args = p.parse_args(argv)
    if args.cmd == "validate": emit(validate_records(read_jsonl(args.records)))
    elif args.cmd == "provenance": emit(audit_record_hashes(read_jsonl(args.records)))
    elif args.cmd == "leakage": emit(audit_leakage(read_jsonl(args.records)))
    elif args.cmd == "reliability": emit(audit_annotations(read_csv(args.annotations)))
    elif args.cmd == "calibration": emit(audit_binary_predictions(read_csv(args.predictions), bins=args.bins))
    elif args.cmd == "agent-audit": emit(audit_agent_outputs(read_jsonl(args.outputs)))
    elif args.cmd == "report":
        report = build_report(args.records, args.annotations, args.predictions, args.agent_outputs, deterministic=args.deterministic)
        write_report(report, args.out_json, args.out_md)
        emit({"out_json": args.out_json, "out_md": args.out_md, "overall_pass": report["overall_pass"]})
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
