# Phase 24 — Duplicate Detection, Content Series & Reliability

## Status

Not Started

---

## Objective

Strengthen the complete content workflow so that large-scale agency usage does not accidentally publish duplicates, lose work, or become difficult to organize.

---

## Part A — Duplicate Detection

Detect:

- Exact same clip.
- Same rendered file.
- Same source range.
- Highly overlapping source range.
- Already scheduled clip.
- Already published clip.
- Near-duplicate clip where practical.

Use combinations of:

- Checksums.
- Source IDs.
- Timestamp ranges.
- Clip fingerprints.
- Local publish history.

---

## User Behavior

When duplicate found:

Warn user.

Show existing related content.

Allow intentional override where appropriate.

Do not silently block legitimate reposting forever.

---

## Part B — Content Series

Detect/group related clips.

Example:

Part 1
Part 2
Part 3

User can:

- Accept.
- Rename.
- Reorder.
- Ungroup.
- Change part number.

---

## Part C — Reliability Hardening

Perform broad fault testing across:

- Analysis jobs.
- Rendering jobs.
- Schedules.
- Publishing jobs.
- App restart.
- Worker crash.
- Disk errors.
- Internet loss.
- Token expiry.

Ensure state machines recover consistently.

---

## Architecture Requirements

Duplicate detection is reusable across all publishing adapters.

Series grouping is local content organization, not platform-specific.

---

## Privacy Requirements

Fingerprints and content history stay local.

---

## Security Requirements

Do not expose local clip hashes/data to Nexus.

---

## Testing Requirements

Critical cases:

- Exact same clip twice.
- Same clip different filename.
- Same source range rendered twice.
- Similar overlapping ranges.
- Legitimate intentional repost.
- Queue replay.
- App crash during publish.
- Restart during render.
- Network recovery.

---

## Acceptance Criteria

- Duplicate warning works.
- User can intentionally override.
- Series works.
- State recovery works.
- No lost publish jobs.
- No silent stuck states.
- Existing published history remains consistent.

---

## Real User Validation

Create 10+ clips from one source.

Schedule several.

Attempt duplicate scheduling.

Create a series.

Restart app during controlled workflow.

Confirm recovery.

---

## Antigravity Instructions

This phase is not for adding new flashy features.

Focus on reliability of what already exists.

Any discovered regression must be fixed and retested.

---

## Completion Report Requirements

Report:

- Fingerprinting strategy.
- Duplicate rules.
- Series behavior.
- Recovery scenarios tested.
- Bugs found/fixed.
- Full regression results.

---

## Phase Completion Rule

The application should now behave safely under realistic repeated agency use.