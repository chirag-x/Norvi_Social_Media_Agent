# Phase 23: Content Series (Multi-Part Generation)

## Overview
This phase upgrades Gemma's reasoning engine to understand the concept of sequential storytelling on short-form platforms (TikTok, Shorts, Reels). When a podcast or video contains a highly engaging story that cannot be squeezed into a standard 60-second window, the AI automatically slices it into sequential parts.

## Key Features
- **Prompt Engineering (AI Logic Update):** The core system prompt in `GemmaEngine` has been heavily modified with strict rules instructing the model to split long stories into sequential parts and append `(Part 1)`, `(Part 2)` to the titles.
- **Cliffhanger Enforcement:** The AI is specifically instructed to choose split-points that create tension (a "cliffhanger") to guarantee viewers return for the next part.
- **Dynamic Metadata Integration:** The metadata generation engine in the `PublishingQueueView` has been taught to recognize series tags in titles. 
  - If it sees `(Part 1)`, the AI will automatically write copy telling the user to "like and follow for Part 2". 
  - If it sees `(Part 2)`, it will write copy reminding viewers to "watch Part 1 first".

## Components Modified
- `src.services.ai.gemma_engine`: Added critical rules for slicing stories.
- `src.ui.views.publishing_queue`: Augmented the post description AI prompt to handle series metadata styling.
