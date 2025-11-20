Single Sign-On (SSO) Architecture Overview
A custom SSO solution typically involves an Identity Provider (IdP)/Auth Server, and one or more client applications (here: the Vue.js frontend and the Frappe backend acting as a resource server). The IdP holds user credentials and issues tokens (ID and access tokens) after authenticating users. Client apps rely on these tokens (via OAuth2/OpenID Connect) instead of maintaining separate sessions. For example, a Node.js-based SSO gateway issues JWT tokens to statelessly authorize clients, and separates concerns among the SSO server, client apps, and user data store. The core components are:
Authentication/Authorization Server (IdP): Central service that authenticates users (e.g. with username/password) and issues OAuth2/OpenID Connect tokens. This can be a custom server or open-source IdP (Keycloak, Dex, Authentik, etc.). It stores user identities (or proxies to a directory) and enforces password policies.
Client Applications: The Vue.js SPA and the Frappe app act as OAuth2 clients. They register with the IdP (getting a Client ID/Secret) and use flows (e.g. Authorization Code with PKCE for the SPA) to obtain tokens. The Frappe backend (resource server) validates access tokens on incoming API calls.
Token Store and Refresh Mechanism: A mechanism to issue and refresh tokens. Access tokens are short-lived (e.g. minutes), refresh tokens are longer-lived and can be rotated for security.
These components interact via standard flows: the user signs in at the IdP (possibly via a Vue redirect), the IdP returns a code or token to the Vue app, which exchanges it for tokens. The Vue app then calls the Frappe API with the access token. The Frappe server validates the token (via introspection or signature verification) and maps it to a Frappe user session. This decouples authentication from the application, providing true SSO across clients.
Transitioning Frappe from Session to Token-Based SSO
By default, Frappe uses cookie-based sessions. To adopt SSO, you would switch Frappe to trust tokens instead of only its internal login. One approach is to configure Frappe as an OAuth client using its Social Login (OpenID Connect) feature. For example, in Integrations > Social Login Key, you add a “Custom” provider pointing to your IdP’s URLs (authorize, token, userinfo). Frappe will then redirect logins to the IdP and accept JWTs/ID tokens. Alternatively, you can enable token authentication using API keys/secrets (built-in) or a JWT-auth app. For instance, the jwt_auth Frappe app lets Frappe validate external JWTs on each request, automatically logging in or registering users. In practice, migrating involves: disabling or bypassing the default Frappe login page (since the SPA will handle login via SSO), and ensuring Frappe’s REST API endpoints accept Bearer tokens. Frappe’s documentation and community examples show how to plug an OAuth2 IdP into Frappe. For example, the Frappe forum notes that Frappe’s own OAuth2 endpoints are /api/method/frappe.integrations.oauth2.authorize and /api/method/frappe.integrations.oauth2.get_token for code flow, and an optional /openid_profile for user info. By setting up these endpoints with your IdP credentials, Frappe can offload authentication to the SSO server.
Vue.js Frontend Integration
The Vue.js SPA should act as an OAuth2/OIDC client. On app load or login button click, redirect the user to the IdP’s Authorization endpoint (with response_type=code, client ID, redirect_uri, scope=openid profile, and a PKCE code challenge). The browser navigates to the IdP, the user logs in, and the IdP sends back an authorization code to the Vue app’s redirect URI. The Vue app then exchanges this code (with the PKCE verifier) at the IdP’s Token endpoint for an ID token (with user identity) and an access token. Libraries like oidc-client or Keycloak’s JS adapter can handle this flow. Once tokens are received, the Vue app stores the access token securely (e.g. in memory or an in-memory Vuex store) and the ID token (optional) for user info. PKCE (Proof Key for Code Exchange) must be used since the SPA is a public client
cheatsheetseries.owasp.org
. After login, the Vue app includes the access token in Authorization: Bearer <token> headers when calling Frappe’s REST API. If Frappe is on a different domain, ensure CORS is configured and use axios or similar with withCredentials if cookies are involved. In a Backend-For-Frontend (BFF) pattern, the Vue app might instead communicate only with the Frappe backend (which acts as BFF). In that case, the Vue app would not see the tokens at all; Frappe would handle token storage. The Auth0 BFF guide describes this pattern: the backend performs the OAuth exchange, sets a secure session cookie for the SPA, and then proxies API calls using the stored token
auth0.com
auth0.com
. Embedding the tokens in the browser is thus avoided, improving security. The diagram below illustrates a BFF SSO flow: Figure: Backend-for-Frontend (BFF) SSO flow (from Auth0) In the above pattern, the Vue SPA simply calls Frappe endpoints (sending the session cookie). Frappe, as a confidential client, fetches and stores the OAuth tokens from the IdP
auth0.com
. Alternatively, in a direct SPA approach, the Vue app would use the tokens itself and call Frappe with Bearer headers. Both methods are viable; the BFF pattern is safer for SPAs because it keeps long-lived credentials off the client
auth0.com
auth0.com
.
Managing Sessions, Access Tokens, and Refresh Tokens
Secure token handling is critical. Access tokens should be short-lived (e.g. minutes) and scoped narrowly to what the app needs. Refresh tokens allow the SPA or backend to obtain new access tokens without re-prompting the user. Best practices include rotating refresh tokens: whenever the client uses a refresh token, the IdP issues a new refresh token and invalidates the old one
cheatsheetseries.owasp.org
. Also, bind tokens to a client (sender-constrained) if possible. The OWASP OAuth2 cheat sheet recommends that refresh tokens use rotation or sender-constraint to prevent replay
cheatsheetseries.owasp.org
. For storage: never put tokens in insecure storage. In a pure SPA (public client), don’t store tokens in localStorage or non-HttpOnly cookies, as they’re vulnerable to XSS. Instead, keep tokens in memory (e.g. a Vue store) and refresh on page reload (though this can force re-login on refresh unless using silent-refresh techniques). A safer approach is using the BFF pattern: store only an HttpOnly, Secure cookie for the session; the backend holds tokens in server-side storage. If the refresh token must be stored client-side, use a cookie with SameSite=None; Secure; HttpOnly and set Access-Control-Allow-Credentials on the server. This ensures it’s sent only via HTTPS and not accessible via JS. Always protect the authorization code flow with state and nonce parameters to prevent CSRF/replay. On Frappe’s side, once the access token is validated, you can either create a server session or treat each API call as stateless (validating the token each time). The jwt_auth app example redirects unauthenticated users to the provider’s login and creates a placeholder Frappe user if needed. Make sure to set reasonable token expiration and to implement logout/Revocation: e.g. calling the IdP’s logout endpoint to clear the SSO session, and have Frappe clear its session or cookies accordingly.
Identity Propagation to Frappe Backend
When the SSO server authenticates a user, that user’s identity (email or username) comes as claims in the ID token or userinfo response. The Frappe backend must map this to a Frappe User. Frappe’s social login creates a Website User by default (with minimal roles) if the user didn’t exist. You can pre-create users or post-provision them with the necessary roles. For example, the Keycloak integration notes that Frappe will auto-create a user without Desk access unless you assign roles in Portal Settings. You should adjust your role mappings so that SSO-users get the correct permissions. Technically, Frappe validates the token signature (or introspects it) using the IdP’s public keys (JWKS). If valid, it looks up the user by an identifier (often email) and logs them in. Any user creation or update can be hooked via Frappe’s OAuth handlers: as shown in the JWT Auth app, incoming JWTs can trigger auto-login or registration. In summary, the IdP authenticates the user, and Frappe trusts the IdP’s tokens to establish a Frappe session (or permissions) for that user.
Cross-Domain Considerations
If the Vue frontend and Frappe backend are on different domains, you must handle cross-origin issues. For token-based APIs, enable CORS on Frappe (Access-Control-Allow-Origin, etc.) and use tokens in Authorization headers, which bypasses cookie domain restrictions. If you prefer cookie-based sessions, you’ll need to set the cookie’s Domain attribute to allow sharing (e.g. a common parent domain) and set SameSite=None; Secure. Then the frontend must send credentials (fetch/axios with withCredentials: true), and Frappe must send Access-Control-Allow-Credentials: true. However, cookie SSO across totally different domains is tricky; often a reverse-proxy is used to present the same domain or use hidden iframes for cross-site login. In any case, using an Authorization header with a bearer token (and CORS) is usually simpler.
Example Architecture and References
A typical architecture is shown below. The IdP (Auth Server) handles login and issues tokens. The Vue SPA and Frappe backend are clients of the IdP. The Vue app obtains tokens and calls the Frappe API; the Frappe API validates tokens (optionally via a library or middleware) to authenticate requests. In a Backend-for-Frontend setup, Frappe itself manages the OAuth flow and session cookie for the SPA, as illustrated by Auth0’s BFF pattern
auth0.com
auth0.com
. Key open-source reference patterns: Frappe’s Social Login Key (custom provider) lets Frappe act as an OAuth client to any OIDC server. The jwt_auth Frappe app shows how to accept external JWTs and auto-register users. Auth0 and OWASP provide best-practice guidelines: always use Authorization Code with PKCE (not implicit) for SPAs
cheatsheetseries.owasp.org
, keep tokens short-lived, and rotate refresh tokens. In summary, build (or adopt) an OAuth2/OIDC server as the central SSO provider; configure your Vue app to use it (via code flow + PKCE); configure Frappe to accept its tokens (via social login or JWT). Manage sessions by securely storing tokens (or using a BFF cookie). By following standards and best practices, you ensure a secure, scalable SSO system for your Frappe/Vue library management app. Sources: Frappe docs and community posts on OAuth/SSO; Auth0’s BFF architecture guide
auth0.com
auth0.com
; OWASP OAuth2 best practices
cheatsheetseries.owasp.org
; example SSO gateway architectures; and JWT Auth for Frappe reference.
Эшлэлүүд

OAuth2 - OWASP Cheat Sheet Series

https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html

The Backend for Frontend Pattern (BFF) | Auth0

https://auth0.com/blog/the-backend-for-frontend-pattern-bff/

The Backend for Frontend Pattern (BFF) | Auth0

https://auth0.com/blog/the-backend-for-frontend-pattern-bff/

OAuth2 - OWASP Cheat Sheet Series

https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html
Бүх Эх сурвалжууд

cheatshe...ies.owasp

auth0



Custom SSO Architecture & Flows

Figure 1: High-level SSO system architecture. The Vue.js (Doppio) frontend and Frappe Desk (admin) both delegate login to a custom SSO/IdP. The SSO issues OAuth2 tokens for users, which the Vue app and Frappe backend use to authorize access. In this design, a single Identity Provider (SSO server) handles all user authentication. The Frappe backend serves as the OAuth2 Resource Server (hosting protected library data) and also registers the front-end and Desk as OAuth2 clients. A Frappe instance “can function as” a Resource Server, an Authorization Server, or an OAuth client
docs.frappe.io
. In practice, our SSO is the Authorization Server/IdP, and Frappe simply trusts it. This central SSO “identity gateway” lets users log in once and then access multiple apps (catalog, account, admin) without re‐authenticating
loginradius.com
. In development, Doppio’s Vue SPA typically proxies its /api/* calls to the Frappe server (port 8000) so that after SSO login the Vue app can securely call Frappe’s REST APIs
discuss.frappe.io
. All network traffic (user → SSO, token exchanges, API calls) uses HTTPS.

Figure 2: Customer login flow using OAuth2 Authorization Code. The Vue.js app redirects the user to the SSO, which authenticates and returns an authorization code; the app then exchanges it for an access token and calls Frappe’s API with that token. A library member visiting the Vue frontend clicks “Login” and is sent to the SSO’s authorization endpoint (front-channel redirect)
loginradius.com
. After entering credentials, the SSO validates the user (using its own user database) and issues an authorization code, redirecting back to the Vue app. The Vue app then sends the code to the SSO’s token endpoint (back-channel) and receives an access token (and optionally a refresh token)
docs.frappe.io
. The Vue app stores this JWT access token client-side. For every subsequent API call to Frappe, the Vue app includes Authorization: Bearer <token>. Frappe (as the Resource Server) “accepts and responds to protected resource requests using access tokens”
docs.frappe.io
: it verifies the token (e.g. checking signature, issuer, audience, expiry) before returning data. This ensures that only an authenticated user with a valid token can read or modify library resources.

Librarian (Frappe Desk) login: The admin login flow uses the same SSO mechanism, but is handled server-side in Frappe. When a librarian accesses the Frappe Desk, Frappe redirects the browser to the SSO (using its OAuth client setup, e.g. a “Social Login Key” connected-app) and requests an auth code. After the librarian logs in at the SSO, the SSO sends the code/token back to Frappe. Frappe then validates the token (or exchanges the code) and establishes a local session. In effect, Frappe’s Desk acts as an OAuth client – after the SSO grants tokens, Frappe creates its own session cookie for the user. Thus librarians only sign in once at the SSO, but Frappe Desk subsequently trusts that identity. (Note: Frappe’s OAuth configuration – the “Connected App”/Social Login records – lets Frappe treat an external IdP as a login provider
docs.frappe.io
.)

After login, token/session validation is critical. The Vue frontend (or its proxy) typically decodes and checks the JWT’s expiry client-side before using it. The Frappe backend, on every API request, treats the access token as proof of identity: it either introspects the token at the SSO or locally verifies its signature and claims
docs.frappe.io
loginradius.com
. In practice Frappe examines each Bearer token, confirms it was issued by the trusted SSO, and checks that it hasn’t expired. If invalid (expired, malformed, or wrong audience), the request is rejected. Best practices (from OAuth/OIDC) dictate always validating the token signature and audience, using short-lived access tokens, and refreshing them securely
loginradius.com
. Refresh tokens obtained at login let the Vue app silently request new access tokens from the SSO when needed, without re-prompting the user. All these exchanges remain over HTTPS to keep tokens confidential.

Sources: Standard OAuth2/SSO architecture and flows
loginradius.com
loginradius.com
docs.frappe.io
docs.frappe.io
discuss.frappe.io
docs.frappe.io
; Frappe OAuth docs illustrating resource server and client roles
docs.frappe.io
docs.frappe.io
.
