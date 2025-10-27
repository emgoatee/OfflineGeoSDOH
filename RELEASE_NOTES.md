# OfflineGeoLocator v1.0.1 - Mac Installer Package

🎉 **Easy one-click installer for macOS!**

## 📥 Download

**For Mac Users (Recommended):**
Download `OfflineGeoLocator-Installer-v1.0.1.pkg` (174MB)

**Installation:**
1. Double-click the `.pkg` file
2. Follow the installer prompts
3. Launch from Applications folder
4. Download states on first run (guided setup)

That's it! Everything else is automatic.

---

## ✨ What's New

- **One-click installer** - Install like any Mac app
- **Auto-opens browser** - No manual URL typing needed
- **First-run setup** - Guided state download process
- **Applications folder** - Appears with all your other apps
- **Dock integration** - Works like a native Mac app

## 🎯 Features

### Offline Geocoding
- Convert US street addresses to coordinates
- Works completely offline (after state data download)
- Covers all 50 states + territories

### Health Indices
- **Social Deprivation Index (SDI)** - Graham Center
- **Social Vulnerability Index (SVI)** - CDC/ATSDR
- **Area Deprivation Index (ADI)** - University of Wisconsin
- **Brokamp Area Deprivation Index** - By ZIP code
- **Child Opportunity Index (COI)** - diversitydatakids.org

### Modular State Downloads
- Download only the states you need
- Core app: 174MB
- Each state: 29KB - 201MB
- Total all states: ~3.2GB

### User Interface
- Clean, responsive web interface
- Mobile-friendly design
- Learn more links for each health index
- Montserrat font with custom color scheme

## 💻 System Requirements

- macOS 10.13 (High Sierra) or later
- 500MB free disk space (core app)
- Additional space for state packages (varies)
- Internet connection (for initial state download only)

## 📦 What's Included

The installer package contains:
- Flask web application
- Geocoding engine
- Health index lookup functions
- CSV data files (SDI, SVI, ADI, COI)
- State downloader utility
- User documentation

## 🚀 Getting Started

### After Installation:

1. **Launch the app** from Applications folder
2. **First run**: Dialog explains you need state data
3. **Terminal opens** with interactive state downloader
4. **Select states** you want to download (or download all)
5. **Browser opens automatically** when ready
6. **Start geocoding** addresses!

### Using the App:

1. Enter a US street address
2. Select the state
3. Click "Geocode Address"
4. View health index results

### Managing States:

- Download more states anytime: Run the downloader in the app's Resources folder
- Remove states: Delete from `/Applications/OfflineGeoLocator.app/Contents/Resources/data/`
- Check what you have: Look in the data folder

## 📊 State Packages (Optional Manual Download)

If you prefer to download states manually instead of using the built-in downloader:

**Required:**
- `core_data.zip` (112MB) - Core CSV/Excel files

**Optional (one per state):**
- `state_AL.zip` through `state_WY.zip`
- Size varies: 29KB (AS) to 201MB (CA)

Extract these into: `/Applications/OfflineGeoLocator.app/Contents/Resources/data/`

## 🔧 Technical Details

- **Built with**: Flask, GeoPandas, Shapely, PyProj
- **Data source**: Census TIGER/Line 2022 shapefiles
- **Runs on**: http://localhost:5001
- **Architecture**: Modular state packages
- **Size reduction**: 94% smaller than monolithic version

## 📚 Documentation

- **README.md** - Development guide
- **DEPLOYMENT.md** - Deployment instructions
- **INSTALLER_GUIDE.md** - Distribution guide
- **RELEASE_SUMMARY.md** - Build details

## 🐛 Known Issues

- **macOS Security**: On first launch, you may need to right-click → Open if you get a security warning
- **Port 5001**: Make sure port 5001 is not in use by another application
- **State Download**: Requires internet connection for initial state download

## 🆘 Support

- **Issues**: https://github.com/emgoatee/OfflineGeoSDOH/issues
- **Documentation**: See README.md in repository

## 📝 Credits

**Data Sources:**
- Census TIGER/Line Shapefiles (2022) - US Census Bureau
- Social Deprivation Index - Graham Center
- Social Vulnerability Index - CDC/ATSDR
- Area Deprivation Index - University of Wisconsin
- Brokamp Area Deprivation Index - Dr. Cole Brokamp
- Child Opportunity Index - diversitydatakids.org

---

**Version**: 1.0.1
**Release Date**: October 27, 2025
**Platform**: macOS (Intel & Apple Silicon)
