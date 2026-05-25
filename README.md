# QA Skill Lab

A structured portfolio demonstrating QA engineering skills — from test documentation through API automation, Python pytest, and end-to-end testing with Playwright.

**Target API:** [Restful-Booker](https://restful-booker.herokuapp.com/apidoc/index.html) — a public hotel booking REST API used as the primary system under test across all modules.

---

## Modules

### ✅ 01 — Test Documentation
Professional QA documentation following IEEE 829 and ISTQB terminology.

- Test plan with scope, risk analysis, entry/exit criteria
- 14 test cases covering the full booking lifecycle (positive, negative, boundary)
- Requirements traceability matrix (100% feature coverage)
- Bug report template + filed defect (BUG-RB-001)

→ [View module](01-documentation/README.md)

---

### 🔄 02 — API Testing with Postman
*(In progress)*

Postman collection with environment variables, `pm.test()` assertions, and Newman CLI runner. Test cases from Module 1 executed and results recorded.

---

### ⏳ 03 — Python Automation (pytest + requests)
*(Pending)*

Same Restful-Booker endpoints reimplemented in pytest. Fixtures for auth and booking lifecycle. Meaningful assertions — not just status codes.

---

### ⏳ 04 — End-to-End Testing (Playwright)
*(Pending)*

Playwright with Python bindings, Page Object Model.

---

### ⏳ 05 — Smoke Tests
*(Pending)*

Fast critical-path suite curated from Modules 3 & 4. Runs on every push via GitHub Actions.

---

## Skills demonstrated

| Skill | Module |
|-------|--------|
| Test plan writing (IEEE 829) | 01 |
| Test case design (EP, BVA, positive/negative) | 01 |
| Requirements traceability | 01 |
| Defect reporting (severity/priority classification) | 01 |
| API testing + assertion depth | 02 |
| Postman environments + pre-request scripts | 02 |
| Newman CLI + CI integration | 02 |
| Python pytest + requests | 03 |
| Fixtures and test lifecycle management | 03 |
| Page Object Model | 04 |
| Smoke testing + CI pipeline | 05 |

## Tooling

- Python 3, pytest, requests, playwright, python-dotenv
- Postman (v2.1 collections), Newman
- GitHub Actions for CI
- ruff for linting
