# Phase 7: YouTube Discovery

## Status
**Completed**

## Overview
This phase implemented the primary content discovery engine, allowing users to search for trending topics or competitor videos across YouTube without needing a paid API key. It uses a clean, abstract provider interface, allowing future extensions (like TikTok or Instagram discovery).

## Accomplishments
1. **Discovery Interface** (`src/discovery/provider.py`):
   - Created `DiscoveryProvider` base class and a `VideoResult` Pydantic model to normalize data across different platforms.
2. **YouTube Implementation** (`src/discovery/youtube.py`):
   - Integrated `youtube-search-python` to anonymously scrape YouTube search results.
   - Parses views, channel names, publish dates, and thumbnails perfectly.
   - Wrapped synchronous scraping inside `asyncio.to_thread` to prevent locking the UI.
3. **Discover UI** (`src/ui/views/discover.py`):
   - Created a responsive layout featuring a niche selection dropdown (General, Tech, Gaming, Finance, etc.) and a keyword search bar.
   - Search runs fully asynchronously in a `BaseWorker` thread.
   - Renders results into a clean list view (`QListWidget`) using custom item widgets (`VideoItemWidget`).
4. **Action Buttons**:
   - Added a red "Watch on YouTube" button that opens the native default browser directly to the video URL using `QDesktopServices`.
   - Added a "Select Source" placeholder button (which will be wired up in Phase 8).

## Action Items Completed
- [x] Discovery provider interface.
- [x] YouTube implementation.
- [x] Search field.
- [x] Niche multi-select.
- [x] Result normalization & parsing.
- [x] Top-five presentation in UI.
- [x] Open-on-YouTube action.

## Next Steps
Now that the user can discover trending content on YouTube, the next step is **Phase 8: Source & Rights Workflow**. We will connect the "Select Source" button so the user can verify creative commons / fair use rights and send the selected video URL directly to the AI for Clip Lab analysis.
