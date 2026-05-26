"""TC-E2E-001, TC-E2E-002 — Homepage: load and room listing"""

import pytest
from pages.home_page import HomePage


def test_homepage_loads(page):
    """TC-E2E-001: Navigating to the site renders without errors."""
    home = HomePage(page)
    home.navigate()
    # Body should contain the B&B name — confirms real content rendered, not error page
    assert "Shady Meadows" in page.inner_text("body")


def test_rooms_are_displayed(page):
    """TC-E2E-002: At least one room card is visible after page load."""
    home = HomePage(page)
    home.navigate()
    count = home.room_count()
    assert count >= 1, f"Expected at least 1 room card, found {count}"
