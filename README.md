# QA Skill Lab

A structured portfolio demonstrating QA engineering skills — from test documentation through API automation, Python pytest, and end-to-end testing with Playwright.

**Target API:** [Restful-Booker](https://restful-booker.herokuapp.com/apidoc/index.html) — a public hotel booking REST API used as the primary system under test across all modules.

---

## Modules

### ✅ 01 — Test Documentation
Professional QA documentation following IEEE 829 and ISTQB terminology.

- Test plan with scope, risk analysis, entry/exit criteria
- 14 test cases covering the full booking lifecycle (positive, negative, boundary)
- Requirements traceability matrix (100% feature coverage)
- Bug report template + filed defect (BUG-RB-001)

→ [View module](01-documentation/README.md)

---

### ✅ 02 — API Testing with Postman
All 14 test cases executed via Postman Collection Runner and Newman CLI. 28 assertions, 26 pass, 2 intentional defect failures documenting known Restful-Booker input validation gaps.

→ [View module](02-api-postman/README.md)

---

### ✅ 03 — Python Automation (pytest + requests)
14 test cases in pytest. Shared fixtures with `yield` teardown, session/module/function scoping, and `xfail` markers for known defects. CI via GitHub Actions.

→ [View module](03-python-automation/README.md)

---

### ✅ 04 — End-to-End Testing (Playwright)
5 E2E tests against Shady Meadows B&B UI. Page Object Model with role-based locators, SPA handling (`networkidle`), and multi-step booking flow assertion.

→ [View module](04-e2e-playwright/README.md)

---

### ✅ 05 — Smoke Tests
5 critical-path tests curated from Modules 3 & 4 via `@pytest.mark.smoke` markers. Runs on every push to any branch. Stops at first failure (`-x`). Covers: API health, auth, booking create, UI load, room listing.

→ [View module](05-smoke-tests/README.md)

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

## Tooling

- Python 3, pytest, requests, playwright, python-dotenv
- Postman (v2.1 collections), Newman
- GitHub Actions for CI
- ruff for linting
