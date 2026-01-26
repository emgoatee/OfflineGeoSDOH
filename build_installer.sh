#!/bin/bash
set -e

VERSION="1.1.2"
APP_NAME="Offline GEO-SDOH"
BUNDLE_ID="com.offlinegeolocator.app"

echo "Building $APP_NAME v$VERSION Installer"
echo "==========================================="
echo ""

# Paths
APP_PATH="installer/${APP_NAME}.app"
COMPONENT_PKG="installer/OfflineGeoLocator-Component-v${VERSION}.pkg"
DIST_XML="installer/Distribution.xml"
FINAL_PKG="OfflineGeoLocator-Installer-v${VERSION}.pkg"

# Load credentials from .env if it exists
if [ -f ".env" ]; then
    echo "🔑 Loading signing credentials from .env..."
    # Use allexport to export all variables in the sourced file
    set -a
    source .env
    set +a
else
    echo "⚠️  No .env file found. Skipping signing and notarization."
fi

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

# --- Step 1: Sign the App Bundle ---
if [ ! -z "$APPLE_SIGNING_IDENTITY" ]; then
    echo "Step 1: Signing app bundle..."
    # Sign all nested binaries, frameworks, and dylibs
    find "$APP_PATH" -type f \( -name "*.dylib" -o -name "*.so" -o -name "OfflineGeoLocator_executable" \) -exec codesign --force --options runtime --entitlements entitlements.plist --sign "$APPLE_SIGNING_IDENTITY" --timestamp {} +
    
    # Sign the main bundle
    codesign --force --options runtime --entitlements entitlements.plist --sign "$APPLE_SIGNING_IDENTITY" --timestamp "$APP_PATH"
    
    echo "✓ App bundle signed."
    echo ""
fi

# --- Step 2: Build and Sign Component Package ---
echo "Step 2: Building component package..."
PKG_SIGNED=false
if [ ! -z "$APPLE_INSTALLER_IDENTITY" ]; then
    if pkgbuild \
        --root "$APP_PATH" \
        --identifier "$BUNDLE_ID" \
        --version "$VERSION" \
        --install-location "/Applications/${APP_NAME}.app" \
        --sign "$APPLE_INSTALLER_IDENTITY" \
        "$COMPONENT_PKG"; then
        PKG_SIGNED=true
        echo "✓ Component package signed."
    else
        echo "⚠️  Failed to sign component package. Building unsigned version..."
        pkgbuild \
            --root "$APP_PATH" \
            --identifier "$BUNDLE_ID" \
            --version "$VERSION" \
            --install-location "/Applications/${APP_NAME}.app" \
            "$COMPONENT_PKG"
    fi
else
    pkgbuild \
        --root "$APP_PATH" \
        --identifier "$BUNDLE_ID" \
        --version "$VERSION" \
        --install-location "/Applications/${APP_NAME}.app" \
        "$COMPONENT_PKG"
fi
echo "✓ Component package created."
echo ""

# --- Step 3: Build and Sign Distribution Installer ---
echo "Step 3: Building distribution installer..."
if [ "$PKG_SIGNED" = true ]; then
    productbuild \
        --distribution "$DIST_XML" \
        --package-path "installer" \
        --resources "installer" \
        --sign "$APPLE_INSTALLER_IDENTITY" \
        "$FINAL_PKG"
    echo "✓ Installer package signed."
else
    echo "🔨 Building unsigned PKG (Installer certificate missing)..."
    productbuild \
        --distribution "$DIST_XML" \
        --package-path "installer" \
        --resources "installer" \
        "$FINAL_PKG"
fi
echo "✓ Installer package created."
echo ""

# --- Step 3.5: Create ZIP for fallback ---
FINAL_ZIP="OfflineGeoLocator-v${VERSION}-macOS.zip"
echo "Step 3.5: Creating ZIP for backup distribution..."
# We zip the .app bundle
cd installer
zip -r "../$FINAL_ZIP" "${APP_NAME}.app"
cd ..
echo "✓ ZIP created: $FINAL_ZIP"
echo ""

# --- Step 4: Notarization ---
if [ ! -z "$APPLE_ID" ] && [ ! -z "$APPLE_PASSWORD" ] && [ ! -z "$APPLE_TEAM_ID" ]; then
    echo "Step 4: Submitting for notarization..."
    
    # We notarize the ZIP (this covers the .app inside)
    # If the PKG was signed, we notarize that too. 
    # Notarizing the ZIP is standard for .app distribution.
    
    SUBMISSION_FILE="$FINAL_ZIP"
    if [ "$PKG_SIGNED" = true ]; then
        SUBMISSION_FILE="$FINAL_PKG"
        echo "Notarizing the signed PKG..."
    else
        echo "Notarizing the ZIP (since PKG is unsigned)..."
    fi

    xcrun notarytool submit "$SUBMISSION_FILE" \
        --apple-id "$APPLE_ID" \
        --password "$APPLE_PASSWORD" \
        --team-id "$APPLE_TEAM_ID" \
        --wait
    
    echo "✓ Notarization successful!"
    echo ""
    
    echo "Step 5: Stapling notarization tickets..."
    if [ "$PKG_SIGNED" = true ]; then
        xcrun stapler staple "$FINAL_PKG"
        echo "✓ Ticket stapled to PKG."
    fi
    
    # Also staple to the .app so it works when extracted from ZIP
    xcrun stapler staple "$APP_PATH"
    echo "✓ Ticket stapled to .app bundle."
    
    # Re-zip the stapled app
    echo "Re-zipping stapled app..."
    rm "$FINAL_ZIP"
    cd installer
    zip -r "../$FINAL_ZIP" "${APP_NAME}.app"
    cd ..
    echo "✓ Final notarized ZIP ready."
    echo ""
fi

# Show file sizes
SIZE_PKG=$(du -sh "$FINAL_PKG" | cut -f1)
SIZE_ZIP=$(du -sh "$FINAL_ZIP" | cut -f1)
echo "==========================================="
echo "✅ SUCCESS!"
echo "==========================================="
echo "Installer (PKG): $FINAL_PKG ($SIZE_PKG)"
echo "App Bundle (ZIP): $FINAL_ZIP ($SIZE_ZIP)"
echo ""
if [ ! -z "$APPLE_ID" ]; then
    if [ "$PKG_SIGNED" = true ]; then
        echo "Status: PKG & ZIP are SIGNED and NOTARIZED 🛡️"
    else
        echo "Status: ZIP is SIGNED and NOTARIZED 🛡️ (PKG is unsigned)"
        echo "Tip: Distribute the ZIP file for the best user experience."
    fi
else
    echo "Status: UNSIGNED (For internal use only)"
fi
echo "==========================================="
echo ""
