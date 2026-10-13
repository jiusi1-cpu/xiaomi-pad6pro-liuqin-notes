[ "$(getprop ro.product.device)" = "liuqin" ] || abort "Only Xiaomi Pad 6 Pro liuqin is supported"
set_perm_recursive "$MODPATH" 0 0 0755 0644
set_perm "$MODPATH/boot-completed.sh" 0 0 0755
set_perm "$MODPATH/apply.sh" 0 0 0755
set_perm "$MODPATH/restore.sh" 0 0 0755
set_perm "$MODPATH/uninstall.sh" 0 0 0755
