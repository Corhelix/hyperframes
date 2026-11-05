# Renders every scene and callout composition to a transparent ProRes 4444 .mov (video edit SOP v0.4, stage 12).
# Usage: powershell -ExecutionPolicy Bypass -File render-all.ps1 -Out F:\gravitate-video-edit\media\work\overlay\full-v0.1 [-Only s02,s17]
param(
  [Parameter(Mandatory = $true)][string]$Out,
  [string[]]$Only = @()
)
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$scenes = Get-Content (Join-Path $here 'scenes.json') -Raw | ConvertFrom-Json
New-Item -ItemType Directory -Force $Out | Out-Null
$log = Join-Path $Out 'render-log.txt'
"start $(Get-Date -Format s)" | Add-Content $log
$ok = 0; $bad = 0
foreach ($s in $scenes) {
  if ($Only.Count -gt 0 -and $Only -notcontains $s.id) { continue }
  $dir = Join-Path $here "scenes\$($s.id)"
  $mov = Join-Path $Out "$($s.id).mov"
  $t0 = Get-Date
  $o = cmd /c "npx --yes hyperframes@0.9.10 render `"$dir`" --format mov --fps 24 --quality looks --output `"$mov`" 2>&1"
  $dur = (& ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 $mov 2>$null)
  $secs = [math]::Round(((Get-Date) - $t0).TotalSeconds)
  if ((Test-Path $mov) -and $dur -and ([math]::Abs([double]$dur - [double]$s.dur) -lt 0.15)) { $ok++; "OK   $($s.id) $([math]::Round([double]$dur,3))s (want $($s.dur)) in ${secs}s" | Add-Content $log }
  else { $bad++; "FAIL $($s.id) dur=$dur want $($s.dur)`n$(($o | Select-Object -Last 6) -join "`n")" | Add-Content $log }
}
"done $(Get-Date -Format s) ok=$ok fail=$bad" | Add-Content $log
"ok=$ok fail=$bad"
