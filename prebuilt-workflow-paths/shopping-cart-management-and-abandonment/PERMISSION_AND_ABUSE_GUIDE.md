# Permission and Abuse Guide

## Authorization boundaries
- **Guest carts:** Secured by a cryptographically strong, unguessable session identifier (e.g., UUIDv4 or signed JWT). Guessing IDs must not grant access to other carts.
- **Authenticated carts:** Bound to the user's secure identity. Requests must carry a valid authentication token.
- **Merge operations:** Only permitted when a valid guest session transitions successfully to an authenticated session during login.

## Misuse paths
- **Inventory lockup:** Attackers repeatedly adding items to carts to lock up inventory (if inventory is reserved at addition). Mitigation: Rate limit additions or reserve inventory only at checkout.
- **Cart hijacking:** Sniffing or guessing session IDs to access another customer's items or personal details. Mitigation: Secure cookies, strict CORS, and TLS.
- **Promotion abuse:** Brute-forcing promotional codes via the cart endpoint. Mitigation: Rate limiting and account-level blocking for repeated invalid attempts.

## Tenant isolation
- In multi-tenant systems, the cart identifier must securely bind to both the user and the tenant. A user must not view carts belonging to another tenant.

## Protected data
- Carts may contain sensitive preferences or pricing tiers. Cart data must not be exposed to unauthorized API clients.
