# Nexus — Development Phases

This folder contains the complete phase-by-phase development plan.

Development must proceed sequentially unless a documented architectural decision explicitly changes the order.

## Phase Order

1. [Project Foundation](PHASE_01_PROJECT_FOUNDATION.md)
2. [Desktop Application Shell](PHASE_02_DESKTOP_APPLICATION_SHELL.md)
3. [Nexus Authentication & Licensing Client](PHASE_03_NORVI_AUTHENTICATION_AND_LICENSING.md)
4. [Local Storage & Privacy Foundation](PHASE_04_LOCAL_STORAGE_AND_PRIVACY_FOUNDATION.md)
5. [Ollama Runtime Management](PHASE_05_OLLAMA_RUNTIME_MANAGEMENT.md)
6. [Gemma Model Management & AI Gateway](PHASE_06_GEMMA_MODEL_AND_AI_GATEWAY.md)
7. [YouTube Discovery Engine](PHASE_07_YOUTUBE_DISCOVERY_ENGINE.md)
8. [Source Selection & Rights Workflow](PHASE_08_SOURCE_SELECTION_AND_RIGHTS.md)
9. [Media Ingestion & Preparation](PHASE_09_MEDIA_INGESTION_AND_PREPARATION.md)
10. [Local Transcription & Timeline Intelligence](PHASE_10_TRANSCRIPTION_AND_TIMELINE_INTELLIGENCE.md)
11. [Full Video Understanding](PHASE_11_FULL_VIDEO_UNDERSTANDING.md)
12. [Clip Candidate Generation](PHASE_12_CLIP_CANDIDATE_GENERATION.md)
13. [Clip Scoring & Ranking](PHASE_13_CLIP_SCORING_AND_RANKING.md)
14. [Clip Lab & Review UI](PHASE_14_CLIP_LAB_AND_REVIEW_UI.md)
15. [Deterministic Video Rendering](PHASE_15_DETERMINISTIC_VIDEO_RENDERING.md)
16. [Captions & Intelligent Reframing](PHASE_16_CAPTIONS_AND_INTELLIGENT_REFRAMING.md)
17. [Hooks, Covers & Brand Profiles](PHASE_17_HOOKS_COVERS_AND_BRAND_PROFILES.md)
18. [Metadata Generation & Approval Workflow](PHASE_18_METADATA_AND_APPROVAL_WORKFLOW.md)
19. [Social Account Integration Foundation](PHASE_19_SOCIAL_ACCOUNT_INTEGRATION_FOUNDATION.md)
20. [Persistent Scheduler & Publishing Queue](PHASE_20_SCHEDULER_AND_PUBLISHING_QUEUE.md)
21. [YouTube Shorts Publishing](PHASE_21_YOUTUBE_SHORTS_PUBLISHING.md)
22. [Instagram Reels Publishing](PHASE_22_INSTAGRAM_REELS_PUBLISHING.md)
23. [Facebook Reels Publishing](PHASE_23_FACEBOOK_REELS_PUBLISHING.md)
24. [Duplicate Detection, Content Series & Reliability](PHASE_24_DUPLICATE_SERIES_AND_RELIABILITY.md)
25. [Analytics & Local Learning](PHASE_25_ANALYTICS_AND_LOCAL_LEARNING.md)
26. [Security, Optimization, Packaging & Full Production Validation](PHASE_26_SECURITY_OPTIMIZATION_PACKAGING_AND_PRODUCTION.md)

---

## Development Rule

Every phase must leave the application in a runnable, tested, non-broken state.

The next phase must not be started while the current phase contains unresolved blocking failures.

For every phase:

READ
→ UNDERSTAND
→ PLAN
→ IMPLEMENT
→ TEST
→ REVIEW
→ FIX
→ RETEST
→ DOCUMENT
→ COMPLETE
