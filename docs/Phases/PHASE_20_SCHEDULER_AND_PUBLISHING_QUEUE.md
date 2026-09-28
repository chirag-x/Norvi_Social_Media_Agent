# Phase 20 — Persistent Scheduler & Publishing Queue

## Status

Not Started

---

## Objective

Build the reliable local scheduling and job system that will execute future YouTube, Instagram, and Facebook publishing.

---

## User Requirements

For every approved clip, user can select:

- Platform.
- Account.
- Date.
- Time.
- Timezone.
- Metadata.
- Cover/options.

Different clips may use different schedules.

The same clip may use different times on different platforms.

---

## Required Work

Implement:

- Schedule entity.
- Date/time UI.
- Timezone handling.
- Persistent scheduler.
- Publishing job entity.
- Durable queue.
- Job state machine.
- Idempotency keys.
- Retry policy.
- Cancellation.
- Rescheduling.
- Queue UI.
- Job history.

---

## Publishing States

Approved
↓
Scheduled
↓
Queued
↓
Uploading
↓
Platform Processing
↓
Published

Failure states:

- FailedTransient.
- FailedPermanent.
- AuthRequired.
- Cancelled.

---

## Idempotency

Every publishing intent must have a stable identifier.

Retrying a job must not blindly create another social post.

This is mandatory.

---

## Offline Behavior

If internet is unavailable at scheduled time:

- Keep job.
- Record failure/state.
- Retry safely according to policy.

---

## Powered-Off Behavior

A locally powered-off computer cannot execute a local API request.

If a platform supports its own server-side scheduling and the post was already submitted, use it appropriately.

Otherwise the local job waits until the application/system becomes available according to documented behavior.

Do not claim otherwise.

---

## Architecture Requirements

Scheduler does not contain platform-specific upload logic.

It invokes publishing adapters.

---

## Privacy Requirements

Schedules and queue remain local.

---

## Security Requirements

Validate:

- Approved clip.
- Correct account.
- Correct platform.
- Correct local authorization.

before queueing/executing.

---

## Error Handling Requirements

Classify:

- Network.
- Rate limit.
- Auth expired.
- Invalid media.
- Permanent platform rejection.
- Unknown transient error.

Never retry permanent failures forever.

---

## Testing Requirements

Test:

- Schedule one job.
- Schedule multiple.
- Different timezones.
- Restart app.
- Offline.
- Reschedule.
- Cancel.
- Duplicate queue event.
- Worker crash/restart.

---

## Acceptance Criteria

- Schedules persist.
- Queue persists.
- Retry system works.
- Cancellation works.
- Rescheduling works.
- Duplicate execution prevented.
- Queue status visible.

---

## Real User Validation

Schedule mock/test jobs a few minutes in the future.

Close/reopen app.

Confirm scheduling remains correct.

Simulate offline state.

---

## Antigravity Instructions

Use a mock publishing provider for queue tests.

Do not prematurely implement platform-specific upload logic here.

---

## Completion Report Requirements

Report:

- Scheduler technology.
- Queue strategy.
- State machine.
- Retry rules.
- Idempotency design.
- Tests.

---

## Phase Completion Rule

Publishing infrastructure must survive failures before connecting it to real social-media side effects.