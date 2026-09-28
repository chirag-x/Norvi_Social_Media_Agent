# Phase 24: Local Analytics Dashboard

## Overview
This phase introduces the Analytics command center, giving the user a high-level overview of their social media empire's performance.

## Key Features
- **Internal Production Metrics:** The dashboard directly queries the `norvi_local.db` SQLite database to dynamically render exactly how many clips the user has extracted, how many are queued in the schedule, and how many have successfully published.
- **Platform Reach Grid (Simulated):** A visual grid displaying aggregate views and likes grouped by platform (YouTube Shorts, TikTok, Instagram Reels). *Note: Because the API upload connections (Phase 19) require the user to manually provision external OAuth keys on Google Cloud before they can pull live data, this section currently displays simulated UI layout data to demonstrate the architecture.*

## Components Built
- `src.ui.views.analytics.AnalyticsView`: A UI view featuring a `QGridLayout` of SaaS-style metric cards.
- Integrated `DatabaseManager` logic to pull real-time counts from the `extracted_clips` and `scheduled_posts` tables on load.
