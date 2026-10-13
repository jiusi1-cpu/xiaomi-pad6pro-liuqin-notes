#!/system/bin/sh
MODDIR=${0%/*}
sleep 10
[ -f "$MODDIR/disable" ] && exit 0
/system/bin/sh "$MODDIR/apply.sh"
# A second bounded apply follows OEM startup; then the script exits.
sleep 15
[ -f "$MODDIR/disable" ] && exit 0
/system/bin/sh "$MODDIR/apply.sh" display-only
