"""Page Object: automationintesting.online homepage"""

from playwright.sync_api import Page, expect


class HomePage:
    """Represents the hotel homepage.

    Responsibilities:
    - Navigate to the site
    - Assert key elements are visible
    - Expose room cards and the contact form
    """

    URL = "https://automationintesting.online"

    def __init__(self, page: Page):
        # Store the Playwright page object — all actions go through it
        self.page = page

        # --- Locators ---
        # Locators are lazy: they don't query the DOM until you call an action on them.
        # Keeping them here means a selector change = one edit, not a file-wide search.
        self.logo = page.locator("nav .navbar-brand, h1").first
        self.room_cards = page.locator(".room-card")
        # exact=True → case-sensitive; skips hero "Book Now" anchor, targets room-level links
        self.book_links = page.get_by_role("link", name="Book now", exact=True)

        # Contact form fields
        self.contact_name = page.locator("#name")
        self.contact_email = page.locator("#email")
        self.contact_phone = page.locator("#phone")
        self.contact_subject = page.locator("#subject")
        self.contact_message = page.locator("#description")
        self.contact_submit = page.get_by_role("button", name="Submit")
        self.contact_success = page.locator(".contact-us .row p").first

    # --- Actions ---

    def navigate(self):
        """Load the homepage and wait for rooms to render."""
        self.page.goto(self.URL)
        # SPA: wait until network settles so React has rendered rooms
        self.page.wait_for_load_state("networkidle")

    def room_count(self) -> int:
        return self.room_cards.count()

    def click_book_first_room(self):
        self.book_links.first.click()

    def submit_contact_form(
        self, name: str, email: str, phone: str, subject: str, message: str
    ):
        self.contact_name.fill(name)
        self.contact_email.fill(email)
        self.contact_phone.fill(phone)
        self.contact_subject.fill(subject)
        self.contact_message.fill(message)
        self.contact_submit.click()
