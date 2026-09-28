# Phase 15: AI Captions

## Overview
This phase links the `faster-whisper` transcription engine with the FFmpeg renderer to automatically burn Alex Hormozi-style animated captions directly into the final video output.

## Key Features
- **SRT Generation Engine:** Before rendering, the app takes the raw JSON transcript generated in Phase 10 and mathematically recalculates the timestamps. If a 10-minute video is sliced to a 30-second clip starting at `01:05.000`, the subtitle engine automatically clamps and resets the timestamps to exactly `00:00.000` so the text perfectly matches the new video clip.
- **FFmpeg Subtitles Filter:** The engine dynamically creates a temporary `.srt` file and injects it into the FFmpeg filter graph using the `subtitles` filter.
- **Styling:** The subtitles are forced into a high-visibility preset: `Arial`, `FontSize=18`, bright yellow (`PrimaryColour=&H00FFFF`), with a thick black outline/shadow (`BorderStyle=3`).

## Components Built
- `src.services.media.renderer._generate_srt`: Iterates through the transcript, calculates relative bounds, formats them into `HH:MM:SS,mmm`, and generates the subtitle file.
- `src.services.media.renderer.extract_clip`: Injects the subtitle file into the `vf` string.

## Transition
With exact trimming, vertical 9:16 reframing, and burned-in captions complete, the actual video asset generation is finished! The next phase is the Publisher Pipeline, which involves moving these rendered assets into a calendar queue to be scheduled and posted automatically to social platforms.
