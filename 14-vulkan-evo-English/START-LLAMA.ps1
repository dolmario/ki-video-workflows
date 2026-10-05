param([Parameter(Mandatory=$true)][string]$Installation,[Parameter(Mandatory=$true)][string]$ModelPath,[int]$Context=8192,[int]$GpuLayers=999,[int]$Port=8091)
$ErrorActionPreference = 'Stop'
if ($Context -lt 512 -or $Port -lt 1024 -or $Port -gt 65535 -or $GpuLayers -lt 0) { throw 'Invalid context, port or GPU layers.' }
$model = (Resolve-Path -LiteralPath $ModelPath).Path
if (-not (Test-Path -LiteralPath $model -PathType Leaf) -or [IO.Path]::GetExtension($model) -ne '.gguf') { throw 'Choose an existing supported GGUF file.' }
$root = (Resolve-Path -LiteralPath $Installation).Path
$servers = @(Get-ChildItem -LiteralPath (Join-Path $root 'runtime') -Recurse -File -Filter llama-server.exe)
if ($servers.Count -ne 1) { throw 'Server executable is not unique.' }
if (Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue) { throw 'Port occupied. Do not terminate another service.' }
Write-Host 'Verify free RAM/GPU memory and idle competing jobs. 999 layers does not create memory.'
if ((Read-Host 'Type START to confirm your resource check') -cne 'START') { throw 'Not started.' }
Set-Location -LiteralPath $servers[0].DirectoryName
& $servers[0].FullName -m $model -c $Context -ngl $GpuLayers --alias lokales-modell --host 127.0.0.1 --port $Port
if ($LASTEXITCODE -ne 0) { throw 'llama-server exited with an error.' }
