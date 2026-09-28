# Phase 12 & 13: Candidate Ranking and Clip Lab UI

## Overview
Once Gemma returns a raw array of generated clips, these phases handle sorting the clips mathematically by virality and rendering them into an interactive UI. The user is presented with a scrollable list of visual "Candidate Cards" summarizing the AI's editorial decisions.

## Key Features
- **Dynamic Scroll Architecture:** Upgraded `ClipLabView` to utilize `QScrollArea`, ensuring the UI gracefully handles an infinite amount of generated clips without vertically overflowing or clipping the screen.
- **Candidate Ranking (Phase 12):** The `_render_clips` engine intercepts Gemma's raw output, extracts the `virality_score` out of 10, and strictly sorts the array in descending order so the absolute best clips are always at the top of the feed.
- **Visual Candidate Cards (Phase 13):** Each clip is rendered as an isolated `QFrame` mimicking a social media card. It surfaces:
  - The clickbait title with a 🔥 emoji.
  - The explicit score out of 10.
  - The precise start and end timestamps.
  - Gemma's exact reasoning for *why* the clip will go viral.
- **Approval Workflow:** Implemented placeholder buttons for `[ Reject ]` and `[ Approve to Queue ]`, paving the way for the video rendering engine in Phase 14.

## Components Built
- `src.ui.views.clip_lab.ClipLabView._render_clips`: The dynamically injecting UI method that translates raw JSON into styled PySide6 widget hierarchies on the fly.
