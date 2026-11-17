from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_bad_login_credentials():
    response = client.post(
        "/login",
        json={
            "email": "invalid_email@example.com",
            "password": "invalid_password"
        }
    )
    
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid email or password"}


def test_missing_credentials():
    response = client.post("/login")
    
    assert response.status_code == 422


def test_missing_password():
    response = client.post(
        "/login",
        json={
            "email": "invalid_email2@example.com"
        }
    )

    assert response.status_code == 422


def test_missing_email():
    response = client.post(
        "/login",
        json={
            "password": "invalid_password2"
        }
    )

    assert response.status_code == 422


def test_invalid_email_format():
    response = client.post(
        "/login",
        json={
            "email": "hello@example@example_.com",
            "password": "bypass?"
        }
    )

    assert response.status_code == 422

    
def test_login_returns_access_token():
    response = client.post(
        "/login",
        json={
            "email": "user@example.com",
            "password": "stringst"
        }
    )

    assert response.status_code == 200
    
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    

def test_invalid_login_returns_401():
    response = client.post(
        "/login",
        json={
            "email": "user@example.com",
            "password": "wrong_password"
        }
    )

    assert response.status_code == 401