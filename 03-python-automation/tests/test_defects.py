import pytest
import requests

@pytest.mark.xfail(reason="Restful-Booker accepts negative totalprice — no input validation")
def test_negative_price_rejected(base_url):
    payload = {
        "firstname": "Test",
        "lastname": "NegativePrice",
        "totalprice": -50,  # Invalid negative price
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-01-05"},
    }
    response = requests.post(f"{base_url}/booking", json=payload)
    assert response.status_code == 400  # will fail — API returns 200

@pytest.mark.xfail(reason="Restful-Booker accepts missing firstname — no input validation")
def test_missing_firstname_rejected(base_url):
    payload = {
        #"firstname": "Test",  # Missing firstname
        "lastname": "MissingFirstName",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-01-05"},
    }
    response = requests.post(f"{base_url}/booking", json=payload)
    assert response.status_code == 400  # will fail — API returns 200