import pytest

def get_token(client):
    resp = client.post("/api/auth/register", json={"email": "transuser@example.com", "password": "testpass123"})
    if resp.status_code not in (200, 400):
        assert False, resp.text
    resp = client.post("/api/auth/login", data={"username": "transuser@example.com", "password": "testpass123"})
    return resp.json()["access_token"]

def test_create_and_list_transactions(client):
    token = get_token(client)
    # Create budget
    resp = client.post("/api/budgets/", json={"name": "Budget for Trans"}, headers={"Authorization": f"Bearer {token}"})
    budget_id = resp.json()["id"]
    # Create category
    resp = client.post("/api/categories/", json={"name": "Bills", "budget_id": budget_id}, headers={"Authorization": f"Bearer {token}"})
    cat_id = resp.json()["id"]
    # Create transaction
    resp = client.post("/api/transactions/", json={"amount": 42.5, "note": "Electricity", "category_id": cat_id}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200, resp.text
    txn = resp.json()
    assert txn["amount"] == 42.5
    assert txn["note"] == "Electricity"
    # List transactions
    resp = client.get(f"/api/transactions/?category_id={cat_id}", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200, resp.text
    txns = resp.json()
    assert any(t["amount"] == 42.5 for t in txns)
