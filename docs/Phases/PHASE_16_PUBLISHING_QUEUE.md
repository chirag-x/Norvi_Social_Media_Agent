# Phase 16: Publishing Queue & Metadata Generation

## Overview
This phase activates the **Publishing Queue** module, moving the physical video files generated in Phase 14 closer to their final destination: social media platforms. 

## Key Features
- **Queue Discovery:** The `PublishingQueueView` automatically scans the `outputs/` directory and builds an interactive list of all rendered `.mp4` video files.
- **AI Metadata Generation (The Real Captions!):** The user can select any video and click "Generate Metadata (AI)". The system queries the local `GemmaEngine` with the video's title to automatically write a viral TikTok/Shorts post description.
- **Marketing Structure:** The AI is instructed to generate a strong hook sentence, engaging body text, and 5-7 highly relevant trending hashtags.
- **Persistent Storage:** Once generated, the Title and Description are saved to a `.json` file sitting directly next to the `.mp4` video in the `outputs/` folder. This ensures that if the app is restarted, the metadata isn't lost.

## Components Built
- `src.ui.views.publishing_queue.PublishingQueueView`: A split-panel UI featuring a list of videos on the left and a metadata editor on the right.
- **Asynchronous Prompting:** Integrated the `BaseWorker` thread pool to call Gemma in the background, preventing the UI from locking up during AI text generation.

## Transition
With the metadata fully generated and the text boxes populated, the final piece of the architecture is the **Publish API Integration**. The next phase will activate the "Schedule Upload" button to actually push these files to the YouTube/TikTok APIs.
