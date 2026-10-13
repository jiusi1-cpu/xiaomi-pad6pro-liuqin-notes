#!/system/bin/sh
failures=0
run() {
 "$@"
 rc=$?
 if [ "$rc" -ne 0 ]; then
  echo "FAILED ($rc): $*" >&2
  failures=$((failures + 1))
 fi
 return "$rc"
}
MODDIR=${0%/*}
[ "$(/system/bin/getprop ro.product.device)" = "liuqin" ] || exit 1
[ -f "$MODDIR/disable" ] && exit 0
LOG="/data/local/tmp/liuqin120.log"
: > "$LOG"
exec >> "$LOG" 2>&1
/system/bin/date
for key in miui_refresh_rate user_refresh_rate; do
 run /system/bin/settings put secure "$key" 120 || exit 2
done
run /system/bin/settings put system peak_refresh_rate 120.0 || exit 2
run /system/bin/settings put system min_refresh_rate 120.0 || exit 2
run /system/bin/settings put system is_smart_fps 0 || exit 2
run /system/bin/cmd display set-user-preferred-display-mode 1800 2880 120 0 || exit 2
# Read native SurfaceFlinger mode identifiers instead of assuming framework IDs.
mode=$(/system/bin/dumpsys SurfaceFlinger | /system/bin/awk '
 /displayModes=/{inside=1;next}
 inside && /displayManagerPolicy=/{inside=0}
 inside && !found && /vsyncRate=120\.00 Hz/{line=$0;sub(/^.*\{id=/,"",line);sub(/,.*/,"",line);print line;found=1}')
case "$mode" in ''|*[!0-9]*) echo "No native120Hz mode found";exit 3;; esac
echo "Native120Hz mode=$mode"
run /system/bin/service call SurfaceFlinger 1035 i32 "$mode" || exit 2
if [ "${1:-}" != "display-only" ]; then
 while IFS= read -r pkg; do
  [ -n "$pkg" ] || continue
  run /system/bin/cmd appops set "$pkg" RUN_IN_BACKGROUND ignore
  run /system/bin/cmd appops set --uid "$pkg" RUN_ANY_IN_BACKGROUND ignore
  run /system/bin/cmd appops set "$pkg" 10008 ignore
  run /system/bin/am force-stop "$pkg"
 done < "$MODDIR/background-packages.txt"
 # Preserve the existing authorized game scheduler across boot.
 run /system/bin/cmd appops set com.omarea.vtools 10008 allow
 run /system/bin/cmd appops set com.omarea.vtools RUN_IN_BACKGROUND allow
 run /system/bin/cmd appops set com.omarea.vtools RUN_ANY_IN_BACKGROUND allow
fi
[ "$failures" -eq 0 ] || { echo "Some background operations failed"; exit 4; }
echo "Applied and exited; no polling daemon"
