"""Resolve StorageGuard entities by their stable unique_id.

The default entity_ids defined in code (e.g. switch.storage_guard_auto_clean_logs)
can be overridden by Home Assistant when translations are active or by users via
the UI. Resolving by unique_id keeps the integration working regardless of the
resulting entity_id slug (which may be in any language).
"""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN, MODE_MANUAL


def resolve(hass: HomeAssistant, domain: str, key: str) -> str | None:
    """Return the current entity_id for a StorageGuard entity by unique_id key."""
    registry = er.async_get(hass)
    unique_id = f"{DOMAIN}_{key}"
    return registry.async_get_entity_id(domain, DOMAIN, unique_id)


def get_switch_state(hass: HomeAssistant, key: str) -> bool:
    """Return True if the StorageGuard switch identified by key is on."""
    entity_id = resolve(hass, "switch", key)
    if not entity_id:
        return False
    state = hass.states.get(entity_id)
    return state is not None and state.state == "on"


def get_number_value(hass: HomeAssistant, key: str, default: float) -> float:
    """Return the float value of a StorageGuard number entity (or default)."""
    entity_id = resolve(hass, "number", key)
    if not entity_id:
        return default
    state = hass.states.get(entity_id)
    if state is None or state.state in ("unknown", "unavailable"):
        return default
    try:
        return float(state.state)
    except (ValueError, TypeError):
        return default


def get_mode(hass: HomeAssistant) -> str:
    """Return the current StorageGuard operating mode."""
    entity_id = resolve(hass, "select", "mode")
    if not entity_id:
        return MODE_MANUAL
    state = hass.states.get(entity_id)
    if state is None or state.state in ("unknown", "unavailable"):
        return MODE_MANUAL
    return state.state
