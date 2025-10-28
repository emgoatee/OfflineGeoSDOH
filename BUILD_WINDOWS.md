# Building Offline GEO-SDOH for Windows

This guide explains how to build the Windows version of Offline GEO-SDOH.

## Prerequisites

### Required Software

1. **Windows 10 or 11** (64-bit)
2. **Python 3.8+** - Download from https://www.python.org/downloads/
3. **Git** - Download from https://git-scm.com/download/win
4. **Inno Setup** (for installer) - Download from https://jrsoftware.org/isinfo.php
5. **Pillow** (for icon conversion) - Will be installed with requirements

## Step-by-Step Build Process

### 1. Clone the Repository

```bash
git clone https://github.com/emgoatee/OfflineGeoSDOH.git
cd OfflineGeoSDOH
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller pillow
```

### 3. Download Core Data Files

You need to have the core health indices data files in the `data/` directory:
- `ACS_deprivation_index.csv`
- `ACS_deprivation_index_by_zipcode.csv`
- `COI_subdomin_data.csv`
- `COI_subdomin_data.xlsx`
- `SVI_2022_US.csv`
- `adi.csv`
- `geodata.csv`
- `hud_zip_tract.csv`

### 4. Build the Executable

```bash
# Run the build script
build_windows.bat
```

This will:
- Create the Windows icon file (SDOH_icon.ico)
- Build the executable with PyInstaller
- Output to `dist\OfflineGeoSDOH.exe`

### 5. Create the Windows Installer

1. Open **Inno Setup**
2. File → Open → Select `installer_windows.iss`
3. Build → Compile
4. The installer will be created as `OfflineGeoSDOH-Installer-v1.0.0-Windows.exe`

## File Locations

### On Windows, the app stores data in:
```
C:\Users\<YourName>\AppData\Roaming\OfflineGeoSDOH\data\
```

### Executable location after build:
```
dist\OfflineGeoSDOH.exe
```

### Installer location after compilation:
```
OfflineGeoSDOH-Installer-v1.0.0-Windows.exe
```

## Testing the Build

1. **Test the executable:**
   ```bash
   dist\OfflineGeoSDOH.exe
   ```
   - The app should start a local web server
   - A browser window should open to http://localhost:5001

2. **Test the installer:**
   - Double-click `OfflineGeoSDOH-Installer-v1.0.0-Windows.exe`
   - Follow the installation wizard
   - Launch the app from Start Menu or Desktop shortcut

## Distributing the Windows Version

Upload to your GitHub release:
1. The installer: `OfflineGeoSDOH-Installer-v1.0.0-Windows.exe` (~180MB)
2. Core data package: `core_data.zip`
3. State packages: `state_*.zip` files

## Troubleshooting

### Python Not Found
- Make sure Python is in your PATH
- Reinstall Python and check "Add Python to PATH" during installation

### PyInstaller Build Fails
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Try deleting `build/` and `dist/` folders and rebuild

### Icon Not Created
- Install Pillow: `pip install pillow`
- Manually run: `python create_windows_icon.py`

### Inno Setup Compile Fails
- Ensure `dist\OfflineGeoSDOH.exe` exists before compiling installer
- Check that `LICENSE` file exists in the root directory

## Differences from Mac Version

| Feature | macOS | Windows |
|---------|-------|---------|
| **App Name** | Offline GEO-SDOH.app | OfflineGeoSDOH.exe |
| **Data Location** | ~/Library/Application Support/OfflineGeoLocator/data | %APPDATA%\OfflineGeoSDOH\data |
| **Installer** | .pkg (176MB) | .exe (180MB) |
| **Console** | Hidden | Visible (shows server output) |

## Building on Mac/Linux (Cross-Compilation)

**Note:** PyInstaller cannot cross-compile. You **must** build the Windows version on a Windows machine.

### Options:
1. **Dual-boot Windows**
2. **Windows VM** (VirtualBox, Parallels, VMware)
3. **GitHub Actions** (automated builds in the cloud)
4. **Wine** (not recommended - unreliable)

## Automated Builds with GitHub Actions

If you want to automate Windows builds, you can set up GitHub Actions. Let me know if you'd like help with that!

## Support

For issues specific to Windows builds, please open an issue at:
https://github.com/emgoatee/OfflineGeoSDOH/issues
