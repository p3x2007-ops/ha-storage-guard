"""Config flow for StorageGuard."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN, DEFAULT_MODE, DEFAULT_ALERT_THRESHOLD


async def _async_has_glances(hass: HomeAssistant) -> bool:
    """Check if Glances integration is providing disk sensors."""
    registry = er.async_get(hass)
    for entry in registry.entities.values():
        if "glances" in entry.entity_id and "disk" in entry.entity_id:
            return True
    states = hass.states.async_all("sensor")
    for state in states:
        if "glances" in state.entity_id and "disk" in state.entity_id:
            return True
    return False


async def _async_is_haos(hass: HomeAssistant) -> bool:
    """Check if running on HA OS or Supervised."""
    return hass.components.hassio.is_hassio(hass)


async def _async_detect_recorder_backend(hass: HomeAssistant) -> str:
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
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if not await _async_is_haos(self.hass):
            return self.async_abort(reason="not_haos")

        if not await _async_has_glances(self.hass):
            return self.async_abort(reason="no_glances")

        if user_input is not None:
            recorder_backend = await _async_detect_recorder_backend(self.hass)
            return self.async_create_entry(
                title="StorageGuard",
                data={
                    "recorder_backend": recorder_backend,
                    "mode": DEFAULT_MODE,
                    "alert_threshold": DEFAULT_ALERT_THRESHOLD,
                },
            )

        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))
