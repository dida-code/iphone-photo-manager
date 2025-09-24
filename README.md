# iPhone Photo Manager

A modern GTK4/LibAdwaita application for accessing and downloading photos from iPhone devices on Linux systems.

![iPhone Photo Manager Screenshot](screenshots/main-window.png)

## Features

- 📱 **Automatic iPhone device detection** - Automatically detects connected iPhone devices
- 💾 **iPhone file system mounting** - Mounts iPhone file system using libimobiledevice
- 🖼️ **Photo browsing with preview panel** - Browse photos with live preview
- 📥 **Batch download of selected photos** - Download multiple photos at once
- 🌐 **Multi-language support** - Serbian and English languages
- 🎨 **Theme selection** - Dark and light themes
- ⚙️ **Persistent settings** - Settings are saved automatically
- 🎯 **Modern GTK4/LibAdwaita interface** - Native Linux desktop experience

## Requirements

### System Dependencies
- Python 3.6 or newer
- GTK4 and LibAdwaita
- libimobiledevice-utils
- ifuse

### Ubuntu/Debian Installation
```bash
sudo apt update
sudo apt install python3 python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 gir1.2-gdkpixbuf-2.0 libimobiledevice-utils ifuse
```

### Fedora/RHEL Installation
```bash
sudo dnf install python3-gobject gtk4-devel libadwaita-devel libimobiledevice-utils fuse-ifuse
```

### Arch Linux Installation
```bash
sudo pacman -S python-gobject gtk4 libadwaita libimobiledevice ifuse
```

## Installation

### Option 1: Install DEB Package (Recommended for Debian/Ubuntu)

1. Download the latest `.deb` package from [Releases](https://github.com/dida-code/iphone-photo-manager.git/releases)
2. Install it:
   ```bash
   sudo dpkg -i iphone-photo-manager_1.0.0.deb
   sudo apt-get install -f  # Fix any dependency issues
   ```

### Option 2: Build from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/dida-code/iphone-photo-manager.git
   cd iphone-photo-manager
   ```

2. Build the DEB package:
   ```bash
   make build
   ```

3. Install the package:
   ```bash
   make install
   ```

### Option 3: Run Directly

If you prefer to run without installation:
```bash
python3 iphone_photo_manager_multilang.py
```

## Usage

1. **Connect your iPhone** via USB cable
2. **Unlock your iPhone** and tap "Trust This Computer" when prompted
3. **Launch the application**:
   - From the menu: Applications → Graphics → iPhone Photo Manager
   - From terminal: `iphone-photo-manager`
4. **Mount the device** by clicking the "Mount" button
5. **Browse folders** in the sidebar to see photo collections
6. **Select photos** you want to download
7. **Choose destination** folder
8. **Click "Download Selected"** to save photos to your computer

## Settings

Access settings by clicking the ⚙️ button in the top-right corner:

- **Language**: Switch between Serbian and English (requires restart)
- **Theme**: Choose between Dark and Light themes (applies immediately)

Settings are automatically saved to `~/.config/iphone-photo-manager/settings.json`

## Troubleshooting

### iPhone not detected

1. Check if user is in the `plugdev` group:
   ```bash
   groups | grep plugdev
   ```

2. If not, add user to the group:
   ```bash
   sudo usermod -a -G plugdev $USER
   ```
   Then log out and log back in.

3. Restart the usbmuxd service:
   ```bash
   sudo systemctl restart usbmuxd
   ```


### Mount failures

For persistent mount failures:
1. Try different USB ports/cables
2. Restart iPhone
3. Restart computer
4. Check system logs: `journalctl -u usbmuxd`

## Development

### Building

```bash
# Build DEB package
make build

# Build and test
make all

# Clean build files
make clean

# Show help
make help
```

### Testing

```bash
# Test with lintian
make test

# Install in development mode
make dev-install
```



## Acknowledgments

- [libimobiledevice](https://libimobiledevice.org/) - For iPhone communication
- [GTK](https://gtk.org/) and [LibAdwaita](https://gnome.pages.gitlab.gnome.org/libadwaita/) - For the user interface
- [ifuse](https://github.com/libimobiledevice/ifuse) - For iPhone file system access


---

**Note**: This application requires your iPhone to be in a trusted state. Always ensure you trust only computers you own and control.
