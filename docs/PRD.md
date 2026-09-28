# Product Requirements Document

## Product

Working Name: Norvi Social Media Agent

Product Type:
Local-first AI social media automation desktop application.

Primary Platform:
Windows desktop.

Primary Programming Language:
Python 3.13.15.

Primary AI Runtime:
Ollama running locally on the user's computer.

Primary AI Model:
Google Gemma 4 31B-class model configured through Ollama.

Development Environment:
Google Antigravity.

---

# 1. Product Vision

Build a complete AI-powered social media automation agent capable of taking a user from:

Content Discovery
→ Video Selection
→ Full Video Understanding
→ Short-Form Clip Generation
→ Editing
→ Approval
→ Scheduling
→ Publishing
→ Analytics
→ Continuous Local Learning

The goal is to remove repetitive social-media work while keeping the user in complete control.

The product must behave as a professional social media operator rather than only a video downloader or video cutter.

---

# 2. Core Product Principles

The product must follow these principles:

1. Local-first.
2. Private by design.
3. Zero mandatory paid AI APIs.
4. Zero mandatory paid cloud services.
5. User content never passes through Norvi infrastructure.
6. AI runs locally through Ollama.
7. Video processing happens locally.
8. Analytics remain locally stored.
9. Social-media credentials remain on the user's device wherever technically possible.
10. User approval is required before publishing.
11. AI makes recommendations.
12. Deterministic systems perform exact operations.
13. Failed jobs must remain visible and recoverable.
14. The application must never claim that a clip is guaranteed to go viral.

---

# 3. Problem

Social-media agencies and creators currently need multiple tools to:

- Discover trends.
- Search for content.
- Watch long videos.
- Find good moments.
- Cut clips.
- Convert horizontal video to vertical video.
- Add subtitles.
- Create titles.
- Create descriptions.
- Generate hashtags.
- Create covers.
- Schedule posts.
- Upload to multiple platforms.
- Track analytics.
- Learn what performs best.

This creates unnecessary manual work.

The Social Media Agent should bring these workflows together inside one desktop application.

---

# 4. Target Users

Primary users:

- Social-media agencies.
- Agency owners.
- Social-media managers.
- Content repurposing teams.
- Freelance social-media managers.
- Video content teams.

Secondary users:

- YouTubers.
- Podcasters.
- Streamers.
- Influencers.
- Brands.
- Individual creators.

---

# 5. Main User Outcome

The user should be able to open one desktop application and:

1. Discover today's relevant YouTube videos.
2. Search any creator, channel, topic, or keyword.
3. Select niches.
4. View the five best results.
5. Select a video.
6. Have AI understand the complete video.
7. Choose a short-form duration between 10 and 120 seconds.
8. Receive multiple high-potential clip suggestions.
9. Preview and edit them.
10. Generate captions and vertical versions.
11. Generate publishing metadata.
12. Select which clips should be published.
13. Select social platforms.
14. Schedule different clips for different dates and times.
15. Automatically publish them.
16. Track performance.
17. Receive better future recommendations based on the user's own local analytics.

---

# 6. Main User Flow

User launches app
↓
Authenticate with Norvi account/license
↓
Local AI environment checked
↓
Ollama started silently
↓
Gemma model checked
↓
Application becomes ready
↓
Select local workspace/client
↓
Discover YouTube content
↓
Search / choose niches
↓
Receive top five videos
↓
Preview / open on YouTube
↓
Select source video
↓
Confirm rights/permission
↓
Choose target clip duration
↓
Analyze complete source
↓
Generate candidate clips
↓
Score candidates
↓
Explain selections
↓
Generate vertical versions
↓
Generate captions
↓
Generate hooks/covers
↓
Review/edit
↓
Approve clips
↓
Generate platform metadata
↓
Select platforms/accounts
↓
Choose schedule
↓
Queue publishing
↓
Publish
↓
Verify publishing
↓
Collect analytics locally
↓
Improve future recommendations locally

---

# 7. Feature Group A — YouTube Discovery

## Requirements

The app must allow the user to discover current YouTube content.

Default discovery behavior should prioritize fresh/recent content.

The main discovery view should display five primary video results.

Each result should include when available:

- Thumbnail.
- Video title.
- Channel name.
- Publication date/time.
- Duration.
- Available engagement information.
- Matching niche.
- Reason the result appeared.
- Open on YouTube button.
- Select Video button.

---

# 8. Search

The user can search using free text.

Examples:

- Techno Gamerz
- MrBeast
- AI news
- Gaming
- Podcast
- GTA
- Technology
- Business advice

Search should support:

- Creator names.
- Channel names.
- Keywords.
- Topics.
- Video subjects.

---

# 9. Niche Selection

The user can select one or multiple niches.

Initial examples:

- Gaming
- Technology
- Podcasts
- News
- Movies
- Entertainment
- Business
- Finance
- Education
- Sports
- Comedy
- Lifestyle
- Music

The exact list may depend on available discovery APIs.

---

# 10. Multi-Niche Behavior

If the user selects multiple niches, the five results should be diversified across those niches whenever enough results are available.

Example:

Gaming + Podcasts + News

Possible results:

1. Gaming
2. Podcast
3. News
4. Gaming
5. Podcast

The system should avoid returning five results from only one selected category unless there are insufficient alternatives.

---

# 11. Source Selection

The user can:

- Preview basic information.
- Open the full source on YouTube.
- Return to the application.
- Select one source video.
- Continue to analysis.

---

# 12. Rights Confirmation

Before downloading, editing, or republishing source content, the user must confirm that they:

- Own the content, or
- Have permission to repurpose it, or
- Have the appropriate rights/license.

Public availability on YouTube must never automatically be treated as permission to repost content.

The application records this confirmation locally.

Norvi must not receive this data.

---

# 13. Clip Duration

The user can choose a target duration from:

10 seconds
to
120 seconds.

Suggested presets:

- 15 seconds
- 30 seconds
- 45 seconds
- 60 seconds
- 90 seconds
- 120 seconds

Custom values between 10 and 120 seconds may also be supported.

---

# 14. Complete Video Analysis

The app should analyze the complete source video before producing final candidate rankings.

Analysis may include:

- Timestamped transcript.
- Topic changes.
- Scene changes.
- Speaker changes.
- Important statements.
- Questions and answers.
- Humor.
- Reactions.
- Emotional moments.
- Surprising moments.
- Strong opinions.
- Useful information.
- Demonstrations.
- Storytelling peaks.
- Before/after moments.
- Visual activity.
- Silence.
- Dead air.
- Repeated content.
- Audio quality.
- Context dependencies.

The app must not simply divide a video into equal chunks.

---

# 15. Candidate Clip Generation

The system should find natural standalone short-form moments.

Each candidate includes:

- Candidate ID.
- Start timestamp.
- End timestamp.
- Duration.
- Transcript.
- Summary.
- Score.
- Score components.
- Selection explanation.
- Warnings.
- Recommended platform fit.
- Preview.

---

# 16. High-Potential Score

Each candidate receives a high-potential score.

Example:

87/100

Possible score dimensions:

- Hook strength.
- Clarity.
- Novelty.
- Emotion.
- Payoff.
- Pacing.
- Information density.
- Visual interest.
- Standalone quality.
- Audience relevance.
- Historical account fit.
- Context dependency.
- Repetition.
- Safety.

The application must not state that a score guarantees virality.

---

# 17. Explainable Selection

Each clip should include an explanation.

Example:

"This segment starts immediately with a strong question, contains a surprising response after 11 seconds, and reaches a clear payoff without requiring the viewer to watch the earlier video."

---

# 18. Vertical Short-Form Creation

The system should support:

- 9:16 conversion.
- Intelligent reframing.
- Subject tracking.
- Speaker tracking where possible.
- Safe areas.
- Audio normalization.
- Resolution normalization.
- Optional watermark.
- Optional logo.
- Optional progress indicator.
- Platform-specific export variants.

---

# 19. Automatic Captions

The application should support:

- Local speech transcription.
- Timestamped subtitles.
- Caption styling.
- Highlighted words.
- User correction.
- Safe-area placement.
- Brand-specific caption presets.

---

# 20. Hook Enhancement

The AI may suggest:

- Removing dead air.
- Starting later.
- Starting on the strongest sentence.
- Adding short hook text.
- Alternative openings.

Any transformation that could change meaning must remain user-reviewable.

The system must never invent a quote and present it as something spoken in the source.

---

# 21. Manual Clip Editor

The user should be able to:

- Change start point.
- Change end point.
- Preview.
- Change crop.
- Correct subtitles.
- Select cover.
- Add/remove branding.
- Edit metadata.
- Save a version.
- Approve.
- Reject.

---

# 22. Cover Selection

The AI should recommend useful frames from the video.

The user may:

- Pick an AI recommendation.
- Select another frame manually.
- Add optional cover text.
- Apply local brand styling.

---

# 23. Metadata Generation

For each approved clip, Gemma can generate:

- Title.
- Description.
- Social caption.
- Hashtags.
- Keywords.
- CTA.
- Alternative versions.

All generated metadata must remain editable.

---

# 24. Initial Publishing Platforms

Target platforms:

- YouTube Shorts.
- Instagram Reels.
- Facebook Reels.

The architecture must allow additional adapters later.

---

# 25. Clip Selection Before Publishing

The AI may generate ten clips.

The user may select only seven.

Only selected and approved clips continue to publishing.

AI generation does not equal publishing permission.

---

# 26. Scheduling

The user can define independently for every clip:

- Platform.
- Account.
- Date.
- Time.
- Timezone.
- Metadata.
- Cover.
- Publishing options.

Different clips can use different schedules.

The same clip can also have different times on different platforms.

---

# 27. Smart Scheduling

When enough analytics exist locally, the AI may suggest posting times.

Recommendations may use:

- Historical performance.
- Content type.
- Clip duration.
- Platform.
- Day.
- Time.
- Audience behavior when available.

The user decides whether to accept the recommendation.

---

# 28. Durable Publishing Queue

Publishing states:

Draft
→ Needs Review
→ Approved
→ Scheduled
→ Queued
→ Uploading
→ Platform Processing
→ Published

Failure states:

- Failed
- Retry Scheduled
- Authentication Required
- Cancelled

A failed post must never disappear.

---

# 29. Retry and Duplicate Protection

The app must:

- Retry appropriate temporary failures.
- Avoid repeating permanent failures.
- Prevent duplicate posts.
- Keep attempt history.
- Ask for account reconnection when authorization expires.
- Verify success before showing Published.

---

# 30. Analytics

Where supported by each platform, the app may collect:

- Views.
- Reach.
- Watch time.
- Average watch duration.
- Retention.
- Likes.
- Comments.
- Shares.
- Saves.
- Followers/subscribers.
- Clicks.

All analytics remain on the user's computer.

Norvi receives none of these analytics.

---

# 31. Local Learning

The AI can use locally stored analytics to improve:

- Clip ranking.
- Suggested duration.
- Hook recommendations.
- Posting-time suggestions.
- Content categories.
- Caption styles.

Learning must remain local.

Data from one client must never influence another client unless the user intentionally combines them.

---

# 32. Local Workspace / Clients

Users can locally manage multiple brands or clients.

Example:

Local Workspace
├── Client A
│   ├── Brand Profile
│   ├── Accounts
│   ├── Videos
│   ├── Schedules
│   └── Analytics
├── Client B
└── Client C

These records remain completely local.

---

# 33. Brand Profiles

A local brand profile can contain:

- Brand name.
- Logo.
- Watermark.
- Fonts.
- Caption style.
- Tone.
- Preferred CTAs.
- Preferred hashtags.
- Banned words.
- Topics to avoid.
- Target audience.
- Preferred duration.
- Preferred platforms.
- Default export configuration.

---

# 34. Duplicate Detection

Before publishing, the app should detect:

- Exact duplicate clips.
- Already scheduled clips.
- Similar source segments.
- Previously published versions.

The user should receive a warning before duplicate publishing.

---

# 35. Content Series

Related clips may be grouped automatically.

Example:

Part 1
Part 2
Part 3

The user can:

- Accept.
- Rename.
- Reorder.
- Remove grouping.

---

# 36. Privacy Requirements

This is a non-negotiable product requirement.

Norvi must NOT collect:

- YouTube searches.
- Source video history.
- Downloaded videos.
- User videos.
- Generated clips.
- Transcripts.
- Captions.
- Prompts.
- Gemma responses.
- Titles.
- Descriptions.
- Hashtags.
- Scheduling history.
- Social account content.
- Social analytics.
- Brand data.
- Client data.
- Local logs.
- Publishing history.

All these stay locally on the user's computer.

---

# 37. Norvi Server Boundary

The Norvi server is used only for account/license authentication.

Permitted information includes:

- User account email.
- Authentication information required by existing Norvi website.
- License/API/activation key.
- Entitlement/activation status.

The app must not send social-media workflow data to Norvi.

Passwords must never be stored in plaintext.

After authentication, token/session-based authentication should be used instead of continually transmitting the password.

The activation/license backend itself is outside the scope of this project.

---

# 38. Local AI Runtime

AI inference must run locally.

Architecture:

Desktop App
→ Local Ollama Runtime
→ Gemma 4 31B-class Model

No paid AI API is required.

---

# 39. Ollama First-Run Experience

On startup:

1. Check whether Ollama exists.
2. If missing, guide/install the supported Ollama runtime.
3. Hide unnecessary command-line windows.
4. Complete required first-time Ollama setup.
5. If the exact Ollama distribution requires account setup, show that required flow.
6. Check whether the required Gemma model exists.
7. If missing, download/pull the model.
8. Show clean application-level progress.
9. Verify Ollama health.
10. Verify model availability.
11. Mark AI Ready.

The user should not need to manually enter Ollama commands.

---

# 40. Normal Ollama Startup

On later app launches:

App opens
→ Check Ollama
→ Start Ollama silently if required
→ Check model
→ Verify health
→ Agent ready

The user should not see CMD/PowerShell windows.

---

# 41. Ollama Shutdown

If the application itself started Ollama, it may stop that Ollama process when the application exits.

If Ollama was already running before the application started, the app must not blindly kill it because another application may be using it.

---

# 42. Zero-Cost Requirement

The product must have:

- No mandatory paid LLM API.
- No mandatory paid transcription API.
- No mandatory paid video-processing API.
- No mandatory paid cloud database.
- No mandatory paid hosting requirement for user content.
- No mandatory paid analytics system.

Prefer:

- Local models.
- Open-source software.
- Official free platform integrations.
- Local storage.
- Local processing.

Internet/electricity/hardware costs are outside the software's control.

---

# 43. AI vs Deterministic Responsibilities

AI responsibilities:

- Understand transcript.
- Understand selected visual context.
- Detect interesting moments.
- Rank clips.
- Explain rankings.
- Generate metadata.
- Recommend posting times.
- Analyze local performance history.

Deterministic responsibilities:

- Video cutting.
- Rendering.
- Storage.
- Database.
- Authentication.
- Scheduling.
- Queue execution.
- OAuth.
- API requests.
- Retry.
- Deduplication.
- Publish verification.

---

# 44. MVP

MVP should prove the full workflow:

- Desktop application.
- Norvi authentication boundary.
- Local database.
- Ollama manager.
- Gemma model manager.
- YouTube discovery.
- Search.
- Niche filtering.
- Five results.
- Source selection.
- Rights confirmation.
- 10–120 second duration.
- Full transcript analysis.
- Candidate generation.
- Candidate score and explanation.
- Preview.
- Basic vertical render.
- Captions.
- Clip approval.
- Metadata.
- One production-quality social publishing adapter.
- Scheduler.
- Queue.
- Retry.
- Publish verification.
- Local history.

---

# 45. Future Expansion

After MVP:

- All three publishing platforms.
- Advanced active-speaker reframing.
- Advanced brand templates.
- Duplicate detection.
- Series detection.
- Smart posting time.
- Local analytics.
- Local learning.
- More platforms.
- Team/client workflows if eventually required.

---

# 46. Out of Scope

Not part of the initial implementation:

- Cloud storage of user social data by Norvi.
- Paid AI services.
- Centralized Norvi analytics collection.
- Training Norvi models using user content.
- Selling user activity data.
- Native mobile app.
- Guaranteed virality.
- Activation system implementation.
- Circumventing social-platform policies.

---

# 47. Success Criteria

The product is successful when a user can:

1. Install/open the application.
2. Authenticate.
3. Have Ollama/model prepared automatically.
4. Search YouTube.
5. Receive five results.
6. Select a video.
7. Analyze the full content.
8. Generate useful short clips.
9. Review/edit them.
10. Approve selected clips.
11. Schedule them.
12. Publish them.
13. Verify publishing.
14. View local analytics.
15. Do all social workflow processing without sending their content to Norvi.