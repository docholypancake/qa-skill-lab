import pytest
import requests


def test_auth_invalid_credentials(base_url): #TC-RB-002 — Authentication with invalid credentials (POST /auth)
    response = requests.post(
        f"{base_url}/auth",
        json={"username": "invalid", "password": "creds"},
    )
    assert response.status_code == 200
    assert response.json().get("reason") == "Bad credentials"
    assert "token" not in response.json()

@pytest.mark.smoke
def test_valid_token_is_string(auth_token):  # TC-RB-004
    assert isinstance(auth_token, str)
    assert len(auth_token) > 0
