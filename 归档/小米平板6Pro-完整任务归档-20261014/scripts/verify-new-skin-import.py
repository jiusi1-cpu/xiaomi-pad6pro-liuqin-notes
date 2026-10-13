from pathlib import Path
from importlib.machinery import SourceFileLoader
import json,shlex
a=SourceFileLoader('dev','work/adb-device.py').load_module()
base=Path('work/new-skin-pak');p=base/'import-record.json';record=json.loads(p.read_text())
rows=[]
for item in record['files']:
 raw=a.root('if [ -f '+shlex.quote(item['target'])+' ]; then sha256sum '+shlex.quote(item['target'])+'; else echo ABSENT; fi').strip()
 rows.append({'name':Path(item['local_payload']).name,'present':raw!='ABSENT','hash_matches':raw.split()[0]==item['payload_sha256'] if raw!='ABSENT' else False})
pid=a.sh('pidof com.tencent.tmgp.pubgmhd',check=False).strip().split()
opened=[]
if pid:
 raw=a.root('ls -l /proc/'+pid[0]+'/fd',check=False)
 opened=[line for line in raw.splitlines() if '16019' in line and ('.pak' in line or '.sig' in line)]
result={'files_after_launch':rows,'game_running':bool(pid),'open_resource_files':opened}
(base/'postlaunch-verification.json').write_bytes(json.dumps(result,ensure_ascii=False,indent=2).encode())
record['latest_postlaunch_check']=result;p.write_bytes(json.dumps(record,ensure_ascii=False,indent=2).encode())
print(json.dumps(result,ensure_ascii=False,indent=2))
