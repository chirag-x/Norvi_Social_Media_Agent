# Phase 14 — Clip Lab & Review UI

## Status

Not Started

---

## Objective

Create the main interface where users review AI-generated candidates and decide which clips deserve further processing.

---

## Required UI

Each candidate card displays:

- Preview/proxy where currently available.
- Candidate number.
- Start/end time.
- Duration.
- Score.
- Explanation.
- Warnings.
- Recommended platform fit.

Actions:

- Preview.
- Approve.
- Reject.
- Edit boundaries.
- Open details.

---

## Sorting / Filtering

Support useful options:

- Highest score.
- Source order.
- Duration.
- Approved only.
- Needs review.
- Rejected.

---

## Review State

States:

- Generated.
- Needs Review.
- Approved.
- Rejected.

State must persist across app restart.

---

## Timeline Editing

At minimum allow user to change:

- Start.
- End.

Use validated boundaries.

Phase 15 performs final rendering.

---

## Architecture Requirements

UI interacts with clip services/repositories.

Do not let UI directly manipulate database rows.

Do not execute FFmpeg directly from widgets.

---

## Privacy Requirements

Everything stays local.

---

## Error Handling Requirements

Handle:

- Preview missing.
- Source missing.
- Invalid edit.
- Candidate deleted/stale.
- Save failure.

---

## Testing Requirements

Test:

- Load 1 candidate.
- Load many candidates.
- Sort.
- Filter.
- Approve.
- Reject.
- Edit.
- Restart.
- Ensure state persists.

---

## Acceptance Criteria

User can comfortably review candidate set.

Approval/rejection persists.

No candidate publishes from this phase.

Edited boundaries remain valid.

UI remains responsive.

---

## Real User Validation

Generate candidates from a real source.

Review them entirely through the application.

Approve some.

Reject others.

Restart and verify state remains.

---

## Antigravity Instructions

Build a practical agency review workflow, not a flashy demo.

Do not begin rendering or social publishing beyond interfaces necessary for this page.

---

## Completion Report Requirements

Report:

- Screens/components.
- State flow.
- Persistence.
- Tests.
- Manual review results.

---

## Phase Completion Rule

Users must be able to confidently select clips before expensive rendering is added.