"""Sensor platform for StorageGuard."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfInformation
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DATA_BACKUP_COUNT,
    DATA_BACKUP_SIZE,
    DATA_DB_SIZE,
    DATA_DISK_FREE,
    DATA_DISK_PERCENT,
    DATA_DISK_USED,
    DATA_LAST_ACTION,
    DATA_LOG_SIZE,
    DATA_SPACE_RECLAIMABLE,
    DOMAIN,
)
from .coordinator import StorageGuardCoordinator


@dataclass(frozen=True, kw_only=True)
class StorageGuardSensorDescription(SensorEntityDescription):
    """Describe a StorageGuard sensor."""

    data_key: str
    round_digits: int = 1


SENSOR_DESCRIPTIONS: tuple[StorageGuardSensorDescription, ...] = (
    StorageGuardSensorDescription(
        key="disk_used_percent",
        translation_key="disk_used_percent",
        data_key=DATA_DISK_PERCENT,
        native_unit_of_measurement=PERCENTAGE,
        device_class=None,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    StorageGuardSensorDescription(
        key="disk_used",
        translation_key="disk_used",
        data_key=DATA_DISK_USED,
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StorageGuardSensorDescription(
        key="disk_free",
        translation_key="disk_free",
        data_key=DATA_DISK_FREE,
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StorageGuardSensorDescription(
        key="database_size",
        translation_key="database_size",
        data_key=DATA_DB_SIZE,
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StorageGuardSensorDescription(
        key="backup_count",
        translation_key="backup_count",
        data_key=DATA_BACKUP_COUNT,
        native_unit_of_measurement="backups",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StorageGuardSensorDescription(
        key="backup_size",
        translation_key="backup_size",
        data_key=DATA_BACKUP_SIZE,
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StorageGuardSensorDescription(
        key="log_size",
        translation_key="log_size",
        data_key=DATA_LOG_SIZE,
        native_unit_of_measurement=UnitOfInformation.MEGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StorageGuardSensorDescription(
        key="last_action",
        translation_key="last_action",
        data_key=DATA_LAST_ACTION,
    ),
    StorageGuardSensorDescription(
        key="space_reclaimable",
        translation_key="space_reclaimable",
        data_key=DATA_SPACE_RECLAIMABLE,
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up StorageGuard sensors."""
    coordinator: StorageGuardCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    async_add_entities(
        StorageGuardSensor(coordinator, description)
        for description in SENSOR_DESCRIPTIONS
    )


class StorageGuardSensor(
    CoordinatorEntity[StorageGuardCoordinator], SensorEntity
):
    """Representation of a StorageGuard sensor."""

    entity_description: StorageGuardSensorDescription

    def __init__(
        self,
        coordinator: StorageGuardCoordinator,
        description: StorageGuardSensorDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{DOMAIN}_{description.key}"
        self._attr_name = f"StorageGuard {description.key.replace('_', ' ').title()}"
        self.entity_id = f"sensor.storage_guard_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, DOMAIN)},
            "name": "StorageGuard",
            "manufacturer": "StorageGuard",
            "model": "Storage Manager",
            "sw_version": "1.0.1",
        }

    @property
    def native_value(self) -> Any:
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None
        value = self.coordinator.data.get(self.entity_description.data_key)
        if value is None:
            return None
        if isinstance(value, float):
            return round(value, self.entity_description.round_digits)
        return value
