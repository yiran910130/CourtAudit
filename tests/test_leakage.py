from courtaudit.leakage import audit_leakage

def test_cross_split_duplicate_detected():
    rows=[{"record_id":"1","source_id":"a","text":"Hello, world!","split":"train"},{"record_id":"2","source_id":"b","text":"hello world","split":"test"}]
    assert audit_leakage(rows)["n_cross_split_text_duplicates"] == 1

def test_clean_split_passes():
    rows=[{"record_id":"1","source_id":"a","text":"alpha","split":"train"},{"record_id":"2","source_id":"b","text":"beta","split":"test"}]
    assert audit_leakage(rows)["pass"]
