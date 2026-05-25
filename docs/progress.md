# Progress — QA Skill Lab

## Module 01 — Test Documentation ✅ Complete

- [x] Test plan (`test-plan.md`) — RB-TP-001, IEEE 829 structure
- [x] Test cases (`test-cases.md`) — 14 cases, full booking lifecycle
- [x] Traceability matrix (`traceability-matrix.md`) — 100% feature coverage
- [x] Bug report template (`bug-report-template.md`)
- [x] Defect filed (`BUG-RB-001.md`) — `POST /auth` returns 200 for bad credentials
- [x] Module README (`01-documentation/README.md`)
- [x] Reflection note (`docs/reflection-01.md`)
- [ ] Manual execution of test cases (deferred — Module 2 Postman will execute and record results)

**Skills demonstrated:** test plan writing, test case design (equivalence partitioning, BVA), assertion depth, RTM, defect reporting, severity/priority classification.

---

## Module 02 — API Testing with Postman 🔄 In progress

- [x] "booking" collection created in Postman
- [x] `GET /ping` request added and executed
- [x] `POST /auth` (invalid credentials) added and executed
- [ ] Postman environment set up (`base_url`, `token`, `booking_id` variables)
- [ ] All TC-RB-001 → TC-RB-014 implemented as requests with `pm.test()` assertions
- [ ] Pre-request script for auth token (auto-fetch before protected requests)
- [ ] Collection exported as v2.1 JSON and committed to `02-api-postman/`
- [ ] Newman CLI run documented
- [ ] Module README
- [ ] Reflection note

---

## Module 03 — Python Automation (pytest + requests) ⏳ Pending

- [ ] Virtual environment set up
- [ ] `requirements.txt` (pytest, requests, python-dotenv)
- [ ] Same endpoints as Module 2 reimplemented in pytest
- [ ] Fixtures for auth token and booking lifecycle
- [ ] Module README
- [ ] Reflection note
- [ ] GitHub Actions workflow

---

## Module 04 — E2E Testing (Playwright) ⏳ Pending

- [ ] Playwright installed (Python bindings)
- [ ] Page Object Model implemented
- [ ] E2E suite against a UI target (TBD)
- [ ] Module README
- [ ] Reflection note
- [ ] GitHub Actions workflow

---

## Module 05 — Smoke Tests ⏳ Pending

- [ ] Critical-path subset curated from Modules 3 & 4
- [ ] Fast, CI-first suite
- [ ] Module README
- [ ] Reflection note
- [ ] GitHub Actions workflow — triggers on every push

---

## Cross-cutting

- [ ] Top-level `README.md` — portfolio landing page (updated after each module ships)
- [ ] GitHub repo created and public
- [ ] Initial commit pushed
