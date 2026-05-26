# Reflection — Module 03: Python Automation (pytest + requests)

## What I built

A pytest suite covering all 14 Restful-Booker test cases in Python. Four test files, a shared conftest.py with three fixtures, and xfail markers for known defects.

## What I learned

**Fixtures replace manual ordering.** In Postman, I had to run TC-011 (DELETE) last to avoid destroying the booking_id. In pytest, the `booking` fixture handles create and delete automatically around each test. Order no longer matters — the test just asks for a `booking` and gets a fresh one every time.

**`yield` is the key to teardown.** Code before `yield` runs before the test. Code after runs after — even if the test fails. This is how you guarantee cleanup. Without teardown, every failed test would leave junk data in the API.

**Fixture scoping is a performance decision.** Auth token: session scope — one network call per suite run. Booking: function scope — one per test, because each test needs its own isolated resource. Getting scope wrong either wastes calls (too narrow) or causes test interference (too wide).

**Fixtures compose.** `booking` depends on `base_url` and `auth_token`. pytest builds the dependency graph and resolves it. I didn't have to think about order — I just declared what I needed.

**`xfail` is better than a comment.** In Module 2, I flagged TC-013 and TC-014 with `[DEFECT]` in the test name. In pytest, `@pytest.mark.xfail` is machine-readable — CI can count expected failures separately, and an unexpected pass (`X`) is a signal that the defect was silently fixed.

## Mistakes made

- Forgot auth header on `booking` fixture teardown DELETE — got 403, booking leaked. Fixed by adding `auth_token` parameter to the fixture.
- Tried `assert booking in response.json()` on the list endpoint — response is `[{"bookingid": 77}, ...]`, not a list of ints. Fixed with list comprehension: `[b["bookingid"] for b in response.json()]`.

## What carries forward to Module 4

Module 4 is Playwright E2E. The pytest patterns are identical — same fixtures, same `yield` teardown, same conftest.py structure. The only new thing is the browser layer replacing the `requests` HTTP layer. Python fluency from this module means Playwright's API is the only variable.
