import pandas as pd

r = pd.read_csv("models/feature_comparison.csv")
for m in ["accuracy", "phishing_caught", "legit_passed"]:
    print(f"\n=== {m} ===")
    print(r.pivot(index="held_out", columns="model", values=m).round(3).to_string())
print("\n=== average accuracy ===")
print(r.groupby("model")["accuracy"].mean().round(4).to_string())
