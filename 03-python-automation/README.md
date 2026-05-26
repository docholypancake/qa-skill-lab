# Module 03 — Python Automation (pytest + requests)

## What's tested

All 14 Restful-Booker test cases reimplemented in Python using pytest and requests. Same domain as Module 2 — new language is the only variable.

## Structure

```
03-python-automation/
├── .env                  # Local config (gitignored) — BASE_URL, USERNAME, PASSWORD
├── .venv/                # Virtual environment (gitignored)
├── pytest.ini            # Tells pytest where to find tests
├── requirements.txt      # Pinned dependencies
└── tests/
    ├── conftest.py       # Shared fixtures: base_url, auth_token, booking (with teardown)
    ├── test_health.py    # TC-RB-003 — GET /ping
    ├── test_auth.py      # TC-RB-002, TC-RB-004 — POST /auth
    ├── test_booking.py   # TC-RB-001, 005, 006, 007, 008, 009, 010, 011, 012
    └── test_defects.py   # TC-RB-013, TC-RB-014 — xfail defect documentation
```

## How to run

```bash
# From repo root, with venv active
cd ~/Documents/GitHub/qa-skill-lab
source 03-python-automation/.venv/bin/activate

# Full suite
pytest 03-python-automation/tests/ -v

# Single file
pytest 03-python-automation/tests/test_booking.py -v
```

## Expected results

```
14 passed, 2 xfailed
```

| Result | Count | Meaning |
|--------|-------|---------|
| passed | 14 | All happy-path and auth/negative tests |
| xfailed | 2 | TC-013, TC-014 — known defects, expected to fail |

## Key patterns demonstrated

**Fixtures with teardown (`yield`)** — `booking` fixture creates a booking before each test, hands the ID to the test via `yield`, then deletes it after — regardless of whether the test passed or failed. No manual ordering required.

**Fixture scopes** — `base_url` and `auth_token` are `session`-scoped (run once per suite). `ping_response` is `module`-scoped (once per file). `booking` is `function`-scoped (fresh booking per test).

**Fixture injection** — fixtures declare other fixtures as parameters. `auth_token` takes `base_url`; `booking` takes both `base_url` and `auth_token`. pytest resolves the dependency graph automatically.

**`xfail` for defect documentation** — TC-013 (negative totalprice) and TC-014 (missing firstname) are marked `@pytest.mark.xfail`. They assert the correct behaviour (400), fail because the API is broken, and surface as `x` rather than `FAILED` — keeping the suite green while documenting known defects.

## QA skills demonstrated

- pytest fixture lifecycle (setup, yield, teardown)
- Fixture scoping to control HTTP call frequency
- Fixture dependency injection
- Meaningful assertions: status code + response shape + field values
- `xfail` for living defect documentation
- Virtual environment and `requirements.txt` for reproducible runs
