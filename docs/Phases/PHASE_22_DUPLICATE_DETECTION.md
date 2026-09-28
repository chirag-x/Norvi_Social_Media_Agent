# Phase 22: Duplicate Detection

## Overview
This phase introduces a safety mechanism to prevent the system from accidentally extracting, generating, or scheduling the exact same video clip multiple times. This is highly important when analyzing the same long-form source video multiple times over different sessions.

## Key Features
- **Extracted Clips Ledger:** Added a new SQLite table `extracted_clips` which creates a ledger of every clip rendered by the app, storing its YouTube `source_video_id` along with its exact start and end times.
- **Overlap Detection:** When the Gemma AI finishes analyzing a transcript and suggests new clips, the app cross-references those suggestions against the database. If a suggestion overlaps within 15 seconds of a previously rendered clip from the same source video, it trips the duplicate flag.
- **UI Safety Mechanisms:** 
  - Duplicate clips are heavily highlighted with a stark red border.
  - The UI explicitly inserts a red `[DUPLICATE]` tag into the title.
  - The "Approve to Queue" button is completely disabled (grayed out) and replaced with an "Already Extracted" warning to prevent accidental extraction.

## Components Built
- `003_extracted_clips.sql`: The ledger table.
- Substantial UI alterations inside `ClipLabView._render_clips` to style and reject duplicate payloads.
