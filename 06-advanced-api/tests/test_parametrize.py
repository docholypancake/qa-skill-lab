"""
Data-driven tests using @pytest.mark.parametrize.

Why parametrize?
Each row in the table becomes a separate test with its own ID, result, and failure
message. Writing 8 near-identical test functions manually would be harder to
maintain and review. Here, the logic is written once — the data changes.

Parametrize syntax:
    @pytest.mark.parametrize("arg1, arg2", [
        (value1a, value2a),   # test case A
        (value1b, value2b),   # test case B
    ])
    def test_something(arg1, arg2):
        ...

pytest generates test IDs from the values, or you can name them with
pytest.param(..., id="my_name").
"""

import pytest
import requests

TIMEOUT = 10


# ---------------------------------------------------------------------------
# 1. Valid booking payloads — different shapes that should all succeed
# ---------------------------------------------------------------------------

VALID_PAYLOADS = [
    pytest.param(
        {
            "firstname": "Alice",
            "lastname": "Smith",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {"checkin": "2025-07-01", "checkout": "2025-07-05"},
        },
        id="standard_booking",
    ),
    pytest.param(
        {
            "firstname": "B",          # single-character name
            "lastname": "C",
            "totalprice": 0,           # boundary: zero price
            "depositpaid": False,
            "bookingdates": {"checkin": "2025-12-31", "checkout": "2025-12-31"},
            "additionalneeds": "",     # empty string — valid optional field
        },
        id="boundary_zero_price_same_day",
    ),
    pytest.param(
        {
            "firstname": "A" * 100,   # boundary: very long name
            "lastname": "B" * 100,
            "totalprice": 99999,
            "depositpaid": True,
            "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-12-31"},
            "additionalneeds": "Needs airport pickup, early check-in, and late checkout",
        },
        id="boundary_max_length_fields",
    ),
    pytest.param(
        {
            "firstname": "José",       # non-ASCII characters
            "lastname": "García",
            "totalprice": 250,
            "depositpaid": True,
            "bookingdates": {"checkin": "2025-08-10", "checkout": "2025-08-15"},
        },
        id="unicode_name",
    ),
]


@pytest.mark.parametrize("payload", VALID_PAYLOADS)
def test_create_booking_valid_payloads(base_url, auth_token, payload):
    """TC-M6-001 to TC-M6-004: All valid payload shapes return 200 with a bookingid."""
    response = requests.post(f"{base_url}/booking", json=payload, timeout=TIMEOUT)

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}. Body: {response.text}"
    )
    body = response.json()
    assert "bookingid" in body, "Response missing 'bookingid'"
    assert isinstance(body["bookingid"], int), "bookingid should be an integer"
    assert body["bookingid"] > 0

    # Teardown: clean up the booking we just created
    requests.delete(
        f"{base_url}/booking/{body['bookingid']}",
        headers={"Cookie": f"token={auth_token}"},
        timeout=TIMEOUT,
    )


# ---------------------------------------------------------------------------
# 2. Filter combinations — GET /booking with query params
# ---------------------------------------------------------------------------

FILTER_CASES = [
    pytest.param(
        {"firstname": "Module", "lastname": "Six"},
        id="filter_by_name",
    ),
    pytest.param(
        {"checkin": "2025-06-01"},
        id="filter_by_checkin",
    ),
    pytest.param(
        {"checkout": "2025-06-07"},
        id="filter_by_checkout",
    ),
    pytest.param(
        {"checkin": "2025-06-01", "checkout": "2025-06-07"},
        id="filter_by_date_range",
    ),
]


@pytest.mark.parametrize("filters", FILTER_CASES)
def test_list_bookings_filter_combinations(base_url, booking, filters):
    """TC-M6-005 to TC-M6-008: Each filter combo returns 200 and a list.

    The `booking` fixture creates a known booking before each test and
    deletes it after. We verify our booking ID appears in the filtered list
    only for name-based filters (date filters on a live API are unreliable
    because other bookings with the same dates may or may not exist).
    """
    response = requests.get(f"{base_url}/booking", params=filters, timeout=TIMEOUT)

    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list), "Response should be a list of booking objects"
    # Each item should have a bookingid key
    for item in result:
        assert "bookingid" in item, f"List item missing 'bookingid': {item}"

    # For name filters we can assert our specific booking is in the results
    if "firstname" in filters and "lastname" in filters:
        ids = [item["bookingid"] for item in result]
        assert booking in ids, (
            f"Expected booking {booking} in filtered results, got IDs: {ids}"
        )


# ---------------------------------------------------------------------------
# 3. Missing required fields — Restful-Booker's (absent) input validation
# ---------------------------------------------------------------------------
# These tests document a known defect: the API accepts invalid payloads.
# xfail = we assert the correct behaviour (400), but expect the API to fail
# that assertion (returning 200 instead). The test is marked xfail so it
# appears in the report as a known issue, not a broken suite.

INVALID_PAYLOADS = [
    pytest.param(
        {
            # firstname missing
            "lastname": "NoFirst",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {"checkin": "2025-01-01", "checkout": "2025-01-02"},
        },
        id="missing_firstname",
    ),
    pytest.param(
        {
            "firstname": "NoPrice",
            "lastname": "Test",
            # totalprice missing
            "depositpaid": True,
            "bookingdates": {"checkin": "2025-01-01", "checkout": "2025-01-02"},
        },
        id="missing_totalprice",
    ),
    pytest.param(
        {
            "firstname": "NoDates",
            "lastname": "Test",
            "totalprice": 100,
            "depositpaid": True,
            # bookingdates missing entirely
        },
        id="missing_bookingdates",
    ),
]


@pytest.mark.xfail(
    reason="Restful-Booker accepts payloads with missing required fields — no server-side validation"
)
@pytest.mark.parametrize("payload", INVALID_PAYLOADS)
def test_create_booking_rejects_invalid_payloads(base_url, payload):
    """TC-M6-009 to TC-M6-011: Missing required fields should be rejected with 400.

    These tests are marked xfail because Restful-Booker returns 200 for all
    of them — it has no input validation. The xfail marker documents the gap
    without breaking the suite.
    """
    response = requests.post(f"{base_url}/booking", json=payload, timeout=TIMEOUT)
    assert response.status_code == 400, (
        f"Expected 400 for invalid payload, got {response.status_code}"
    )
