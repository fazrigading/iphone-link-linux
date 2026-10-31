#!/usr/bin/env bash
set -euo pipefail

# iPhone Link — Linux launcher helper
# Usage:
#   ./build_executable.sh
#
# This script prepares the Linux run script and verifies the launcher shape.
# It does NOT produce a compiled ELF binary because iPhone Link is a Python +
# pywebview app. The intended Linux entry points are:
#   - ./run.sh               (launcher with venv guidance)
#   - python3 -m handset          (direct module run)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

RUN_SH="run.sh"

if [ ! -f "requirements.txt" ]; then
  echo "ERROR: requirements.txt not found in project root" >&2
  exit 1
fi

cat > "$RUN_SH" <<'EOF'
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
EOF

chmod +x "$RUN_SH"

if [ ! -x "$RUN_SH" ]; then
  echo "ERROR: failed to make $RUN_SH executable" >&2
  exit 1
fi

echo "Created executable: $RUN_SH"
echo "Verify with: ./run.sh --help"
echo "Or run directly: python3 -m handset"

# Optional: print a short desktop-launcher template for Linux users who want one.
cat > "iphone-link.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=iPhone Link
Comment=Native iPhone mirroring and control (Linux source build)
Exec=/absolute/path/to/iphone-link/run.sh
Icon=/absolute/path/to/iphone-link/assets/iphone_link.png
Terminal=false
Categories=Utility;
EOF

echo "Created desktop template: iphone-link.desktop"
echo "Edit Exec= and Icon= to match your install path before using it."
