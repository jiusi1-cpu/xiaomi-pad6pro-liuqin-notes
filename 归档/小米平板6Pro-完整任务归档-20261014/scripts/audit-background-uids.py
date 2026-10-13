from pathlib import Path
from importlib.machinery import SourceFileLoader
import re,json
a=SourceFileLoader('dev','work/adb-device.py').load_module()
pkgs=Path('work/game-fps-research/prepared/persistent120/module/background-packages.txt').read_text().splitlines()
rows=[]
for line in a.sh('pm list packages -U').splitlines():
 m=re.match(r'package:(\S+) uid:(\d+)',line)
 if m: rows.append((m[1],int(m[2])))
result=[]
for p in pkgs:
 ids=[u for name,u in rows if name==p]
 if not ids:result.append({'package':p,'missing':True});continue
 u=ids[0];result.append({'package':p,'uid':u,'shared_packages':[name for name,other in rows if other==u and name!=p],'system_uid':u<10000})
Path('work/game-fps-research/prepared/background-uid-audit.json').write_bytes(json.dumps(result,indent=2).encode())
print(json.dumps({'packages_checked':len(result),'shared_or_system':[r for r in result if r.get('shared_packages') or r.get('system_uid') or r.get('missing')]},ensure_ascii=False))
