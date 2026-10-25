import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

SRC = Path("data/raw/sources")
FILES = ["CEAS_08", "Enron", "Ling", "Nazario", "Nigerian_Fraud", "SpamAssassin"]

frames = []
for name in FILES:
    df = pd.read_csv(SRC / f"{name}.csv", encoding_errors="replace", on_bad_lines="skip")
    text = df["subject"].fillna("").astype(str) + " " + df["body"].fillna("").astype(str)
    out = pd.DataFrame({
        "text": text.str.slice(0, 5000),
        "label": pd.to_numeric(df["label"], errors="coerce"),
        "source": name,
    }).dropna(subset=["label"])
    out["label"] = out["label"].astype(int)
    out = out[out["text"].str.strip() != ""]
    frames.append(out)
    print(name, len(out), out["label"].value_counts().to_dict())

data = pd.concat(frames, ignore_index=True).drop_duplicates(subset="text")
print("Total after removing duplicates:", len(data), "\n")

rows = []
for held in FILES:
    train = data[data.source != held]
    test = data[data.source == held]
    model = make_pipeline(
        TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_features=100000, sublinear_tf=True),
        LogisticRegression(max_iter=1000, class_weight="balanced"),
    )
    model.fit(train["text"], train["label"])
    pred = pd.Series(model.predict(test["text"]), index=test.index)

    phish = test.label == 1
    legit = test.label == 0
    rows.append({
        "held_out": held,
        "messages": len(test),
        "phishing_share": round(test.label.mean(), 3),
        "accuracy": round((pred == test.label).mean(), 4),
        "phishing_caught": round((pred[phish] == 1).mean(), 4) if phish.any() else None,
        "legit_passed": round((pred[legit] == 0).mean(), 4) if legit.any() else None,
    })
    print("Finished", held)

results = pd.DataFrame(rows)
print("\n", results.to_string(index=False))
results.to_csv("models/cross_source_results.csv", index=False)