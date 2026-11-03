#!/usr/bin/env bash
set -euo pipefail

# iPhone Link — Linux launcher
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
  echo "iPhone Link: VERBOSE mode — backend logs -> ${XDG_STATE_HOME:-$HOME/.local/state}/iphone-link/iphone-link.log" >&2
fi

# AppImage support
if [ -n "${APPDIR:-}" ]; then
  # Use bundled python
  if [ -x "$APPDIR/usr/bin/python3" ]; then
    PYTHON="$APPDIR/usr/bin/python3"
  elif [ -x "$APPDIR/bin/python3" ]; then
    PYTHON="$APPDIR/bin/python3"
  else
    PYTHON="$(command -v python3 || command -v python)"
  fi
  
  # Set up PYTHONPATH for bundled packages
  for p in "$APPDIR/usr/lib/python3.14/site-packages" "$APPDIR/usr/lib/python3.12/site-packages" "$APPDIR/usr/lib/python3.11/site-packages"; do
    if [ -d "$p" ]; then
      export PYTHONPATH="$p${PYTHONPATH:+:$PYTHONPATH}"
    fi
  done
  
  # Linux dependency checks for AppImage
  if ! command -v usbmuxd >/dev/null 2>&1; then
    echo "iPhone Link: usbmuxd not found. Install it:" >&2
    echo "  Fedora: sudo dnf install usbmuxd libimobiledevice libimobiledevice-utils ifuse" >&2
    echo "  Debian: sudo apt install usbmuxd libimobiledevice-1.0-6 libimobiledevice-utils ifuse" >&2
    echo "  Arch:   sudo pacman -S usbmuxd libimobiledevice libimobiledevice-utils ifuse" >&2
    exit 1
  fi
  
  exec "$PYTHON" -m handset "$@"
  exit $?
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
  if [ ! -d ".venv" ]; then
    echo "iPhone Link: no virtualenv found at ./.venv" >&2
    echo "iPhone Link: run the following once to set up dependencies:" >&2
    echo "  $PYTHON -m venv .venv" >&2
    echo "  source .venv/bin/activate" >&2
    echo "  pip install -r requirements.txt" >&2
    exit 1
  fi
  echo "iPhone Link: activating local venv at ./.venv" >&2
  # shellcheck source=/dev/null
  source .venv/bin/activate
fi

# Linux dependency checks
if ! command -v usbmuxd >/dev/null 2>&1; then
  echo "iPhone Link: usbmuxd not found. Install it:" >&2
  echo "  Fedora: sudo dnf install usbmuxd libimobiledevice libimobiledevice-utils ifuse" >&2
  echo "  Debian: sudo apt install usbmuxd libimobiledevice-1.0-6 libimobiledevice-utils ifuse" >&2
  echo "  Arch:   sudo pacman -S usbmuxd libimobiledevice libimobiledevice-utils ifuse" >&2
  exit 1
fi

exec "$PYTHON" -m handset "$@"
