# Test Plan

## 1. Goal

Prove that the application works as a real user would use it.

Testing must cover:

- Functional behavior.
- Local privacy.
- Local AI.
- Media.
- Scheduling.
- Publishing.
- Recovery.
- Security.
- Performance.

---

# 2. Authentication

Test:

- Valid email/password/key.
- Invalid email.
- Invalid password.
- Invalid activation key.
- Expired activation.
- Network unavailable.
- Session expiration.
- Logout.
- App restart with valid session.

Verify:

- Password not stored plaintext.
- User content not included in authentication requests.

---

# 3. Ollama Already Installed

Test:

App starts
→ Ollama detected
→ Ollama starts silently if needed
→ health passes
→ model available
→ application ready

Verify no terminal window appears.

---

# 4. Ollama Already Running

Test:

Start Ollama outside app.
Open agent.
Close agent.

Expected:

Existing Ollama process remains running.

---

# 5. Ollama Missing

Test first-run setup.

Expected:

- Missing state detected.
- User receives clean setup experience.
- Runtime installation succeeds.
- App continues.
- Model preparation starts.

Test installation failure.

Expected:
clear retry/error state.

---

# 6. Model Present

Expected:

Do not download again.

AI health test passes.

---

# 7. Model Missing

Expected:

- Download starts.
- Progress visible.
- App remains responsive.
- Interrupted download handled.
- Retry available.
- Final model verification passes.

---

# 8. Ollama Shutdown

Scenario A:

App started Ollama.

Expected:
App may stop it on application exit after safe cleanup.

Scenario B:

Ollama existed before app.

Expected:
App must not kill it.

---

# 9. Privacy Network Test

Monitor outgoing network traffic.

Confirm user content is never sent to Nexus.

Verify Nexus requests contain only required account/license/session information.

Test that:

- transcript does not leave.
- video does not leave.
- clip does not leave.
- analytics do not leave.
- search history does not leave to Nexus.
- prompt does not leave to Nexus.

---

# 10. Discovery

Test:

- No search text.
- Keyword.
- Channel name.
- Creator name.
- One niche.
- Multiple niches.
- Fresh content.
- Empty results.
- Provider unavailable.

Expected:
Five primary results when sufficient results exist.

---

# 11. Multi-Niche

Gaming + Podcast + News.

Verify:
reasonable category diversity.

Do not require impossible equal distribution when data is unavailable.

---

# 12. Source Selection

Test:

- Open on YouTube.
- Select source.
- Return to application.
- Persist selection.

---

# 13. Rights Confirmation

Without confirmation:
analysis blocked.

With confirmation:
analysis allowed.

Verify local-only storage.

---

# 14. Clip Duration

Boundary tests:

9 → rejected

10 → accepted

15 → accepted

60 → accepted

120 → accepted

121 → rejected

null → rejected

invalid text → rejected

---

# 15. Media Validation

Test:

- Normal video.
- Long video.
- Unsupported codec.
- Corrupt video.
- Missing audio.
- Audio-only.
- Invalid URL/source.
- Interrupted acquisition.
- Insufficient disk space.

---

# 16. Transcription

Test:

- Clear speech.
- Multiple speakers.
- Background music.
- Silence.
- Poor audio.
- Very long video.
- No speech.

Verify timestamps.

---

# 17. Analysis

Verify:

- Full source considered.
- AI returns schema-valid output.
- Invalid AI output recovered.
- Timeout recovered.
- No candidate outside video bounds.
- No negative timestamps.

---

# 18. Candidate Duration

Every candidate:

start >= 0

end <= source duration

end > start

duration approximately respects user's requested target.

Do not cut mid-sentence unnecessarily.

---

# 19. Candidate Explanation

Verify explanation describes actual clip.

Reject/test hallucinated explanations.

---

# 20. Scoring

Verify:

- Score exists.
- Component scores exist.
- Ranking works.
- Missing optional signals do not crash.
- Duplicate candidates receive penalty/removal.

---

# 21. Rendering

Test:

- 9:16 output.
- Correct trim.
- Audio sync.
- Captions.
- Logo.
- Watermark.
- Cover.
- Crop.
- Re-render.

Verify playable file.

---

# 22. Captions

Test:

- Timing.
- Long sentence.
- Multi-line.
- Correction.
- Special characters.
- Emoji if supported.
- Multiple languages if supported later.
- Safe area.

---

# 23. Manual Editing

Verify:

- Start changes persist.
- End changes persist.
- Caption edit persists.
- Crop edit persists.
- Cover persists.
- New version created appropriately.

---

# 24. Metadata

Verify:

- Title.
- Caption.
- Description.
- Hashtags.
- CTA.
- Platform variants.
- Manual edit.
- Regeneration.

AI should not silently overwrite approved user edits.

---

# 25. Approval

Generated:
cannot publish.

Approved:
can schedule.

Rejected:
cannot publish unless status changed.

Editing approved content must follow defined reapproval behavior.

---

# 26. OAuth / Social Connections

Test:

- Successful connection.
- User rejects consent.
- Expired token.
- Revoked token.
- Missing permissions.
- Invalid account.
- Reconnection.

---

# 27. Scheduler

Test:

- One clip.
- Ten clips.
- Different dates.
- Different times.
- Different platforms.
- Different timezones.
- Reschedule.
- Cancel.
- App restart.

Schedule must persist.

---

# 28. PC Offline

At scheduled time:

Network unavailable.

Expected:

- Job remains queued.
- Failure recorded.
- Safe retry later.

---

# 29. PC Powered Off

Test documented behavior.

If platform scheduling was already submitted:
platform handles it.

If local execution was required:
job executes appropriately when app/system becomes available according to defined rules.

Never claim a powered-off computer executed a local API request.

---

# 30. Publishing

Test each platform adapter:

- Valid upload.
- Invalid media.
- Invalid metadata.
- Rate limit.
- Network failure.
- Authentication expired.
- Platform processing failure.
- Successful post.

---

# 31. Duplicate Prevention

Critical:

Simulate app crash after platform accepts upload but before local success was saved.

Restart.

Verify retry does not create a duplicate post when status can be reconciled.

---

# 32. Analytics

Test:

- Successful metrics retrieval.
- Missing metric.
- Unsupported metric.
- Auth failure.
- Rate limit.
- Sync retry.
- Historical snapshots.

Missing metric != zero.

---

# 33. Local Learning

Verify:

- Correct client's analytics used.
- Client A data not used for Client B.
- Empty history works.
- Recommendation includes reasoning/evidence where possible.

---

# 34. Security

Test:

- Malicious filename.
- Malicious URL.
- Path traversal.
- Prompt injection in transcript.
- Prompt injection in YouTube description.
- Oversized input.
- Invalid media.
- Token theft attempts.
- Unauthorized local data access paths where practical.

---

# 35. UI

Verify:

- Loading states.
- Error states.
- Empty states.
- Keyboard navigation.
- Resize.
- High DPI.
- Multiple screen resolutions.
- Long text.
- Slow machine.

---

# 36. Performance

Benchmark:

- App startup.
- Ollama startup.
- Model warm-up.
- 10-minute video.
- 30-minute video.
- 60-minute video.
- Transcription.
- Analysis.
- Rendering.
- Memory usage.
- VRAM usage.
- CPU usage.
- Disk usage.

---

# 37. Application Exit

Test exit during:

- Model download.
- Analysis.
- Rendering.
- Upload.
- Idle.

Ensure:

- Files not corrupted.
- Database consistent.
- Ollama ownership rule respected.

---

# 38. Full E2E Test

Open app
→ Authenticate
→ Ollama ready
→ Gemma ready
→ Discover
→ Select source
→ Confirm rights
→ Choose 60 sec
→ Analyze
→ Generate candidates
→ Preview
→ Edit
→ Approve
→ Generate metadata
→ Connect platform
→ Schedule
→ Publish
→ Verify
→ Analytics

This test must pass before production release.

---

# 39. Release Gate

Production candidate requires:

- Unit tests pass.
- Integration tests pass.
- E2E tests pass.
- Privacy test passes.
- Security review passes.
- Packaging test passes.
- Clean-machine installation tested.
- Upgrade tested.
- Uninstall tested.