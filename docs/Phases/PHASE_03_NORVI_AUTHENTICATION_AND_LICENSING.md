# Phase 3: Norvi Authentication Boundary

## Status
**Completed**

## Overview
This phase integrated the authentication boundary into the desktop application. We established a secure Login UI where the user inputs their email, password, and activation key. The client securely extracts a stable Hardware ID (HWID) to adhere to the strict 3-device limit enforced by your agency backend, and manages the resulting session token securely within the OS credential store.

## Accomplishments
1. **Hardware ID (HWID) Module** (`src/services/auth/hwid.py`):
   - Created a module to fetch a stable, unique machine identifier.
   - Primarily queries the `wmic csproduct get uuid` on Windows.
   - Includes a cross-platform MAC-address fallback (`uuid.getnode()`).
   - Hashes the resulting string (SHA-256) to ensure a clean, stable token format before sending it to the agency backend.
2. **Auth Client** (`src/services/auth/client.py`):
   - Implemented an asynchronous `httpx` client that packages the email, password, activation key, and the `hardware_id` and sends it to the `NORVI_API_URL`.
   - Includes robust error handling for network timeouts and invalid credentials.
3. **Secure Session Manager** (`src/services/auth/session.py`):
   - Utilizes the `keyring` library to securely save, load, and clear the resulting access token in the Windows Credential Manager.
   - Ensures no passwords or active tokens are ever persisted in plaintext log files or local databases.
4. **Login UI & Window Integration** (`src/ui/views/login.py`, `src/ui/main_window.py`):
   - Built the `LoginView` with a professional interface for capturing credentials.
   - Ensured the UI uses the `BaseWorker` thread to run the authentication without freezing the application.
   - Modified `MainWindow` to act as an authentication guard: it hides the sidebar and shows the login screen if the user is unauthenticated, automatically bringing them to the Dashboard upon success.
5. **Logout Flow**:
   - Added a "Logout" button to the main sidebar.
   - Emits a signal to cleanly delete the secure token and immediately push the user back to the login screen.

## Action Items Completed
- [x] Login UI.
- [x] Email field.
- [x] Password field.
- [x] Activation/API key field.
- [x] Auth client.
- [x] Session/token handling.
- [x] Logout.
- [x] License state.
- [x] Secure token storage.
- [x] No plaintext password persistence.

## Next Steps
Proceeding to **Phase 4: Local Storage and Privacy Foundation**, which will lay the groundwork for managing the local SQLite database where all video metadata and schedules will securely reside.