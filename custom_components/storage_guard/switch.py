"""Switch platform for StorageGuard."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import DOMAIN, SWITCHES


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up StorageGuard switches."""
    async_add_entities(
        StorageGuardSwitch(entry, key, default)
        for key, default in SWITCHES.items()
    )


class StorageGuardSwitch(RestoreEntity, SwitchEntity):
    """Switch entity for StorageGuard feature toggles."""

    def __init__(self, entry: ConfigEntry, key: str, default: bool) -> None:
        """Initialize the switch."""
        self._entry = entry
        self._key = key
        self._attr_unique_id = f"{DOMAIN}_{key}"
        self._attr_name = f"StorageGuard {key.replace('_', ' ').title()}"
        self.entity_id = f"switch.storage_guard_{key}"
        self._attr_is_on = default
        self._default = default
        self._attr_device_info = {
            "identifiers": {(DOMAIN, DOMAIN)},
            "name": "StorageGuard",
            "manufacturer": "StorageGuard",
            "model": "Storage Manager",
            "sw_version": "1.0.0",
        }

    async def async_added_to_hass(self) -> None:
        """Restore previous state."""
        await super().async_added_to_hass()
        if (last_state := await self.async_get_last_state()) is not None:
            self._attr_is_on = last_state.state == "on"

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        self._attr_is_on = False
        self.async_write_ha_state()
