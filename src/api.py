import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from predictor import MODEL_PATH, predict

app = FastAPI(title="Phishing Detector", version="1.0")
INFO_PATH = Path(MODEL_PATH).parent / "model_info.json"


class Message(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)
    threshold: float = Field(0.5, ge=0.05, le=0.95)


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": Path(MODEL_PATH).exists()}


@app.get("/model-info")
def model_info():
    if not INFO_PATH.exists():
        raise HTTPException(404, "Run train_final.py first.")
    return json.loads(INFO_PATH.read_text())


@app.post("/predict")
def predict_one(msg: Message):
    return predict(msg.text, msg.threshold)
