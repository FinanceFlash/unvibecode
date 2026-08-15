# Core 20 Scenarios

1. Valid credentials — **Must not happen:** valid users are denied without a policy reason.
2. Invalid password — **Must not happen:** an authenticated session is created.
3. Unknown account — **Must not happen:** account existence is unnecessarily disclosed.
4. MFA required — **Must not happen:** login succeeds before the required challenge.
5. Invalid MFA — **Must not happen:** the challenge is bypassed.
6. Expired MFA — **Must not happen:** an expired challenge authenticates.
7. Replayed MFA — **Must not happen:** the same one-time challenge works twice.
8. Session creation — **Must not happen:** a session is issued for an unauthenticated identity.
9. Session expiry — **Must not happen:** an expired session remains accepted.
10. Session rotation — **Must not happen:** a pre-authentication session remains privileged after login.
11. Logout — **Must not happen:** a revoked session remains usable.
12. Concurrent logout/use — **Must not happen:** a revoked session wins a race and performs protected work.
13. Refresh rotation — **Must not happen:** a reused rotated refresh token creates a new session.
14. Recovery request — **Must not happen:** the request reveals account existence beyond policy.
15. Expired recovery token — **Must not happen:** an expired token changes credentials.
16. Replayed recovery token — **Must not happen:** a consumed token works again.
17. Recovery scope — **Must not happen:** a token for one account changes another account.
18. Credential change — **Must not happen:** old credentials remain accepted when policy requires invalidation.
19. Rate limit/lockout — **Must not happen:** unlimited guessing remains possible.
20. Security notification/audit — **Must not happen:** sensitive secrets are recorded in notifications or logs.
