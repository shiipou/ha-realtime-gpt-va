"""Config flow for OpenAI Realtime integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_API_KEY,
    CONF_INSTRUCTIONS,
    CONF_LANGUAGE,
    CONF_MODEL,
    CONF_VOICE,
    DEFAULT_INSTRUCTIONS,
    DEFAULT_LANGUAGE,
    DEFAULT_MODEL,
    DEFAULT_VOICE,
    DOMAIN,
    SUPPORTED_LANGUAGES,
    SUPPORTED_MODELS,
    SUPPORTED_VOICES,
)

_LOGGER = logging.getLogger(__name__)


class OpenAIRealtimeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for OpenAI Realtime."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate API key format (basic check)
            api_key = user_input[CONF_API_KEY]
            if not api_key or not api_key.startswith("sk-"):
                errors[CONF_API_KEY] = "invalid_api_key"
            else:
                # Create the entry
                return self.async_create_entry(
                    title="OpenAI Realtime",
                    data={CONF_API_KEY: api_key},
                    options={
                        CONF_MODEL: user_input.get(CONF_MODEL, DEFAULT_MODEL),
                        CONF_VOICE: user_input.get(CONF_VOICE, DEFAULT_VOICE),
                        CONF_INSTRUCTIONS: user_input.get(
                            CONF_INSTRUCTIONS, DEFAULT_INSTRUCTIONS
                        ),
                        CONF_LANGUAGE: user_input.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),
                    },
                )

        # Show the form
        data_schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): str,
                vol.Optional(CONF_MODEL, default=DEFAULT_MODEL): vol.In(
                    SUPPORTED_MODELS
                ),
                vol.Optional(CONF_VOICE, default=DEFAULT_VOICE): vol.In(
                    SUPPORTED_VOICES
                ),
                
                vol.Optional(
                    CONF_INSTRUCTIONS, default=DEFAULT_INSTRUCTIONS
                ): str,
                vol.Optional(CONF_LANGUAGE, default=DEFAULT_LANGUAGE): vol.In(
                    SUPPORTED_LANGUAGES
                ),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> OptionsFlowHandler:
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for OpenAI Realtime."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        # Don't set self.config_entry explicitly - it's handled by parent class
        super().__init__()

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Get current options with defaults
        current_options = self.config_entry.options
        
        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_MODEL,
                    default=current_options.get(CONF_MODEL, DEFAULT_MODEL),
                ): vol.In(SUPPORTED_MODELS),
                vol.Optional(
                    CONF_VOICE,
                    default=current_options.get(CONF_VOICE, DEFAULT_VOICE),
                ): vol.In(SUPPORTED_VOICES),
                
                vol.Optional(
                    CONF_INSTRUCTIONS,
                    default=current_options.get(CONF_INSTRUCTIONS, DEFAULT_INSTRUCTIONS),
                ): str,
                vol.Optional(
                    CONF_LANGUAGE,
                    default=current_options.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),
                ): vol.In(SUPPORTED_LANGUAGES),
            }
        )

        return self.async_show_form(step_id="init", data_schema=data_schema)
