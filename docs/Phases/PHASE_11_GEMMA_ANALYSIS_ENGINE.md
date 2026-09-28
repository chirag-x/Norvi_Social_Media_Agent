# Phase 11: Gemma Analysis Engine

## Overview
This phase bridges the gap between raw transcription data and intelligent editorial decision-making. By leveraging the user's local instance of Ollama running the `gemma4:cloud` model, the app can read through the entire video transcript and mathematically locate the most viral, high-retention segments.

## Key Features
- **Prompt Architecture:** The engine injects a highly specific system prompt commanding Gemma to act as an "elite viral social media producer." It passes the entire formatted script along with the video's title and niche to provide maximal context.
- **Structured JSON Schemas:** To ensure the output can be parsed by our backend, Gemma is strictly locked into outputting a JSON array using Ollama's `format: "json"` parameter.
- **Candidate Extraction:** The engine identifies exact start and end timestamps (in seconds), writes clickbait titles, scores the virality (1-10), and provides reasoning for each clip.
- **Seamless UI Chaining:** In the `ClipLabView`, as soon as `WhisperTranscriber` finishes, the transcript is immediately piped into `GemmaEngine` running on a separate worker thread.

## Components Built
- `src.services.ai.gemma_engine.GemmaEngine`: Manages asynchronous HTTP POST requests to the local Ollama instance (`/api/generate`), validates the JSON output, and wraps errors safely.

## Transition
The extracted JSON array of clip candidates is stored in `AppState.extracted_clips`. The next step (Phase 12/13) will involve displaying these generated candidates in a beautiful UI where the user can visually review, accept, or reject the AI's cutting suggestions.
