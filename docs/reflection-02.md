# Reflection — Module 02: API Testing with Postman

## What I built

A Postman collection executing all 14 Restful-Booker test cases with meaningful assertions, environment variables, data chaining between requests, and Newman CLI integration.

## What I learned

**Environment variables are not just convenience.** `{{base_url}}`, `{{token}}`, `{{booking_id}}` make the collection portable — swap one environment file and the entire suite runs against a different target. Hardcoded URLs and IDs in requests are a maintainability trap.

**Data chaining is a first-class concern.** TC-RB-001 creates a booking and saves its ID with `pm.environment.set("booking_id", ...)`. TC-RB-004 saves the auth token the same way. Every request that follows reads these values from the environment. This is the Postman equivalent of pytest fixtures — shared setup state that flows through the suite.

**Order is a test design decision, not an afterthought.** TC-RB-011 (DELETE) must be last because it destroys `booking_id`. TC-RB-004 must precede any authenticated request. Ignoring order produces flaky tests — pass sometimes, fail others depending on what ran before.

**Assertion depth catches what status codes miss.** Asserting `200 OK` alone is noise. The meaningful assertions were:
- Shape: does the response have all expected fields?
- Value: do field values match the payload we sent?
- Side-effect: does `tc-006` confirm that `tc-001`'s bookingid appears in the listing?
- Negative: does `tc-002`'s body have `reason` but NOT `token`?

**Intentional failures surface real bugs.** TC-RB-014 was written expecting a 400. Newman reported 500 — a server crash on missing `firstname`. The test was right; the API is broken in a worse way than anticipated. A test that "fails correctly" is doing its job.

## Surprises

TC-RB-014 returned 500 Internal Server Error, not 200. That upgrades the defect from "input validation gap" (Medium) to "unhandled exception on malformed input" (High). A missing field should never crash a server — it should be caught and rejected cleanly.

## What carries forward to Module 3

The same 14 test cases get reimplemented in pytest + requests. The Postman collection becomes a reference — I already know the expected response shapes, which fields to assert, and what the intentional failures look like. Module 3 introduces the same concepts in Python: fixtures replace environment variables, teardown replaces manual ordering, and `assert` replaces `pm.expect`.
