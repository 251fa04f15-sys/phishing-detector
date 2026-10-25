import re
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.sparse import hstack, csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import StandardScaler

SRC = Path("data/raw/sources")
FILES = ["CEAS_08", "Enron", "Ling", "Nazario", "Nigerian_Fraud", "SpamAssassin"]

URGENT = r"urgent|immediately|asap|suspend|expire|final notice|act now|limited time|deadline|within 24"
CREDENTIAL = r"password|verify|login|log in|account|bank|confirm|security|credit card|paypal|update your"
MONEY = r"[$£€]|million|dollars|winner|lottery|inheritance|transfer"

# ---- load all six sources, keeping the original case and punctuation ----
frames = []
for name in FILES:
    df = pd.read_csv(SRC / f"{name}.csv", encoding_errors="replace", on_bad_lines="skip")
    out = pd.DataFrame({
        "subject": df["subject"].fillna("").astype(str).str.slice(0, 300),
        "body": df["body"].fillna("").astype(str).str.slice(0, 5000),
        "label": pd.to_numeric(df["label"], errors="coerce"),
        "source": name,
    }).dropna(subset=["label"])
    out["label"] = out["label"].astype(int)
    frames.append(out)

data = pd.concat(frames, ignore_index=True)
data["text"] = data["subject"] + " " + data["body"]
data = data[data["text"].str.strip() != ""].drop_duplicates(subset="text").reset_index(drop=True)
print("Messages:", len(data))

# ---- style features that exist for every source ----
def style_features(d):
    text, subj = d["text"], d["subject"]
    n = text.str.len().clip(lower=1)
    letters = text.str.count(r"[A-Za-z]").clip(lower=1)
    f = pd.DataFrame(index=d.index)
    f["log_len"] = np.log1p(n)
    f["upper_ratio"] = text.str.count(r"[A-Z]") / letters
    f["digit_ratio"] = text.str.count(r"\d") / n
    f["exclaim"] = np.log1p(text.str.count("!"))
    f["n_urls"] = np.log1p(text.str.count(r"https?://|www\."))
    f["ip_urls"] = np.log1p(text.str.count(r"https?://\d{1,3}(?:\.\d{1,3}){3}"))
    f["html_tags"] = np.log1p(text.str.count(r"<[a-zA-Z/]"))
    f["urgent"] = np.log1p(text.str.count(URGENT, flags=re.I))
    f["credential"] = np.log1p(text.str.count(CREDENTIAL, flags=re.I))
    f["money"] = np.log1p(text.str.count(MONEY, flags=re.I))
    f["subj_len"] = np.log1p(subj.str.len())
    f["subj_upper"] = subj.str.count(r"[A-Z]") / subj.str.count(r"[A-Za-z]").clip(lower=1)
    f["subj_exclaim"] = subj.str.count("!")
    f["at_signs"] = np.log1p(text.str.count("@"))
    return f

style = style_features(data)

def score(pred, y):
    pred, y = np.asarray(pred), np.asarray(y)
    phish, legit = y == 1, y == 0
    return {
        "accuracy": (pred == y).mean(),
        "phishing_caught": (pred[phish] == 1).mean() if phish.any() else np.nan,
        "legit_passed": (pred[legit] == 0).mean() if legit.any() else np.nan,
    }

rows = []
for held in FILES:
    tr = data.source != held
    te = ~tr
    y_tr, y_te = data.loc[tr, "label"], data.loc[te, "label"]

    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_features=100000, sublinear_tf=True)
    T_tr = vec.fit_transform(data.loc[tr, "text"])
    T_te = vec.transform(data.loc[te, "text"])

    sc = StandardScaler().fit(style[tr])
    S_tr = np.clip(sc.transform(style[tr]), -5, 5)
    S_te = np.clip(sc.transform(style[te]), -5, 5)

    preds = {}
    preds["A_words_only"] = LogisticRegression(max_iter=1000, class_weight="balanced") \
        .fit(T_tr, y_tr).predict(T_te)
    preds["B_words_plus_style"] = LogisticRegression(max_iter=1000, class_weight="balanced") \
        .fit(hstack([T_tr, csr_matrix(S_tr)]).tocsr(), y_tr) \
        .predict(hstack([T_te, csr_matrix(S_te)]).tocsr())
    preds["C_style_only"] = HistGradientBoostingClassifier(class_weight="balanced", random_state=42) \
        .fit(S_tr, y_tr).predict(S_te)

    for model_name, p in preds.items():
        rows.append({"held_out": held, "model": model_name, **score(p, y_te)})
    print("Finished", held)

res = pd.DataFrame(rows)
res.to_csv("models/feature_comparison.csv", index=False)

for metric in ["accuracy", "phishing_caught", "legit_passed"]:
    print(f"\n=== {metric} ===")
    print(res.pivot(index="held_out", columns="model", values=metric).round(4).to_string())
print("\n=== average accuracy ===")
print(res.groupby("model")["accuracy"].mean().round(4).to_string())
