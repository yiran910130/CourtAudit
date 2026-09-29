from courtaudit.calibration import audit_binary_predictions

def test_calibration_metrics():
    rows=[{"y_true":"1","y_pred":"1","confidence":"0.9"},{"y_true":"0","y_pred":"0","confidence":"0.8"}]
    r=audit_binary_predictions(rows,bins=5)
    assert r["accuracy"] == 1.0
    assert r["brier_score"] < 0.05
