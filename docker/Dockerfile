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

# Install Python packages (using latest versions)
# Note: xoneai is installed from PyPI - remove version pin to use latest available
RUN pip install --no-cache-dir \
    flask \
    xoneai \
    "xoneai[api]" \
    gunicorn \
    markdown

# Copy application code
COPY . .

# Set environment variables for directory management
ENV XONE_CONFIG_DIR=/root/.xone
ENV DOCKER_CONTAINER=true

# Create health check API if api.py doesn't exist
RUN if [ ! -f api.py ]; then \
    echo "from flask import Flask\n\
    app = Flask(__name__)\n\
    \n\
    @app.route('/health')\n\
    def health():\n\
    return {'status': 'healthy'}, 200\n\
    \n\
    if __name__ == '__main__':\n\
    app.run()" > api.py; \
    fi

EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "api:app"]
