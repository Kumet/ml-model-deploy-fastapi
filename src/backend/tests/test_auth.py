def test_token_success(client):
    response = client.post("/auth/token", json={"username": "admin", "password": "changeme"})
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_token_invalid_credentials(client):
    response = client.post("/auth/token", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401
