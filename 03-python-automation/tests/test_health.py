"""TC-RB-003 — Health check (GET /ping)"""

def test_ping_returns_201(ping_response):
    assert ping_response.status_code == 201


def test_ping_body_is_created(ping_response):
    assert ping_response.text == "Created"
