# Phase 4 — Local Storage & Privacy Foundation

## Status

Not Started

---

## Objective

Create the local-only storage system that keeps the user's projects, clients, content history, schedules, analytics, and settings private on their own computer.

---

## Scope

Implement:

- Application data directory.
- Local database.
- Database initialization.
- Schema versioning/migrations.
- Local settings.
- Local workspace.
- Client model.
- Brand profile model.
- Project/source metadata models.
- Secure credential abstraction.
- File-storage manager.
- Cache structure.
- Temp-file management.
- Local privacy boundary.

---

## Required Work

Recommended database baseline:

SQLite.

Database should be used for metadata, not large video binary storage.

Large files remain in managed local directories.

Suggested local entities:

- settings
- local_workspaces
- clients
- brand_profiles
- source_videos
- projects
- clip_candidates
- clip_versions
- schedules
- publish_jobs
- published_posts
- analytics_snapshots
- audit_events

Not every table needs full functionality yet, but the design must support later phases.

---

## Local File Organization

Use stable application-owned directories for:

- source videos
- proxy videos
- generated clips
- captions
- covers
- analytics cache
- temporary files
- logs

Never rely on the current working directory for permanent user data.

---

## Architecture Requirements

Use repositories/data services.

Do not let UI execute SQL.

Do not let each feature create its own database connection strategy.

Original user media must remain immutable.

Generated versions must use unique IDs/version IDs.

---

## Privacy Requirements

This entire storage layer is local.

No database synchronization to Nexus.

No client profile upload.

No analytics upload.

No background backup to Nexus.

---

## Security Requirements

- Sensitive social tokens must not be plaintext ordinary database fields.
- Sanitize file paths.
- Prevent path traversal.
- Use safe generated filenames/internal IDs.
- Avoid predictable temp-file collisions.
- Local database corruption should be detectable.
- Migration failures must not destroy existing data.

---

## Error Handling Requirements

Handle:

- Missing directories.
- Permission denied.
- Database locked.
- Database corrupt.
- Disk full.
- Migration error.
- File missing.
- Cache failure.

---

## Testing Requirements

Test:

- Fresh database creation.
- Reopen existing database.
- Migration.
- Client creation.
- Brand profile creation.
- Project creation.
- Local paths.
- Invalid path.
- Database failure.
- Temp cleanup.
- Secure-store abstraction.

---

## Acceptance Criteria

- Local DB initializes correctly.
- Application data persists across restart.
- Clients stay separated.
- No private local data sent to Nexus.
- UI does not directly access DB.
- Migration mechanism exists.
- Secure credential boundary exists.
- Disk/path failures handled.

---

## Real User Validation

Create:

- Client A.
- Client B.
- Separate brand profiles.

Restart application.

Verify all local information remains and stays separated.

Disconnect internet after authentication where possible and verify local stored data remains usable.

---

## Antigravity Instructions

Do not implement analytics logic or publishing logic yet.

Create only the durable local data/privacy foundation those features will use later.

---

## Completion Report Requirements

Report:

- Database selected.
- Schema/entities.
- Storage paths.
- Credential strategy.
- Migration strategy.
- Tests.
- Privacy verification.

---

## Phase Completion Rule

Local data must be stable and private before the application starts generating substantial user content.