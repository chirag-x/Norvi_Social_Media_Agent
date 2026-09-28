# Phase 2 — Desktop Application Shell

## Status

Not Started

---

## Objective

Create the real desktop application shell that every future feature will live inside.

The application should look and behave like a professional product even though most feature pages are still empty.

---

## Scope

Implement:

- Desktop UI framework.
- Main window.
- Navigation.
- Page routing.
- Dashboard shell.
- Discover page shell.
- Clip Lab shell.
- Calendar shell.
- Publishing Queue shell.
- Analytics shell.
- Clients/Brands shell.
- Integrations shell.
- Settings shell.
- Global loading system.
- Global error presentation.
- Background-task-safe UI foundation.
- Dark Norvi visual design.
- Application lifecycle hooks.

---

## Required Work

Use the finalized desktop framework.

Preferred current architecture:

PySide6 / Qt.

Create:

- Main window.
- Sidebar navigation.
- Content container.
- Page manager/router.
- Reusable buttons.
- Reusable cards.
- Status badges.
- Empty-state component.
- Error-state component.
- Progress component.
- Confirmation dialog.
- Toast/notification system where appropriate.

Implement the dark black/blue visual system defined in `DESIGN.md`.

---

## Architecture Requirements

UI must not:

- Directly access SQLite.
- Directly execute FFmpeg.
- Directly call Ollama.
- Directly call YouTube APIs.
- Directly publish social posts.

Pages communicate through application services/controllers.

Long-running operations must never freeze the UI thread.

---

## Files / Modules Involved

Primarily:

- `src/ui/`
- `src/app/application.py`
- `src/app/lifecycle.py`
- `assets/`
- UI-related tests.

---

## Functional Requirements

Application starts into a real desktop window.

Navigation works between all major sections.

Pages may contain placeholders such as:

"Feature not implemented yet."

but must be visually consistent.

Window resizing must work.

The UI must remain responsive.

---

## Privacy Requirements

No telemetry.

No cloud UI analytics.

No external fonts/assets loaded at runtime unless intentionally approved.

---

## Security Requirements

Never display:

- Passwords.
- Tokens.
- Activation keys.
- Internal secrets.

Diagnostic views must redact sensitive values.

---

## Error Handling Requirements

UI initialization failure must produce a readable local error instead of a silent crash.

Individual page failure should not necessarily crash the complete application.

---

## Testing Requirements

Test:

- Main window startup.
- Navigation.
- All page construction.
- Reusable component rendering where practical.
- Basic application close.
- UI remains responsive during simulated background task.

---

## Acceptance Criteria

- Real desktop window opens.
- All planned navigation destinations exist.
- Dark Norvi theme is consistent.
- Navigation works.
- Window resizing works.
- No major blocking UI operation.
- No feature logic is incorrectly implemented in UI.
- Phase 1 tests still pass.

---

## Real User Validation

Run:

`python main.py`

Manually verify:

- Window opens correctly.
- Sidebar works.
- Every page can be opened.
- No broken layout.
- Close button exits normally.
- Multiple navigation changes do not crash.

---

## Antigravity Instructions

Do not implement later features.

Build only the reusable application shell and visual foundation.

Do not fill pages with fake functionality.

Preserve clean separation between UI and services.

---

## Completion Report Requirements

Report:

- UI framework/version.
- Screens created.
- Shared components created.
- Files changed.
- Tests.
- Manual UI validation.
- Remaining UX issues.

---

## Phase Completion Rule

The application must behave like a stable empty product shell before feature implementation begins.