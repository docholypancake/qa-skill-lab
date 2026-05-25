# Test Plan — Restful-Booker API

| Field                 | Value                                                  |
| --------------------- | ------------------------------------------------------ |
| **Test Plan ID**      | RB-TP-001                                              |
| **Version**           | 0.1 (draft)                                            |
| **Author**            | Oleh Blazhko                                           |
| **Date**              | 2026-05-24                                             |
| **System Under Test** | Restful-Booker REST API                                |
| **Base URL**          | https://restful-booker.herokuapp.com                   |
| **Reference**         | https://restful-booker.herokuapp.com/apidoc/index.html |

> This plan follows the structure of **IEEE 829** (Test Plan) trimmed to what a single QA engineer needs, with terminology from the **ISTQB Foundation** syllabus. Each section answers one question: *what, why, how, and when do we stop.*

---

## 1. Introduction & Objective

Restful-Booker is a public REST API that simulates the booking system of a small hotel. It exposes authentication and full CRUD (Create, Read, Update, Delete) operations over hotel bookings, plus a health-check endpoint.

**Objective of this test effort:** verify that the booking lifecycle behaves correctly — that bookings can be created, retrieved, modified, and deleted; that authentication gates the operations it should; and that the API responds sensibly to invalid input. This plan governs the **manual/documented** test design for Module 1. The same scope is later automated in Modules 2 (Postman) and 3 (pytest), so the test cases written here are the single source of truth those modules trace back to.

## 2. Test Items

| Item | Endpoint(s) | Notes |
|------|-------------|-------|
| Health check | `GET /ping` | Returns `201 Created` when the service is up |
| Authentication | `POST /auth` | Returns an auth `token` used for protected operations |
| Create booking | `POST /booking` | No auth required |
| Read booking(s) | `GET /booking`, `GET /booking/:id` | List of IDs (filterable) / single booking |
| Update booking (full) | `PUT /booking/:id` | Auth required |
| Update booking (partial) | `PATCH /booking/:id` | Auth required |
| Delete booking | `DELETE /booking/:id` | Auth required |

**Booking resource shape:**

```json
{
  "firstname": "Jim",
  "lastname": "Brown",
  "totalprice": 111,
  "depositpaid": true,
  "bookingdates": { "checkin": "2024-01-01", "checkout": "2024-01-05" },
  "additionalneeds": "Breakfast"
}
```

## 3. Features To Be Tested (In Scope)

- **Health:** service availability via `/ping`.
- **Auth:** valid credentials return a token; invalid credentials are rejected.
- **Create:** a booking is created and the response echoes the submitted data with a new `bookingid`.
- **Read:** a created booking can be retrieved by ID; listing returns IDs; filters narrow results.
- **Update:** full (`PUT`) and partial (`PATCH`) updates change the right fields and require a valid token.
- **Delete:** a booking can be removed and is no longer retrievable afterward.
- **Authorization rules:** protected operations are refused without a valid token.
- **Input handling:** the API's response to malformed or out-of-range data (negative price, missing required fields, illogical dates).

## 4. Features NOT To Be Tested (Out of Scope)

- Performance, load, and stress behaviour (response under concurrency).
- Security testing beyond the documented auth flow (injection, rate limiting, etc.).
- The XML response variant (`Accept: application/xml`) — JSON only for this module.
- The hosting platform / infrastructure (Heroku cold starts, TLS config).
- UI — Restful-Booker has no UI; this is an API-only effort.

Out-of-scope items are listed deliberately: stating them prevents scope creep and tells a reviewer what *not* to expect coverage for.

## 5. Test Approach / Strategy

- **Test design techniques:** equivalence partitioning and boundary value analysis for inputs (e.g. price, dates); positive and negative paths for every operation.
- **Assertion depth:** assertions go beyond status codes. Each test checks the **response shape** (expected fields/types) and the **business rule** (e.g. a retrieved booking matches what was created; an updated field actually changed). A bare `200 OK` is never sufficient.
- **Test levels:** API/integration level (the API is treated as a black box over HTTP).
- **Progression:** documented manually in this module, then executed via Postman (Module 2) and automated in pytest (Module 3). Test case IDs are stable so they trace across all three.
- **Data management:** each create test produces its own booking and cleans up after itself where possible, so tests stay independent.

## 6. Item Pass/Fail Criteria

A test case **passes** when the actual HTTP status, response body shape, and business-rule assertions all match the expected results recorded in the test case. A test case **fails** on any mismatch. A defect is logged for every failure that reflects incorrect API behaviour (as opposed to a mistake in the test itself).

## 7. Entry & Exit Criteria

**Entry (start testing when all true):**
- Base URL is reachable (`GET /ping` returns `201`).
- Valid test credentials are available for `/auth`.
- Test cases for the in-scope features are written and reviewed.

**Exit (stop testing when all true):**
- 100% of in-scope test cases have been executed.
- No open defect of **Critical** or **High** severity remains.
- A traceability matrix shows every in-scope feature maps to at least one executed test case.

## 8. Suspension & Resumption Criteria

**Suspend** testing if the base URL is unreachable or `/auth` stops issuing tokens (blocks the majority of cases). **Resume** once `GET /ping` returns `201` and a fresh token can be obtained, re-running any case interrupted mid-execution.

## 9. Test Deliverables

- This test plan (`test-plan.md`).
- Test cases (`test-cases.md`).
- Requirements traceability matrix (`traceability-matrix.md`).
- Bug report template (`bug-report-template.md`) and any filed defects.

## 10. Test Environment

| Element | Value |
|---------|-------|
| Target | Restful-Booker (public hosted instance) |
| Base URL | https://restful-booker.herokuapp.com |
| Protocol | HTTPS, JSON request/response |
| Auth | Token from `POST /auth`, sent as `Cookie: token=<token>` |
| Tooling | Manual design now; Postman (Mod 2), pytest + requests (Mod 3) later |

## 11. Risks & Contingencies

| Risk | Likelihood | Impact | Contingency |
|------|-----------|--------|-------------|
| Shared public instance — data created by others / reset periodically | High | Medium | Tests create their own data and assert on their own IDs; never assume a fixed dataset |
| Heroku free-tier cold start / downtime | Medium | High | `/ping` gate before runs; suspend per §8 if down |
| Known intentional defects in Restful-Booker | Medium | Low | Treated as findings, documented in bug reports — they're learning fuel, not blockers |
| Token expiry mid-run | Low | Medium | Re-authenticate and retry the affected case |

## 12. Approvals

| Role | Name | Status |
|------|------|--------|
| QA Engineer / Author | Oleh | Draft for review |
| Mentor review | Claude (senior QA) | Pending |
