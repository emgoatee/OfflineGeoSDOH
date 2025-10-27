# Deployment Guide for OfflineGeoLocator

## Overview

This guide explains how to build and distribute the modular OfflineGeoLocator application.

## Modular Architecture

The application uses a modular packaging system to reduce download sizes:

- **Core App**: Application code + templates + CSV data (~600MB total)
- **State Packages**: Individual state shapefiles (29KB - 201MB each)
- **Total**: 3.2GB compressed (vs 11GB uncompressed original)

Users download only what they need!

## Step 1: Package State Data

From the project root:

```bash
python package_states.py
```

This creates `state_packages/` directory with:
- `core_data.zip` (112MB) - Required CSV/Excel files
- `state_XX.zip` (varies) - One per state/territory

**Output:**
- 57 ZIP files (1 core + 56 states/territories)
- Total size: ~3.2GB compressed

## Step 2: Build Core Application

### Option A: Build Locally

```bash
# Install PyInstaller
pip install pyinstaller

# Build for your current platform
pyinstaller OfflineGeoLocator_core.spec

# Result: dist/OfflineGeoLocator (or .exe on Windows)
```

### Option B: Use GitHub Actions (Recommended)

1. **Prerequisites:**
   - Code is pushed to GitHub
   - State packages are uploaded to a release or external storage

2. **Trigger Build:**
   ```bash
   # Create and push a version tag
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **GitHub Actions will:**
   - Build Mac and Windows core apps
   - Package state data (if data folder is available)
   - Upload to GitHub Release

## Step 3: Distribute Files

### Upload to GitHub Releases

1. Go to: https://github.com/emgoatee/OfflineGeoSDOH/releases
2. Create new release or edit existing
3. Upload files:
   - `OfflineGeoLocator-Core-macOS.zip`
   - `OfflineGeoLocator-Core-Windows.zip`
   - `core_data.zip` (required)
   - All `state_XX.zip` files

### Alternative: External Hosting

For large state packages, consider:
- AWS S3 bucket
- Google Cloud Storage
- Dropbox/Google Drive with public links

Update `download_states.py` to point to your storage URLs.

## Step 4: User Installation

Users follow these steps:

1. **Download Core App**
   - Download platform-specific ZIP from releases
   - Extract

2. **Download Core Data**
   - Download `core_data.zip`
   - Extract into `data/` folder next to executable

3. **Download States**
   - Option A: Manually download state ZIPs and extract to `data/`
   - Option B: Use `download_states.py` utility

4. **Run**
   - Execute the app
   - Browse to http://localhost:5001

## File Size Reference

| Component | Size | Required |
|-----------|------|----------|
| Core App (Mac/Win) | ~500MB | Yes |
| core_data.zip | 112MB | Yes |
| state_AL.zip | 22MB | Optional |
| state_AK.zip | 8.4MB | Optional |
| state_CA.zip | 201MB | Optional |
| state_TX.zip | ~150MB | Optional |
| ... (other states) | varies | Optional |

**Minimum install**: ~600MB (core app + core data, no states)
**Example install**: ~1.5GB (core + OH + PA + NY)
**Full install**: ~3.8GB (core + all 56 states/territories)

## Handling Large Data in Git

### Option 1: Git LFS (Limited)

```bash
# Install Git LFS
brew install git-lfs  # macOS
# or download from https://git-lfs.github.com

# Initialize
git lfs install
git lfs track "state_packages/*.zip"
git add .gitattributes state_packages/
git commit -m "Add state packages with LFS"
```

**Limitations:**
- GitHub LFS: 1GB storage + 1GB/month bandwidth (free tier)
- Not practical for 3.2GB of state packages

### Option 2: Manual Upload (Recommended)

1. Build state packages locally: `python package_states.py`
2. Upload `state_packages/*.zip` to GitHub Release manually
3. Don't commit to git

### Option 3: External Storage

1. Upload state packages to S3/GCS/Dropbox
2. Update `GITHUB_RELEASE_URL` in `download_states.py`
3. Users download from external storage

## Troubleshooting

### Build Fails - Missing Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
```

### GitHub Actions - Workflow Scope Error

Your Personal Access Token needs `workflow` scope:
1. Settings → Developer settings → Personal access tokens
2. Create new token with `workflow` scope
3. Use when pushing workflow files

### State Packages Too Large

Consider:
- Compressing with higher compression (7zip ultra)
- Splitting largest states into regions
- Hosting externally (S3, GCS)

## Next Steps

1. **Test locally**: Build and test core app with a few states
2. **Create release**: Tag version and let GitHub Actions build
3. **Upload states**: Manually upload state packages to release
4. **Test distribution**: Download and test as end-user
5. **Document**: Update README with actual download links

## Continuous Deployment

For ongoing releases:

```bash
# Make changes
git add .
git commit -m "Description"

# Create new version
git tag v1.1.0
git push origin main v1.1.0

# GitHub Actions builds automatically
# Upload state_packages/*.zip to new release manually
```

## Support

For issues or questions:
- GitHub Issues: https://github.com/emgoatee/OfflineGeoSDOH/issues
- See README.md for user documentation
- See CLAUDE.md for development documentation
