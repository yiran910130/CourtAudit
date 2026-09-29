from pathlib import Path
from courtaudit.report import build_report

def test_deterministic_report_is_equal():
    base=Path(__file__).parents[1]/"demo_data"
    a=build_report(str(base/"records_clean.jsonl"), deterministic=True)
    b=build_report(str(base/"records_clean.jsonl"), deterministic=True)
    assert a == b
