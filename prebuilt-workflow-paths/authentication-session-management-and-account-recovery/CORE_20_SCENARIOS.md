\# Core 20 Scenarios



Each scenario is distinct by trigger, stage, permission boundary, timing condition, dependency failure, concurrency condition, or abuse mechanism.



Every scenario states what must not happen.



| # | Scenario | Trigger | Expected outcome | Must not happen |

|---|---|---|---|---|

| 1 | Valid authentication | A registered user submits valid authentication credentials. | The credentials are validated and an authenticated session is established. | An authenticated session must not be created for an account other than the account being authenticated. |

| 2 | Invalid credentials | A user submits invalid credentials. | Authentication is denied. | Invalid credentials must not create an authenticated session. |

| 3 | Unknown account | Authentication is attempted for an account identifier that does not exist. | Authentication is denied without exposing unnecessary account-existence information. | The response must not reveal whether a particular account exists. |

| 4 | Locked or restricted account | Authentication is attempted for an account that is temporarily locked or otherwise restricted from authentication. | Authentication is denied according to the account's security policy. | A restricted account must not bypass its authentication restriction through an ordinary login attempt. |

| 5 | Authentication retry boundary | Repeated authentication failures reach the configured retry threshold. | Further authentication attempts are limited according to the security policy. | Unlimited credential guessing must not remain possible through repeated requests. |

| 6 | Multi-factor authentication challenge | Valid primary authentication requires an additional authentication factor. | A valid second factor completes authentication. | Passing only the primary authentication step must not create a fully authenticated session when the additional factor is required. |

| 7 | Invalid multi-factor challenge | A user submits an invalid or expired additional authentication factor. | The authentication challenge is rejected. | An invalid or expired factor must not complete authentication. |

| 8 | Session creation | All required authentication steps succeed. | A new authenticated session or token is created for the correct account. | Session credentials must not be issued for the wrong account or without successful authentication. |

| 9 | Session expiration | An authenticated session reaches its configured expiration boundary. | The session can no longer be used as an authenticated credential. | An expired session must not continue granting authenticated access. |

| 10 | Explicit logout | An authenticated user explicitly logs out. | The relevant session is terminated or invalidated. | A logged-out session must not remain usable for authenticated requests. |

| 11 | Concurrent session termination | A user terminates a session while another request attempts to use that same session. | Session validity follows the application's defined revocation ordering. | A revoked session must not regain authenticated validity because of a concurrent request. |

| 12 | Recovery request for a valid account | A user requests account recovery for an existing account. | A recovery process is initiated according to the configured recovery policy. | The recovery process must not directly authenticate the requester without sufficient recovery proof. |

| 13 | Recovery request for an unknown account | A user requests recovery for an account identifier that does not exist. | The request is handled without revealing unnecessary account-existence information. | Recovery responses must not become an account-enumeration mechanism. |

| 14 | Valid recovery token | A user submits a valid, unexpired recovery token. | The token is accepted and the permitted recovery operation can proceed. | A valid token must not grant access to a different account. |

| 15 | Expired recovery token | A user submits an expired recovery token. | Recovery is denied. | An expired token must not restore account access or permit credential changes. |

| 16 | Recovery token replay | A previously consumed recovery token is submitted again. | The repeated use is rejected. | A recovery token must not be reusable after successful consumption. |

| 17 | Credential replacement after recovery | A user completes the required recovery verification. | The credential is changed according to the recovery policy and affected sessions or tokens are handled appropriately. | An attacker must not retain authenticated access through stale credentials or sessions when the policy requires invalidation. |

| 18 | Recovery dependency failure | A required recovery dependency, such as an email, identity, or notification provider, fails during recovery. | Recovery does not falsely report success and remains recoverable through an appropriate retry or alternative path. | The system must not claim successful account recovery when the required recovery operation did not complete. |

| 19 | Concurrent recovery and authentication | Account recovery and ordinary authentication occur concurrently for the same account. | Credential and session state follows a deterministic ordering and security policy. | Concurrent operations must not leave the account in a contradictory authentication state. |

| 20 | Authorization boundary after authentication | An authenticated session attempts to access protected account data or actions belonging to another account. | The request is denied unless the authenticated identity has an explicit authorization grant. | Authentication of one account must not provide unauthorized access to another account's protected data or actions. |

