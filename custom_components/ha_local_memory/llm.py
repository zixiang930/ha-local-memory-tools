"""LLM tools contributed by HA Local Memory Tools."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.components import llm
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.llm import LLMContext, ToolInput
from homeassistant.util.json import JsonObjectType

from .const import DATA_STORE, DEFAULT_RECALL_LIMIT, DOMAIN
from .memory import LocalMemoryStore


def _get_store(hass: HomeAssistant) -> LocalMemoryStore:
    domain_data = hass.data.get(DOMAIN)
    if not domain_data:
        raise HomeAssistantError("HA Local Memory Tools is not configured")
    first = next(iter(domain_data.values()), None)
    if not first or DATA_STORE not in first:
        raise HomeAssistantError("Memory store is unavailable")
    return first[DATA_STORE]


class RememberTool(llm.Tool):
    """Store one explicit memory."""

    name = "Remember"
    description = (
        "Store a durable fact or preference only when the user clearly wants it remembered."
    )
    parameters = vol.Schema(
        {
            vol.Required("text"): str,
            vol.Optional("tags", default=[]): [str],
        }
    )

    async def async_call(
        self, hass: HomeAssistant, tool_input: ToolInput, llm_context: LLMContext
    ) -> JsonObjectType:
        memory = await _get_store(hass).async_remember(
            tool_input.tool_args["text"], tool_input.tool_args.get("tags", [])
        )
        return {"stored": True, "id": memory.id, "text": memory.text, "tags": memory.tags}


class RecallTool(llm.Tool):
    """Recall relevant memory."""

    name = "Recall"
    description = "Search durable user-approved memories for facts relevant to the current request."
    parameters = vol.Schema(
        {
            vol.Required("query"): str,
            vol.Optional("limit", default=DEFAULT_RECALL_LIMIT): vol.All(
                int, vol.Range(min=1, max=20)
            ),
        }
    )

    async def async_call(
        self, hass: HomeAssistant, tool_input: ToolInput, llm_context: LLMContext
    ) -> JsonObjectType:
        matches = _get_store(hass).recall(
            tool_input.tool_args["query"], tool_input.tool_args["limit"]
        )
        return {"matches": matches, "count": len(matches)}


class ForgetTool(llm.Tool):
    """Delete one memory."""

    name = "Forget"
    description = "Delete a stored memory when the user asks to forget it."
    parameters = vol.Schema({vol.Required("memory_id"): str})

    async def async_call(
        self, hass: HomeAssistant, tool_input: ToolInput, llm_context: LLMContext
    ) -> JsonObjectType:
        deleted = await _get_store(hass).async_forget(tool_input.tool_args["memory_id"])
        return {"deleted": deleted, "id": tool_input.tool_args["memory_id"]}


class MemoryStatsTool(llm.Tool):
    """Return local memory statistics."""

    name = "MemoryStats"
    description = "Return the number of durable memories currently stored."
    parameters = vol.Schema({})

    async def async_call(
        self, hass: HomeAssistant, tool_input: ToolInput, llm_context: LLMContext
    ) -> JsonObjectType:
        return {"count": _get_store(hass).count}


@callback
def async_get_tools(
    hass: HomeAssistant, llm_context: LLMContext, api_id: str
) -> llm.LLMTools | None:
    """Expose local memory tools to Home Assistant LLM APIs."""
    if not hass.data.get(DOMAIN):
        return None

    return llm.LLMTools(
        tools=[RememberTool(), RecallTool(), ForgetTool(), MemoryStatsTool()],
        prompt=(
            "Use Remember only for information the user clearly asks to preserve or durable "
            "preferences that are appropriate to store. Use Recall when durable memory may help. "
            "Never store secrets, authentication tokens, payment data, or highly sensitive data "
            "unless the user explicitly requests it. Use Forget when the user asks to delete memory."
        ),
    )
