from pathlib import Path
from importlib.machinery import SourceFileLoader
import json,re,subprocess,hashlib
a=SourceFileLoader('dev','work/adb-device.py').load_module()
mod=Path('work/game-fps-research/prepared/persistent120/module')
pkgs=(mod/'background-packages.txt').read_text().splitlines()
commands=[]
for p in pkgs:
 commands+=['echo PACKAGE:'+p,'cmd appops get '+p+' RUN_IN_BACKGROUND','cmd appops get --uid '+p+' RUN_ANY_IN_BACKGROUND','cmd appops get '+p+' 10008']
raw=a.root('; '.join(commands),timeout=90)
fail=[]
for block in raw.split('PACKAGE:')[1:]:
 p=block.splitlines()[0]
 for op,pattern in [('RUN_IN_BACKGROUND',r'RUN_IN_BACKGROUND: ignore'),('UID_RUN_ANY',r'Uid mode: RUN_ANY_IN_BACKGROUND: ignore'),('AUTOSTART',r'(?:AUTO_START|MIUIOP\(10008\)|10008): ignore')]:
  if not re.search(pattern,block):fail.append({'package':p,'operation':op,'raw':block})
sf=a.root('dumpsys SurfaceFlinger')
display=a.sh('dumpsys display')
essential=a.root('getprop sys.boot_completed; id; cat /data/adb/modules/liuqin120/module.prop; cat /data/local/tmp/liuqin120.log; cmd appops get --uid com.miui.huanji RUN_ANY_IN_BACKGROUND; dumpsys accessibility | head -55; pidof scene-daemon',timeout=45)
settings=a.root('settings get secure miui_refresh_rate; settings get secure user_refresh_rate; settings get system peak_refresh_rate; settings get system min_refresh_rate; settings get system is_smart_fps')
hashes={}
for p in mod.iterdir():
 remote=a.root('sha256sum /data/adb/modules/liuqin120/'+p.name).split()[0]
 local=hashlib.sha256(p.read_bytes()).hexdigest();hashes[p.name]=remote==local
result={'background_package_count':len(pkgs),'background_failures':fail,'all_module_hashes_match':all(hashes.values()),'module_hashes':hashes,'essential':essential,'settings':settings,'sf_active_lines':[s for s in sf.splitlines() if 'activeMode=' in s or 'refreshRate=' in s or 'mDebugDisplayMode' in s],'display_active_lines':[s for s in display.splitlines() if 'mActiveModeId=' in s],'appops_raw':raw}
Path('work/game-fps-research/prepared/final-reboot-verification.json').write_bytes(json.dumps(result,ensure_ascii=False,indent=2).encode())
print(json.dumps({k:v for k,v in result.items() if k not in ['appops_raw','module_hashes','essential']},ensure_ascii=False,indent=2))
print(essential.split('User state')[0])
