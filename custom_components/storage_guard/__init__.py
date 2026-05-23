"""StorageGuard - Storage lifecycle management for Home Assistant."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .coordinator import StorageGuardCoordinator
from .services import async_setup_services, async_unload_services

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up StorageGuard from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    coordinator = StorageGuardCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {"coordinator": coordinator}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    await async_setup_services(hass)

    # Register frontend card as static path
    try:
        hass.http.register_static_path(
            "/storage_guard/storage-guard-card.js",
            hass.config.path(
                "custom_components/storage_guard/frontend/storage-guard-card.js"
            ),
            cache_headers=False,
        )
    except Exception:
        _LOGGER.debug("Static path already registered")

    # Auto-register card as Lovelace resource
    try:
        await _async_register_card(hass)
    except Exception as err:
        _LOGGER.debug("Could not auto-register card resource: %s", err)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a StorageGuard config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        if not hass.data[DOMAIN]:
            await async_unload_services(hass)

    return unload_ok


async def _async_register_card(hass: HomeAssistant) -> None:
    """Register the companion card as a Lovelace resource."""
    url = "/storage_guard/storage-guard-card.js"
    resources = hass.data.get("lovelace_resources")
    if resources is None:
        return
    for item in resources.async_items():
        if url in item.get("url", ""):
            return
    await resources.async_create_item({"res_type": "module", "url": url})
