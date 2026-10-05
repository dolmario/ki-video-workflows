# Pinned official example release; not freshly installed for this video.
param([string]$Destination = (Join-Path $PWD 'Dolmario-Vulkan'))
$ErrorActionPreference = 'Stop'
if (Test-Path -LiteralPath $Destination) { throw 'Destination exists. Choose a NEW folder.' }
New-Item -ItemType Directory -Path $Destination | Out-Null
$root = (Resolve-Path -LiteralPath $Destination).Path
$archive = Join-Path $root 'llama-vulkan.zip'
$url = 'https://github.com/ggml-org/llama.cpp/releases/download/b11078/llama-b11078-bin-win-vulkan-x64.zip'
Invoke-WebRequest -Uri $url -OutFile $archive
$expected = '0649f258e140a8b3b1a4c58d863c317b0fd3427eed2e72132399dbde363df861'
if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expected) { throw 'Official archive SHA256 mismatch. Do not unpack.' }
Expand-Archive -LiteralPath $archive -DestinationPath (Join-Path $root 'runtime')
$servers = @(Get-ChildItem -LiteralPath (Join-Path $root 'runtime') -Recurse -File -Filter llama-server.exe)
if ($servers.Count -ne 1) { throw 'Server executable is not unique.' }
Set-Location -LiteralPath $servers[0].DirectoryName
& $servers[0].FullName --version
if ($LASTEXITCODE -ne 0) { throw 'Version check failed.' }
& $servers[0].FullName --list-devices
if ($LASTEXITCODE -ne 0) { throw 'Device check failed.' }
Write-Host 'Inspect Vulkan device listing. No model has been started. Read README before START-LLAMA.ps1.'
