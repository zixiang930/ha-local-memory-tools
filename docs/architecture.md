# Architecture

## Goal

Expose a minimal set of durable-memory tools through Home Assistant's LLM tool
contribution mechanism while keeping persistence local.

## Components

- `config_flow.py`: creates one UI-configured integration entry.
- `memory.py`: persistence using Home Assistant storage.
- `ranking.py`: dependency-free lightweight relevance ranking.
- `llm.py`: contributes Remember, Recall, Forget, and MemoryStats tools.

## Threat model

The integration does not create a network listener and does not call external
services. The primary privacy boundary is the configured LLM provider: recalled
memory text can be included in an LLM tool interaction.

## Non-goals for v0.1

- Vector databases
- Embeddings
- Automatic extraction of every conversation
- Cross-home synchronization
- Cloud-hosted memory
