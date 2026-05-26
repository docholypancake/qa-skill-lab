"""TC-E2E-003, — Contact form"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage


def test_contact_form_success(page):
    """TC-E2E-003: Submitting valid contact details shows a success message."""
    home = HomePage(page)
    home.navigate()

    # Scroll the contact form into view — it sits at page bottom
    home.contact_name.scroll_into_view_if_needed()

    home.submit_contact_form(
        name="Jane Tester",
        email="jane@example.com",
        phone="01234567890",
        subject="Test enquiry subject",
        message="This is a test message sent by an automated Playwright test suite.",
    )

    # After submit the site replaces the form with a confirmation heading
    success = page.get_by_role("heading", name="Thanks for getting in touch")
    expect(success).to_be_visible(timeout=5000)


