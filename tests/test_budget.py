import pytest

def get_token(client):
    resp = client.post("/api/auth/register", json={"email": "budgetuser@example.com", "password": "testpass123"})
    if resp.status_code not in (200, 400):
        assert False, resp.text
    resp = client.post("/api/auth/login", data={"username": "budgetuser@example.com", "password": "testpass123"})
    return resp.json()["access_token"]

def test_create_and_list_budgets(client):
    token = get_token(client)
    # Create budget
    resp = client.post("/api/budgets/", json={"name": "My Budget"}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200, resp.text
    budget = resp.json()
    assert budget["name"] == "My Budget"
    # List budgets
    resp = client.get("/api/budgets/", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200, resp.text
    budgets = resp.json()
    assert any(b["name"] == "My Budget" for b in budgets)
