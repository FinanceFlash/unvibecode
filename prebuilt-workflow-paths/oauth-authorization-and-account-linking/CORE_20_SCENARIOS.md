# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Eligible user links a provider account once | One provider account creates duplicate local links |
| 2 | Returning user signs in with the linked provider | The provider subject maps to the wrong local account |
| 3 | State or PKCE verifier is missing or wrong | The callback still creates a session or link |
| 4 | Provider denies consent | Denial is stored as a successful connection |
| 5 | Callback code is replayed | A second session or duplicate link is created |
| 6 | Redirect target is unapproved | The flow forwards tokens or users to an attacker-controlled destination |
| 7 | Requested scopes exceed policy | Broader access is granted without explicit approval |
| 8 | Provider subject is already linked elsewhere | The existing link is silently reassigned |
| 9 | Email or claim collides with another account | A guessed identity joins the wrong user |
| 10 | Two link attempts run concurrently | Both succeed and create conflicting provider-link state |
| 11 | Callback arrives after cancellation or expiry | A stale request still becomes active |
| 12 | Token exchange succeeds but local write fails | Retrying creates a second link or loses the successful exchange |
| 13 | Local write succeeds but response is lost | The user repeats the flow and duplicates the link or session |
| 14 | Refresh token rotates | The old token remains active and breaks future recovery |
| 15 | Provider revokes access later | Local state still shows an active trusted connection |
| 16 | Cross-tenant provider identity is supplied | An identity from another tenant crosses the boundary |
| 17 | Support or admin relink is attempted without authority | Privileged tooling bypasses normal ownership checks |
| 18 | OAuth error details are logged | Tokens, claims, or secrets leak into logs or support traces |
| 19 | Provider callback omits required claim data | The system invents or over-trusts missing identity fields |
| 20 | Reconciliation runs after uncertain exchange status | Manual repair changes the wrong account or provider link |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).
