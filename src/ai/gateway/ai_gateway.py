"""
Central AI Gateway.

All Gemma/Ollama requests must flow through this layer.

Expected responsibilities:

- Semantic video analysis
- Candidate generation
- Candidate scoring
- Metadata generation
- Analytics interpretation
- Recommendation generation

Never allow raw model output to directly execute sensitive actions.
"""
