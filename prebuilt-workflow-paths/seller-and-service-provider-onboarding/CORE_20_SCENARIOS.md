# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Eligible provider becomes active | Supply access is duplicated or granted before checks complete |
| 2 | Information request is resubmitted | Edits silently alter the already reviewed version |
| 3 | Ineligible application is rejected | Seller entitlement is provisioned despite rejection |
| 4 | Required application data is missing | An incomplete application reaches approval |
| 5 | Evidence is malformed or unsafe | Unsafe content is rendered or treated as verified |
| 6 | Provider is ineligible | Ineligible supply is activated |
| 7 | Actor cannot change application | An application identifier grants control |
| 8 | Duplicate identity is detected | Unrelated providers merge or a suspended seller evades history |
| 9 | Approve and reject arrive together | The application becomes both approved and rejected |
| 10 | Evidence expires at decision boundary | Expired evidence activates supply through race or clock differences |
| 11 | Submission response is lost | Duplicate applications and checks are created |
| 12 | Verification callback is replayed | Verification, approval, or activation repeats |
| 13 | Applications are flooded or forged | Fake supply overwhelms reviewers or bypasses limits |
| 14 | Application commits but verification fails | It is silently approved or permanently stranded |
| 15 | Verification provider times out | Uncertainty becomes verified or triggers blind duplicate checks |
| 16 | Approval commits but response is lost | Roles or accounts duplicate |
| 17 | Cross-tenant application is referenced | Identifiers cross marketplace boundaries |
| 18 | Sensitive evidence causes an error | Documents or sensitive review notes leak |
| 19 | Stale approval follows withdrawal | Old evidence unexpectedly activates supply |
| 20 | Approved account provisioning fails | Provider appears active without required controls |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).

