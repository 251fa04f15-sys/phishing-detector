import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

OUT = Path("data/processed")
df = pd.read_parquet(OUT / "all.parquet")
start = len(df)

# 1. Cut very long messages (keeps training fast; the start of an email holds most signal)
df["text"] = df["text"].str.slice(0, 10000)

# 2. Drop very short messages that carry almost no signal
df = df[df["text"].str.len() >= 20]

# 3. Remove exact duplicates
df = df.drop_duplicates(subset="text")

# 4. Remove texts that appear with BOTH labels (contradictory)
label_counts = df.groupby("text")["label"].nunique()
conflicting = label_counts[label_counts > 1].index
print("Conflicting-label texts removed:", len(conflicting))
df = df[~df["text"].isin(conflicting)]

print(f"Rows: {start} -> {len(df)}")

# 5. Shuffle and split 70 / 15 / 15, keeping the class ratio the same in each part
train, temp = train_test_split(df, test_size=0.30, stratify=df["label"], random_state=42)
val, test = train_test_split(temp, test_size=0.50, stratify=temp["label"], random_state=42)

for name, part in [("train", train), ("val", val), ("test", test)]:
    part.to_parquet(OUT / f"{name}.parquet", index=False)
    print(f"{name}: {len(part)} rows, phishing share {part['label'].mean():.1%}")

# 6. Shortcut check: how many messages in each class contain a link word?
print("\nShare containing http/www, by label (train set):")
has_link = train["text"].str.contains(r"http|www")
print(has_link.groupby(train["label"]).mean().map("{:.1%}".format))