#!/usr/bin/env bash
set -euo pipefail

# iPhone Link — Linux launcher
# This script launches iPhone Link from a source checkout.
# For a standalone frozen build, run the frozen executable instead.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
else
  if command -v python >/dev/null 2>&1; then
    PYTHON=python
  else
    echo "ERROR: python3 or python not found on PATH" >&2
    exit 1
  fi
fi

# If run from a source checkout without an activated venv, remind the user.
if [ -z "${VIRTUAL_ENV:-}" ]; then
  if [ ! -d "venv" ]; then
    echo "iPhone Link: no virtualenv found at ./venv" >&2
    echo "iPhone Link: run the following once to set up dependencies:" >&2
    echo "  $PYTHON -m venv venv" >&2
    echo "  source venv/bin/activate" >&2
    echo "  pip install -r requirements.txt" >&2
    exit 1
  fi
  echo "iPhone Link: activating local venv at ./venv" >&2
  # shellcheck source=/dev/null
  source venv/bin/activate
fi

exec "$PYTHON" -m handset "$@"
