$ErrorActionPreference = 'Stop'
$tabletSerial = '1916b8f1'
$adbExecutable = (Get-Command adb -ErrorAction Stop).Source
$connectionState = & $adbExecutable -s $tabletSerial get-state 2>&1
if ($LASTEXITCODE -ne 0 -or ($connectionState -join '').Trim() -ne 'device') {
    throw '请连接本次优化的小米平板，并允许 USB 调试后再运行。'
}
# 原来未设置此项，删除后桌面会实时恢复默认的 1.0 响应比例。
& $adbExecutable -s $tabletSerial shell settings delete global transition_animation_duration_ratio
if ($LASTEXITCODE -ne 0) { throw '恢复动画参数失败。' }
Write-Host '已恢复原厂桌面动画响应时间。桌面预编译保留，应用和桌面布局不受影响。'
