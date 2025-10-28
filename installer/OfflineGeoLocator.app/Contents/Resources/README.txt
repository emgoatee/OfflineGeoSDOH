OfflineGeoLocator - Core Application
======================================

This is the core application (175MB) without state data files.

GETTING STARTED
---------------

1. DOWNLOAD STATE PACKAGES
   You need to download state packages for the states you'll be geocoding.

   Option A - Use the downloader utility (recommended):
   - Run: python download_states.py
   - Follow the prompts to download states interactively

   Option B - Manual download:
   - Download state ZIP files from: https://github.com/emgoatee/OfflineGeoSDOH/releases
   - Extract state files into the 'data' folder next to this executable

   Option C - Download core data first:
   - Download core_data.zip from releases
   - Extract into 'data' folder
   - Then download individual state packages as needed

2. RUN THE APPLICATION
   - Double-click the OfflineGeoLocator executable
   - OR run from terminal: ./OfflineGeoLocator
   - Open your web browser to: http://localhost:5001

3. ENTER AN ADDRESS
   - Fill in the address form with a US street address
   - The address must be in a state for which you've downloaded data
   - Click "Geocode Address" to get health index data

FILE SIZES
----------
Core App: 175MB (this file)
core_data.zip: 112MB (required CSV/Excel data)
Each State: 29KB - 201MB (varies by state)

Examples:
- Minimum setup: 287MB (core app + core data, no states)
- Ohio + Pennsylvania + New York: ~750MB total
- All 56 states/territories: ~3.2GB total

WHAT'S INCLUDED
---------------
This core app includes:
- Flask web application
- Geocoding engine
- Health index lookup functions
- CSV data files (SDI, SVI, ADI, COI, etc.)

What you need to download:
- State shapefiles for geocoding (download per state)

AVAILABLE HEALTH INDICES
-------------------------
- Social Deprivation Index (SDI)
- Social Vulnerability Index (SVI)
- Area Deprivation Index (ADI)
- Brokamp Area Deprivation Index (by ZIP)
- Child Opportunity Index (COI)

TROUBLESHOOTING
---------------
Q: "Address not found"
A: Make sure you've downloaded the state package for that address's state

Q: Port 5001 already in use
A: Another application is using port 5001. Close it or modify app.py

Q: Application won't start
A: Check that you have the 'data' folder with at least core_data files

SUPPORT
-------
GitHub: https://github.com/emgoatee/OfflineGeoSDOH
Issues: https://github.com/emgoatee/OfflineGeoSDOH/issues
Documentation: See DEPLOYMENT.md in the repository

Version: 1.0.0
Build: Core (Modular)
