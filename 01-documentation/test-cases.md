# Test Cases — Restful-Booker API

Traces to **RB-TP-001**. Each case is atomic, independent, and maps to one in-scope feature so the traceability matrix can link them. Expected results are defined *before* execution — that is what makes a test a test, not an exploration.

**ID scheme:** `TC-RB-###` · **Base URL:** `https://restful-booker.herokuapp.com`

---

## TC-RB-001 — Create a booking with valid data

| Field             | Value                                     |
| ----------------- | ----------------------------------------- |
| **Test Case ID**  | TC-RB-001                                 |
| **Feature**       | Create (`POST /booking`)                  |
| **Type**          | Positive / Functional                     |
| **Priority**      | High                                      |
| **Preconditions** | API reachable — `GET /ping` returns `201` |

**Test data**

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

**Steps**

1. Send `POST /booking` with the test data as the JSON body.
2. Set request headers `Content-Type: application/json` and `Accept: application/json`.
3. Capture the response status and body.

**Expected result**

1. Status code is `200 OK`.
2. Response body contains a `bookingid` that is an integer greater than 0. *(response shape)*
3. Response body `booking` object equals the submitted payload field-for-field — `firstname`, `lastname`, `totalprice`, `depositpaid`, both `bookingdates`, and `additionalneeds` all match what was sent. *(business rule — the server stored what we gave it)*

**Postconditions**

A booking now exists with the returned `bookingid`. It should be removed in teardown (`DELETE /booking/:id`) so the test leaves no residue.

> **Why this case matters:** it demonstrates the module's core assertion principle — status code *and* response shape *and* business rule. Asserting only `200 OK` would pass even if the API silently dropped every field we sent.

---

## TC-RB-002 — authenticate with invalid credentials.

| Field             | Value                                     |
| ----------------- | ----------------------------------------- |
| **Test Case ID**  | TC-RB-002                                 |
| **Feature**       | Auth (POST /auth)                         |
| **Type**          | Negative                                  |
| **Priority**      | High                                      |
| **Preconditions** | API reachable — `GET /ping` returns `201` |
**Test data**

```json
{
"username": "invalid",
"password": "creds"
}
```

**Steps**
1. Send POST /auth with the test data in the JSON body
2. Set request header `Content-Type: application/json`.
3. Capture the response status and body.

**Expected result**
1. Status code is `200 OK` — note: *not* `401 Unauthorized` (see defect note below).
2. Response body is `{"reason": "Bad credentials"}` — i.e. it contains a `reason` field. *(documented behaviour; confirm byte-for-byte in Module 2)*
3. Response body contains **no** `token` field — no usable credential is issued. *(the load-bearing negative assertion: a passing negative-auth test proves the caller cannot proceed to protected operations)*

**Postconditions**
User not authenticated, no access to tests that need auth.

> **Why this case matters:** a user must not gain authenticated access with invalid credentials. Without this check, any credentials might authenticate the caller, leaving a serious security vulnerability open.

> **Possible defect (candidate for bug report):** returning `200 OK` for a failed login — instead of `401 Unauthorized` — hides authentication failures from clients that branch on status code alone. Flagged here; to be filed properly in the bug-report step.

---
## TC-RB-003 — health check.

| Field             | Value                |
| ----------------- | -------------------- |
| **Test Case ID**  | TC-RB-003            |
| **Feature**       | Health (GET /ping)   |
| **Type**          | Functional, positive |
| **Priority**      | High                 |
| **Preconditions** | none                 |
**Test data**

```http
No request body required
```

**Steps**
1. Send GET request (ping) to https://restful-booker.herokuapp.com/ping.
2. Capture the response status and body.

**Expected result**
1. Status code is `201`
2. Response body is `Created`

**Postconditions**
If succeeded, the api is online. All other tests are possible.

> **Why this case matters:** This case is the precondition to every other case in the plan. Without the API being alive, all other tests can't be done. This tests accounts for API health.

---

## TC-RB-004 — Authenticate with valid credentials

| Field             | Value                                     |
| ----------------- | ----------------------------------------- |
| **Test Case ID**  | TC-RB-004                                 |
| **Feature**       | Auth (`POST /auth`)                       |
| **Type**          | Positive / Functional                     |
| **Priority**      | High                                      |
| **Preconditions** | API reachable — `GET /ping` returns `201` |

**Test data**

```json
{
  "username": "admin",
  "password": "password123"
}
```

**Steps**

1. Send `POST /auth` with the test data as the JSON body.
2. Set request header `Content-Type: application/json`.
3. Capture the response status and body.

**Expected result**

1. Status code is `200 OK`. *(response shape)*
2. Response body contains a `token` field. *(shape)*
3. `token` value is a non-empty string. *(business rule — a usable credential was issued)*

**Postconditions**

Token value is available for use as `Cookie: token=<token>` in any subsequent test case that requires auth (`PUT`, `PATCH`, `DELETE`).

> **Why this case matters:** valid credentials must produce a usable token — without confirming this, any test that depends on auth has an unverified precondition. Pair with TC-RB-002: together they prove the auth gate works in both directions.

---

## TC-RB-005 — Read a booking by ID

| Field             | Value                                                                     |
| ----------------- | ------------------------------------------------------------------------- |
| **Test Case ID**  | TC-RB-005                                                                 |
| **Feature**       | Read (`GET /booking/:id`)                                                 |
| **Type**          | Positive / Functional                                                     |
| **Priority**      | High                                                                      |
| **Preconditions** | API reachable — `GET /ping` returns `201`. TC-RB-001 has been executed and a `bookingid` captured from its response. |

**Test data**

No request body required. The `{id}` path parameter is the `bookingid` returned by TC-RB-001.

**Steps**

1. Send `GET /booking/{id}` where `{id}` is the `bookingid` captured from TC-RB-001.
2. Set request header `Accept: application/json`.
3. Capture the response status and body.

**Expected result**

1. Status code is `200 OK`. *(response shape)*
2. Response body contains all six booking fields: `firstname`, `lastname`, `totalprice`, `depositpaid`, `bookingdates` (with `checkin` and `checkout`), and `additionalneeds`. *(shape)*
3. Each field value matches the payload sent in TC-RB-001. *(business rule — the server returns exactly what was stored)*

**Postconditions**

No state change. Booking created in TC-RB-001 still exists; teardown (`DELETE /booking/{id}`) remains the responsibility of TC-RB-001 or the test session cleanup.

> **Why this case matters:** confirming a created resource can be retrieved by ID closes the write→read loop. A system that creates records but can't retrieve them has a critical data-access failure. This case also reuses TC-RB-001's output, demonstrating how test cases form a lifecycle chain — the same chain that becomes a fixture in Module 3 automation.

---

## TC-RB-006 — List bookings with a filter

| Field             | Value                                                                     |
| ----------------- | ------------------------------------------------------------------------- |
| **Test Case ID**  | TC-RB-006                                                                 |
| **Feature**       | Read (`GET /booking`)                                                     |
| **Type**          | Positive / Functional                                                     |
| **Priority**      | Medium                                                                    |
| **Preconditions** | API reachable — `GET /ping` returns `201`. TC-RB-001 has been executed; `bookingid` and submitted `firstname`/`lastname` values are known. |

**Test data**

No request body required. Query parameters: `?firstname=Jim&lastname=Brown` (values from TC-RB-001 payload).

**Steps**

1. Send `GET /booking?firstname=Jim&lastname=Brown`.
2. Set request header `Accept: application/json`.
3. Capture the response status and body.

**Expected result**

1. Status code is `200 OK`. *(response shape)*
2. Response body is a JSON array. *(shape)*
3. Array contains at least one object with a `bookingid` field. *(shape)*
4. The `bookingid` from TC-RB-001 is present in the array. *(business rule — the filter returns the record we created)*

**Postconditions**

No state change.

> **Why this case matters:** list + filter is a distinct code path from single-ID retrieval. A bug could affect one but not the other. Also validates that query-param filtering works, which matters for any consumer building search features on top of this API.

---

## TC-RB-007 — Full update of a booking (PUT)

| Field             | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| **Test Case ID**  | TC-RB-007                                                                          |
| **Feature**       | Update full (`PUT /booking/:id`)                                                   |
| **Type**          | Positive / Functional                                                              |
| **Priority**      | High                                                                               |
| **Preconditions** | API reachable. TC-RB-001 executed — `bookingid` known. TC-RB-004 executed — `token` known. |

**Test data**

```json
{
  "firstname": "Jane",
  "lastname": "Doe",
  "totalprice": 250,
  "depositpaid": false,
  "bookingdates": { "checkin": "2024-06-01", "checkout": "2024-06-07" },
  "additionalneeds": "Lunch"
}
```

**Steps**

1. Send `PUT /booking/{id}` where `{id}` is the `bookingid` from TC-RB-001.
2. Set headers: `Content-Type: application/json`, `Accept: application/json`, `Cookie: token=<token from TC-RB-004>`.
3. Use the test data above as the request body.
4. Capture the response status and body.
5. Send `GET /booking/{id}` and capture the response body.

**Expected result**

1. `PUT` response status is `200 OK`. *(response shape)*
2. `PUT` response body contains all six booking fields with the new values. *(shape + business rule — server echoes the update)*
3. Subsequent `GET` response body matches the updated values field-for-field. *(business rule — the change was persisted, not just echoed)*

**Postconditions**

Booking now holds updated values. If cleanup is needed, delete via TC-RB-011 pattern.

> **Why this case matters:** PUT replaces the entire resource. The two-step assertion (echo + re-fetch) is the difference between a test that proves the API stored the change versus one that only proves it returned your payload back at you.

---

## TC-RB-008 — Full update rejected without valid token (PUT)

| Field             | Value                                                    |
| ----------------- | -------------------------------------------------------- |
| **Test Case ID**  | TC-RB-008                                                |
| **Feature**       | Update full — auth guard (`PUT /booking/:id`)            |
| **Type**          | Negative / Security                                      |
| **Priority**      | High                                                     |
| **Preconditions** | API reachable. TC-RB-001 executed — `bookingid` known.   |

**Test data**

Same payload as TC-RB-007. No `Cookie` header sent.

**Steps**

1. Send `PUT /booking/{id}` with the TC-RB-007 payload but **omit** the `Cookie: token` header.
2. Set headers: `Content-Type: application/json`, `Accept: application/json`.
3. Capture the response status and body.

**Expected result**

1. Status code is `403 Forbidden`. *(business rule — unauthenticated write is refused)*
2. Booking data is **not** changed — a subsequent `GET /booking/{id}` returns original values. *(business rule — the auth guard actually blocks the write, not just returns an error)*

**Postconditions**

Booking unchanged.

> **Why this case matters:** verifying the error code is not enough — a broken auth guard could return `403` and still mutate the resource. The re-fetch assertion is the load-bearing assertion here.

---

## TC-RB-009 — Partial update of a booking (PATCH)

| Field             | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| **Test Case ID**  | TC-RB-009                                                                          |
| **Feature**       | Update partial (`PATCH /booking/:id`)                                              |
| **Type**          | Positive / Functional                                                              |
| **Priority**      | High                                                                               |
| **Preconditions** | API reachable. TC-RB-001 executed — `bookingid` and original field values known. TC-RB-004 executed — `token` known. |

**Test data**

```json
{
  "firstname": "Updated",
  "totalprice": 999
}
```

**Steps**

1. Send `PATCH /booking/{id}` with the partial payload above.
2. Set headers: `Content-Type: application/json`, `Accept: application/json`, `Cookie: token=<token from TC-RB-004>`.
3. Capture the response status and body.
4. Send `GET /booking/{id}` and capture the response body.

**Expected result**

1. `PATCH` response status is `200 OK`. *(response shape)*
2. `GET` response shows `firstname` is `"Updated"` and `totalprice` is `999`. *(business rule — patched fields changed)*
3. `GET` response shows all other fields (`lastname`, `depositpaid`, `bookingdates`, `additionalneeds`) are unchanged from TC-RB-001 values. *(business rule — PATCH must not wipe unspecified fields)*

**Postconditions**

Booking holds partially updated values.

> **Why this case matters:** PATCH semantics are distinct from PUT — only the specified fields should change. Assertion 3 is the critical one; a naive implementation might zero-out or null unspecified fields.

---

## TC-RB-010 — Partial update rejected without valid token (PATCH)

| Field             | Value                                                    |
| ----------------- | -------------------------------------------------------- |
| **Test Case ID**  | TC-RB-010                                                |
| **Feature**       | Update partial — auth guard (`PATCH /booking/:id`)       |
| **Type**          | Negative / Security                                      |
| **Priority**      | High                                                     |
| **Preconditions** | API reachable. TC-RB-001 executed — `bookingid` known.   |

**Test data**

Same partial payload as TC-RB-009. No `Cookie` header sent.

**Steps**

1. Send `PATCH /booking/{id}` with TC-RB-009 payload but **omit** the `Cookie: token` header.
2. Capture the response status and body.
3. Send `GET /booking/{id}` and confirm the resource is unchanged.

**Expected result**

1. Status code is `403 Forbidden`. *(business rule)*
2. Subsequent `GET` shows original field values — no mutation occurred. *(business rule)*

**Postconditions**

Booking unchanged.

> **Why this case matters:** same principle as TC-RB-008. The auth guard on PATCH must be independently verified — shared middleware doesn't guarantee shared enforcement.

---

## TC-RB-011 — Delete a booking

| Field             | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| **Test Case ID**  | TC-RB-011                                                                          |
| **Feature**       | Delete (`DELETE /booking/:id`)                                                     |
| **Type**          | Positive / Functional                                                              |
| **Priority**      | High                                                                               |
| **Preconditions** | API reachable. TC-RB-001 executed — `bookingid` known. TC-RB-004 executed — `token` known. |

**Test data**

No request body required. Path parameter `{id}` from TC-RB-001.

**Steps**

1. Send `DELETE /booking/{id}` with header `Cookie: token=<token from TC-RB-004>`.
2. Capture the response status.
3. Send `GET /booking/{id}` and capture the response status.

**Expected result**

1. `DELETE` response status is `201 Created`. *(Restful-Booker quirk — returns `201` not `204` on delete)*
2. Subsequent `GET /booking/{id}` returns `404 Not Found`. *(business rule — deleted resource is no longer retrievable)*

**Postconditions**

Booking is permanently removed. `bookingid` is no longer valid.

> **Why this case matters:** delete must be verified with a follow-up read. A `DELETE` that returns `201` but leaves the record in the database is a silent data-integrity failure — only the re-fetch catches it.

---

## TC-RB-012 — Delete rejected without valid token

| Field             | Value                                                    |
| ----------------- | -------------------------------------------------------- |
| **Test Case ID**  | TC-RB-012                                                |
| **Feature**       | Delete — auth guard (`DELETE /booking/:id`)              |
| **Type**          | Negative / Security                                      |
| **Priority**      | High                                                     |
| **Preconditions** | API reachable. TC-RB-001 executed — `bookingid` known.   |

**Test data**

No request body. No `Cookie` header.

**Steps**

1. Send `DELETE /booking/{id}` with **no** `Cookie: token` header.
2. Capture the response status.
3. Send `GET /booking/{id}` and confirm the booking still exists.

**Expected result**

1. Status code is `403 Forbidden`. *(business rule)*
2. Subsequent `GET /booking/{id}` returns `200 OK` with full booking body — record was not deleted. *(business rule)*

**Postconditions**

Booking unchanged and still exists.

> **Why this case matters:** completing the auth-guard triad alongside TC-RB-008 and TC-RB-010. All three protected verbs must be individually tested — one shared auth layer can be misconfigured on any individual route.

---

## TC-RB-013 — Input handling: boundary value (negative totalprice)

| Field             | Value                                     |
| ----------------- | ----------------------------------------- |
| **Test Case ID**  | TC-RB-013                                 |
| **Feature**       | Input handling (`POST /booking`)          |
| **Type**          | Negative / Boundary                       |
| **Priority**      | Medium                                    |
| **Preconditions** | API reachable — `GET /ping` returns `201` |

**Test data**

```json
{
  "firstname": "Test",
  "lastname": "User",
  "totalprice": -1,
  "depositpaid": true,
  "bookingdates": { "checkin": "2024-01-01", "checkout": "2024-01-05" },
  "additionalneeds": ""
}
```

**Steps**

1. Send `POST /booking` with the test data as the JSON body.
2. Set headers: `Content-Type: application/json`, `Accept: application/json`.
3. Capture the response status and body.

**Expected result**

1. Status code is `400 Bad Request`. *(business rule — a negative price is not a valid booking)*

**Actual result (known)**

Restful-Booker accepts the request and returns `200 OK` with a booking containing `totalprice: -1`. This is a candidate defect — the API performs no input validation on price range.

> **Why this case matters:** boundary value analysis (ISTQB test design technique) tests at the edge of valid input ranges. `totalprice = -1` is one step below the valid lower boundary of `0`. This case is listed as an intentional failure — it documents the API's lack of input validation and is the kind of finding that would generate a bug report in a production context.

---

## TC-RB-014 — Create booking with missing required field

| Field             | Value                                     |
| ----------------- | ----------------------------------------- |
| **Test Case ID**  | TC-RB-014                                 |
| **Feature**       | Create — input validation (`POST /booking`) |
| **Type**          | Negative / Functional                     |
| **Priority**      | Medium                                    |
| **Preconditions** | API reachable — `GET /ping` returns `201` |

**Test data**

```json
{
  "lastname": "Brown",
  "totalprice": 111,
  "depositpaid": true,
  "bookingdates": { "checkin": "2024-01-01", "checkout": "2024-01-05" }
}
```

`firstname` is deliberately omitted.

**Steps**

1. Send `POST /booking` with the incomplete payload above.
2. Set headers: `Content-Type: application/json`, `Accept: application/json`.
3. Capture the response status and body.

**Expected result**

1. Status code is `400 Bad Request`. *(business rule — `firstname` is a required field)*

**Actual result (known)**

Restful-Booker accepts the request and returns `200 OK` with `firstname` absent or empty in the response. Candidate defect — required-field validation is not enforced.

> **Why this case matters:** tests the API's contract enforcement. A well-behaved API rejects incomplete resources at the boundary rather than storing partial data. Like TC-RB-013, this is an intentional failure case — its value is demonstrating what a real defect surfacing looks like, which is a module requirement.