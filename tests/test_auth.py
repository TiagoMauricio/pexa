import pytest

def test_register_and_login(client):
    # Register
    resp = client.post("/api/auth/register", json={"email": "test@example.com", "password": "testpass123"})
    assert resp.status_code == 200, resp.text
    user = resp.json()
    assert user["email"] == "test@example.com"
    # Login
    resp = client.post("/api/auth/login", data={"username": "test@example.com", "password": "testpass123"})
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["access_token"]
    assert "refresh_token" in data

def test_refresh_token(client):
    # Use a unique email for isolation
    import uuid
    refresh_email = f"refresh_{uuid.uuid4()}@example.com"
    password = "refreshpass"
    # Register and login
    resp = client.post("/api/auth/register", json={"email": refresh_email, "password": password})
    assert resp.status_code == 200, resp.text
    resp = client.post("/api/auth/login", data={"username": refresh_email, "password": password})
    tokens = resp.json()
    refresh_token = tokens["refresh_token"]
    # Use refresh endpoint
    resp = client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_me(client):
    # Register and login
    resp = client.post("/api/auth/register", json={"email": "me@example.com", "password": "pass123"})
    assert resp.status_code == 200, resp.text
    resp = client.post("/api/auth/login", data={"username": "me@example.com", "password": "pass123"})
    token = resp.json()["access_token"]
    # Get current user
    resp = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200, resp.text
    user = resp.json()
    assert user["email"] == "me@example.com"
