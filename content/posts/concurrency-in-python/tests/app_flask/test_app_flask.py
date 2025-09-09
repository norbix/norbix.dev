from app_flask import create_app

def test_predict_single():
    app = create_app()
    client = app.test_client()

    r = client.post("/predict", json={"text": "awesome and excellent"})
    assert r.status_code == 200
    data = r.get_json()
    assert data["label"] == "positive"
    assert -1.0 <= data["score"] <= 1.0

def test_predict_batch_validation():
    app = create_app()
    client = app.test_client()

    r = client.post("/predict-batch", json={"texts": ["bad", "great", "meh"]})
    assert r.status_code == 200
    out = r.get_json()
    assert len(out) == 3
