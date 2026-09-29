from courtaudit.agent import audit_agent_outputs

def test_agent_policy_flag():
    rows=[{"request_id":"r1","response_text":"x","completion_status":"complete","direct_model_inference":True,"web_search_used":True,"external_sources_used":False}]
    r=audit_agent_outputs(rows)
    assert not r["pass"]
    assert r["issues"][0]["code"] == "WEB_SEARCH_USED"
