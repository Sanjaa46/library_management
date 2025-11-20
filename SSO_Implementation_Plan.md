### SSO Implementation Plan

#### **Phase 1: Backend (Frappe) Configuration**

1.  **Install JWT Authentication:** Install and configure a JWT authentication app in your Frappe bench to connect to your SSO provider.
2.  **Create "Social Login Key":** In the Frappe Desk, set up a custom "Social Login Key" with your SSO provider's URLs and credentials.
3.  **Modify Authentication Logic:** Update `library_management/auth.py` to validate JWTs from the `Authorization` header and create Frappe sessions.
4.  **Implement User Provisioning:** Add a hook to automatically create a `User` and `Library Member` on the first SSO login.

#### **Phase 2: Frontend (Vue.js) Implementation**

5.  **Install OIDC Client:** Add a library like `oidc-client-ts` to your frontend project.
6.  **Create Authentication Service:** In `frontend/src/authService.js`, encapsulate OIDC logic for login, token handling, and logout.
7.  **Integrate Auth Service:** Initialize the service in your Vue app, add login/logout buttons to `Header.vue`, and protect routes in `router.js` with an authentication guard.
8.  **Update API Calls:** Use an `axios` interceptor to automatically add the access token to all API requests.

#### **Phase 3: Testing and Refinement**

9.  **End-to-End Testing:** Thoroughly test the entire login, logout, and user provisioning flow.
10. **Security Review:** Review your implementation, focusing on secure token handling and storage.