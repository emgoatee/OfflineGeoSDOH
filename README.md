# OfflineGeoLocator

A Flask web application that performs offline geocoding of US addresses and retrieves multiple Social Determinants of Health (SDOH) indices.

## Features

- **Offline Geocoding**: Convert US street addresses to coordinates using Census TIGER/Line shapefiles
- **Multiple Health Indices**: Retrieve SDI, SVI, ADI, Brokamp ADI, and COI data
- **All 50 States + Territories**: Supports all US states and territories
- **Standalone Application**: Can be packaged as a standalone executable for Mac and Windows

## Development

### Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at http://localhost:5001

### Building Executables

#### Local Build

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller OfflineGeoLocator.spec
```

The executable will be in the `dist/` directory.

#### Automated Builds with GitHub Actions

This project uses GitHub Actions to automatically build executables for both Mac and Windows.

**To trigger a build:**

1. **Push a version tag:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Or manually trigger:**
   - Go to GitHub Actions tab
   - Select "Build Executables" workflow
   - Click "Run workflow"

**Built executables will be:**
- Attached as artifacts to the workflow run (available for 90 days)
- Attached to the GitHub Release (if triggered by a tag)

## Handling Large Data Files (11GB)

The `data/` folder contains 11GB of Census TIGER/Line shapefiles and is excluded from git. You have several options:

### Option 1: Git LFS (Recommended for GitHub)

```bash
# Install Git LFS
# macOS: brew install git-lfs
# Windows: Download from https://git-lfs.github.com

# Initialize Git LFS
git lfs install

# Track the data folder
git lfs track "data/**"
git add .gitattributes
git add data/
git commit -m "Add data files with Git LFS"
git push
```

**Note:** GitHub has LFS storage limits. Free accounts get 1GB storage/month bandwidth.

### Option 2: External Hosting

Upload the `data/` folder to:
- AWS S3
- Google Cloud Storage
- Dropbox/Google Drive

Then update the GitHub Actions workflow to download it during builds.

### Option 3: Manual Distribution

1. Build locally (since you have the data folder)
2. Manually upload executables to GitHub Releases
3. Share download links with users

## Application Structure

- `app.py` - Main Flask application with geocoding logic
- `templates/index.html` - Web interface
- `data/` - Census shapefiles and health index data (11GB)
- `OfflineGeoLocator.spec` - PyInstaller configuration
- `.github/workflows/build.yml` - GitHub Actions workflow

## For Users

1. Download the executable for your operating system from Releases
2. Extract the ZIP file
3. Run the executable
4. Open http://localhost:5001 in your web browser
5. Enter a US address to get health index data

## License

[Add your license here]

## Credits

Data sources:
- Census TIGER/Line Shapefiles (2022)
- Social Deprivation Index - Graham Center
- Social Vulnerability Index - CDC/ATSDR
- Area Deprivation Index - University of Wisconsin
- Brokamp Area Deprivation Index - Dr. Cole Brokamp
- Child Opportunity Index - diversitydatakids.org
