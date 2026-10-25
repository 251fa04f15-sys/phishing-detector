import pandas as pd
import joblib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

D = Path("data/processed")
train = pd.read_parquet(D / "train.parquet")
val = pd.read_parquet(D / "val.parquet")   # the test set stays untouched for now

model = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_features=100000, sublinear_tf=True),
    LogisticRegression(max_iter=1000, class_weight="balanced"),
)
model.fit(train["text"], train["label"])

pred = model.predict(val["text"])
proba = model.predict_proba(val["text"])[:, 1]

print(classification_report(val["label"], pred, digits=4))
print("Confusion matrix (rows = true, cols = predicted):")
print(confusion_matrix(val["label"], pred))
print("ROC-AUC:", round(roc_auc_score(val["label"], proba), 4))

Path("models").mkdir(exist_ok=True)
joblib.dump(model, "models/baseline.joblib")

# What did the model learn? Strongest words for each class.
vec = model.named_steps["tfidfvectorizer"]
clf = model.named_steps["logisticregression"]
names = vec.get_feature_names_out()
order = clf.coef_[0].argsort()
print("\nTop words pushing toward PHISHING:", list(names[order[-25:]][::-1]))
print("Top words pushing toward LEGITIMATE:", list(names[order[:25]]))

# Error analysis: what does it get wrong?
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