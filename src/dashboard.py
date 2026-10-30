import json
from pathlib import Path

import pandas as pd
import streamlit as st
from emailfile import read_email_file
from predictor import MODEL_PATH, predict

ROOT = Path(__file__).resolve().parent.parent

st.set_page_config(page_title="Phishing Detector", layout="wide")

from intro import show_intro
from theme import apply_theme

apply_theme()
show_intro()
st.title("Phishing Detector")
st.caption("TF-IDF + logistic regression, tested on sources it never saw during training.")

tab_check, tab_results, tab_limits = st.tabs(["Check a message", "Evaluation results", "Limitations"])

with tab_check:
    examples = {
        "(write your own)": "",
        "Account scare": "URGENT: Your bank account will be suspended unless you verify immediately.",
        "Normal work mail": "Hi team, attached is the agenda for Thursday."
    }

    choice = st.selectbox("Load an example", list(examples))
    uploaded = st.file_uploader("Or upload an email file (.txt or .eml)", type=["txt", "eml"])

    file_text = read_email_file(uploaded.getvalue(), uploaded.name) if uploaded else ""

    text = st.text_area("Paste an email or SMS", value=file_text)

    threshold = st.slider("Phishing threshold", 0.05, 0.95, 0.5, 0.05)
    go = st.button("Analyse", type="primary") and bool(text.strip())
    if go and len(text.split()) < 8:
           st.warning("Not enough text to give a reliable verdict. Paste at least 8 words.")
    elif go:
        r = predict(text, threshold)
        c1, c2, c3 = st.columns(3)
        c1.metric("Verdict", r["label"].upper())
        c2.metric("Phishing probability", f"{r['phishing_probability']:.0%}")
        c3.metric("Risk", r["risk"].upper())
        st.progress(r["phishing_probability"])
        left, right = st.columns(2)
        left.subheader("Pushed toward phishing")
        left.dataframe(pd.DataFrame(r["words_pointing_to_phishing"]), hide_index=True)
        right.subheader("Pushed toward legitimate")
        right.dataframe(pd.DataFrame(r["words_pointing_to_legitimate"]), hide_index=True)
        st.info("This is a screening aid, not a verdict. Check the sender and links yourself.")

with tab_results:
    info_path = ROOT / "models" / "model_info.json"
    if info_path.exists():
        info = json.loads(info_path.read_text())
        a, b, c = st.columns(3)
        a.metric("Random-split accuracy (optimistic)", f"{info['random_split_accuracy']:.1%}")
        b.metric("Unseen-source accuracy (realistic)", f"{info['cross_source_accuracy_avg']:.1%}")
        c.metric("Training messages", f"{info['n_messages']:,}")
    cmp_path = ROOT / "models" / "feature_comparison.csv"
    if cmp_path.exists():
        res = pd.read_csv(cmp_path)
        metric = st.selectbox("Metric", ["accuracy", "phishing_caught", "legit_passed"])
        table = res.pivot(index="held_out", columns="model", values=metric).round(3)
        st.dataframe(table)
        st.bar_chart(table)

with tab_limits:
    st.markdown("""
- Realistic accuracy is about 88%, not the 98.8% a random split shows.
- Nazario-style phishing (fake bank and account emails) is the weakest case.
- On unseen business mail, about 17% was wrongly flagged.
- Most sources label spam as phishing, so the model partly learned spam versus normal mail.
- The data is mostly older. Modern phishing wording is not covered.
- Hand-built style features were tested and did not help.
- Very short messages (under 8 words) are not judged. The model was trained on full emails.
""")
    
