# OPPO/vivo reference and Xiaomi cold-start implications

Read-only primary-source research, 2026-10-13. No device mutation.

## Primary claims and limits

- vivo current official page is OriginOS 7, with first rollout listed October 9, 2026. It explicitly describes first-frame-interruptible interaction, continuous response to the new gesture, unified motion rhythm, and changes spanning scheduling, memory, compilation, and multi-window rendering. The advertised percentage improvements are vendor-lab comparisons, not predictions for this Xiaomi tablet. https://www.vivo.com.cn/originos
- ColorOS 15 official introduction describes multiple animations/windows drawn in parallel before the previous animation finishes; this is a system drawing/rendering architecture change. https://www.coloros.com/article/A00000066/
- ColorOS 16 official page describes evolution from parallel to unified seamless architecture, independent rendering across system modules, and a dedicated dynamic frame-sync/performance pipeline. These pages do not publish a drop-in Xiaomi engine or source implementation. https://www.oppo.com/in/coloros16/

Replicable goals: respond to new input promptly, maintain visual position/shape/opacity during interruption, preserve a coherent motion rhythm, ensure the app's first frame arrives without starving launcher/SystemUI rendering. These are engineering interpretations of the above, not direct documentation of their algorithms.

Not established: that a launcher APK transplant, a duration multiplier, a kernel module, or global CPU minimum frequency can reproduce the OPPO/vivo architecture.

## Cold starts require a second metric

Android distinguishes cold process creation, warm activity recreation, and hot foreground resumption. Cold start has process, Application, Activity, UI initialization and first drawing; TTID and TTFD are different. Perfetto Android App Startups is the recommended way to attribute the work. https://developer.android.com/topic/performance/issues/launch-time

Thus stable transition frames and time-to-first-app-frame should both be measured. Shortening animation duration alone can expose a waiting starting window sooner, and cannot remove an app's initialization/network work. This last point is an inference from the startup sequence.

## Concrete supported optimization

Inspect actual ART status and profiles for the launcher and representative lagging apps. Verify means bytecode verification without AOT; speed compiles all methods; speed-profile selectively compiles the important code. Compile only selected apps, and verify status plus cold-start traces afterward. Avoid indiscriminate all-app speed compilation. Android documents both modes reduce interpreter/JIT interference, while only speed-profile reduces runtime class-loading impact. https://developer.android.com/topic/performance/memory/guide/app-code ; https://developer.android.com/topic/performance/measuring-performance ; https://developer.android.com/topic/performance/baselineprofiles/debug-baseline-profiles

For this actual Xiaomi APK, the existing transition_animation_duration_ratio remains the only directly inspected, observer-backed motion parameter suitable for a small reversible A/B comparison. Static code already has native breakable animation managers. No newly validated native toggle or safe custom interruption hook was found in this follow-up. See actual-apk-findings.md.

## Suggested acceptance cases

1. Cold launch from actual desktop icon (app process absent): capture launcher/SystemUI frame timeline and app TTID.
2. Hot launch/Home cycles with bottom swipe: record missed inputs, hard jumps, and long animation stalls.
3. Recents entry, horizontal scroll, reopening another app: preserve task selection and gestures.
4. Test stock animation ratio and tuned ratio with the same display/thermal state; separately compare before/after ART compilation. Do not call warmer page cache an animation-engine improvement.
