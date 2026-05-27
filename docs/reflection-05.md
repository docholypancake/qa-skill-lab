# Reflection — Module 05: Smoke Tests

## What we built

A fast, critical-path suite that runs on every push to any branch. Not a separate test file — a curated selection of existing tests from Modules 03 and 04, selected via `@pytest.mark.smoke`.

Five tests total:
- `test_ping_returns_201` — API server reachable
- `test_valid_token_is_string` — auth service works
- `test_create_booking_returns_id` — core write path works
- `test_homepage_loads` — UI reachable and renders real content
- `test_rooms_are_displayed` — React hydration and API connection working

## Key lessons

### Markers are the right tool for smoke selection

The alternative was copying tests into a `05-smoke-tests/` folder. That creates duplication: two copies of the same test to maintain, potential drift, and confusion about which is canonical. Markers let you *tag* tests where they live and collect them from multiple modules in one run. No duplication.

The `@pytest.mark.smoke` decorator costs one line per test. The root `pytest.ini` makes the marker official (suppresses the warning) and configures `testpaths` to collect from both module folders.

### `requests` has no default timeout

This was the hardest bug of the module. The smoke suite appeared to hang indefinitely on `test_valid_token_is_string`. The real cause was `requests.post()` with no `timeout` argument — it waits forever for a response that was stalled due to a Heroku cold start.

Fix: define a module-level `TIMEOUT = 10` constant and pass `timeout=TIMEOUT` to every `requests` call. This makes failures fast and explicit rather than silent hangs.

### Heroku free tier cold starts are real

Restful-Booker runs on Heroku's free (or low) tier. Dynos spin down after inactivity. The first request after a sleep period can take 60–90 seconds. This is not a test bug — it's infrastructure behaviour. The `requests` timeout doesn't prevent this; it just surfaces it as a clear `ConnectionError` or `Timeout` rather than an infinite hang. In CI this isn't an issue (fresh environment, no cold state), but locally you may need to wake the dyno manually first.

### Fail-fast is deliberate design

`pytest -m smoke -x` stops at the first failure. This is intentional: if the API is down, there's no point running the UI tests. Smoke tests answer a binary question — is the system alive? — and you want the answer immediately.

### CI trigger strategy

Smoke workflow triggers on every push to any branch. Module workflows (03, 04) trigger only when files in their folder change. This means:
- Every push gets a fast sanity check (smoke, ~30–60s)
- Full regression only reruns when relevant code changes

This is a common CI design pattern: fast gates on every commit, slow gates on relevant changes.

## What I would do differently

The `requests` timeout should have been there from the start of Module 03. Any network call without a timeout is a latent bug. Going forward: always set a timeout.

## Open questions

- Could we add a retry on the smoke suite for Heroku cold-start flakiness? (Yes — `pytest-rerunfailures` plugin, `--reruns 2 --reruns-delay 5`)
- Should smoke tests also cover the E2E booking flow? (Probably not — that test is slower and more fragile; smoke should be the fastest possible check)
