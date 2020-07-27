from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

api_key = 'testkpi'

def test_put_main():
    payload = {"key": "test", "value": "prova"}
    headers = {'X-API-Key': api_key}
    response = client.post("/storage/single", json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"detail": "success"}


def test_get_main():
    headers = {'X-API-Key': api_key}
    response = client.get("/storage/single/test", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"key": "test", "value": "prova"}


def test_delete_main():
    headers = {'X-API-Key': api_key}
    response = client.delete("/storage/single/test", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"detail": "success"}
