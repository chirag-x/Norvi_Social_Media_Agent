# Phase 15 — Deterministic Video Rendering

## Status

Not Started

---

## Objective

Turn approved candidate timestamps into real local video files using deterministic media processing.

---

## Core Principle

Gemma decides what segment is interesting.

A deterministic media engine performs the exact cut.

---

## Scope

Implement:

- Render job.
- Exact clip extraction.
- Audio/video synchronization.
- Base vertical 9:16 output.
- Resolution configuration.
- Audio normalization baseline.
- Encoding.
- Output validation.
- Clip versioning.
- Preview output.
- Render progress.

Advanced captions/reframing are Phase 16.

---

## Output Requirements

Every render should record:

- Clip version ID.
- Source ID.
- Input timestamps.
- Render configuration.
- Output path.
- Output duration.
- Dimensions.
- File checksum where useful.
- Created time.

---

## Architecture Requirements

Central `MediaEngine` / FFmpeg wrapper.

Do not scatter raw FFmpeg command strings across the project.

Render jobs run in background.

Original media remains untouched.

---

## Privacy Requirements

Rendering is fully local.

---

## Security Requirements

Validate all paths and parameters before constructing media commands.

Prefer safe subprocess argument handling.

Do not execute arbitrary AI-generated FFmpeg commands.

---

## Error Handling Requirements

Handle:

- FFmpeg missing.
- Encoder unavailable.
- Invalid input.
- Disk full.
- Worker cancelled.
- Output corrupt.
- Invalid duration.
- Permission error.

Do not destroy previous good render after a failed re-render.

---

## Testing Requirements

Validate output:

- File exists.
- Playable.
- Correct approximate duration.
- Expected dimensions.
- Audio present where expected.
- No A/V drift for sample clips.

Test multiple source resolutions and frame rates.

---

## Acceptance Criteria

Approved clip can render successfully.

Generated file is valid.

Rendering doesn't block UI.

Render failure is recoverable.

Original media is intact.

---

## Real User Validation

Render several candidate clips from real media.

Play them in the app and an external media player.

Verify exact content boundaries manually.

---

## Antigravity Instructions

No AI should control raw rendering commands.

Keep the render layer deterministic and independently testable.

---

## Completion Report Requirements

Report:

- FFmpeg strategy.
- Encoding settings.
- Render time.
- Output validation.
- Tests.
- Sample real results.

---

## Phase Completion Rule

Basic reliable clips must render before advanced visual treatment begins.