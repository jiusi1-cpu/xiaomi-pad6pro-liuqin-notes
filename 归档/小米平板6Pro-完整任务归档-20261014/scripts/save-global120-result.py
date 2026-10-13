from pathlib import Path
import json,zipfile,hashlib
base=Path('work/game-fps-research/prepared')
measure=json.loads((base/'final-reboot-aa-off-training90sec.json').read_text())
verification=json.loads((base/'final-reboot-verification.json').read_text())
allocation=json.loads((base/'final-game-allocation.json').read_text());allocation['scene_accessibility_bound']=True
(base/'final-game-allocation.json').write_bytes(json.dumps(allocation,ensure_ascii=False,indent=2).encode())
mod=base/'persistent120/module'
with zipfile.ZipFile('outputs/小米平板6Pro-全局120Hz与后台限制.zip') as z:
 for p in mod.iterdir():assert z.read(p.name)==p.read_bytes()
statepath=Path('work/STATE.json');state=json.loads(statepath.read_text(encoding='utf-8-sig'))
state['objective']='Global native120Hz and selected background limits across reboot; improve real game120FPS. Persistence verified; absolute sustained120FPS not achieved.'
state['latest_game_performance']={
 'module':'liuqin120 version1.2 enabled;23 background apps;23 UID restrictions and autostart verified after full reboot',
 'native_display':'SurfaceFlinger native mode0 1800x2880 actual120.00Hz; verified HOME and game',
 'game_graphics':'Fluent120FPS; anti-aliasing OFF confirmed saved via UI',
 'cpu_thread_masks':allocation['thread_masks'],
 'measurement_final':{k:v for k,v in measure.items() if k not in ['timestamps','polls']},
 'measurement_limit':'Final90sec training-ground capture; manual movement during this repeat not independently confirmed. Not whole-match or absolute120 proof.',
 'earlier_measurement_failure':'180sec user-operated trial failed on ADB call after150sec; only partial30sec printouts retained, not a complete benchmark. Approx114.6,117.6,117.4,118.4,107.6FPS; do not use as aggregatevalidated benchmark.',
 'shared_uid_protection':'com.miui.huanji UID6100 shared with com.miui.backup excluded; original package and UID modes restored',
 'scene_recovery':'CRLF numeric config crash corrected using LF and exact original file; accessibility bound, no crashed services after final reboot',
 'artifacts':['outputs/小米平板6Pro-全局120Hz与后台限制.zip','outputs/恢复全局刷新率与后台限制.ps1','outputs/和平精英120帧优化结果.md'],
 'remaining':'No absolute120FPS claim; frame p9916.66ms, occasional double intervals. No further CPU thermal or frequency experiments applied.'}
state['device']['last_battery_percent']=measure['health'][-1]['level']
statepath.write_bytes(json.dumps(state,ensure_ascii=False,indent=2).encode())
bins=measure['bins10sec'];mini=min(x['fps'] for x in bins);maxi=max(x['fps'] for x in bins)
summary=f'''# 小米平板6 Pro：120Hz 与和平精英优化结果

设备：小米平板6 Pro / liuqin；HyperOS OS3.0.7.0.VMYCNXM，Android15。2026-10-13 完成检查。

## 已应用并验证

- 已启用本机专用 KernelSU 模块 liuqin120 v1.2。完整重启后，桌面和游戏中的屏幕实际模式均为120.00Hz。
- 23 个指定应用限制后台活动及自启动，开机清理一次；逐项核对23项包级后台限制、UID级后台限制和自启动设置，全部通过。
- 保留桌面、系统服务、网络、游戏及 Scene 的必要运行权限。换机工具与系统备份共享UID6100，已排除并恢复权限。
- 所选应用没有卸载；手动打开仍可使用。其后台通知、自动同步会受到限制。
- Scene 开机后正常运行，无辅助服务崩溃。游戏主线程、渲染及RHI线程的CPU允许范围为4—6；一个主要线程为7。不是把整个游戏挤在单一核心。
- 游戏使用流畅画质、120帧档位；抗锯齿已关闭，并在界面确认保存和立即生效。
- GPU按负载调频，读到的最大频率为900MHz。没有新增GPU超频或GPU核心绑定。

## 最后一轮实际帧率

训练场90秒采集：有效帧时间跨度 {measure['frame_span_seconds']:.2f} 秒，{measure['actual_frame_count']} 个实际呈现帧。

| 指标 | 结果 |
|---|---:|
| 平均帧率 | {measure['average_fps']:.2f} FPS |
| 10秒窗口范围 | {mini:.1f}—{maxi:.1f} FPS |
| 帧间隔中位数 | {measure['interval_p50_ms']:.2f} ms |
| 95%帧间隔 | {measure['interval_p95_ms']:.2f} ms |
| 99%帧间隔 | {measure['interval_p99_ms']:.2f} ms |
| 超过25ms的间隔 | {measure['interval_over25ms_count']} 次 |
| 采集错误 | {len(measure['errors'])} 次 |
| 最大采集间隔 | {measure['max_poll_gap_seconds']:.3f} 秒 |

这是游戏画面的实际呈现帧率，不是系统设置里写入的120。此轮持续跑动是否覆盖完整90秒没有独立确认，不能作为整局激烈实战稳帧结论。此前用户操作的三分钟试验在150秒后采集失败，仅保留分段打印结果，未纳入此统计。

当前已消除本次观察到的系统60Hz限制，并验证重启自动生效。复测仍有短时掉帧，没有实现任何场景都绝对120FPS。菜单、加载、视频或应用自身的帧率上限也不会因屏幕120Hz而自动提高。

## GitHub 方案与选择

1. [RefreshRateSwitcher](https://github.com/XGMRXXC/RefreshRateSwitcher)已有小米刷新率切换、按应用规则和KSU支持。源码包含应用及持续守护逻辑；本次固定全局120Hz需求不需要再添加这些常驻任务。参考其系统设置与显示控制路径，实际模式编号由本机原生模式表读取。
2. [HyperOS3 ADB 120Hz方法](https://github.com/Neostein65/Force-120Hz-on-All-Apps-HyperOS-3-ADB/blob/f5b5af5ecbeaca191b23241c789b91e771b8fd25/README.md)说明miui_refresh_rate对MIUI刷新率策略的作用。作者验证机型是Redmi17，不能直接当作Pad6 Pro兼容性证明；本次通过实际显示状态与完整重启验证补足。
3. 按[KernelSU官方模块机制](https://kernelsu.org/guide/module.html)将已经验证的本机设置在开机完成后执行，两次有界应用后退出。CPU调度复用已有Scene，避免第二套调度同时写入。

## 文件与恢复

- 小米平板6Pro-全局120Hz与后台限制.zip：已安装的同版本备份；仅适用liuqin，不需要再次刷入。
- 恢复全局刷新率与后台限制.ps1：平板连接本机且允许USB调试时运行，停用本模块、恢复此前144Hz设置与所选后台权限、然后重启。保留KSU、Scene及现有机型配置。

后续系统更新或其他刷新率工具重新写入设置时，需要重新检查实际模式。全局120Hz的持久设置不等于所有应用都能输出120FPS。
'''
Path('outputs/和平精英120帧优化结果.md').write_bytes(summary.encode())
print(json.dumps({'average_fps':measure['average_fps'],'bins10sec_min':mini,'bins10sec_max':maxi,'zip_matches_installed_verified_files':True,'saved_report':True},ensure_ascii=False))
