# Phase 8 — Source Selection & Rights Workflow

## Status

Not Started

---

## Objective

Create the complete selected-source workflow that bridges discovery to media processing.

---

## Scope

Implement:

- Selected-source record.
- Source details screen.
- Source preview.
- Original YouTube link.
- Rights/permission confirmation.
- Local rights confirmation record.
- Target clip duration selection.
- Validation.
- Start-analysis request.

---

## Rights Requirement

Before repurposing source media, the user confirms that they:

- Own the content, or
- Have permission, or
- Have the required rights/license.

Public availability must not be treated as automatic reuse permission.

---

## Duration Requirement

Allowed:

10–120 seconds.

Suggested presets:

- 15
- 30
- 45
- 60
- 90
- 120

Support a validated custom value if desired.

---

## Architecture Requirements

Discovery result becomes a persistent local source record.

The rights confirmation must be stored locally with:

- Source identifier.
- Confirmation timestamp.
- Local user/account reference where applicable.

Do not send confirmation details to Nexus.

---

## Functional Requirements

User can:

1. Select a result.
2. View selected source.
3. Open original on YouTube.
4. Confirm rights.
5. Choose clip duration.
6. Start source preparation.

Without rights confirmation:

Analysis must remain blocked.

---

## Privacy Requirements

Selected video history and rights confirmations remain local.

---

## Security Requirements

Validate source identifiers/URLs.

Do not trust raw URLs from UI without provider normalization.

---

## Error Handling Requirements

Handle:

- Video removed.
- Invalid source.
- Invalid duration.
- Rights not confirmed.
- Source metadata unavailable.
- User returns to discovery.

---

## Testing Requirements

Boundary tests:

- 9 seconds rejected.
- 10 accepted.
- 60 accepted.
- 120 accepted.
- 121 rejected.
- Missing confirmation blocks processing.

---

## Acceptance Criteria

- Selected source persists.
- User sees correct source.
- Rights gate cannot be bypassed through normal workflow.
- Duration is validated.
- Start processing creates correct next-stage request.

---

## Real User Validation

Search for a video.

Select it.

Confirm rights.

Choose 60 seconds.

Start analysis.

Verify the app transitions correctly to source preparation without performing unsupported processing yet.

---

## Antigravity Instructions

Do not implement video intelligence yet.

Build the workflow contract Phase 9 will consume.

---

## Completion Report Requirements

Report:

- Data stored.
- Rights workflow.
- Duration validation.
- Tests.
- Real user flow.

---

## Phase Completion Rule

The source must be well-defined and explicitly authorized before any media acquisition begins.