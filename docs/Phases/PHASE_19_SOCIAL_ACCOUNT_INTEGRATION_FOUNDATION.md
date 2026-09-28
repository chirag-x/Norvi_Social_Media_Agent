# Phase 19 — Social Account Integration Foundation

## Status

Not Started

---

## Objective

Create the secure reusable foundation for connecting user-owned social-media accounts directly from the local application.

---

## Initial Platforms

- YouTube.
- Instagram.
- Facebook.

This phase builds integration infrastructure.

Actual publishing implementations come in later phases.

---

## Required Work

Create:

- Social account model.
- Integration status.
- OAuth/auth flow abstraction.
- Secure token storage.
- Token refresh handling.
- Reconnect behavior.
- Disconnect behavior.
- Permission tracking.
- Platform-adapter interfaces.
- Integration settings UI.

---

## Architecture

Core interfaces may include:

`PlatformAuthProvider`

`PublishingProvider`

`AnalyticsProvider`

Platform-specific implementations live in their adapter modules.

---

## Privacy Requirements

Social OAuth tokens must not be sent to Norvi.

Norvi must not proxy social publishing.

Flow:

User PC
→ YouTube/Meta

not:

User PC
→ Norvi
→ Social Platform

---

## Security Requirements

- Use supported OAuth mechanisms.
- Secure local token storage.
- Validate callback/state.
- Protect against CSRF/state mismatch.
- Never log token values.
- Least-required permissions.
- User can disconnect.
- Expired/revoked token clearly handled.

---

## UI Requirements

Integration page shows:

- Platform.
- Connected/disconnected.
- Account identity where allowed.
- Permission status.
- Reconnect.
- Disconnect.
- Authentication required.

---

## Error Handling Requirements

Handle:

- User denies authorization.
- Token expired.
- Refresh fails.
- Permissions missing.
- Account unsupported.
- Network failure.
- Callback failure.

---

## Testing Requirements

Use mock providers plus sandbox/test accounts where available.

Test:

- Connect.
- Disconnect.
- Expired token.
- Invalid state.
- Missing permission.
- Restart with saved secure token.

---

## Acceptance Criteria

- Secure account connection framework exists.
- Platform adapters follow common interfaces.
- Tokens remain local.
- Integrations page works.
- No content publishing yet unless needed only for provider smoke testing.

---

## Real User Validation

Connect available test accounts through the real application.

Restart application.

Verify connections are correctly recognized without exposing tokens.

---

## Antigravity Instructions

Do not implement three entire publishing platforms in this phase.

Build the shared integration foundation first.

---

## Completion Report Requirements

Report:

- OAuth approach.
- Token storage.
- Permissions.
- Integration interfaces.
- Tests.
- Real account validation.

---

## Phase Completion Rule

Social-account authentication must be secure and stable before scheduler/publishing side effects are introduced.