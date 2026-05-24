"""Service handlers for StorageGuard."""

from __future__ import annotations

import logging
import os

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.util import dt as dt_util

from .const import (
    DEFAULT_BACKUP_KEEP_COUNT,
    DEFAULT_PURGE_KEEP_DAYS,
    DOMAIN,
    MODE_FULL_AUTO,
    MODE_MANUAL,
    SERVICE_CLEAN_BACKUPS,
    SERVICE_CLEAN_LOGS,
    SERVICE_EXCLUDE_ENTITY,
    SERVICE_INCLUDE_ENTITY,
    SERVICE_PURGE_DATABASE,
    SERVICE_RUN_ANALYSIS,
    SERVICE_RUN_CLEANUP,
    SWITCH_AUTO_CLEAN_BACKUPS,
    SWITCH_AUTO_CLEAN_LOGS,
    SWITCH_AUTO_PURGE_DB,
)
from .coordinator import StorageGuardCoordinator
from .entity_resolver import get_mode, get_number_value, get_switch_state

_LOGGER = logging.getLogger(__name__)


def _get_coordinator(hass: HomeAssistant) -> StorageGuardCoordinator | None:
    """Get the active coordinator."""
    for entry_data in hass.data.get(DOMAIN, {}).values():
        if "coordinator" in entry_data:
            return entry_data["coordinator"]
    return None


def _now_hm() -> str:
    """Return the current local time in HH:MM (respects HA's timezone)."""
    return dt_util.now().strftime("%H:%M")


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up StorageGuard services."""

    async def handle_purge_database(call: ServiceCall) -> None:
        """Handle purge database service call."""
        coordinator = _get_coordinator(hass)
        keep_days = call.data.get(
            "keep_days",
            get_number_value(hass, "purge_keep_days", DEFAULT_PURGE_KEEP_DAYS),
        )
        keep_days = int(keep_days)

        _LOGGER.info("StorageGuard: Purging database, keeping %d days", keep_days)

        await hass.services.async_call(
            "recorder",
            "purge",
            {"keep_days": keep_days, "repack": True},
            blocking=True,
        )

        if coordinator:
            coordinator.set_last_action(f"Purged DB to {keep_days}d at {_now_hm()}")

    async def handle_clean_backups(call: ServiceCall) -> None:
        """Handle clean backups service call."""
        coordinator = _get_coordinator(hass)
        keep_count = int(
            call.data.get(
                "keep_count",
                get_number_value(hass, "backup_keep_count", DEFAULT_BACKUP_KEEP_COUNT),
            )
        )

        _LOGGER.info("StorageGuard: Cleaning backups, keeping %d", keep_count)

        try:
            from homeassistant.components.hassio import get_supervisor_client
            client = get_supervisor_client(hass)
            backups = await client.backups.list()
            if not backups:
                return

            # Drop entries without a date — we cannot safely order them.
            dated = [b for b in backups if getattr(b, "date", None)]
            sorted_backups = sorted(dated, key=lambda b: b.date)
            to_delete = (
                sorted_backups[:-keep_count]
                if len(sorted_backups) > keep_count
                else []
            )

            for backup in to_delete:
                slug = getattr(backup, "slug", None)
                if slug:
                    await client.backups.remove(slug)
                    _LOGGER.info("StorageGuard: Deleted backup %s", slug)

            if coordinator and to_delete:
                coordinator.set_last_action(
                    f"Deleted {len(to_delete)} backup(s) at {_now_hm()}"
                )
        except Exception as err:  # noqa: BLE001
            _LOGGER.error("StorageGuard: Error cleaning backups: %s", err)

    def _truncate_log_sync(log_path: str) -> float:
        """Return size before truncate (MB). Empties the log file."""
        if not os.path.exists(log_path):
            return 0.0
        size_before = os.path.getsize(log_path) / 1024 / 1024
        with open(log_path, "w"):
            pass
        return size_before

    async def handle_clean_logs(call: ServiceCall) -> None:
        """Handle clean logs service call."""
        coordinator = _get_coordinator(hass)
        log_path = hass.config.path("home-assistant.log")

        _LOGGER.info("StorageGuard: Cleaning logs at %s", log_path)

        try:
            size_before = await hass.async_add_executor_job(
                _truncate_log_sync, log_path
            )
            if coordinator:
                coordinator.set_last_action(
                    f"Cleaned logs ({size_before:.0f}MB) at {_now_hm()}"
                )
        except Exception as err:  # noqa: BLE001
            _LOGGER.error("StorageGuard: Error cleaning logs: %s", err)

    async def handle_exclude_entity(call: ServiceCall) -> None:
        """Handle exclude entity service call."""
        entity_id = call.data["entity_id"]
        _LOGGER.info("StorageGuard: Excluding entity %s from recorder", entity_id)
        # Note: Dynamic recorder exclusion requires modifying recorder config
        # This is a placeholder — full implementation needs recorder reload
        coordinator = _get_coordinator(hass)
        if coordinator:
            coordinator.set_last_action(f"Excluded {entity_id} at {_now_hm()}")

    async def handle_include_entity(call: ServiceCall) -> None:
        """Handle include entity service call."""
        entity_id = call.data["entity_id"]
        _LOGGER.info("StorageGuard: Re-including entity %s in recorder", entity_id)
        coordinator = _get_coordinator(hass)
        if coordinator:
            coordinator.set_last_action(f"Included {entity_id} at {_now_hm()}")

    async def handle_run_analysis(call: ServiceCall) -> None:
        """Handle run analysis service call."""
        coordinator = _get_coordinator(hass)
        if coordinator:
            top = await coordinator._async_get_top_entities()
            coordinator._top_entities = top
            coordinator.set_last_action(f"Analysis run at {_now_hm()}")

    async def handle_run_cleanup(call: ServiceCall) -> None:
        """Handle full cleanup cycle."""
        mode = get_mode(hass)
        force = call.data.get("force", False)

        if mode == MODE_MANUAL and not force:
            _LOGGER.info("StorageGuard: Manual mode, skipping auto cleanup")
            return

        _LOGGER.info(
            "StorageGuard: Running cleanup cycle (mode=%s, force=%s)", mode, force
        )

        # Priority order: logs → DB → backups
        if get_switch_state(hass, SWITCH_AUTO_CLEAN_LOGS):
            await handle_clean_logs(call)

        if get_switch_state(hass, SWITCH_AUTO_PURGE_DB):
            await handle_purge_database(call)

        if (mode == MODE_FULL_AUTO or force) and get_switch_state(
            hass, SWITCH_AUTO_CLEAN_BACKUPS
        ):
            await handle_clean_backups(call)

        coordinator = _get_coordinator(hass)
        if coordinator:
            coordinator.set_last_action(f"Full cleanup ({mode}) at {_now_hm()}")

    hass.services.async_register(
        DOMAIN, SERVICE_PURGE_DATABASE, handle_purge_database,
        schema=vol.Schema({vol.Optional("keep_days"): cv.positive_int}),
    )
    hass.services.async_register(
        DOMAIN, SERVICE_CLEAN_BACKUPS, handle_clean_backups,
        schema=vol.Schema({vol.Optional("keep_count"): cv.positive_int}),
    )
    hass.services.async_register(
        DOMAIN, SERVICE_CLEAN_LOGS, handle_clean_logs,
    )
    hass.services.async_register(
        DOMAIN, SERVICE_EXCLUDE_ENTITY, handle_exclude_entity,
        schema=vol.Schema({vol.Required("entity_id"): cv.entity_id}),
    )
    hass.services.async_register(
        DOMAIN, SERVICE_INCLUDE_ENTITY, handle_include_entity,
        schema=vol.Schema({vol.Required("entity_id"): cv.entity_id}),
    )
    hass.services.async_register(
        DOMAIN, SERVICE_RUN_ANALYSIS, handle_run_analysis,
    )
    hass.services.async_register(
        DOMAIN, SERVICE_RUN_CLEANUP, handle_run_cleanup,
        schema=vol.Schema({vol.Optional("force"): cv.boolean}),
    )


async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload StorageGuard services."""
    for service in (
        SERVICE_PURGE_DATABASE,
        SERVICE_CLEAN_BACKUPS,
        SERVICE_CLEAN_LOGS,
        SERVICE_EXCLUDE_ENTITY,
        SERVICE_INCLUDE_ENTITY,
        SERVICE_RUN_ANALYSIS,
        SERVICE_RUN_CLEANUP,
    ):
        hass.services.async_remove(DOMAIN, service)
