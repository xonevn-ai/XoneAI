FROM python:3.12-slim-bookworm

RUN set -eux; \
  apt-get update && \
  apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    curl \
    git \
  && rm -rf /var/lib/apt/lists/*

COPY run.sh /usr/local/bin/xoneai-install-smoke
RUN chmod +x /usr/local/bin/xoneai-install-smoke

ENTRYPOINT ["/usr/local/bin/xoneai-install-smoke"]
