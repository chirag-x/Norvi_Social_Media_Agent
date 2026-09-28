# Phase 3 — Norvi Authentication & Licensing Client

## Status

Not Started

---

## Objective

Connect the desktop application to the existing Norvi account/licensing system without expanding the Norvi server into a social-media data backend.

---

## Scope

Implement desktop-side:

- Login screen/dialog.
- Email input.
- Password input.
- Activation/API/license key input.
- Authentication request.
- Session handling.
- Access token handling.
- Logout.
- Session expiry.
- License/entitlement state.
- Offline/auth-server failure states.
- Secure local session storage.

Do not build or redesign the Norvi backend.

---

## Privacy Boundary

Norvi may receive only information necessary for:

- Account authentication.
- License validation.
- Activation.
- Entitlement.
- Session management.

Norvi must never receive:

- YouTube searches.
- Social account information.
- Videos.
- Clips.
- Transcripts.
- AI prompts.
- AI output.
- Analytics.
- Scheduling data.
- Brand/client data.

This boundary is mandatory.

---

## Required Work

Create a dedicated Norvi authentication client.

The UI must never make raw authentication calls directly.

Authentication flow:

App opens
→ Existing valid session?
→ Yes: validate/continue
→ No: show login
→ Email/password/license authentication
→ Receive authenticated session/token
→ Store securely
→ Enter application

Do not persist plaintext password.

---

## Architecture Requirements

Use:

`UI → AuthService → NorviAuthClient`

not:

`UI → random HTTP requests`.

Authentication failures must use normalized errors.

The activation/license backend remains outside the project scope.

---

## Files / Modules Involved

Expected:

- `src/services/auth/`
- `src/integrations/norvi/`
- `src/storage/credentials/`
- login UI.
- settings/account UI.
- authentication tests.

---

## Security Requirements

- HTTPS required for production Norvi communication.
- Never log password.
- Never log activation key.
- Never log full access/refresh tokens.
- Store authentication tokens using secure OS-backed storage where possible.
- Password field must be masked.
- Clear password from UI/state when no longer needed.
- Session invalidation must be handled correctly.

---

## Error Handling Requirements

Handle:

- Wrong email/password.
- Invalid license.
- Expired license.
- Server unreachable.
- Timeout.
- Invalid server response.
- Expired session.
- Revoked session.

Display useful messages without leaking server internals.

---

## Testing Requirements

Use mock/test Norvi responses where real backend testing is unavailable.

Test:

- Valid login.
- Invalid login.
- Invalid activation key.
- Expired session.
- Server unavailable.
- Logout.
- App restart with saved valid session.
- Secret redaction.

---

## Acceptance Criteria

- User can authenticate.
- Valid session unlocks application.
- Invalid credentials do not.
- Password is not persisted.
- Norvi client sends no social workflow information.
- Logout removes/revokes local session appropriately.
- Authentication errors are clear.
- Previous phases remain working.

---

## Real User Validation

Using the real approved Norvi test environment:

1. Open application.
2. Login.
3. Verify authorized state.
4. Restart application.
5. Verify session behavior.
6. Logout.
7. Verify protected app flow requires authentication again.

---

## Antigravity Instructions

Do not create new Norvi server endpoints unless the project owner explicitly supplies/approves that work.

Implement only the desktop authentication client boundary.

Do not mix authentication code into unrelated application modules.

---

## Completion Report Requirements

Report:

- Authentication flow.
- Credential storage method.
- Norvi data fields transmitted.
- Files changed.
- Tests.
- Real validation results if available.
- Any backend dependency still required.

---

## Phase Completion Rule

Authentication must be functional and privacy-bounded before local user-data features begin.