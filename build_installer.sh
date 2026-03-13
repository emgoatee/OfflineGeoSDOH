#!/bin/bash
set -e

# Load metadata
VERSION="${VERSION:-1.1.4}"
APP_NAME="Offline GEO-SDOH"
BUNDLE_ID="com.offlinegeolocator.app"

echo "Building $APP_NAME v$VERSION (Signed & Notarized)"
echo "==========================================="
echo ""

# Paths
APP_PATH="installer/${APP_NAME}.app"
DIST_XML="installer/Distribution.xml"
FINAL_ZIP="OfflineGeoLocator-v${VERSION}-macOS.zip"
FINAL_PKG="OfflineGeoLocator-Installer-v${VERSION}.pkg"
COMPONENT_PKG="OfflineGeoLocator-v${VERSION}-Component.pkg"

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
    
    echo "  Deep cleaning attributes..."
    xattr -rc "$APP_PATH"
    xattr -cr "$APP_PATH"
    
    echo "  Setting permissions and timestamps..."
    find "$APP_PATH" -type f -print0 | xargs -0 touch 2>/dev/null || true
    chmod +x "$APP_PATH/Contents/MacOS/launcher"
    chmod +x "$APP_PATH/Contents/Resources/OfflineGeoLocator_executable"
    
    # Wait for filesystem to settle
    sleep 2
    
    echo "  Removing old signatures..."
    codesign --remove-signature "$APP_PATH/Contents/Resources/OfflineGeoLocator_executable" || true
    codesign --remove-signature "$APP_PATH" || true
    
    # Sign nested components first
    echo "  Signing nested binaries..."
    find "$APP_PATH" -type f \( -name "*.dylib" -o -name "*.so" \) -exec codesign --force --options runtime --sign "$APPLE_SIGNING_IDENTITY" --timestamp {} +
    
    # Sign the main executable with entitlements
    echo "  Signing main executable..."
    codesign --force --options runtime --entitlements entitlements.plist --sign "$APPLE_SIGNING_IDENTITY" --timestamp "$APP_PATH/Contents/Resources/OfflineGeoLocator_executable"
    
    # Sign the launcher with entitlements
    echo "  Signing launcher..."
    codesign --force --options runtime --entitlements entitlements.plist --sign "$APPLE_SIGNING_IDENTITY" --timestamp "$APP_PATH/Contents/MacOS/launcher"

    # Sign the main bundle
    echo "  Signing package bundle..."
    codesign --force --options runtime --entitlements entitlements.plist --sign "$APPLE_SIGNING_IDENTITY" --timestamp "$APP_PATH"
    
    echo "  Verifying signature..."
    codesign --verify --deep --strict --verbose=2 "$APP_PATH"
    
    echo "✓ App bundle signed."
    echo ""
fi

# --- Step 2: ZIP for Distribution (Required for Notarization) ---
echo "Step 2: Creating ZIP for notarization using ditto..."
rm -f "$FINAL_ZIP"
# Use ditto for bundling to preserve extended attributes and permissions correctly
ditto -c -k --sequesterRsrc --keepParent "$APP_PATH" "$FINAL_ZIP"
echo "✓ ZIP created: $FINAL_ZIP"
echo ""

# --- Step 3: Notarization ---
if [ ! -z "$APPLE_ID" ] && [ ! -z "$APPLE_PASSWORD" ] && [ ! -z "$APPLE_TEAM_ID" ]; then
    echo "Step 3: Creating and signing .pkg installer..."
    if [ ! -z "$APPLE_INSTALLER_IDENTITY" ] && security find-identity -p basic -v | grep -q "$APPLE_INSTALLER_IDENTITY"; then
        # Create component package
        PKG_SCRIPTS=""
        [ -d "installer/scripts" ] && PKG_SCRIPTS="--scripts installer/scripts"
        
        pkgbuild --component "$APP_PATH" \
                 --install-location "/Applications" \
                 $PKG_SCRIPTS \
                 "$COMPONENT_PKG"
        
        # Create distribution package
        PKG_RESOURCES=""
        [ -d "installer/resources" ] && PKG_RESOURCES="--resources installer/resources"
        
        productbuild --distribution "$DIST_XML" \
                     --package-path "." \
                     $PKG_RESOURCES \
                     --sign "$APPLE_INSTALLER_IDENTITY" \
                     "$FINAL_PKG"
        
        rm "$COMPONENT_PKG"
        echo "✓ .pkg installer created and signed."
    else
        echo "⚠️  APPLE_INSTALLER_IDENTITY not found in keychain. Skipping .pkg creation."
        echo "   (This is OK - the ZIP distribution will still be notarized and functional.)"
    fi
    echo ""

    echo "Step 4: Submitting to Apple for Notarization..."
    
    # Submit the ZIP (contains the .app)
    echo "  Submitting ZIP..."
    xcrun notarytool submit "$FINAL_ZIP" \
        --apple-id "$APPLE_ID" \
        --password "$APPLE_PASSWORD" \
        --team-id "$APPLE_TEAM_ID" \
        --wait
    
    # Submit the PKG if created
    if [ -f "$FINAL_PKG" ]; then
        echo "  Submitting PKG..."
        xcrun notarytool submit "$FINAL_PKG" \
            --apple-id "$APPLE_ID" \
            --password "$APPLE_PASSWORD" \
            --team-id "$APPLE_TEAM_ID" \
            --wait
    fi
    
    echo "✓ Notarization successful!"
    echo ""
    
    echo "Step 5: Stapling notarization ticket..."
    xcrun stapler staple "$APP_PATH"
    if [ -f "$FINAL_PKG" ]; then
        xcrun stapler staple "$FINAL_PKG"
    fi
    echo "✓ Ticket stapled."
    
    # Re-zip the stapled app using ditto
    echo "  Re-zipping stapled app using ditto..."
    rm "$FINAL_ZIP"
    ditto -c -k --sequesterRsrc --keepParent "$APP_PATH" "$FINAL_ZIP"
    echo "✓ Final notarized ZIP ready: $FINAL_ZIP"
    echo ""
fi

# Show result
SIZE_ZIP=$(du -sh "$FINAL_ZIP" | cut -f1)
[ -f "$FINAL_PKG" ] && SIZE_PKG=$(du -sh "$FINAL_PKG" | cut -f1)
echo "==========================================="
echo "✅ SUCCESS!"
echo "==========================================="
echo "App Bundle (ZIP): $FINAL_ZIP ($SIZE_ZIP)"
[ -f "$FINAL_PKG" ] && echo "Installer (PKG):  $FINAL_PKG ($SIZE_PKG)"
echo ""
if [ ! -z "$APPLE_ID" ]; then
    echo "Status: SIGNED and NOTARIZED 🛡️"
else
    echo "Status: UNSIGNED (Internal use only)"
fi
echo "==========================================="
