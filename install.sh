#!/usr/bin/env bash
set -euo pipefail

# iPhone Link - Linux installer (source checkout)
# Installs system deps, creates a venv, installs Python deps,
# and adds a desktop entry.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "iPhone Link: checking system dependencies..."
if command -v dnf >/dev/null 2>&1; then
  sudo dnf install -y python3-gobject webkit2gtk4.1 usbmuxd libimobiledevice ifuse xclip wl-clipboard || true
elif command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y python3-gi gir1.2-webkit2-4.1 usbmuxd libimobiledevice6 ifuse xclip wl-clipboard || true
elif command -v pacman >/dev/null 2>&1; then
  sudo pacman -S --needed --noconfirm python-gobject webkit2gtk usbmuxd libimobiledevice ifuse xclip wl-clipboard || true
fi

if [ ! -d ".venv" ]; then
  echo "iPhone Link: creating virtualenv..."
  python3 -m venv .venv
fi
# shellcheck source=/dev/null
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

chmod +x run.sh

# Desktop entry
DESKTOP_DIR="${HOME}/.local/share/applications"
mkdir -p "$DESKTOP_DIR"
ICON_PATH="$SCRIPT_DIR/assets/iphone_link.png"
cat > "$DESKTOP_DIR/iphone-link.desktop" <<DESKTOP
[Desktop Entry]
Name=iPhone Link
Comment=iPhone mirroring and control for Linux
Exec=$SCRIPT_DIR/run.sh
Icon=$ICON_PATH
Type=Application
Terminal=false
Categories=Utility;
DESKTOP
update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true

echo "iPhone Link: installed. Launch from app menu or run ./run.sh"
