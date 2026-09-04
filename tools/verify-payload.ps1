[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$utf8 = [Text.UTF8Encoding]::new($false)
$repository = (Resolve-Path -LiteralPath (Split-Path -Parent $PSScriptRoot)).Path.TrimEnd('\')
$releasePath = Join-Path $repository 'governance\RELEASE.json'
$manifestPath = Join-Path $repository 'governance\PAYLOAD-MANIFEST.csv'
$release = [IO.File]::ReadAllText($releasePath, $utf8) | ConvertFrom-Json -Depth 20
$payload = (Resolve-Path -LiteralPath (Join-Path $repository ([string]$release.payload.path))).Path.TrimEnd('\')
[object[]]$rows = @(Import-Csv -LiteralPath $manifestPath)
[object[]]$actual = @(Get-ChildItem -LiteralPath $payload -Force -Recurse -File)
[object[]]$reparse = @(Get-ChildItem -LiteralPath $payload -Force -Recurse | Where-Object { ($_.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0 })
$map = [Collections.Generic.Dictionary[string,object]]::new([StringComparer]::Ordinal)
foreach ($file in $actual) {
    $relative = [IO.Path]::GetRelativePath($payload, $file.FullName).Replace('\', '/')
    $map.Add($relative, $file)
}
$issues = [Collections.Generic.List[string]]::new()
$normalized = [Collections.Generic.List[string]]::new()
foreach ($row in $rows) {
    $relative = [string]$row.relative_path
    if (-not $map.ContainsKey($relative)) { $issues.Add("missing:$relative"); continue }
    $file = $map[$relative]
    $sha = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    if ([int64]$file.Length -ne [int64]$row.size) { $issues.Add("size:$relative") }
    if ($sha -cne [string]$row.sha256) { $issues.Add("sha256:$relative") }
    $normalized.Add("$relative|$($file.Length)|$sha")
    [void]$map.Remove($relative)
}
foreach ($extra in $map.Keys) { $issues.Add("extra:$extra") }
if ($reparse.Count -gt 0) { $issues.Add("reparse-items:$($reparse.Count)") }
$digest = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($utf8.GetBytes(($normalized -join "`n")))).ToLowerInvariant()
if ($rows.Count -ne [int]$release.payload.file_count) { $issues.Add('manifest-file-count') }
if ($actual.Count -ne [int]$release.payload.file_count) { $issues.Add('actual-file-count') }
if ($digest -cne [string]$release.payload.normalized_sha256) { $issues.Add('normalized-sha256') }
$result = [pscustomobject][ordered]@{
    status = if ($issues.Count -eq 0) { 'PASS' } else { 'FAIL' }
    payload = $payload
    manifest_rows = $rows.Count
    actual_files = $actual.Count
    normalized_sha256 = $digest
    issues = @($issues)
}
$result | ConvertTo-Json -Depth 20
if ($issues.Count -gt 0) { exit 1 }
