"""Linux audio integration for iPhone Link.

On Linux the Windows AudioPlaybackConnection A2DP stack stays unchanged in handset/audio.py.
This module adds a small Linux-side volume control helper (PulseAudio/PipeWire via pactl,
or a no-op fallback) and exposes the same status shape the web UI already reads.

The app still mirrors iPhone audio to the PC's default output device; this module exists so
the Linux launcher can keep the "Stream Audio to PC" tray toggle meaningful without calling
Windows APIs (/dev/video3 would be off-topic here).
"""

from __future__ import annotations

import os
import subprocess
import sys
from typing import Any, Dict, Optional


def _prefer_controller() -> Optional[str]:
    for tool in ("pactl", "wpctl"):
        if _which(tool):
            return tool
    return None


def _which(name: str) -> Optional[str]:
    path = os.environ.get("PATH", "").split(os.pathsep)
    for entry in path:
        candidate = os.path.join(entry, name)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None


class LinuxAudioManager:
    """Thin Linux volume/status adapter used by the Linux launcher and tray menu."""

    def __init__(self):
        self._enabled = False
        self._active = False
        self._device_name = "default"
        self._connection_state = "Off"
        self._cached_volume: Optional[int] = None
        self._controller = _prefer_controller()

    def is_active(self) -> bool:
        return bool(self._enabled and self._active)

    def status(self, refresh_volume: bool = False) -> Dict[str, Any]:
        if self._controller == "pactl":
            try:
                self._cached_volume = _pactl_volume()
            except Exception:
                self._cached_volume = None
        elif self._controller == "wpctl":
            try:
                self._cached_volume = _wpctl_volume()
            except Exception:
                self._cached_volume = None
        else:
            self._cached_volume = None

        if refresh_volume:
            pass

        return {
            "enabled": self._enabled,
            "active": self._active,
            "device": self._device_name,
            "state": self._connection_state if self._active else "Off",
            "volume": self._cached_volume,
        }

    def get_volume(self) -> int:
        vol = self._cached_volume
        if vol is None:
            try:
                if self._controller == "pactl":
                    vol = _pactl_volume()
                elif self._controller == "wpctl":
                    vol = _wpctl_volume()
                else:
                    vol = 100
            except Exception:
                vol = 100
        return vol if isinstance(vol, int) else 100

    def set_volume(self, level_percent: int) -> Dict[str, Any]:
        vol = max(0, min(100, int(level_percent)))
        if self._controller == "pactl":
            _pactl_set_volume(vol)
        elif self._controller == "wpctl":
            _wpctl_set_volume(vol)
        self._cached_volume = vol
        return {"ok": True, "volume": vol}

    def open_bluetooth_settings(self) -> Dict[str, Any]:
        return {"ok": False, "error": "Bluetooth settings not handled on Linux in this build"}

    def enable(self) -> Dict[str, Any]:
        if self._controller:
            self._enabled = True
            self._active = True
            self._connection_state = "Opened"
            try:
                self._device_name = "default"
            except Exception:
                self._device_name = "default"
            return self.status()
        self._enabled = False
        self._active = False
        return self.status()

    def disable(self) -> Dict[str, Any]:
        self._enabled = False
        self._active = False
        self._connection_state = "Off"
        return self.status()

    def shutdown(self) -> None:
        self.disable()

    def stop(self) -> Dict[str, Any]:
        return self.disable()

    def toggle(self, enable: Optional[bool] = None) -> Dict[str, Any]:
        if enable is None:
            should_enable = not self._enabled
        else:
            should_enable = bool(enable)
        if should_enable:
            return self.enable()
        return self.disable()


def _pactl_volume() -> int:
    completed = subprocess.run(
        ["pactl", "get-sink-volume", "@DEFAULT@"],
        text=True,
        capture_output=True,
        check=False,
    )
    for line in (completed.stdout or "").splitlines():
        if "%" in line:
            for part in line.replace(",", " ").split():
                if part.endswith("%"):
                    try:
                        return int(part[:-1])
                    except ValueError:
                        continue
    return 100


def _pactl_set_volume(percent: int) -> None:
    subprocess.run(
        ["pactl", "set-sink-volume", "@DEFAULT@", f"{percent}%%"],
        check=False,
    )


def _wpctl_volume() -> int:
    completed = subprocess.run(
        ["wpctl", "get-volume", "@DEFAULT@"],
        text=True,
        capture_output=True,
        check=False,
    )
    for line in (completed.stdout or "").splitlines():
        if "Volume:" in line:
            parts = line.split()
            if len(parts) >= 2:
                try:
                    return max(0, min(100, round(float(parts[1]) * 100)))
                except ValueError:
                    continue
    return 100


def _wpctl_set_volume(percent: int) -> None:
    subprocess.run(
        ["wpctl", "set-volume", "@DEFAULT@", f"{percent / 100.0:.3f}"],
        check=False,
    )


linux_audio_manager = LinuxAudioManager()
