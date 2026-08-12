# HA Local Memory Tools

Local, persistent memory tools for LLM-powered assistants in Home Assistant.

> **Status:** early preview (`v0.1.x`). Expect breaking changes while the storage
> model and Home Assistant LLM integration are hardened.

## Why this exists

Home Assistant conversations already have short-term chat context, but many
assistant workflows benefit from explicit, user-controlled facts that survive
across conversations.

HA Local Memory Tools adds a small set of LLM-callable tools:

- `Remember`: store a user-approved fact locally.
- `Recall`: search stored facts.
- `Forget`: delete one fact by ID.
- `MemoryStats`: inspect the number of stored memories.

The integration is intentionally simple: no external database, no analytics,
and no extra cloud service.

## Privacy model

Memories are stored in Home Assistant's local storage. This project does not
send memory data to any additional service by itself. Your configured LLM
provider may receive memory text when the assistant calls `Recall`, so review
that provider's privacy settings before storing sensitive information.

## Requirements

- A recent Home Assistant release with the LLM tool contribution API.
- An LLM conversation integration that can use Home Assistant LLM tools.

## Manual installation

1. Copy `custom_components/ha_local_memory` into your Home Assistant
   `config/custom_components/` directory.
2. Restart Home Assistant.
3. Open **Settings → Devices & services → Add integration**.
4. Search for **HA Local Memory Tools** and add it.
5. In your assistant/conversation integration, select the Home Assistant LLM
   API that includes contributed tools.

## HACS

The repository includes `hacs.json` so it can be added as a custom repository
while the project is not yet in the HACS default catalog.

## Example

A compatible assistant can call:

```text
Remember(text="The bedroom should be 22°C at night", tags=["preference", "bedroom"])
Recall(query="bedroom temperature")
Forget(memory_id="...")
```

## Design principles

1. **Local first** — storage stays with Home Assistant.
2. **Explicit control** — facts can be inspected and deleted.
3. **Provider agnostic** — tools attach to Home Assistant's LLM API rather than
   a single model vendor.
4. **Small surface area** — fewer moving parts, easier review.

## Roadmap

- [x] Local persistent storage
- [x] Remember / Recall / Forget / Stats tools
- [x] UI setup flow
- [x] English and Simplified Chinese strings
- [ ] Configurable retention limits
- [ ] Better relevance scoring
- [ ] Export/import
- [ ] Per-assistant memory namespaces
- [ ] Integration tests against current Home Assistant
- [ ] HACS default-store submission

## Security

Please see [SECURITY.md](SECURITY.md). Do not include private Home Assistant
configuration or memory contents in public bug reports.

## Contributing

Bug reports and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
