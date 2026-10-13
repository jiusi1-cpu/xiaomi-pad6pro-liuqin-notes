# 刷机与 KernelSU

## 设备与系统

- 设备：小米平板 6 Pro，型号 `23046RP50C`，代号 `liuqin`
- 系统：HyperOS `OS3.0.7.0.VMYCNXM`，Android 15
- Bootloader：已解锁并现场验证
- 活动槽位：`_a`
- 内核：`5.10.236-android12-9`

## 已完成

1. 从设备当前已安装系统分区提取官方镜像，并对操作过程和最终 boot 分区做 SHA-256 校验。
2. 使用官方 KernelSU v3.3.1 build 32680 的 Android 12 / 5.10 LKM 资源对原厂 boot 做补丁。
3. 刷入补丁 boot，正常启动后验证 KernelSU 管理器、`ksud` 和 UID 0 root。
4. 保留原厂内核、原始 init 和 boot 元数据；同时保留 stock boot 作为回退材料。

## 关键文件

- `firmware/boot-stock-OS3.0.7.0.VMYCNXM.img`
- `firmware/boot-KernelSU-v3.3.1-OS3.0.7.0.VMYCNXM.img`
- `firmware/KernelSU_v3.3.1_32680-release.apk`
- `evidence/boot-verification.json`
- `evidence/device-extraction.json`

## 验证结论

补丁 boot 在正常启动中生效，root 权限可用，MT 和 Scene 的 root 授权也在此基础上完成。这里记录的是已验证结果，不代表对后续系统 OTA、第三方模块兼容性或游戏账号风险作保证。
