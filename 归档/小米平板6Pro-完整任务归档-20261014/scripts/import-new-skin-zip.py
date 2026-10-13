from pathlib import Path,PurePosixPath
from importlib.machinery import SourceFileLoader
import subprocess,zipfile,json,hashlib,shlex
a=SourceFileLoader('dev','work/adb-device.py').load_module()
base=Path('work/new-skin-pak');meta=json.loads((base/'inspection.json').read_text())
local=base/'user-skin-pack.zip'
assert hashlib.sha256(local.read_bytes()).hexdigest()==meta['zip_sha256']
assert a.root('sha256sum '+shlex.quote(meta['source'])).split()[0]==meta['zip_sha256'],'Source archive changed'
recordpath=base/'import-record.json'
assert not recordpath.exists(),'Import record already exists; inspect it before resuming'
root='/sdcard/Android/data/com.tencent.tmgp.pubgmhd/'
prefix='files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/Paks/'
backup=base/'original-files';backup.mkdir(exist_ok=True)
extract=base/'extracted';extract.mkdir(exist_ok=True)
rows=[]
with zipfile.ZipFile(local) as z:
 for i in z.infolist():
  if i.is_dir() or not i.filename.startswith(prefix):continue
  p=PurePosixPath(i.filename)
  assert '..' not in p.parts and not p.is_absolute() and '\\' not in i.filename
  assert p.parent.as_posix()==prefix.rstrip('/')
  assert p.suffix in ['.pak','.sig'] or p.name=='@byrj6'
  target=root+i.filename;data=z.read(i)
  out=extract/p.name;out.write_bytes(data)
  exists=a.root('if [ -f '+shlex.quote(target)+' ]; then echo YES; else echo NO; fi').strip()=='YES'
  row={'archive_path':i.filename,'target':target,'local_payload':str(out),'payload_sha256':hashlib.sha256(data).hexdigest(),'existed_before':exists,'imported':False}
  if exists:
   original=backup/p.name
   subprocess.run(a.adb+['pull',target,str(original)],capture_output=True,check=True)
   row['original_backup']=str(original);row['original_sha256']=hashlib.sha256(original.read_bytes()).hexdigest()
   assert a.root('sha256sum '+shlex.quote(target)).split()[0]==row['original_sha256']
  rows.append(row)
assert len(rows)==5,'Unexpected package file count'
record={'source':meta['source'],'zip_sha256':meta['zip_sha256'],'files':rows,'all_copied':False,'appearance_verified':False}
recordpath.write_bytes(json.dumps(record,ensure_ascii=False,indent=2).encode())
with zipfile.ZipFile('outputs/本次和平皮肤导入前原文件备份.zip','w',zipfile.ZIP_DEFLATED) as z:
 for row in rows:
  if row['existed_before']:z.write(row['original_backup'],PurePosixPath(row['archive_path']).name)
 z.writestr('manifest.json',json.dumps(record,ensure_ascii=False,indent=2))
a.sh('am force-stop com.tencent.tmgp.pubgmhd')
for index,row in enumerate(rows):
 remote='/data/local/tmp/user-skin-payload-'+str(index)
 subprocess.run(a.adb+['push',row['local_payload'],remote],capture_output=True,check=True)
 a.root('cp '+shlex.quote(remote)+' '+shlex.quote(row['target']))
 actual=a.root('sha256sum '+shlex.quote(row['target'])).split()[0]
 assert actual==row['payload_sha256'],'Installed checksum mismatch'
 row['imported']=True;row['installed_sha256']=actual
 recordpath.write_bytes(json.dumps(record,ensure_ascii=False,indent=2).encode())
record['all_copied']=True;recordpath.write_bytes(json.dumps(record,ensure_ascii=False,indent=2).encode())
print(json.dumps({'copied_files':len(rows),'original_files_backed_up':sum(r['existed_before'] for r in rows),'each_installed_hash_verified':True,'filenames':[PurePosixPath(r['archive_path']).name for r in rows]},ensure_ascii=False))
print(a.sh('am start -n com.tencent.tmgp.pubgmhd/com.epicgames.ue4.SplashActivity'))
