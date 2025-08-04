import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models.user import User

TEST_EMAILS = [
    "test@example.com",
    "me@example.com",
    "budgetuser@example.com",
    "catuser@example.com",
    "transuser@example.com",
]

@pytest.fixture(scope="function", autouse=True)
def cleanup_users():
    db = SessionLocal()
    try:
        for email in TEST_EMAILS:
            db.query(User).filter(User.email == email).delete()
        db.commit()
    finally:
        db.close()

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
