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
$writer = [System.IO.StreamWriter]::new(
    $rawPath,
    $false,
    [System.Text.UTF8Encoding]::new($false)
)
$writer.AutoFlush = $true

$summary = [System.Collections.Generic.List[string]]::new()
$phaseCounts = @{}
try {
    while (($line = $reader.ReadLine()) -ne $null) {
        if ($line.StartsWith("#")) {
            Write-Host $line
            $summary.Add($line.Substring(1).Trim())
        } else {
            $writer.WriteLine($line)
            if (-not $line.StartsWith("time_ms,")) {
                $phase = ($line -split ',', 3)[1]
                $phaseCounts[$phase] = 1 + $phaseCounts[$phase]
                if (($phaseCounts[$phase] % 500) -eq 0) {
                    Write-Host "[$phase] $($phaseCounts[$phase]) samples captured"
                }
            }
        }
    }
} finally {
    $writer.Dispose()
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
