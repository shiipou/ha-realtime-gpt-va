# OpenAI Realtime Voice Assistant for Home Assistant

A custom Home Assistant integration that provides low-latency voice assistant capabilities using OpenAI's Realtime API with streaming speech-to-text (STT) and text-to-speech (TTS).

## Features

- 🎤 **Low-latency streaming STT/TTS** using OpenAI's Realtime API
- 🔊 **Real-time audio streaming** with WebSocket connection
- ⚡ **Conversation interruption** - Cut off the AI when you start speaking
- 🗣️ **Voice Activity Detection (VAD)** - Automatic speech detection
- 🌍 **Multi-language support** - English, Spanish, French, German, Italian, Portuguese, Dutch, Polish, Russian, Japanese, Korean, Chinese
- 🎭 **Multiple voice options** - Choose from Alloy, Echo, or Shimmer
- ⚙️ **Configurable** - Adjust instructions, and more

## Installation

### HACS (Recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=shiipou&repository=ha-realtime-gpt-va&category=integration)


1. Add this repository as a custom repository in HACS
2. Search for "OpenAI Realtime Voice Assistant" in HACS
3. Click "Download"
4. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/openai_realtime` folder to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

### Initial Setup

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "OpenAI Realtime Voice Assistant"
4. Enter your OpenAI API key
5. Click **Submit**

### Getting an API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign in or create an account
3. Navigate to [API Keys](https://platform.openai.com/api-keys)
4. Click **Create new secret key**
5. Copy the key (you won't be able to see it again!)

### Configuration Options

After adding the integration, you can configure the following options:

- **Model**: The OpenAI model to use (default: `gpt-4o-realtime-preview-2024-10-01`)
- **Voice**: Choose from Alloy, Echo, or Shimmer
- **Instructions**: System instructions for the AI assistant

## Usage

### Setting Up Voice Assistant

1. Go to **Settings** → **Voice Assistants**
2. Click on your assistant (default is "Home Assistant")
3. Under **Speech-to-text**, select **OpenAI Realtime STT**
4. Under **Text-to-speech**, select **OpenAI Realtime TTS**
5. Save your changes

### Using the Voice Assistant

#### Via Home Assistant UI

1. Click the microphone icon in the top right
2. Start speaking to the assistant
3. The AI will respond with voice
4. You can interrupt the AI at any time by speaking

#### Via Voice Satellites

Configure your voice satellite devices (like ESPHome devices) to use the OpenAI Realtime assistant.

## Architecture

The integration consists of several components:

- **WebSocket Client** (`realtime_client.py`): Manages connection to OpenAI Realtime API
- **STT Platform** (`stt.py`): Converts speech to text in real-time
- **TTS Platform** (`tts.py`): Converts text to speech with streaming audio
- **Config Flow** (`config_flow.py`): Handles setup and configuration

### How It Works

1. **Audio Input**: Your microphone captures audio
2. **Streaming to OpenAI**: Audio is streamed in real-time to OpenAI's WebSocket
3. **VAD Detection**: Server-side voice activity detection identifies when you're speaking
4. **Transcription**: Your speech is transcribed on-the-fly
5. **AI Processing**: GPT-4 processes your request
6. **Audio Response**: AI response is streamed back as audio
7. **Interruption**: If you start speaking, the current response is cancelled immediately

## Advanced Configuration

### Custom Instructions

You can customize the AI's behavior by setting custom instructions:

```
You are a helpful voice assistant for a smart home.
- Be concise and natural
- Prioritize controlling devices when asked
- Use casual, friendly language
- Keep responses under 30 seconds when possible
```

### Home Assistant Integration

The assistant has access to Home Assistant's state and can control devices. Configure this in your Voice Assistant settings.

## Troubleshooting

### Audio Issues

**Problem**: No audio playback or recording

**Solutions**:
- Talk Louder, Assistant didn't hear you.
- Verify your audio devices are configured correctly
- Check Home Assistant audio settings
- Test with other TTS/STT providers to isolate the issue

### Connection Issues

**Problem**: "Failed to connect to OpenAI Realtime API"

**Solutions**:
- Verify your API key is correct
- Check your internet connection
- Ensure you have credits in your OpenAI account
- Check Home Assistant logs for detailed error messages

### High Latency

**Problem**: Slow response times

**Solutions**:
- Check your internet connection speed
- Verify you're using the realtime model

### API Quota Issues

**Problem**: "Rate limit exceeded"

**Solutions**:
- Check your OpenAI account usage
- Consider upgrading your OpenAI plan
- Reduce frequency of voice assistant usage

## Development

### Project Structure

```
custom_components/openai_realtime/
├── __init__.py           # Integration setup
├── manifest.json         # Integration metadata
├── const.py             # Constants and configuration
├── config_flow.py       # Configuration UI
├── realtime_client.py   # WebSocket client for OpenAI
├── stt.py              # Speech-to-text platform
└── tts.py              # Text-to-speech platform
```

### Testing

1. Enable debug logging in `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.openai_realtime: debug
```

2. Restart Home Assistant
3. Check logs at **Settings** → **System** → **Logs**

## Requirements

- Home Assistant 2024.1.0 or newer
- OpenAI API key with access to GPT-4 Realtime API
- Active internet connection
- Sufficient OpenAI API credits

## Cost Considerations

The OpenAI Realtime API uses token-based pricing:
- Audio input: ~$0.06 per minute
- Audio output: ~$0.24 per minute
- Text tokens: Standard GPT-4 pricing

Monitor your usage at [OpenAI Usage Dashboard](https://platform.openai.com/usage).

## Known Limitations

- Require open word because of Home Assistant Conversationnal agent (PR are welcome to fix this)
- Requires active internet connection
- May have higher latency on slower connections
- API costs can add up with frequent use
- Limited to OpenAI's supported languages

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Credits

Inspired by:
- [extended_openai_conversation](https://github.com/jekalmin/extended_openai_conversation) by jekalmin
- OpenAI's Realtime API documentation
- Home Assistant community
