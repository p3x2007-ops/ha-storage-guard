"""Binary sensor platform for StorageGuard."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DATA_DISK_PERCENT,
    DEFAULT_ALERT_THRESHOLD,
    DEFAULT_CRITICAL_THRESHOLD,
    DOMAIN,
)
from .coordinator import StorageGuardCoordinator


@dataclass(frozen=True, kw_only=True)
class StorageGuardBinarySensorDescription(BinarySensorEntityDescription):
    """Describe a StorageGuard binary sensor."""

    threshold_key: str
    default_threshold: int


BINARY_SENSOR_DESCRIPTIONS: tuple[StorageGuardBinarySensorDescription, ...] = (
    StorageGuardBinarySensorDescription(
        key="threshold_exceeded",
        translation_key="threshold_exceeded",
        device_class=BinarySensorDeviceClass.PROBLEM,
        threshold_key="alert_threshold",
        default_threshold=DEFAULT_ALERT_THRESHOLD,
    ),
    StorageGuardBinarySensorDescription(
        key="critical",
        translation_key="critical",
        device_class=BinarySensorDeviceClass.PROBLEM,
        threshold_key="critical_threshold",
        default_threshold=DEFAULT_CRITICAL_THRESHOLD,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up StorageGuard binary sensors."""
    coordinator: StorageGuardCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    async_add_entities(
        StorageGuardBinarySensor(coordinator, description, entry)
        for description in BINARY_SENSOR_DESCRIPTIONS
    )


class StorageGuardBinarySensor(
    CoordinatorEntity[StorageGuardCoordinator], BinarySensorEntity
):
    """Representation of a StorageGuard binary sensor."""

    entity_description: StorageGuardBinarySensorDescription

    def __init__(
        self,
        coordinator: StorageGuardCoordinator,
        description: StorageGuardBinarySensorDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._entry = entry
        self._attr_unique_id = f"{DOMAIN}_{description.key}"
        self._attr_name = f"StorageGuard {description.key.replace('_', ' ').title()}"
        self.entity_id = f"binary_sensor.storage_guard_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, DOMAIN)},
            "name": "StorageGuard",
            "manufacturer": "StorageGuard",
            "model": "Storage Manager",
            "sw_version": "1.0.0",
        }

    @property
    def is_on(self) -> bool | None:
        """Return true if threshold is exceeded."""
        if self.coordinator.data is None:
            return None
        disk_percent = self.coordinator.data.get(DATA_DISK_PERCENT)
        if disk_percent is None:
            return None
        threshold = self._entry.options.get(
            self.entity_description.threshold_key,
            self.entity_description.default_threshold,
        )
        return disk_percent > threshold
