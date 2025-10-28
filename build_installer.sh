#!/bin/bash
set -e

echo "Building OfflineGeoLocator v1.0.0 Installer"
echo "==========================================="
echo ""

VERSION="1.0.0"
APP_NAME="OfflineGeoLocator"
BUNDLE_ID="com.offlinegeolocator.app"

# Paths
APP_PATH="installer/${APP_NAME}.app"
COMPONENT_PKG="installer/${APP_NAME}-Component-v${VERSION}.pkg"
DIST_XML="installer/Distribution.xml"
FINAL_PKG="${APP_NAME}-Installer-v${VERSION}.pkg"

# Check that app bundle exists
if [ ! -d "$APP_PATH" ]; then
    echo "Error: App bundle not found at $APP_PATH"
    exit 1
fi

# Check that executable exists
if [ ! -f "$APP_PATH/Contents/Resources/OfflineGeoLocator_executable" ]; then
    echo "Error: Executable not found in app bundle!"
    echo "Please copy the PyInstaller executable to:"
    echo "  $APP_PATH/Contents/Resources/OfflineGeoLocator_executable"
    exit 1
fi

echo "Step 1: Building component package..."
pkgbuild \
    --root "$APP_PATH" \
    --identifier "$BUNDLE_ID" \
    --version "$VERSION" \
    --install-location "/Applications/${APP_NAME}.app" \
    "$COMPONENT_PKG"

echo "✓ Component package created: $COMPONENT_PKG"
echo ""

echo "Step 2: Building distribution installer..."
productbuild \
    --distribution "$DIST_XML" \
    --package-path "installer" \
    --resources "installer" \
    "$FINAL_PKG"

echo "✓ Installer package created: $FINAL_PKG"
echo ""

# Show file size
SIZE=$(du -sh "$FINAL_PKG" | cut -f1)
echo "==========================================="
echo "✅ SUCCESS!"
echo "==========================================="
echo "Installer: $FINAL_PKG"
echo "Size: $SIZE"
echo ""
echo "Test it with: open $FINAL_PKG"
echo ""
