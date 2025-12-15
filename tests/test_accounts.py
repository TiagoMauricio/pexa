import pytest
from fastapi.testclient import TestClient

@pytest.fixture()

def test_create_account(client: TestClient):
    """Test successful creation"""
    pass

def test_create_account_error(client: TestClient):
    """Test error on account creation"""
    pass


def test_duplicate_account_name(client: TestClient):
    """Test duplicate account name"""
    pass


def test_update_account_name(client: TestClient):
    """Test update account"""
    pass


def test_get_user_accounts(client: TestClient):
    """Get list of user account"""
    pass


def test_get_phorbiden_account(client: TestClient, token):
    """Attempt access of an account that the user is not an owner of"""
    print("WHAT:", token)
    headers={
            "Authorization": f"Bearer {token}"
        }
    response = client.get("/api/accounts/1123123", headers=headers)

    assert response.status_code == 403
