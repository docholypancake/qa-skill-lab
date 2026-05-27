# Module 06 — Advanced API Testing (Python)

## What this is

Three advanced API testing techniques applied to the Restful-Booker API, all in Python + pytest. These go beyond "does the endpoint return 200?" into data-driven coverage, contract validation, and performance gates.

## Techniques covered

### 1. Data-driven testing (`test_parametrize.py`)

`@pytest.mark.parametrize` runs one test function with multiple input rows. Each row becomes a separate test with its own ID and result — no duplicated test functions.

**What's tested:**
- 4 valid booking payloads: standard, zero price (boundary), max-length fields, unicode names
- 4 filter combinations on `GET /booking`: by name, checkin, checkout, date range
- 3 invalid payloads (missing required fields) — marked `xfail` to document Restful-Booker's absent input validation

### 2. Schema validation (`test_schema.py`)

`jsonschema.validate()` checks that a response body matches a declared schema. Catches type regressions, missing fields, and structural changes that functional tests miss entirely.

**Schema defined in:** `schemas/booking.json`

**What's tested:**
- `POST /booking` → `booking` object matches schema (types, required fields, date format)
- `GET /booking/{id}` → booking object matches schema
- `GET /booking` list → every item has `bookingid` as integer ≥ 1
- Intentional failure: `totalprice` as string → `ValidationError` raised (proves schema catches type regressions)
- Intentional failure: `bookingdates` missing → `ValidationError` raised (proves schema catches missing required fields)

### 3. Response time assertions (`test_performance.py`)

`response.elapsed.total_seconds()` measures server response time. Asserting against a threshold makes slow responses a test failure, not a helpdesk ticket.

**SLA thresholds:**

| Endpoint | Threshold |
|----------|-----------|
| `GET /ping` | < 1.0s |
| `GET /booking` (list) | < 2.0s |
| `GET /booking/{id}` | < 2.0s |
| `POST /booking` | < 3.0s |
| `DELETE /booking/{id}` | < 3.0s |

All timing tests are marked `@pytest.mark.slow` — exclude them on flaky networks with `-m "not slow"`.

## How to run

```bash
# From repo root — use the shared venv from module 03
source 03-python-automation/.venv/bin/activate

# Install the one new dependency
pip install jsonschema

# Run all module 06 tests
cd 06-advanced-api && pytest tests/ -v

# Skip slow timing tests
pytest tests/ -v -m "not slow"

# Run only parametrize tests
pytest tests/test_parametrize.py -v

# Run only schema tests
pytest tests/test_schema.py -v
```

## What intentional failures look like

```
XFAIL tests/test_parametrize.py::test_create_booking_rejects_invalid_payloads[missing_firstname]
XFAIL tests/test_parametrize.py::test_create_booking_rejects_invalid_payloads[missing_totalprice]
XFAIL tests/test_parametrize.py::test_create_booking_rejects_invalid_payloads[missing_bookingdates]
```

`xfail` = we expected failure and got it. The API returns 200 for invalid payloads; that's the documented defect.

```
PASSED tests/test_schema.py::test_schema_catches_wrong_type
PASSED tests/test_schema.py::test_schema_catches_missing_required_field
```

These pass because `ValidationError` was correctly raised — the schema is enforcing the contract as expected.

## QA skills demonstrated

- **Data-driven testing** — `@pytest.mark.parametrize` for systematic edge case and boundary coverage without code duplication
- **Contract testing** — JSON Schema validation catches structural regressions that status-code checks miss
- **Performance SLA gates** — `response.elapsed` assertions surface timing regressions in CI
- **Boundary value analysis** — zero price, single-character names, 100-character strings, same-day checkin/checkout
- **Defect documentation** — `xfail` markers quantify missing input validation (3 endpoints, 3 confirmed gaps)
- **Test isolation** — every test that creates data cleans up after itself via fixture teardown or inline delete
