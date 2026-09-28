# Phase 13 — Clip Scoring & Ranking

## Status

Not Started

---

## Objective

Give every clip candidate an explainable high-potential score so users can quickly identify the strongest opportunities.

---

## Important Product Language

Never claim:

"This will go viral."

Use:

- High-potential.
- Strong candidate.
- Recommended.
- Higher relative score.

---

## Score Dimensions

Possible dimensions:

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
- Context dependency penalty.
- Duplicate penalty.
- Safety/quality penalties.

Historical account fit will be enhanced later after analytics exist.

---

## Output

Each candidate receives:

- Final score, e.g. 87/100.
- Component scores.
- Explanation.
- Strengths.
- Weaknesses/warnings.
- Recommended platform fit if useful.

---

## Explainability Requirement

Example:

"Strong opening question, unexpected answer within the first 12 seconds, and a clear payoff before the ending."

Do not output unexplained black-box numbers.

---

## Architecture Requirements

Scoring uses AI Gateway.

A deterministic aggregation layer may combine validated component values.

Keep scoring version/config identifiable so future algorithm changes can be tracked.

---

## Privacy Requirements

Scores remain local.

No candidate or score sent to Norvi.

---

## Error Handling Requirements

Handle:

- Missing signals.
- Invalid score.
- Score > 100.
- Score < 0.
- Invalid structured response.
- AI timeout.

---

## Testing Requirements

Verify:

- Scores validated.
- Component values validated.
- Explanation exists.
- Candidate ranking stable enough under defined configuration.
- Duplicate candidates rank appropriately.
- Missing optional features do not crash scoring.

Use a manually reviewed internal sample set.

---

## Acceptance Criteria

- Every candidate receives valid score.
- Every score has explanation.
- Candidates can be sorted.
- No guarantee-of-virality language.
- Invalid AI scoring safely rejected/retried.

---

## Real User Validation

Take candidates from Phase 12.

Compare ranking against human judgment.

The system does not need perfect agreement but should avoid obviously poor top-ranked segments.

---

## Antigravity Instructions

Do not overfit scoring to one sample channel.

Do not hardcode Gaming-specific scoring into universal core.

---

## Completion Report Requirements

Report:

- Score dimensions.
- Aggregation.
- Prompt/schema.
- Evaluation samples.
- Tests.
- Known limitations.

---

## Phase Completion Rule

Scoring must be understandable and useful before presenting a finished Clip Lab.