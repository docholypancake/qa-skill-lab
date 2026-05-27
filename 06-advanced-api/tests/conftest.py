import os
import pytest
import requests
from dotenv import load_dotenv

# Reuse the same .env as module 03 (one source of truth for credentials)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", "03-python-automation", ".env"))

TIMEOUT = 10  # seconds


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")


@pytest.fixture(scope="session")
def auth_token(base_url):
    """Authenticate once per session. Returns the token string."""
    response = requests.post(
        f"{base_url}/auth",
        json={
            "username": os.getenv("USERNAME", "admin"),
            "password": os.getenv("PASSWORD", "password123"),
        },
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return response.json()["token"]


@pytest.fixture(scope="function")
def booking(base_url, auth_token):
    """Create a booking, yield its ID, then delete it.

    This is the same yield-fixture pattern from module 03.
    scope="function" means a fresh booking is created for each test
    that requests this fixture, and cleaned up after that test finishes.
    """
    payload = {
        "firstname": "Module",
        "lastname": "Six",
        "totalprice": 200,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-06-01",
            "checkout": "2025-06-07",
        },
        "additionalneeds": "Late checkout",
    }
    response = requests.post(f"{base_url}/booking", json=payload, timeout=TIMEOUT)
    response.raise_for_status()
    booking_id = response.json()["bookingid"]

    yield booking_id

    requests.delete(
        f"{base_url}/booking/{booking_id}",
        headers={"Cookie": f"token={auth_token}"},
        timeout=TIMEOUT,
    )
