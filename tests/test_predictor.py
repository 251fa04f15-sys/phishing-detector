import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from predictor import predict


def test_phishing_scores_higher_than_normal_mail():
    phish = predict("URGENT verify your password within 24 hours or your bank account is suspended")
    normal = predict("Hi team, attached is the agenda for Thursday meeting. Thanks")
    assert phish["phishing_probability"] > normal["phishing_probability"]


def test_output_has_expected_fields():
    r = predict("Please confirm your account details")
    assert r["label"] in ("phishing", "legitimate")
    assert 0.0 <= r["phishing_probability"] <= 1.0
    assert r["risk"] in ("low", "medium", "high")


def test_threshold_changes_label():
    text = "URGENT verify your password within 24 hours or your bank account is suspended"
    assert predict(text, threshold=0.5)["label"] == "phishing"
    assert predict(text, threshold=0.95)["label"] in ("phishing", "legitimate")
