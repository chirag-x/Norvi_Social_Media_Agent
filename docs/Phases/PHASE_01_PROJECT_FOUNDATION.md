# Phase 1 — Project Foundation

## Status

Not Started

---

## Objective

Create the stable foundation of the Norvi Social Media Agent.

At the end of this phase, the project must have a clean Python 3.13.15 development environment, validated repository structure, configuration system, logging foundation, testing foundation, startup flow, dependency strategy, and developer tooling.

No actual social-media automation feature should be implemented yet.

---

## Why This Phase Exists

This project contains local AI, video processing, background jobs, social-platform integrations, local databases, authentication, scheduling, and desktop UI.

If the foundation is weak, later phases will create duplicated logic, dependency conflicts, broken imports, inconsistent configuration, and architecture drift.

This phase establishes the rules every later subsystem must follow.

---

## Scope

Implement:

- Python 3.13.15 project.
- `.venv` development workflow.
- Repository structure.
- Application package structure.
- Configuration loading.
- Environment validation.
- Structured local logging.
- Base exception hierarchy.
- Application startup/bootstrap.
- Basic health-check framework.
- Test framework.
- Linting.
- Formatting.
- Static/type checking where selected.
- Git-ready configuration.
- Development scripts.
- Dependency documentation.

Do not implement:

- Ollama.
- Gemma.
- YouTube.
- Video processing.
- Authentication UI.
- Publishing.
- Social APIs.
- Full application UI.

---

## Required Work

### 1. Validate Repository Architecture

Review the existing structure generated for the project.

Do not recreate a second architecture.

Use the existing main areas:

- `src/app`
- `src/ui`
- `src/domain`
- `src/services`
- `src/ai`
- `src/media`
- `src/integrations`
- `src/storage`
- `src/workers`
- `src/scheduler`
- `src/security`
- `src/config`
- `src/diagnostics`
- `tests`
- `docs`

Clean up only if necessary.

### 2. Python Environment

The project targets:

`Python 3.13.15`

Create and document a standard virtual-environment workflow.

The project must fail clearly if an unsupported Python version is used.

### 3. Dependency Management

Create a clear dependency strategy.

Do not add every future library in this phase.

Only install packages actually needed for the current foundation.

Dependencies required by later phases should be introduced when those phases begin.

### 4. Configuration

Create a centralized settings/configuration system.

Configuration should support:

- Development.
- Testing.
- Production/local release.

Never scatter environment-variable reads throughout the project.

### 5. Logging

Implement structured local logging.

Logs should support:

- Timestamp.
- Log level.
- Module.
- Message.
- Optional request/job identifiers.

Never log secrets.

### 6. Base Errors

Create normalized application error classes.

Suggested categories:

- ConfigurationError
- ValidationError
- AuthenticationError
- IntegrationError
- MediaError
- AIError
- StorageError
- SchedulingError
- PublishingError

Do not over-engineer yet.

### 7. Application Bootstrap

`main.py` should call one clean application bootstrap path.

Bootstrap should eventually initialize subsystems, but for this phase it only needs the foundation.

### 8. Health Framework

Create a generic health-check mechanism that later phases can extend.

Possible future components:

- Local database.
- Ollama.
- AI model.
- FFmpeg.
- Network.
- Social integrations.

### 9. Tests

Configure pytest and create initial foundation tests.

---

## Architecture Requirements

- `main.py` must remain small.
- Initialization belongs in application/bootstrap modules.
- Configuration must be centralized.
- No business logic in `main.py`.
- No UI-specific logic inside domain/services.
- No paid service dependency.
- No cloud user-data dependency.
- No future subsystem should be mocked as "completed."

---

## Files / Modules Involved

Expected areas:

- `main.py`
- `pyproject.toml`
- `requirements.txt`
- `.env.example`
- `.gitignore`
- `src/app/bootstrap.py`
- `src/app/application.py`
- `src/config/`
- `src/diagnostics/`
- `src/models/`
- `src/utils/`
- `tests/`

Antigravity may create additional files where architecturally justified.

---

## Functional Requirements

The following command should start the current application foundation without crashing:

`python main.py`

The application may only show a minimal development bootstrap at this phase.

A development environment check should clearly report:

- Python version.
- Configuration status.
- Important runtime prerequisites currently applicable.

---

## Privacy Requirements

No telemetry.

No automatic data upload.

No user-content networking.

No analytics SDK.

No hidden remote logging.

---

## Security Requirements

- No secrets committed to Git.
- `.env` ignored.
- `.env.example` contains placeholders only.
- Sensitive values must be redacted from logs.
- Configuration errors must not print secrets.

---

## Error Handling Requirements

Missing required development configuration must produce a useful error.

Do not use broad silent exception handlers.

Startup failure must identify which subsystem failed.

---

## Testing Requirements

Run:

- Python syntax/compile check.
- Unit tests.
- Lint.
- Formatting validation.
- Static/type checks where configured.

Minimum tests:

- Bootstrap imports.
- Settings load.
- Invalid configuration handling.
- Logging initializes.
- Base health system works.

---

## Acceptance Criteria

Phase 1 passes only when:

- Python 3.13.15 environment works.
- Project imports cleanly.
- `python main.py` runs.
- Tests run successfully.
- No paid service added.
- No secret committed.
- Repository structure remains clean.
- Configuration is centralized.
- Documentation matches implementation.

---

## Real User Validation

From a clean terminal:

1. Activate `.venv`.
2. Install dependencies.
3. Run tests.
4. Run `python main.py`.
5. Confirm the application starts without import/runtime errors.

---

## Antigravity Instructions

Before coding:

Read all project documentation.

Inspect the existing repository completely.

Do not restructure the entire project.

First report:

1. Current structure.
2. Missing foundation pieces.
3. Dependencies required for Phase 1 only.
4. Planned files to modify/create.
5. Testing strategy.

Then implement.

Do not begin Phase 2.

---

## Completion Report Requirements

Report:

1. Files created.
2. Files modified.
3. Dependencies added.
4. Startup behavior.
5. Tests executed.
6. Exact test results.
7. Remaining warnings.
8. Documentation changed.

---

## Phase Completion Rule

Phase 1 is complete only when the foundation is actually runnable and tested.

Do not continue with unresolved import errors, dependency errors, failing tests, or architecture duplication.