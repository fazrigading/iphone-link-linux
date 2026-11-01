"""Linux clipboard integration for iPhone Link.

Integrates with the desktop clipboard via:
- pyperclip
- wl-copy/wl-paste (Wayland)
- xclip/xsel (X11)
"""

from __future__ import annotations

import os
import subprocess
import sys
from typing import Optional


def _prefer_tool() -> str:
    """Prefer Wayland clipboard when available, else fall back to X11 or pyperclip."""
    in_wayland = (
        os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland"
        or os.environ.get("WAYLAND_DISPLAY", "")
    )
    if in_wayland:
        for tool in ("wl-copy", "wl-paste"):
            if _which(tool):
                return tool
        return "wl-paste"
    for tool in ("xclip", "xsel"):
        if _which(tool):
            return tool
    return "pyperclip"


def _which(name: str) -> Optional[str]:
    path = os.environ.get("PATH", "").split(os.pathsep)
    for entry in path:
        candidate = os.path.join(entry, name)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None


def _run(args: list[str], input_text: Optional[str], timeout: float = 5.0) -> str:
    try:
        completed = subprocess.run(
            args,
            input=input_text,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        if completed.returncode != 0 and completed.stdout.strip():
            return completed.stdout.strip()
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or f"exit {completed.returncode}")
        return completed.stdout.strip()
    except Exception as error:
        raise RuntimeError(f"clipboard helper failed: {error}") from error


def get_clipboard_text() -> Optional[str]:
    tool = _prefer_tool()
    if tool == "pyperclip":
        try:
            import pyperclip

            return pyperclip.paste() or None
        except Exception:
            return None
    if tool.startswith("wl-paste"):
        try:
            text = _run(["wl-paste", "--no-newline", "--type", "text/plain"], None)
            return text or None
        except Exception:
            return None
    if tool == "xclip":
        try:
            text = _run(["xclip", "-selection", "clipboard", "-o"], None)
            return text or None
        except Exception:
            return None
    if tool == "xsel":
        try:
            text = _run(["xsel", "--clipboard", "--output"], None)
            return text or None
        except Exception:
            return None
    return None


def set_clipboard_text(text: str) -> bool:
    if not text:
        return False
    tool = _prefer_tool()
    if tool == "pyperclip":
        try:
            import pyperclip

            pyperclip.copy(text)
            return True
        except Exception:
            return False
    if tool.startswith("wl-copy"):
        try:
            _run(["wl-copy", "--type", "text/plain"], text)
            return True
        except Exception:
            return False
    if tool == "xclip":
        try:
            _run(["xclip", "-selection", "clipboard"], text)
            return True
        except Exception:
            return False
    if tool == "xsel":
        try:
            _run(["xsel", "--clipboard", "--input"], text)
            return True
        except Exception:
            return False
    return False
