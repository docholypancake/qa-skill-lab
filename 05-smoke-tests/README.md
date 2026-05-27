# Module 05 — Smoke Tests

## What this is

A fast, critical-path suite that runs on **every push** to any branch. Not a new test file — a curated selection of existing tests from Modules 3 and 4, identified by the `@pytest.mark.smoke` marker.

Answers one question: **is the system alive?**

## Smoke tests selected

| ID | Test | Module | What it catches |
|----|------|--------|----------------|
| TC-RB-003 | `test_ping_returns_201` | 03 | API unreachable or server down |
| TC-RB-004 | `test_valid_token_is_string` | 03 | Auth service broken |
| TC-RB-001 | `test_create_booking_returns_id` | 03 | Core write path broken |
| TC-E2E-001 | `test_homepage_loads` | 04 | UI unreachable or blank page |
| TC-E2E-002 | `test_rooms_are_displayed` | 04 | React hydration / API connection failed |

## How to run

```bash
# From repo root — activate the shared venv first
source 03-python-automation/.venv/bin/activate

# Run smoke suite: stop on first failure (-x), all smoke-marked tests
pytest -m smoke -x -v
```

`-x` stops on the first failure. Smoke tests are meant to fail fast — if the API is down you don't need to wait for five failures to know something is wrong.

## How to run individual modules normally

```bash
# Module 03 only (all tests)
cd 03-python-automation && pytest tests/ -v

# Module 04 only (all tests)
cd 04-e2e-playwright && pytest tests/ -v
```

## CI behaviour

The smoke workflow (`.github/workflows/05-smoke.yml`) triggers on every push to any branch. Module workflows (03, 04) trigger only when files in their folder change.

## QA skills demonstrated

- **Marker-based test selection** — `@pytest.mark.smoke` tags tests without duplicating them
- **Cross-module collection** — root `pytest.ini` collects from both `03-python-automation/tests` and `04-e2e-playwright/tests` in one run
- **Fail-fast strategy** — `-x` stops at first failure; smoke tests surface blockers immediately
- **CI pipeline design** — separate triggers for smoke (every push) vs. full regression (path-filtered)
