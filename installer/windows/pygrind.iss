; PyGrind Inno Setup Script
; Builds a Windows installer from the PyInstaller dist/pygrind output.
;
; Prerequisites:
;   1. Build with: python scripts/build.py
;   2. Download embedded Python: python installer/windows/embed_python.py
;   3. Compile this script with Inno Setup 6+
;
; Output: dist/PyGrind-Setup.exe

#define AppName "PyGrind"
#define AppVersion "1.0.0"
#define AppPublisher "PyGrind Project"
#define AppExeName "pygrind.exe"
#define AppURL "https://github.com/pygrind/pygrind"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
LicenseFile=..\..\LICENSE
OutputDir=..\..\dist
OutputBaseFilename=PyGrind-Setup
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\{#AppExeName}
UninstallDisplayName={#AppName}
ArchitecturesAllowed=x64compatible
ArchitecturesInstallMode=x64compatible
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; PyInstaller output — the bundled application
Source: "..\..\dist\pygrind\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Embedded Python runtime for code execution
Source: "python-embed\*"; DestDir: "{app}\python-embed"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
