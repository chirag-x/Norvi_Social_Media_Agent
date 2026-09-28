# Project Memory

## Product

Working Name:
Norvi Social Media Agent

---

# Current Status

Planning stage.

No production implementation has started yet.

The full product vision has been defined.

The next step is to finalize remaining technology/module decisions and then begin Phase 1.

---

# Current Core Architecture

Windows desktop application.

Python:
3.13.15.

Development:
Google Antigravity.

AI:
Local Gemma 4 31B-class model.

Runtime:
Ollama.

Processing:
Local.

User content storage:
Local.

Norvi server:
Authentication/licensing only.

Paid AI:
None.

---

# Core Workflow

Discover YouTube
↓
Top five
↓
Select source
↓
Confirm usage rights
↓
Choose 10–120 sec
↓
Full analysis
↓
Generate candidate clips
↓
Score + explain
↓
Vertical rendering
↓
Captions
↓
Hooks / covers
↓
Review
↓
Approve
↓
Metadata
↓
Schedule
↓
Publish
↓
Verify
↓
Local analytics
↓
Local recommendations

---

# Privacy Requirement

Norvi must not collect:

- Searches.
- Videos.
- Clips.
- Transcripts.
- AI prompts.
- AI responses.
- Social posts.
- Schedules.
- Social credentials.
- Analytics.
- Brand profiles.
- Client data.

All social-media workflow data stays on the user's machine.

---

# Authentication Requirement

The existing Norvi website/account system supplies:

- Email login.
- Password authentication.
- Activation/API/license key validation.

Desktop app should use session/access tokens after authentication.

Plaintext passwords must not be stored locally.

Activation-system backend implementation is not part of this agent project.

---

# Ollama Requirements

Startup:

Check Ollama.
Install/setup if missing.
Start silently.
Check required model.
Download model if missing.
Verify model.
Agent ready.

Normal user should not see terminal windows.

Shutdown:

Stop Ollama only if this application started that instance.

---

# Video Intelligence

The app analyzes:

- Transcript.
- Scenes.
- Topics.
- Keyframes.
- Important moments.
- Emotional/high-energy moments.
- Hooks.
- Payoffs.
- Context.

Do not split videos blindly.

---

# Generated Clip Requirements

Every candidate needs:

- Start.
- End.
- Duration.
- Preview.
- Score.
- Explanation.
- Warnings.
- Recommendation.

---

# Short-Form Creation

Support:

- 9:16.
- Intelligent crop.
- Captions.
- Audio normalization.
- Branding.
- Covers.
- Hook suggestions.
- Manual correction.

---

# Publishing

Initial:

- YouTube Shorts.
- Instagram Reels.
- Facebook Reels.

Each clip can have independent:

- Account.
- Platform.
- Date.
- Time.
- Metadata.

Publishing must be durable and duplicate-safe.

---

# Analytics

Local only.

Use metrics to improve local recommendations.

No Norvi analytics collection.

---

# Development Rules

Use Antigravity.

One task at a time.

Read docs before coding.

Test every feature.

Never silently change architecture.

Never introduce paid services without explicit approval.

---

# Pending Decisions

- Final application name.
- Final PySide6 decision.
- Local database implementation.
- Exact Gemma/Ollama model ID.
- Local transcription engine.
- Scene detection.
- Scheduler.
- Secure credential storage.
- Exact social APIs.
- Packaging/installer approach.

---

# Current Task

Finalize remaining technologies.

Then update:

DECISIONS.md
ARCHITECTURE.md
TASKS.md

Then begin project setup.

---

# Known Risks

- Ollama/model size.
- User hardware limitations.
- Long video processing time.
- Social API limitations.
- OAuth expiration.
- Rate limits.
- Copyright/reuse rights.
- Meta API requirements.
- Local scheduling when PC is off.
- Large disk usage.
- Prompt injection through untrusted media text.
- Model hallucination.
- Duplicate posting.
- Broken/partial media downloads.

---

# Next Step

After the owner finalizes technologies/modules:

1. Update pending ADRs.
2. Lock architecture.
3. Create .env.example.
4. Initialize repository.
5. Give all documentation to Antigravity.
6. Ask Antigravity to review the architecture first.
7. Start Phase 1 only after its review.