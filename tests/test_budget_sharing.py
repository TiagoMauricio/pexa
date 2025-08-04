import pytest

USER1 = {"email": "owner@example.com", "password": "testpass123"}
USER2 = {"email": "shared@example.com", "password": "testpass123"}
USER3 = {"email": "readonly@example.com", "password": "testpass123"}


@pytest.fixture
def user_tokens(client):
    # Register and login 3 users
    tokens = {}
    for user in [USER1, USER2, USER3]:
        client.post("/api/auth/register", json=user)
        resp = client.post(
            "/api/auth/login",
            data={"username": user["email"], "password": user["password"]},
        )
        tokens[user["email"]] = resp.json()["access_token"]
    yield tokens
    # Teardown: delete users after test (cascade deletes budgets, shares, cats, txns)
    for user in [USER1, USER2, USER3]:
        client.delete(f"/api/users/{user['email']}")


def test_budget_sharing_permissions(client, user_tokens):
    owner_token = user_tokens[USER1["email"]]
    shared_token = user_tokens[USER2["email"]]
    readonly_token = user_tokens[USER3["email"]]

    # Owner creates budget
    resp = client.post(
        "/api/budgets/",
        json={"name": "Shared Budget"},
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    assert resp.status_code == 200, resp.text
    budget_id = resp.json()["id"]

    # Owner shares with USER2 (write) and USER3 (read only)
    resp = client.post(
        "/api/budgets/share",
        params={"budget_id": budget_id, "user_id": 2, "can_write": True},
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    assert resp.status_code == 200, resp.text
    resp = client.post(
        "/api/budgets/share",
        params={"budget_id": budget_id, "user_id": 3, "can_write": False},
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    assert resp.status_code == 200, resp.text

    # Owner, USER2 (write), USER3 (read) list budgets
    for token in [owner_token, shared_token, readonly_token]:
        resp = client.get("/api/budgets/", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200, resp.text
        names = [b["name"] for b in resp.json()]
        assert "Shared Budget" in names

    # Owner can add category
    resp = client.post(
        "/api/categories/",
        json={"name": "OwnerCat", "budget_id": budget_id},
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    assert resp.status_code == 200, resp.text
    owner_cat_id = resp.json()["id"]

    # USER2 (write) can add category
    resp = client.post(
        "/api/categories/",
        json={"name": "SharedCat", "budget_id": budget_id},
        headers={"Authorization": f"Bearer {shared_token}"},
    )
    assert resp.status_code == 200, resp.text
    shared_cat_id = resp.json()["id"]

    # USER3 (read only) cannot add category
    resp = client.post(
        "/api/categories/",
        json={"name": "ReadCat", "budget_id": budget_id},
        headers={"Authorization": f"Bearer {readonly_token}"},
    )
    assert resp.status_code == 403

    # Owner can add transaction to own category
    txn = {"amount": 10, "note": "OwnerTxn", "category_id": owner_cat_id}
    resp = client.post(
        "/api/transactions/",
        json=txn,
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    assert resp.status_code == 200, resp.text

    # USER2 (write) can add transaction to shared category
    txn = {"amount": 20, "note": "SharedTxn", "category_id": shared_cat_id}
    resp = client.post(
        "/api/transactions/",
        json=txn,
        headers={"Authorization": f"Bearer {shared_token}"},
    )
    assert resp.status_code == 200, resp.text

    # USER3 (read only) cannot add transaction
    txn = {"amount": 30, "note": "ReadTxn", "category_id": owner_cat_id}
    resp = client.post(
        "/api/transactions/",
        json=txn,
        headers={"Authorization": f"Bearer {readonly_token}"},
    )
    assert resp.status_code == 403
