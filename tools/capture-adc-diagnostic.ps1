param(
    [string]$HostName = "decca.local",
    [int]$Port = 4242,
    [string]$OutputDirectory = ".\diagnostics"
)

$ErrorActionPreference = "Stop"
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$rawPath = Join-Path $OutputDirectory "adc-noise-$stamp.csv"
$summaryPath = Join-Path $OutputDirectory "adc-noise-$stamp-summary.md"

$client = [System.Net.Sockets.TcpClient]::new()
$client.Connect($HostName, $Port)
$reader = [System.IO.StreamReader]::new($client.GetStream())

$summary = [System.Collections.Generic.List[string]]::new()
try {
    while (($line = $reader.ReadLine()) -ne $null) {
        Write-Host $line
        if ($line.StartsWith("#")) {
            $summary.Add($line.Substring(1).Trim())
        } else {
            Add-Content -LiteralPath $rawPath -Value $line -Encoding utf8
        }
    }
} finally {
    $reader.Dispose()
    $client.Dispose()
}

$report = @(
    "# Decca ADC noise diagnostic"
    ""
    "Captured: $(Get-Date -Format o)"
    "Raw data: $rawPath"
    ""
    "## Device output"
    ""
) + $summary
$report | Set-Content -LiteralPath $summaryPath -Encoding utf8

Write-Host "Raw log: $rawPath"
Write-Host "Summary: $summaryPath"
