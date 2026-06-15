param(
  [Parameter(Mandatory = $false)]
  [string]$OutputDir = "E:\codex"
)

$ErrorActionPreference = "Stop"

function Normalize-OutputDir {
  param([string]$Path)
  $p = $Path.Trim()
  $p = $p -replace "/", "\"
  if ($p -match "^[A-Za-z];\\") {
    $p = $p.Substring(0, 1) + ":\\" + $p.Substring(3)
  }
  if ($p -notmatch "^[A-Za-z]:\\") {
    throw "Invalid output path format: $Path . Use Windows absolute format, for example E:\codex"
  }
  return $p.TrimEnd("\")
}

$normalized = Normalize-OutputDir -Path $OutputDir
New-Item -ItemType Directory -Path $normalized -Force | Out-Null

$prefPath = Join-Path $normalized "codex_output_preference.txt"
@"
default_output_dir=$normalized\
path_style=windows_absolute
updated_at=$(Get-Date -Format "yyyy-MM-dd")
"@ | Set-Content -Path $prefPath -Encoding ASCII

$profilePath = $PROFILE
$profileDir = Split-Path -Parent $profilePath
if (-not (Test-Path $profileDir)) {
  New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
}

$beginMarker = "# Codex local output defaults (managed) BEGIN"
$endMarker = "# Codex local output defaults (managed) END"
$managedBlock = @"
$beginMarker
`$env:CODEX_OUTPUT_DIR = '$normalized'
if (-not (Test-Path `$env:CODEX_OUTPUT_DIR)) {
  New-Item -ItemType Directory -Path `$env:CODEX_OUTPUT_DIR -Force | Out-Null
}
function Get-CodexOutputDir {
  return `$env:CODEX_OUTPUT_DIR
}
Set-Alias -Name codex-out -Value Get-CodexOutputDir -Force
$endMarker
"@

$profileExisting = if (Test-Path $profilePath) { Get-Content $profilePath -Raw } else { "" }
$legacyPattern = '(?ms)^# Codex local output defaults \(managed\)\r?\n\$env:CODEX_OUTPUT_DIR = ''.*?''\r?\nif \(-not \(Test-Path \$env:CODEX_OUTPUT_DIR\)\) \{\r?\n  New-Item -ItemType Directory -Path \$env:CODEX_OUTPUT_DIR -Force \| Out-Null\r?\n\}\r?\nfunction Get-CodexOutputDir \{\r?\n  return \$env:CODEX_OUTPUT_DIR\r?\n\}\r?\nSet-Alias -Name codex-out -Value Get-CodexOutputDir -Force\r?\n?'
$profileExisting = [regex]::Replace($profileExisting, $legacyPattern, "")
if ($profileExisting.Contains($beginMarker)) {
  $idx = $profileExisting.IndexOf($beginMarker)
  if ($idx -gt 0) {
    $prefix = $profileExisting.Substring(0, $idx)
    $prefix = [regex]::Replace($prefix, '(?ms)^# Codex local output defaults \(managed\)\r?\n.*?Set-Alias -Name codex-out -Value Get-CodexOutputDir -Force\r?\n\r?\n?', '')
    $profileExisting = $prefix + $profileExisting.Substring($idx)
  }
}
if ($profileExisting -match [regex]::Escape($beginMarker) -and $profileExisting -match [regex]::Escape($endMarker)) {
  $pattern = "(?s)" + [regex]::Escape($beginMarker) + ".*?" + [regex]::Escape($endMarker)
  $profileUpdated = [regex]::Replace($profileExisting, $pattern, $managedBlock)
  Set-Content -Path $profilePath -Value $profileUpdated -Encoding ASCII
} else {
  if ($profileExisting.Trim().Length -gt 0) {
    Add-Content -Path $profilePath -Value "`r`n$managedBlock"
  } else {
    Set-Content -Path $profilePath -Value $managedBlock -Encoding ASCII
  }
}

$memoryDir = Join-Path $env:USERPROFILE ".codex\memories\extensions\ad_hoc\notes"
if (Test-Path $memoryDir) {
  $stamp = Get-Date -Format "yyyyMMdd-HHmm"
  $memoryPath = Join-Path $memoryDir "$stamp-codex-output-default.md"
  @"
# Codex output default preference

- user_preference: default local output directory is $normalized\
- path_normalization: use Windows absolute path format ($normalized\)
- set_at: $(Get-Date -Format "yyyy-MM-dd")
- scope: local Codex desktop workflow
"@ | Set-Content -Path $memoryPath -Encoding UTF8
}

. $PROFILE

Write-Output "OUTPUT_DIR=$normalized"
Write-Output "PREFERENCE_FILE=$prefPath"
Write-Output "PROFILE_PATH=$profilePath"
Write-Output "CODEX_OUTPUT_DIR=$env:CODEX_OUTPUT_DIR"
Write-Output "ALIAS_CodexOut=$(codex-out)"
