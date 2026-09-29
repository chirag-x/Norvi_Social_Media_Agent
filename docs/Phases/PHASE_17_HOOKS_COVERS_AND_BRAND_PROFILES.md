# Phase 17 — Hooks, Covers & Brand Profiles

## Status

Not Started

---

## Objective

Add client-specific branding and AI-assisted presentation improvements without changing the meaning of source content.

---

## Brand Profiles

Support local:

- Brand name.
- Logo.
- Watermark.
- Caption preset.
- Tone.
- Preferred CTA.
- Preferred hashtags.
- Banned words.
- Topics to avoid.
- Preferred clip length.
- Preferred platforms.
- Cover style.

All client/brand data stays local.

---

## Hook Enhancement

Gemma may recommend:

- Remove dead air.
- Start slightly later.
- Open on stronger sentence.
- Add short on-screen hook text.
- Alternative start.

Do not fabricate speech.

Do not modify meaning without user review.

---

## Cover Selection

Generate/recommend multiple frames.

User can:

- Select recommendation.
- Scrub manually.
- Add optional cover title.
- Apply client branding.

---

## Architecture Requirements

Separate:

- Brand service.
- Hook recommendation.
- Cover extraction.
- Cover composition.

Brand profile is applied as configuration, not hardcoded per client.

---

## Privacy Requirements

No brand/client information goes to Nexus.

---

## Error Handling Requirements

Handle:

- Missing logo.
- Invalid image.
- Unsupported font.
- No useful cover frame.
- Hook generation failure.

Core clip should remain usable even if optional enhancement fails.

---

## Testing Requirements

Create at least two different brand profiles.

Verify:

- Client A branding never appears on Client B.
- Captions/logo/cover use correct profile.
- Hook suggestions can be rejected.
- Manual cover works.

---

## Acceptance Criteria

- Brand profiles work locally.
- Clip branding is client-specific.
- Cover recommendations work.
- Hook suggestions are editable/rejectable.
- No semantic fabrication.

---

## Real User Validation

Create two sample client profiles.

Render the same base clip using both.

Verify branding isolation.

---

## Antigravity Instructions

Do not assume one agency style fits every client.

Keep design settings data-driven.

---

## Completion Report Requirements

Report:

- Brand fields.
- Hook workflow.
- Cover workflow.
- Isolation tests.
- Real rendered examples.

---

## Phase Completion Rule

Brand-specific content must remain properly isolated before metadata and approval become final.