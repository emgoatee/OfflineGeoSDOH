# Building a Signed & Notarized App

This guide walks you through building the app with signing and notarization so coworkers can install it without security warnings.

## Prerequisites

✅ **You've completed:**
- Created `.env` file with Apple ID, Team ID, App-Specific Password, and Signing Identities
- Have an active Apple Developer account

⚠️ **You still need:**
- **Developer ID certificates** installed in your Mac's Keychain

### Installing Developer ID Certificates

1. **Go to Apple Developer Portal:**
   - Visit: https://developer.apple.com/account/resources/certificates/list
   - Sign in with your Apple ID

2. **Download certificates:**
   - **Developer ID Application** certificate (for signing the .app)
   - **Developer ID Installer** certificate (for signing the .pkg - optional)

3. **Install certificates:**
   - Double-click the downloaded `.cer` files
   - They will be added to your **login** keychain automatically
   - Verify in Keychain Access app: `Developer ID Application: Bobbin LLC (8YY98N4P3K)` should appear

4. **Verify certificates are installed:**
   ```bash
   security find-identity -p basic -v | grep "Developer ID"
   ```
   You should see both certificates listed.

## Build Steps

### Step 1: Ensure the Executable is Built

The installer app bundle needs the PyInstaller executable. If you haven't built it yet:

```bash
cd /Users/tom6nz/Desktop/OfflineGeoLocator

# Activate virtual environment (if using one)
source .venv/bin/activate  # or: source venv/bin/activate

# Install PyInstaller if needed
pip install pyinstaller

# Build the executable
pyinstaller OfflineGeoLocator_core.spec

# Copy the executable into the installer app bundle
cp dist/OfflineGeoLocator "installer/Offline GEO-SDOH.app/Contents/Resources/OfflineGeoLocator_executable"
chmod +x "installer/Offline GEO-SDOH.app/Contents/Resources/OfflineGeoLocator_executable"
```

**Note:** If `dist/OfflineGeoLocator` already exists and is up-to-date, you can skip this step.

### Step 2: Run the Build Script

Simply run the build script:

```bash
cd /Users/tom6nz/Desktop/OfflineGeoLocator
./build_installer.sh
```

The script will:
1. ✅ Load credentials from `.env`
2. ✅ Sign the app bundle with your Developer ID
3. ✅ Create a ZIP file for distribution
4. ✅ (Optional) Create and sign a .pkg installer
5. ✅ Submit to Apple for notarization (takes 5-15 minutes)
6. ✅ Staple the notarization ticket to the app
7. ✅ Create the final signed and notarized ZIP

### Step 3: Wait for Notarization

The script will wait for Apple's notarization to complete. This typically takes **5-15 minutes**. You'll see output like:

```
Step 4: Submitting to Apple for Notarization...
  Submitting ZIP...
  id: abc123...
  status: Accepted
✓ Notarization successful!
```

### Step 4: Find Your Signed App

After the build completes, you'll have:

- **`OfflineGeoLocator-v1.1.4-macOS.zip`** ← **This is what you share with coworkers!**
  - ✅ Signed with Developer ID
  - ✅ Notarized by Apple
  - ✅ No security warnings on other Macs

- **`OfflineGeoLocator-Installer-v1.1.4.pkg`** (if certificates were found)
  - ✅ Signed installer package
  - ✅ Alternative distribution method

## What to Share with Coworkers

**Share the ZIP file** (`OfflineGeoLocator-v1.1.4-macOS.zip`):

1. Upload to GitHub Releases, or
2. Share via email/cloud storage

**Tell coworkers:**
1. Download the ZIP
2. Extract it
3. Move `Offline GEO-SDOH.app` to their **Applications** folder
4. Double-click to launch (no security warnings!)

## Troubleshooting

### "No signing identity found"

**Problem:** Script says certificates aren't in keychain.

**Solution:**
1. Download certificates from Apple Developer Portal (see Prerequisites above)
2. Double-click to install them
3. Verify with: `security find-identity -p basic -v | grep "Developer ID"`
4. Run the build script again

### "Notarization failed"

**Problem:** Apple rejected the notarization.

**Solution:**
- Check the error message in the script output
- Common issues:
  - Expired certificates → Renew in Apple Developer Portal
  - Invalid entitlements → Check `entitlements.plist`
  - Malformed app bundle → Rebuild the executable

### "The app is damaged and can't be opened" (on other Macs)

**Problem:** App wasn't properly signed/notarized, or the ZIP was corrupted.

**Solution:**
- Re-run the build script to ensure signing and notarization completed
- Verify the final ZIP: `codesign --verify --deep --strict "Offline GEO-SDOH.app"`
- Make sure you're sharing the **ZIP** from the build output, not an old version

### Build takes a long time

**Normal:** Notarization typically takes 5-15 minutes. The script waits automatically.

## Quick Reference

```bash
# Full build process (if starting from scratch)
cd /Users/tom6nz/Desktop/OfflineGeoLocator
source .venv/bin/activate  # if using venv
pip install pyinstaller
pyinstaller OfflineGeoLocator_core.spec
cp dist/OfflineGeoLocator "installer/Offline GEO-SDOH.app/Contents/Resources/OfflineGeoLocator_executable"
chmod +x "installer/Offline GEO-SDOH.app/Contents/Resources/OfflineGeoLocator_executable"
./build_installer.sh

# Result: OfflineGeoLocator-v1.1.4-macOS.zip (signed & notarized)
```
