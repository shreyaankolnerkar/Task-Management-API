from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.main import app

client = TestClient(app)


def test_register_user():
    res = client.post("/users/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "123456"
    })
    assert res.status_code in [200, 400]


def test_login_user():
    res = client.post("/users/login", json={
        "email": "test@example.com",
        "password": "123456"
    })
    assert res.status_code in [200, 401]


def test_create_task_unauthorized():
    res = client.post("/tasks/", params={
        "title": "Task1",
        "team_id": 1
    })
    assert res.status_code in [401, 403]


def test_update_task_not_found():
    res = client.put("/tasks/999", params={"title": "Updated"})
    assert res.status_code in [401, 403, 404]


def test_assign_task_not_found():
    res = client.put("/tasks/999/assign", params={"assigned_to": 1})
    assert res.status_code in [401, 403, 404]


def test_delete_task_not_found():
    res = client.delete("/tasks/999")
    assert res.status_code in [401, 403, 404]