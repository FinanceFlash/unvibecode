# Paths and Edge Cases

## Supported paths
- Signed-in user links an external provider to an existing local account
- Returning user signs in through a previously linked provider subject
- Policy allows first-time local account creation from trusted provider claims
- Incremental consent adds an approved new scope to an existing provider link
- Provider revocation or token rotation is detected and the link is updated safely

## Denied or blocked paths
- Actor lacks permission to create, relink, or use the provider connection
- State, nonce, PKCE, issuer, tenant, or redirect binding is invalid
- Requested or returned scopes exceed policy
- Provider subject is already linked to another local account
- Claims are missing, unverifiable, or collide with an unsafe account match

## Timing and boundary cases
- Two link flows complete at nearly the same time
- Callback arrives after user cancellation or request expiry
- Browser session changes between request creation and callback handling
- Provider revokes access while the local session is still active
- Token rotation occurs while another refresh or relink is in progress

## Recovery-focused paths
- Provider exchange succeeds but the local database update fails
- Local write succeeds but the completion response is lost
- Callback handling crashes after token receipt but before audit completion
- Automated reconciliation repairs an uncertain link without reassignment
