"""
Response time assertions.

Why measure response time in tests?
Performance regressions are invisible to functional tests. An endpoint
can return correct data in 8 seconds — every assertion passes, every user
suffers. Asserting `elapsed < threshold` makes slow responses a test failure,
not a helpdesk ticket.

How it works:
    response = requests.get(url, timeout=10)
    assert response.elapsed.total_seconds() < 2.0

`response.elapsed` is a timedelta set by requests from the moment the
request was sent to the moment the first byte of the response arrived.
It does NOT include connection setup time on the first request (use a
`requests.Session` for that). It's not a load test — it's a single-request
SLA gate.

Thresholds used here:
  - /ping (health check)    < 1.0s  — should be near-instant
  - GET /booking            < 2.0s  — simple read with filters
  - GET /booking/{id}       < 2.0s  — single-record fetch
  - POST /booking           < 3.0s  — write operation, DB insert
  - DELETE /booking/{id}    < 3.0s  — write operation, DB delete

These are conservative thresholds for a free-tier Heroku dyno. In a real
project you'd calibrate against a baseline and tighten over time.

Important: timing tests are inherently flaky on slow networks or cold dynos.
Mark them with `@pytest.mark.slow` so they can be excluded in CI with `-m "not slow"`.
"""

import pytest
import requests

TIMEOUT = 10


# SLA thresholds in seconds
SLA = {
    "ping": 1.0,
    "read": 2.0,
    "write": 3.0,
}


@pytest.mark.slow
def test_ping_response_time(base_url):
    """TC-M6-017: GET /ping responds within SLA."""
    response = requests.get(f"{base_url}/ping", timeout=TIMEOUT)
    elapsed = response.elapsed.total_seconds()

    assert response.status_code == 201
    assert elapsed < SLA["ping"], (
        f"GET /ping too slow: {elapsed:.3f}s (SLA: {SLA['ping']}s)"
    )


@pytest.mark.slow
def test_list_bookings_response_time(base_url):
    """TC-M6-018: GET /booking list responds within SLA."""
    response = requests.get(f"{base_url}/booking", timeout=TIMEOUT)
    elapsed = response.elapsed.total_seconds()

    assert response.status_code == 200
    assert elapsed < SLA["read"], (
        f"GET /booking too slow: {elapsed:.3f}s (SLA: {SLA['read']}s)"
    )


@pytest.mark.slow
def test_get_single_booking_response_time(base_url, booking):
    """TC-M6-019: GET /booking/{id} responds within SLA.

    `booking` fixture creates a real booking to fetch — avoids testing
    against a non-existent ID which would return 404 at a different speed.
    """
    response = requests.get(f"{base_url}/booking/{booking}", timeout=TIMEOUT)
    elapsed = response.elapsed.total_seconds()

    assert response.status_code == 200
    assert elapsed < SLA["read"], (
        f"GET /booking/{{id}} too slow: {elapsed:.3f}s (SLA: {SLA['read']}s)"
    )


@pytest.mark.slow
def test_create_booking_response_time(base_url, auth_token):
    """TC-M6-020: POST /booking responds within SLA."""
    payload = {
        "firstname": "Perf",
        "lastname": "Test",
        "totalprice": 50,
        "depositpaid": False,
        "bookingdates": {"checkin": "2025-11-01", "checkout": "2025-11-03"},
    }
    response = requests.post(f"{base_url}/booking", json=payload, timeout=TIMEOUT)
    elapsed = response.elapsed.total_seconds()

    assert response.status_code == 200
    assert elapsed < SLA["write"], (
        f"POST /booking too slow: {elapsed:.3f}s (SLA: {SLA['write']}s)"
    )

    # Cleanup
    booking_id = response.json()["bookingid"]
    requests.delete(
        f"{base_url}/booking/{booking_id}",
        headers={"Cookie": f"token={auth_token}"},
        timeout=TIMEOUT,
    )


@pytest.mark.slow
def test_delete_booking_response_time(base_url, booking, auth_token):
    """TC-M6-021: DELETE /booking/{id} responds within SLA.

    Note: the `booking` fixture will also attempt a DELETE in teardown.
    Deleting an already-deleted booking returns 405 on Restful-Booker,
    which is fine — fixture teardown ignores the response code.
    """
    response = requests.delete(
        f"{base_url}/booking/{booking}",
        headers={"Cookie": f"token={auth_token}"},
        timeout=TIMEOUT,
    )
    elapsed = response.elapsed.total_seconds()

    assert response.status_code == 201
    assert elapsed < SLA["write"], (
        f"DELETE /booking/{{id}} too slow: {elapsed:.3f}s (SLA: {SLA['write']}s)"
    )
