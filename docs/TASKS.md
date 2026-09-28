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

- [x] Initialize Python 3.13.15 project.
- [x] Create virtual environment.
- [x] Create source structure.
- [x] Configure Git.
- [x] Configure formatting.
- [x] Configure linting.
- [x] Configure tests.
- [x] Configure logging.
- [x] Create config system.
- [x] Add environment validation.
- [x] Add basic application startup.
- [x] Add CI if desired.

Tests:

- [x] Clean install.
- [x] App starts.
- [x] Tests run.
- [x] Lint passes.
- [x] Python version validated.

---

# Phase 2 — Desktop Application Shell

- [x] Main window.
- [x] Sidebar.
- [x] Navigation.
- [x] Dashboard.
- [x] Settings.
- [x] Loading components.
- [x] Error components.
- [x] Notification system.
- [x] Background worker foundation.

---

# Phase 3 — Norvi Authentication Boundary

- [x] Login UI.
- [x] Email field.
- [x] Password field.
- [x] Activation/API key field.
- [x] Auth client.
- [x] Session/token handling.
- [x] Logout.
- [x] License state.
- [x] Secure token storage.
- [x] No plaintext password persistence.

Do NOT implement the Norvi server/license backend itself.

---

# Phase 4 — Ollama Runtime Manager

- [x] Detect Ollama.
- [x] Detect running Ollama.
- [x] Start silently.
- [x] Health check.
- [x] Track process ownership.
- [x] Safe stop.
- [x] Handle existing external instance.
- [x] First-run installation flow.
- [x] Installation error state.
- [x] No visible terminal window in normal use.

Critical test:

App must not kill an Ollama instance that existed before app startup.

---

# Phase 5 — Gemma Model Manager

- [x] Define exact model ID/config.
- [x] List local models.
- [x] Detect required model.
- [x] Pull missing model.
- [x] Show download progress.
- [x] Handle interrupted download.
- [x] Verify model.
- [x] AI smoke test.
- [x] Ready state.

---

# Phase 6 — Local Privacy Storage

- [x] Application data directories.
- [x] Local SQLite database.
- [x] Schema versioning.
- [x] Secure credentials.
- [ ] Client/brand models.
- [x] Local settings.
- [x] Project model.
- [ ] Privacy controls.
- [ ] Cleanup policy.

---

# Phase 7 — YouTube Discovery

- [x] Discovery provider interface.
- [x] YouTube implementation.
- [x] Search field.
- [x] Niche multi-select.
- [x] Freshness logic.
- [x] Result normalization.
- [x] Result ranking.
- [x] Multi-niche diversification.
- [x] Top-five presentation.
- [x] Open-on-YouTube action.
- [x] Select source.

---

# Phase 8 — Source & Rights Workflow

- [x] Selected-source page.
- [x] Source metadata.
- [x] Rights confirmation.
- [x] Duration selector.
- [x] 10-second minimum.
- [x] 120-second maximum.
- [x] Start-analysis action.

---

# Phase 9 — Media Preparation

- [x] Approved source acquisition method.
- [x] Media validation.
- [x] FFmpeg probe.
- [x] Audio extraction.
- [x] Keyframe generation.
- [x] Checksums.
- [x] Local source storage.
- [x] Cleanup.

---

# Phase 10 — Transcription and Video Understanding

- [x] Local transcription.
- [x] Timestamped transcript.
- [x] Scene detection.
- [x] Silence detection.
- [x] Keyframe extraction.
- [x] Topic segmentation.
- [x] Optional speaker detection.
- [x] Structured analysis representation.

---

# Phase 11 — Gemma Analysis Engine

- [x] AI gateway.
- [x] Prompt architecture.
- [x] Structured response schemas.
- [x] Complete-source reasoning.
- [x] Candidate generation.
- [x] Boundary suggestions.
- [x] Explanation.
- [x] Safety/context flags.

---

# Phase 12 — Candidate Ranking

- [x] Hook score.
- [x] Clarity score.
- [x] Novelty.
- [x] Emotional strength.
- [x] Payoff.
- [x] Standalone score.
- [x] Pacing.
- [x] Visual interest.
- [x] Duplicate penalty.
- [x] Context penalty.
- [x] Final score.
- [x] Ranking.

---

# Phase 13 — Clip Lab

- [x] Candidate cards.
- [x] Preview.
- [x] Score.
- [x] Explanation.
- [x] Sort.
- [x] Filter.
- [x] Approve.
- [x] Reject.
- [x] Save state.

---

# Phase 14 — Video Rendering

- [x] Exact trim.
- [x] 9:16 output.
- [x] Reframing.
- [ ] Subject tracking baseline.
- [ ] Audio normalization.
- [x] Export.
- [ ] Render validation.
- [ ] Version tracking.

---

# Phase 15 — Captions

- [x] Caption timing.
- [x] Caption renderer.
- [x] Highlight styles.
- [x] Caption editor.
- [x] Safe areas.
- [ ] Brand caption presets.
- [ ] Re-render.

---

# Phase 16 — Hook / Cover / Branding

- [x] Dead-air removal suggestion.
- [x] Hook suggestions.
- [x] Alternative start suggestions.
- [x] Cover frame recommendations.
- [x] Manual cover selection.
- [x] Logo/watermark.
- [x] Brand defaults.

---

# Phase 17 — Metadata

- [x] Titles.
- [x] Descriptions.
- [x] Captions.
- [x] Hashtags.
- [x] CTAs.
- [x] Alternative versions.
- [x] Platform-specific variants.
- [x] Editable UI.

---

# Phase 18 — Approval Workflow

- [x] Generated.
- [x] Needs Review.
- [x] Approved.
- [x] Rejected.
- [x] Approval persistence.
- [ ] Reapproval behavior after editing.
- [ ] Local audit history.

---

# Phase 19 — Social Account Integrations

- [x] Platform adapter interface.
- [x] Secure OAuth credentials.
- [x] Account connection UI.
- [x] Connection status.
- [x] Token refresh.
- [x] Re-authentication.

Then implement:

- [ ] YouTube.
- [ ] Instagram.
- [ ] Facebook.

---

# Phase 20 — Scheduler

- [x] Local schedule database.
- [x] Date/time.
- [ ] Timezone.
- [ ] Per-clip schedule.
- [ ] Per-platform schedule.
- [ ] Reschedule.
- [ ] Cancel.
- [x] Calendar UI.
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

- [x] Clip fingerprint.
- [x] Source-segment comparison.
- [x] Previously scheduled check.
- [ ] Previously published check.
- [x] Warning.
- [x] User override.

---

# Phase 23 — Content Series

- [x] Related clip detection.
- [x] Series grouping.
- [x] Part numbers.
- [x] Reorder.
- [x] Rename.
- [x] Ungroup.

---

# Phase 24 — Local Analytics

- [x] Analytics provider abstraction.
- [ ] YouTube metrics.
- [ ] Instagram metrics.
- [ ] Facebook metrics.
- [x] Local snapshots.
- [x] Analytics UI.
- [x] Refresh/sync.

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