"""Config flow for StorageGuard."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, DEFAULT_MODE, DEFAULT_ALERT_THRESHOLD


def _has_glances(hass: HomeAssistant) -> bool:
    """Check if Glances integration is providing disk sensors."""
    states = hass.states.async_all("sensor")
    for state in states:
        if "glances" in state.entity_id and (
            "disk" in state.entity_id
            or "disque" in state.entity_id
            or "espace" in state.entity_id
        ):
            return True
    return False


def _find_glances_disk_entities(hass: HomeAssistant) -> dict[str, str]:
    """Find the correct Glances disk entity IDs dynamically."""
    entities = {"disk_used": "", "disk_free": "", "disk_percent": ""}
    states = hass.states.async_all("sensor")

    for state in states:
        eid = state.entity_id
        if "glances" not in eid:
            continue
        if ("utilisation_disque" in eid or "disk_use_percent" in eid) and (
            "data" in eid or "homeassistant" in eid
        ):
            entities["disk_percent"] = eid
        elif (
            ("espace_utilise" in eid or "disk_use" in eid)
            and "echange" not in eid
            and ("data" in eid or "homeassistant" in eid)
        ):
            if not entities["disk_used"]:
                entities["disk_used"] = eid
        elif ("espace_libre" in eid or "disk_free" in eid) and (
            "data" in eid or "homeassistant" in eid
        ):
            if not entities["disk_free"]:
                entities["disk_free"] = eid

    return entities


def _is_haos(hass: HomeAssistant) -> bool:
    """Check if running on HA OS or Supervised."""
    return "hassio" in hass.config.components


def _detect_recorder_backend(hass: HomeAssistant) -> str:
    """Detect recorder database backend."""
    try:
        from homeassistant.components.recorder import get_instance
        instance = get_instance(hass)
        db_url = instance.db_url
        if "mysql" in db_url or "mariadb" in db_url:
            return "mariadb"
        if "postgresql" in db_url:
            return "postgresql"
    except Exception:
        pass
    return "sqlite"


class StorageGuardConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for StorageGuard."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if not _is_haos(self.hass):
            return self.async_abort(reason="not_haos")

        if not _has_glances(self.hass):
            return self.async_abort(reason="no_glances")

        if user_input is not None:
            recorder_backend = _detect_recorder_backend(self.hass)
            glances_entities = _find_glances_disk_entities(self.hass)
            return self.async_create_entry(
                title="StorageGuard",
                data={
                    "recorder_backend": recorder_backend,
                    "mode": DEFAULT_MODE,
                    "alert_threshold": DEFAULT_ALERT_THRESHOLD,
                    "glances_disk_used": glances_entities["disk_used"],
                    "glances_disk_free": glances_entities["disk_free"],
                    "glances_disk_percent": glances_entities["disk_percent"],
                },
            )

        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))
