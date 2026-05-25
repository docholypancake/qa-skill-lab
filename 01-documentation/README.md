# Module 01 — Test Documentation

## What this module demonstrates

Professional QA documentation following **IEEE 829** structure and **ISTQB Foundation** terminology. The deliverables here are the single source of truth that Modules 2 (Postman) and 3 (pytest) trace back to — test case IDs are stable across all three modules.

## System under test

**Restful-Booker** — a public REST API simulating a hotel booking system.
Base URL: `https://restful-booker.herokuapp.com`
API docs: `https://restful-booker.herokuapp.com/apidoc/index.html`

## Deliverables

| File | What it is |
|------|-----------|
| `test-plan.md` | IEEE 829-style test plan (RB-TP-001). Defines scope, approach, entry/exit criteria, risks. |
| `test-cases.md` | 14 test cases covering the full booking lifecycle. Each case includes test data, steps, expected results, and a business-rule rationale. |
| `traceability-matrix.md` | Bidirectional RTM mapping all 14 in-scope features to test cases. 100% feature coverage at the written stage. |
| `bug-report-template.md` | Reusable bug report template with severity/priority guidance. |
| `BUG-RB-001.md` | Filed defect — `POST /auth` returns `200 OK` instead of `401 Unauthorized` for invalid credentials. |

## Test case summary

| TC ID | Title | Type | Priority |
|-------|-------|------|----------|
| TC-RB-001 | Create booking with valid data | Positive | High |
| TC-RB-002 | Authenticate with invalid credentials | Negative | High |
| TC-RB-003 | Health check | Positive | High |
| TC-RB-004 | Authenticate with valid credentials | Positive | High |
| TC-RB-005 | Read a booking by ID | Positive | High |
| TC-RB-006 | List bookings with a filter | Positive | Medium |
| TC-RB-007 | Full update of a booking (PUT) | Positive | High |
| TC-RB-008 | Full update rejected without valid token | Negative | High |
| TC-RB-009 | Partial update of a booking (PATCH) | Positive | High |
| TC-RB-010 | Partial update rejected without valid token | Negative | High |
| TC-RB-011 | Delete a booking | Positive | High |
| TC-RB-012 | Delete rejected without valid token | Negative | High |
| TC-RB-013 | Input handling: negative totalprice (intentional failure) | Negative/Boundary | Medium |
| TC-RB-014 | Create booking with missing required field (intentional failure) | Negative | Medium |

TC-RB-013 and TC-RB-014 are **intentional failure cases** — they document known Restful-Booker defects (no input validation). A test suite that only ever passes is not a useful test suite.

## QA skills demonstrated

- **Test plan writing** — scope definition, risk analysis, entry/exit criteria, IEEE 829 structure
- **Test case design** — equivalence partitioning, boundary value analysis, positive/negative paths
- **Assertion depth** — every case asserts status code + response shape + business rule, never status code alone
- **Requirements traceability** — bidirectional RTM, 100% feature coverage documented
- **Defect reporting** — severity vs. priority classification, atomic reproduction steps, actual vs. expected separation
- **Test lifecycle awareness** — preconditions, postconditions, teardown, dependency chains between cases

## How to read the test cases

Each case follows this structure:

1. **Metadata table** — ID, feature, type, priority, preconditions
2. **Test data** — exact payload or "no request body required"
3. **Steps** — atomic, reproducible, environment-agnostic
4. **Expected result** — labelled by assertion type: *(response shape)* / *(business rule)*
5. **Postconditions** — state left behind; teardown responsibility
6. **Why this case matters** — the QA reasoning, not just the mechanics

## Execution

Test cases in this module are documented for **manual execution** (run in Postman or curl, record results by hand). Automated execution is covered in:
- **Module 02** — Postman collection with `pm.test()` assertions + Newman CLI runner
- **Module 03** — pytest + requests automation suite
