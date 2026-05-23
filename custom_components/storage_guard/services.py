"""Service handlers for StorageGuard."""

from __future__ import annotations

import logging
from datetime import datetime

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import (
    DEFAULT_BACKUP_KEEP_COUNT,
    DEFAULT_PURGE_KEEP_DAYS,
    DOMAIN,
    MODE_FULL_AUTO,
    MODE_MANUAL,
    MODE_SEMI_AUTO,
    SERVICE_CLEAN_BACKUPS,
    SERVICE_CLEAN_LOGS,
    SERVICE_EXCLUDE_ENTITY,
    SERVICE_INCLUDE_ENTITY,
    SERVICE_PURGE_DATABASE,
    SERVICE_RUN_ANALYSIS,
    SERVICE_RUN_CLEANUP,
    SWITCH_AUTO_CLEAN_BACKUPS,
    SWITCH_AUTO_CLEAN_LOGS,
    SWITCH_AUTO_EXCLUDE_ENTITIES,
    SWITCH_AUTO_PURGE_DB,
)
from .coordinator import StorageGuardCoordinator

_LOGGER = logging.getLogger(__name__)


def _get_coordinator(hass: HomeAssistant) -> StorageGuardCoordinator | None:
    """Get the active coordinator."""
    for entry_data in hass.data.get(DOMAIN, {}).values():
        if "coordinator" in entry_data:
            return entry_data["coordinator"]
    return None


def _get_switch_state(hass: HomeAssistant, key: str) -> bool:
    """Get a StorageGuard switch state."""
    entity_id = f"switch.storage_guard_{key}"
    state = hass.states.get(entity_id)
    if state is None:
        return False
    return state.state == "on"


def _get_number_value(hass: HomeAssistant, key: str, default: float) -> float:
    """Get a StorageGuard number value."""
    entity_id = f"number.storage_guard_{key}"
    state = hass.states.get(entity_id)
    if state is None:
        return default
    try:
        return float(state.state)
    except (ValueError, TypeError):
        return default


def _get_mode(hass: HomeAssistant) -> str:
    """Get current operation mode."""
    state = hass.states.get("select.storage_guard_mode")
    if state is None:
        return MODE_MANUAL
    return state.state


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up StorageGuard services."""

    async def handle_purge_database(call: ServiceCall) -> None:
        """Handle purge database service call."""
        coordinator = _get_coordinator(hass)
        keep_days = call.data.get(
            "keep_days",
            _get_number_value(hass, "purge_keep_days", DEFAULT_PURGE_KEEP_DAYS),
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
            coordinator.set_last_action(
                f"Purged DB to {keep_days}d at {datetime.now().strftime('%H:%M')}"
            )

    async def handle_clean_backups(call: ServiceCall) -> None:
        """Handle clean backups service call."""
        coordinator = _get_coordinator(hass)
        keep_count = int(
            call.data.get(
                "keep_count",
                _get_number_value(hass, "backup_keep_count", DEFAULT_BACKUP_KEEP_COUNT),
            )
        )

        _LOGGER.info("StorageGuard: Cleaning backups, keeping %d", keep_count)

        try:
            from homeassistant.components.hassio import get_supervisor_client
            client = get_supervisor_client(hass)
            backups = await client.backups.list()
            if backups:
                sorted_backups = sorted(backups, key=lambda b: getattr(b, "date", ""))
                to_delete = sorted_backups[:-keep_count] if len(sorted_backups) > keep_count else []

                for backup in to_delete:
                    slug = getattr(backup, "slug", None)
                    if slug:
                        await client.backups.remove(slug)
                        _LOGGER.info("StorageGuard: Deleted backup %s", slug)

                if coordinator and to_delete:
                    coordinator.set_last_action(
                        f"Deleted {len(to_delete)} backup(s) at {datetime.now().strftime('%H:%M')}"
                    )
        except Exception as err:
            _LOGGER.error("StorageGuard: Error cleaning backups: %s", err)

    async def handle_clean_logs(call: ServiceCall) -> None:
        """Handle clean logs service call."""
        coordinator = _get_coordinator(hass)
        log_path = hass.config.path("home-assistant.log")

        _LOGGER.info("StorageGuard: Cleaning logs at %s", log_path)

        try:
            import os
            if os.path.exists(log_path):
                size_before = os.path.getsize(log_path) / 1024 / 1024
                with open(log_path, "w") as f:
                    f.write("")
                if coordinator:
                    coordinator.set_last_action(
                        f"Cleaned logs ({size_before:.0f}MB) at {datetime.now().strftime('%H:%M')}"
                    )
        except Exception as err:
            _LOGGER.error("StorageGuard: Error cleaning logs: %s", err)

    async def handle_exclude_entity(call: ServiceCall) -> None:
        """Handle exclude entity service call."""
        entity_id = call.data["entity_id"]
        _LOGGER.info("StorageGuard: Excluding entity %s from recorder", entity_id)
        # Note: Dynamic recorder exclusion requires modifying recorder config
        # This is a placeholder — full implementation needs recorder reload
        coordinator = _get_coordinator(hass)
        if coordinator:
            coordinator.set_last_action(
                f"Excluded {entity_id} at {datetime.now().strftime('%H:%M')}"
            )

    async def handle_include_entity(call: ServiceCall) -> None:
        """Handle include entity service call."""
        entity_id = call.data["entity_id"]
        _LOGGER.info("StorageGuard: Re-including entity %s in recorder", entity_id)
        coordinator = _get_coordinator(hass)
        if coordinator:
            coordinator.set_last_action(
                f"Included {entity_id} at {datetime.now().strftime('%H:%M')}"
            )

    async def handle_run_analysis(call: ServiceCall) -> None:
        """Handle run analysis service call."""
        coordinator = _get_coordinator(hass)
        if coordinator:
            coordinator._top_entities = await coordinator._async_get_top_entities()
            coordinator.set_last_action(
                f"Analysis run at {datetime.now().strftime('%H:%M')}"
            )

    async def handle_run_cleanup(call: ServiceCall) -> None:
        """Handle full cleanup cycle."""
        mode = _get_mode(hass)
        force = call.data.get("force", False)

        if mode == MODE_MANUAL and not force:
            _LOGGER.info("StorageGuard: Manual mode, skipping auto cleanup")
            return

        _LOGGER.info("StorageGuard: Running cleanup cycle (mode=%s, force=%s)", mode, force)

        # Priority order: logs → DB → backups → entities
        if _get_switch_state(hass, SWITCH_AUTO_CLEAN_LOGS):
            await handle_clean_logs(call)

        if _get_switch_state(hass, SWITCH_AUTO_PURGE_DB):
            await handle_purge_database(call)

        if mode == MODE_FULL_AUTO or force:
            if _get_switch_state(hass, SWITCH_AUTO_CLEAN_BACKUPS):
                await handle_clean_backups(call)

        coordinator = _get_coordinator(hass)
        if coordinator:
            coordinator.set_last_action(
                f"Full cleanup ({mode}) at {datetime.now().strftime('%H:%M')}"
            )

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
