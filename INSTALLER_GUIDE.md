# OfflineGeoLocator Installer Guide

## ✅ Installer Package Ready!

Your Mac installer has been created:
**File**: `OfflineGeoLocator-Installer-v1.0.0.pkg` (174MB)

## How Users Will Install and Use It

### Step 1: Download the Installer
Users download `OfflineGeoLocator-Installer-v1.0.0.pkg` from your GitHub release

### Step 2: Double-Click to Install
- Double-click the `.pkg` file
- macOS Installer will open with a welcome screen
- Click "Continue" and follow the prompts
- The app will be installed to `/Applications/OfflineGeoLocator.app`

### Step 3: First Launch
When users launch the app for the first time:

1. **Welcome Dialog** appears explaining they need to download state data
2. **Terminal opens automatically** with the state downloader
3. **User selects states** to download interactively
4. **Browser opens automatically** to http://localhost:5001 when ready
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
❌ Navigate to http://localhost:5001
❌ Understand file structures

## Distributing the Installer

### Upload to GitHub Release

1. **Create a new release** at:
   https://github.com/emgoatee/OfflineGeoSDOH/releases/new

2. **Tag**: `v1.0.0`

3. **Title**: `v1.0.0 - Easy Install Package`

4. **Upload these files**:
   - `OfflineGeoLocator-Installer-v1.0.0.pkg` (174MB) - **The main installer**
   - `state_packages/core_data.zip` (112MB) - Core CSV data
   - All `state_packages/state_*.zip` files (for manual downloads)

5. **Release notes**: See below

### Suggested Release Notes

```markdown
# OfflineGeoLocator v1.0.0

Easy-to-install Mac application for offline geocoding and health index lookups.

## 🎉 New: One-Click Installer Package

**Download**: `OfflineGeoLocator-Installer-v1.0.0.pkg` (174MB)

### Installation
1. Download the .pkg file
2. Double-click to install
3. Launch from Applications folder
4. Download states on first run

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
https://github.com/emgoatee/OfflineGeoSDOH/releases/download/v1.0.0/OfflineGeoLocator-Installer-v1.0.0.pkg
```

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
5. Starts Flask server on port 5001
6. Opens default browser
7. Shows notification when ready

### How It Works:
- The .app bundle contains a launcher script
- Launcher checks if first run
- Starts the Flask executable
- Opens browser to localhost:5001
- Stays running in Dock until quit

## Next Steps

1. ✅ Installer created
2. ⏳ Upload to GitHub release
3. ⏳ Test installation on a clean Mac
4. ⏳ Share link with users

## File Locations

- **Installer**: `/Users/tom6nz/Desktop/OfflineGeoLocator/OfflineGeoLocator-Installer-v1.0.0.pkg`
- **State packages**: `/Users/tom6nz/Desktop/OfflineGeoLocator/state_packages/` (57 files)
- **Source code**: Already on GitHub

---

**Ready to distribute!** 🚀
