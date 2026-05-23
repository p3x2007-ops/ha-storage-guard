"""Automation logic for StorageGuard — threshold-based cleanup triggers."""

from __future__ import annotations

import logging
from datetime import datetime

from homeassistant.core import HomeAssistant

from .const import (
    DATA_DISK_PERCENT,
    DEFAULT_ALERT_THRESHOLD,
    DOMAIN,
    MODE_FULL_AUTO,
    MODE_MANUAL,
    MODE_SEMI_AUTO,
    SWITCH_AUTO_CLEAN_BACKUPS,
    SWITCH_AUTO_CLEAN_LOGS,
    SWITCH_AUTO_EXCLUDE_ENTITIES,
    SWITCH_AUTO_PURGE_DB,
    SWITCH_NOTIFY_ACTION,
    SWITCH_NOTIFY_CRITICAL,
    SWITCH_NOTIFY_THRESHOLD,
)

_LOGGER = logging.getLogger(__name__)


def _get_switch_state(hass: HomeAssistant, key: str) -> bool:
    """Get a StorageGuard switch state."""
    entity_id = f"switch.storage_guard_{key}"
    state = hass.states.get(entity_id)
    return state is not None and state.state == "on"


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


async def async_evaluate_thresholds(hass: HomeAssistant, data: dict) -> None:
    """Evaluate storage thresholds and trigger appropriate actions."""
    disk_percent = data.get(DATA_DISK_PERCENT)
    if disk_percent is None:
        return

    threshold = _get_number_value(hass, "alert_threshold", DEFAULT_ALERT_THRESHOLD)
    mode = _get_mode(hass)

    if disk_percent <= threshold:
        return

    _LOGGER.info(
        "StorageGuard: Threshold exceeded (%.1f%% > %.0f%%), mode=%s",
        disk_percent, threshold, mode,
    )

    # Always notify if enabled
    if _get_switch_state(hass, SWITCH_NOTIFY_THRESHOLD):
        await _async_notify(
            hass,
            f"Storage at {disk_percent:.1f}% (threshold: {threshold:.0f}%)",
            f"StorageGuard detected disk usage above your configured threshold.",
        )

    # Critical notification
    if disk_percent > 95 and _get_switch_state(hass, SWITCH_NOTIFY_CRITICAL):
        await _async_notify(
            hass,
            f"CRITICAL: Storage at {disk_percent:.1f}%",
            "Disk space is critically low! Immediate action recommended.",
            notification_id="storage_guard_critical",
        )

    if mode == MODE_MANUAL:
        return

    # Semi-auto: execute non-destructive actions
    if mode in (MODE_SEMI_AUTO, MODE_FULL_AUTO):
        if _get_switch_state(hass, SWITCH_AUTO_CLEAN_LOGS):
            await hass.services.async_call(DOMAIN, "clean_logs", blocking=True)
            if _get_switch_state(hass, SWITCH_NOTIFY_ACTION):
                await _async_notify(
                    hass, "StorageGuard: Logs cleaned", "Log files have been truncated."
                )

        if _get_switch_state(hass, SWITCH_AUTO_PURGE_DB):
            await hass.services.async_call(DOMAIN, "purge_database", blocking=True)
            if _get_switch_state(hass, SWITCH_NOTIFY_ACTION):
                await _async_notify(
                    hass, "StorageGuard: Database purged", "Recorder has been purged."
                )

    # Full-auto: also execute destructive actions
    if mode == MODE_FULL_AUTO:
        if _get_switch_state(hass, SWITCH_AUTO_CLEAN_BACKUPS):
            await hass.services.async_call(DOMAIN, "clean_backups", blocking=True)
            if _get_switch_state(hass, SWITCH_NOTIFY_ACTION):
                await _async_notify(
                    hass, "StorageGuard: Backups cleaned", "Old backups have been removed."
                )

    # Semi-auto: request confirmation for destructive actions
    if mode == MODE_SEMI_AUTO:
        if _get_switch_state(hass, SWITCH_AUTO_CLEAN_BACKUPS):
            await _async_notify(
                hass,
                "StorageGuard: Backup cleanup pending",
                "Disk space is low. Approve backup cleanup in the StorageGuard card.",
                notification_id="storage_guard_confirm_backups",
            )


async def _async_notify(
    hass: HomeAssistant,
    title: str,
    message: str,
    notification_id: str | None = None,
) -> None:
    """Send a persistent notification."""
    data = {"title": title, "message": message}
    if notification_id:
        data["notification_id"] = notification_id
    else:
        data["notification_id"] = f"storage_guard_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    await hass.services.async_call(
        "persistent_notification", "create", data, blocking=False
    )
