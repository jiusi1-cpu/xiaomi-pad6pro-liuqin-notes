# Actual Xiaomi Pad launcher animation findings

Read-only inspection of `work/MiuiHome-current.apk`, launcher RELEASE-4.50.0.1056-1118-12161038. Decompiled using official JADX 1.5.6; no device mutation by this research agent.

## Actionable existing setting

`TransitionAnimDurationHelper.java:51` reads `Settings.Global transition_animation_duration_ratio`, default 1.0. Its ContentObserver watches this key and updates live. Value is clamped 0..1 and multiplied by the device transition ratio. `RectFSpringAnim.java:910` multiplies its spring response by that result. A backed-up, reversible comparison at 0.85 or 0.90 is possible without Xposed. This changes animation timing, not the interruption state machine. Verify actual visual gestures and logs before asserting improvement.

## Old interruption hook is unsuitable

`NavStubView.java:1141` onInputConsumerEvent only checks input ignore/quick-switch/fixed-rotation conditions, copies MotionEvent, and queues it to MAIN_THREAD_EXECUTOR. The lambda forwards it to mEventReceiver.test. It does not synchronously access mAppToHomeAnim2. Thus old HyperCeiler FixAnimation's temporary field-null before/synchronous restore-after cannot address this asynchronous path.

`ItemIcon.java:619` initPerformClickRunnable reads Android View.mPerformClick reflectively; post() executes this exact Runnable synchronously. Old FixAnimation replacing initialization with an empty implementation causes the field to remain null and removes the immediate-execution shortcut, adding queuing rather than establishing animation continuity. This is an implementation inference, not an observed runtime bug.

## Native interruption already exists

`NavStubView.java:2172` needBreakOpenAnim requires a live app-transition manager, IconAndTaskBreakableAnimManager.isAnimChainOn(), and NOT DeviceLevelUtils.isUseSimpleAnim(). breakOpenAnimIfNeeded invokes QuickstepAppTransitionManagerImpl.breakOpenAnim().

`QuickstepAppTransitionManagerImpl.java:185` removes finish callbacks from launch-animation end detectors and sets mRectFSpringAnim.setMoveToTargetRectWhenAnimEnd(false), preserving the interrupted state instead of snapping to the target.

`BreakableAnimManager.java:31` setupAnimAndBreakLast captures the current animation parameters, initializes the next animation from them, and cancels the previous animation. IconAndTaskBreakableAnimManager captures the current RectF, radius, and alpha; its listener sets moveToTargetRectWhenAnimEnd(false).

`DeviceLevelUtils.java:127` isUseSimpleAnim depends on CPU/GPU Folme classification plus device lists. Its dump method prints sCpuLevel, sGpuLevel, sDeviceLevelFromFolme. Confirm runtime classification before proposing a force-full-animation hook. No settings key controls this condition in this class.

`Utilities.java:2298` isUseSmoothAnimationEffect is a device-list check (cmi, umi, phoenix, picasso); liuqin is absent. In inspected RectFSpringAnim it only toggles a 0.9 response multiplier. Forcing this flag is not evidence of a newer OPPO/vivo-style engine.

## Recommendation

Prefer the existing specific duration setting for the first conservative visual A/B comparison, preserving the full native animation and interruption handling. Do not deploy old FixAnimation or blanket cancellation/input hooks. A genuine logic fix would require reproducing and tracing the exact bad transition under bottom-swipe HOME; the static code already supports chained interruption.

## Evidence files

NavStubView.java, ItemIcon.java, HomeBreakableAnimManager.java, IconAndTaskBreakableAnimManager.java, BreakableAnimManager.java, QuickstepAppTransitionManagerImpl.java, RectFSpringAnim.java, DeviceLevelUtils.java, Utilities.java, TransitionAnimDurationHelper.java in this directory.
