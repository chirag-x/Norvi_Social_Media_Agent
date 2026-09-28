# Phase 10 — Local Transcription & Timeline Intelligence

## Status

Not Started

---

## Objective

Convert source media into a structured chronological representation that later AI phases can understand efficiently.

---

## Scope

Implement local:

- Audio extraction.
- Speech transcription.
- Timestamped transcript.
- Silence/dead-air detection.
- Scene detection.
- Keyframe extraction.
- Optional basic speaker segmentation where practical.
- Timeline artifact storage.
- Background progress.

---

## Transcription Requirement

Use a local, zero-mandatory-cost transcription solution.

Recommended current family:

faster-whisper or another approved local engine.

Do not use a paid speech API.

---

## Timeline Representation

Create structured artifacts such as:

TranscriptSegment:
- start
- end
- text
- confidence where available

SceneSegment:
- start
- end
- keyframe reference

SilenceSegment:
- start
- end

SpeakerSegment where available.

---

## Architecture Requirements

Transcription is not Gemma's responsibility.

Scene detection is not Gemma's responsibility.

Use deterministic/local specialized tools first.

Gemma receives the structured result later.

---

## Performance Requirements

Long videos must run in a background worker.

The UI must show meaningful progress stages.

Avoid loading an entire huge media file into memory unnecessarily.

---

## Privacy Requirements

Transcript stays local.

Extracted audio stays local.

Keyframes stay local.

No Norvi upload.

---

## Security Requirements

Temporary extracted audio and frames must use safe internal paths.

Clean unneeded temporary artifacts.

---

## Error Handling Requirements

Handle:

- No audio.
- Unsupported audio.
- Transcription model unavailable.
- Out of memory.
- Worker cancelled.
- Scene detector error.
- Partial result.
- Low-confidence transcript.

Do not lose already valid media source state.

---

## Testing Requirements

Use samples:

- Clear speech.
- Multiple speakers.
- Silence.
- Background music.
- Gaming content.
- Interview.
- Poor audio.
- No audio.
- Long video.

Verify timestamps remain within source duration.

---

## Acceptance Criteria

- Transcript generated locally.
- Transcript timestamps valid.
- Scene data generated.
- Keyframes generated.
- Long task does not freeze UI.
- Job state persists correctly.
- Phase 9 remains stable.

---

## Real User Validation

Analyze a real authorized 10–20 minute sample.

Review transcript and timeline manually.

Verify major speech and scene transitions align with the source.

---

## Antigravity Instructions

Do not generate clips yet.

The output of this phase should be high-quality structured input for the AI.

---

## Completion Report Requirements

Include:

- Transcription engine.
- Models/config.
- Processing speed.
- Scene method.
- Accuracy observations.
- Test results.

---

## Phase Completion Rule

Do not proceed until the application can reliably create a usable full-video timeline.