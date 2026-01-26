#!/bin/bash
set -e

# Load metadata
VERSION="1.1.4"
APP_NAME="Offline GEO-SDOH"
BUNDLE_ID="com.offlinegeolocator.app"

echo "Building $APP_NAME v$VERSION (Signed & Notarized)"
echo "==========================================="
echo ""

# Paths
APP_PATH="installer/${APP_NAME}.app"
DIST_XML="installer/Distribution.xml"
FINAL_ZIP="OfflineGeoLocator-v${VERSION}-macOS.zip"

# Load credentials from .env if it exists
if [ -f ".env" ]; then
    echo "🔑 Loading signing credentials from .env..."
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

# --- Step 1: Sign the App Bundle ---
if [ ! -z "$APPLE_SIGNING_IDENTITY" ]; then
    echo "Step 1: Signing app bundle..."
    
    # Aggressively clean metadata and previous signatures
    echo "  Cleaning attributes..."
    xattr -rc "$APP_PATH"
    
    echo "  Removing old signatures..."
    codesign --remove-signature "$APP_PATH/Contents/Resources/OfflineGeoLocator_executable" || true
    codesign --remove-signature "$APP_PATH" || true
    
    # Sign nested components first
    echo "  Signing nested binaries..."
    find "$APP_PATH" -type f \( -name "*.dylib" -o -name "*.so" \) -exec codesign --force --options runtime --sign "$APPLE_SIGNING_IDENTITY" --timestamp {} +
    
    # Sign the main executable with entitlements
    echo "  Signing main executable..."
    codesign --force --options runtime --entitlements entitlements.plist --sign "$APPLE_SIGNING_IDENTITY" --timestamp "$APP_PATH/Contents/Resources/OfflineGeoLocator_executable"
    
    # Sign the launcher
    echo "  Signing launcher..."
    codesign --force --options runtime --sign "$APPLE_SIGNING_IDENTITY" --timestamp "$APP_PATH/Contents/MacOS/launcher"

    # Sign the main bundle
    echo "  Signing package bundle..."
    codesign --force --options runtime --entitlements entitlements.plist --sign "$APPLE_SIGNING_IDENTITY" --timestamp "$APP_PATH"
    
    echo "✓ App bundle signed."
    echo ""
fi

# --- Step 2: ZIP for Distribution (Required for Notarization) ---
echo "Step 2: Creating ZIP for notarization..."
rm -f "$FINAL_ZIP"
cd installer
zip -r "../$FINAL_ZIP" "${APP_NAME}.app" > /dev/null
cd ..
echo "✓ ZIP created: $FINAL_ZIP"
echo ""

# --- Step 3: Notarization ---
if [ ! -z "$APPLE_ID" ] && [ ! -z "$APPLE_PASSWORD" ] && [ ! -z "$APPLE_TEAM_ID" ]; then
    echo "Step 3: Submitting to Apple for Notarization..."
    
    xcrun notarytool submit "$FINAL_ZIP" \
        --apple-id "$APPLE_ID" \
        --password "$APPLE_PASSWORD" \
        --team-id "$APPLE_TEAM_ID" \
        --wait
    
    echo "✓ Notarization successful!"
    echo ""
    
    echo "Step 4: Stapling notarization ticket..."
    xcrun stapler staple "$APP_PATH"
    echo "✓ Ticket stapled to .app bundle."
    
    # Re-zip the stapled app
    echo "  Re-zipping stapled app..."
    rm "$FINAL_ZIP"
    cd installer
    zip -r "../$FINAL_ZIP" "${APP_NAME}.app" > /dev/null
    cd ..
    echo "✓ Final notarized ZIP ready: $FINAL_ZIP"
    echo ""
fi

# Show result
SIZE_ZIP=$(du -sh "$FINAL_ZIP" | cut -f1)
echo "==========================================="
echo "✅ SUCCESS!"
echo "==========================================="
echo "App Bundle (ZIP): $FINAL_ZIP ($SIZE_ZIP)"
echo ""
if [ ! -z "$APPLE_ID" ]; then
    echo "Status: SIGNED and NOTARIZED 🛡️"
else
    echo "Status: UNSIGNED (Internal use only)"
fi
echo "==========================================="
