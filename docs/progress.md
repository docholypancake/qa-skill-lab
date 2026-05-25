# Progress — QA Skill Lab

## Module 01 — Test Documentation ✅ Complete

- [x] Test plan (`test-plan.md`) — RB-TP-001, IEEE 829 structure
- [x] Test cases (`test-cases.md`) — 14 cases, full booking lifecycle
- [x] Traceability matrix (`traceability-matrix.md`) — 100% feature coverage
- [x] Bug report template (`bug-report-template.md`)
- [x] Defect filed (`BUG-RB-001.md`) — `POST /auth` returns 200 for bad credentials
- [x] Module README (`01-documentation/README.md`)
- [x] Reflection note (`docs/reflection-01.md`)
- [x] Manual execution of test cases — executed via Postman Collection Runner (Module 2)

**Skills demonstrated:** test plan writing, test case design (equivalence partitioning, BVA), assertion depth, RTM, defect reporting, severity/priority classification.

---

## Module 02 — API Testing with Postman ✅ Complete

- [x] "Booker" collection created in Postman
- [x] Postman environment set up (`base_url`, `token`, `booking_id` variables)
- [x] All TC-RB-001 → TC-RB-014 implemented as requests with `pm.test()` assertions
- [x] Data chaining: TC-RB-001 saves `booking_id`, TC-RB-004 saves `token` via `pm.environment.set()`
- [x] Collection run: 28 assertions, 26 pass, 2 intentional defect failures (TC-013, TC-014)
- [x] Bonus finding: TC-RB-014 returns 500 (server crash) — severity upgraded to High
- [x] Collection exported as v2.1 JSON → committed to `02-api-postman/`
- [x] Newman CLI run verified (same 26/28 result, 3.9s total)
- [x] Module README (`02-api-postman/README.md`)
- [x] Reflection note (`docs/reflection-02.md`)

**Skills demonstrated:** Postman environments, data chaining, assertion depth, dependency ordering, Newman CLI, intentional failure documentation.

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

- [x] Top-level `README.md` — portfolio landing page (updated after each module ships)
- [x] GitHub repo created and public — https://github.com/docholypancake/qa-skill-lab
- [x] Initial commit pushed
