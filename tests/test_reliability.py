from courtaudit.reliability import cohens_kappa, krippendorff_alpha_nominal

def test_kappa_perfect():
    assert cohens_kappa([("A","A"),("B","B")]) == 1.0

def test_alpha_perfect():
    assert krippendorff_alpha_nominal({"1":["A","A"],"2":["B","B"]}) == 1.0
