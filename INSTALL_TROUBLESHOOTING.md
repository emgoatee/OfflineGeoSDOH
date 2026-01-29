# Mac Installation Troubleshooting (Coworkers & Other Macs)

This guide explains why the app may not install or open on other Macs and how to fix it.

---

## Why Installation Fails on Other Macs

### 1. **Gatekeeper blocking (most common)**

macOS blocks apps that are not **signed** and **notarized** by Apple. When a coworker downloads the app (ZIP or PKG) and double-clicks it, they may see:

- *"Offline GEO-SDOH can't be opened because it is from an unidentified developer"*
- *"Apple cannot check it for malicious software"*
- *"The app is damaged and can't be opened"* (sometimes shown when Gatekeeper blocks)

**Cause:** The build was created without Apple Developer signing/notarization (no `.env` with credentials), or the distributed file is the unsigned PKG instead of the notarized ZIP.

### 2. **Quarantine attribute**

Files downloaded from the internet (e.g. from GitHub, email, or shared drive) get a **quarantine** flag. macOS uses this to trigger security prompts or block execution.

**Cause:** The app was downloaded from a browser or transferred from another machine; the system marks it as “from the internet.”

### 3. **Wrong architecture (Intel vs Apple Silicon)**

The app is built for **one** CPU architecture (either Intel **x86_64** or Apple Silicon **arm64**). If you build on an Intel Mac, the app will not run on M1/M2/M3 Macs, and vice versa.

**Cause:** PyInstaller is built with `target_arch=None` (current machine only). There is no universal binary.

### 4. **Missing executable in the app bundle**

The `.app` must contain `OfflineGeoLocator_executable` inside `Contents/Resources/`. If someone only copies the repo or an incomplete build (e.g. without running PyInstaller and copying the executable into the installer app), the launcher will fail.

**Cause:** The executable is in `.gitignore` and is only present after a full build; sharing the repo or an incomplete ZIP omits it.

---

## Recommended Solutions

### For you (person building and distributing)

1. **Sign and notarize the app (best fix for Gatekeeper)**  
   - Use an Apple Developer account (Developer ID Application + notarization).  
   - In the project root, create a `.env` from `signing_credentials.template.env` and fill in:
     - `APPLE_SIGNING_IDENTITY`
     - `APPLE_ID`, `APPLE_PASSWORD`, `APPLE_TEAM_ID`
     - (Optional) `APPLE_INSTALLER_IDENTITY` for the PKG.
   - Run the full build so that the **ZIP** is signed and notarized:
     - Build the core executable: `pyinstaller OfflineGeoLocator_core.spec`
     - Copy `dist/OfflineGeoLocator` into `installer/Offline GEO-SDOH.app/Contents/Resources/` and rename it to `OfflineGeoLocator_executable`
     - Run `./build_installer.sh`
   - **Distribute the notarized ZIP** (`OfflineGeoLocator-v1.1.4-macOS.zip`), not the PKG, so coworkers get the signed/notarized app.  
   - In README/INSTALLER_GUIDE, tell users to install from the **ZIP** (extract and move the app to Applications).

2. **Support both Intel and Apple Silicon**  
   - Build on **both** an Intel Mac and an Apple Silicon Mac (or use two build machines/CI).  
   - Produce two ZIPs, e.g.:
     - `OfflineGeoLocator-v1.1.4-macOS-Intel.zip`
     - `OfflineGeoLocator-v1.1.4-macOS-AppleSilicon.zip`
   - In release notes, tell users to pick the one that matches their Mac (About This Mac → Chip).

3. **Document the one-time “Open Anyway” flow**  
   - Even with signing, some environments (e.g. strict MDM or first-time open) may show a prompt.  
   - In INSTALLER_GUIDE/README, add short steps: **Right-click the app → Open** (first time), or **System Settings → Privacy & Security → Open Anyway** if a message appears.

### For coworkers (when the app is still blocked)

Use these only if the app is safe and from your organization.

1. **Right-click → Open (first launch)**  
   - Right-click (or Control+click) the app → **Open** → **Open** in the dialog.  
   - This allows this specific app once; no need to disable Gatekeeper globally.

2. **Remove quarantine (advanced)**  
   - In Terminal, for the **downloaded** app (e.g. in Downloads or the extracted folder):
     ```bash
     xattr -cr "/path/to/Offline GEO-SDOH.app"
     ```
   - Then open the app as usual (double-click or Right-click → Open).

3. **System Settings → Privacy & Security**  
   - If macOS shows a message that the app was blocked, open **System Settings → Privacy & Security**.  
   - At the bottom, if the app is listed, click **Open Anyway** and confirm.

4. **Use the correct build**  
   - If the app doesn’t start or says something like “cannot be opened” or “inappropriate architecture,” they may need the other architecture build (Intel vs Apple Silicon). Provide the matching ZIP and instructions (e.g. “If you have M1/M2/M3, use the Apple Silicon download”).

---

## Quick checklist before sharing with coworkers

- [ ] App was built with **signing and notarization** (`.env` set, `build_installer.sh` run to completion).
- [ ] You’re sharing the **notarized ZIP** (e.g. `OfflineGeoLocator-v1.1.4-macOS.zip`), not only the PKG.
- [ ] You have a build for **their Mac type** (Intel and/or Apple Silicon) and tell them which to use.
- [ ] README or INSTALLER_GUIDE says: extract ZIP → move app to Applications → first time: **Right-click → Open** if macOS blocks it.
- [ ] Coworkers know that the executable is inside the app bundle (they should install the whole `.app`, not move individual files).

---

## Summary

| Problem              | Solution (you)                          | Solution (coworker)                |
|----------------------|------------------------------------------|------------------------------------|
| Gatekeeper blocking  | Sign + notarize; distribute the ZIP      | Right-click → Open; Open Anyway    |
| Quarantine           | Same as above; notarization helps        | `xattr -cr "…/App.app"`            |
| Wrong architecture   | Build and ship both Intel + Apple Silicon| Download the correct ZIP           |
| App won’t start      | Ensure executable is in the app bundle   | Re-download full ZIP from you      |

After you sign/notarize and ship the right ZIP(s) with short instructions, most “can’t install” issues on coworker Macs should be resolved.
