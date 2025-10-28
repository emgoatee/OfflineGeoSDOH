; Inno Setup Script for Offline GEO-SDOH Windows Installer
; Download Inno Setup: https://jrsoftware.org/isinfo.php

#define MyAppName "Offline GEO-SDOH"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "GooteeMD"
#define MyAppURL "https://github.com/emgoatee/OfflineGeoSDOH"
#define MyAppExeName "OfflineGeoSDOH.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
AppId={{A5B6C7D8-E9F0-1A2B-3C4D-5E6F7A8B9C0D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=.
OutputBaseFilename=OfflineGeoSDOH-Installer-v{#MyAppVersion}-Windows
SetupIconFile=SDOH_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\OfflineGeoSDOH.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  MsgBox('Welcome to Offline GEO-SDOH Setup!' + #13#10 + #13#10 +
         'This will install the application on your computer.' + #13#10 + #13#10 +
         'After installation, you will need to download state data packages on first launch.',
         mbInformation, MB_OK);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create data directory in user's AppData
    CreateDir(ExpandConstant('{userappdata}\OfflineGeoSDOH\data'));
  end;
end;
