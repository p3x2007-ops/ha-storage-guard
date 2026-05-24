"""Select platform for StorageGuard."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import DEFAULT_MODE, DOMAIN, MODES


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up StorageGuard select entities."""
    async_add_entities([StorageGuardModeSelect(entry)])


class StorageGuardModeSelect(RestoreEntity, SelectEntity):
    """Select entity for StorageGuard operation mode."""

    _attr_options = MODES

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the mode select."""
        self._entry = entry
        self._attr_unique_id = f"{DOMAIN}_mode"
        self._attr_name = "StorageGuard Mode"
        self.entity_id = "select.storage_guard_mode"
        self._attr_current_option = DEFAULT_MODE
        self._attr_device_info = {
            "identifiers": {(DOMAIN, DOMAIN)},
            "name": "StorageGuard",
            "manufacturer": "StorageGuard",
            "model": "Storage Manager",
            "sw_version": "1.0.1",
        }

    async def async_added_to_hass(self) -> None:
        """Restore previous state."""
        await super().async_added_to_hass()
        if (last_state := await self.async_get_last_state()) is not None:
            if last_state.state in MODES:
                self._attr_current_option = last_state.state

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option
        self.async_write_ha_state()
