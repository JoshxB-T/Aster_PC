from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_missing_name_signup_field():
    response = client.post(
        "/signup",
        json={
            "email": "test1@example.com",
            "password": ""
        }
    )

    assert response.status_code == 422

def test_missing_email_signup_field():
    response = client.post(
        "/signup",
        json={
            "username": "John",
            "password": "test123"
        }
    )

    assert response.status_code == 422


def test_missing_password_signup_field():
    response = client.post(
        "/signup",
        json={
            "username": "John",
            "email": "test1@example.com",
        }
    )

    assert response.status_code == 422


def test_password_too_short_signup():
    response = client.post(
        "/signup",
        json={
            "username": "John",
            "email": "test1@example.com",
            "password": "test123"
        }
    )

    assert response.status_code == 422


def test_duplicate_email_signup():
    response = client.post(
        "/signup",
        json={
            "username": "John",
            "email": "test1@example.com",
            "password": "test1234"
        }
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}

