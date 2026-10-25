import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW / "phishing_email.csv")
df = df.rename(columns={"text_combined": "text"})

df = df.dropna(subset=["text", "label"])
df["text"] = df["text"].astype(str)
df = df[df["text"].str.strip() != ""]
df["label"] = df["label"].astype(int)
df["channel"] = "email"
df["source"] = "kaggle_phishing_email"

df = df[["text", "channel", "label", "source"]]
df.to_parquet(OUT / "all.parquet", index=False)

print("Rows:", len(df))
print(df["label"].value_counts())
print("Exact duplicate texts:", df.duplicated(subset="text").sum())

print("\nCharacters per message by label:")
print(df.groupby("label")["text"].apply(lambda s: s.str.len().describe()))

print("\nShare of messages containing:")
checks = {
    "uppercase letters": r"[A-Z]",
    "http or www": r"http|www\.",
    "punctuation": r"[.,!?;:]",
}
for name, pattern in checks.items():
    print(f"  {name}: {df['text'].str.contains(pattern).mean():.1%}")