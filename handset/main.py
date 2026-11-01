"""Linux desktop entry point for iPhone Link.

Runs the backend server and provides a native Linux window with pywebview
and desktop integration (app icon, system tray, volume control, clipboard).
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

# pywebview's Linux GTK backend needs PyGObject (python3-gobject / python3-gi),
# which is a system package and is not pip-installable into the venv. Make the
# system site-packages available so `import gi` resolves when running from a
# venv that does not include it.
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

try:
    import gi  # noqa: F401
    gi.require_version("Gtk", "3.0")
    gi.require_version("WebKit2", "4.1")
except Exception as _gi_err:
    print(
        "iPhone Link: missing Linux system dependency PyGObject/WebKit2GTK.\n"
        "  Fedora:   sudo dnf install python3-gobject webkit2gtk4.1\n"
        "  Debian:   sudo apt install python3-gi gir1.2-webkit2-4.1\n"
        "  Arch:     sudo pacman -S python-gobject webkit2gtk\n"
        f"  (import error: {_gi_err})",
        file=sys.stderr,
    )
    raise SystemExit(2)

from handset import get_app_root, get_bundle_root, get_user_cache_dir, get_user_state_dir
from handset.server import HOST, PORT, create_http_server

# Linux UI helpers: Linux clipboard and audio are Linux-only; WindowApi stays in
# handset/gui.py because it is the pywebview JS bridge for this frontend.
from handset.clipboard import get_clipboard_text, set_clipboard_text
from handset.audio import audio_manager

_SERVER_PROC = None


def _resolve_web_root() -> Path:
    for cand in (
        get_app_root() / "handset" / "web",
        get_bundle_root() / "handset" / "web",
        Path(__file__).resolve().parent / "web",
    ):
        if cand.is_dir():
            return cand
    return Path(__file__).resolve().parent / "web"







def _build_server_command(host: str, port: int) -> list[str]:
    if getattr(sys, "frozen", False):
        return [sys.executable, "-m", "handset", "--server-child", "--host", host, "--port", str(port)]
    return [sys.executable, "-m", "handset", "--server-child", "--host", host, "--port", str(port)]


def _webview_available() -> bool:
    try:
        import webview  # noqa: F401
        return True
    except Exception:
        return False


def _spawn_tray_in_background(api):
    try:
        from handset.gui import _spawn_tray_in_background as _real

        return _real(api)
    except Exception:
        return None


def _start_backend_server(host: str, port: int, timeout: float = 10.0) -> bool:
    ready_url = f"http://{host}:{port}/api/tray-state"

    import urllib.request

    def _responding(url: str, timeout_s: float = 2.0) -> bool:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "iPhoneLink-Linux"})
            with urllib.request.urlopen(req, timeout=timeout_s) as resp:
                return resp.status == 200
        except Exception:
            return False

    if _responding(ready_url, timeout_s=0.6):
        return True

    cmd = _build_server_command(host, port)
    child_env = dict(os.environ)
    child_env["PANE_HOST"] = host
    child_env["PANE_PORT"] = str(port)

    if os.environ.get("PANE_VERBOSE"):
        log_path = get_user_state_dir() / "iphone-link.log"
        log_file = open(log_path, "a", buffering=1)
        log_file.write(f"\n===== backend start {time.strftime('%Y-%m-%d %H:%M:%S')} =====\n")
        log_file.flush()
        stdout_target = log_file
        stderr_target = subprocess.STDOUT
    else:
        stdout_target = subprocess.DEVNULL
        stderr_target = subprocess.DEVNULL

    global _SERVER_PROC
    proc = subprocess.Popen(
        cmd,
        cwd=str(get_app_root()),
        env=child_env,
        stdin=subprocess.DEVNULL,
        stdout=stdout_target,
        stderr=stderr_target,
    )
    _SERVER_PROC = proc

    start = time.time()
    while time.time() - start < timeout:
        if proc.poll() is not None:
            return False
        if _responding(ready_url, timeout_s=5.0):
            return True
        time.sleep(0.12)

    proc.terminate()
    proc.wait(timeout=2.0)
    return False


def _is_server_responding(url: str, timeout: float = 2.0) -> bool:
    try:
        import urllib.request

        req = urllib.request.Request(url, headers={"User-Agent": "iPhoneLink-Linux"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False


def _focus_existing_window_if_running(host: str, port: int) -> bool:
    try:
        url = f"http://{host}:{port}/api/tray-state"
        if _is_server_responding(url, timeout=0.5):
            _open_window(host, port)
            return True
    except Exception:
        pass
    return False


def _open_window(host: str, port: int) -> None:
    import webview

    # NOTE: Linux frontend uses handset/gui.WindowApi as its JS bridge.
    # If Linux is ever rebased onto handset/gui.py, this is the import to swap.
    from handset.gui import WindowApi

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

    storage_path = _resolve_storage_path(host=host)
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


def _resolve_storage_path(host: str = "127.0.0.1") -> str:
    return _resolve_storage_path_for_host(host)


def _resolve_storage_path_for_host(host: str) -> str:
    host_slot = host.replace(":", "_")
    local_dir = get_user_cache_dir() / "webview_storage" / host_slot
    try:
        local_dir.mkdir(parents=True, exist_ok=True)
        return str(local_dir)
    except OSError:
        import hashlib

        folder_id = hashlib.sha256(
            os.path.normcase(str(get_app_root().resolve())).encode("utf-8")
        ).hexdigest()[:12]
        fallback = get_user_cache_dir() / "webview_storage_instances" / f"{folder_id}_{host_slot}"
        fallback.mkdir(parents=True, exist_ok=True)
        return str(fallback)


def main() -> None:
    if "--server-child" in sys.argv or "--server-only" in sys.argv:
        host = os.environ.get("PANE_HOST", HOST)
        port = int(os.environ.get("PANE_PORT", PORT))
        server = create_http_server(host=host, port=port)
        try:
            server.serve_forever()
        finally:
            audio_manager.shutdown()
        return

    host = os.environ.get("PANE_HOST", HOST)
    port = int(os.environ.get("PANE_PORT", PORT))

    try:
        if _focus_existing_window_if_running(host, port):
            return

        if not _start_backend_server(host, port, timeout=10.0):
            print("iPhone Link: failed to start backend server", file=sys.stderr)
            raise SystemExit(2)

        if not _is_server_responding(f"http://{host}:{port}/api/tray-state", timeout=0.5):
            _open_window(host, port)
            return

        _open_window(host, port)
    finally:
        global _SERVER_PROC
        if _SERVER_PROC is not None and _SERVER_PROC.poll() is None:
            try:
                _SERVER_PROC.terminate()
                _SERVER_PROC.wait(timeout=3.0)
            except Exception:
                try:
                    _SERVER_PROC.kill()
                except Exception:
                    pass
        import os as _os
        _os._exit(0)


if __name__ == "__main__":
    main()


def _resolve_webview_storage_path(host: str = "127.0.0.1") -> str:
    """Compatibility alias for handset.gui.WindowApi users."""
    return _resolve_storage_path_for_host(host)
