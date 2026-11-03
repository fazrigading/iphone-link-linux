<p align="center">
  <img src="assets/logo.png" width="180" height="180" alt="iPhone Link logo" style="border-radius: 40px; box-shadow: 0 16px 36px rgba(0, 120, 212, 0.35);">
</p>

<h1 align="center">📱🔗 iPhone Link: Native iPhone Mirroring & Control for Linux</h1>

<p align="center">
  <a href="https://github.com/fazrigading"><img src="https://img.shields.io/badge/Author-Fazri%20Gading%20(%40fazrigading)-4F46E5?style=flat-square&logo=github" alt="Author: Fazri Gading"></a>
  <a href="https://github.com/kelvindaniyar/iphone-link"><img src="https://img.shields.io/badge/Forked%20from-kelvindaniyar%2Fiphone--link-blue?style=flat-square&logo=github" alt="Forked from kelvindaniyar"></a>
  <a href="https://github.com/teyboxv1/pane-iphone-mirror-windows"><img src="https://img.shields.io/badge/Upstream-teyboxv1%2Fpane--iphone--mirror--windows-blue?style=flat-square&logo=github" alt="Forked from teyboxv1"></a>
  <a href="https://github.com/fazrigading/iphone-link-linux/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-GPL--3.0-green.svg?style=flat-square" alt="License: GPL-3.0"></a>
  <img src="https://img.shields.io/badge/Verified%20OS-Fedora%20x86__64-0078D4.svg?style=flat-square&logo=linux" alt="Verified OS: Fedora x86_64">
</p>

**For full Indonesian documentation, see [README.id.md](README.id.md)**

## Overview

**iPhone Link** mirrors an iPhone screen to a Linux desktop over USB, provides low‑latency control, and enables bidirectional copy‑paste. 

> [!NOTE]
> The Linux port reuses the original backend and web UI while replacing Windows‑specific window, clipboard, and tray integrations with native Linux equivalents.

## Features

- **💻️ Native frameless UI** – pywebview GTK window with collapsible side drawer.
- **⚡ 60 fps zero‑delay mirroring** – hardware‑accelerated HEVC decoding via WebCodecs.
- **🌑 Stealth dim mode** – dim iPhone display to 0 % while keeping PC view bright.
- **🎮️ Landscape gaming mode** – rotate canvas for optimal gaming.
- **🔓 Remote wake & unlock** – wake iPhone, bypass Face ID, inject PIN.
- **📋 Smart OCR copy‑paste** – extract text from iPhone apps, copy to PC clipboard.
- **⌨️ PC‑to‑iPhone paste** – inject system clipboard into iPhone.
- **📥 System tray icon** – quick actions, auto‑trim working set.

## Installation

### Prerequisites
- Python ≥ 3.9
- System packages (choose your distro):
  - **Fedora**: 
    ```bash
    sudo dnf install python3-gobject webkit2gtk4.1 usbmuxd libimobiledevice libimobiledevice-utils ifuse xclip wl-clipboard
    ```
  - **Debian/Ubuntu**:
    ```bash
    sudo apt install python3-gi gir1.2-webkit2-4.1 usbmuxd libimobiledevice6 libimobiledevice-utils ifuse xclip wl-clipboard
    ```
  - **Arch**:
    ```bash
    sudo pacman -S python-gobject webkit2gtk usbmuxd libimobiledevice libimobiledevice-utils ifuse xclip wl-clipboard
    ```
- iPhone with **Developer Mode** enabled and trusted by the host PC.
  - To enable Developer Mode on iOS 16+, go to **Settings -> Privacy & Security -> Developer Mode** and toggle it on, then restart the device when prompted.
  - If you **don't see** the Developer Mode option, you can enable it by using the `idevicepair` command from the `libimobiledevice-utils` package:
  ```bash
  idevicepair pair
  ```


### Quick install from source
```bash
git clone https://github.com/fazrigading/iphone-link-linux.git
cd iphone-link-linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
chmod +x run.sh
./run.sh   # or: python -m handset
```

## Usage

- Launch with `./run.sh` or `python -m handset`.
- Keyboard shortcuts (see **Keyboard Shortcuts** section in the UI) expose core actions such as landscape mode (`Alt+H`), copy (`Alt+C`), paste (`Alt+V`), and dim toggle (`Alt+D`). 

> [!NOTE]
> Full list of shortcuts is available in the **Keyboard Shortcuts** section of the app's side drawer or see the [shortcuts reference](docs/shortcuts.md).

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make changes, ensuring `python -m py_compile handset/*.py` passes.
4. Open a Pull Request with a concise description.

## Credits

- **Author & Maintainer (Linux Port)**: Fazri Gading - <https://github.com/fazrigading/iphone-link-linux>
- **Original Author (Windows)**: Kelvin Daniyar (`iphone-link`) - <https://github.com/kelvindaniyar/iphone-link>
- **Upstream Project**: Abdulrahman Ali (`pane`) - <https://github.com/teyboxv1/pane-iphone-mirror-windows>
- **Core Library**: Doron Zavelevsky (`pymobiledevice3`) - <https://github.com/doronz88/pymobiledevice3>

## License

GPL‑3.0 – see [LICENSE](LICENSE).