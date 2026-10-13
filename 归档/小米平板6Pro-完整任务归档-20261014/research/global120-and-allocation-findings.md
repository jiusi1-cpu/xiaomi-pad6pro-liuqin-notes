# Global 120 Hz persistence and existing Scene CPU allocation

Read-only research on 2026-10-13. No device commands, UI, installation or mutation.

## Recommended reuse

Use the device's already tested native refresh settings and Android display preference; persist them once after boot through the existing KernelSU general service-script mechanism if reboot resets a required value. Do not add a refresh App/daemon merely to restore a fixed global target. A minimal script should wait for `sys.boot_completed=1`, apply only verified display settings, log/check command results, and exit. Create UTF-8/LF files with no BOM; parent observed Scene's numeric parser failed on CRLF `120\r`.

Android 15's `cmd display set-user-preferred-display-mode WIDTH HEIGHT FPS DISPLAY_ID` is an existing framework path. DisplayManagerService stores per-display resolution and refresh preference in PersistentDataStore and calls saveIfNeeded. Thus this preference is designed to persist; Xiaomi policy can still override its active result. Width/height must match the device's existing supported mode. Do not copy a phone's dimensions or assume a framework mode ID is SurfaceFlinger index+1.

Primary sources:
- Android 15 shell command: https://android.googlesource.com/platform/frameworks/base/+/refs/heads/android15-release/services/core/java/com/android/server/display/DisplayManagerShellCommand.java
- Android 15 persistence: https://android.googlesource.com/platform/frameworks/base/+/refs/heads/android15-release/services/core/java/com/android/server/display/DisplayManagerService.java (setUserPreferredDisplayModeInternal, storeModeInPersistentDataStoreLocked)
- KernelSU official general boot-script guide: https://kernelsu.org/guide/module.html (service.d scripts must be executable; late_start runs nonblocking). Existing KSU version behavior should still be verified after reboot.

Native Xiaomi key evidence from existing GitHub implementations includes `secure miui_refresh_rate`, not merely AOSP peak_refresh_rate. This evidence does not prove every listed setting is needed on liuqin. Parent should reuse the smallest tested device-specific set and verify actual HOME/app/display mode after full reboot; no reason to copy untested persist properties, stop thermal services or add indefinite polling.

## Concrete GitHub candidates reviewed

1. XGMRXXC/RefreshRateSwitcher, last commit 2026-09-24 13:31:31 UTC, SHA cc825dadc89662109c87b94bb23c8901c97e1abe. Native source uses cmd display plus secure miui_refresh_rate/secure user_refresh_rate/system plugin_refresh_rate, and SF1035 fallback. README names newer Xiaomi tablets/K Pad and Xiaomi17Pro; no reviewed explicit liuqin/HyperOS3Android15 test. Not recommended to install for fixed global120: adds App, notification/overlay permission/battery exemption, two duplicate 60-second watchdog loops in service.sh, and a shell display-enforcement daemon checking every second. No thermal-service or CPU/GPU tuning found in reviewed files. Its dynamic fallback may mis-map framework modeId-1 in daemon even though ModeUtil separately documents this mapping is not universal.
   - https://github.com/XGMRXXC/RefreshRateSwitcher
   - https://github.com/XGMRXXC/RefreshRateSwitcher/blob/cc825dadc89662109c87b94bb23c8901c97e1abe/ksu-module/service.sh
   - https://github.com/XGMRXXC/RefreshRateSwitcher/blob/cc825dadc89662109c87b94bb23c8901c97e1abe/app/src/main/java/com/dsh/refreshswitch/ModeUtil.java
   - https://github.com/XGMRXXC/RefreshRateSwitcher/blob/cc825dadc89662109c87b94bb23c8901c97e1abe/app/src/main/java/com/dsh/refreshswitch/Daemon.java

2. Neostein65/Force-120Hz-on-All-Apps-HyperOS-3-ADB, last commit 2026-09-25 14:35:35 UTC, SHA f5b5af5ecbeaca191b23241c789b91e771b8fd25. Only README, two commits; test claim limited to Redmi17 5G, HyperOS3. Its tested secure miui_refresh_rate=120 changes MIUI vote and survives reboot, whereas preferred-display command alone was overridden. Useful implementation evidence, not mature universal module or liuqin compatibility proof.
   - https://github.com/Neostein65/Force-120Hz-on-All-Apps-HyperOS-3-ADB/blob/f5b5af5ecbeaca191b23241c789b91e771b8fd25/README.md

3. thelordalex/120-Display-Ultra, last commit 2024-08-21 02:55:14 UTC, SHA c973ae8188edd74f0d8e6f9ad4f9f7d789d51aa9. Repository module consists of system.prop+module.prop. No native settings/display command or current HyperOS3 verification reviewed. It modifies display density (280 and420), EGL swapinterval0, pointer/fling/scroll properties and assorted speculative FPS/GPU properties. Those changes expand scope without showing actual liuqin120 control. Reject for this task; no thermal stopping found in this specific module, but unrelated global properties are reason enough.
   - https://github.com/thelordalex/120-Display-Ultra/blob/c973ae8188edd74f0d8e6f9ad4f9f7d789d51aa9/system.prop

GitHub dates/SHAs verified via official API; fetched source and metadata are saved under `refresh-github/`.

## Scene already contains CPU allocation

Scene 9.4.11 APK raw resource `res/raw/perf_core_allocation` (saved as `refresh-github/scene-perf_core_allocation.json`) defines store `features/cpuset.conf`, launched by dw1.java via ActivityPerfOptions.

Exact fields/defaults:
- in_apps=1, in_games=1: app/game core allocation.
- use_presets=1: raw description says Scene supplies thread-affinity presets for a few popular games; without a preset its framework distributes according to load.
- gold_first=0: lock main thread to highest performance core; description says reboot required. Keep off absent measured reason.
- ebpf_enhanced=0: monitor thread creation through eBPF, description Linux>4.19 and potentially higher overhead. Hardware kernel5.10 satisfies stated version only, not proof of capability or benefit.
- high_priority=0, UI hidden: description explicitly warns higher heavy-thread priority may cause some games to freeze suddenly. Keep off.
- blacklist empty default.

Stored APK defaults prove supported options, not actual live enable flags. No reviewed package-specific affinity preset in assets or EP profile for com.tencent.tmgp.pubgmhd, UE4/GameThread/RenderThread; native daemon may hold its own presets, so do not invent exact PUBG thread mapping.

Extracted EP profile already sets common_gaming `@cpuset` values `0-3`, `0-3`, `0-5`, `0-7` and SurfaceFlinger cpuset `0-5`; it uses WALT latency/target loads, CPU freq ranges and DDR/L3 settings. GPU max path is merely alias-defined in profile; no reviewed call in profile/_Games/powercfg assigns it. Process group allocation and thread affinity are CPU controls, not a GPU core allocation mechanism. No evidence justifies forcing all game threads onto cpu7 or locking GPU at maximum before a bottleneck/thermal measurement.

Official Scene config docs: https://download.omarea.com/scene9/docs/apps.md (local apps.md says child cpuset settings replace parent); HP/EP comparison https://download.omarea.com/scene9/compare/hp_lp_ep.md. These docs plus extracted current profile/raw resource support reuse of Scene rather than a second CPU scheduler module. Keep background restrictions scoped to chosen apps; service force-stop is not equivalent to permanently preventing restart.
