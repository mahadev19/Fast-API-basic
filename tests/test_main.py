from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.main import app
client = TestClient(app)


def test_create_user():
    response = client.post("/users", json={
        "name": "Mahadev",
        "email": "test@gmail.com"
    })

    assert response.status_code == 200
    assert "name" in response.json()


def test_error():
    response = client.get("/wrong-url")
    assert response.status_code == 404


def test_login():
    # Step 1: Create user first
    client.post("/users", json={
        "name": "admin",
        "email": "admin@gmail.com"
    })

    # Step 2: Login
    response = client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin"
        }
    )

    print(response.json())  # DEBUG

    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None

def test_protected():
    # Create user first
    client.post("/users", json={
        "name": "admin",
        "email": "admin@gmail.com"
    })

    login = client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin"
        }
    )

    print(login.json())  # DEBUG

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200