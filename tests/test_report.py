from pathlib import Path
from courtaudit.report import build_report

def test_demo_report_builds():
    base=Path(__file__).parents[1]/"demo_data"
    r=build_report(str(base/"records_clean.jsonl"), str(base/"annotations.csv"), str(base/"predictions.csv"), str(base/"agent_outputs_clean.jsonl"))
    assert r["schema"]["valid"]
    assert r["leakage"]["pass"]
    assert r["agent_outputs"]["pass"]
