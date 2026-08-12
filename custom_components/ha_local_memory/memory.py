"""Persistent local memory store."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from uuid import uuid4

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import MAX_MEMORIES, STORAGE_KEY, STORAGE_VERSION
from .ranking import relevance


@dataclass(slots=True)
class Memory:
    """One explicit memory item."""

    id: str
    text: str
    tags: list[str]
    created_at: str
    updated_at: str


class LocalMemoryStore:
    """Manage local persistent memories."""

    def __init__(self, hass: HomeAssistant) -> None:
        self._store: Store[list[dict]] = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._items: list[Memory] = []

    async def async_load(self) -> None:
        """Load memories from Home Assistant storage."""
        raw = await self._store.async_load() or []
        self._items = [
            Memory(
                id=str(item["id"]),
                text=str(item["text"]),
                tags=[str(tag) for tag in item.get("tags", [])],
                created_at=str(item["created_at"]),
                updated_at=str(item.get("updated_at", item["created_at"])),
            )
            for item in raw
            if isinstance(item, dict) and item.get("id") and item.get("text")
        ]

    async def _async_save(self) -> None:
        await self._store.async_save([asdict(item) for item in self._items])

    async def async_remember(self, text: str, tags: list[str] | None = None) -> Memory:
        """Store a new memory."""
        clean = " ".join(text.split()).strip()
        if not clean:
            raise ValueError("Memory text cannot be empty")

        now = datetime.now(UTC).isoformat()
        memory = Memory(
            id=uuid4().hex,
            text=clean,
            tags=sorted({tag.strip().casefold() for tag in (tags or []) if tag.strip()}),
            created_at=now,
            updated_at=now,
        )
        self._items.append(memory)
        if len(self._items) > MAX_MEMORIES:
            self._items = self._items[-MAX_MEMORIES:]
        await self._async_save()
        return memory

    def recall(self, query: str, limit: int) -> list[dict]:
        """Search memory without I/O."""
        scored = []
        q = query.strip()
        for memory in self._items:
            score = relevance(q, memory.text, memory.tags)
            if q.casefold() in memory.text.casefold():
                score = max(score, 0.95)
            if score > 0:
                scored.append((score, memory))

        scored.sort(key=lambda pair: (pair[0], pair[1].updated_at), reverse=True)
        return [
            {"id": m.id, "text": m.text, "tags": m.tags, "score": round(score, 3)}
            for score, m in scored[:limit]
        ]

    async def async_forget(self, memory_id: str) -> bool:
        """Delete a memory by ID."""
        before = len(self._items)
        self._items = [item for item in self._items if item.id != memory_id]
        changed = len(self._items) != before
        if changed:
            await self._async_save()
        return changed

    @property
    def count(self) -> int:
        """Return memory count."""
        return len(self._items)
