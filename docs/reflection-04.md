# Reflection — Module 04: End-to-End Testing (Playwright)

## What I built

Five E2E tests against a live Next.js hotel booking UI using Playwright with Python bindings and the Page Object Model. Two page objects (`HomePage`, `ReservationPage`), three test files.

## What I learned

**Static HTML lies.** The site is a React SPA — raw HTML is a loading spinner. Every selector had to be discovered by Playwright navigating the live, rendered DOM. You cannot write E2E selectors from a View Source.

**Role-based locators beat CSS IDs.** The reservation form fields had no `id` attributes. `get_by_label("Firstname")` worked where `#firstname` failed. Role-based locators (`get_by_role`, `get_by_label`) are more stable because they match what users actually see, not implementation details.

**`exact=True` matters on case.** `get_by_role("link", name="Book now")` matched the hero "Book Now" anchor (same-page scroll) because Playwright name matching is case-insensitive by default. `exact=True` made it case-sensitive, targeting only the room-level "Book now" links.

**Multi-step flows need explicit steps.** The reservation page has two states: calendar view → guest form. Clicking "Reserve Now" toggles between them. The test has to mirror that flow — assert step 1 is correct, perform the action, then assert step 2. Skipping the intermediate assertion hides bugs where step 1 broke silently.

**`wait_for_load_state("networkidle")` is the SPA handshake.** Without it, Playwright would interact with a half-rendered page. `networkidle` waits until no network requests have fired for 500ms — a reliable signal that React has finished hydrating.

**POM pays off immediately.** When the `Book now` locator was wrong, I fixed it in one place (`home_page.py`) and both tests that use it were fixed. Without POM, I'd have hunted the selector across every test file.

## Mistakes made

- Used `.hotel-room-info` for room cards — wrong class. Discovery test found `.room-card`.
- `get_by_role("link", name="Book now")` matched hero CTA (uppercase N) first — `exact=True` fixed it.
- Assumed `#firstname` IDs — reservation page uses label-based fields only.
- Wrote TC-E2E-004 as an imperative `pytest.xfail()` (skips test body entirely) — should have been `@pytest.mark.xfail` decorator. Corrected to Option A (deleted speculative test).

## What carries forward to Module 5

Module 5 is the smoke suite — fast, critical-path only, runs on every push. The smoke tests will cherry-pick from Modules 3 and 4: API health check, auth token, homepage load, room count. Same fixtures, same POMs, new `pytest.ini` with `--timeout` and `-x` (stop on first failure).
