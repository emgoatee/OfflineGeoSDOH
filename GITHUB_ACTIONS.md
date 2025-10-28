# GitHub Actions - Automated Builds

This repository uses GitHub Actions to automatically build the Windows version in the cloud. No Windows machine required!

## How It Works

GitHub Actions runs your builds on Microsoft's servers. When you push a new version tag, it automatically:

1. ✅ Sets up a Windows environment
2. ✅ Installs Python and dependencies
3. ✅ Builds the executable with PyInstaller
4. ✅ Creates the installer with Inno Setup
5. ✅ Uploads the installer to your GitHub Release

**Cost:** FREE for public repositories (unlimited minutes)

## Two Workflows

### 1. `build-windows.yml` - Windows Build Only
- Builds Windows installer
- Uploads as artifact
- Triggered on version tags or manually

### 2. `create-release.yml` - Full Release
- Builds Windows installer
- Creates GitHub Release
- Auto-generates release notes
- Triggered on version tags or manually

## How to Use

### Method 1: Create a New Release (Recommended)

1. **Update version in files** (if needed):
   - `installer/Distribution.xml` - Mac installer version
   - `installer_windows.iss` - Windows installer version
   - `README.md` - Documentation

2. **Commit and push changes**:
   ```bash
   git add .
   git commit -m "Prepare for v1.0.1 release"
   git push
   ```

3. **Create and push a version tag**:
   ```bash
   git tag -a v1.0.1 -m "Release v1.0.1"
   git push origin v1.0.1
   ```

4. **Wait for build to complete** (5-10 minutes)
   - Go to: https://github.com/emgoatee/OfflineGeoSDOH/actions
   - Watch the workflow run

5. **Build your Mac installer locally**:
   ```bash
   ./build_installer.sh
   ```

6. **Upload Mac installer to the release**:
   - Go to: https://github.com/emgoatee/OfflineGeoSDOH/releases
   - Find your release (created automatically)
   - Click "Edit release"
   - Upload `OfflineGeoLocator-Installer-v1.0.1.pkg`
   - Also upload `core_data.zip` and state packages
   - Click "Update release"

### Method 2: Manual Trigger (Testing)

1. Go to: https://github.com/emgoatee/OfflineGeoSDOH/actions

2. Click on "Build Windows Installer" or "Create Multi-Platform Release"

3. Click "Run workflow"

4. Enter version (if prompted)

5. Click "Run workflow" button

6. Wait for completion

7. Download artifacts from the workflow run

## Viewing Build Status

### Check if a build is running:
1. Go to: https://github.com/emgoatee/OfflineGeoSDOH/actions
2. You'll see all workflow runs and their status

### Download build artifacts (for testing):
1. Click on a completed workflow run
2. Scroll down to "Artifacts"
3. Download `windows-installer`

## Troubleshooting

### Build Failed - Missing Data Files

**Problem:** Build completes but app doesn't work because data files are missing.

**Solution:** The automated build doesn't include the 11GB of shapefiles (too large for GitHub). This is by design. Users download state data separately on first run.

**If you need to test the full build:**
1. Download artifacts from GitHub Actions
2. Test the installer on a Windows VM
3. Use the state downloader to fetch data

### Build Failed - Python Errors

**Problem:** Build fails during PyInstaller step.

**Solution:**
- Check `requirements.txt` includes all dependencies
- Make sure `OfflineGeoLocator_windows.spec` is correct
- Look at the error in the Actions log

### Build Failed - Inno Setup Error

**Problem:** Installer creation fails.

**Solution:**
- Verify `installer_windows.iss` references the correct files
- Make sure `LICENSE` file exists
- Check that `dist\OfflineGeoSDOH.exe` was created

### Can't Find the Installer

**Problem:** Build succeeded but can't find the installer.

**Solution:**
- If building from a tag: Check the Releases page
- If manual trigger: Download from workflow artifacts
- Look for `OfflineGeoSDOH-Installer-v*-Windows.exe`

## What Gets Built

### Windows Installer Includes:
- ✅ Python executable (bundled)
- ✅ All Python dependencies
- ✅ Flask web server
- ✅ Templates (HTML/CSS)
- ✅ Core health indices CSV files
- ✅ State downloader utility
- ❌ State shapefiles (too large - downloaded separately)

### File Sizes:
- **Executable**: ~180MB
- **Installer**: ~180MB
- **Total with all states**: ~3.4GB (downloaded separately)

## Building Both Platforms

### Current Workflow:
1. **Windows**: Automated via GitHub Actions ✅
2. **macOS**: Build locally on your Mac 🍎

### Why Mac isn't automated:
- GitHub Actions macOS runners can't create signed .pkg installers
- macOS requires code signing (needs Apple Developer account)
- Building on your Mac is simpler and faster

## Release Checklist

When creating a new release, make sure you:

- [ ] Update version numbers in relevant files
- [ ] Commit and push all changes
- [ ] Create and push version tag
- [ ] Wait for Windows build to complete
- [ ] Build Mac installer locally
- [ ] Test both installers
- [ ] Upload Mac installer to GitHub Release
- [ ] Upload core_data.zip
- [ ] Upload state packages (if changed)
- [ ] Update release notes if needed
- [ ] Announce the release!

## GitHub Actions Limits (Free Tier)

- **Public repos**: Unlimited minutes ✅
- **Private repos**: 2,000 minutes/month
- **Storage**: 500MB artifacts (we're well under this)
- **Retention**: 90 days (artifacts deleted after)

Since your repo is public, you have **unlimited builds** for free! 🎉

## Advanced: Customizing the Workflow

### To modify the Windows build:
1. Edit `.github/workflows/build-windows.yml`
2. Commit and push
3. Next build will use the updated workflow

### To add build notifications:
- Add email notifications
- Add Slack/Discord webhooks
- Configure in workflow YAML under `jobs:` > `steps:`

### To add automated testing:
- Add a test step before building
- Run `pytest` or other test framework
- Fail the build if tests fail

## Support

For GitHub Actions issues:
- Check the Actions tab for detailed logs
- Open an issue if builds are consistently failing
- Review GitHub Actions documentation: https://docs.github.com/en/actions

---

**Happy Building! 🚀**

You can now build Windows installers without ever touching a Windows machine!
