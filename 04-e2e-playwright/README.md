# Module 04 — End-to-End Testing with Playwright

## What's tested

UI end-to-end tests against [Shady Meadows B&B](https://automationintesting.online/) — the frontend for the Restful-Booker platform.

| ID | Test | File |
|----|------|------|
| TC-E2E-001 | Homepage loads and renders B&B content | `test_homepage.py` |
| TC-E2E-002 | At least one room card is displayed | `test_homepage.py` |
| TC-E2E-003 | Contact form: valid submission shows confirmation | `test_contact.py` |
| TC-E2E-004 | "Book now" link navigates to /reservation/ URL | `test_booking_flow.py` |
| TC-E2E-005 | Reserve Now reveals guest detail form fields | `test_booking_flow.py` |

## Page Object Model

```
pages/
├── home_page.py         # Homepage: nav, room cards, contact form
└── reservation_page.py  # Reservation page: calendar, Reserve Now, guest form
```

Each page object holds locators and actions for one page. Tests talk to page objects — not raw selectors. A UI change means updating one class, not every test.

## How to run

This module shares the venv from Module 03 (pytest-playwright was installed into it).

```bash
# From repo root — activate Module 03 venv
source 03-python-automation/.venv/bin/activate

cd 04-e2e-playwright
pytest tests/ -v
```

Run headed (watch the browser):
```bash
pytest tests/ -v --headed
```

Run a single test:
```bash
pytest tests/test_homepage.py::test_rooms_are_displayed -v
```

## QA skills demonstrated

- **Page Object Model** — locators and actions encapsulated per page; tests stay selector-free
- **Playwright locator strategy** — role-based (`get_by_role`, `get_by_label`) over fragile CSS IDs
- **SPA handling** — `wait_for_load_state("networkidle")` for React-rendered content
- **Multi-step flows** — calendar → Reserve Now → guest form; each step asserted before proceeding
- **Real selector discovery** — DOM inspected via Playwright accessibility tree, not assumed from static HTML

## Intentional failure case

TC-E2E-002 (`test_rooms_are_displayed`) would fail immediately if rooms stopped rendering — e.g. API down, React hydration error. Asserting `count >= 1` catches silent regressions where the page loads but content doesn't.
