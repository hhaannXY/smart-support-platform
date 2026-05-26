import pytest
from fastapi.testclient import TestClient
from backend.app.main import app


@pytest.fixture()
def client():
    return TestClient(app)


def test_health(client):
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json().get('status') == 'ok'


def test_create_ticket(client):
    # register user
    reg = client.post('/auth/register', json={"username": "tester", "password": "secret"})
    assert reg.status_code == 200
    # obtain token
    token_resp = client.post('/auth/token', data={"username": "tester", "password": "secret"})
    assert token_resp.status_code == 200
    token = token_resp.json().get('access_token')
    assert token
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"text": "I have a payment issue"}
    r = client.post('/tickets', json=payload, headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert 'id' in data
    assert 'category' in data
