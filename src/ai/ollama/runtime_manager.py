"""
Ollama Runtime Manager.

Responsibilities:

- Detect whether Ollama is installed
- Detect an existing running instance
- Start Ollama silently when required
- Track whether this application owns the process
- Health-check the Ollama service
- Stop only an application-owned Ollama process
"""
