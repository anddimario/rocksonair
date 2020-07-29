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


def test_put_batch_main():
    payload = [{"key": "test", "value": 1111, "type": "put"}, {"key": "test1", "value": 2222, "type": "put"}, {
        "key": "test2", "value": 2222, "type": "put"}, {"key": "test1", "value": "false", "type": "delete"}]
    headers = {'X-API-Key': api_key}
    response = client.post("/storage/batch", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"detail": "success"}


def test_get_batch_main():
    headers = {'X-API-Key': api_key}
    response = client.get(
        "/storage/batch?keys=test,test1,test2,test3", headers=headers)
    assert response.status_code == 200
    assert response.json()["detail"] == "success"


def test_keys_main():
    headers = {'X-API-Key': api_key}
    response = client.get("/storage/keys?order=last", headers=headers)
    assert response.status_code == 200
    assert response.json()["detail"] == "success"


def test_iterate_prefix_main():
    headers = {'X-API-Key': api_key}
    response = client.get("/storage/iterate/test", headers=headers)
    assert response.status_code == 200
    assert response.json()["detail"] == "success"
