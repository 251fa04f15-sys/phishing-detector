# Phishing Detector

TF-IDF + logistic regression phishing classifier, evaluated leave-one-source-out.
Realistic accuracy on unseen sources: about 88% (random split: 98.8%, optimistic).

Live demo: (add your streamlit.app link here)

## Run locally
    pip install -r requirements.txt
    streamlit run src/dashboard.py
    uvicorn api:app --reload --app-dir src
    pytest

## Data
Kaggle "Phishing Email Dataset" (naserabdullahalam). Cite: Al-Subaiey et al., 2024, arXiv 2405.11619.
The raw data is not included in this repo. Download it from Kaggle and place the six source CSVs in data/raw/sources/.

## Limitations
Nazario-style phishing is missed about 4 times in 10. About 17% of unseen business mail is wrongly flagged.
Most sources label spam as phishing, and the data is mostly older.

## Interface
Animated neon theme with a cinematic title intro, built in Streamlit with CSS animations. Live app: https://poojith-phishing-detector-1.streamlit.app
