"""DataUpdateCoordinator for StorageGuard."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    DATA_BACKUP_COUNT,
    DATA_BACKUP_SIZE,
    DATA_DB_SIZE,
    DATA_DISK_FREE,
    DATA_DISK_PERCENT,
    DATA_DISK_TOTAL,
    DATA_DISK_USED,
    DATA_LAST_ACTION,
    DATA_LOG_SIZE,
    DATA_SPACE_RECLAIMABLE,
    DATA_TOP_ENTITIES,
    UPDATE_INTERVAL_DISK,
)

_LOGGER = logging.getLogger(__name__)


class StorageGuardCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator that polls all storage data sources."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL_DISK),
        )
        self.config_entry = entry
        self._backup_data: dict[str, Any] = {}
        self._db_data: dict[str, Any] = {}
        self._top_entities: list[dict[str, Any]] = []
        self._last_action: str = "None"
        self._update_count: int = 0

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from all sources."""
        data: dict[str, Any] = {}

        data.update(await self._async_get_disk_data())

        self._update_count += 1
        if self._update_count % 5 == 0:
            self._db_data = await self._async_get_db_data()
            data.update(self._db_data)
        else:
            data.update(self._db_data)

        if self._update_count % 10 == 0:
            self._backup_data = await self._async_get_backup_data()
            data.update(self._backup_data)
        else:
            data.update(self._backup_data)

        if self._update_count % 5 == 0:
            log_data = await self._async_get_log_data()
            data.update(log_data)

        if self._update_count % 60 == 0:
            self._top_entities = await self._async_get_top_entities()

        data[DATA_TOP_ENTITIES] = self._top_entities
        data[DATA_LAST_ACTION] = self._last_action
        data[DATA_SPACE_RECLAIMABLE] = self._calculate_reclaimable(data)

        # Evaluate thresholds for automation
        from .automation import async_evaluate_thresholds
        await async_evaluate_thresholds(self.hass, data)

        return data

    async def _async_get_disk_data(self) -> dict[str, Any]:
        """Get disk usage from Glances sensors."""
        data = {}
        try:
            entry_data = self.config_entry.data
            disk_used_id = entry_data.get("glances_disk_used", "")
            disk_free_id = entry_data.get("glances_disk_free", "")
            disk_pct_id = entry_data.get("glances_disk_percent", "")

            if disk_used_id:
                disk_use = self.hass.states.get(disk_used_id)
                if disk_use and disk_use.state not in ("unknown", "unavailable"):
                    data[DATA_DISK_USED] = float(disk_use.state)

            if disk_free_id:
                disk_free = self.hass.states.get(disk_free_id)
                if disk_free and disk_free.state not in ("unknown", "unavailable"):
                    data[DATA_DISK_FREE] = float(disk_free.state)

            if disk_pct_id:
                disk_pct = self.hass.states.get(disk_pct_id)
                if disk_pct and disk_pct.state not in ("unknown", "unavailable"):
                    data[DATA_DISK_PERCENT] = float(disk_pct.state)

            used = data.get(DATA_DISK_USED, 0)
            free = data.get(DATA_DISK_FREE, 0)
            data[DATA_DISK_TOTAL] = round(used + free, 2) if used and free else 0

        except (ValueError, TypeError) as err:
            _LOGGER.debug("Error reading Glances sensors: %s", err)

        return data

    async def _async_get_db_data(self) -> dict[str, Any]:
        """Get database size from recorder."""
        data = {DATA_DB_SIZE: 0}
        try:
            try:
                from homeassistant.components.recorder import get_instance
            except ImportError:
                from homeassistant.helpers.recorder import get_instance
            instance = get_instance(self.hass)
            stat = await instance.async_add_executor_job(
                self._get_db_size_sync, instance
            )
            data[DATA_DB_SIZE] = stat
        except Exception as err:
            _LOGGER.debug("Error getting DB size: %s", err)
        return data

    def _get_db_size_sync(self, instance: Any) -> float:
        """Get database file size (sync)."""
        try:
            db_url = instance.db_url
            if "mysql" in db_url or "mariadb" in db_url:
                from sqlalchemy import text
                with instance.get_session() as session:
                    result = session.execute(text(
                        "SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024 / 1024, 2) "
                        "FROM information_schema.tables WHERE table_schema = DATABASE()"
                    ))
                    row = result.fetchone()
                    if row and row[0]:
                        return float(row[0])
            else:
                import os
                db_path = db_url.replace("sqlite:///", "")
                if os.path.exists(db_path):
                    return round(os.path.getsize(db_path) / 1024 / 1024 / 1024, 2)
        except Exception as err:
            _LOGGER.debug("Error querying DB size: %s", err)
        return 0

    async def _async_get_backup_data(self) -> dict[str, Any]:
        """Get backup information from Supervisor API."""
        data = {DATA_BACKUP_COUNT: 0, DATA_BACKUP_SIZE: 0}
        try:
            from homeassistant.components.hassio import get_supervisor_client
            client = get_supervisor_client(self.hass)
            backups = await client.backups.list()
            if backups:
                data[DATA_BACKUP_COUNT] = len(backups)
                total_size = sum(
                    getattr(b, "size", 0) or 0 for b in backups
                )
                data[DATA_BACKUP_SIZE] = round(total_size, 2)
        except Exception as err:
            _LOGGER.debug("Error getting backup data: %s", err)
        return data

    async def _async_get_log_data(self) -> dict[str, float]:
        """Get log file size."""
        data = {DATA_LOG_SIZE: 0}
        try:
            import os
            log_path = self.hass.config.path("home-assistant.log")
            if os.path.exists(log_path):
                size_mb = os.path.getsize(log_path) / 1024 / 1024
                data[DATA_LOG_SIZE] = round(size_mb, 1)
        except Exception as err:
            _LOGGER.debug("Error getting log size: %s", err)
        return data

    async def _async_get_top_entities(self) -> list[dict[str, Any]]:
        """Analyze top storage-consuming entities."""
        entities: list[dict[str, Any]] = []
        try:
            try:
                from homeassistant.components.recorder import get_instance
            except ImportError:
                from homeassistant.helpers.recorder import get_instance
            instance = get_instance(self.hass)
            entities = await instance.async_add_executor_job(
                self._get_top_entities_sync, instance
            )
        except Exception as err:
            _LOGGER.debug("Error analyzing top entities: %s", err)
        return entities

    def _get_top_entities_sync(self, instance: Any) -> list[dict[str, Any]]:
        """Query top entities by state change frequency (sync)."""
        entities: list[dict[str, Any]] = []
        try:
            db_url = instance.db_url
            if "mysql" in db_url or "mariadb" in db_url:
                from sqlalchemy import text
                with instance.get_session() as session:
                    result = session.execute(text(
                        "SELECT sm.entity_id, COUNT(*) as changes, "
                        "ROUND(COUNT(*) * 0.0001, 2) as est_mb_per_day "
                        "FROM states s "
                        "JOIN states_meta sm ON s.metadata_id = sm.metadata_id "
                        "WHERE s.last_updated_ts > UNIX_TIMESTAMP(NOW() - INTERVAL 1 DAY) "
                        "GROUP BY sm.entity_id "
                        "ORDER BY changes DESC "
                        "LIMIT 10"
                    ))
                    for row in result:
                        entities.append({
                            "entity_id": row[0],
                            "changes_per_day": row[1],
                            "est_size_mb": row[2],
                        })
        except Exception as err:
            _LOGGER.debug("Error querying top entities: %s", err)
        return entities

    def _calculate_reclaimable(self, data: dict[str, Any]) -> float:
        """Estimate total reclaimable space in GB."""
        reclaimable = 0.0
        db_size = data.get(DATA_DB_SIZE, 0)
        if db_size > 0:
            reclaimable += db_size * 0.5

        backup_size = data.get(DATA_BACKUP_SIZE, 0)
        backup_count = data.get(DATA_BACKUP_COUNT, 0)
        keep_count = 3
        if backup_count > keep_count and backup_size > 0:
            avg_backup = backup_size / backup_count
            reclaimable += avg_backup * (backup_count - keep_count)

        log_size = data.get(DATA_LOG_SIZE, 0)
        reclaimable += log_size / 1024

        return round(reclaimable, 2)

    def set_last_action(self, action: str) -> None:
        """Record the last action performed."""
        self._last_action = action
        self.async_set_updated_data(self.data)
