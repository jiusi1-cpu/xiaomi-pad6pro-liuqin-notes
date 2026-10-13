from pathlib import Path
from importlib.machinery import SourceFileLoader
import subprocess,zipfile,json
a=SourceFileLoader('dev','work/adb-device.py').load_module()
base=Path('work/game-fps-research/prepared/persistent120');mod=base/'module'
header='''failures=0
run() {
 "$@"
 rc=$?
 if [ "$rc" -ne 0 ]; then
  echo "FAILED ($rc): $*" >&2
  failures=$((failures + 1))
 fi
 return "$rc"
}
'''
for name in ['apply.sh','restore.sh']:
 p=mod/name;s=p.read_text()
 lines=s.splitlines();result=[]
 for line in lines:
  trimmed=line.lstrip();indent=line[:len(line)-len(trimmed)]
  if trimmed.startswith('/system/bin/') and not trimmed.startswith('/system/bin/date'):
   line=indent+'run '+trimmed
   if name=='apply.sh' and trimmed.startswith(('/system/bin/settings','/system/bin/cmd display','/system/bin/service call')):
    if '|| exit' not in line:line+=' || exit 2'
  if name=='apply.sh' and trimmed.startswith('echo "Applied and exited;'):
   line='[ "$failures" -eq 0 ] || { echo "Some background operations failed"; exit 4; }\n'+line
  result.append(line)
 s='\n'.join(result)+'\n'
 s=s.replace('#!/system/bin/sh\n','#!/system/bin/sh\n'+header,1)
 if name=='restore.sh':s+='[ "$failures" -eq 0 ] || exit 4\nexit 0\n'
 p.write_bytes(s.encode())
# Clone tool shares a privileged UID with the system backup service. Exclude it.
p=mod/'background-packages.txt';p.write_bytes(('\n'.join(x for x in p.read_text().splitlines() if x!='com.miui.huanji')+'\n').encode())
p=mod/'module.prop';p.write_bytes(p.read_text().replace('version=1.1','version=1.2').replace('versionCode=2','versionCode=3').encode())
p=Path('outputs/恢复全局刷新率与后台限制.ps1');s=p.read_text(encoding='utf-8-sig');s=s.replace('& $adbPath -s $tabletSerial reboot\n','& $adbPath -s $tabletSerial reboot\nif ($LASTEXITCODE -ne 0) { throw \'设置已恢复，但重启失败；请手动重启平板。\' }\n');p.write_bytes(s.encode('utf-8-sig'))
original=json.loads((base/'background-original.json').read_text())
print('Excluded package backup:',json.dumps(original['com.miui.huanji']))
for op,mode in original['com.miui.huanji'].items():
 if op in ['RUN_IN_BACKGROUND','RUN_ANY_IN_BACKGROUND','10008']:
  a.root('cmd appops set com.miui.huanji '+op+' '+mode)
uidmode=json.loads((base/'uid-original.json').read_text())['com.miui.huanji']
a.root('cmd appops set --uid com.miui.huanji RUN_ANY_IN_BACKGROUND '+uidmode)
for p in mod.iterdir():
 data=p.read_bytes();assert b'\r' not in data and not data.startswith(b'\xef\xbb\xbf')
 remote='/data/local/tmp/liuqin120-final-'+p.name
 subprocess.run(a.adb+['push',str(p),remote],capture_output=True,check=True)
 if p.suffix=='.sh':a.root('sh -n '+remote)
 a.root('cat '+remote+' > /data/adb/modules/liuqin120/'+p.name)
a.root('chmod 0755 /data/adb/modules/liuqin120/*.sh')
with zipfile.ZipFile('outputs/小米平板6Pro-全局120Hz与后台限制.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in mod.iterdir():z.write(p,p.name)
print('Version1.2 installed;23 background packages; shell syntax and LF verified')
