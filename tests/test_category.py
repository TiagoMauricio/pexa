import pytest

def get_token(client):
    resp = client.post("/api/auth/register", json={"email": "catuser@example.com", "password": "testpass123"})
    if resp.status_code not in (200, 400):
        assert False, resp.text
    resp = client.post("/api/auth/login", data={"username": "catuser@example.com", "password": "testpass123"})
    return resp.json()["access_token"]

def test_create_and_list_categories(client):
    token = get_token(client)
    # Create budget first
    resp = client.post("/api/budgets/", json={"name": "Budget for Cat"}, headers={"Authorization": f"Bearer {token}"})
    budget_id = resp.json()["id"]
    # Create category
    resp = client.post("/api/categories/", json={"name": "Food", "budget_id": budget_id}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200, resp.text
    cat = resp.json()
    assert cat["name"] == "Food"
    # List categories
    resp = client.get(f"/api/categories/?budget_id={budget_id}", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200, resp.text
    cats = resp.json()
    assert any(c["name"] == "Food" for c in cats)
