#!/usr/bin/env bash
# Test the XoneAI installer in Docker
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SMOKE_IMAGE="${XONEAI_SMOKE_IMAGE:-xoneai-install-smoke:local}"
INSTALL_URL="${XONEAI_INSTALL_URL:-file:///install.sh}"

echo "==> Build smoke test image: $SMOKE_IMAGE"
docker build \
  -t "$SMOKE_IMAGE" \
  -f "$ROOT_DIR/scripts/docker/install-smoke/Dockerfile" \
  "$ROOT_DIR/scripts/docker/install-smoke"

echo "==> Run installer smoke test"
docker run --rm -t \
  -v "$ROOT_DIR/scripts/install.sh:/install.sh:ro" \
  -e XONEAI_INSTALL_URL="$INSTALL_URL" \
  -e XONEAI_EXPECTED_VERSION="${XONEAI_EXPECTED_VERSION:-}" \
  -e XONEAI_EXTRAS="${XONEAI_EXTRAS:-}" \
  "$SMOKE_IMAGE"

echo "==> Smoke test completed successfully!"
