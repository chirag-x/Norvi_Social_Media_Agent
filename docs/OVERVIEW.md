# Nexus

## Overview

Nexus is a local-first AI-powered desktop application for discovering content, generating short-form clips, scheduling posts, publishing to social platforms, and learning from performance.

The application is designed for agencies, creators, and social-media managers.

---

# Main Workflow

Discover
→ Analyze
→ Create
→ Review
→ Schedule
→ Publish
→ Measure
→ Improve

---

# Core Features

## YouTube Discovery

- Search YouTube.
- Search creators/channels.
- Select niches.
- Multi-niche filtering.
- Fresh/recent discovery.
- Top-five results.
- Open source on YouTube.

---

## AI Video Analysis

- Analyze complete videos.
- Timestamped transcript.
- Scene understanding.
- Topic understanding.
- Strong-moment detection.
- High-potential scoring.
- Explainable recommendations.

---

## Short-Form Generation

Target duration:

10–120 seconds.

Features:

- Intelligent clip selection.
- 9:16 rendering.
- Smart crop.
- Captions.
- Hook suggestions.
- Covers.
- Branding.
- Manual editing.

---

## AI Metadata

Generate:

- Titles.
- Descriptions.
- Captions.
- Hashtags.
- CTAs.
- Platform-specific alternatives.

---

## Publishing

Initial platforms:

- YouTube Shorts.
- Instagram Reels.
- Facebook Reels.

Features:

- Per-clip platform selection.
- Per-clip scheduling.
- Local publishing queue.
- Retry.
- Duplicate protection.
- Publish verification.

---

## Analytics

Where supported:

- Views.
- Reach.
- Watch time.
- Retention.
- Likes.
- Comments.
- Shares.
- Saves.

Analytics stay local.

---

# Privacy

The application is privacy-first.

Nexus does NOT receive:

- Your videos.
- Your generated clips.
- Your transcripts.
- Your prompts.
- Your social account activity.
- Your publishing history.
- Your analytics.
- Your client data.
- Your brand data.

Social-media workflow data remains on the user's computer.

Nexus server communication is restricted to account authentication/licensing functionality.

---

# AI

Primary AI:

Google Gemma 4 31B-class model.

Runtime:

Ollama.

AI inference:

Local.

Paid AI API:

Not required.

---

# Ollama Experience

Normal operation is automatic.

When the app starts:

1. Check Ollama.
2. Start it silently when required.
3. Check required Gemma model.
4. Prepare/download model when missing.
5. Verify AI.
6. Start application workflow.

Normal users should not need to use CMD or PowerShell.

If this application started Ollama, it can close its owned Ollama process when the application exits.

If Ollama was already running independently, the app should leave it running.

---

# First Run

Typical first run:

Launch app
↓
Login using Nexus account/license
↓
Check local AI runtime
↓
Install/setup Ollama if required
↓
Download required model if missing
↓
Verify local AI
↓
Open dashboard

Large model download may take time.

The app should show clear progress.

---

# Requirements

Target OS:

Windows.

Python development version:

Python 3.13.15.

Local AI:

Ollama.

AI model:

Configured Gemma 4 31B-class model.

Media tools:

Local deterministic video-processing stack.

Internet is required for:

- Initial software/model downloads.
- Nexus authentication.
- YouTube discovery.
- Social platform OAuth.
- Publishing.
- Analytics retrieval.

Core AI reasoning and media processing are local.

---

# Development Environment

Primary AI coding environment:

Google Antigravity.

Development follows:

Read
→ Understand
→ Plan
→ Implement
→ Test
→ Review
→ Fix
→ Commit
→ Update Documentation

Do not ask Antigravity to build the entire application in one prompt.

Use TASKS.md.

---

# Project Documentation

docs/

PRD.md
Product requirements.

ARCHITECTURE.md
System architecture.

DESIGN.md
UI/UX design.

RULES.md
AI/development rules.

DECISIONS.md
Permanent project decisions.

MEMORY.md
Current project state.

TEST_PLAN.md
Testing requirements.

SECURITY.md
Security/privacy requirements.

Root:

TASKS.md
Implementation roadmap.

README.md
Project overview.

---

# Development Setup

The exact installation commands should be added after final dependency selection.

Expected high-level process:

1. Install Python 3.13.15.
2. Clone repository.
3. Create virtual environment.
4. Install dependencies.
5. Configure development environment variables.
6. Run tests.
7. Start application.

Do not place production secrets in the repository.

---

# Project Structure

social-media-agent/
├── docs/
├── src/
│   ├── app/
│   ├── ui/
│   ├── domain/
│   ├── services/
│   ├── ai/
│   ├── media/
│   ├── integrations/
│   ├── storage/
│   ├── security/
│   ├── workers/
│   └── utils/
├── tests/
├── assets/
├── scripts/
├── README.md
├── TASKS.md
├── .env.example
└── .gitignore

---

# Development Rules

Before making changes:

Read relevant documentation.

Inspect existing code.

Plan.

Do not modify unrelated files.

After implementation:

Run tests.

Fix failures.

Review security/privacy.

Update documentation.

---

# Product Safety Rules

- Never publish without required approval.
- Never upload user content to Nexus.
- Never expose tokens.
- Never treat public content as automatically reusable.
- Never guarantee virality.
- Never blindly retry a publishing action that could create duplicates.
- Never kill an Ollama process the application does not own.

---

# Cost Philosophy

The application should use zero mandatory paid services.

Preferred:

- Local AI.
- Open-source libraries.
- Local storage.
- Official free APIs where available.

A provider changing its free quota or policy may require future adaptation, but the architecture must not deliberately depend on a paid AI service.

---

# Current Status

Planning.

Core product architecture and requirements defined.

Remaining technology choices must be finalized before implementation begins.

See:

TASKS.md

DECISIONS.md

MEMORY.md