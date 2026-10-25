import pandas as pd
from pathlib import Path

SRC = Path("data/raw/sources")
FILES = ["CEAS_08", "Enron", "Ling", "Nazario", "Nigerian_Fraud", "SpamAssassin"]
frames = []
for n in FILES:
    d = pd.read_csv(SRC / f"{n}.csv", encoding_errors="replace", on_bad_lines="skip")
    d["source"] = n
    frames.append(d[["subject", "body", "label", "source"]])
a = pd.concat(frames, ignore_index=True)
a["text"] = a["subject"].fillna("").astype(str) + " " + a["body"].fillna("").astype(str)
print("Rows before cleaning:", len(a))
print("Duplicate texts:", a.duplicated(subset="text").sum())
print(a.groupby("source")["label"].agg(["count", "mean"]).round(3))
print("Label counts:")
print(a["label"].value_counts())
