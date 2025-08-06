# API Monitor

A Python script that monitors the health of an API endpoint and sends Telegram notifications when the service is down or returns non-200 status codes.

## Features

- 🔍 **API Health Monitoring**: Continuously monitors your configured API endpoint
- 📱 **Telegram Notifications**: Sends alerts via Telegram bot when API is down
- 🐳 **Docker Support**: Easy deployment with Docker and Docker Compose
- 📊 **Logging**: Comprehensive logging with both console and file output
- ⚙️ **Configurable**: Environment variables for easy configuration
- 🔄 **Automatic Restart**: Docker container restarts automatically on failure

## Prerequisites

1. **Telegram Bot**: You need to create a Telegram bot and get the bot token
2. **Chat ID**: The chat ID where notifications will be sent

### Setting up Telegram Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Save the bot token
4. Start a conversation with your bot
5. Get your chat ID by visiting: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone or download the files**

2. **Create environment file**:
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` file with your configuration**:
   ```bash
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   API_URL=https://your-api-endpoint.com
   CHECK_INTERVAL=60
   ```

4. **Build and run**:
   ```bash
   docker-compose up -d
   ```

### Using Docker directly

1. **Build the image**:
   ```bash
   docker build -t server-health-checker .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     --name server-health-checker \
     --restart unless-stopped \
     -e TELEGRAM_BOT_TOKEN=your_bot_token \
     -e TELEGRAM_CHAT_ID=your_chat_id \
     -e CHECK_INTERVAL=60 \
     server-health-checker
   ```

### Running locally

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**:
   ```bash
   export TELEGRAM_BOT_TOKEN=your_bot_token
   export TELEGRAM_CHAT_ID=your_chat_id
   export CHECK_INTERVAL=60
   ```

3. **Run the script**:
   ```bash
   python monitor.py
   ```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | - | Yes |
| `TELEGRAM_CHAT_ID` | Chat ID for notifications | - | Yes |
| `API_URL` | API endpoint to monitor | `https://your-api-endpoint.com` | No |
| `CHECK_INTERVAL` | Check interval in seconds | `60` | No |

## Monitoring

### View logs

```bash
# Docker Compose
docker-compose logs -f server-health-checker

# Docker
docker logs -f server-health-checker

# Local
tail -f monitor.log
```

### Check container status

```bash
docker-compose ps
# or
docker ps
```

## Telegram Message Format

When the API is down, you'll receive a message like this:

```
🚨 API Health Alert

URL: https://your-api-endpoint.com
Status Code: 500
Message: API returned status 500
Time: 2024-01-15 14:30:25
```

## Troubleshooting

### Common Issues

1. **Telegram bot not sending messages**:
   - Verify your bot token is correct
   - Make sure you've started a conversation with your bot
   - Check that the chat ID is correct

2. **Container exits immediately**:
   - Check the logs: `docker logs api-monitor`
   - Verify environment variables are set correctly

3. **API monitoring not working**:
   - Check if the API URL is accessible
   - Verify network connectivity

### Debug Mode

To run with debug logging:

```bash
# Set log level
export PYTHONPATH=/app
python -c "import logging; logging.getLogger().setLevel(logging.DEBUG)" && python monitor.py
```

## Development

### Project Structure

```
.
├── monitor.py          # Main monitoring script
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose configuration
└── README.md         # This file
```

### Adding Features

The script is modular and easy to extend:

- Add new notification channels by extending the `APIMonitor` class
- Modify the health check logic in `check_api_health()`
- Add custom alert conditions

## License

This project is open source and available under the MIT License. 