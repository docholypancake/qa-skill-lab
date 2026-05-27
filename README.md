# QA Skill Lab

A structured portfolio demonstrating QA engineering skills — from test documentation through API automation, Python pytest, and end-to-end testing with Playwright.

**Target API:** [Restful-Booker](https://restful-booker.herokuapp.com/apidoc/index.html) — a public hotel booking REST API used as the primary system under test across all modules.

---

## Modules

### ✅ 01 — Test Documentation
Documented the full Restful-Booker booking lifecycle before writing a single line of code.

- **Test plan** (IEEE 829): scope, risk analysis, entry/exit criteria, test approach for a hotel booking REST API
- **14 test cases**: happy path (create/read/update/delete booking), auth failure, boundary values (min/max price, date edge cases), missing required fields, unauthorised mutation attempts
- **Traceability matrix**: every requirement mapped to at least one test — 100% coverage verified
- **BUG-RB-001**: `POST /auth` returns HTTP 200 (not 401) for invalid credentials and includes a `reason` field instead of an error status — filed with severity, steps to reproduce, expected vs actual

→ [View module](01-documentation/README.md)

---

### ✅ 02 — API Testing with Postman
Executed all 14 test cases against the live API. 28 assertions across the booking lifecycle — 26 pass, 2 intentionally fail to document known defects.

What the tests verified:
- `GET /ping` → 201 Created (server alive)
- `POST /auth` with valid credentials → returns a token string; with invalid credentials → returns `reason: "Bad credentials"` (no token)
- `POST /booking` → creates booking, response includes `bookingid` integer and echoes all fields back correctly
- `GET /booking/{id}` → returns correct firstname, lastname, price, dates
- `GET /booking?firstname=Jim&lastname=Brown` → booking ID appears in filtered list
- `PUT /booking/{id}` with token → full update accepted, response reflects new values
- `PATCH /booking/{id}` with token → partial update (firstname only) accepted, other fields unchanged
- `PUT` and `PATCH` without token → 403 Forbidden
- `DELETE /booking/{id}` with token → 201 Created (booking gone)
- **Defect TC-013**: `POST /booking` with `totalprice: -50` → API returns 200 (should reject negative price)
- **Defect TC-014**: `POST /booking` with `firstname` omitted → API returns 200 (should require mandatory field)

→ [View module](02-api-postman/README.md)

---

### ✅ 03 — Python Automation (pytest + requests)
Same 14 test cases reimplemented in pytest. Automated the full CRUD lifecycle including teardown — each test cleans up its own data via a `yield` fixture.

What the tests verified (beyond Module 2):
- Booking ID returned by `POST /booking` is an integer > 0 (not just any response)
- `GET /booking/{id}` after create confirms `firstname == "Jim"` — round-trip data integrity
- Filtered list `GET /booking?firstname=Jim&lastname=Brown` contains the specific booking ID just created
- `PUT` response echoes the updated name (`"Jane"` replaces `"Jim"`)
- `PATCH` updates only `firstname` to `"Updated"` while `lastname` stays `"Brown"` — partial update doesn't clobber untouched fields
- `PUT`/`PATCH` without token → 403 (auth enforced on write paths)
- `DELETE` with token → 201; fixture teardown confirms delete path works on every test run
- `POST /auth` with bad credentials → 200 but `reason == "Bad credentials"`, no `token` key in response
- Defects TC-013 and TC-014 marked `xfail` — test runs, asserts 400, gets 200, recorded as known failure not a broken suite

→ [View module](03-python-automation/README.md)

---

### ✅ 04 — End-to-End Testing (Playwright)
5 browser tests against the Shady Meadows B&B frontend (`automationintesting.online`) — the React UI backed by Restful-Booker.

What the tests verified:
- **TC-E2E-001**: navigating to the site renders real content — page body contains `"Shady Meadows"`, not an error page or blank shell
- **TC-E2E-002**: at least one room card (`div.room-card`) is visible after page load — confirms React hydrated and the API returned room data
- **TC-E2E-003**: contact form submits successfully — fills name/email/phone/subject/message, clicks Submit, asserts `"Thanks for getting in touch"` heading appears
- **TC-E2E-004**: clicking "Book now" on a room navigates to a URL containing `/reservation/` — routing works, room links are functional
- **TC-E2E-005**: reservation form is reachable — clicking "Reserve Now" reveals the guest detail fields (Firstname, Lastname, Email, Phone) and submit button

→ [View module](04-e2e-playwright/README.md)

---

### ✅ 05 — Smoke Tests
5 tests curated from Modules 3 & 4 that answer one question: **is the system alive?** Runs on every push, stops at first failure.

| Test | What it catches |
|------|----------------|
| `GET /ping` → 201 | API server unreachable or crashed |
| `POST /auth` returns token string | Auth service broken or returning garbage |
| `POST /booking` returns integer ID | Core write path broken, DB down |
| Homepage loads with "Shady Meadows" | UI unreachable or serving error page |
| At least 1 room card visible | React failed to hydrate or rooms API returning empty |

→ [View module](05-smoke-tests/README.md)

---

### ✅ 06 — Advanced API Testing (Python)
Three techniques that go beyond status-code checks: data-driven coverage, contract validation, and performance SLA gates. 22 tests total.

What the tests verified:
- **Parametrize (11 tests)**: 4 valid booking shapes (standard, zero price, 100-char names, unicode), 4 filter combos on `GET /booking`, 3 missing-required-field cases marked `xfail` — systematic boundary coverage without duplicated test functions
- **Schema validation (6 tests)**: `POST /booking` and `GET /booking/{id}` response bodies validated against `schemas/booking.json` — required fields, types, ISO date pattern, nested object structure; intentional failures prove the schema catches type regressions and missing fields
- **Response time assertions (5 tests)**: SLA gates — `/ping` < 1s, reads < 2s, writes < 3s; marked `@pytest.mark.slow`, run as `continue-on-error` in CI to surface flakiness without blocking the build

→ [View module](06-advanced-api/README.md)

---

## Skills demonstrated

| Skill | Module |
|-------|--------|
| Test plan writing (IEEE 829) | 01 |
| Test case design (EP, BVA, positive/negative) | 01 |
| Requirements traceability | 01 |
| Defect reporting (severity/priority classification) | 01 |
| API testing + assertion depth | 02 |
| Postman environments + pre-request scripts | 02 |
| Newman CLI + CI integration | 02 |
| Python pytest + requests | 03 |
| Fixtures and test lifecycle management | 03 |
| Page Object Model | 04 |
| Smoke testing + CI pipeline | 05 |
| Data-driven testing (`@pytest.mark.parametrize`) | 06 |
| JSON Schema contract validation | 06 |
| Response time SLA assertions | 06 |

## Tooling

- Python 3, pytest, requests, playwright, python-dotenv, jsonschema
- Postman (v2.1 collections), Newman
- GitHub Actions for CI
- ruff for linting
