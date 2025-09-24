#!/bin/bash
# iPhone Photo Manager - DEB Package Build Script v1.0.0
# Supports multi-language and theme functionalities

set -e

# Build configuration
PACKAGE_NAME="iphone-photo-manager"
VERSION="1.0.0"
PACKAGE_DIR="${PACKAGE_NAME}_${VERSION}"
PYTHON_SCRIPT="iphone_photo_manager_multilang.py"

echo "=== iPhone Photo Manager DEB Package Builder ==="
echo "Package: $PACKAGE_NAME"
echo "Version: $VERSION"
echo ""

# Check if main script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "ERROR: $PYTHON_SCRIPT not found!"
    echo "Please ensure the Python script is in the current directory."
    exit 1
fi

# Clean previous build
if [ -d "$PACKAGE_DIR" ]; then
    echo "Cleaning previous build..."
    rm -rf "$PACKAGE_DIR"
fi

echo "=== Creating package structure ==="
mkdir -p "$PACKAGE_DIR"
cd "$PACKAGE_DIR"

# Create directory structure
mkdir -p DEBIAN
mkdir -p usr/bin
mkdir -p usr/share/applications
mkdir -p usr/share/pixmaps
mkdir -p usr/share/iphone-photo-manager
mkdir -p usr/share/doc/iphone-photo-manager

echo "=== Creating control file ==="
cat > DEBIAN/control << 'EOF'
Package: iphone-photo-manager
Version: 1.0.0
Section: utils
Priority: optional
Architecture: all
Depends: python3 (>= 3.6), python3-gi, gir1.2-gtk-4.0, gir1.2-adw-1, gir1.2-gdkpixbuf-2.0, libimobiledevice-utils, ifuse
Maintainer: iPhone Photo Manager <https://github.com/dida-code>
Description: iPhone Photo Manager - GTK4 application for accessing iPhone photos
 A modern GTK4/LibAdwaita application for accessing and downloading photos
 from iPhone devices using libimobiledevice on Linux systems.
 .
 Features:
  * Automatic iPhone device detection
  * iPhone file system mounting
  * Photo browsing with preview panel
  * Batch download of selected photos
  * Multi-language support (Serbian/English)
  * Theme selection (dark/light)
  * Persistent settings
  * Modern GTK4/LibAdwaita interface
Homepage: https://github.com/dida-code/iphone-photo-manager.git
EOF

echo "=== Creating postinst script ==="
cat > DEBIAN/postinst << 'EOF'
#!/bin/bash
set -e

# Determine user to add to groups
if [ -n "$SUDO_USER" ]; then
    USER_TO_ADD="$SUDO_USER"
elif [ -n "$USER" ] && [ "$USER" != "root" ]; then
    USER_TO_ADD="$USER"
else
    # Find first non-root user
    USER_TO_ADD=$(getent passwd | awk -F: '$3>=1000 && $3<65534 {print $1; exit}')
fi

if [ -n "$USER_TO_ADD" ]; then
    echo "Adding user $USER_TO_ADD to plugdev and fuse groups..."
    usermod -a -G plugdev,fuse "$USER_TO_ADD" 2>/dev/null || true
    
    # Create config directory for settings
    echo "Creating config directory..."
    sudo -u "$USER_TO_ADD" mkdir -p "/home/$USER_TO_ADD/.config/iphone-photo-manager" 2>/dev/null || true
fi

# Create udev rules for iPhone
echo "Creating udev rules for iPhone..."
cat > /etc/udev/rules.d/39-libimobiledevice.rules << 'UDEV_EOF'
# iPhone/iPad udev rules for libimobiledevice
SUBSYSTEM=="usb", ATTR{idVendor}=="05ac", ATTR{idProduct}=="12a8", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="05ac", ATTR{idProduct}=="1281", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="05ac", ATTR{idProduct}=="1290", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="05ac", ATTR{idProduct}=="1292", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="05ac", ATTR{idProduct}=="1294", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="05ac", ATTR{idProduct}=="1297", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="05ac", ATTR{idProduct}=="129a", MODE="0666", GROUP="plugdev"
UDEV_EOF

# Reload udev rules
udevadm control --reload-rules || true
udevadm trigger || true

# Update desktop database
update-desktop-database || true

# Restart usbmuxd service
systemctl restart usbmuxd 2>/dev/null || service usbmuxd restart 2>/dev/null || true

echo ""
echo "=========================================="
echo "iPhone Photo Manager has been successfully installed!"
echo ""
echo "NEW FEATURES:"
echo "• Support for Serbian and English languages"
echo "• Theme selection (dark/light)"
echo "• Persistent settings"
echo ""
echo "NOTE: You may need to log out and"
echo "log back in for group permissions to take effect."
echo ""
echo "To launch the application:"
echo " - From the menu: Applications → Graphics → iPhone Photo Manager"
echo " - From the terminal: iphone-photo-manager"
echo ""
echo "To access settings, click the ⚙️ button"
echo "in the top-right corner of the application."
echo ""
echo "=========================================="
EOF
chmod 755 DEBIAN/postinst

echo "=== Creating prerm script ==="
cat > DEBIAN/prerm << 'EOF'
#!/bin/bash
set -e

echo "Removing iPhone Photo Manager..."

# Stop any running instances
pkill -f iphone_photo_manager_multilang.py || true

# Unmount any mounted iPhones
for user_home in /home/*; do
    if [ -d "$user_home/iphone_mount" ]; then
        fusermount -u "$user_home/iphone_mount" 2>/dev/null || true
        umount "$user_home/iphone_mount" 2>/dev/null || true
    fi
done

# Note: We do not delete config files to preserve user settings
EOF
chmod 755 DEBIAN/prerm

echo "=== Creating desktop file ==="
cat > usr/share/applications/iphone-photo-manager.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=iPhone Photo Manager
Name[sr]=iPhone Photo Manager
Comment=Access and download photos from iPhone devices
Comment[sr]=Pristup i preuzimanje fotografija sa iPhone uređaja
Exec=iphone-photo-manager
Icon=iphone-photo-manager
Terminal=false
StartupNotify=true
Categories=Graphics;Photography;Utility;System;
Keywords=iPhone;photos;mobile;device;sync;backup;theme;multilanguage;
MimeType=
StartupWMClass=iphone-photo-manager
EOF

echo "=== Creating launcher script ==="
cat > usr/bin/iphone-photo-manager << 'EOF'
#!/bin/bash
# iPhone Photo Manager Launcher Script

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Do not run iPhone Photo Manager as root!"
    echo "Use: iphone-photo-manager (without sudo)"
    exit 1
fi

# Check dependencies
MISSING_DEPS=""
command -v python3 >/dev/null || MISSING_DEPS="$MISSING_DEPS python3"
command -v idevice_id >/dev/null || MISSING_DEPS="$MISSING_DEPS libimobiledevice-utils"
command -v ifuse >/dev/null || MISSING_DEPS="$MISSING_DEPS ifuse"

if [ -n "$MISSING_DEPS" ]; then
    echo "Missing required packages:$MISSING_DEPS"
    echo "Install them with: sudo apt install$MISSING_DEPS"
    exit 1
fi

# Check if user is in required groups
if ! groups | grep -q plugdev; then
    echo "User is not in the 'plugdev' group."
    echo "Run: sudo usermod -a -G plugdev \$USER"
    echo "Then log out and log back in."
fi

# Set environment
export PYTHONPATH="/usr/share/iphone-photo-manager:$PYTHONPATH"

# Create config directory if it doesn't exist
mkdir -p "$HOME/.config/iphone-photo-manager"

# Change to app directory and run
cd /usr/share/iphone-photo-manager
exec python3 iphone_photo_manager_multilang.py "$@"
EOF
chmod 755 usr/bin/iphone-photo-manager

echo "=== Creating enhanced icon ==="
cat > usr/share/pixmaps/iphone-photo-manager.svg << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <!-- iPhone outline -->
  <rect x="14" y="4" width="20" height="36" rx="4" ry="4"
        fill="none" stroke="#333" stroke-width="2"/>
  
  <!-- Screen -->
  <rect x="16" y="8" width="16" height="24" rx="1" ry="1"
        fill="#87CEEB" stroke="#333" stroke-width="1"/>
  
  <!-- Home button -->
  <circle cx="24" cy="36" r="2" fill="none" stroke="#333" stroke-width="1"/>
  
  <!-- Photo icon on screen -->
  <rect x="18" y="12" width="12" height="8" rx="1" fill="#fff" opacity="0.8"/>
  <circle cx="21" cy="16" r="1.5" fill="#ffeb3b"/>
  <path d="m18 18 3-2 3 2 3-3 3 3v2h-12z" fill="#4caf50"/>
  
  <!-- Settings gear (to indicate settings availability) -->
  <g transform="translate(36, 10)">
    <circle cx="4" cy="4" r="6" fill="#666" opacity="0.7"/>
    <circle cx="4" cy="4" r="2.5" fill="none" stroke="#fff" stroke-width="1"/>
    <path d="M4 0 L4 2 M8 4 L6 4 M4 8 L4 6 M0 4 L2 4
             M6.8 1.2 L5.4 2.6 M6.8 6.8 L5.4 5.4
             M1.2 1.2 L2.6 2.6 M1.2 6.8 L2.6 5.4"
          stroke="#fff" stroke-width="1"/>
  </g>
  
  <!-- Language indicator (A/Ð) -->
  <text x="8" y="12" font-family="sans-serif" font-size="8" fill="#007acc" font-weight="bold">A</text>
  <text x="8" y="20" font-family="sans-serif" font-size="8" fill="#007acc" font-weight="bold">Ð</text>
  
  <!-- Theme indicator (sun/moon) -->
  <circle cx="40" cy="32" r="3" fill="#ffd700" opacity="0.8"/>
  <path d="M40 26 L40 28 M46 32 L44 32 M40 38 L40 36 M34 32 L36 32
           M43.5 28.5 L42.1 29.9 M43.5 35.5 L42.1 34.1
           M36.5 28.5 L37.9 29.9 M36.5 35.5 L37.9 34.1"
        stroke="#ffd700" stroke-width="1"/>
</svg>
EOF

# Create symbolic link for PNG fallback
ln -sf iphone-photo-manager.svg usr/share/pixmaps/iphone-photo-manager.png

echo "=== Copying main script ==="
if [ -f "../$PYTHON_SCRIPT" ]; then
    cp "../$PYTHON_SCRIPT" usr/share/iphone-photo-manager/
    echo "Copied: $PYTHON_SCRIPT"
else
    echo "WARNING: $PYTHON_SCRIPT not found!"
    echo "Please ensure the file is in the parent directory."
    exit 1
fi

echo "=== Creating documentation ==="
cat > usr/share/doc/iphone-photo-manager/README << 'EOF'
iPhone Photo Manager v1.0.0
============================

A modern GTK4/LibAdwaita application for accessing and downloading photos
from iPhone devices on Linux systems.

NEW FEATURES in v1.0.0:
------------------------------
• Support for Serbian and English languages
• Theme selection (dark/light)
• Persistent settings in ~/.config/iphone-photo-manager/
• Improved user interface
• Better error handling

INSTALLATION:
------------
The application is automatically installed via the .deb package.

LAUNCHING:
---------
- From the application menu: Applications → Graphics → iPhone Photo Manager
- From the terminal: iphone-photo-manager

USAGE:
-----
1. Connect your iPhone via USB cable
2. Unlock your iPhone and tap "Trust This Computer"
3. In the application, click "Mount"
4. Select the photos you want to download
5. Click "Download Selected"

SETTINGS:
--------
Click the ⚙️ button in the top-right corner of the application to access:
• Language selection (Serbian/English) - requires restart
• Theme selection (dark/light) - applies immediately

Settings are automatically saved in:
~/.config/iphone-photo-manager/settings.json

DEPENDENCIES:
------------
- python3 (>= 3.6)
- python3-gi
- gir1.2-gtk-4.0
- gir1.2-adw-1
- libimobiledevice-utils
- ifuse

TROUBLESHOOTING:
---------------
If the application cannot access the iPhone:

1. Check if the user is in the plugdev group:
   groups | grep plugdev

2. If not, add the user:
   sudo usermod -a -G plugdev $USER
   (then log out and log back in)

3. Restart the usbmuxd service:
   sudo systemctl restart usbmuxd

4. On the iPhone, go to Settings → General → Reset →
   Reset Location & Privacy, then trust the computer again

5. For issues with language or theme, delete the config file:
   rm ~/.config/iphone-photo-manager/settings.json

AUTHOR:
------
iPhone Photo Manager Team <developer@example.com>

LICENSE:
-------
GPL v3
EOF

cat > usr/share/doc/iphone-photo-manager/changelog << 'EOF'
iphone-photo-manager (1.0.0) stable; urgency=low

  * Initial release with multi-language and theme support
  * GTK4/LibAdwaita interface
  * iPhone device detection and mounting
  * Photo browsing with preview panel
  * Batch download functionality
  * Multi-language support (Serbian/English)
  * Theme selection (Dark/Light)
  * Settings persistence via JSON config
  * Improved error handling and user feedback
  * Enhanced icon with settings indicators

 -- iPhone Photo Manager Team <developer@example.com>  $(date -R)
EOF

cat > usr/share/doc/iphone-photo-manager/copyright << 'EOF'
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: iphone-photo-manager
Upstream-Contact: iPhone Photo Manager Team <developer@example.com>
Source: https://github.com/dida-code/iphone-photo-manager.git

Files: *
Copyright: 2025 iPhone Photo Manager Team <https://github.com/dida-code>
License: GPL-3+

License: GPL-3+
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 .
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.
 .
 You should have received a copy of the GNU General Public License
 along with this program. If not, see <https://www.gnu.org/licenses/>.
 .
 On Debian systems, the complete text of the GNU General
 Public License version 3 can be found in "/usr/share/common-licenses/GPL-3".
EOF

echo "=== Compressing documentation ==="
gzip -9 usr/share/doc/iphone-photo-manager/changelog

echo "=== Creating .deb package ==="
cd ..
dpkg-deb --build "$PACKAGE_DIR"

echo ""
echo "=========================================="
echo "DEB package created: ${PACKAGE_DIR}.deb"
echo ""
echo "NEW FEATURES:"
echo "• Multi-language support (Serbian/English)"
echo "• Theme selection (dark/light)"
echo "• Persistent settings"
echo "• Enhanced icon with indicators"
echo ""
echo "To install:"
echo "sudo dpkg -i ${PACKAGE_DIR}.deb"
echo "sudo apt-get install -f # to resolve dependency issues"
echo ""
echo "To test the package:"
echo "lintian ${PACKAGE_DIR}.deb"
echo ""
echo "=========================================="
