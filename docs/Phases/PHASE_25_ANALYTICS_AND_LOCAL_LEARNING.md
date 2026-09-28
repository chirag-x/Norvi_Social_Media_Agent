# Phase 25 — Analytics & Local Learning

## Status

Not Started

---

## Objective

Complete the feedback loop by collecting available platform performance data locally and using it to improve future recommendations.

---

## Analytics Sources

Initial:

- YouTube.
- Instagram.
- Facebook.

Use each platform's supported metrics.

Do not pretend every platform exposes identical data.

---

## Possible Metrics

Where available:

- Views.
- Reach.
- Watch time.
- Average view duration.
- Retention.
- Likes.
- Comments.
- Shares.
- Saves.
- Follower/subscriber changes.
- Clicks.

---

## Data Model

Store local historical snapshots.

Do not overwrite previous snapshots when time-series history is valuable.

Represent unavailable metric as unavailable/null, not zero.

---

## Analytics UI

Support useful views:

- Overview.
- Platform.
- Client.
- Clip.
- Content category.
- Posting time.
- Clip duration.

---

## Local Learning

Use only local history to recommend:

- Better clip lengths.
- Better posting windows.
- Stronger hook patterns.
- Better-performing topics.
- Better caption styles.
- Potential content direction.

---

## Recommendation Requirements

Recommendations should include evidence.

Example:

"Your last 12 gaming clips between 30–45 seconds had higher average completion than clips longer than 60 seconds."

Avoid unsupported causation.

Say:

"historically associated with"

rather than:

"this caused performance."

---

## Cold Start

When little/no history exists:

- Use general content-quality signals.
- Clearly say that there is insufficient personal history.
- Do not fabricate account-specific conclusions.

---

## Client Isolation

Client A analytics cannot influence Client B unless the user explicitly chooses a shared analysis model.

Default is strict separation.

---

## Privacy Requirements

This is one of the most important rules:

Analytics remain local.

Performance history remains local.

Learning remains local.

Norvi gets none of it.

---

## Error Handling Requirements

Handle:

- Unsupported metric.
- API unavailable.
- Expired token.
- Partial analytics response.
- Rate limit.
- Missing historical post.
- Deleted social post.

---

## Testing Requirements

Test:

- Successful sync.
- Missing metrics.
- Historical snapshots.
- Multiple platforms.
- Multiple clients.
- Cold start.
- Recommendation generation.
- Cross-client leakage prevention.

---

## Acceptance Criteria

- Analytics sync locally.
- UI displays available metrics correctly.
- Missing data not misrepresented.
- Recommendations use local history.
- Recommendations explain evidence.
- Client separation maintained.

---

## Real User Validation

Use test/real published posts from earlier phases.

Fetch available metrics.

Verify numbers against platform interfaces where possible.

Generate local recommendations.

---

## Antigravity Instructions

Do not add Norvi cloud analytics.

This feature must preserve the product's local-first privacy promise.

---

## Completion Report Requirements

Report:

- Metrics by platform.
- Local schema.
- Sync behavior.
- Recommendation logic.
- Privacy verification.
- Tests.

---

## Phase Completion Rule

The full discover → create → publish → learn loop must now exist locally.