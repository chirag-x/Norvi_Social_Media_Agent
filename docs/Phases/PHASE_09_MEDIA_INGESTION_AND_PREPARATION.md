# Phase 9 — Media Ingestion & Preparation

## Status

Not Started

---

## Objective

Create a safe, compliant, local media preparation pipeline that turns an authorized selected source into local media artifacts suitable for analysis.

---

## Important Rule

Do not implement mechanisms that bypass access controls, DRM, authentication restrictions, or platform protections.

Source acquisition must use an approved method appropriate to content the user owns or is authorized to process.

Where direct provider-supported acquisition is unavailable, support a user-provided authorized local source file or another compliant workflow rather than pretending an unsupported route is safe.

---

## Scope

Implement:

- Source preparation job.
- Media source abstraction.
- Local-file source support.
- Approved provider source support where available.
- Media probing.
- Validation.
- Checksum.
- Metadata extraction.
- Local managed copy/reference.
- Proxy generation if required.
- Audio extraction foundation.
- Cleanup rules.

---

## Media Metadata

Capture:

- Duration.
- Resolution.
- Frame rate.
- Audio availability.
- Container.
- Codec information where needed.
- File size.
- Local source identifier.
- Checksum.

---

## Architecture Requirements

Create a dedicated ingestion/media-source layer.

Do not put acquisition logic in:

- YouTube discovery UI.
- AI gateway.
- Rendering service.

---

## Privacy Requirements

Media stays local except communication explicitly required with the original authorized source provider.

Never upload source media to Nexus.

---

## Security Requirements

Validate:

- Path.
- Extension.
- Actual media structure.
- Size.
- Duration.
- Safe filenames.

Do not trust the extension alone.

Use application-owned temporary paths.

---

## Error Handling Requirements

Handle:

- Unsupported format.
- Corrupt file.
- Missing file.
- Source unavailable.
- Disk full.
- Permission error.
- Partial transfer.
- FFmpeg/probe unavailable.
- Cancelled operation.

Never mark a partial file as ready.

---

## Testing Requirements

Test:

- Valid MP4.
- Other supported format.
- Corrupt file.
- Zero-byte file.
- Missing audio.
- Very long video.
- Unicode filename.
- Malicious filename/path.
- Disk failure simulation where practical.

---

## Acceptance Criteria

- Valid source becomes usable local media.
- Metadata is correct.
- Invalid media rejected.
- Original remains immutable.
- Partial operations do not corrupt state.
- Cleanup works.
- User data remains local.

---

## Real User Validation

Process an authorized sample video through the real app.

Verify:

- Source is recognized.
- Metadata is displayed/stored.
- Application stays responsive.
- Prepared source is usable by Phase 10.

---

## Antigravity Instructions

Do not add transcript/AI logic yet.

Focus on robust local source preparation.

---

## Completion Report Requirements

Include:

- Supported source paths.
- Media formats tested.
- FFmpeg/probe behavior.
- Local storage behavior.
- Failures tested.

---

## Phase Completion Rule

Only verified media may proceed to transcription.