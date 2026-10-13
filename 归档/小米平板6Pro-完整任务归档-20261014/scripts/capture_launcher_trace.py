import subprocess,time,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('label');a=p.parse_args();out=Path('work/launcher-tests')/a.label;out.mkdir(parents=True,exist_ok=True)
adb=['adb','-s','1916b8f1']
def sh(c):return subprocess.check_output(adb+['shell',c],text=True,encoding='utf-8',errors='replace')
config='''buffers { size_kb: 131072 fill_policy: RING_BUFFER }
duration_ms: 30000
data_sources { config { name: "linux.ftrace" ftrace_config {
ftrace_events: "sched/sched_switch"
ftrace_events: "sched/sched_waking"
ftrace_events: "power/cpu_frequency"
ftrace_events: "power/cpu_idle"
atrace_categories: "am"
atrace_categories: "wm"
atrace_categories: "gfx"
atrace_categories: "view"
atrace_categories: "input"
atrace_categories: "dalvik"
atrace_apps: "com.miui.home"
atrace_apps: "com.android.settings"
atrace_apps: "com.android.systemui"
} } }
data_sources { config { name: "android.surfaceflinger.frametimeline" } }
data_sources { config { name: "linux.process_stats" process_stats_config { scan_all_processes_on_start: true } } }
'''
out.joinpath('config.txt').write_text(config,encoding='utf-8')
subprocess.run(adb+['push',str(out/'config.txt'),'/data/local/tmp/launcher-trace-config.txt'],check=True,stdout=subprocess.DEVNULL)
sh('input keyevent 224; wm dismiss-keyguard; input keyevent 3');time.sleep(.6);sh('input keyevent 3');time.sleep(.8)
proc=subprocess.Popen(adb+['shell','perfetto','--txt','-c','-','-o','/data/misc/perfetto-traces/launcher-cold.pftrace'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
proc.stdin.write(config.encode());proc.stdin.close();proc.stdin=None
time.sleep(1)
for i in range(4):
    sh('am force-stop com.android.settings');time.sleep(.4)
    sh('input tap 1975 950');time.sleep(1.5)
    focus=sh('dumpsys window');is_settings='com.android.settings' in '\n'.join(x for x in focus.splitlines() if 'mCurrentFocus=' in x)
    if not is_settings:raise RuntimeError('Wrong foreground during icon test')
    sh('input swipe 1440 1790 1440 1050 120; sleep 0.10; input tap 1975 950; sleep 0.10; input swipe 1440 1790 1440 1050 120');time.sleep(.6)
    print('cold+interrupt cycle',i,flush=True)
stdout,_=proc.communicate(timeout=35);out.joinpath('capture.txt').write_bytes(stdout)
if proc.returncode:raise RuntimeError(stdout.decode(errors='replace'))
subprocess.run(adb+['pull','/data/misc/perfetto-traces/launcher-cold.pftrace',str(out/'trace.pftrace')],check=True)
print('TRACE_READY',out/'trace.pftrace',flush=True)

