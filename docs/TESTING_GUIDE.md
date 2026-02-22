# 🧪 Oscar Legal Practitioners - Testing & Verification Guide

This guide provides a structured approach for testing the integrated Oscar Legal Practitioners system. It covers functional verification of the frontend, backend, and AI service.

---

## 🔑 1. Test Credentials
Use these seeded accounts to verify the system's role-based access:

| Role | Email | Password | Purpose |
| :--- | :--- | :--- | :--- |
| **Lawyer** | `counselor@oscarlegal.com` | `password123` | Dashboard, CRM, AI Tools, Blog |
| **Client** | `john.doe@example.com` | `password123` | Portal access, static views |

---

## 🏗️ 2. Functional Test Scenarios

### 🔓 Scenario A: Authentication & Security
1.  **Sign In**: Navigate to `signin.html`, enter Lawyer credentials.
    *   **Success**: Redirect to `dashboard.html`.
2.  **Protected Access**: Try to open `dashboard.html` in an Incognito window without logging in.
    *   **Success**: Redirected automatically to `signin.html`.
3.  **Logout**: Click "Logout" in the sidebar.
    *   **Success**: Local storage cleared, redirect to `index.html`.

### 📊 Scenario B: Lawyer Dashboard & CRM
1.  **Live Stats**: Verify stats cards (Clients: 1, Active Cases: 1).
    *   **Success**: Data matches the seeded database state.
2.  **Client Management**: Go to `clients.html`, add a new client.
    *   **Success**: Client appears in the table.
3.  **Case Details**: Click "Manage" on the seeded "Intellectual Property Dispute".
    *   **Success**: Navigates to the case management view.

### 🤖 Scenario C: AI Legal Tools
1.  **AI Research**: Navigate to `research.html` and search: *"What is the supreme law in Nigeria?"*
    *   **Success**: System retrieves "Constitution" from the vector DB and generates a cited answer.
2.  **AI Drafting**: Navigate to `drafting.html`, select "Non-Disclosure Agreement", enter parties.
    *   **Success**: Generates a professional legal draft in the preview window.
3.  **Legal Analysis**: Open `analysis.html`, describe a conflict scenario.
    *   **Success**: Returns a structured risk assessment (Overview, Principles, Strategic Advice).

### ✍️ Scenario D: Knowledge Sharing (Blog)
1.  **Publish Insight**: On the dashboard, click **"Publish Insight"**.
2.  **Draft**: Fill in Title ("The Future of AI in Law"), Excerpt, and Content.
3.  **Broadcast**: Click "Publish Now".
4.  **Public View**: Navigate to `blog.html`.
    *   **Success**: Your new post is listed at the top.

---

## 🛠️ 3. Troubleshooting & Logs
If a feature isn't responding, check the following Docker service health:

*   **Backend Issues** (Auth/Stat errors):
    ```powershell
    docker logs oscar_legal_backend --tail 50
    ```
*   **AI Service Issues** (Search/Drafting hangs):
    ```powershell
    docker logs oscar_legal_ai --tail 50
    ```
*   **Web Routing Issues** (404/502 errors):
    ```powershell
    docker logs oscar_legal_nginx --tail 50
    ```

---

## 🚦 4. System Status Check
Ensure all points are green before full production:
- [x] Nginx Proxy Routing (Port 80)
- [x] JWT Token persistence in LocalStorage
- [x] SQLAlchemy DB Schema (v1)
- [x] ChromaDB Vector Data seeding
- [x] Shared Sidebar Logic (common.js)

---
*Created for Oscar Legal Practitioners - Academic Implementation v0.1.0*
