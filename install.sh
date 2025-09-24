#!/bin/bash
# iPhone Photo Manager - Installation Script

set -e

echo "=========================================="
echo "iPhone Photo Manager - Installation Script"
echo "=========================================="
echo ""

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    VERSION=$VERSION_ID
else
    echo "Cannot detect OS. Please install dependencies manually."
    exit 1
fi

echo "Detected OS: $OS"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please do not run this script as root!"
    echo "Run as normal user: ./install.sh"
    exit 1
fi

# Install system dependencies based on OS
echo "Installing system dependencies..."

case "$OS" in
    "ubuntu"|"debian"|"linuxmint"|"pop")
        echo "Installing dependencies for Ubuntu/Debian..."
        sudo apt update
        sudo apt install -y python3 python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 gir1.2-gdkpixbuf-2.0 libimobiledevice-utils ifuse dpkg-dev build-essential
        ;;
    "fedora"|"rhel"|"centos")
        echo "Installing dependencies for Fedora/RHEL..."
        sudo dnf install -y python3-gobject gtk4-devel libadwaita-devel libimobiledevice-utils fuse-ifuse rpm-build
        ;;
    "arch"|"manjaro")
        echo "Installing dependencies for Arch Linux..."
        sudo pacman -S --needed python-gobject gtk4 libadwaita libimobiledevice ifuse base-devel
        ;;
    "opensuse"|"opensuse-leap"|"opensuse-tumbleweed")
        echo "Installing dependencies for openSUSE..."
        sudo zypper install -y python3-gobject-Gdk typelib-1_0-Gtk-4_0 typelib-1_0-Adw-1 libimobiledevice-tools ifuse rpm-build
        ;;
    *)
        echo "Unsupported OS: $OS"
        echo "Please install dependencies manually:"
        echo "- python3 and python3-gi"
        echo "- GTK4 development files"
        echo "- LibAdwaita development files"
        echo "- libimobiledevice-utils"
        echo "- ifuse"
        exit 1
        ;;
esac

echo ""
echo "Dependencies installed successfully!"
echo ""

# Add user to required groups
echo "Adding user $USER to required groups..."
sudo usermod -a -G plugdev,fuse "$USER" 2>/dev/null || true

# Create config directory
echo "Creating configuration directory..."
mkdir -p "$HOME/.config/iphone-photo-manager"

# Check if we should build or install pre-built package
if [ -f "iphone-photo-manager_1.0.0.deb" ] && [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
    echo "Found pre-built DEB package, installing..."
    sudo dpkg -i iphone-photo-manager_1.0.0.deb || true
    sudo apt-get install -f -y
elif [ -f "build_deb.sh" ] && [ -f "iphone_photo_manager_multilang.py" ]; then
    echo "Building from source..."
    chmod +x build_deb.sh
    ./build_deb.sh
    
    # Install the built package
    if [ -f "iphone-photo-manager_1.0.0.deb" ]; then
        echo "Installing built package..."
        sudo dpkg -i iphone-photo-manager_1.0.0.deb || true
        sudo apt-get install -f -y
    else
        echo "Build failed!"
        exit 1
    fi
else
    echo "ERROR: Required files not found!"
    echo "Please ensure you have either:"
    echo "- A pre-built .deb package, OR"
    echo "- build_deb.sh and iphone_photo_manager_multilang.py files"
    exit 1
fi

# Create udev rules if not created by package
if [ ! -f "/etc/udev/rules.d/39-libimobiledevice.rules" ]; then
    echo "Creating udev rules for iPhone..."
    sudo tee /etc/udev/rules.d/39-libimobiledevice.rules > /dev/null << 'EOF'
# iPhone/iPad udev rules for libimobiledevice
SUBSYSTEM=="usb", ATTR{idVendor}=="05ac", ATTR{idProduct}=="12a8", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="05ac", ATTR{idProduct}=="1281", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="05ac", ATTR{idProduct}=="1290", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="05ac", ATTR{idProduct}=="1292", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="05ac", ATTR{idProduct}=="1294", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="05ac", ATTR{idProduct}=="1297", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="05ac", ATTR{idProduct}=="129a", MODE="0666", GROUP="plugdev"
EOF
    
    # Reload udev rules
    sudo udevadm control --reload-rules
    sudo udevadm trigger
fi

# Restart usbmuxd service
echo "Restarting usbmuxd service..."
sudo systemctl restart usbmuxd 2>/dev/null || sudo service usbmuxd restart 2>/dev/null || true

echo ""
echo "=========================================="
echo "Installation completed successfully!"
echo ""
echo "IMPORTANT: You need to log out and log back in"
echo "for group permissions to take effect."
echo ""
echo "To start the application:"
echo "- From menu: Applications → Graphics → iPhone Photo Manager"
echo "- From terminal: iphone-photo-manager"
echo ""
echo "First time setup:"
echo "1. Connect your iPhone via USB"
echo "2. Unlock iPhone and tap 'Trust This Computer'"
echo "3. Launch iPhone Photo Manager"
echo "4. Click 'Mount' to access photos"
echo ""
echo "If you encounter issues, check the README.md"
echo "for troubleshooting steps."
echo "=========================================="
