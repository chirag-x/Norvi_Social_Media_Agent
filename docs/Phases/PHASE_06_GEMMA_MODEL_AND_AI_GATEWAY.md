# Phase 6 — Gemma Model Management & AI Gateway

## Status

Not Started

---

## Objective

Make the configured Gemma4:Cloud-class Ollama model automatically available and create one central AI gateway for all future AI intelligence.

---

## Scope

Implement:

- Required model configuration.
- Installed-model detection.
- Automatic model pull/download when missing.
- Download progress.
- Interrupted download handling.
- Model readiness check.
- AI health test.
- Central AI gateway.
- Structured AI request/response support.
- Timeout handling.
- Schema validation.
- Prompt template organization.

---

## Model Requirement

Use the exact model identifier approved by the project owner.

Do not guess the final Ollama model ID.

Store the model identifier in centralized configuration.

---

## Startup Flow

Ollama Ready
↓
List local models
↓
Required model exists?
├── Yes → readiness test
└── No → download/pull
            ↓
       progress UI
            ↓
       verify model
↓
Gemma Ready

---

## Required Work

Create:

- Model manager.
- Local Ollama client.
- AI gateway.
- Structured output validator.
- AI request timeout/retry policy.
- AI health check.
- Prompt/version organization.

---

## AI Gateway Responsibilities

Future calls will include:

- Video semantic analysis.
- Clip candidate creation.
- Scoring.
- Explanation.
- Metadata generation.
- Scheduling recommendations.
- Analytics summaries.

No future service should directly create random Ollama HTTP requests.

---

## Structured Output Requirement

AI responses used programmatically must follow validated schemas.

Example categories:

- clip candidate
- score result
- metadata result
- recommendation result

Malformed model output must be rejected/repaired/retried safely.

---

## Privacy Requirements

All Gemma inference remains local.

No prompt.

No transcript.

No frames.

No generated text.

should be sent to Nexus.

---

## Security Requirements

Treat prompts and external media content as untrusted data.

Never execute arbitrary model-generated shell commands.

Never allow AI text to directly control sensitive APIs without validation.

---

## Error Handling Requirements

Handle:

- Model not found.
- Model pull failure.
- Disk full.
- Ollama unavailable.
- Model load timeout.
- Invalid AI response.
- AI timeout.
- Cancelled request.
- Out-of-memory/runtime error.

---

## UI Requirements

First-time download should show:

- Model preparation state.
- Progress if measurable.
- Clear warning that the local AI model may be large.
- Retry on failure.

---

## Testing Requirements

Test:

- Model installed.
- Model missing.
- Pull interrupted.
- Ollama unavailable.
- Simple inference.
- Structured response parsing.
- Invalid JSON/structure.
- Timeout.
- Cancellation.

---

## Acceptance Criteria

- Required model automatically detected.
- Missing model can be prepared.
- User does not need manual Ollama commands.
- AI gateway works.
- Structured responses validated.
- AI remains local.
- Previous phase tests pass.

---

## Real User Validation

Launch application with model installed.

Verify AI-ready state.

Then, in a controlled environment, test missing-model flow if practical.

Execute a simple internal test request and confirm a valid response.

---

## Antigravity Instructions

Do not yet implement social-media AI behavior.

Build the reusable intelligence infrastructure only.

Do not hardcode feature prompts directly into random services.

---

## Completion Report Requirements

Include:

- Exact model ID.
- Download flow.
- AI gateway API.
- Validation approach.
- Timeout strategy.
- Tests.
- Resource observations.

---

## Phase Completion Rule

Local AI must be dependable before it becomes responsible for content understanding.