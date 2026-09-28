# Tasks

## Current Project Status

Planning complete enough to begin technical setup after final stack confirmation.

---

# Phase 0 — Final Technology Lock

- [x] Confirm final application name.
- [x] Confirm PySide6 or alternative desktop UI.
- [x] Confirm SQLite implementation.
- [x] Confirm local transcription engine.
- [x] Confirm video scene detection library.
- [x] Confirm FFmpeg packaging strategy.
- [x] Confirm exact Ollama model identifier.
- [x] Confirm YouTube discovery integration.
- [x] Confirm YouTube publishing integration.
- [x] Confirm Meta publishing integration.
- [x] Confirm local scheduler.
- [x] Confirm secure credential storage.
- [x] Update DECISIONS.md.

Exit:
No unresolved foundational choice.

---

# Phase 1 — Project Foundation

- [ ] Initialize Python 3.13.15 project.
- [ ] Create virtual environment.
- [ ] Create source structure.
- [ ] Configure Git.
- [ ] Configure formatting.
- [ ] Configure linting.
- [ ] Configure tests.
- [ ] Configure logging.
- [ ] Create config system.
- [ ] Add environment validation.
- [ ] Add basic application startup.
- [ ] Add CI if desired.

Tests:

- [ ] Clean install.
- [ ] App starts.
- [ ] Tests run.
- [ ] Lint passes.
- [ ] Python version validated.

---

# Phase 2 — Desktop Application Shell

- [ ] Main window.
- [ ] Sidebar.
- [ ] Navigation.
- [ ] Dashboard.
- [ ] Settings.
- [ ] Loading components.
- [ ] Error components.
- [ ] Notification system.
- [ ] Background worker foundation.

---

# Phase 3 — Norvi Authentication Boundary

- [ ] Login UI.
- [ ] Email field.
- [ ] Password field.
- [ ] Activation/API key field.
- [ ] Auth client.
- [ ] Session/token handling.
- [ ] Logout.
- [ ] License state.
- [ ] Secure token storage.
- [ ] No plaintext password persistence.

Do NOT implement the Norvi server/license backend itself.

---

# Phase 4 — Ollama Runtime Manager

- [ ] Detect Ollama.
- [ ] Detect running Ollama.
- [ ] Start silently.
- [ ] Health check.
- [ ] Track process ownership.
- [ ] Safe stop.
- [ ] Handle existing external instance.
- [ ] First-run installation flow.
- [ ] Installation error state.
- [ ] No visible terminal window in normal use.

Critical test:

App must not kill an Ollama instance that existed before app startup.

---

# Phase 5 — Gemma Model Manager

- [ ] Define exact model ID/config.
- [ ] List local models.
- [ ] Detect required model.
- [ ] Pull missing model.
- [ ] Show download progress.
- [ ] Handle interrupted download.
- [ ] Verify model.
- [ ] AI smoke test.
- [ ] Ready state.

---

# Phase 6 — Local Privacy Storage

- [ ] Application data directories.
- [ ] Local SQLite database.
- [ ] Schema versioning.
- [ ] Secure credentials.
- [ ] Client/brand models.
- [ ] Local settings.
- [ ] Project model.
- [ ] Privacy controls.
- [ ] Cleanup policy.

---

# Phase 7 — YouTube Discovery

- [ ] Discovery provider interface.
- [ ] YouTube implementation.
- [ ] Search field.
- [ ] Niche multi-select.
- [ ] Freshness logic.
- [ ] Result normalization.
- [ ] Result ranking.
- [ ] Multi-niche diversification.
- [ ] Top-five presentation.
- [ ] Open-on-YouTube action.
- [ ] Select source.

---

# Phase 8 — Source & Rights Workflow

- [ ] Selected-source page.
- [ ] Source metadata.
- [ ] Rights confirmation.
- [ ] Duration selector.
- [ ] 10-second minimum.
- [ ] 120-second maximum.
- [ ] Start-analysis action.

---

# Phase 9 — Media Preparation

- [ ] Approved source acquisition method.
- [ ] Media validation.
- [ ] FFmpeg probe.
- [ ] Audio extraction.
- [ ] Keyframe generation.
- [ ] Checksums.
- [ ] Local source storage.
- [ ] Cleanup.

---

# Phase 10 — Transcription and Video Understanding

- [ ] Local transcription.
- [ ] Timestamped transcript.
- [ ] Scene detection.
- [ ] Silence detection.
- [ ] Keyframe extraction.
- [ ] Topic segmentation.
- [ ] Optional speaker detection.
- [ ] Structured analysis representation.

---

# Phase 11 — Gemma Analysis Engine

- [ ] AI gateway.
- [ ] Prompt architecture.
- [ ] Structured response schemas.
- [ ] Complete-source reasoning.
- [ ] Candidate generation.
- [ ] Boundary suggestions.
- [ ] Explanation.
- [ ] Safety/context flags.

---

# Phase 12 — Candidate Ranking

- [ ] Hook score.
- [ ] Clarity score.
- [ ] Novelty.
- [ ] Emotional strength.
- [ ] Payoff.
- [ ] Standalone score.
- [ ] Pacing.
- [ ] Visual interest.
- [ ] Duplicate penalty.
- [ ] Context penalty.
- [ ] Final score.
- [ ] Ranking.

---

# Phase 13 — Clip Lab

- [ ] Candidate cards.
- [ ] Preview.
- [ ] Score.
- [ ] Explanation.
- [ ] Sort.
- [ ] Filter.
- [ ] Approve.
- [ ] Reject.
- [ ] Save state.

---

# Phase 14 — Video Rendering

- [ ] Exact trim.
- [ ] 9:16 output.
- [ ] Reframing.
- [ ] Subject tracking baseline.
- [ ] Audio normalization.
- [ ] Export.
- [ ] Render validation.
- [ ] Version tracking.

---

# Phase 15 — Captions

- [ ] Caption timing.
- [ ] Caption renderer.
- [ ] Highlight styles.
- [ ] Caption editor.
- [ ] Safe areas.
- [ ] Brand caption presets.
- [ ] Re-render.

---

# Phase 16 — Hook / Cover / Branding

- [ ] Dead-air removal suggestion.
- [ ] Hook suggestions.
- [ ] Alternative start suggestions.
- [ ] Cover frame recommendations.
- [ ] Manual cover selection.
- [ ] Logo/watermark.
- [ ] Brand defaults.

---

# Phase 17 — Metadata

- [ ] Titles.
- [ ] Descriptions.
- [ ] Captions.
- [ ] Hashtags.
- [ ] CTAs.
- [ ] Alternative versions.
- [ ] Platform-specific variants.
- [ ] Editable UI.

---

# Phase 18 — Approval Workflow

- [ ] Generated.
- [ ] Needs Review.
- [ ] Approved.
- [ ] Rejected.
- [ ] Approval persistence.
- [ ] Reapproval behavior after editing.
- [ ] Local audit history.

---

# Phase 19 — Social Account Integrations

- [ ] Platform adapter interface.
- [ ] Secure OAuth credentials.
- [ ] Account connection UI.
- [ ] Connection status.
- [ ] Token refresh.
- [ ] Re-authentication.

Then implement:

- [ ] YouTube.
- [ ] Instagram.
- [ ] Facebook.

---

# Phase 20 — Scheduler

- [ ] Local schedule database.
- [ ] Date/time.
- [ ] Timezone.
- [ ] Per-clip schedule.
- [ ] Per-platform schedule.
- [ ] Reschedule.
- [ ] Cancel.
- [ ] Calendar UI.
- [ ] Persistent execution.

---

# Phase 21 — Publishing Queue

- [ ] Job state machine.
- [ ] Durable queue.
- [ ] Idempotency key.
- [ ] Retry policy.
- [ ] Failure classification.
- [ ] Publish verification.
- [ ] External post ID.
- [ ] External URL.
- [ ] Queue UI.

---

# Phase 22 — Duplicate Detection

- [ ] Clip fingerprint.
- [ ] Source-segment comparison.
- [ ] Previously scheduled check.
- [ ] Previously published check.
- [ ] Warning.
- [ ] User override.

---

# Phase 23 — Content Series

- [ ] Related clip detection.
- [ ] Series grouping.
- [ ] Part numbers.
- [ ] Reorder.
- [ ] Rename.
- [ ] Ungroup.

---

# Phase 24 — Local Analytics

- [ ] Analytics provider abstraction.
- [ ] YouTube metrics.
- [ ] Instagram metrics.
- [ ] Facebook metrics.
- [ ] Local snapshots.
- [ ] Analytics UI.
- [ ] Refresh/sync.

---

# Phase 25 — Local Recommendation Engine

- [ ] Best duration suggestions.
- [ ] Best posting-time suggestions.
- [ ] Best hook-type suggestions.
- [ ] Topic suggestions.
- [ ] Evidence display.
- [ ] Client isolation.
- [ ] Empty-history behavior.

---

# Phase 26 — Privacy Verification

- [ ] Network audit.
- [ ] Ensure no user content sent to Norvi.
- [ ] No telemetry.
- [ ] No transcript upload.
- [ ] No analytics upload.
- [ ] No social-history upload.
- [ ] Secure local tokens.
- [ ] Local logs reviewed.

---

# Phase 27 — Security Hardening

- [ ] Input validation.
- [ ] URL validation.
- [ ] SSRF protection.
- [ ] Media validation.
- [ ] Prompt injection defense.
- [ ] Token encryption.
- [ ] Localhost service hardening.
- [ ] Dependency review.
- [ ] Installer validation.
- [ ] Update-security design.

---

# Phase 28 — Performance

- [ ] Long-video benchmark.
- [ ] Gemma benchmark.
- [ ] Transcription benchmark.
- [ ] Rendering benchmark.
- [ ] Concurrent job limits.
- [ ] GPU/CPU resource controls.
- [ ] Disk usage controls.
- [ ] Low-memory behavior.

---

# Phase 29 — Packaging

- [ ] Windows build.
- [ ] Installer.
- [ ] FFmpeg dependency strategy.
- [ ] Ollama bootstrap.
- [ ] Desktop shortcuts.
- [ ] Uninstall.
- [ ] Preserve/delete user data choice.
- [ ] Signed build if available.

---

# Phase 30 — Full End-to-End Validation

Test:

Open application
→ Authenticate
→ Ollama starts
→ Gemma ready
→ Search YouTube
→ Select video
→ Confirm rights
→ Select duration
→ Analyze
→ Generate candidates
→ Preview
→ Edit
→ Approve
→ Generate metadata
→ Connect social account
→ Schedule
→ Publish
→ Verify
→ Fetch analytics

Everything must work through the real application.

---

# Definition of Done

A task is complete only when:

- Required behavior works.
- Relevant tests pass.
- No privacy rule is violated.
- No paid service was accidentally introduced.
- Documentation matches implementation.
- Error states work.
- Existing functionality still works.