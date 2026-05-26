"""Page Object: /reservation/{id} — room booking form"""

from playwright.sync_api import Page, expect


class ReservationPage:
    """Represents the room reservation page.

    Reached by clicking 'Book now' on a room card.
    URL pattern: /reservation/{room_id}?checkin=YYYY-MM-DD&checkout=YYYY-MM-DD
    """

    def __init__(self, page: Page):
        self.page = page

        # Step 1: calendar + price summary → click this to reveal guest form
        self.reserve_now = page.get_by_role("button", name="Reserve Now")

        # Step 2: guest detail fields (visible only after Reserve Now clicked)
        # Fields have no id attributes — located by accessible label name
        self.firstname = page.get_by_label("Firstname")
        self.lastname = page.get_by_label("Lastname")
        self.email = page.get_by_label("Email")
        self.phone = page.get_by_label("Phone")
        self.submit = page.get_by_role("button", name="Reserve Now")

        # Confirmation shown after successful booking
        self.confirmation_heading = page.get_by_role(
            "heading", name="Booking Confirmed!"
        )

    def is_loaded(self) -> bool:
        """Return True if URL contains /reservation/ — confirms navigation succeeded."""
        return "/reservation/" in self.page.url

    def proceed_to_guest_form(self):
        """Click Reserve Now once to reveal the guest details form.
        The same button is clicked again (with form filled) to confirm booking.
        """
        self.reserve_now.click()

    def fill_guest_details(
        self, firstname: str, lastname: str, email: str, phone: str
    ):
        self.firstname.fill(firstname)
        self.lastname.fill(lastname)
        self.email.fill(email)
        self.phone.fill(phone)

    def submit_booking(self):
        self.submit.click()
