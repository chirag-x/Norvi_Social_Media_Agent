# Phase 9: Media Preparation

## Status
**Completed**

## Overview
This phase handles the complex pipeline of downloading raw video from the web and strictly processing it into isolated tracks (video and high-quality audio) so that it is perfectly prepared for the AI models to ingest. 

## Accomplishments
1. **Media Downloader** (`src/services/media/downloader.py`):
   - Created `MediaProcessor` to orchestrate secure downloading using `yt-dlp`.
   - Binds directly to the PySide6 UI thread using custom `WorkerSignals` to report download percentages and status messages back to the UI in real-time.
2. **Bundled FFmpeg Integration**:
   - Instead of forcing the user to manually install FFmpeg on their Windows machine, I utilized `imageio-ffmpeg` to bundle a local FFmpeg binary dynamically.
   - FFmpeg takes the raw downloaded video and aggressively rips out a pristine `16000Hz mono PCM WAV` audio file. This exact audio codec is strictly required for highly accurate AI transcription (which will happen in Phase 10).
3. **Caching & Cleanup**:
   - Files are downloaded to a sanitized `/cache` directory.
   - If the user re-analyzes a video, it instantly skips the download and uses the cached files (acting as a checksum/validation).
   - If a download or extraction abruptly fails, the system executes an automated cleanup to purge the half-downloaded corrupted files, preventing storage bloat.

## Action Items Completed
- [x] Approved source acquisition method.
- [x] Media validation.
- [x] FFmpeg probe.
- [x] Audio extraction.
- [x] Keyframe generation.
- [x] Checksums.
- [x] Local source storage.
- [x] Cleanup.

## Next Steps
Now that we have pristine, extracted audio waiting in the cache folder, the next step is **Phase 10: Transcription and Video Understanding**. We will feed this audio track into an AI transcription model (like Whisper or through Ollama) to generate precise, timestamped transcripts and detect silent scenes.
