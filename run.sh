#!/usr/bin/env bash
set -euo pipefail

# iPhone Link — Linux launcher
# This script launches iPhone Link from a source checkout.
# For a standalone frozen build, run the frozen executable instead.
#
# Usage:
#   ./run_linux.sh                # normal launch
#   ./run_linux.sh --verbose      # verbose: keep backend logs in ./iphone-link.log

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VERBOSE=0
for arg in "$@"; do
  case "$arg" in
    --verbose|-v) VERBOSE=1 ;;
  esac
done

if [ "$VERBOSE" = "1" ]; then
  export PANE_VERBOSE=1
  echo "iPhone Link: VERBOSE mode — backend logs -> $SCRIPT_DIR/iphone-link.log" >&2
fi

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
  if [ -d ".venv" ]; then
    VENV_DIR=".venv"
  elif [ -d "venv" ]; then
    VENV_DIR="venv"
  else
    echo "iPhone Link: no virtualenv found at ./.venv (or ./venv)" >&2
    echo "iPhone Link: run the following once to set up dependencies:" >&2
    echo "  $PYTHON -m venv .venv" >&2
    echo "  source .venv/bin/activate" >&2
    echo "  pip install -r requirements.txt" >&2
    exit 1
  fi
  echo "iPhone Link: activating local venv at ./$VENV_DIR" >&2
  # shellcheck source=/dev/null
  source "$VENV_DIR/bin/activate"
fi

# Linux dependency checks
if ! command -v usbmuxd >/dev/null 2>&1; then
  echo "iPhone Link: usbmuxd not found. Install it:" >&2
  echo "  Fedora: sudo dnf install usbmuxd libimobiledevice ifuse" >&2
  echo "  Debian: sudo apt install usbmuxd libimobiledevice6 ifuse" >&2
  exit 1
fi

exec "$PYTHON" -m handset "$@"
