# iPhone Link for Linux

<p align="center">
  <img src="assets/logo.png" width="180" height="180" alt="iPhone Link logo" style="border-radius: 40px; box-shadow: 0 16px 36px rgba(0, 120, 212, 0.35);">
</p>

<h1 align="center">📱🔗 iPhone Link</h1>

<p align="center">
  <a href="https://github.com/fazrigading"><img src="https://img.shields.io/badge/Author-Fazri%20Gading%20(%40fazrigading)-4F46E5?style=flat-square&logo=github" alt="Author: Fazri Gading"></a>
  <a href="https://github.com/kelvindaniyar/iphone-link"><img src="https://img.shields.io/badge/Forked%20from-kelvindaniyar%2Fiphone--link-blue?style=flat-square&logo=github" alt="Forked from kelvindaniyar"></a>
  <a href="https://github.com/teyboxv1/pane-iphone-mirror-windows"><img src="https://img.shields.io/badge/Upstream-teyboxv1%2Fpane--iphone--mirror--windows-blue?style=flat-square&logo=github" alt="Forked from teyboxv1"></a>
  <img src="https://img.shields.io/badge/License-GPL--3.0-green.svg?style=flat-square" alt="License: GPL-3.0">
  <img src="https://img.shields.io/badge/Verified%20OS-Fedora%20x86__64-0078D4.svg?style=flat-square&logo=linux" alt="Verified OS: Fedora x86_64">
</p>

### Tested Linux Environment
- 🐧 **Linux**: **x86_64 desktop** (Python runtime + pywebview window; see Linux notes below)
  - Audio sink (streaming iPhone audio to the PC) is Windows-only; Linux supports PC volume control only.
- Tested by **Fazri Gading** (`@fazrigading`) on **Fedora Linux 44 (Workstation Edition)**, kernel `7.2.13-200.fc44.x86_64`.
- Test device: **iPhone XS** running **iOS 18.7.11**. 
- Note: Screen streaming could not be tested because the stream requires **iOS 27+**; USB device detection, `usbmuxd` integration, and the Linux GUI window were verified.

---

### 🌟 Author, Attribution & Open-Source Lineage

- **Author & Maintainer (Linux Port)**: **Fazri Gading** ([GitHub `@fazrigading`](https://github.com/fazrigading))
- **Previous Authors & Lineage**:
  - **Kelvin Daniyar** ([GitHub `@kelvindaniyar`](https://github.com/kelvindaniyar)) - Original creator of [iPhone Link](https://github.com/kelvindaniyar/iphone-link), licensed under the GNU General Public License v3.0 (GPL-3.0).
  - **teyboxv1** ([GitHub `@teyboxv1`](https://github.com/teyboxv1)) - Creator of foundational upstream project [pane-iphone-mirror-window*](https://github.com/teyboxv1/pane-iphone-mirror-windows), licensed under the GNU General Public License v3.0 (GPL-3.0).
  - **Doron Zavelevsky** ([GitHub `@doronz88`](https://github.com/doronz88)) - Creator of [pymobiledevice3](https://github.com/doronz88/pymobiledevice3) for establishing the foundational USB RemoteXPC tunneling mechanism.

---

## 🚀 Key Features Overview

| Feature | Description |
| :--- | :--- |
| **🪟 Native frameless UI** | Compact frameless window with a collapsible settings side drawer. Windows uses the WinUI-style Liquid Glass frontend; Linux uses a native pywebview window with the same web UI. |
| **⚡ 60fps Zero-Delay Mirroring** | Ultra-responsive 60fps video stream over USB cable, powered by hardware-accelerated HEVC (H.265) decoding and WebCodecs. |
| **🌑 Mac-Style Stealth Dim Mode** | Remotely dims the physical iPhone OLED display down to **0% brightness (completely dark on your desk)** while mirroring remains 100% bright on your PC. |
| **💡 Calibrated ~25% Brightness Restore** | Restores the physical iPhone display to exactly **4 single iOS bars (~25% brightness)** on exit or stealth toggle, with strict guards preventing 100% brightness surges. |
| **🎮 Landscape Gaming Mode (`Alt+H`)** | Full 90°/270° canvas rotation with dynamic aspect-ratio adaptation (19.5:9 widescreen), inverse touch mapping matrix for landscape games (*eFootball*, *Genshin Impact*, *Call of Duty*), and maximized PC monitor viewing. |
| **🔓 Remote Wake &amp; Auto-PIN Unlock** | Wakes your iPhone screen, executes an automated swipe-up, bypasses the Face ID scanning delay on newer devices (iPhone 16/17 Pro), and injects your PIN via isolated HID keycodes. |
| **🔒 Remote Screen Lock (`Alt+L`)** | Instantly puts your physical iPhone into standby sleep with one keystroke or UI button. |
| **📋 Bidirectional Smart OCR Copy-Paste** | High-precision OCR for **Apple Notes** and **Google Keep**: repairs split words (`Cut-Off`), neutralizes selection handles, stitches multi-screen captions, and copies text directly to your system clipboard. |
| **⌨️ Direct PC-to-iPhone Paste (`Alt+V`)** | Pastes text from your system clipboard directly into the focused iOS text field via raw HID keystroke simulation. |
| **🧹 Smart Auto-Clear Cache** | Automatically flushes OCR stitching memory whenever you return Home, switch apps, or press Back, preventing cross-app text contamination. |
| **🖱️ 2-Finger Trackpad &amp; Smooth Scroll** | Natural precision scrolling with mouse wheel and laptop trackpads. |
| **🔊 Zero-Stutter Bluetooth Audio Sink** | On Windows, stream iPhone media audio (TikTok, YouTube, Spotify) directly into PC speakers or headphones with EcoQoS anti-throttling, 1ms multimedia timer scheduling, and radio-safe polling. |
| **📥 System Tray &amp; Low RAM** | System tray icon with Show/Hide and quick actions, plus automatic working-set trimming so mirroring &amp; audio run lightweight in the background. |

> **Platform note**: Some features are Windows-first because they depend on Windows-only stack pieces (for example the WinUI-style frontend and Windows audio sink). The Linux build reuses the same backend and web UI, with Linux-native window, clipboard, and tray integration where available.

---

## ⌨️ Keyboard Shortcuts Reference

iPhone Link provides intuitive keyboard shortcuts mapped for maximum productivity:

| Shortcut | Action | Description |
| :---: | :--- | :--- |
| **`Alt + H`** | **🔄 Toggle Landscape Mode** | Switches instantly between Vertical Portrait (0°) and Horizontal Landscape (270° eFootball Gaming Mode). |
| **`Alt + C`** | **📥 Copy iPhone Text** | Runs Smart OCR on the selected iPhone screen region and copies clean text to your system clipboard (`✓ Copied to PC!`). |
| **`Alt + V`** | **📋 Paste PC Text** | Injects text from your system clipboard into the active iPhone app as native keystrokes. |
| **`Alt + R`** | **🧹 Clear Copy Cache** | Flushes OCR session chunk memory manually (`✓ Cache Cleared!`). |
| **`Alt + D`** | **🌑 Toggle Stealth Dim** | Switches physical iPhone display between 0% (Stealth Dim) and calibrated ~25% brightness. |
| **`Alt + U`** | **🔓 Remote Wake &amp; Unlock** | Wakes iPhone, swipes up, bypasses Face ID delay, and inputs PIN. |
| **`Alt + L`** | **🔒 Lock iPhone Screen** | Safely restores brightness if dimmed, then puts iPhone to sleep. |
| **`Ctrl + K`** | **⌨️ Toggle On-Screen Keyboard** | Shows / hides the iOS virtual software keyboard. |
| **`Ctrl + C`** | **Internal iOS Copy** | Instant internal copy within iOS apps without triggering system OCR. |
| **`Ctrl + V`** | **Internal iOS Paste** | Instant native iOS paste preserving all internal rich formatting. |
| **`Ctrl + A`** | **Select All** | Selects all text in the focused iOS field. |
| **`Ctrl + Z`** | **Undo** | Reverses the last text action in iOS. |

---

## 📦 Quick Start Guide

### 📋 Prerequisites & iPhone Setup (Persyaratan Sistem & Konfigurasi iPhone)

#### 1. PC Requirements
- **Operating System**: Windows 10/11 26H2 (64-bit) **or** a Linux x86_64 desktop with Python and a supported GUI environment.
- **Apple USB Drivers (Windows)**: Install the official **[Apple Devices](https://apps.microsoft.com/detail/9np83lwlpz9k)** app (or iTunes) from the Microsoft Store so Windows can recognize the *Apple Mobile Device* USB driver.
- **USB Connection**: A working iPhone USB cable. Mirroring and control are USB-based, not Wi-Fi-based.

#### 2. iPhone Configuration (Wajib Mengaktifkan Developer Mode)
Before running iPhone Link, you **MUST** enable **Developer Mode** on the iPhone:
- Connect the iPhone to the PC using a USB data cable.
- On the iPhone, tap **Trust This Computer** and enter your lock-screen PIN.
- Open **Settings → Privacy & Security → Developer Mode**.
- Slide the toggle to **ON**. The iPhone will ask to restart.
- After the iPhone restarts, unlock it, tap **Turn On** on the confirmation pop-up, then enter your PIN once more.

---

> ### 💡 Tips Khusus: Cara Memunculkan Menu Developer Mode yang Tersembunyi via 3uTools
> *(How to Reveal Hidden Developer Mode Menu on iPhone via 3uTools)*
>
> **Kendala / Problem**:  \n> Pada iPhone baru atau iPhone yang belum pernah disambungkan ke Mac / Xcode, Apple secara default **menyembunyikan menu "Mode Pengembang (Developer Mode)"** di dalam *Pengaturan → Privasi & Keamanan*.
>
> **Solusi Cepat 1-Menit (Bahasa Indonesia)**:
> 1. Unduh dan pasang aplikasi gratis **[3uTools](https://www.3u.com/)** di PC Windows Anda.
> 2. Hubungkan iPhone ke PC via kabel USB dan ketuk *Trust This Computer* (Percayai Komputer Ini).
> 3. Buka 3uTools, lalu masuk ke tab menu **Toolbox → Realtime Screen**.
> 4. Begitu jendela *Realtime Screen* terbuka, layanan Apple Developer Service secara otomatis diinisialisasi pada iPhone Anda, dan menu **Mode Pengembang (Developer Mode)** akan **seketika muncul secara ajaib** di iPhone pada:  \n>    **Pengaturan → Privasi & Keamanan → Mode Pengembang** (di bagian paling bawah).
> 5. Buka menu tersebut di iPhone, geser ke posisi **Nyalakan (ON)**, lalu restart iPhone Anda. Setelah restart, tekan *Turn On* dan masukkan PIN layar kunci. Anda sekarang 100% siap menggunakan iPhone Link!
>
> ---
>
> **English Quick Guide**: *By default, iOS hides the Developer Mode toggle under Settings → Privacy & Security on devices that have never been connected to Xcode or a developer environment.*
> 1. Download and install **[3uTools](https://www.3u.com/)** on your Windows PC.  \n> 2. Connect your iPhone via USB cable and tap *Trust This Computer*.
> 3. In 3uTools, navigate to **Toolbox → Realtime Screen**.
> 4. As soon as *Realtime Screen* launches, it mounts the developer disk image, and the hidden **Developer Mode** toggle will **instantly appear** at the bottom of:  \n>    **Settings → Privacy & Security → Developer Mode**.
> 5. Toggle it **ON**, allow your iPhone to reboot, and tap *Turn On* upon restart. iPhone Link is now 100% ready to mirror!

---

### Option 1A: Standalone Windows EXE (Recommended — Zero Python Required!)
1. Download **`iPhone-Link-Win64-Standalone-EXE-v1.0.0.zip`** from [**Releases**](../../releases/latest).
2. Extract the ZIP archive anywhere on your PC (e.g., `D:\iPhone-Link`).
3. *(Optional 1-Click)* Double-click **`Create-Desktop-Shortcut.bat`** to generate a Desktop and Start Menu shortcut pointing directly to **`iPhone Link.exe`** with the official app icon!
4. Double-click **`iPhone Link.exe`** to launch immediately — **no Python installation required!**
5. Click **Start mirroring** and enjoy 60fps low-latency control!

### Option 1B: Lightweight Smart-Portable Release (`iPhone-Link-Portable-v1.0.0.zip`)
1. Download **`iPhone-Link-Portable-v1.0.0.zip`** from [**Releases**](../../releases/latest) and extract it anywhere on your PC.
2. Double-click **`iPhone Link.bat`** (silent mode) or **`run.bat`** (console diagnostic mode).
3. **Automatic First-Time Setup (Hanya 1x Saja)**: On the very first launch in a new folder, the Smart Auto-Bootstrapping Launcher automatically builds a local `venv` and installs `pywebview` & `pymobiledevice3` (and offers 1-click `winget` Python 3.12 installation if Python is missing). Every launch after that opens in **< 1 second with 0% console windows!**
4. *(Optional 1-Click)* Double-click **`Create-Desktop-Shortcut.bat`** to generate a Desktop and Start Menu shortcut with the official app icon!

---

### Run from Source (Linux)
```bash
# 1. Clone repository
git clone https://github.com/fazrigading/iphone-link-linux.git
cd iphone-link-linux

# 2. Set up Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Make the launcher executable
chmod +x run.sh

# 5. Launch iPhone Link
./run.sh
# (or run via: python3 -m handset)
```

If the GUI does not start, make sure your Linux session has access to a display/server and that `python3 -c "import webview"` works in the same environment.

Linux (source run) also needs the system packages that pip cannot install:
```bash
# Fedora
sudo dnf install python3-gobject webkit2gtk4.1 usbmuxd libimobiledevice ifuse xclip wl-clipboard
# Debian / Ubuntu
sudo apt install python3-gi gir1.2-webkit2-4.1 usbmuxd libimobiledevice6 ifuse xclip wl-clipboard
# Arch Linux
sudo pacman -S python-gobject webkit2gtk usbmuxd libimobiledevice ifuse xclip wl-clipboard
```
iPhone Link uses pywebview's GTK backend on Linux, which depends on the system PyGObject + WebKit2GTK.

---

### 🔒 Privacy & Clean Uninstall

Privasi dan kendali data Anda adalah prioritas mutlak iPhone Link:
- **Hapus Bersih dari UI**: Di dalam menu Pengaturan (Side Drawer) bagian *iPhone Screen & Stealth Control*, klik tombol **`🗑️ Clear Saved PIN & Privacy Data`** untuk menghapus instan PIN dari memori browser, riwayat viewport, dan file log lokal.
- **1-Klik Clean Uninstaller (`Uninstall-iPhone-Link.bat`)**: Ingin menghapus total iPhone Link dari PC Anda? Cukup klik 2x script **`Uninstall-iPhone-Link.bat`** di dalam folder rilis. Script ini otomatis:
  1. Menghentikan semua proses latar belakang iPhone Link.
  2. Menghapus tuntas seluruh cache WebView2 / `pywebview` (termasuk PIN `localStorage`).
  3. Menghapus riwayat ketik lokal, pengaturan, dan cache OCR.
  4. Menghapus shortcut Desktop dan Start Menu Windows.
  5. Memberikan opsi konfirmasi untuk menghapus seluruh folder aplikasi dari harddisk.

---

## 🐧 Linux Notes

- The Linux frontend is a native windowedpywebview app that reuses the same iPhone Link backend and web UI.
- Linux builds are **source-based for now**: run `./run.sh` from a checkout, or run `python3 -m handset`.
- Linux-specific helpers live in `handset/`:
  - `handset/main.py` — entry point
  - `handset/gui.py` — window + JS bridge
  - `handset/clipboard.py` — clipboard helpers
  - `handset/audio.py` — audio manager

---

## 🛠️ Architecture & Under the Hood

iPhone Link establishes a secure, local-only communication pipeline between your PC and iPhone:

```
┌─────────────────┐        USB Cable (RemoteXPC / RSD Tunnel)       ┌────────────────────────┐
│  iPhone Device  │ ◄─────────────────────────────────────────────► │ iPhone Link App        │
│  (iOS 17 - 27+) │   • 60fps HEVC Video Stream (Port 62078)        │ (In-Process GUI+Server)│
└─────────────────┘   • Direct HID Multi-Touch & Keystrokes         │ • 127.0.0.1:8765 HTTP  │
                      • Consumer Page Display Brightness / Power    │ • WebView / WebCodecs  │
                                                                    └────────────────────────┘
```

1. **In-Process Unified Architecture**: The local HTTP backend server runs in-process with the UI—eliminating separate console server windows and orphaned background processes on exit.
2. **RSD / RemoteXPC Tunneling**: Uses `pymobiledevice3` to securely establish a CoreDevice tunnel over USB.
3. **Hardware HEVC Decoding**: Streams raw H.265 NAL units directly to the browser's WebCodecs video decoder, eliminating frame lag.
4. **Isolated Direct HID Injection**: Passes mouse clicks as capacitive touch points (`0..32768`) and keyboard strokes through USB HID Consumer and Keyboard usage pages.
5. **Local Privacy**: 100% of video streaming, OCR computation, and keyboard inputs stay on your local machine (`127.0.0.1`). No cloud telemetry or third-party servers are ever contacted.

---

## 📄 License & Credits

- **Author & Maintainer (Linux Port)**: [**Fazri Gading @fazrigading**](https://github.com/fazrigading).
- **Previous Authors & Credits**:
  - [**Kelvin Daniyar**](https://github.com/kelvindaniyar) - Original [iPhone Link](https://github.com/kelvindaniyar/iphone-link) author.
  - [**teyboxv1**](https://github.com/teyboxv1) - Upstream [Pane: iPhone Mirror on Windows](https://github.com/teyboxv1/pane-iphone-mirror-windows) project author.
  - [**Doron Zavelevsky (`doronz88`)**](https://github.com/doronz88) - Core library [pymobiledevice3](https://github.com/doronz88/pymobiledevice3).
- **License**: GNU General Public License v3.0 ([GPL-3.0](LICENSE)).
