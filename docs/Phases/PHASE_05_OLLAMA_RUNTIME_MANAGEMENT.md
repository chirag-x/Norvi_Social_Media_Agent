# Phase 5 — Ollama Runtime Management

## Status

Not Started

---

## Objective

Make local Ollama operation invisible and reliable for normal users.

The application should detect, prepare, start, monitor, and safely stop the local Ollama runtime.

---

## Core User Experience

Normal startup:

App opens
→ Check Ollama
→ Detect running service
→ Start silently if necessary
→ Health check
→ Continue

The user should not need CMD or PowerShell.

---

## First-Run Behavior

If Ollama is missing:

1. Detect that it is unavailable.
2. Show a clean first-run setup screen.
3. Explain that the local AI runtime must be installed.
4. Use a trusted official installation path.
5. Perform supported automated/silent installation when possible.
6. If OS/vendor interaction is mandatory, show the required user step.
7. Verify installation.
8. Start runtime.
9. Continue.

Do not assume account/login is required unless the installed Ollama version actually requires it.

---

## Required Work

Create `OllamaRuntimeManager`.

Responsibilities:

- Detect installation.
- Locate executable.
- Detect existing service/process.
- Determine local endpoint.
- Start Ollama without visible terminal window.
- Health-check service.
- Track ownership.
- Restart app-owned instance where safe.
- Stop app-owned instance on application shutdown.
- Leave externally owned instance untouched.

---

## Critical Ownership Rule

If Ollama was already running before the application started:

`owned_by_app = false`

Do not kill it.

If this application starts Ollama:

`owned_by_app = true`

The application may safely stop that instance during shutdown after active work is complete.

---

## Architecture Requirements

All Ollama lifecycle behavior must be centralized.

Do not scatter:

- `subprocess` commands.
- Process detection.
- Service startup.

across unrelated modules.

---

## Privacy Requirements

Ollama endpoint should remain local.

Do not expose local AI server to the internet.

Do not send AI prompts through Norvi.

---

## Security Requirements

- Use trusted official installer/source.
- Avoid unknown mirrors.
- Validate paths.
- Avoid shell injection.
- Prefer subprocess argument lists.
- Bind/use localhost only where possible.
- Do not open firewall rules unnecessarily.

---

## Error Handling Requirements

Handle:

- Ollama missing.
- Install fails.
- Executable not found.
- Port unavailable.
- Service fails to start.
- Health check fails.
- Existing incompatible process.
- Shutdown failure.

---

## UI Requirements

Provide states:

- Checking Local AI
- Runtime Missing
- Installing
- Starting
- Ready
- Failed

Raw console output should not be the default UX.

---

## Testing Requirements

Critical tests:

1. Ollama installed, stopped.
2. Ollama installed, already running.
3. Ollama missing.
4. Startup failure.
5. Existing process ownership.
6. App-owned shutdown.
7. External Ollama remains running after app exits.
8. No visible shell window during normal startup.

---

## Acceptance Criteria

- Ollama detected correctly.
- Ollama can start silently.
- Health check works.
- Process ownership works.
- Existing external Ollama is never killed.
- Missing installation has clear setup flow.
- App remains responsive.

---

## Real User Validation

Test on a Windows machine where:

A. Ollama is installed and stopped.

B. Ollama is already running.

C. Ollama is not installed, if safe test environment is available.

Record actual behavior.

---

## Antigravity Instructions

This phase is runtime management only.

Do not implement Gemma prompting or video analysis yet.

If something fails on a real Windows run, find the root cause and fix it before marking the phase complete.

---

## Completion Report Requirements

Include:

- Detection method.
- Startup method.
- Ownership logic.
- Shutdown logic.
- Installer behavior.
- Tests.
- Real Windows validation.

---

## Phase Completion Rule

Ollama runtime lifecycle must be reliable before adding model management.