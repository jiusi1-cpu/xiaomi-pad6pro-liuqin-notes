from importlib.machinery import SourceFileLoader
from pathlib import Path
import json,re
a=SourceFileLoader('dev','work/adb-device.py').load_module()
pid=a.sh('pidof com.tencent.tmgp.pubgmhd').strip().split()[0]
raw=a.root('for t in /proc/'+pid+'/task/*; do n=$(cat "$t/comm"); case "$n" in MainThread-UE4|RHIThread|RenderThread*|Thread-22) echo "$t:$n"; cat "$t/status" | grep Cpus_allowed_list;; esac; done')
limits=a.root('for p in /sys/devices/system/cpu/cpufreq/policy*; do echo "$p"; cat "$p/scaling_min_freq" "$p/scaling_max_freq"; done; cat /sys/class/kgsl/kgsl-3d0/gpuclk /sys/class/kgsl/kgsl-3d0/max_gpuclk')
access=a.sh('dumpsys accessibility')
r={'pid':pid,'thread_masks':raw,'cpu_gpu_limits':limits,'scene_accessibility_bound':bool(re.search(r'Bound services:.*?SCENE.*?Crashed services',access,re.S)),'crashed_services':[s for s in access.splitlines() if 'Crashed services' in s]}
Path('work/game-fps-research/prepared/final-game-allocation.json').write_bytes(json.dumps(r,ensure_ascii=False,indent=2).encode());print(json.dumps(r,ensure_ascii=False,indent=2))
