# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Valid email submits reset request and receives token link | Reset link is not delivered or token is not recorded |
| 2 | Unregistered email submits reset request | Response reveals whether the email is registered |
| 3 | Valid token used within expiry window | Credential is updated without consuming the token |
| 4 | Expired token submitted for reset | Credential is updated using an expired token |
| 5 | Already-consumed token is replayed | Credential is updated a second time with the same token |
| 6 | New reset request arrives while prior token is still valid | Both tokens remain valid simultaneously |
| 7 | User sets a new password meeting all policy rules | Credential update proceeds without policy verification |
| 8 | New password fails complexity or length policy | Non-compliant credential replaces the current one |
| 9 | New password is identical to the current password | Reused credential is silently accepted when policy prohibits it |
| 10 | Credential update succeeds | Active sessions remain valid after the credential changes |
| 11 | Two concurrent reset requests arrive for the same account | Both tokens are issued and both remain valid |
| 12 | Token format is tampered or structurally invalid | Malformed input reaches the credential store |
| 13 | Rate limit is exceeded for reset requests | Unlimited reset emails are sent from one source |
| 14 | Reset request arrives for a locked or suspended account | Token is issued and credential is changed for a restricted account |
| 15 | Account is deleted between request submission and token use | Deleted account credential is updated |
| 16 | Credential update succeeds but session invalidation response is lost | Retry creates a duplicate credential update |
| 17 | Token link is opened after the account email address has changed | Token validates against the new email owner |
| 18 | Reset request response time differs between registered and unregistered emails | Timing difference reveals account existence |
| 19 | Successful credential update is not followed by a confirmation notification | User is unaware that their credential was changed |
| 20 | Admin triggers a forced password reset for a user | User can authenticate with the old credential before completing the forced reset |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).
