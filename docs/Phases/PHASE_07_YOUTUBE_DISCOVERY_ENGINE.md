# Phase 7 — YouTube Discovery Engine

## Status

Not Started

---

## Objective

Implement the first complete user-facing feature: discovering current YouTube content using free-text search and niche filters and showing five useful video candidates.

---

## User Experience

Discover page contains:

- Search field.
- Niche multi-select.
- Fresh/recent mode.
- Search action.
- Five primary video cards.

Each card displays available:

- Thumbnail.
- Title.
- Channel.
- Publication date/time.
- Duration.
- Relevant statistics.
- Matched niche.
- Reason/result context.
- Open on YouTube.
- Select Video.

---

## Search Requirements

Accept:

- Creator name.
- Channel name.
- Topic.
- Keyword.
- General search text.

Examples:

- Techno Gamerz
- MrBeast
- gaming
- AI podcast

---

## Freshness Requirement

The default goal is to prioritize current/recent content, especially content relevant today.

Do not fabricate a platform concept called "today trending" if the selected official integration cannot provide it exactly.

If necessary, transparently derive a fresh/high-interest result set from current video search data.

---

## Niche Requirements

Support multiple selected niches.

Potential niches:

- Gaming.
- Technology.
- Podcasts.
- News.
- Entertainment.
- Movies.
- Business.
- Finance.
- Education.
- Sports.
- Comedy.
- Lifestyle.
- Music.

Final mapping should match available platform capabilities.

---

## Multi-Niche Diversification

If multiple niches are selected, distribute results across selected niches where reasonable.

Avoid returning five results from one niche simply because it dominates raw ranking.

---

## Architecture Requirements

Create:

`VideoDiscoveryProvider`

YouTube implementation remains behind its adapter.

UI does not directly call YouTube.

Normalize all returned result data into internal domain models.

---

## Cost Requirement

Use no mandatory paid search service.

Prefer official supported free/quota-based mechanisms.

---

## Privacy Requirements

Search requests go only to the service required to fulfill the YouTube search.

Nexus must never receive the user's YouTube query or result history.

Search history should remain local if stored.

---

## Error Handling Requirements

Handle:

- No internet.
- Quota/rate limit.
- Invalid API credential/config.
- Zero results.
- Fewer than five results.
- Invalid/missing video metadata.
- Removed video.
- Provider timeout.

---

## Testing Requirements

Test:

- Empty/default discovery.
- Keyword.
- Creator.
- Channel.
- Single niche.
- Multiple niches.
- Freshness.
- Fewer than five results.
- No results.
- API/network failure.
- Result normalization.
- Diversification.

---

## Acceptance Criteria

- Discovery UI works.
- User can search.
- User can choose niches.
- Five primary candidates shown when available.
- Results can be opened on YouTube.
- User can select a video.
- Nexus receives no discovery data.

---

## Real User Validation

From real application:

1. Search `Techno Gamerz`.
2. Search a topic.
3. Select Gaming.
4. Select multiple niches.
5. Open a result on YouTube.
6. Select a video inside the app.
7. Confirm no crash or stale loading state.

---

## Antigravity Instructions

Do not implement video downloading or analysis yet.

This phase ends when source discovery and selection handoff work reliably.

Do not hardcode example channels into product logic.

---

## Completion Report Requirements

Include:

- Discovery source.
- Result ranking logic.
- Multi-niche strategy.
- API/quota limitations.
- Tests.
- Real searches performed.

---

## Phase Completion Rule

The application must reliably find and select source videos before building downstream processing.