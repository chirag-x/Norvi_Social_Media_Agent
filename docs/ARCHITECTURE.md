# Architecture

## 1. Architecture Type

Local-first Windows desktop application.

Primary language:
Python 3.13.15.

Development:
Google Antigravity.

AI:
Local Ollama + Gemma 4 31B-class model.

User content:
Processed and stored locally.

Norvi cloud responsibility:
Authentication/licensing only.

---

# 2. High-Level Architecture

User
↓
Desktop Application
│
├── Authentication Client
│      ↓
│   Norvi Auth/License Server
│
├── Local AI Runtime Manager
│      ↓
│   Ollama
│      ↓
│   Gemma
│
├── Discovery Engine
│      ↓
│   YouTube
│
├── Media Ingestion
│
├── Video Analysis Engine
│
├── Clip Intelligence Engine
│
├── Render Engine
│
├── Caption Engine
│
├── Metadata Engine
│
├── Approval System
│
├── Local Scheduler
│
├── Publishing Queue
│      ├── YouTube Adapter
│      ├── Instagram Adapter
│      └── Facebook Adapter
│
├── Local Analytics
│
├── Recommendation Engine
│
└── Local Database / Files

Norvi must not sit between the app and the user's social-media platforms.

---

# 3. Application Layers

## UI Layer

Responsibilities:

- Windows.
- Views.
- Dialogs.
- User input.
- Progress.
- Video preview.
- Timeline.
- Scheduling calendar.
- Notifications.

Recommended framework:
PySide6 / Qt for Python.

If another UI framework is selected later, record it in DECISIONS.md before changing architecture.

---

## Application Layer

Contains use cases such as:

- Discover videos.
- Select source.
- Analyze video.
- Generate clips.
- Approve clip.
- Schedule clip.
- Publish clip.
- Refresh analytics.

The UI should call application services instead of directly calling low-level providers.

---

## Domain Layer

Contains core entities:

- Workspace.
- Client.
- BrandProfile.
- SourceVideo.
- Transcript.
- AnalysisJob.
- ClipCandidate.
- ClipVersion.
- Approval.
- SocialAccount.
- Schedule.
- PublishJob.
- PublishedPost.
- AnalyticsSnapshot.

---

## Infrastructure Layer

Contains:

- Ollama integration.
- FFmpeg integration.
- Transcription integration.
- YouTube integration.
- Meta integration.
- Local database.
- Secure credential storage.
- File storage.
- Scheduler.
- Queue.
- Network clients.

---

# 4. Ollama Runtime Architecture

Create a dedicated OllamaRuntimeManager.

Responsibilities:

check_installed()
install_if_approved()
detect_running_instance()
start_if_needed()
health_check()
list_models()
ensure_model()
pull_model()
warm_model_if_needed()
stop_owned_process()

Important:

The app must track whether it started Ollama.

If Ollama was already running:
owned_by_app = false

If our app starts it:
owned_by_app = true

Only stop Ollama automatically when owned_by_app = true.

---

# 5. Ollama First-Run Flow

App starts
↓
Check Ollama installation
↓
Missing?
├── Yes → first-run installation flow
└── No → continue
↓
Detect/start local Ollama runtime
↓
Check required model
↓
Missing?
├── Yes → download model with visible progress
└── No
↓
Health check
↓
Model test
↓
AI READY

No visible terminal window should be required during normal operation.

If an external installer requires user interaction, show a clean onboarding step rather than pretending installation is invisible.

Do not make Ollama account/login a hard dependency unless the exact Ollama distribution/version actually requires it.

---

# 6. AI Gateway

All Gemma interaction must go through one AI gateway.

Example responsibilities:

analyze_transcript()
analyze_visual_context()
generate_candidates()
score_candidates()
generate_metadata()
recommend_schedule()
summarize_analytics()

The rest of the application must not scatter direct Ollama calls throughout the codebase.

---

# 7. AI Structured Output

Whenever possible, Gemma should return validated structured data.

Example candidate:

{
  candidate_id,
  start_time,
  end_time,
  score,
  score_components,
  summary,
  reason,
  hook_type,
  platform_fit,
  warnings
}

Never trust free-form model output directly for destructive actions.

---

# 8. Video Analysis Pipeline

Source
↓
Media Probe
↓
Audio Extraction
↓
Local Transcription
↓
Timestamped Transcript
↓
Scene Detection
↓
Keyframe Extraction
↓
Optional Speaker/Subject Detection
↓
Topic Segmentation
↓
Gemma Semantic Analysis
↓
Candidate Moment Generation
↓
Context Expansion
↓
Scoring
↓
Deduplication
↓
Candidate Ranking

---

# 9. Long Video Strategy

Do not send every frame of a long video to Gemma.

Instead create an efficient representation:

- Full timestamped transcript.
- Scene boundaries.
- Keyframes.
- Topic summaries.
- Audio/activity signals.
- Important timestamps.

Gemma receives the structured representation needed for reasoning.

---

# 10. Transcription

Use a local transcription engine.

Recommended family:
faster-whisper or another compatible local speech-to-text solution.

Requirements:

- Local execution.
- Timestamp support.
- No paid API requirement.
- No transcript upload to Norvi.

---

# 11. Media Processing

Use a deterministic media-processing layer.

Recommended core:
FFmpeg.

Optional supporting tools:

- OpenCV.
- PySceneDetect.
- Local subject/person detection.
- Local tracking.

Responsibilities:

- Exact trims.
- Aspect conversion.
- Scaling.
- Cropping.
- Audio normalization.
- Captions.
- Brand overlays.
- Export.
- Media validation.

---

# 12. Local Data Architecture

User data stays inside an application-specific local directory.

Conceptual layout:

app_data/
├── database/
├── projects/
├── sources/
├── proxies/
├── clips/
├── captions/
├── covers/
├── analytics/
├── logs/
├── cache/
└── temp/

Temporary files should be cleaned safely.

Original media must not be modified.

---

# 13. Local Database

Recommended baseline:
SQLite.

Reasons:

- Free.
- Local.
- Embedded.
- Reliable.
- No cloud dependency.
- Suitable for desktop application metadata.

Potential stored data:

- Local clients.
- Brand profiles.
- Source metadata.
- Transcript references.
- Clip records.
- Schedules.
- Publishing jobs.
- Analytics.
- Settings.

Sensitive OAuth secrets should not be stored as plaintext database fields.

---

# 14. Credential Storage

Use OS-provided secure credential storage when practical.

On Windows, sensitive tokens should be protected using an appropriate Windows credential/encryption mechanism.

Never store:

- Plaintext passwords.
- Plaintext refresh tokens in normal JSON files.
- Secrets in logs.

---

# 15. Norvi Authentication Boundary

Desktop App
↓
Norvi Authentication Endpoint
↓
Account / License Validation
↓
Access Token
↓
Desktop App

Permitted server-side information:

- Account identity/email.
- Authentication record.
- Activation/license key.
- Entitlement.
- Session/token information.

Not permitted:

- Social searches.
- Videos.
- Clips.
- Analytics.
- Social credentials.
- Client data.
- Prompts.
- Transcripts.

The activation system implementation remains outside this project's responsibility.

---

# 16. YouTube Discovery Provider

Create a provider abstraction.

VideoDiscoveryProvider

Functions conceptually:

search()
get_video()
get_channel()
normalize_result()

The discovery layer handles:

- Query.
- Niches.
- Freshness.
- Ranking.
- Diversification.
- Top five.

---

# 17. Rights Service

Before media acquisition:

source selected
↓
rights confirmation
↓
local confirmation stored
↓
processing allowed

No rights confirmation:
processing blocked.

---

# 18. Job System

Long-running work must use background jobs.

Examples:

- Model download.
- Source preparation.
- Transcription.
- Analysis.
- Rendering.
- Publishing.
- Analytics sync.

Do not freeze the UI thread.

---

# 19. Analysis State Machine

CREATED
↓
SOURCE_READY
↓
TRANSCRIBING
↓
ANALYZING
↓
GENERATING_CANDIDATES
↓
SCORING
↓
CANDIDATES_READY

Failure states:

TRANSCRIPTION_FAILED
ANALYSIS_FAILED
CANCELLED

---

# 20. Clip Rendering State

DRAFT
↓
RENDER_REQUESTED
↓
RENDERING
↓
READY_FOR_REVIEW
↓
APPROVED

Possible:
RENDER_FAILED
REJECTED

---

# 21. Publishing State Machine

DRAFT
↓
APPROVED
↓
SCHEDULED
↓
QUEUED
↓
UPLOADING
↓
PLATFORM_PROCESSING
↓
PUBLISHED

Failure states:

FAILED_TRANSIENT
FAILED_PERMANENT
AUTH_REQUIRED
CANCELLED

---

# 22. Scheduler

Use a persistent local scheduler.

Requirements:

- Survive application restart.
- Store timezone.
- Store requested date/time.
- Support rescheduling.
- Support cancellation.
- Trigger durable jobs.

If the user's PC is powered off and the platform does not support server-side future scheduling, the app cannot execute local API requests while powered off.

Where the platform supports its own scheduling, prefer that capability.

Otherwise execute as soon as appropriate when the local system becomes available.

---

# 23. Publishing Layer

Core abstraction:

PublishingProvider

validate_account()
validate_media()
publish()
get_status()
fetch_post()

Initial adapters:

- YouTube.
- Instagram.
- Facebook.

Platform-specific implementation must not leak across the whole codebase.

---

# 24. Idempotency

Publishing retries must not duplicate posts.

Each publishing intent gets a stable internal identifier based on:

- Clip version.
- Account.
- Platform.
- Scheduled action.

Repeated execution should detect an already completed/in-progress intent.

---

# 25. Analytics

Each platform adapter may expose an analytics interface.

Normalize available metrics but retain original platform meaning.

Never convert "metric unavailable" into zero.

---

# 26. Local Recommendation Engine

Inputs:

- Clip features.
- Platform.
- Duration.
- Hook.
- Topic.
- Publish time.
- Historical local metrics.

Outputs:

- Suggested clip duration.
- Suggested posting window.
- Suggested content style.
- Suggested hook style.

All processing stays local.

---

# 27. Privacy Architecture

Network communication should occur only when required for:

1. Norvi account/license authentication.
2. YouTube discovery/source access.
3. Social account OAuth/API operations.
4. Publishing.
5. Analytics retrieval.
6. Required application/model downloads.

User content must never be automatically uploaded to Norvi.

No default telemetry.

---

# 28. Suggested Repository Structure

social-media-agent/
│
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   ├── DESIGN.md
│   ├── RULES.md
│   ├── DECISIONS.md
│   ├── MEMORY.md
│   ├── TEST_PLAN.md
│   └── SECURITY.md
│
├── src/
│   ├── app/
│   ├── ui/
│   ├── domain/
│   ├── services/
│   │   ├── auth/
│   │   ├── discovery/
│   │   ├── analysis/
│   │   ├── rendering/
│   │   ├── publishing/
│   │   ├── scheduling/
│   │   └── analytics/
│   ├── ai/
│   │   ├── ollama/
│   │   ├── prompts/
│   │   └── schemas/
│   ├── media/
│   ├── integrations/
│   │   ├── youtube/
│   │   └── meta/
│   ├── storage/
│   ├── security/
│   ├── workers/
│   ├── models/
│   ├── utils/
│   └── config/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   ├── security/
│   └── reliability/
│
├── assets/
├── scripts/
├── README.md
├── TASKS.md
├── .env.example
└── .gitignore

---

# 29. Architecture Rules

1. UI must not contain social API implementation.
2. AI calls go through AI Gateway.
3. Ollama lifecycle goes through OllamaRuntimeManager.
4. FFmpeg commands go through MediaEngine.
5. Social platforms use adapters.
6. Local content never goes to Norvi.
7. Long tasks run outside UI thread.
8. No plaintext secrets.
9. Publishing must be idempotent.
10. AI output must be validated.
11. User approval is required.
12. Original files stay immutable.
13. App must not kill a pre-existing Ollama instance.
14. No paid dependency may be introduced without explicit owner approval.