# MT 管理器与 Scene

## 已安装与授权

- MT 管理器：`bin.mt.plus`，2.26.10；通过 KernelSU 授权后可读取 `/data/adb`，root 验证通过。
- Scene：`com.omarea.vtools`，9.4.11；root、CPU/GPU 监控和调度界面验证通过。
- Scene 的辅助服务在一次冷启动测试中被系统清掉，之后已恢复绑定；最终重启后没有发现 crashed services。

## EP 按钮问题的处理记录

Scene EP 配置已显示为可选特性并能打开。用户所说的“EP 旁边图标没有反应”没有被单独判定为硬件故障；在后续配置页和服务恢复后，相关调度配置可以保存和生效。

## 使用边界

Scene 的 CPU/GPU 观察和游戏配置保留；没有购买或兑换专业账号。后续测试避免再次强制停止 Scene，以免再次清理辅助服务状态。

## 证据

- `screenshots/MT-root-verified.png`
- `screenshots/Scene-root-authorized.png`
- `screenshots/Scene-EP-config-selector-verified.png`
- `screenshots/Scene-EP-features-verified.png`
- `screenshots/Scene-EP-ready.png`
- `evidence/Scene-accessibility-final.txt`
