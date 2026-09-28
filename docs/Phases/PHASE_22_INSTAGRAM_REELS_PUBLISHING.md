# Phase 22 — Instagram Reels Publishing

## Status

Not Started

---

## Objective

Add real Instagram Reels publishing using supported Meta platform functionality.

---

## Scope

Implement:

- Instagram account eligibility validation.
- Media validation.
- Metadata/caption mapping.
- Reel publishing flow.
- Scheduling where supported through the chosen official mechanism.
- Processing-state tracking.
- Publish verification.
- External post ID.
- Result URL when available.
- Error normalization.
- Queue integration.

---

## Account Compatibility

Do not assume every Instagram account type supports every API feature.

Detect requirements and explain them clearly to the user.

---

## Privacy Requirements

User PC communicates directly with Meta services.

No media passes through Norvi.

---

## Security Requirements

Use the permissions approved for the supported publishing flow.

Do not:

- Reuse browser passwords.
- Steal cookies.
- Automate login screens through credential scraping.
- Bypass Meta restrictions.

---

## Error Handling Requirements

Handle:

- Unsupported account.
- Missing page/business linkage if relevant.
- Permission missing.
- Token expired.
- Media rejected.
- Container/processing timeout.
- Rate limit.
- Network failure.
- Duplicate retry.

---

## Testing Requirements

Use a test/appropriate account.

Test:

- Successful Reel publish.
- Invalid media.
- Invalid caption.
- Token expiration.
- Network failure.
- Processing failure.
- Replay/idempotency.
- App restart.

---

## Acceptance Criteria

- Supported Instagram account connects.
- Approved clip publishes.
- Result verified.
- Failure states normalized.
- Queue/retry works.
- No duplicate in tested replay scenarios.

---

## Real User Validation

Publish a controlled test Reel through the real desktop app.

Verify it in Instagram.

---

## Antigravity Instructions

Follow current supported Meta integration requirements.

Do not fake unsupported capabilities.

Surface platform limitations honestly.

---

## Completion Report Requirements

Include:

- Supported account type.
- Permissions.
- Real upload result.
- Scheduling behavior.
- Limitations.
- Tests.

---

## Phase Completion Rule

Instagram publishing must be independently reliable before Facebook implementation.