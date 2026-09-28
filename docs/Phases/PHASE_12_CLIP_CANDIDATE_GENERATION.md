# Phase 12 — Clip Candidate Generation

## Status

Not Started

---

## Objective

Convert full-video understanding into multiple coherent short-form candidate segments based on the user-selected duration.

---

## Core Rule

Do not:

00:00–01:00
01:00–02:00
02:00–03:00

blindly.

Candidates must be semantically selected.

---

## Candidate Requirements

Each candidate includes:

- Candidate ID.
- Source ID.
- Start timestamp.
- End timestamp.
- Duration.
- Transcript excerpt.
- Summary.
- Hook type.
- Main payoff.
- Context dependency.
- Reason for candidate selection.
- Warning flags.

Scoring is Phase 13.

---

## Boundary Selection

The system should:

- Start near natural sentence/story boundaries.
- Avoid cutting a sentence unnecessarily.
- Include enough context.
- Reach a payoff.
- Respect requested duration as closely as sensible.
- Never exceed source boundaries.

---

## Duration Behavior

A 60-second request does not necessarily mean every clip must be exactly 60.000 seconds.

Use a reasonable tolerance when a natural boundary improves the result.

But never ignore the requested duration completely.

---

## Candidate Diversity

Avoid generating 10 nearly identical overlapping clips.

Candidates should represent distinct meaningful moments.

---

## Architecture Requirements

Gemma proposes semantic ranges.

A deterministic validator checks:

- Valid timestamps.
- Duration.
- Overlap.
- Source bounds.
- Transcript mapping.

---

## Privacy Requirements

All candidates stored locally.

---

## Security Requirements

AI-generated timestamps are untrusted until validated.

Never pass arbitrary model text directly into FFmpeg.

---

## Error Handling Requirements

Handle:

- Invalid timestamp.
- End before start.
- Out-of-range time.
- Candidate too short.
- Candidate too long.
- Excessive overlap.
- Missing transcript reference.

---

## Testing Requirements

Test requested durations:

- 15 sec.
- 30 sec.
- 60 sec.
- 90 sec.
- 120 sec.

Test:

- Short source.
- Long source.
- One strong moment.
- Many strong moments.
- Low-value source.
- Highly repetitive source.

---

## Acceptance Criteria

- Multiple coherent candidates generated.
- Timestamp validation passes.
- Candidate set is reasonably diverse.
- User-selected duration meaningfully influences output.
- Candidates map to actual source content.
- No rendering performed yet.

---

## Real User Validation

Use a 15–30 minute authorized source.

Choose 60 seconds.

Listen/watch proposed candidate ranges manually.

Confirm they make sense independently.

---

## Antigravity Instructions

Focus on candidate quality and boundary correctness.

Do not add visual rendering or publishing.

---

## Completion Report Requirements

Include:

- Candidate algorithm.
- Boundary logic.
- Duration tolerance.
- Deduplication logic.
- Candidate samples.
- Tests.

---

## Phase Completion Rule

Candidate timestamps must be trustworthy before scoring or rendering.