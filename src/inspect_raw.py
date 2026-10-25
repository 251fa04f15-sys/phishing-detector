import sys
import pandas as pd

df = pd.read_csv(sys.argv[1])
print("Shape:", df.shape)
print("\nColumns:", list(df.columns))
print("\nMissing values:\n", df.isna().sum())
print("\nLabel counts:\n", df["label"].value_counts())
print("\nFirst rows:")
for i in range(3):
    print(f"\n[{df['label'].iloc[i]}]", str(df.iloc[i, 0])[:300])