# Reflection — Module 01: Test Documentation

**Date completed:** 2026-05-25
**Module:** 01-documentation
**Time invested:** ~2 sessions

## What I built

A complete documentation suite for the Restful-Booker API:
- Test plan (IEEE 829 structure)
- 14 test cases covering the full booking lifecycle
- Requirements traceability matrix (100% feature coverage)
- Bug report template + one filed defect (BUG-RB-001)

## What clicked

**Assertions have layers.** Before this module I would have written "status is 200" and called it a test. Now I write three layers: status code (did it respond?), response shape (did it return the right fields?), business rule (did it actually do what it was supposed to?). The third layer is the one that catches real bugs.

**Severity ≠ Priority.** These felt like synonyms before. They're not. A broken admin endpoint can be High severity (the functionality is completely broken) and Low priority (nobody uses it this week). A cosmetic bug on the login page is the reverse. The axes are independent — I have to think about both separately.

**The RTM isn't busywork.** Writing test cases and then mapping them to features immediately showed me where I had zero coverage. Seeing "❌ No test" for DELETE and all the auth-guard cases made it obvious what was missing, without anyone having to tell me. The matrix makes gaps visible.

**Preconditions are test design.** TC-RB-003 (health check) has no preconditions — everything else depends on it. Documenting the dependency chain forces you to think about execution order and what "independent" really means in practice.

**Intentional failure cases are honest.** TC-RB-013 and TC-RB-014 are expected to fail. Including them is more useful than hiding them — they document the API's actual behaviour and show what a defect surfacing looks like.

## What was hard

Distinguishing what belongs in "test data" vs. "steps" vs. "preconditions" took a few iterations. The rule I settled on: preconditions = state that must exist before step 1; test data = the input the test itself supplies; steps = the actions in order.

## Open questions going into Module 2

- TC-RB-013 and TC-RB-014: what does Restful-Booker actually return? The actual result is marked as "known" but not verified live. Postman will confirm.
- TC-RB-011 (delete): the API docs say it returns `201 Created` on delete — that's unusual. Needs live verification.
- Token expiry: TC-RB-004 produces a token. How long does it last? Does it matter for the test session?

## What I'd do differently

Start the RTM at the same time as the test plan, not after the test cases. Writing the feature rows first and leaving them empty would have made the gaps visible earlier and given me a checklist to write against.
