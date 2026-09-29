from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from .agent import audit_agent_outputs
from .calibration import audit_binary_predictions
from .io import read_csv, read_jsonl, write_json
from .leakage import audit_leakage
from .provenance import audit_record_hashes, sha256_file
from .reliability import audit_annotations
from .schema import validate_records


def build_report(records_path: str, annotations_path: str | None = None, predictions_path: str | None = None, agent_path: str | None = None, deterministic: bool = False) -> dict[str, Any]:
    records = read_jsonl(records_path)
    result: dict[str, Any] = {
        "tool": "CourtAudit",
        "version": "0.1.0",
        "generated_at_utc": None if deterministic else datetime.now(timezone.utc).isoformat(),
        "inputs": {"records": {"path": str(records_path), "sha256": sha256_file(records_path)}},
        "schema": validate_records(records),
        "provenance": audit_record_hashes(records),
        "leakage": audit_leakage(records),
    }
    if annotations_path:
        result["inputs"]["annotations"] = {"path": str(annotations_path), "sha256": sha256_file(annotations_path)}
        result["reliability"] = audit_annotations(read_csv(annotations_path))
    if predictions_path:
        result["inputs"]["predictions"] = {"path": str(predictions_path), "sha256": sha256_file(predictions_path)}
        result["calibration"] = audit_binary_predictions(read_csv(predictions_path))
    if agent_path:
        result["inputs"]["agent_outputs"] = {"path": str(agent_path), "sha256": sha256_file(agent_path)}
        result["agent_outputs"] = audit_agent_outputs(read_jsonl(agent_path))
    result["overall_pass"] = bool(result["schema"].get("valid") and result["leakage"].get("pass") and result.get("agent_outputs", {"pass": True}).get("pass"))
    return result


def report_markdown(report: dict[str, Any]) -> str:
    def status(v: bool) -> str:
        return "PASS" if v else "FLAG"
    lines = [
        "# CourtAudit report",
        "",
        f"Version: {report['version']}",
        f"Generated: {report['generated_at_utc']}",
        "",
        "## Gate summary",
        "",
        "| Gate | Status | Detail |",
        "|---|---|---|",
        f"| Schema | {status(report['schema']['valid'])} | {report['schema']['n_errors']} error(s) |",
        f"| Split leakage | {status(report['leakage']['pass'])} | {report['leakage']['n_cross_split_text_duplicates']} text duplicate(s); {report['leakage']['n_cross_split_groups']} group overlap(s) |",
    ]
    if "agent_outputs" in report:
        lines.append(f"| Agent outputs | {status(report['agent_outputs']['pass'])} | {report['agent_outputs']['n_issues']} issue(s) |")
    lines.extend(["", "## Metrics", ""])
    if "reliability" in report:
        r = report["reliability"]
        lines += [f"- Krippendorff alpha (nominal): {r['krippendorff_alpha_nominal']:.4f}" if r['krippendorff_alpha_nominal'] is not None else "- Krippendorff alpha: n/a",
                  f"- Cohen kappa (two coders): {r['cohens_kappa_two_coders']:.4f}" if r['cohens_kappa_two_coders'] is not None else "- Cohen kappa: n/a"]
    if "calibration" in report:
        c = report["calibration"]
        if c.get("n", 0):
            lines += [f"- Accuracy: {c['accuracy']:.4f}", f"- Brier score: {c['brier_score']:.4f}", f"- Expected calibration error: {c['ece']:.4f}"]
    lines += ["", f"Overall gate status: **{status(report['overall_pass'])}**", ""]
    return "\n".join(lines)


def write_report(report: dict[str, Any], out_json: str, out_md: str | None = None) -> None:
    write_json(out_json, report)
    if out_md:
        Path(out_md).write_text(report_markdown(report), encoding="utf-8")
