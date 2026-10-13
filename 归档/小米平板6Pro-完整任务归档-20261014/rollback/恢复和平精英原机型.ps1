$ErrorActionPreference = 'Stop'
$tabletSerial = '1916b8f1'
$adbCommand = Get-Command adb -ErrorAction Stop
& $adbCommand.Source -s $tabletSerial get-state
if ($LASTEXITCODE -ne 0) { throw '请连接原来的小米平板，并允许 USB 调试。' }
& $adbCommand.Source -s $tabletSerial shell "su -c '/data/adb/ksud module disable COPG'"
if ($LASTEXITCODE -ne 0) { throw '关闭机型伪装失败，请检查 root 授权。' }
& $adbCommand.Source -s $tabletSerial shell "su -c '/data/adb/ksud module disable zygisksu'"
if ($LASTEXITCODE -ne 0) { throw '关闭本次新增的依赖失败。' }
& $adbCommand.Source -s $tabletSerial reboot
if ($LASTEXITCODE -ne 0) { throw '重启失败；请手动重启平板。' }
Write-Host '已关闭本次机型伪装及其依赖。重启后和平精英恢复读取小米机型，KernelSU root 保留。'
