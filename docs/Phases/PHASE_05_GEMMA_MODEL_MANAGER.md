# Phase 5: Gemma Model Manager

## Status
**Completed**

## Overview
This phase built the integration with Ollama to ensure the specific required language model is downloaded, verified, and ready before the user attempts any content generation. It directly queries the local Ollama registry via the REST API and streams the download progress natively into the PySide6 UI.

## Accomplishments
1. **Model Manager Core** (`src/ai/model_manager.py`):
   - Created the singleton `ModelManager`.
   - Uses `httpx` to hit `GET /api/tags` to list installed models.
   - Compares installed models against the required `NORVI_OLLAMA_MODEL` defined in the configuration (e.g., `gemma4:cloud` or `gemma:2b`).
2. **Native Asynchronous Downloads**:
   - Uses `httpx` streaming to pull the model asynchronously via `POST /api/pull`.
   - Yields JSON chunks that represent download progress, percentage, and bytes completed.
3. **UI Integration**:
   - Added a "Model Status" checker below the AI status on the Dashboard.
   - If the model is missing, it reveals a "Download Required Model" button and a Progress Bar.
   - Clicking the button streams the percentage directly into the Progress Bar smoothly without locking the UI.
4. **Smoke Testing**:
   - Upon a successful download, the app automatically runs a tiny silent test prompt (`"Say 'OK' if you are online."`) via `POST /api/generate` to guarantee the model didn't get corrupted and is properly loaded into memory.

## Action Items Completed
- [x] Define exact model ID/config.
- [x] List local models.
- [x] Detect required model.
- [x] Pull missing model.
- [x] Show download progress.
- [x] Handle interrupted download.
- [x] Verify model.
- [x] AI smoke test.
- [x] Ready state.

## Next Steps
Now that the core local privacy storage, AI runtime, and Model management are fully established, we move to the application logic: **Phase 7: YouTube Discovery** (since Phase 6 was completed early). We will integrate a scraper/API to discover top trending YouTube content based on user niches.
