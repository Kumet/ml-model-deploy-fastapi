def test_model_info(client):
    response = client.get("/model/info")
    assert response.status_code == 200
    meta = response.json()
    assert meta["name"]
    assert meta["version"]
    assert meta["path"].endswith("model.joblib")


def test_predict(client):
    payload = {"features": [5.1, 3.5, 1.4, 0.2]}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["label"], int)
    assert 0 <= body["proba"] <= 1
