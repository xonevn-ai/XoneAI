# Dockerfile for XoneAI Slack Bot
# Secrets are passed at runtime via environment variables

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create xone config directory
RUN mkdir -p /root/.xone

# Install xoneai with bot dependencies
RUN pip install --no-cache-dir \
    xoneai \
    slack-bolt \
    slack-sdk \
    "discord.py>=2.0.0" \
    "python-telegram-bot>=20.0"

# Set environment variables for directory management
ENV XONE_CONFIG_DIR=/root/.xone
ENV DOCKER_CONTAINER=true

# Bot tokens should be passed at runtime (not baked into image)
# SLACK_BOT_TOKEN=xoxb-...
# SLACK_APP_TOKEN=xapp-...

# Optional: Copy custom agent configuration
# COPY agent.yaml /app/agent.yaml

# Expose no ports - Socket Mode doesn't need them
# For webhook mode, expose port 3000

# Default command - tokens from environment
CMD ["xoneai", "bot", "slack"]
