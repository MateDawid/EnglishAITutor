# ADR 0002: Cookie-based browser authentication

- Status: Accepted
- Date: 2026-10-28

## Context

The current backend returns a bearer token to the frontend, which stores and sends it from JavaScript. The target application is a browser-based SPA with authenticated HTTP and WebSocket communication. The authentication design must protect credentials from direct access by browser scripts and address cross-site request forgery for cookie-authenticated requests.

## Decision

- Use a signed access JWT in an `HttpOnly`, `Secure`, `SameSite=Lax`, host-only cookie scoped to `/`. The browser sends the cookie automatically; frontend JavaScript does not read or store the JWT.
- Use a 24-hour hard access-token lifetime. After expiry, the user must authenticate again; a refresh-token flow is not part of this decision.
- Provide a CSRF bootstrap endpoint that issues a signed CSRF token for the frontend to keep in memory and send in the `X-CSRF-Token` header on unsafe HTTP requests, including registration and login.
- Require a trusted `Origin` and a valid CSRF token for unsafe HTTP requests. Restrict credentialed CORS to explicitly configured frontend origins.
- Use the access-token cookie to authenticate protected HTTP requests and WebSocket handshakes. WebSocket connections also validate the trusted origin and conversation ownership, and are closed when the access token expires.
- Logout clears the browser cookie. It does not revoke an already-issued token; that token remains valid until expiry.

## Consequences

- The frontend must send credentials with API requests and obtain/send CSRF tokens for unsafe requests.
- The backend must set and clear the access cookie, validate CSRF and origin checks, and authenticate WebSocket handshakes from the cookie.
- Cookie authentication is the accepted target. The current bearer-token implementation remains in place until the backend and frontend are migrated.
- Cookie attributes and token lifetime are security-sensitive settings and must be kept consistent across login, logout, HTTP, and WebSocket flows. The 24-hour expiry is a simple initial policy and can be revisited if usage warrants longer sessions or refresh support.
