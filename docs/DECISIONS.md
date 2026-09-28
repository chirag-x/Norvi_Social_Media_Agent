# Architecture Decisions

## ADR-001 — Desktop Application

Decision:
Build a desktop application instead of a web SaaS.

Reason:
Video processing, local AI, local media, privacy, and background operations are better suited to a desktop architecture.

Status:
Accepted.

---

## ADR-002 — Python 3.13.15

Decision:
Use Python 3.13.15 as the primary language.

Status:
Accepted.

---

## ADR-003 — Google Antigravity

Decision:
Use Google Antigravity as the primary AI coding environment.

Status:
Accepted.

---

## ADR-004 — Local-First Architecture

Decision:
User social-media workflow data stays on the user's computer.

Status:
Accepted.

---

## ADR-005 — No Norvi Content Collection

Decision:
Norvi does not receive user videos, clips, prompts, transcripts, analytics, social history, brand data, or client data.

Status:
Accepted.

---

## ADR-006 — Norvi Authentication Only

Decision:
Norvi backend communication is restricted to authentication, activation/license, entitlement, and session functionality.

Activation backend implementation is outside this project's scope.

Status:
Accepted.

---

## ADR-007 — Ollama Runtime

Decision:
Run the AI model locally through Ollama.

Status:
Accepted.

---

## ADR-008 — Gemma 4 31B-Class Model

Decision:
Use the configured Google Gemma 4 31B-class model as the main local intelligence model.

Exact Ollama model identifier must be recorded once finalized.

Status:
Accepted.

---

## ADR-009 — Automatic Ollama Management

Decision:
The application manages Ollama startup automatically and hides terminal windows during normal use.

Status:
Accepted.

---

## ADR-010 — Safe Ollama Shutdown

Decision:
Only stop Ollama on application exit when the application itself started that instance.

Status:
Accepted.

---

## ADR-011 — Automatic Model Availability

Decision:
Check for the required model at startup and guide/download it when missing.

Status:
Accepted.

---

## ADR-012 — Zero Mandatory Paid Services

Decision:
The application must not require paid AI APIs or paid processing services.

Status:
Accepted.

---

## ADR-013 — Local Transcription

Decision:
Speech transcription occurs locally.

Status:
Accepted.

---

## ADR-014 — Deterministic Media Processing

Decision:
Use deterministic local media tools for cutting/rendering rather than asking the LLM to perform exact media operations.

Status:
Accepted.

---

## ADR-015 — AI Recommends, Code Executes

Decision:
Gemma provides semantic decisions and recommendations.

Validated deterministic modules execute exact operations.

Status:
Accepted.

---

## ADR-016 — YouTube Discovery First

Decision:
YouTube is the initial content discovery source.

Status:
Accepted.

---

## ADR-017 — Five Primary Search Results

Decision:
Discovery presents five primary videos.

Status:
Accepted.

---

## ADR-018 — Multi-Niche Diversification

Decision:
Multiple selected niches should be represented across the five results when possible.

Status:
Accepted.

---

## ADR-019 — Full-Video Understanding

Decision:
Analyze the complete source before final candidate ranking.

Status:
Accepted.

---

## ADR-020 — 10–120 Second Clips

Decision:
User-selected target duration is between 10 and 120 seconds.

Status:
Accepted.

---

## ADR-021 — Score + Explanation

Decision:
Every candidate includes both a score and an explanation.

Status:
Accepted.

---

## ADR-022 — No Guaranteed Virality

Decision:
Do not claim any candidate is guaranteed to become viral.

Status:
Accepted.

---

## ADR-023 — Human Approval

Decision:
AI-generated clips require user approval before publishing.

Status:
Accepted.

---

## ADR-024 — Initial Platforms

Decision:
Initial publishing targets:

YouTube Shorts
Instagram Reels
Facebook Reels

Status:
Accepted.

---

## ADR-025 — Platform Adapters

Decision:
Social-platform logic must be implemented behind platform-specific adapters.

Status:
Accepted.

---

## ADR-026 — Durable Local Publishing Queue

Decision:
Publishing uses persistent local jobs with retries and idempotency.

Status:
Accepted.

---

## ADR-027 — Local Analytics

Decision:
Analytics are retrieved directly by the user's app and stored locally.

Status:
Accepted.

---

## ADR-028 — Local Learning

Decision:
Historical performance may influence future recommendations, but that learning stays on the device.

Status:
Accepted.

---

## ADR-029 — No Default Telemetry

Decision:
No usage analytics or user content telemetry is sent to Norvi by default.

Status:
Accepted.

---

## ADR-030 — Original Media Is Immutable

Decision:
Derived clips must never overwrite the original source.

Status:
Accepted.

---

# Pending Decisions

## ADR-P01 — Desktop UI Framework

Recommended:
PySide6.

Final:
Pending confirmation.

---

## ADR-P02 — Local Database

Recommended:
SQLite.

Final:
Pending confirmation.

---

## ADR-P03 — Local Transcription

Recommended:
faster-whisper or compatible local solution.

Final:
Pending confirmation.

---

## ADR-P04 — Scene Detection

Candidate:
PySceneDetect / OpenCV pipeline.

Final:
Pending confirmation.

---

## ADR-P05 — Secure Credential Storage

Final implementation:
Pending confirmation.

---

## ADR-P06 — Scheduler

Final local scheduler/queue library:
Pending confirmation.

---

## ADR-P07 — Exact Ollama Model ID

Exact model string:
Pending confirmation.

---

## ADR-P08 — Social API Implementations

Exact supported official integration methods:
Pending technical verification.