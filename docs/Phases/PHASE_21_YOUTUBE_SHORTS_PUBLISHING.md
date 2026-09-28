# Phase 21 — YouTube Shorts Publishing

## Status

Not Started

---

## Objective

Implement real YouTube publishing through the platform integration foundation and persistent publishing queue.

---

## Scope

Implement:

- YouTube media validation.
- Metadata mapping.
- Account validation.
- Upload.
- Scheduling/publish configuration where officially supported.
- Status tracking.
- Publish verification.
- External video/post ID.
- Result URL.
- Error normalization.
- Retry compatibility.
- Analytics identity handoff.

---

## Important Requirement

Use supported official mechanisms.

Do not bypass YouTube security or account protections.

---

## Workflow

Approved Clip
↓
Schedule
↓
Queue
↓
YouTube Adapter Validation
↓
Upload
↓
Platform Processing
↓
Verify
↓
Store YouTube ID / URL
↓
Published

---

## Validation

Before upload validate:

- Clip exists.
- Clip version approved.
- Account connected.
- Required permissions.
- Media constraints.
- Metadata constraints.

---

## Privacy Requirements

Upload goes:

User PC
→ YouTube

not through Norvi.

---

## Error Handling Requirements

Handle:

- Auth expired.
- Quota/rate limits.
- Invalid video.
- Invalid title/metadata.
- Upload interruption.
- Processing failure.
- Duplicate retry.
- Account issue.

---

## Idempotency Requirement

Special attention must be paid to timeout/crash after the platform accepted upload.

Attempt reconciliation before starting a replacement upload.

---

## Testing Requirements

Use test/private/unlisted content where appropriate.

Test:

- Successful upload.
- Scheduled upload if supported.
- Network interruption.
- Invalid metadata.
- Auth expiry.
- Retry.
- App restart during workflow.
- Duplicate replay.

---

## Acceptance Criteria

- Real test upload succeeds.
- Published state verified.
- External identity stored.
- Retry does not create duplicate during tested scenarios.
- Failure states visible.
- Queue remains consistent.

---

## Real User Validation

From real application:

1. Approve test clip.
2. Select YouTube.
3. Schedule or publish test post.
4. Verify on YouTube.
5. Confirm local published URL/state.

---

## Antigravity Instructions

A successful API response alone is not enough.

Verify the actual final platform state.

If real-user test fails:

find cause
→ fix
→ test again

until the supported flow genuinely works.

---

## Completion Report Requirements

Include:

- API integration used.
- Permissions.
- Upload flow.
- Scheduling capabilities/limitations.
- Real test result.
- Failure tests.
- Idempotency observations.

---

## Phase Completion Rule

YouTube publishing must work end-to-end before moving to Instagram.