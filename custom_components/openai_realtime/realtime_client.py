"""OpenAI Realtime API WebSocket client."""
from __future__ import annotations

import asyncio
import base64
import json
import logging
from typing import Any, Callable

import websockets
from websockets.client import WebSocketClientProtocol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant

from .const import (
    AUDIO_FORMAT,
    AUDIO_SAMPLE_RATE,
    CONF_INSTRUCTIONS,
    CONF_MODEL,
    CONF_MODALITIES,
    CONF_VOICE,
    DEFAULT_INSTRUCTIONS,
    DEFAULT_MODALITIES,
    DEFAULT_MODEL,
    DEFAULT_VOICE,
    EVENT_TYPE_CONVERSATION_ITEM_CREATE,
    EVENT_TYPE_INPUT_AUDIO_BUFFER_APPEND,
    EVENT_TYPE_INPUT_AUDIO_BUFFER_CLEAR,
    EVENT_TYPE_INPUT_AUDIO_BUFFER_COMMIT,
    EVENT_TYPE_RESPONSE_AUDIO_DELTA,
    EVENT_TYPE_RESPONSE_AUDIO_TRANSCRIPT_DELTA,
    EVENT_TYPE_RESPONSE_CANCEL,
    EVENT_TYPE_RESPONSE_CREATE,
    EVENT_TYPE_RESPONSE_DONE,
    EVENT_TYPE_SESSION_UPDATE,
    EVENT_TYPE_INPUT_AUDIO_BUFFER_SPEECH_STARTED,
    EVENT_TYPE_INPUT_AUDIO_BUFFER_SPEECH_STOPPED,
    EVENT_RESPONSE_CREATED,
    OPENAI_REALTIME_URL,
    VAD_PREFIX_PADDING_MS,
    VAD_SILENCE_DURATION_MS,
    VAD_THRESHOLD,
)

_LOGGER = logging.getLogger(__name__)


class OpenAIRealtimeClient:
    """Client for OpenAI Realtime API."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the client."""
        self.hass = hass
        self.config_entry = config_entry
        self._ws: WebSocketClientProtocol | None = None
        self._connected = False
        self._receive_task: asyncio.Task | None = None
        self._audio_callback: Callable[[bytes], None] | None = None
        self._transcript_callback: Callable[[str], None] | None = None
        self._response_done_callback: Callable[[], None] | None = None
        self._speech_started_callback: Callable[[], None] | None = None
        self._speech_stopped_callback: Callable[[], None] | None = None
        
        # Audio buffer for incoming audio
        self._audio_buffer: list[bytes] = []
        self._is_speaking = False
        self._has_active_response = False

    @property
    def connected(self) -> bool:
        """Return if connected."""
        return self._connected and self._ws is not None

    async def connect(self) -> None:
        """Connect to OpenAI Realtime API."""
        if self._connected:
            return

        api_key = self.config_entry.data[CONF_API_KEY]
        options = self.config_entry.options
        model = options.get(CONF_MODEL, DEFAULT_MODEL)

        url = f"{OPENAI_REALTIME_URL}?model={model}"
        headers = {
            "Authorization": f"Bearer {api_key}",
        }

        try:
            _LOGGER.debug("Connecting to OpenAI Realtime API: %s", url)
            self._ws = await websockets.connect(url, additional_headers=headers)
            self._connected = True
            _LOGGER.info("Connected to OpenAI Realtime API")

            # Start receiving messages
            self._receive_task = asyncio.create_task(self._receive_messages())

            # Configure session
            await self._configure_session()

        except Exception as err:
            _LOGGER.error("Failed to connect to OpenAI Realtime API: %s", err)
            self._connected = False
            raise

    async def disconnect(self) -> None:
        """Disconnect from OpenAI Realtime API."""
        if not self._connected:
            return

        self._connected = False

        if self._receive_task:
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass
            self._receive_task = None

        if self._ws:
            await self._ws.close()
            self._ws = None

        _LOGGER.info("Disconnected from OpenAI Realtime API")

    async def _configure_session(self) -> None:
        """Configure the session with desired settings."""
        options = self.config_entry.options
        
        session_config = {
            "type": EVENT_TYPE_SESSION_UPDATE,
            "session": {
                "type": "realtime",
                "model": options.get(CONF_MODEL, DEFAULT_MODEL),
                "output_modalities": ["audio"],
                "audio": {
                    "input": {
                        "format": {"type": "audio/pcm", "rate": AUDIO_SAMPLE_RATE},
                        "turn_detection": {"type": "semantic_vad"}
                    },
                    "output": {
                        "format": {"type": "audio/pcm", "rate": AUDIO_SAMPLE_RATE},
                        "voice": options.get(CONF_VOICE, DEFAULT_VOICE)
                    }
                },
                "instructions": options.get(CONF_INSTRUCTIONS, DEFAULT_INSTRUCTIONS),
            }
        }

        await self._send_event(session_config)
        _LOGGER.debug("Session configured")

    async def _send_event(self, event: dict[str, Any]) -> None:
        """Send an event to the WebSocket."""
        if not self._ws:
            _LOGGER.error("WebSocket not connected")
            return

        try:
            event_json = json.dumps(event)
            await self._ws.send(event_json)
            _LOGGER.debug("Sent event: %s", event.get("type"))
            if event.get("type") == EVENT_TYPE_SESSION_UPDATE:
                _LOGGER.debug("Session config: %s", event_json)
        except Exception as err:
            _LOGGER.error("Error sending event: %s", err)

    async def _receive_messages(self) -> None:
        """Receive and process messages from WebSocket."""
        if not self._ws:
            return

        try:
            async for message in self._ws:
                await self._handle_message(message)
        except asyncio.CancelledError:
            _LOGGER.debug("Receive task cancelled")
        except Exception as err:
            _LOGGER.error("Error receiving messages: %s", err)
            self._connected = False

    async def _handle_message(self, message: str) -> None:
        """Handle incoming WebSocket message."""
        try:
            data = json.loads(message)
            event_type = data.get("type")
            
            _LOGGER.debug("Received event: %s - %s", event_type, data.keys())

            if event_type == EVENT_RESPONSE_CREATED:
                # Track that we have an active response
                self._has_active_response = True
                _LOGGER.info("Response created, tracking active response")

            elif event_type == EVENT_TYPE_RESPONSE_AUDIO_DELTA:
                # Audio chunk received from AI
                _LOGGER.debug("Audio delta event: %s", data.keys())
                audio_b64 = data.get("delta")
                if audio_b64:
                    _LOGGER.debug("Audio delta size: %d bytes (base64)", len(audio_b64))
                    if self._audio_callback:
                        audio_bytes = base64.b64decode(audio_b64)
                        _LOGGER.debug("Decoded audio size: %d bytes", len(audio_bytes))
                        self._audio_callback(audio_bytes)
                else:
                    _LOGGER.warning("No audio delta in event: %s", data)

            elif event_type == EVENT_TYPE_RESPONSE_AUDIO_TRANSCRIPT_DELTA:
                # Transcript chunk received
                transcript = data.get("delta", "")
                if transcript and self._transcript_callback:
                    self._transcript_callback(transcript)

            elif event_type == EVENT_TYPE_RESPONSE_DONE:
                # Response completed
                self._has_active_response = False
                _LOGGER.debug("Response done, no longer active")
                if self._response_done_callback:
                    self._response_done_callback()

            elif event_type == EVENT_TYPE_INPUT_AUDIO_BUFFER_SPEECH_STARTED:
                # User started speaking - interrupt AI only if there's an active response
                _LOGGER.debug("User started speaking")
                self._is_speaking = True
                if self._speech_started_callback:
                    self._speech_started_callback()
                if self._has_active_response:
                    _LOGGER.debug("Cancelling active response")
                    await self.cancel_response()

            elif event_type == EVENT_TYPE_INPUT_AUDIO_BUFFER_SPEECH_STOPPED:
                # User stopped speaking
                _LOGGER.debug("User stopped speaking")
                self._is_speaking = False
                if self._speech_stopped_callback:
                    self._speech_stopped_callback()

            elif event_type == "error":
                error = data.get("error", {})
                error_code = error.get("code")
                
                # Don't log certain expected errors as errors
                if error_code in ("response_cancel_not_active", "conversation_already_has_active_response"):
                    _LOGGER.debug("OpenAI API notice: %s", error.get("message"))
                else:
                    _LOGGER.error("OpenAI API error: %s", error)

        except json.JSONDecodeError as err:
            _LOGGER.error("Failed to decode message: %s", err)
        except Exception as err:
            _LOGGER.error("Error handling message: %s", err)

    async def send_audio(self, audio_data: bytes) -> None:
        """Send audio data to OpenAI."""
        if not self._connected or not self._ws:
            _LOGGER.warning("Cannot send audio: not connected")
            return

        # Encode audio as base64
        audio_b64 = base64.b64encode(audio_data).decode("utf-8")

        event = {
            "type": EVENT_TYPE_INPUT_AUDIO_BUFFER_APPEND,
            "audio": audio_b64,
        }

        await self._send_event(event)

    async def commit_audio(self) -> None:
        """Commit audio buffer and request response."""
        if not self._connected:
            return

        # Commit the audio buffer
        await self._send_event({"type": EVENT_TYPE_INPUT_AUDIO_BUFFER_COMMIT})
        
        # Request a response only if we don't already have one active
        # Voice and audio format are already configured in the session
        if not self._has_active_response:
            await self._send_event({"type": EVENT_TYPE_RESPONSE_CREATE})
            self._has_active_response = True

    async def cancel_response(self) -> None:
        """Cancel the current AI response (for interruption)."""
        if not self._connected:
            return

        # Only cancel if we actually have an active response
        if self._has_active_response:
            await self._send_event({"type": EVENT_TYPE_RESPONSE_CANCEL})
            self._has_active_response = False
        
        # Clear input audio buffer
        await self._send_event({"type": EVENT_TYPE_INPUT_AUDIO_BUFFER_CLEAR})

    async def send_text(self, text: str) -> None:
        """Send text message to the conversation."""
        if not self._connected:
            _LOGGER.warning("Cannot send text: not connected")
            return

        event = {
            "type": EVENT_TYPE_CONVERSATION_ITEM_CREATE,
            "item": {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": text}],
            }, 
        }

        await self._send_event(event)
        
        # Request a response only if we don't already have one active
        # Voice and audio format are already configured in the session
        if not self._has_active_response:
            await self._send_event({"type": EVENT_TYPE_RESPONSE_CREATE})
            self._has_active_response = True
            self._has_active_response = True

    def set_audio_callback(self, callback: Callable[[bytes], None]) -> None:
        """Set callback for received audio."""
        self._audio_callback = callback

    def set_transcript_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for received transcript."""
        self._transcript_callback = callback

    def set_response_done_callback(self, callback: Callable[[], None]) -> None:
        """Set callback for response completion."""
        self._response_done_callback = callback

    def set_speech_started_callback(self, callback: Callable[[], None]) -> None:
        """Set callback for when user starts speaking."""
        self._speech_started_callback = callback

    def set_speech_stopped_callback(self, callback: Callable[[], None]) -> None:
        """Set callback for when user stops speaking."""
        self._speech_stopped_callback = callback
