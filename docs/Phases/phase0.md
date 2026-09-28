# Phase 0: Final Technology Lock

## Status
**Completed**

## Overview
This phase finalizes the core technology stack required to build the Norvi Social Media Agent. By definitively selecting these libraries and frameworks, we ensure that the architecture described in `ARCHITECTURE.md` can be implemented successfully, meeting all privacy, cost, and local-first requirements.

## Technology Decisions

1. **Application Name**: Norvi Social Media Agent (Confirmed)
2. **Desktop UI Framework**: PySide6 (Qt for Python). It is a robust, professional-grade framework suited for complex desktop applications.
3. **Local Database**: SQLite. It's embedded, serverless, and perfect for a local-first application to store client, scheduling, and analytics data.
4. **Local Transcription Engine**: `faster-whisper`. It provides excellent performance and accuracy for local speech-to-text without relying on cloud APIs.
5. **Video Scene Detection**: `PySceneDetect` combined with `opencv-python-headless`. This allows for programmatic and accurate scene boundary detection in long videos.
6. **FFmpeg Packaging Strategy**: We will rely on the `ffmpeg-python` wrapper for Python logic, and the user's local FFmpeg installation (or a bundled binary in the final release phase) for deterministic media processing.
7. **Exact Ollama Model Identifier**: `gemma2:27b`. This will serve as the Gemma 31B-class representation for local video understanding, metadata generation, and decision making until the next iteration of the model becomes officially available on the Ollama registry.
8. **YouTube Discovery & Publishing**: `google-api-python-client`. The official Google client library provides the most reliable access to the YouTube Data API v3 for both searching content and uploading Shorts.
9. **Meta Publishing (Instagram & Facebook)**: Using `requests` to interact directly with the official Instagram Graph API and Facebook Graph API, as Meta's official Python SDKs are heavily focused on ads rather than content publishing.
10. **Local Scheduler**: `APScheduler`. A powerful, in-process task scheduler for Python that supports persistent job stores (perfectly integrating with our SQLite database).
11. **Secure Credential Storage**: `keyring`. Provides a cross-platform way to access the OS-level secure credential store (e.g., Windows Credential Locker) to safely hold OAuth refresh tokens without keeping them in plain text.

## Action Items Completed
- [x] Confirmed final application name.
- [x] Confirmed PySide6 or alternative desktop UI.
- [x] Confirmed SQLite implementation.
- [x] Confirmed local transcription engine.
- [x] Confirmed video scene detection library.
- [x] Confirmed FFmpeg packaging strategy.
- [x] Confirmed exact Ollama model identifier.
- [x] Confirmed YouTube discovery integration.
- [x] Confirmed YouTube publishing integration.
- [x] Confirmed Meta publishing integration.
- [x] Confirmed local scheduler.
- [x] Confirmed secure credential storage.
- [x] Updated `DECISIONS.md`.
- [x] Generated initial `requirements.txt`.
