"""The OpenAI Realtime Voice Assistant integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.discovery import async_load_platform

from .const import DOMAIN
from .realtime_client import OpenAIRealtimeClient

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up OpenAI Realtime Voice Assistant from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    try:
        client = OpenAIRealtimeClient(hass, entry)
        hass.data[DOMAIN][entry.entry_id] = {
            "client": client,
        }
        
        # Load TTS and STT platforms with discovery info
        hass.async_create_task(
            async_load_platform(
                hass,
                Platform.TTS,
                DOMAIN,
                {"entry_id": entry.entry_id},
                hass.data[Platform.TTS],
            )
        )
        
        hass.async_create_task(
            async_load_platform(
                hass,
                Platform.STT,
                DOMAIN,
                {"entry_id": entry.entry_id},
                hass.data[Platform.STT],
            )
        )
        
        return True
        
    except Exception as err:
        _LOGGER.error("Error setting up OpenAI Realtime: %s", err)
        raise ConfigEntryNotReady from err


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    data = hass.data[DOMAIN].pop(entry.entry_id)
    client: OpenAIRealtimeClient = data["client"]
    await client.disconnect()
    
    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
