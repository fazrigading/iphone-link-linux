"""Linux GUI front-end for iPhone Link using pywebview.

Provides the WindowApi JS bridge, webview window, system tray integration,
and desktop integration hooks.
"""

from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
from pathlib import Path

try:
    import gi  # noqa: F401
except Exception:
    _ver = f"{sys.version_info.major}.{sys.version_info.minor}"
    for _base in ("/usr/lib", "/usr/lib64", "/usr/local/lib"):
        for _sub in ("site-packages", "dist-packages"):
            _candidate = f"{_base}/python{_ver}/{_sub}"
            if os.path.isdir(_candidate) and _candidate not in sys.path:
                sys.path.append(_candidate)
    if os.path.isdir("/usr/lib/python3/dist-packages") and "/usr/lib/python3/dist-packages" not in sys.path:
        sys.path.append("/usr/lib/python3/dist-packages")

from handset import get_app_root, get_bundle_root, get_user_cache_dir
from handset.server import HOST, PORT
from handset.clipboard import get_clipboard_text, set_clipboard_text
from handset.audio import audio_manager
from handset.server import load_user_settings, save_user_settings


try:
    import pystray  # noqa: F401
    import PIL  # noqa: F401
    _tray_available = True
except Exception:
    _tray_available = False


def _tray_available() -> bool:
    return _tray_available


def _resolve_icon_path() -> Path | None:
    candidates = [
        get_app_root() / "assets" / "iphone_link.png",
        get_bundle_root() / "assets" / "iphone_link.png",
        Path(__file__).resolve().parent.parent / "assets" / "iphone_link.png",
        get_app_root() / "packaging" / "pane.png",
        get_bundle_root() / "packaging" / "pane.png",
    ]
    for cand in candidates:
        if cand.is_file():
            return cand
    return None


def _is_server_responding(url: str, timeout: float = 2.0) -> bool:
    import urllib.request

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "iPhoneLink-Linux"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False


def _parse_host_port() -> tuple[str, int]:
    host = os.environ.get("PANE_HOST", HOST)
    port = int(os.environ.get("PANE_PORT", PORT))
    argv = sys.argv[1:]
    for idx, arg in enumerate(argv):
        if arg == "--host" and idx + 1 < len(argv):
            host = argv[idx + 1]
        elif arg.startswith("--host="):
            host = arg.split("=", 1)[1]
        elif arg == "--port" and idx + 1 < len(argv):
            try:
                port = int(argv[idx + 1])
            except ValueError:
                pass
        elif arg.startswith("--port="):
            try:
                port = int(arg.split("=", 1)[1])
            except ValueError:
                pass
    return host, port


class WindowApi:
    """JS-accessible API exposed under window.pywebview.api (Linux build)."""

    def __init__(self, host: str = HOST, port: int = PORT):
        self._window = None
        self._host = host
        self._port = port
        self._is_landscape = False
        self._drawer_open = False
        self._hidden_to_tray = False
        self._theme = "dark"

    def set_window(self, window):
        self._window = window

    def _eval_js(self, script: str) -> None:
        if self._window is None:
            return
        try:
            self._window.evaluate_js(script)
        except Exception:
            pass

    def _api_get(self, path: str, timeout: float = 1.5) -> dict:
        import json
        import urllib.request

        req = urllib.request.Request(f"http://{self._host}:{self._port}{path}",
                                      headers={"User-Agent": "iPhoneLink-Linux"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _api_post(self, path: str, payload: bytes = b"{}", timeout: float = 1.5) -> dict:
        import json
        import urllib.request

        req = urllib.request.Request(
            f"http://{self._host}:{self._port}{path}",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def start_window_drag(self) -> None:
        return

    def minimize(self) -> None:
        if self._window:
            try:
                self._window.minimize()
            except Exception:
                pass

    def minimize_to_tray(self) -> dict:
        self._hidden_to_tray = True
        if self._window:
            try:
                self._window.hide()
            except Exception:
                pass
        return {"ok": True, "hidden": True}

    def restore_from_tray(self) -> dict:
        self._hidden_to_tray = False
        if self._window:
            try:
                self._window.show()
                self._window.restore()
            except Exception:
                pass
            self._eval_js("window.dispatchEvent(new Event('resize'));")
        return {"ok": True, "hidden": False}

    def toggle_tray_window(self) -> dict:
        if self._hidden_to_tray:
            return self.restore_from_tray()
        return self.minimize_to_tray()

    def tray_toggle_landscape(self) -> None:
        self._eval_js("if (window.toggleLandscapeMode) window.toggleLandscapeMode();")

    def tray_toggle_stealth(self) -> None:
        self._eval_js("if (window.triggerToggleStealthDim) window.triggerToggleStealthDim();")

    def tray_toggle_audio(self) -> None:
        try:
            self._api_post("/api/audio/toggle", b"{}")
        except Exception:
            pass

    def tray_clear_copy_cache(self) -> None:
        try:
            self._api_post("/api/ocr/clear-chunks", b"{}", timeout=0.8)
        except Exception:
            pass
        self._eval_js("if (window.triggerClearCopyCacheWithFeedback) window.triggerClearCopyCacheWithFeedback();")

    def get_tray_menu_state(self) -> dict:
        stealth_on = False
        audio_on = audio_manager.is_active()
        try:
            data = self._api_get("/api/tray-state", timeout=0.35)
            stealth_on = bool(data.get("stealth"))
        except Exception:
            pass
        return {
            "landscape": bool(self._is_landscape),
            "stealth": stealth_on,
            "audio": audio_on,
        }

    def close(self) -> None:
        self._hidden_to_tray = False
        if self._window:
            try:
                self._window.destroy()
            except Exception:
                pass

    def toggle_fullscreen(self) -> None:
        if self._window:
            try:
                self._window.toggle_fullscreen()
            except Exception:
                pass

    def set_orientation(self, landscape: bool, drawer_open: bool = False) -> None:
        if not self._window:
            return
        self._is_landscape = bool(landscape)
        self._drawer_open = bool(drawer_open)
        if self._is_landscape:
            target_w = 1200 if self._drawer_open else 840
            target_h = 720 if self._drawer_open else 490
        else:
            target_w = 740 if self._drawer_open else 380
            target_h = 840
        try:
            self._window.resize(target_w, target_h)
        except Exception as e:
            print("set_orientation error:", e)

    def sync_device_aspect(self, display_width: int, drawer_open: bool = False) -> None:
        if not self._window:
            return
        self._drawer_open = bool(drawer_open)
        if self._is_landscape:
            target_w = 1200 if self._drawer_open else 840
            target_h = 720 if self._drawer_open else 490
        else:
            dw = max(380, min(800, int(display_width)))
            target_w = dw + (360 if self._drawer_open else 0)
            target_h = max(self._window.height or 840, 840)
        try:
            self._window.resize(target_w, target_h)
        except Exception as e:
            print("sync_device_aspect error:", e)

    def set_drawer(self, is_open: bool) -> None:
        if not self._window:
            return
        self._drawer_open = bool(is_open)
        if self._is_landscape:
            target_w = 1200 if self._drawer_open else 840
            target_h = 720 if self._drawer_open else 490
        else:
            target_w = 740 if self._drawer_open else 380
            target_h = 840
        try:
            self._window.resize(target_w, target_h)
        except Exception as e:
            print("set_drawer error:", e)

    def set_theme(self, theme: str) -> None:
        self._theme = theme

    def is_pywebview(self) -> bool:
        return True

    def wipe_privacy_data(self) -> dict:
        try:
            return self._api_post("/api/device/wipe-privacy-data", b"{}", timeout=2.0)
        except Exception:
            from handset.screen import wipe_all_privacy_data
            return wipe_all_privacy_data()


def _tray_loop(api: WindowApi) -> None:
    return


def _has_gtk_tray() -> bool:
    return False


def _start_tray(api: WindowApi) -> bool:
    """Start a separate Linux system tray icon for the window.

    Uses ``pystray`` + Pillow. If unavailable, returns False and
    the window keeps its pywebview tray (if any).
    """
    try:
        import pystray
        from PIL import Image
    except Exception:
        return False

    icon_path = _resolve_icon_path()
    if icon_path is None:
        return False

    icon = pystray.Icon(
        "iphonelink",
        Image.open(icon_path).resize((64, 64)),
        "iPhone Link",
        menu=pystray.Menu(
            pystray.MenuItem("Show", lambda _: _run(lambda: api.restore_from_tray())),
            pystray.MenuItem("Hide", lambda _: _run(lambda: api.minimize_to_tray())),
            pystray.Separator(),
            pystray.MenuItem("Quit", lambda _: _run(lambda: sys.exit(0))),
        ),
    )
    api._hidden_to_tray = False
    icon.run_detached()
    return True


def _run(fn):
    import threading
    threading.Thread(target=fn, daemon=True).start()


def _spawn_tray_in_background(api: WindowApi) -> None:
    import threading

    def _tray_worker():
        _start_tray(api)

    t = threading.Thread(target=_tray_worker, name="iphonelink-linux-tray", daemon=True)
    t.start()


def main() -> None:
    if "--server-child" in sys.argv or "--server-only" in sys.argv:
        host, port = _parse_host_port()
        from handset.server import serve as _serve_backend
        _serve_backend(host=host, port=port)
        return

    host, port = _parse_host_port()

    if _is_server_responding(f"http://{host}:{port}/api/tray-state", timeout=0.5):
        _open_window(host, port)
        return

    _open_window(host, port)


def _open_window(host: str, port: int) -> None:
    import webview

    api = WindowApi(host=host, port=port)

    url = f"http://{host}:{port}/?t={int(time.time())}"
    window = webview.create_window(
        title="iPhone Link",
        url=url,
        js_api=api,
        width=380,
        height=840,
        frameless=True,
        min_size=(368, 450),
        background_color="#0f172a",
        text_select=False,
        resizable=True,
    )
    api.set_window(window)

    icon_path = _resolve_icon_path()
    if icon_path is not None:
        try:
            window.set_icon(str(icon_path))
        except Exception:
            pass

    storage_path = _resolve_webview_storage_path()
    tray_icon_path = icon_path
    menu_items = []
    if tray_icon_path is not None:
        menu_items.append(
            ("Show", lambda _: window.show() if window is not None else None)
        )
        menu_items.append(
            ("Hide", lambda _: window.hide() if window is not None else None)
        )
        menu_items.append(("Quit", lambda _: sys.exit(0)))

    try:
        webview.start(
            func=None,
            args=None,
            debug=False,
            private_mode=False,
            storage_path=storage_path,
            user_agent="iPhoneLink-Linux",
            icon=tray_icon_path,
            menu=menu_items,
        )
    finally:
        api.close()
        _spawn_tray_in_background(api)


def _resolve_webview_storage_path() -> str:
    local_dir = get_user_cache_dir() / "webview_storage"
    try:
        local_dir.mkdir(parents=True, exist_ok=True)
        return str(local_dir)
    except OSError:
        import hashlib

        folder_id = hashlib.sha256(
            os.path.normcase(str(get_app_root().resolve())).encode("utf-8")
        ).hexdigest()[:12]
        fallback = get_user_cache_dir() / "webview_storage_instances" / folder_id
        fallback.mkdir(parents=True, exist_ok=True)
        return str(fallback)


if __name__ == "__main__":
    main()

