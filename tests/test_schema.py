from courtaudit.schema import validate_records

def test_valid_records():
    r = validate_records([{"record_id":"1","source_id":"s1","text":"x"}])
    assert r["valid"]

def test_missing_required():
    r = validate_records([{"record_id":"1","text":"x"}])
    assert not r["valid"]
