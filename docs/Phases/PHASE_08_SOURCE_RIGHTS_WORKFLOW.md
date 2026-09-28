# Phase 8: Source & Rights Workflow

## Status
**Completed**

## Overview
This phase handles the critical bridge between discovering content on the web and passing it into our AI engine for processing. It establishes a centralized global application state and builds the Clip Lab entry UI. A major focus is on enforcing user compliance with Fair Use before any media is downloaded or analyzed.

## Accomplishments
1. **Global App State** (`src/app/state.py`):
   - Created a singleton `AppState` using Qt Signals.
   - Securely tracks the `active_source` across the entire application.
   - When a user clicks "Select Source" in the Discover tab, it instantly writes to global state, notifies the Dashboard, and navigates the view automatically.
2. **Clip Lab Entry View** (`src/ui/views/clip_lab.py`):
   - Replaced the placeholder with a fully styled interface.
   - If no source is selected, it elegantly prompts the user to return to the Discover tab.
   - If a source is selected, it displays the full Title, Channel, and URL.
3. **Fair Use Verification**:
   - Built a mandatory 3-part verification checklist enforcing Transformative Value, Commercialization Risks, and Proper Attribution.
   - The "Analyze with AI" button remains locked and disabled until the user manually checks all three boxes, ensuring strict compliance before the system downloads any third-party media.
4. **Duration Selector**:
   - Added a numeric input (`QSpinBox`) for target clip duration, enforcing a strict minimum of 10 seconds and maximum of 120 seconds.

## Action Items Completed
- [x] Selected-source page (Clip Lab View).
- [x] Source metadata display.
- [x] Rights confirmation checklist.
- [x] Duration selector.
- [x] 10-second minimum constraint.
- [x] 120-second maximum constraint.
- [x] Start-analysis action button (locked via checklist).

## Next Steps
Now that we have a fully validated content source ready for processing, we will proceed to **Phase 9: Media Preparation**. This phase will involve using an approved tool (like `yt-dlp`) to acquire the video file securely and running FFmpeg to probe its tracks and prepare the audio payload for our local transcription engine.
