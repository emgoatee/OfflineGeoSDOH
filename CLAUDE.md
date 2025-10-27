# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OfflineGeoLocator is a Flask web application that performs offline geocoding of US addresses and retrieves multiple Social Determinants of Health (SDOH) indices. The application operates entirely offline using pre-downloaded Census TIGER/Line shapefiles and CSV datasets.

**Key Purpose:** Given a US street address, the app geocodes it to latitude/longitude, determines the census tract, and looks up multiple health equity indices (SDI, SVI, ADI, ACS Deprivation Index, Brokamp ADI, and COI).

## Development Commands

### Setup and Running

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask development server
python app.py

# Access the application at http://localhost:5000
```

### Building Standalone Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build the executable (creates dist/OfflineGeoLocator)
pyinstaller OfflineGeoLocator.spec

# The executable will be in the dist/ directory
# It bundles the entire app, data files, and templates
```

## Application Architecture

### Two-Stage Geocoding Process

The application uses a two-stage offline geocoding approach:

1. **Address → Lat/Lon** (`offline_geocode()` function in app.py:101-134)
   - Parses street address into number and street name
   - Normalizes street names (e.g., "Street" → "st", "Avenue" → "ave")
   - Searches county-level TIGER/Line addrfeat shapefiles (`tl_2022_{state_fips}{county_fips}_addrfeat.shp`)
   - Matches address number to street segment ranges (LFROMADD-LTOADD, RFROMADD-RTOADD)
   - Interpolates position along the matched street segment
   - Returns longitude and latitude

2. **Lat/Lon → Census Tract** (`latlon_to_geoid()` function in app.py:136-147)
   - Creates a Point geometry from coordinates
   - Spatially joins point to state-level census tract boundaries (`tl_2022_{state_fips}_tract.shp`)
   - Returns 11-digit GEOID (census tract FIPS code)

### Multi-Level FIPS Lookup Strategy

The `lookup_any_fips()` function (app.py:150-156) implements a fallback strategy for finding matches in datasets with varying FIPS code precision:
- Tries 11-digit FIPS (full census tract)
- Falls back to 10-digit FIPS
- Falls back to 9-digit FIPS (county level)

This handles inconsistencies in source data formatting.

### Data Sources and Lookup Functions

Each health index has a dedicated lookup function in app.py:

- **SDI** (Social Deprivation Index): `lookup_sdi()` - Returns SDI score and category
- **SVI** (Social Vulnerability Index): `lookup_svi()` - Returns poverty and minority percentiles, theme scores
- **ADI** (Area Deprivation Index): `lookup_adi()` - Returns national and state rankings
- **ACS**: `lookup_acs()` - Returns median income and deprivation index
- **Brokamp ADI**: `lookup_brokamp()` - ZIP code-based lookup (not tract-based)
- **COI** (Child Opportunity Index): `lookup_coi()` - Returns national scores and subdomains (education, health, social/economic)

### Data Files Structure

The `data/` directory contains:
- **Census tract boundaries**: `tl_2022_{state_fips}_tract.shp` - One shapefile per state/territory
- **Address features**: `tl_2022_{state_fips}{county_fips}_addrfeat.shp` - County-level address ranges for geocoding
- **Health indices CSV files**:
  - `geodata.csv` - SDI data
  - `SVI_2022_US.csv` - Social Vulnerability Index
  - `adi.csv` - Area Deprivation Index
  - `ACS_deprivation_index.csv` - ACS data by tract
  - `ACS_deprivation_index_by_zipcode.csv` - Brokamp ADI by ZIP
  - `COI_subdomin_data.xlsx` - Child Opportunity Index

### State and FIPS Code Handling

The application supports all 50 states plus US territories (AS, GU, MP, PR, VI). State FIPS codes are mapped in `STATE_FIPS` dictionary (app.py:25-34).

### Resource Path Helper

The `resource_path()` function (app.py:10-14) enables compatibility between:
- Development mode: Uses local file paths
- PyInstaller executable: Uses temporary `_MEIPASS` directory where bundled files are extracted

## Key Implementation Details

### Address Normalization

The `clean_street_name()` function (app.py:39-48) standardizes street names by:
- Converting to lowercase
- Removing punctuation
- Replacing common suffixes (Street → st, Avenue → ave, etc.)
- Replacing directional prefixes (North → n, South → s, etc.)

This improves matching success when user input varies from shapefile data.

### Address Range Matching

The application handles two TIGER/Line schema variants:
- Newer format: LFROMADD, LTOADD, RFROMADD, RTOADD
- Older format: LFROMHN, LTOHN, RFROMHN, RTOHN

The `get_addr_range_cols()` function (app.py:58-62) detects the schema and returns the correct column names.

### Flask Route Structure

Single route `/` (app.py:221-275):
- GET: Displays empty form
- POST: Processes address submission, performs geocoding and lookups, returns results

Results are passed to the Jinja2 template with separate variables for each index type.

## Common Development Patterns

### Adding a New Health Index

To add a new health index dataset:

1. Place the CSV/Excel file in the `data/` directory
2. Load it at module level (around app.py:71-82) with proper FIPS/GEOID formatting
3. Create a lookup function following the pattern of `lookup_sdi()`, `lookup_adi()`, etc.
4. Call the lookup function in the POST handler (app.py:247-252)
5. Pass the result to the template (app.py:263-275)
6. Update `templates/index.html` to display the new data

### Testing Geocoding

The application prints detailed logs to console during geocoding:
- Successful matches show: street name, address range, ZIP codes, and coordinates
- Failed matches show: "No addrfeat files found" or return None

Review console output when debugging geocoding issues.

## Known Limitations

- **Address matching**: Only works for addresses in the TIGER/Line database (generally works well for most US addresses)
- **ZIP code**: Not strictly required but improves matching accuracy
- **City field**: Currently collected but not used in geocoding logic
- **Performance**: Initial startup loads all state tract shapefiles into memory (takes 30-60 seconds)
- **Data currency**: Based on 2022 Census TIGER/Line files

## Dependencies

Core spatial libraries:
- **geopandas**: Spatial data operations (reading shapefiles, spatial joins)
- **shapely**: Geometric operations (Point creation, contains checks)
- **pandas**: Tabular data manipulation
- **Flask**: Web framework
- **pyogrio/fiona**: Shapefile reading backends

Note: `geopy` is listed in requirements.txt but not currently used in the code.
