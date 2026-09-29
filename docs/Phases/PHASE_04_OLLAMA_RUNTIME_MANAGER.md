# Phase 4: Ollama Runtime Manager

## Status
**Completed**

## Overview
This phase built the underlying architecture to strictly manage the local AI engine, Ollama. Adhering to the rule that zero cloud AI APIs are used for content processing, the desktop app now acts as a silent supervisor for the Ollama runtime. It detects installation, seamlessly boots the AI engine in the background when the app starts, handles external ownership safely, and guarantees proper shutdown without leaving hanging processes.

## Accomplishments
1. **Ollama Manager** (`src/ai/ollama_manager.py`):
   - Created a singleton manager to control the AI process.
   - Checks if `ollama` is in the system `PATH`.
   - Uses asynchronous HTTP checks (`httpx`) against `http://localhost:11434/api/tags` to verify if the engine is already running.
2. **Process Ownership & Safe Shutdown**:
   - The app strictly tracks whether *it* started the Ollama process, or if the user already had it running in the background.
   - If the app starts Ollama, it uses `subprocess.Popen` with `CREATE_NO_WINDOW` so no ugly terminal pops up on the user's screen.
   - Integrated into `MainWindow.closeEvent()`: When the user closes the Nexus app, it cleanly kills the Ollama process *only* if the app was the one to start it.
3. **UI Integration**:
   - Added a live "System Status" indicator to the Dashboard.
   - When the user logs in, the dashboard spins up a background worker to silently boot/verify Ollama.
   - Displays a green "🟢 AI Engine Online (Ollama)" on success, or a red error message if installation is missing.

## Action Items Completed
- [x] Detect Ollama.
- [x] Detect running Ollama.
- [x] Start silently.
- [x] Health check.
- [x] Track process ownership.
- [x] Safe stop.
- [x] Handle existing external instance.
- [x] First-run installation flow / error state.
- [x] No visible terminal window in normal use.

## Next Steps
Proceeding to **Phase 5: Gemma Model Manager**, where we will ensure the application detects, downloads, and validates the required `gemma4:cloud` model (or fallback model) before allowing AI operations.
