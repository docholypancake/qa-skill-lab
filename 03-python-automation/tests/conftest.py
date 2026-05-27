import os
import pytest
import requests
from dotenv import load_dotenv

# Load environment variables once at session start
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

@pytest.fixture(scope="session")
def base_url():
    """Return the base URL from environment variables."""
    return os.getenv("BASE_URL")


TIMEOUT = 10  # seconds — fail fast instead of hanging forever


@pytest.fixture(scope="module")
def ping_response(base_url):
    return requests.get(f"{base_url}/ping", timeout=TIMEOUT)


@pytest.fixture(scope="session")
def auth_token(base_url):
    """Authenticate and return auth token from /auth endpoint."""
    response = requests.post(
        f"{base_url}/auth",
        json={
            "username": os.getenv("USERNAME"),
            "password": os.getenv("PASSWORD"),
        },
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return response.json()["token"]


@pytest.fixture(scope="function")
def booking(base_url, auth_token):
    payload = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01",
        },
        "additionalneeds": "Breakfast",
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
     
