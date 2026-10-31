#!/usr/bin/env bash
set -euo pipefail

# iPhone Link — Linux build/verify helper
# Usage:
#   ./build.sh
#
# Verifies the Linux source tree is intact. Does NOT regenerate run.sh
# (run.sh is maintained by hand).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

for f in run.sh install.sh requirements.txt handset/__main__.py; do
  if [ ! -f "$f" ]; then
    echo "ERROR: missing $f" >&2
    exit 1
  fi
done

chmod +x run.sh install.sh
bash -n run.sh
bash -n install.sh

echo "Verified: run.sh, install.sh, requirements.txt, handset/__main__.py"
echo "Launch with: ./run.sh"
EOF
echo done