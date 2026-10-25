import pandas as pd
import joblib
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

D = Path("data/processed")
val = pd.read_parquet(D / "val.parquet")   # the test set stays untouched
model = joblib.load("models/baseline.joblib")

pred = model.predict(val["text"])
proba = model.predict_proba(val["text"])[:, 1]

print(classification_report(val["label"], pred, digits=4))
print("Confusion matrix (rows = true, cols = predicted):")
print(confusion_matrix(val["label"], pred))
print("ROC-AUC:", round(roc_auc_score(val["label"], proba), 4))

vec = model.named_steps["tfidfvectorizer"]
clf = model.named_steps["logisticregression"]
names = vec.get_feature_names_out()
order = clf.coef_[0].argsort()
print("\nTop words pushing toward PHISHING:", list(names[order[-25:]][::-1]))
print("Top words pushing toward LEGITIMATE:", list(names[order[:25]]))

val = val.assign(pred=pred)
fp = val[(val.label == 0) & (val.pred == 1)]
fn = val[(val.label == 1) & (val.pred == 0)]
print(f"\nFalse positives: {len(fp)}   False negatives: {len(fn)}")
print("\n--- Legitimate messages flagged as phishing ---")
for t in fp["text"].head(8):
    print("-", t[:200])
print("\n--- Phishing messages it missed ---")
for t in fn["text"].head(8):
    print("-", t[:200])