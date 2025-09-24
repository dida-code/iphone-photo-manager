# iPhone Photo Manager - Makefile for creating DEB package

PACKAGE_NAME = iphone-photo-manager
VERSION = 1.0.0
PACKAGE_DIR = $(PACKAGE_NAME)_$(VERSION)
DEB_FILE = $(PACKAGE_DIR).deb

# Build variables
PYTHON_SCRIPT = iphone_photo_manager_multilang.py
BUILD_DIR = build
DIST_DIR = dist

.PHONY: all clean build install test package help debug info extract list

help:
	@echo "iPhone Photo Manager - Build System"
	@echo "=================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make build     - Create DEB package"
	@echo "  make install   - Install package locally"
	@echo "  make test      - Test package with lintian"
	@echo "  make clean     - Delete build files"
	@echo "  make package   - Alias for build"
	@echo "  make all       - Build + test"
	@echo "  make debug     - Show build variables"
	@echo "  make info      - Show package information"
	@echo "  make extract   - Extract package contents"
	@echo "  make list      - List package contents"
	@echo "  make help      - Show this help"

all: build test

build: check-deps
	@echo "Building DEB package using build script..."
	@chmod +x build_deb.sh
	@./build_deb.sh

install: $(DEB_FILE)
	@echo "Installing package..."
	sudo dpkg -i $(DEB_FILE) || true
	sudo apt-get install -f -y
	@echo "Package installed!"

test: $(DEB_FILE)
	@echo "Testing package with lintian..."
	@if command -v lintian >/dev/null 2>&1; then \
		lintian $(DEB_FILE); \
	else \
		echo "lintian not installed. Install with: sudo apt install lintian"; \
	fi

clean:
	@echo "Cleaning build files..."
	@rm -rf $(PACKAGE_DIR)
	@rm -f $(DEB_FILE)
	@rm -rf $(BUILD_DIR) $(DIST_DIR)
	@rm -rf extracted/
	@echo "Clean completed!"

check-deps:
	@echo "Checking build dependencies..."
	@command -v dpkg-deb >/dev/null || (echo "dpkg-deb not available!"; exit 1)
	@test -f $(PYTHON_SCRIPT) || (echo "$(PYTHON_SCRIPT) does not exist!"; exit 1)
	@test -f build_deb.sh || (echo "build_deb.sh does not exist!"; exit 1)
	@echo "All dependencies are available."

package: build

# Debug and information targets
debug: 
	@echo "Debug information:"
	@echo "PACKAGE_NAME: $(PACKAGE_NAME)"
	@echo "VERSION: $(VERSION)" 
	@echo "PACKAGE_DIR: $(PACKAGE_DIR)"
	@echo "DEB_FILE: $(DEB_FILE)"
	@echo "PYTHON_SCRIPT: $(PYTHON_SCRIPT)"

info:
	@if [ -f $(DEB_FILE) ]; then \
		echo "Package information:"; \
		dpkg-deb -I $(DEB_FILE); \
	else \
		echo "DEB package does not exist. Run 'make build' first."; \
	fi

extract:
	@if [ -f $(DEB_FILE) ]; then \
		echo "Extracting package contents..."; \
		dpkg-deb -x $(DEB_FILE) extracted/; \
		echo "Contents extracted to extracted/"; \
	else \
		echo "DEB package does not exist."; \
	fi

list:
	@if [ -f $(DEB_FILE) ]; then \
		echo "Package contents:"; \
		dpkg-deb -c $(DEB_FILE); \
	else \
		echo "DEB package does not exist."; \
	fi

# Development targets
dev-install: build
	@echo "Installing in development mode..."
	@sudo dpkg -i $(DEB_FILE) --force-overwrite || true
	@sudo apt-get install -f -y

dev-remove:
	@echo "Removing development installation..."
	@sudo dpkg -r $(PACKAGE_NAME) || true

# GitHub release preparation
github-release: clean build test
	@echo "Preparing for GitHub release..."
	@mkdir -p release/
	@cp $(DEB_FILE) release/
	@echo "Release files prepared in release/ directory"

# Quick development cycle
dev: clean build dev-install
	@echo "Development cycle complete!"
