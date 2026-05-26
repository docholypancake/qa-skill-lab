"""TC-E2E-004, TC-E2E-005 — Booking flow: navigation and form"""

from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.reservation_page import ReservationPage


def test_book_now_navigates_to_reservation(page):
    """TC-E2E-004: Clicking 'Book now' navigates to the reservation page."""
    home = HomePage(page)
    home.navigate()

    # Click the first 'Book now' link and wait for navigation to settle
    home.book_links.first.click()
    page.wait_for_load_state("networkidle")

    reservation = ReservationPage(page)
    assert reservation.is_loaded(), (
        f"Expected URL to contain '/reservation/' but got: {page.url}"
    )


def test_reservation_form_is_visible(page):
    """TC-E2E-005: Clicking Reserve Now reveals the guest details form."""
    home = HomePage(page)
    home.navigate()
    home.book_links.first.click()
    page.wait_for_load_state("networkidle")

    reservation = ReservationPage(page)
    # Reservation page is a two-step flow:
    # Step 1 — calendar + price summary visible
    expect(reservation.reserve_now).to_be_visible()

    # Step 2 — click Reserve Now → guest form renders
    reservation.proceed_to_guest_form()
    expect(reservation.firstname).to_be_visible()
    expect(reservation.lastname).to_be_visible()
    expect(reservation.email).to_be_visible()
    expect(reservation.phone).to_be_visible()
    expect(reservation.submit).to_be_visible()
