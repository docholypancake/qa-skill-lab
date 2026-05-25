# Requirements Traceability Matrix — Restful-Booker API

| Field | Value |
|-------|-------|
| **Document ID** | RB-RTM-001 |
| **Version** | 1.0 (complete — all 14 test cases written) |
| **Traces to test plan** | RB-TP-001 |
| **Author** | Oleh |
| **Date** | 2026-05-25 |

> **What this is:** a bidirectional map between in-scope features (from §3 of the test plan) and test cases. A ✅ cell means at least one test covers that feature+type combination.
>
> **Why it matters:** at the exit-criteria checkpoint in §7 of the test plan, every in-scope feature must map to at least one executed test case. All gaps are now closed at the written stage; execution status is tracked separately.

---

## Feature × Test Case Map

| Req ID | Feature | Endpoint | Test Type | TC-001 | TC-002 | TC-003 | TC-004 | TC-005 | TC-006 | TC-007 | TC-008 | TC-009 | TC-010 | TC-011 | TC-012 | TC-013 | TC-014 | Coverage |
|--------|---------|----------|-----------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|----------|
| RB-F-01 | Health check | `GET /ping` | Positive | | | ✅ | | | | | | | | | | | | ✅ Covered |
| RB-F-02 | Auth — valid credentials | `POST /auth` | Positive | | | | ✅ | | | | | | | | | | | ✅ Covered |
| RB-F-03 | Auth — invalid credentials | `POST /auth` | Negative | | ✅ | | | | | | | | | | | | | ✅ Covered |
| RB-F-04 | Create booking — valid data | `POST /booking` | Positive | ✅ | | | | | | | | | | | | | | ✅ Covered |
| RB-F-05 | Create booking — missing required field | `POST /booking` | Negative | | | | | | | | | | | | | | ✅ | ✅ Covered |
| RB-F-06 | Read booking by ID | `GET /booking/:id` | Positive | | | | | ✅ | | | | | | | | | | ✅ Covered |
| RB-F-07 | List bookings (all + filtered) | `GET /booking` | Positive | | | | | | ✅ | | | | | | | | | ✅ Covered |
| RB-F-08 | Full update | `PUT /booking/:id` | Positive | | | | | | | ✅ | | | | | | | | ✅ Covered |
| RB-F-09 | Full update — no/invalid token | `PUT /booking/:id` | Negative | | | | | | | | ✅ | | | | | | | ✅ Covered |
| RB-F-10 | Partial update | `PATCH /booking/:id` | Positive | | | | | | | | | ✅ | | | | | | ✅ Covered |
| RB-F-11 | Partial update — no/invalid token | `PATCH /booking/:id` | Negative | | | | | | | | | | ✅ | | | | | ✅ Covered |
| RB-F-12 | Delete booking | `DELETE /booking/:id` | Positive | | | | | | | | | | | ✅ | | | | ✅ Covered |
| RB-F-13 | Delete booking — no/invalid token | `DELETE /booking/:id` | Negative | | | | | | | | | | | | ✅ | | | ✅ Covered |
| RB-F-14 | Input handling — boundary/invalid data | Various | Negative | | | | | | | | | | | | | ✅ | | ✅ Covered |

---

## Reverse Map — Test Case → Features

| Test Case | Title | Features Covered |
|-----------|-------|-----------------|
| TC-RB-001 | Create booking with valid data | RB-F-04 |
| TC-RB-002 | Authenticate with invalid credentials | RB-F-03 |
| TC-RB-003 | Health check | RB-F-01 |
| TC-RB-004 | Authenticate with valid credentials | RB-F-02 |
| TC-RB-005 | Read a booking by ID | RB-F-06 |
| TC-RB-006 | List bookings with a filter | RB-F-07 |
| TC-RB-007 | Full update of a booking (PUT) | RB-F-08 |
| TC-RB-008 | Full update rejected without valid token | RB-F-09 |
| TC-RB-009 | Partial update of a booking (PATCH) | RB-F-10 |
| TC-RB-010 | Partial update rejected without valid token | RB-F-11 |
| TC-RB-011 | Delete a booking | RB-F-12 |
| TC-RB-012 | Delete rejected without valid token | RB-F-13 |
| TC-RB-013 | Input handling: boundary value (negative totalprice) | RB-F-14 |
| TC-RB-014 | Create booking with missing required field | RB-F-05 |

---

## Coverage Summary

| Metric | Value |
|--------|-------|
| Total in-scope features | 14 |
| Features with ≥ 1 test case | 14 |
| **Coverage (%)** | **100%** |
| Test cases written | 14 |
| Test cases executed | 0 (manual execution pending — Module 2 Postman will execute and record results) |
| Intentional failure cases | 2 (TC-RB-013, TC-RB-014 — known Restful-Booker defects) |

---

## Version History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1 | 2026-05-24 | Oleh | Initial draft — 2 cases mapped, gaps identified |
| 0.2 | 2026-05-24 | Oleh + Claude | TC-RB-003/004 added; coverage 14% → 29% |
| 0.3 | 2026-05-24 | Claude | TC-RB-005 added; coverage 29% → 36% |
| 1.0 | 2026-05-25 | Claude | TC-RB-006 through TC-RB-014 added; coverage 36% → 100% |
