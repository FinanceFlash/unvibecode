# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | All sequential reviewers approve | A later step starts early or finalization runs twice |
| 2 | Parallel stage reaches quorum | A non-vote counts or additional responses duplicate effects |
| 3 | Authorized reviewer rejects | Later stages proceed as though approved |
| 4 | Required request evidence is missing | An incomplete request reaches final approval |
| 5 | Decision input is malformed | Malformed content reaches storage, rendering, or logs unsafely |
| 6 | Reviewer is no longer eligible | Old assignment alone authorizes approval |
| 7 | Requester attempts self-approval | Self-approval bypasses required independent review |
| 8 | Request changes after approval | Version two inherits stale approval silently |
| 9 | Approve and reject arrive together | The workflow ends both approved and rejected |
| 10 | Decision arrives at deadline | Client time or race conditions extend eligibility unpredictably |
| 11 | Submission response is lost | Duplicate workflows and notifications are created |
| 12 | Recorded decision is replayed | Votes, finalization, or downstream effects repeat |
| 13 | Approval actions are automated or flooded | Notification amplification or policy bypass occurs |
| 14 | Decision commits but notification fails | The decision is rolled back incorrectly or repeated |
| 15 | Policy or identity dependency times out | Unverified eligibility becomes approval |
| 16 | Final approval response is lost | Finalization or downstream work runs again |
| 17 | Cross-tenant reviewer attempts action | Identifiers alone cross the tenant boundary |
| 18 | Sensitive evidence causes an error | Evidence, comments, or authorization proof appears in unsafe logs or messages |
| 19 | Late approval follows terminal action | The request returns to approved through a stale action |
| 20 | Approved request downstream work fails | The system reports complete while the business outcome is missing |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).

