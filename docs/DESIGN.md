# Design System

## 1. Product Design Direction

Style:

- Modern.
- Premium.
- Minimal.
- Professional.
- Dark-first.
- Agency-oriented.
- AI-native.
- Clean rather than futuristic/gimmicky.

The application should feel like a serious professional content-control center.

---

# 2. Visual Theme

Primary theme:

Black / dark charcoal + blue accents.

Suggested baseline:

Background:
#090B10

Surface:
#11151D

Elevated Surface:
#171C26

Primary Blue:
#3578FF

Bright Accent:
#52A0FF

Primary Text:
#F5F7FA

Secondary Text:
#A8B0BD

Muted:
#70798A

Success:
semantic success token

Warning:
semantic warning token

Error:
semantic destructive token

Exact colors can be adjusted later to match final Nexus branding.

---

# 3. Typography

Use a professional, readable UI font.

Recommended:
Inter or another freely distributable application-safe font.

Do not package font files without checking their license.

Typography hierarchy:

Display
Heading 1
Heading 2
Heading 3
Body
Small
Caption
Metadata

---

# 4. UI Principles

- Important information first.
- Minimal clutter.
- Clear status.
- Large video previews.
- Fast clip review.
- Never hide failures.
- Avoid excessive modals.
- Progress should be visible.
- User always knows what happens next.

---

# 5. Main Navigation

Dashboard

Discover

Projects / Content

Clip Lab

Calendar

Publishing Queue

Analytics

Clients / Brands

Integrations

Activity

Settings

---

# 6. Authentication Screen

Fields:

- Email.
- Password.
- Nexus activation/API key.

Actions:

- Login.
- Logout.
- Activation status.

Never display the user's password after submission.

---

# 7. First-Run Local AI Setup

If Ollama/model setup is required, show a polished onboarding page.

Stages:

Checking local AI
↓
Installing runtime
↓
Starting runtime
↓
Downloading model
↓
Verifying model
↓
AI Ready

Show:

- Friendly description.
- Progress percentage when measurable.
- Download size if available.
- Current stage.
- Retry.
- Cancel when safe.

Do not show:

- Command prompt.
- Raw shell output.
- Internal CLI commands.

Advanced logs can exist in a diagnostic view.

---

# 8. Dashboard

Show:

- Ready-to-review clips.
- Scheduled posts.
- Failed jobs.
- Recently published content.
- Current processing jobs.
- Top recent local performers.
- Active client.
- Quick Discover button.

---

# 9. Discover Screen

Top:

Search field

Niche chips/toggles

Freshness/filter controls

Search button

Results:

Five large video cards.

Each card:

- Thumbnail.
- Title.
- Channel.
- Published information.
- Duration.
- Niche.
- Open on YouTube.
- Select.

---

# 10. Source Screen

Show:

- Large source preview.
- Title.
- Channel.
- Duration.
- Source link.
- Rights confirmation.
- Target clip duration.
- Analyze button.

---

# 11. Analysis Screen

Never use only an indefinite spinner.

Show stages:

Preparing video
Transcribing
Understanding content
Finding strong moments
Scoring moments
Creating previews
Finished

Allow application to remain responsive.

---

# 12. Clip Lab

Candidate card:

Thumbnail/preview
Score
Duration
Start/end
Explanation
Warnings
Platform recommendations

Actions:

Preview
Edit
Approve
Reject

Sort:

Highest Score
Source Order
Duration
Approved

---

# 13. Clip Editor

Desktop-oriented layout.

Left / Center:

Video preview.

Bottom:

Timeline.

Right:

- Transcript.
- Captions.
- Crop.
- Branding.
- Cover.
- Metadata.
- Score explanation.

Controls:

- Start.
- End.
- Undo.
- Save.
- Render.
- Approve.
- Reject.

---

# 14. Captions UI

Allow:

- Editing text.
- Correcting timestamps if practical.
- Style preset.
- Font.
- Size.
- Position.
- Highlighting.
- Preview.

---

# 15. Cover Selection

Show 3–5 recommended frames.

Allow manual frame scrub.

Optional:

- Cover text.
- Brand logo.
- Background treatment.

---

# 16. Publishing Composer

For every clip:

- Platform icons.
- Account.
- Title/caption.
- Hashtags.
- Cover.
- Date.
- Time.
- Timezone.
- Suggested best time.
- Final preview.

Main action:

Schedule

or

Publish Now

Both require confirmation.

---

# 17. Calendar

Views:

- Day.
- Week.
- Month.

Scheduled card:

- Thumbnail.
- Platform.
- Account.
- Client.
- Time.
- Status.

Actions:

- Open.
- Edit.
- Reschedule.
- Cancel.

---

# 18. Publishing Queue

Each job shows:

- Thumbnail.
- Platform.
- Account.
- Scheduled time.
- State.
- Attempt count.
- Last error.
- Next action.

States should use text + icon, not color alone.

---

# 19. Analytics

Views:

Overview
By Platform
By Client
By Clip
By Content Type
By Posting Time

Possible information:

- Views.
- Watch time.
- Engagement.
- Retention.
- Best duration.
- Best hook type.
- Best publishing windows.

Clearly distinguish:

Observed data

from

AI recommendation.

---

# 20. Client / Brand Profile

Fields:

- Brand name.
- Logo.
- Watermark.
- Caption preset.
- Tone.
- CTA.
- Hashtags.
- Banned words.
- Preferred duration.
- Preferred platforms.

Show live preview where useful.

---

# 21. Privacy UI

Settings should include a clear privacy section:

"Your content is processed locally."

Explain:

- Nexus does not receive videos.
- Nexus does not receive transcripts.
- Nexus does not receive analytics.
- Nexus does not receive social history.

Show network integrations individually so the user knows which external service receives what.

---

# 22. Loading States

Required for:

- Search.
- Ollama setup.
- Model download.
- Video preparation.
- Analysis.
- Rendering.
- Metadata.
- Scheduling.
- Publishing.
- Analytics.

---

# 23. Empty States

Design states for:

- No search results.
- No projects.
- No clips.
- No social accounts.
- No schedule.
- No analytics.
- No failures.

Each empty state should show the useful next action.

---

# 24. Error States

Every meaningful error should show:

What failed?

Why, when known?

Is retry safe?

What can the user do?

Support/reference ID if relevant.

Avoid generic:
"Something went wrong."

---

# 25. Accessibility

- Keyboard navigation.
- Visible focus.
- Sufficient contrast.
- Readable text.
- Accessible labels.
- Screen-reader-compatible form controls.
- Reduced motion.
- No color-only status.

---

# 26. Motion

Use subtle animation for:

- Screen transition.
- Job progress.
- Status changes.
- Card expansion.
- Success.

Avoid excessive glowing, motion, particles, or animations that slow productive work.