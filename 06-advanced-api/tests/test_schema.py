"""
Schema validation tests using jsonschema.

Why schema validation?
A test that only checks `status_code == 200` will pass even if the response
body is `{"error": null}`. Schema validation asserts the *contract* — the
exact shape the API promises to return. This catches:
  - Missing fields added/removed during a deploy
  - Type changes (e.g. totalprice becomes a string "100" instead of int 100)
  - Structural regressions in nested objects

How jsonschema works:
    from jsonschema import validate, ValidationError

    validate(instance=response_body, schema=my_schema)

`validate()` raises `ValidationError` if the instance doesn't match the schema.
If it passes, it returns None silently. We use pytest's `raises()` context
manager for the intentional-failure test, and rely on the silent pass for
positive cases.

The schema lives in schemas/booking.json — one source of truth shared
across all tests in this module.
"""

import json
import os
import pytest
import requests
from jsonschema import validate, ValidationError

TIMEOUT = 10

# Load the schema once at module import time.
# os.path.dirname(__file__) gives us the tests/ directory.
# We go up one level (../) to reach the module root, then into schemas/.
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "schemas", "booking.json")
with open(SCHEMA_PATH) as f:
    BOOKING_SCHEMA = json.load(f)


# ---------------------------------------------------------------------------
# 1. POST /booking response contains a valid booking object
# ---------------------------------------------------------------------------

def test_create_booking_response_schema(base_url, auth_token):
    """TC-M6-012: POST /booking booking field matches the booking schema."""
    payload = {
        "firstname": "Schema",
        "lastname": "Test",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {"checkin": "2025-09-01", "checkout": "2025-09-05"},
        "additionalneeds": "Breakfast",
    }
    response = requests.post(f"{base_url}/booking", json=payload, timeout=TIMEOUT)
    assert response.status_code == 200

    body = response.json()
    # POST /booking wraps the booking object inside a "booking" key:
    # { "bookingid": 123, "booking": { ...booking fields... } }
    assert "booking" in body, f"Response missing 'booking' key: {body}"

    # validate() raises ValidationError if shape is wrong — otherwise silent
    validate(instance=body["booking"], schema=BOOKING_SCHEMA)

    # Cleanup
    requests.delete(
        f"{base_url}/booking/{body['bookingid']}",
        headers={"Cookie": f"token={auth_token}"},
        timeout=TIMEOUT,
    )


# ---------------------------------------------------------------------------
# 2. GET /booking/{id} returns a valid booking object
# ---------------------------------------------------------------------------

def test_get_booking_response_schema(base_url, booking):
    """TC-M6-013: GET /booking/{id} response matches the booking schema.

    The `booking` fixture creates a booking and yields its ID.
    We fetch that booking and validate the response shape.
    """
    response = requests.get(f"{base_url}/booking/{booking}", timeout=TIMEOUT)
    assert response.status_code == 200

    # GET /booking/{id} returns the booking object directly (no wrapper)
    validate(instance=response.json(), schema=BOOKING_SCHEMA)


# ---------------------------------------------------------------------------
# 3. GET /booking (list) — each item has a bookingid integer
# ---------------------------------------------------------------------------

LIST_ITEM_SCHEMA = {
    "type": "object",
    "required": ["bookingid"],
    "properties": {
        "bookingid": {"type": "integer", "minimum": 1}
    },
    "additionalProperties": False,
}


def test_list_bookings_item_schema(base_url):
    """TC-M6-014: Every item in GET /booking list matches the list-item schema."""
    response = requests.get(f"{base_url}/booking", timeout=TIMEOUT)
    assert response.status_code == 200

    items = response.json()
    assert isinstance(items, list), "Expected a list"
    assert len(items) > 0, "Expected at least one booking in the list"

    for item in items:
        validate(instance=item, schema=LIST_ITEM_SCHEMA)


# ---------------------------------------------------------------------------
# 4. Intentional failure — demonstrate what a schema violation looks like
# ---------------------------------------------------------------------------

def test_schema_catches_wrong_type():
    """TC-M6-015: Demonstrate that schema validation catches a type mismatch.

    This test doesn't call the API at all — it validates a hand-crafted
    bad object against the schema. The purpose is to show that jsonschema
    would catch a regression where totalprice becomes a string.

    We expect ValidationError to be raised — so we assert that it IS raised.
    If it weren't, the test would fail (meaning our schema is too permissive).
    """
    bad_booking = {
        "firstname": "Type",
        "lastname": "Mismatch",
        "totalprice": "one hundred",   # string instead of integer — should fail
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-01-01",
            "checkout": "2025-01-05",
        },
    }

    with pytest.raises(ValidationError) as exc_info:
        validate(instance=bad_booking, schema=BOOKING_SCHEMA)

    # Confirm the error message points to the right field
    assert "totalprice" in str(exc_info.value.path) or "is not of type" in str(exc_info.value.message)


def test_schema_catches_missing_required_field():
    """TC-M6-016: Schema catches a response missing 'bookingdates'.

    Same pattern — hand-crafted bad object, assert ValidationError raised.
    """
    bad_booking = {
        "firstname": "Missing",
        "lastname": "Dates",
        "totalprice": 100,
        "depositpaid": False,
        # bookingdates intentionally omitted
    }

    with pytest.raises(ValidationError):
        validate(instance=bad_booking, schema=BOOKING_SCHEMA)
