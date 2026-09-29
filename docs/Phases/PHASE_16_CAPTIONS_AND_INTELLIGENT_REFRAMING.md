# Phase 16 — Captions & Intelligent Reframing

## Status

Not Started

---

## Objective

Transform basic rendered clips into polished short-form vertical videos with readable captions and intelligent framing.

---

## Caption Features

Implement:

- Caption segments from transcript.
- Timing alignment.
- Subtitle correction UI.
- Style presets.
- Position.
- Size.
- Line wrapping.
- Safe areas.
- Optional highlighted current word.
- Rendered subtitles.

---

## Reframing Features

Implement a practical baseline for:

- Horizontal-to-vertical conversion.
- Subject detection.
- Main-person tracking where available.
- Active speaker awareness where practical.
- Smooth crop movement.
- Manual crop override.

Do not make advanced tracking mandatory if it makes the basic feature unreliable.

---

## User Control

User can override:

- Crop position.
- Caption style.
- Caption text.
- Caption placement.

AI/vision suggestions never remove manual control.

---

## Architecture Requirements

Keep:

- Caption generation.
- Caption rendering.
- Subject tracking.
- Reframing.

as separate modules.

Do not embed everything in one FFmpeg function.

---

## Privacy Requirements

Vision/tracking is local.

No frame upload to Nexus.

---

## Error Handling Requirements

Handle:

- No subject detected.
- Multiple subjects.
- Tracking lost.
- Transcript mismatch.
- Caption too long.
- Unsupported characters.
- Render failure.

Fallback:

Use safe center/manual crop rather than fail the entire clip.

---

## Testing Requirements

Test:

- One speaker.
- Two speakers.
- Gaming screen.
- Screen recording.
- Moving person.
- No person.
- Long captions.
- Fast speech.
- Silence.

---

## Acceptance Criteria

- Captions readable and synchronized.
- Vertical result looks acceptable.
- Main subject usually remains visible.
- Manual override works.
- Tracking failure has fallback.
- Render remains deterministic.

---

## Real User Validation

Produce at least:

- Podcast clip.
- Gaming clip.
- Talking-head clip.

Watch on a phone-sized viewport.

Verify caption placement and framing.

---

## Antigravity Instructions

Optimize for reliability first.

Do not introduce expensive paid vision APIs.

---

## Completion Report Requirements

Report:

- Caption engine.
- Tracking/reframing approach.
- Fallback strategy.
- Tests.
- Example results.

---

## Phase Completion Rule

Generated clips must look like real short-form content before branding and hooks are added.