# OptAppLaunchDelay evaluation against actual Pad APK

Read-only. No device mutation; SystemUI pull unnecessary because the target class exists in the actual launcher APK.

## Verdict

Do not deploy the current HyperCeiler OptAppLaunchDelay hook on this launcher. The exact target signature is absent, and a blanket adapted hook would bypass deliberate transition-merge coordination without observed evidence of that wait causing this tablet's reported cold-start stall.

## Signature mismatch

HyperCeiler source `OptAppLaunchDelay.java` looks for executeFinishCallback(boolean, boolean, int, WindowContainerTransaction, ShellTransitionCallback, boolean, boolean) and sets args[5]=false.

Actual `WindowTransitionCallbackHelper.java`, decompiled from MiuiHome-current.apk, has only:

- line 173: executeFinishCallback(boolean, boolean)
- line 230: executeFinishCallback(boolean, WindowContainerTransaction, ShellTransitionCallback)
- line 234: executeFinishCallback(boolean, WindowContainerTransaction, ShellTransitionCallback, boolean, boolean)

There is no seven-argument overload. This hook would fail method lookup rather than optimize the current launcher.

## Current five-parameter semantics

At line 234, z is toHome. z2 (index 3) controls whether finishing the main transition may wait for the merged transition coordination. z3 (index 4) is passed to onlyFinishRecentsIfNeeded and then RecentsAnimationControllerCompat.finish; it is userLeaveHint, not an animation waiting flag.

At lines 315-327, a wait occurs only when z2 is true, the stored recents merge info is not app-opening, and a merge-finish callback exists. It finishes the merge callback, saves the main finish transaction, and schedules mFinishRunnable after 50ms. checkHandlerRunnable can reschedule this 50ms wait while mWaitMergeAnimTimes>0, initially 2. Otherwise it finishes merge and main callbacks directly.

Forcing index3=false could bypass this transition-end synchronization. This is logically related to merged HOME/recents transitions, but does not bypass process creation, Application.onCreate, resource reads, or first-frame app rendering. It cannot be claimed to improve general cold-start TTID from these code paths alone. Potential visual/task-lifecycle consequences need runtime trace and regression testing, so no adapted hook is recommended.

Runtime logs that would establish whether this path participates in a bad sequence: tag MiuiPadHome_TransitionCallback; messages `set is waitFinishMainAnim true, postDelayed`, `checkHandlerRunnable has mFinishRunnable in handler`, `mFinishRunnable run is waitFinishMainAnim`, `execute finishMainCallbackSync return, no need post delay`.

## Current HyperCeiler integration

Current OS3 HomePad.java and HomePhone.java do not import or init OptAppLaunchDelay. OS2 HomePadOld.java imports at line82 and initializes it at line266 using home_other_opt_app_launch_delay. This supports not assuming old-version menu functionality applies to the Android15 HyperOS3 Pad launcher.

Primary source URLs:

- https://github.com/ReChronoRain/HyperCeiler/blob/main/library/libhook/src/main/java/com/sevtinge/hyperceiler/libhook/rules/home/other/OptAppLaunchDelay.java
- https://github.com/ReChronoRain/HyperCeiler/blob/main/library/libhook/src/main/java/com/sevtinge/hyperceiler/libhook/app/Home/os3/HomePad.java
- https://github.com/ReChronoRain/HyperCeiler/blob/main/library/libhook/src/main/java/com/sevtinge/hyperceiler/libhook/app/Home/os2/HomePadOld.java

Local evidence: WindowTransitionCallbackHelper.java, OptAppLaunchDelay.java, HomePad.java, HomePadOld.java, HomePhone.java.
