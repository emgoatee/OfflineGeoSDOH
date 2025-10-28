# Offline Geo SDOH Match

A Mac application that performs **completely offline** geocoding of US addresses and retrieves multiple Social Determinants of Health (SDOH) indices.

## Features

- ✅ **100% Offline Operation**: Works without internet after initial setup
- ✅ **Offline Geocoding**: Convert US street addresses to coordinates using Census TIGER/Line shapefiles
- ✅ **Multiple Health Indices**: Retrieve SDI, SVI, ADI, Brokamp ADI, and COI data
- ✅ **Modular State Packages**: Download only the states you need (29KB - 201MB each)
- ✅ **All 50 States + Territories**: Supports all US states and territories
- ✅ **Easy Installation**: One-click Mac installer, installs like any Mac app

## Installation (For Users)

### Quick Start - Mac Installer (Recommended)

1. **Download the installer** from [Releases](https://github.com/emgoatee/OfflineGeoSDOH/releases/latest)
   - File: `OfflineGeoLocator-Installer-v1.0.0.pkg`

2. **Install the package**
   - **Right-click** (or Control+click) on the `.pkg` file
   - Select **"Open"** from the menu
   - Click **"Open"** in the security dialog
   - Follow the installation prompts
   - *(macOS blocks unsigned apps by default - this is safe!)*

3. **Launch and setup** (first time only)
   - Find OfflineGeoLocator in Applications folder
   - **Right-click → Open** (first time only)
   - Follow guided setup to download state data
   - Browser opens automatically

4. **Start geocoding!**
   - Enter addresses and get health index data
   - Works 100% offline after initial setup

> **Note:** You may see a security warning because this app isn't signed with an Apple Developer certificate. The app is [open-source](https://github.com/emgoatee/OfflineGeoSDOH) and safe to use. Use the right-click method above to bypass the warning.

### System Requirements

- **macOS 10.13 (High Sierra) or later**
- **500MB disk space** (core app)
- **Additional space for states** (varies: 29KB - 201MB per state)
- **Internet connection** (for initial install and state downloads only)

### What Happens on First Launch

1. Welcome dialog explains state download needed
2. Terminal opens with interactive state downloader
3. Select which states you need (or download all)
4. Browser opens automatically to http://localhost:5001
5. App is ready to use offline!

### File Sizes

- **Installer**: 174MB (one-time download)
- **Core Data**: 112MB (required, downloads automatically)
- **Each State**: 29KB - 201MB (varies by state size)
- **Minimum Setup**: ~286MB (installer + core data, no states yet)
- **Example**: Core + OH + PA + NY ≈ 750MB
- **Full Install**: ~3.4GB (all 56 states/territories)

**You only download what you need!**

## How It Works

### Completely Offline

After initial setup, OfflineGeoLocator works **100% offline**:

✅ **Geocoding** (address → coordinates) - Uses local Census TIGER/Line shapefiles
✅ **Census tract lookup** - Uses local boundary data
✅ **Health index retrieval** - Uses local CSV files
✅ **Web interface** - Runs on your computer (localhost)

**Perfect for:**
- Remote locations without internet
- Air-gapped networks
- Privacy-sensitive work
- Traveling
- Reliable offline research

### Health Indices Provided

1. **Social Deprivation Index (SDI)** - Census tract-level socioeconomic measure
2. **Social Vulnerability Index (SVI)** - CDC measure of community resilience
3. **Area Deprivation Index (ADI)** - Neighborhood disadvantage measure
4. **Brokamp Area Deprivation Index** - ZIP code-level disadvantage measure
5. **Child Opportunity Index (COI)** - Neighborhood resources for children

## Using the Application

1. Launch OfflineGeoLocator from Applications
2. Browser opens to http://localhost:5001
3. Enter a US street address
4. Select state from dropdown (only shows downloaded states)
5. Click "Geocode Address"
6. View comprehensive health index results

### Supported Locations

All 50 US states plus:
- District of Columbia (DC)
- Puerto Rico (PR)
- American Samoa (AS)
- Guam (GU)
- Northern Mariana Islands (MP)
- US Virgin Islands (VI)

## For Developers

See [DEPLOYMENT.md](DEPLOYMENT.md) for build and deployment instructions.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/emgoatee/OfflineGeoSDOH.git
cd OfflineGeoSDOH

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

The application will be available at http://localhost:5001

### Project Structure

- `app.py` - Main Flask application with geocoding logic
- `templates/index.html` - Web interface
- `data/` - Census shapefiles and health index CSV files (excluded from git)
- `package_states.py` - Script to create state packages
- `download_states.py` - User utility to download states
- `OfflineGeoLocator_core.spec` - PyInstaller configuration
- `installer/` - Mac .app bundle and installer components

### Building the Installer

See [INSTALLER_GUIDE.md](INSTALLER_GUIDE.md) for detailed instructions on building the Mac installer package.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Credits

Data sources:
- Census TIGER/Line Shapefiles (2022)
- Social Deprivation Index - Graham Center
- Social Vulnerability Index - CDC/ATSDR
- Area Deprivation Index - University of Wisconsin
- Brokamp Area Deprivation Index - Dr. Cole Brokamp
- Child Opportunity Index - diversitydatakids.org
