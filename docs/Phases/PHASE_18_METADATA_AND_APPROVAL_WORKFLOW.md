# Phase 18 — Metadata Generation & Approval Workflow

## Status

Not Started

---

## Objective

Generate platform-ready publishing copy and establish the final approval gate before anything may be scheduled or published.

---

## Metadata Generation

Gemma generates editable suggestions for:

- Title.
- Description.
- Social caption.
- Hashtags.
- Keywords/tags where applicable.
- CTA.
- Alternative versions.

Use:

- Clip transcript.
- Topic.
- Brand profile.
- Selected platform.
- Local preferences.

---

## Platform-Specific Metadata

Do not assume identical copy for:

- YouTube.
- Instagram.
- Facebook.

Provider rules/limits should be validated separately.

---

## Approval Workflow

Required state flow:

Generated
↓
Needs Review
↓
Approved

Alternative:

Rejected

No clip can enter publishing workflow without Approved status.

---

## Editing After Approval

Define a clear rule.

Recommended:

Significant edits to media or publishing content after approval move the item back to `Needs Review`.

Minor scheduling-only changes may preserve approval if product rules allow.

Document exact behavior.

---

## Architecture Requirements

AI generates suggestions.

User owns final metadata.

Approval state is deterministic and persisted locally.

---

## Privacy Requirements

Metadata and approvals stay local.

---

## Security Requirements

Do not treat AI-generated links/hashtags as trusted.

Validate platform fields before publishing.

---

## Error Handling Requirements

Handle:

- AI generation failure.
- Metadata too long.
- Invalid characters.
- Empty required field.
- Save failure.
- Regeneration failure.

Never overwrite manually edited/approved metadata without explicit confirmation.

---

## Testing Requirements

Test:

- Generate all fields.
- Regenerate.
- Manual editing.
- Platform variants.
- Brand banned-word handling.
- Approval.
- Rejection.
- Edit after approval.
- Restart persistence.

---

## Acceptance Criteria

- Metadata generated locally.
- User can edit everything.
- Approval gate works.
- Unapproved clips cannot proceed.
- Approved state persists.
- Reapproval rule works.

---

## Real User Validation

Prepare several real clips.

Edit AI-generated titles/captions.

Approve selected clips.

Verify only approved items appear as publishable.

---

## Antigravity Instructions

Do not start social platform upload implementation yet.

Finalize the content package that future publishing adapters consume.

---

## Completion Report Requirements

Report:

- Metadata schemas.
- Prompt strategy.
- Approval state machine.
- Validation.
- Tests.

---

## Phase Completion Rule

The product must have a trustworthy human approval boundary before any social-account integration can perform publishing actions.