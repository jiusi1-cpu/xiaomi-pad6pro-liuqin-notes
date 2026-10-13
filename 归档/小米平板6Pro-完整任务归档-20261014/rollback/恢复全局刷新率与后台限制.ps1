$ErrorActionPreference = 'Stop'
$tabletSerial = '1916b8f1'
$adbPath = (Get-Command adb -ErrorAction Stop).Source
& $adbPath -s $tabletSerial get-state
if ($LASTEXITCODE -ne 0) { throw '请连接平板并允许 USB 调试。' }
& $adbPath -s $tabletSerial shell "su -c '/data/adb/ksud module disable liuqin120'"
if ($LASTEXITCODE -ne 0) { throw '停用配置模块失败，请检查 root 授权。' }
& $adbPath -s $tabletSerial shell "su -c 'sh /data/adb/modules/liuqin120/restore.sh'"
if ($LASTEXITCODE -ne 0) { throw '恢复失败，已停用模块；请在 KernelSU 中核对。' }
& $adbPath -s $tabletSerial reboot
if ($LASTEXITCODE -ne 0) { throw '设置已恢复，但重启失败；请手动重启平板。' }
Write-Host '已恢复此前的 144Hz 设置和所选应用的后台权限，并重启平板。KSU、机型配置和 Scene 保留。'
