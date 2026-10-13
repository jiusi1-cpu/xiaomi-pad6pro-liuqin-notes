import subprocess,time,re,json
from pathlib import Path
adb=['adb','-s','1916b8f1'];out=Path('work/launcher-tests/final-warm-gestures');out.mkdir(parents=True,exist_ok=True)
def sh(c):return subprocess.check_output(adb+['shell',c],text=True,encoding='utf-8',errors='replace')
sh('input keyevent 224; wm dismiss-keyguard; input keyevent 3');time.sleep(.7);sh('input keyevent 3');time.sleep(.7);sh('input swipe 2350 900 350 900 180');time.sleep(.6)
sh('dumpsys gfxinfo com.miui.home reset');valid=[]
for pkg,x in [('bin.mt.plus',1617),('com.omarea.vtools',1975)]:
    sh(f'input tap {x} 950');time.sleep(1)
    focus=sh('dumpsys window')
    if pkg not in '\n'.join(s for s in focus.splitlines() if 'mCurrentFocus=' in s):raise RuntimeError('Unexpected foreground '+pkg)
    sh('input swipe 1440 1790 1440 1050 120');time.sleep(.7)
    for i in range(4):
        sh(f'input tap {x} 950; sleep 0.10; input swipe 1440 1790 1440 1050 120; sleep 0.06; input tap {x} 950; sleep 0.10; input swipe 1440 1790 1440 1050 120');time.sleep(.3)
    valid.append(pkg);print('bottom-HOME repeated switches passed',pkg,flush=True)
sh('input keyevent 3');time.sleep(.6)
gfx=sh('dumpsys gfxinfo com.miui.home framestats');out.joinpath('gfxinfo.txt').write_text(gfx,encoding='utf-8');out.joinpath('accessibility.txt').write_text(sh('dumpsys accessibility'),encoding='utf-8');out.joinpath('focus.txt').write_text(sh('dumpsys window'),encoding='utf-8');out.joinpath('end.png').write_bytes(subprocess.check_output(adb+['exec-out','screencap','-p']))
print('\n'.join(s for s in gfx.splitlines()[:30] if any(k in s for k in ['Total frames','Janky frames','percentile'])))
