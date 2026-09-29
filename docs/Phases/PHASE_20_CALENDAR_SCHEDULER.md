# Phase 18 & 20: Calendar & Scheduler

## Overview
These phases transition the application from a video editor into a true social media manager. It introduces a persistent database schema and UI required to queue, schedule, and visually track when content will go live on various platforms.

## Key Features
- **Database Schema:** Created the `scheduled_posts` table inside `nexus_local.db` via SQL migrations to persistently store video paths, AI-generated metadata, platform targets, and scheduled release times.
- **Publishing Queue Integration:** Added a `QDateTimeEdit` calendar picker directly into the Publishing Queue so the user can accurately set the future publish date/time immediately after generating metadata.
- **Calendar Dashboard:** Built the `CalendarView` tab featuring a read-only `QTableWidget`. This acts as the command center for the user to see all pending and published posts sorted by their chronological release time.

## Components Built
- `src.storage.database.schemas.001_initial`: The SQL table defining the scheduled post entity.
- `src.ui.views.calendar_view.CalendarView`: The visual data grid representing the schedule.
- UI extensions in the `PublishingQueueView` to bridge metadata generation and scheduling.

## Transition
With the schedule now persistently saving to the local database, the final frontier is Phase 19: Social Account Integrations. The next step is building the Settings tab where the user can connect their YouTube and TikTok API keys, allowing the background engine to actually execute these scheduled database records and upload the files to the internet.
