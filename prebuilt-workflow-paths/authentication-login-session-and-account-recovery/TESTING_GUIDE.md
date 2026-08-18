# Testing Guide

| # | Given | When | Expect |
|---|---|---|---|
| 1 | Active account and valid password | Login | Session is created |
| 2 | Active account and wrong password | Login | Denied and attempt recorded |
| 3 | Unknown identifier | Login | Policy-consistent response without enumeration |
| 4 | MFA-enabled account | Correct password | MFA challenge required |
| 5 | MFA challenge issued | Wrong code submitted | Denied |
| 6 | Expired MFA challenge | Code submitted | Denied |
| 7 | Consumed MFA challenge | Same code submitted again | Denied |
| 8 | No authenticated principal | Protected request | Denied |
| 9 | Expired session | Protected request | Denied |
| 10 | Pre-login session | Login succeeds | Session identity is safely rotated/bound |
| 11 | Active session | Logout | Session becomes unusable |
| 12 | Logout racing with protected request | Concurrent requests | Revocation policy is deterministic |
| 13 | Rotated refresh token | Reuse old token | Reuse is rejected |
| 14 | Recovery requested | Unknown/known identifier | Response follows enumeration policy |
| 15 | Expired recovery token | Reset submitted | Denied |
| 16 | Used recovery token | Reset submitted again | Denied |
| 17 | Token for account A | Apply to account B | Denied |
| 18 | Password changed | Old password used | Rejected according to policy |
| 19 | Repeated bad attempts | Guessing continues | Rate limit/lockout applies |
| 20 | Authentication/recovery completes | Logs/audit emitted | No secrets are exposed |

Suggested levels: unit tests for token/state rules; integration tests for session stores and providers; end-to-end tests for login/recovery journeys.
