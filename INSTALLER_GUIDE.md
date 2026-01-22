# OfflineGeoLocator Distribution Guide

## ✅ Professional Distribution Ready!

Your signed and notarized app bundle is ready for professional distribution.

**Recommended File**: `OfflineGeoLocator-v1.1.1-macOS.zip` (96MB)
- ✅ **Signed** with your Developer ID
- ✅ **Notarized** by Apple
- ✅ **Warning-free** installation

**Alternative**: `OfflineGeoLocator-Installer-v1.1.1.pkg` (95MB)
- ⚠️ Unsigned (users will see a security warning)

## How Users Will Install and Use It (Recommended ZIP)

### Step 1: Download the ZIP
Users download `OfflineGeoLocator-v1.1.1-macOS.zip` from your GitHub release.

### Step 2: Extract and Move
- Extract the ZIP file.
- Move `OfflineGeoSDOH` (the app) to the **Applications** folder.

### Step 3: First Launch
When users launch the app for the first time:

1. **Welcome Dialog** appears explaining they need to download state data
2. **Terminal opens automatically** with the state downloader
3. **User selects states** to download interactively
4. **Browser opens automatically** to http://localhost:5002 when ready
5. **App appears in Dock** while running

### Step 4: Using the App
- **Launch**: Double-click `OfflineGeoLocator` in Applications folder
- **Use**: Browser opens automatically to the web interface
- **Quit**: Cmd+Q or quit from Dock (stops the server)

## Improved User Experience ✨

### What's Better Than Before:
✅ **One-click install** - No manual file extraction needed
✅ **Applications folder** - Appears like any normal Mac app
✅ **Auto-opens browser** - No need to type URL
✅ **First-run setup** - Guided state download process
✅ **Dock integration** - App appears in Dock when running
✅ **Easy to quit** - Quits like a normal app

### What Users DON'T Need to Do:
❌ Extract ZIP files manually
❌ Open Terminal to run commands
❌ Navigate to http://localhost:5002
❌ Understand file structures

## Distributing the Installer

### Upload to GitHub Release

1. **Create a new release** at:
   https://github.com/emgoatee/OfflineGeoSDOH/releases/new

2. **Tag**: `v1.1.1`

3. **Title**: `v1.1.1 - Easy Install Package`

4. **Upload these files**:
   - `OfflineGeoLocator-v1.1.1-macOS.zip` (96MB) - **The recommended professional version**
   - `OfflineGeoLocator-Installer-v1.1.1.pkg` (95MB) - (Unsigned fallback)
   - `state_packages/core_data.zip` (112MB) - Core CSV data
   - All `state_packages/state_*.zip` files (for manual downloads)

5. **Release notes**: See below

### Suggested Release Notes

```markdown
# OfflineGeoLocator v1.1.1

Easy-to-install Mac application for offline geocoding and health index lookups.

## 🎉 Professional Distribution Ready

**Recommended Download**: `OfflineGeoLocator-v1.1.1-macOS.zip` (96MB)

### Installation (ZIP)
1. Download the .zip file
2. Extract to your **Applications** folder
3. Launch `OfflineGeoSDOH`
4. macOS will verify and open it immediately (No security warnings)

That's it! The app handles everything else automatically.

## Features
- Offline geocoding for all US states and territories
- 5 health indices (SDI, SVI, ADI, Brokamp ADI, COI)
- Modular state downloads (only download what you need)
- Clean web interface with responsive design
- Runs entirely offline after state download

## System Requirements
- macOS 10.13 or later
- 500MB disk space (core app only)
- Additional space for state packages (varies)

## State Packages
State packages are downloaded automatically on first launch, or you can download manually:
- Core data (required): `core_data.zip` (112MB)
- Individual states: `state_XX.zip` (29KB - 201MB each)

## Support
- Documentation: See README.md
- Issues: https://github.com/emgoatee/OfflineGeoSDOH/issues
```

## Link to Share

Once you create the release, share these links:

**Main download page:**
```
https://github.com/emgoatee/OfflineGeoSDOH/releases/latest
```

**Direct installer download:**
```
https://github.com/emgoatee/OfflineGeoSDOH/releases/download/v1.1.1/OfflineGeoLocator-Installer-v1.1.1.pkg
```

## 🔐 Security Troubleshooting (macOS)

Because the installer is not digitally signed through the Apple Developer Program, macOS Gatekeeper will block it by default.

### If you see "Apple could not verify..." or "Blocked":

1. **Attempt to open** the installer (it will fail with the warning).
2. Open **System Settings** (or System Preferences).
3. Go to **Privacy & Security**.
4. Scroll down to the **Security** section.
5. You will see a message: `"OfflineGeoLocator-Installer-v1.1.1.pkg" was blocked from use because it is not from an identified developer.`
6. Click **Open Anyway**.
7. Enter your Mac password when prompted.
8. A final box will appear asking if you are sure—click **Open**.

> [!TIP]
> **Advanced Users**: You can also use the terminal to remove the "quarantine" flag that causes this warning:
> `xattr -d com.apple.quarantine ~/Downloads/OfflineGeoLocator-Installer-v1.1.1.pkg`

---

## Technical Details

### What's Included in the Installer:
- Mac .app bundle with proper structure
- Launcher script that auto-opens browser
- Flask executable (175MB)
- State downloader utility
- User documentation

### What Happens on Installation:
1. Installs to `/Applications/OfflineGeoLocator.app`
2. Sets executable permissions
3. Creates proper Mac app structure
4. Ready to launch immediately

### What Happens on First Launch:
1. Checks for `data/` folder
2. If missing/empty, shows welcome dialog
3. Opens Terminal with state downloader
4. Waits for core data download
5. Starts Flask server on port 5002
6. Opens default browser
7. Shows notification when ready

### How It Works:
- The .app bundle contains a launcher script
- Launcher checks if first run
- Starts the Flask executable
- Opens browser to localhost:5002
- Stays running in Dock until quit

## Next Steps

- **Installer**: `/Users/tom6nz/Desktop/OfflineGeoLocator/OfflineGeoLocator-Installer-v1.1.1.pkg`
- **State packages**: `/Users/tom6nz/Desktop/OfflineGeoLocator/state_packages/` (57 files)
- **Source code**: Already on GitHub
- **Credentials**: `.env` (contains private signing keys - **DO NOT SHARE**)

---

## 🔏 Automated Signing & Notarization

The project now includes automated signing and notarization in the `build_installer.sh` script.

### Setup

1.  **Credentials**: Ensure you have a `.env` file based on `signing_credentials.template.env` with your Apple ID and App-Specific Password.
2.  **Identities**: Your machine should have the "Developer ID Application" and "Developer ID Installer" certificates installed in KeyChain.
3.  **Run Build**: Simply run `./build_installer.sh`.

### What it does:
1.  **Codesigns** the `.app` bundle (required for Gatekeeper).
2.  **Signs** the `.pkg` component and distribution packages.
3.  **Submits** to Apple for notarization.
4.  **Staples** the notarization ticket to the final `.pkg`.

Once the build finishes with "Status: SIGNED and NOTARIZED", users will be able to install the app without any security warnings!

---

**Ready to distribute professionally!** 🚀
