"""Number platform for StorageGuard."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.number import NumberEntity, NumberEntityDescription, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    DEFAULT_ALERT_THRESHOLD,
    DEFAULT_BACKUP_KEEP_COUNT,
    DEFAULT_PURGE_KEEP_DAYS,
    DOMAIN,
)


@dataclass(frozen=True, kw_only=True)
class StorageGuardNumberDescription(NumberEntityDescription):
    """Describe a StorageGuard number entity."""

    default_value: float


NUMBER_DESCRIPTIONS: tuple[StorageGuardNumberDescription, ...] = (
    StorageGuardNumberDescription(
        key="alert_threshold",
        translation_key="alert_threshold",
        native_min_value=50,
        native_max_value=95,
        native_step=5,
        native_unit_of_measurement=PERCENTAGE,
        mode=NumberMode.SLIDER,
        default_value=DEFAULT_ALERT_THRESHOLD,
    ),
    StorageGuardNumberDescription(
        key="purge_keep_days",
        translation_key="purge_keep_days",
        native_min_value=1,
        native_max_value=30,
        native_step=1,
        native_unit_of_measurement="days",
        mode=NumberMode.SLIDER,
        default_value=DEFAULT_PURGE_KEEP_DAYS,
    ),
    StorageGuardNumberDescription(
        key="backup_keep_count",
        translation_key="backup_keep_count",
        native_min_value=1,
        native_max_value=10,
        native_step=1,
        native_unit_of_measurement="backups",
        mode=NumberMode.BOX,
        default_value=DEFAULT_BACKUP_KEEP_COUNT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up StorageGuard number entities."""
    async_add_entities(
        StorageGuardNumber(entry, description) for description in NUMBER_DESCRIPTIONS
    )


class StorageGuardNumber(RestoreEntity, NumberEntity):
    """Number entity for StorageGuard configuration."""

    entity_description: StorageGuardNumberDescription
    _attr_has_entity_name = True

    def __init__(
        self, entry: ConfigEntry, description: StorageGuardNumberDescription
    ) -> None:
        """Initialize the number entity."""
        self.entity_description = description
        self._entry = entry
        self._attr_unique_id = f"{DOMAIN}_{description.key}"
        self._attr_native_value = description.default_value
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
            try:
                self._attr_native_value = float(last_state.state)
            except (ValueError, TypeError):
                pass

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        self._attr_native_value = value
        self.async_write_ha_state()
