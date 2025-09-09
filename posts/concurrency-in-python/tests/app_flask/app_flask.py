# app.py
from __future__ import annotations
from flask import Flask, request, jsonify, g
import os, time, threading

# --- "Model" (toy sentiment) ---
POS = {"good", "great", "excellent", "love", "happy", "awesome"}
NEG = {"bad", "terrible", "awful", "hate", "sad", "horrible"}

def load_model():
    # Here you would load a real model (e.g., torch.load / joblib.load)
    # Keep it fast for demo.
    time.sleep(0.05)  # simulate load
    return {"pos": POS, "neg": NEG}

def score_sentiment(model, text: str) -> float:
    tokens = {t.strip(".,!?").lower() for t in text.split()}
    pos = len(tokens & model["pos"])
    neg = len(tokens & model["neg"])
    if pos == 0 and neg == 0:
        return 0.0
    return (pos - neg) / (pos + neg)

def predict_label(score: float) -> str:
    return "positive" if score > 0 else "negative" if score < 0 else "neutral"

# --- App Factory (recommended for prod/gunicorn) ---
def create_app():
    app = Flask(__name__)
    app.config.update(
        MODEL=None,
        READY=False,
        NAME=os.environ.get("APP_NAME", "ai-service"),
    )

    # Load model at startup (main process). With gunicorn --preload this shares memory.
    app.config["MODEL"] = load_model()
    app.config["READY"] = True

    # Simple per-request timing
    @app.before_request
    def _start_timer():
        g.t0 = time.perf_counter()

    @app.after_request
    def _timing(resp):
        if hasattr(g, "t0"):
            resp.headers["X-Process-Time"] = f"{time.perf_counter() - g.t0:.3f}s"
        return resp

    # Health endpoints
    @app.get("/health")
    def health():
        return {"status": "ok", "service": app.config["NAME"]}

    @app.get("/ready")
    def ready():
        return ({"ready": True}, 200) if app.config["READY"] else ({"ready": False}, 503)

    # Inference: single
    @app.post("/predict")
    def predict():
        data = request.get_json(silent=True) or {}
        text = data.get("text", "")
        if not isinstance(text, str) or not text.strip():
            return jsonify(error="`text` (string) is required"), 400

        s = score_sentiment(app.config["MODEL"], text)
        return {"label": predict_label(s), "score": s}

    # Inference: batch
    @app.post("/predict-batch")
    def predict_batch():
        data = request.get_json(silent=True) or {}
        texts = data.get("texts", [])
        if not isinstance(texts, list) or any(not isinstance(t, str) for t in texts):
            return jsonify(error="`texts` must be a list[str]"), 400

        out = []
        for t in texts:
            s = score_sentiment(app.config["MODEL"], t)
            out.append({"text": t, "label": predict_label(s), "score": s})
        return out

    # Basic error handler (clean JSON)
    @app.errorhandler(Exception)
    def on_error(err):
        return jsonify(error=type(err).__name__, message=str(err)), 500

    return app

# Dev entrypoint: `python app.py`
if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
