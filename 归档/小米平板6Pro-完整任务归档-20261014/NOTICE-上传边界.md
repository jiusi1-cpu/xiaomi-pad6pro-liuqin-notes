# 上传边界与材料说明

这份归档用于记录个人设备上的操作和验证。它同时包含用户提供的第三方资源、厂商系统镜像、KernelSU/应用安装包和设备调试证据。

## 建议公开到 GitHub 的内容

- 主题 Markdown 文档
- 精选验证 JSON 和去除敏感信息后的截图
- 本机模块脚本、回滚脚本和研究摘要
- `raw-materials-manifest.json` 中的文件索引

## 建议保留私有的内容

- `system.img`、`product.img`、`vendor.img` 等完整系统镜像
- 7 GB 级别的 OTA 临时包和 boot 分块
- KernelSU、MT、Scene 等 APK
- 第三方和平精英 PAK / SIG 资源
- 含设备序列号、完整调试日志、屏幕截图或账户信息的原始记录

上传前请检查仓库可见性、许可证和第三方分发条款。当前工作目录没有配置 Git remote，所以本轮只完成了本地整理和压缩，没有上传动作。
