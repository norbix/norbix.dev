# app_flask.py
from flask import Flask, request, jsonify

app = Flask(__name__)

POS = {"good", "great", "excellent", "love", "happy", "awesome"}
NEG = {"bad", "terrible", "awful", "hate", "sad", "horrible"}

def score_sentiment(text: str) -> float:
    tokens = {t.strip(".,!?").lower() for t in text.split()}
    pos = len(tokens & POS)
    neg = len(tokens & NEG)
    if pos == 0 and neg == 0:
        return 0.0
    return (pos - neg) / (pos + neg)

def predict_label(text: str) -> str:
    s = score_sentiment(text)
    return "positive" if s > 0 else "negative" if s < 0 else "neutral"

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.post("/predict")
def predict():
    data = request.get_json(force=True) or {}
    text = data.get("text", "")
    return jsonify({"label": predict_label(text), "score": score_sentiment(text)})

@app.post("/predict-batch")
def predict_batch():
    data = request.get_json(force=True) or {}
    texts = data.get("texts", [])
    out = [{"text": t, "label": predict_label(t), "score": score_sentiment(t)} for t in texts]
    return jsonify(out)
