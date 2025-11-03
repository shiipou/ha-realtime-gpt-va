"""Constants for the OpenAI Realtime integration."""

DOMAIN = "openai_realtime"

# Configuration keys
CONF_API_KEY = "api_key"
CONF_MODEL = "model"
CONF_VOICE = "voice"
CONF_INSTRUCTIONS = "instructions"
CONF_LANGUAGE = "language"
CONF_MODALITIES = "modalities"

# Default values
DEFAULT_MODEL = "gpt-realtime"
DEFAULT_VOICE = "alloy"
DEFAULT_INSTRUCTIONS = (
    "You are a helpful voice assistant integrated with Home Assistant. "
    "You can help users control their smart home devices and answer questions. "
    "Be concise and natural in your responses."
)
DEFAULT_LANGUAGE = "en"
DEFAULT_MODALITIES = ["text", "audio"]

# Supported options
SUPPORTED_MODELS = [
    "gpt-4o-realtime-preview-2024-12-17",
    "gpt-4o-realtime-preview",
    "gpt-realtime",
]

SUPPORTED_VOICES = [
    "alloy",
    "echo",
    "shimmer",
    "ash",
    "ballad",
    "coral",
    "sage",
    "verse",
]

SUPPORTED_LANGUAGES = {
    "en": "English",
    "fr": "Français",
    "es": "Español",
    "de": "Deutsch",
    "it": "Italiano",
    "pt": "Português",
    "nl": "Nederlands",
    "pl": "Polski",
    "ru": "Русский",
    "ja": "日本語",
    "ko": "한국어",
    "zh": "中文",
    "ar": "العربية",
    "hi": "हिन्दी",
}

SUPPORTED_MODALITIES = ["text", "audio"]

# API Configuration
API_URL = "wss://api.openai.com/v1/realtime"
OPENAI_REALTIME_URL = "wss://api.openai.com/v1/realtime"  # Alias for compatibility
API_MODEL_PARAM = "model"

# Audio Configuration
AUDIO_FORMAT = "pcm16"
AUDIO_SAMPLE_RATE = 24000
AUDIO_CHANNELS = 1

# Session Configuration
SESSION_TURN_DETECTION_TYPE = "server_vad"
SESSION_TURN_DETECTION_THRESHOLD = 0.5
SESSION_TURN_DETECTION_PREFIX_PADDING_MS = 300
SESSION_TURN_DETECTION_SILENCE_DURATION_MS = 200

# VAD Configuration (aliases for compatibility)
VAD_THRESHOLD = 0.5
VAD_PREFIX_PADDING_MS = 300
VAD_SILENCE_DURATION_MS = 200

# WebSocket Events - Outgoing
EVENT_SESSION_UPDATE = "session.update"
EVENT_INPUT_AUDIO_BUFFER_APPEND = "input_audio_buffer.append"
EVENT_INPUT_AUDIO_BUFFER_COMMIT = "input_audio_buffer.commit"
EVENT_INPUT_AUDIO_BUFFER_CLEAR = "input_audio_buffer.clear"
EVENT_RESPONSE_CREATE = "response.create"
EVENT_RESPONSE_CANCEL = "response.cancel"
EVENT_CONVERSATION_ITEM_CREATE = "conversation.item.create"

# Event type aliases for compatibility
EVENT_TYPE_SESSION_UPDATE = "session.update"
EVENT_TYPE_INPUT_AUDIO_BUFFER_APPEND = "input_audio_buffer.append"
EVENT_TYPE_INPUT_AUDIO_BUFFER_COMMIT = "input_audio_buffer.commit"
EVENT_TYPE_INPUT_AUDIO_BUFFER_CLEAR = "input_audio_buffer.clear"
EVENT_TYPE_RESPONSE_CREATE = "response.create"
EVENT_TYPE_RESPONSE_CANCEL = "response.cancel"
EVENT_TYPE_CONVERSATION_ITEM_CREATE = "conversation.item.create"

# WebSocket Events - Incoming
EVENT_SESSION_CREATED = "session.created"
EVENT_SESSION_UPDATED = "session.updated"
EVENT_INPUT_AUDIO_BUFFER_COMMITTED = "input_audio_buffer.committed"
EVENT_INPUT_AUDIO_BUFFER_CLEARED = "input_audio_buffer.cleared"
EVENT_INPUT_AUDIO_BUFFER_SPEECH_STARTED = "input_audio_buffer.speech_started"
EVENT_INPUT_AUDIO_BUFFER_SPEECH_STOPPED = "input_audio_buffer.speech_stopped"
EVENT_RESPONSE_CREATED = "response.created"
EVENT_RESPONSE_DONE = "response.done"
EVENT_RESPONSE_OUTPUT_ITEM_ADDED = "response.output_item.added"
EVENT_RESPONSE_OUTPUT_ITEM_DONE = "response.output_item.done"
EVENT_RESPONSE_CONTENT_PART_ADDED = "response.content_part.added"
EVENT_RESPONSE_CONTENT_PART_DONE = "response.content_part.done"
EVENT_RESPONSE_AUDIO_DELTA = "response.output_audio.delta"
EVENT_RESPONSE_AUDIO_DONE = "response.output_audio.done"
EVENT_RESPONSE_AUDIO_TRANSCRIPT_DELTA = "response.output_audio_transcript.delta"
EVENT_RESPONSE_AUDIO_TRANSCRIPT_DONE = "response.output_audio_transcript.done"
EVENT_RESPONSE_TEXT_DELTA = "response.text.delta"
EVENT_RESPONSE_TEXT_DONE = "response.text.done"
EVENT_RESPONSE_FUNCTION_CALL_ARGUMENTS_DELTA = "response.function_call_arguments.delta"
EVENT_RESPONSE_FUNCTION_CALL_ARGUMENTS_DONE = "response.function_call_arguments.done"
EVENT_ERROR = "error"

# Event type aliases for compatibility
EVENT_TYPE_INPUT_AUDIO_BUFFER_SPEECH_STARTED = "input_audio_buffer.speech_started"
EVENT_TYPE_INPUT_AUDIO_BUFFER_SPEECH_STOPPED = "input_audio_buffer.speech_stopped"
EVENT_TYPE_RESPONSE_DONE = "response.done"
EVENT_TYPE_RESPONSE_AUDIO_DELTA = "response.output_audio.delta"
EVENT_TYPE_RESPONSE_AUDIO_TRANSCRIPT_DELTA = "response.output_audio_transcript.delta"

# Error codes
ERROR_INVALID_API_KEY = "invalid_api_key"
ERROR_CONNECTION_FAILED = "connection_failed"
ERROR_AUDIO_PROCESSING = "audio_processing_error"
ERROR_UNKNOWN = "unknown_error"
