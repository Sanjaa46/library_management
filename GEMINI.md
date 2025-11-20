# Project Overview

This is a **Library Management System** built on the **Frappe Framework**. The project consists of a Python-based backend and a modern Vue.js frontend.

## Backend

*   **Framework**: Frappe
*   **Language**: Python
*   **Key Dependencies**:
    *   `frappe-bench`: The core Frappe framework for backend development.
    *   `stripe`: Used for payment processing, likely for library memberships or fees.

## Frontend

*   **Framework**: Vue.js (v3)
*   **Build Tool**: Vite
*   **UI Framework**: `frappe-ui` and `tailwindcss`
*   **Routing**: `vue-router`
*   **Real-time Communication**: `socket.io-client`

# Building and Running

## Backend (Frappe)

1.  **Install Bench (Frappe's CLI)**:
    Follow the official Frappe documentation to [install the bench CLI](https://docs.frappe.io/framework/user/en/installation).

2.  **Get the App**:
    ```bash
    bench get-app https://github.com/Sanjaa46/library_management.git
    ```

3.  **Install Dependencies**:
    ```bash
    bench pip install -r ./apps/library_management/requirements.txt
    ```

4.  **Create a New Site**:
    ```bash
    bench new-site <site_name>
    ```

5.  **Install the App on Your Site**:
    ```bash
    bench --site <site_name> install-app library_management
    ```

6.  **Start the Bench**:
    ```bash
    bench start
    ```

## Frontend (Vue.js)

1.  **Navigate to the Frontend Directory**:
    ```bash
    cd frontend
    ```

2.  **Install Dependencies**:
    ```bash
    npm install
    ```
    or
    ```bash
    yarn install
    ```

3.  **Run the Development Server**:
    ```bash
    npm run dev
    ```
    or
    ```bash
    yarn dev
    ```

4.  **Build for Production**:
    ```bash
    npm run build
    ```
    or
    ```bash
    yarn build
    ```

# Development Conventions

*   **Backend**: The backend follows the standard Frappe framework conventions, with business logic encapsulated in DocTypes and Python controllers.
*   **Frontend**: The frontend is a single-page application (SPA) built with Vue.js. Components are located in `frontend/src/assets/components`.
*   **API**: The Frappe backend exposes a REST API that the frontend consumes. The API documentation can be found in `APIDocumentation.md`.
*   **Deployment**: The project is configured to be deployed using Docker. See the `docker-compose.yml` file and the "Deployment" section in the `README.md` for more details.
