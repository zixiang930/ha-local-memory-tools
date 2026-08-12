"""HA Local Memory Tools integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DATA_STORE, DOMAIN
from .memory import LocalMemoryStore


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HA Local Memory Tools."""
    store = LocalMemoryStore(hass)
    await store.async_load()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {DATA_STORE: store}
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload HA Local Memory Tools."""
    domain_data = hass.data.get(DOMAIN, {})
    domain_data.pop(entry.entry_id, None)
    if not domain_data:
        hass.data.pop(DOMAIN, None)
    return True
