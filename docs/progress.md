# Progress — QA Skill Lab

## Module 01 — Test Documentation ✅ Complete

- [x] Test plan (`test-plan.md`) — RB-TP-001, IEEE 829 structure
- [x] Test cases (`test-cases.md`) — 14 cases, full booking lifecycle
- [x] Traceability matrix (`traceability-matrix.md`) — 100% feature coverage
- [x] Bug report template (`bug-report-template.md`)
- [x] Defect filed (`BUG-RB-001.md`) — `POST /auth` returns 200 for bad credentials
- [x] Module README (`01-documentation/README.md`)
- [x] Reflection note (`docs/reflection-01.md`)
- [x] Manual execution of test cases — executed via Postman Collection Runner (Module 2)

**Skills demonstrated:** test plan writing, test case design (equivalence partitioning, BVA), assertion depth, RTM, defect reporting, severity/priority classification.

---

## Module 02 — API Testing with Postman ✅ Complete

- [x] "Booker" collection created in Postman
- [x] Postman environment set up (`base_url`, `token`, `booking_id` variables)
- [x] All TC-RB-001 → TC-RB-014 implemented as requests with `pm.test()` assertions
- [x] Data chaining: TC-RB-001 saves `booking_id`, TC-RB-004 saves `token` via `pm.environment.set()`
- [x] Collection run: 28 assertions, 26 pass, 2 intentional defect failures (TC-013, TC-014)
- [x] Bonus finding: TC-RB-014 returns 500 (server crash) — severity upgraded to High
- [x] Collection exported as v2.1 JSON → committed to `02-api-postman/`
- [x] Newman CLI run verified (same 26/28 result, 3.9s total)
- [x] Module README (`02-api-postman/README.md`)
- [x] Reflection note (`docs/reflection-02.md`)

**Skills demonstrated:** Postman environments, data chaining, assertion depth, dependency ordering, Newman CLI, intentional failure documentation.

---

## Module 03 — Python Automation (pytest + requests) ✅ Complete

- [x] Virtual environment set up (`03-python-automation/.venv/`)
- [x] `requirements.txt` (pytest, requests, python-dotenv)
- [x] All 14 test cases reimplemented in pytest across 4 test files
- [x] `conftest.py` — shared fixtures: `base_url`, `auth_token` (session), `ping_response` (module), `booking` with yield teardown (function)
- [x] `xfail` markers for TC-013 and TC-014 — known defect documentation
- [x] Suite result: 14 passed, 2 xfailed
- [x] Module README (`03-python-automation/README.md`)
- [x] Reflection note (`docs/reflection-03.md`)
- [x] GitHub Actions workflow (`.github/workflows/03-python-tests.yml`)

**Skills demonstrated:** pytest fixtures, yield teardown, fixture scoping, fixture injection, xfail markers, virtual environments, requests library.

---

## Module 04 — E2E Testing (Playwright) ✅ Complete

- [x] Playwright installed into Module 3 venv (`pytest-playwright`, `playwright install chromium`)
- [x] Target UI: `https://automationintesting.online/` (Shady Meadows B&B — Restful-Booker frontend)
- [x] `HomePage` POM — room cards (`.room-card`), contact form, Book now links
- [x] `ReservationPage` POM — two-step flow: calendar → Reserve Now → guest form
- [x] 5 E2E tests: TC-E2E-001 through TC-E2E-005 — all passing
- [x] Real selector discovery via Playwright accessibility tree (SPA — static HTML useless)
- [x] Root `conftest.py` — fixes VSCode test extension `sys.path` for POM imports
- [x] Module README (`04-e2e-playwright/README.md`)
- [x] Reflection note (`docs/reflection-04.md`)
- [x] GitHub Actions workflow (`.github/workflows/04-e2e-tests.yml`)

**Skills demonstrated:** POM, role-based locators, `exact=True` case-sensitive matching, SPA networkidle handling, multi-step flow testing, live DOM selector discovery.

---

## Module 05 — Smoke Tests ✅ Complete

- [x] `@pytest.mark.smoke` markers added to 3 API tests (health, auth, booking create) and 2 UI tests (homepage load, rooms displayed)
- [x] Root `pytest.ini` — collects from both `03-python-automation/tests` and `04-e2e-playwright/tests` in one run
- [x] `TIMEOUT = 10` added to all `requests` calls — fail-fast instead of infinite Heroku cold-start hangs
- [x] `pytest -m smoke -x -v` — stop on first failure, all 5 smoke tests pass
- [x] Module README (`05-smoke-tests/README.md`)
- [x] Reflection note (`docs/reflection-05.md`)
- [x] GitHub Actions workflow (`.github/workflows/05-smoke.yml`) — triggers on every push to any branch

---

## Cross-cutting

- [x] Top-level `README.md` — portfolio landing page (updated after each module ships)
- [x] GitHub repo created and public — https://github.com/docholypancake/qa-skill-lab
- [x] Initial commit pushed
