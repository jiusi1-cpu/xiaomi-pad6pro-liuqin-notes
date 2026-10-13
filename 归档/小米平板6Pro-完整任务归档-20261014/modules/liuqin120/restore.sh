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
run /system/bin/settings put secure miui_refresh_rate 144
run /system/bin/settings put secure user_refresh_rate 144
run /system/bin/settings put system peak_refresh_rate 144
run /system/bin/settings delete system min_refresh_rate
run /system/bin/settings put system is_smart_fps 0
run /system/bin/cmd display clear-user-preferred-display-mode 0
run /system/bin/service call SurfaceFlinger 1035 i32 -1 >/dev/null 2>&1
run /system/bin/service call SurfaceFlinger 1036 i32 0 >/dev/null 2>&1
run /system/bin/cmd appops set com.android.fileexplorer RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.android.fileexplorer RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.android.fileexplorer 10008 ignore
run /system/bin/cmd appops set com.android.htmlviewer RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.android.htmlviewer RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.android.htmlviewer 10008 default
run /system/bin/cmd appops set com.miui.notes RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.notes RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.notes 10008 ignore
run /system/bin/cmd appops set com.miui.gallery RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.gallery RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.gallery 10008 ignore
run /system/bin/cmd appops set com.miui.mediaeditor RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.mediaeditor RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.mediaeditor 10008 ignore
run /system/bin/cmd appops set com.miui.creation RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.creation RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.creation 10008 ignore
run /system/bin/cmd appops set com.xiaomi.gamecenter RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.xiaomi.gamecenter RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.xiaomi.gamecenter 10008 ignore
run /system/bin/cmd appops set com.xiaomi.market RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.xiaomi.market RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.xiaomi.market 10008 allow
run /system/bin/cmd appops set com.miui.weather2 RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.weather2 RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.weather2 10008 ignore
run /system/bin/cmd appops set com.miui.player RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.player RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.player 10008 ignore
run /system/bin/cmd appops set com.miui.video RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.video RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.video 10008 ignore
run /system/bin/cmd appops set com.qiyi.video.pad RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.qiyi.video.pad RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.qiyi.video.pad 10008 ignore
run /system/bin/cmd appops set com.smile.gifmaker RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.smile.gifmaker RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.smile.gifmaker 10008 ignore
run /system/bin/cmd appops set com.ss.android.ugc.aweme RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.ss.android.ugc.aweme RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.ss.android.ugc.aweme 10008 ignore
run /system/bin/cmd appops set com.xiaomi.shop RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.xiaomi.shop RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.xiaomi.shop 10008 ignore
run /system/bin/cmd appops set com.xiaomi.smarthome RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.xiaomi.smarthome RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.xiaomi.smarthome 10008 ignore
run /system/bin/cmd appops set cn.wps.moffice_eng RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set cn.wps.moffice_eng RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set cn.wps.moffice_eng 10008 ignore
run /system/bin/cmd appops set cn.wps.moffice_eng.xiaomi.lite RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set cn.wps.moffice_eng.xiaomi.lite RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set cn.wps.moffice_eng.xiaomi.lite 10008 ignore
run /system/bin/cmd appops set com.duokan.reader RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.duokan.reader RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.duokan.reader 10008 ignore
run /system/bin/cmd appops set com.miui.cleanmaster RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.cleanmaster RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.cleanmaster 10008 ignore
run /system/bin/cmd appops set com.miui.calculator RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.calculator RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.calculator 10008 ignore
run /system/bin/cmd appops set com.xiaomi.scanner RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.xiaomi.scanner RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.xiaomi.scanner 10008 ignore
run /system/bin/cmd appops set com.miui.huanji RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.huanji RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.miui.huanji 10008 ignore
run /system/bin/cmd appops set com.android.email RUN_IN_BACKGROUND allow
run /system/bin/cmd appops set com.android.email RUN_ANY_IN_BACKGROUND allow
run /system/bin/cmd appops set com.android.email 10008 ignore
run /system/bin/cmd appops set --uid com.android.fileexplorer RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.android.htmlviewer RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.miui.notes RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.miui.gallery RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.miui.mediaeditor RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.miui.creation RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.xiaomi.gamecenter RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.xiaomi.market RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.miui.weather2 RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.miui.player RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.miui.video RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.qiyi.video.pad RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.smile.gifmaker RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.ss.android.ugc.aweme RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.xiaomi.shop RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.xiaomi.smarthome RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid cn.wps.moffice_eng RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid cn.wps.moffice_eng.xiaomi.lite RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.duokan.reader RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.miui.cleanmaster RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.miui.calculator RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.xiaomi.scanner RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.miui.huanji RUN_ANY_IN_BACKGROUND default
run /system/bin/cmd appops set --uid com.android.email RUN_ANY_IN_BACKGROUND default
[ "$failures" -eq 0 ] || exit 4
exit 0
