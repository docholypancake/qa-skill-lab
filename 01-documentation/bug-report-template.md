# Bug Report

| Field | Value |
|-------|-------|
| **Bug ID** | BUG-RB-### |
| **Title** | _One line: what breaks, where_ |
| **Reported by** | |
| **Date** | |
| **Status** | New |

---

## Classification

| Field | Value |
|-------|-------|
| **Severity** | Critical / High / Medium / Low |
| **Priority** | High / Medium / Low |
| **Type** | Functional / Security / Performance / UI / Other |
| **Affected endpoint** | |
| **Traces to test case** | TC-RB-### |

> **Severity vs. Priority reminder:**
> Severity = how bad is the break (impact on functionality).
> Priority = how urgently must it be fixed (business/user impact).
> They are independent. A broken admin-only feature can be High severity, Low priority. A typo on the homepage can be Low severity, High priority.

---

## Environment

| Field                   | Value                                |
| ----------------------- | ------------------------------------ |
| **Base URL**            | https://restful-booker.herokuapp.com |
| **Tested via**          | Postman / curl / pytest              |
| **Date of observation** |                                      |

---

## Steps to Reproduce

_Must be atomic — a dev with no context must reach the same failure cold._

1.
2.
3.

---

## Expected Result

_What the API should do according to the spec, HTTP standards, or reasonable contract._

---

## Actual Result

_What the API actually does. Quote exact status code and response body._

```
HTTP/1.1 ???
Body: ???
```

---

## Evidence

_Paste request + response, screenshot, or link to test case output._

```
Request:
POST /???
Content-Type: application/json

{ }

Response:
HTTP ???
{ }
```

---

## Impact

_Who or what is affected if this stays unfixed. One or two sentences._

---

## Notes / Workaround

_Any known workaround. Leave blank if none._
