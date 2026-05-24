"""Automation logic for StorageGuard — threshold-based cleanup triggers."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from .const import (
    AUTO_COOLDOWN_SECONDS,
    DATA_DISK_PERCENT,
    DEFAULT_ALERT_THRESHOLD,
    DEFAULT_CRITICAL_THRESHOLD,
    DOMAIN,
    MODE_FULL_AUTO,
    MODE_MANUAL,
    MODE_SEMI_AUTO,
    SWITCH_AUTO_CLEAN_BACKUPS,
    SWITCH_AUTO_CLEAN_LOGS,
    SWITCH_AUTO_PURGE_DB,
    SWITCH_NOTIFY_ACTION,
    SWITCH_NOTIFY_CRITICAL,
    SWITCH_NOTIFY_THRESHOLD,
)
from .entity_resolver import get_mode, get_number_value, get_switch_state

_LOGGER = logging.getLogger(__name__)


async def async_evaluate_thresholds(hass: HomeAssistant, data: dict) -> None:
    """Evaluate storage thresholds and trigger appropriate actions."""
    disk_percent = data.get(DATA_DISK_PERCENT)
    if disk_percent is None:
        return

    threshold = get_number_value(hass, "alert_threshold", DEFAULT_ALERT_THRESHOLD)
    mode = get_mode(hass)

    coordinator = _get_coordinator(hass)

    if disk_percent <= threshold:
        # Disarm cooldown as soon as disk drops back under threshold so the
        # next breach triggers cleanup immediately.
        if coordinator is not None:
            coordinator.reset_auto_cooldown()
        return

    _LOGGER.debug(
        "StorageGuard: Threshold exceeded (%.1f%% > %.0f%%), mode=%s",
        disk_percent, threshold, mode,
    )

    if get_switch_state(hass, SWITCH_NOTIFY_THRESHOLD):
        await _async_notify(
            hass,
            f"Storage at {disk_percent:.1f}% (threshold: {threshold:.0f}%)",
            "StorageGuard detected disk usage above your configured threshold.",
            notification_id="storage_guard_threshold",
        )

    critical_threshold = get_number_value(
        hass, "critical_threshold", DEFAULT_CRITICAL_THRESHOLD
    )
    if disk_percent > critical_threshold and get_switch_state(
        hass, SWITCH_NOTIFY_CRITICAL
    ):
        await _async_notify(
            hass,
            f"CRITICAL: Storage at {disk_percent:.1f}%",
            "Disk space is critically low! Immediate action recommended.",
            notification_id="storage_guard_critical",
        )

    if mode == MODE_MANUAL:
        return

    if coordinator is not None and not coordinator.can_run_auto_cleanup(
        AUTO_COOLDOWN_SECONDS
    ):
        _LOGGER.debug(
            "StorageGuard: skipping auto cleanup (cooldown active)"
        )
        return

    triggered = False

    if mode in (MODE_SEMI_AUTO, MODE_FULL_AUTO):
        if get_switch_state(hass, SWITCH_AUTO_CLEAN_LOGS):
            await hass.services.async_call(DOMAIN, "clean_logs", blocking=True)
            triggered = True
            if get_switch_state(hass, SWITCH_NOTIFY_ACTION):
                await _async_notify(
                    hass,
                    "StorageGuard: Logs cleaned",
                    "Log files have been truncated.",
                )

        if get_switch_state(hass, SWITCH_AUTO_PURGE_DB):
            await hass.services.async_call(DOMAIN, "purge_database", blocking=True)
            triggered = True
            if get_switch_state(hass, SWITCH_NOTIFY_ACTION):
                await _async_notify(
                    hass,
                    "StorageGuard: Database purged",
                    "Recorder has been purged.",
                )

    if mode == MODE_FULL_AUTO and get_switch_state(
        hass, SWITCH_AUTO_CLEAN_BACKUPS
    ):
        await hass.services.async_call(DOMAIN, "clean_backups", blocking=True)
        triggered = True
        if get_switch_state(hass, SWITCH_NOTIFY_ACTION):
            await _async_notify(
                hass,
                "StorageGuard: Backups cleaned",
                "Old backups have been removed.",
            )

    if mode == MODE_SEMI_AUTO and get_switch_state(
        hass, SWITCH_AUTO_CLEAN_BACKUPS
    ):
        await _async_notify(
            hass,
            "StorageGuard: Backup cleanup pending",
            "Disk space is low. Approve backup cleanup in the StorageGuard card.",
            notification_id="storage_guard_confirm_backups",
        )

    if triggered and coordinator is not None:
        coordinator.mark_auto_cleanup_run()


def _get_coordinator(hass: HomeAssistant):
    """Return the active StorageGuard coordinator, if any."""
    for entry_data in hass.data.get(DOMAIN, {}).values():
        if "coordinator" in entry_data:
            return entry_data["coordinator"]
    return None


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
        data["notification_id"] = (
            f"storage_guard_{dt_util.now().strftime('%Y%m%d%H%M%S')}"
        )

    await hass.services.async_call(
        "persistent_notification", "create", data, blocking=False
    )
