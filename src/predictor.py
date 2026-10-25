from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "phish_model.joblib"


@lru_cache(maxsize=1)
def _load():
    bundle = joblib.load(MODEL_PATH)
    return bundle["vectorizer"], bundle["classifier"]


def risk_level(p):
    if p >= 0.85:
        return "high"
    if p >= 0.5:
        return "medium"
    return "low"


def predict(text, threshold=0.5, top_k=8):
    vec, clf = _load()
    X = vec.transform([text])
    prob = float(clf.predict_proba(X)[0, 1])

    contrib = X.multiply(clf.coef_[0]).tocsr()
    idx, vals = contrib.indices, contrib.data
    names = vec.get_feature_names_out()
    order = np.argsort(vals)
    to_legit = [(names[idx[i]], float(vals[i])) for i in order[:top_k] if vals[i] < 0]
    to_phish = [(names[idx[i]], float(vals[i])) for i in order[::-1][:top_k] if vals[i] > 0]

    return {
        "label": "phishing" if prob >= threshold else "legitimate",
        "phishing_probability": round(prob, 4),
        "risk": risk_level(prob),
        "words_pointing_to_phishing": [{"word": w, "weight": round(v, 4)} for w, v in to_phish],
        "words_pointing_to_legitimate": [{"word": w, "weight": round(v, 4)} for w, v in to_legit],
    }
