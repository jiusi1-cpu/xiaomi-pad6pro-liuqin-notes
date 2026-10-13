import subprocess,time,json,re,argparse
from pathlib import Path

parser=argparse.ArgumentParser();parser.add_argument('label');parser.add_argument('--cycles',type=int,default=10)
parser.add_argument('--x',type=int,default=1975);parser.add_argument('--y',type=int,default=950)
parser.add_argument('--no-record',action='store_true')
args=parser.parse_args();out=Path('work/launcher-tests')/args.label;out.mkdir(parents=True,exist_ok=True)
adb=['adb','-s','1916b8f1']
def shell(command):return subprocess.check_output(adb+['shell',command],text=True,stderr=subprocess.STDOUT)
shell('input keyevent KEYCODE_HOME');time.sleep(.7)
shell('input keyevent KEYCODE_HOME');time.sleep(1.5)
for attempt in range(3):
    shell(f'input tap {args.x} {args.y}');time.sleep(1)
    warm=shell('dumpsys activity activities')
    if 'com.android.settings/' in '\n'.join(x for x in warm.splitlines() if 'topResumedActivity' in x):break
else:raise RuntimeError('Settings icon did not launch Settings; aborting invalid benchmark')
print('\n'.join(x for x in warm.splitlines() if 'topResumedActivity' in x),flush=True)
shell('input swipe 1440 1790 1440 1050 120');time.sleep(.8)
shell('dumpsys gfxinfo com.miui.home reset')
record=None if args.no_record else subprocess.Popen(adb+['shell','screenrecord','--size','1280x800','--bit-rate','4000000','--time-limit','35','/sdcard/launcher-test.mp4'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
start=time.time()
events=[]
for i in range(args.cycles):
    t=time.time()-start
    result=shell(f'input tap {args.x} {args.y}; sleep 0.10; input swipe 1440 1790 1440 1050 120; sleep 0.04')
    events.append({'cycle':i,'start_sec':t,'end_sec':time.time()-start,'output':result})
time.sleep(.5)
out.joinpath('gfxinfo.txt').write_text(shell('dumpsys gfxinfo com.miui.home framestats'),encoding='utf-8')
out.joinpath('events.json').write_text(json.dumps(events,indent=2),encoding='utf-8')
out.joinpath('display.txt').write_text(shell('dumpsys display'),encoding='utf-8')
out.joinpath('logcat.txt').write_text(shell('logcat -d -t 2500'),encoding='utf-8')
out.joinpath('end.png').write_bytes(subprocess.check_output(adb+['exec-out','screencap','-p']))
print('gesture cycles finished',round(time.time()-start,2),'sec',flush=True)
# Finish the screen recording cleanly. Only signal the screenrecord command owned by this test.
if record:
    pid=shell('pidof screenrecord').strip()
    if pid and pid.isdecimal():shell('kill -2 '+pid)
    try:record.communicate(timeout=5)
    except subprocess.TimeoutExpired:record.terminate();record.communicate(timeout=3)
    subprocess.run(adb+['pull','/sdcard/launcher-test.mp4',str(out/'screen.mp4')],check=True)
text=out.joinpath('gfxinfo.txt').read_text(encoding='utf-8')
print('\n'.join(x for x in text.splitlines()[:30] if any(k in x for k in ['Total frames','Janky frames','percentile','Missed Vsync','Slow UI thread','Frame deadline missed'])))
