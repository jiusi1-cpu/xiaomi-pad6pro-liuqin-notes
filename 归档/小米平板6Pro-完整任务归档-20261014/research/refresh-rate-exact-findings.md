# Scene 9.4.11 per-app refresh rate: verified APK evidence

Read-only investigation of `work/scene_9.4.11.apk`; relevant JADX classes under `work/scene-performance-research/jadx/sources/`. No device mutation. APK decompilation emitted errors in other classes; the classes cited below were decompiled.

## Files and schema

App files directory: `/data/user/0/com.omarea.vtools/files/` (`u60.d/e`).

`REFRESH_RATE.CONF`: newline-delimited `PACKAGE MIN_HZ MAX_HZ`, parsed as exactly three space-separated columns by `e11.i`; min/max represented by `a11.b/a`. Saved by `e11.l`. Existing `com.tencent.tmgp.pubgmhd 60 90` is a saved range, not the feature enable flag.

For game 120 Hz and launcher 144 Hz:

```text
com.tencent.tmgp.pubgmhd 120 120
com.miui.home 144 144
```

`features/refresh_rate.conf`: plain `key=value` lines handled by `nz0`. Boolean true is `1`. Global enable is `enable=1` (`e11.b`, `hw1.h`, `fw1.onClick`). Missing enable defaults false. The saved snapshot does not establish the current device flag.

To keep non-game behavior at panel peak instead of activating the old stock 60/90 Hz per-app overrides, back up the original file and replace its entries with the two explicit entries above. Do not leave it empty: `e11` constructor calls `o()` to populate `assets/refresh_rate.txt` when the loaded map has no entries.

Keep all unmentioned existing feature settings. Appropriate refresh policy values for the requested non-game 144 Hz behavior:

```text
enable=1
apps_default=peak
apps_inactive=peak
games_default=peak
gesture=peak
```

This is verified field/value schema, not measured daemon precedence. `peak` is the device maximum, shown as 144 Hz for this panel (`jy0.a`); `high` is specifically 120 Hz (`ky0.a`), not peak. `apps_default` defaults high (`yw0`), `apps_inactive` defaults low (`ax0`), `games_default` defaults high (`dx0`), `gesture` defaults high (`nx0`). Keeping `games_default=peak` avoids applying a new blanket 120 Hz policy to unrelated games; the specific pubgmhd entry provides its 120 Hz range.

Preserve current screen-off, low-battery, brightness, tap/scroll delay, strict, compatible, and display_modes fields. The APK's defaults include `low_battery_threshold=5`, `low_battery_mode=low`, `screen_off=high`; no need to remove these guards to configure this game's range.

## Supported apply/reload route

Scheduling -> optional features dialog is `hw1`; its refresh control switch ID is `refresh_rate_enable`, details ID `refresh_rate_text`. Details open `ActivityPerfOptions` with `ny0` field definitions and store `features/refresh_rate.conf` (`yv1`).

Closing the optional features dialog calls `bw1.onDismiss` -> `q50.w0` -> `q50.v0` -> daemon API **`scheduler-refresh`**, argument **`custom-cache`**, timeout 2000 ms (`q50.java:160-164,1723-1725`). Thus after prepared file edits, open/close that existing dialog to request the app's own refresh. Merely writing files is not evidence of live reload. UI confirm also stores the enable flag (`fw1`), and the same dismiss callback requests refresh.

No verified daemon CLI was found. Do not invent a `scene-daemon scheduler-refresh` command. App API transport can use abstract LocalSocket `Scene` (`n60`) or its established TCP SocketChannel; requests are framed/encrypted by `q50.Q0/H/R0/T0` and `r50`, so a plain shell string sent to a socket is not valid.

The floating game panel additionally calls API `set-refresh-rate` with the selected integer (`e11.n`, `q50.H0`) for immediate selection. That alone is not evidence of ongoing foreground/background policy enforcement.

Verify actual foreground game display mode and HOME mode after applying; display Hz configuration alone is not proof of actual game rendering 120 FPS.

## FAS

FAS is separate CPU scheduling support, not a requirement for this refresh control. `qt0.q` only exposes FAS for LP+online source unless the active configuration manifest explicitly has `features.fas=true`, and also requires daemon support. The extracted EP 20260620 manifest has only `strict` and `pedestal`; no `fas` key. Accordingly this extracted EP configuration does not advertise FAS support. Do not infer daemon state if its manifest has changed since extraction.

FAS app files are independent (`features/fas_whitelist.conf`, `fas_blacklist.conf`, `fas_fps_levels.conf`, offsets); a default FAS level list containing 120 does not unlock game FPS. Official comparison document says FAS can lose some frame rate and lower input responsiveness: https://download.omarea.com/scene9/compare/hp_lp_ep.md (previously fetched local `hp_lp_ep.md`, lines 36-37; direct web open on this pass failed). No current measured evidence requires enabling FAS for the 120 FPS target; keep it unchanged during the refresh-policy correction.
