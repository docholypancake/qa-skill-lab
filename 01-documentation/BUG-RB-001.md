# Bug Report

| Field           | Value                             |
| --------------- | --------------------------------- |
| **Bug ID**      | BUG-RB-001                        |
| **Title**       | POST /auth 200 with invalid creds |
| **Reported by** | Oleh Blazhko                      |
| **Date**        | May 25, 2026                      |
| **Status**      | New                               |

---

## Classification

| Field                   | Value                |
| ----------------------- | -------------------- |
| **Severity**            | Medium               |
| **Priority**            | Medium               |
| **Type**                | Security, Functional |
| **Affected endpoint**   | /auth                |
| **Traces to test case** | TC-RB-002            |

---

## Environment

| Field                   | Value                                |
| ----------------------- | ------------------------------------ |
| **Base URL**            | https://restful-booker.herokuapp.com |
| **Tested via**          | curl                                 |
| **Date of observation** | May 24, 2026                         |

---

## Steps to Reproduce

1. Send `POST https://restful-booker.herokuapp.com/auth` with header `Content-Type: application/json` and body `{"username": "invalid", "password": "creds"}`.
2. Capture the HTTP response status code.
3. Capture the response body and confirm no `token` field is present.

---

## Expected Result

Status code is `401 Unauthorized`. Response body contains no `token` field.

---

## Actual Result

```
HTTP/1.1 200 OK
Body: {"reason": "Bad credentials"}
```

---

## Evidence

```
Request:
POST /auth
Content-Type: application/json

{
	"username": "invalid",
	"password": "creds"
}

Response:
HTTP 200 OK
{
    "reason": "Bad credentials"
}
```

---

## Impact

Any client that branches on HTTP status code alone (e.g. `if status == 200: proceed`) will treat a failed login as a success. The `reason` field in the body is the only signal that auth failed — clients must parse the body to detect failure, which violates the HTTP contract.

---

## Notes / Workaround

Workaround: callers must inspect the response body for the absence of a `token` field to detect auth failure. TC-RB-002 documents this as the tested behaviour. Restful-Booker is a deliberately imperfect practice API; this defect is intentional on the vendor's part and will not be fixed.
