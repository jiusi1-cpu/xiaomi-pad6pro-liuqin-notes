from pathlib import Path,PurePosixPath
from importlib.machinery import SourceFileLoader
import subprocess,zipfile,json,hashlib
a=SourceFileLoader('dev','work/adb-device.py').load_module()
base=Path('work/new-skin-pak');base.mkdir(exist_ok=True)
source='/sdcard/Download/MiShare/仁济和平_全皮肤美化_PAK.zip'
local=base/'user-skin-pack.zip'
subprocess.run(a.adb+['pull',source,str(local)],capture_output=True,check=True)
rows=[]
with zipfile.ZipFile(local) as z:
 bad=z.testzip();assert bad is None,'ZIP CRC error: '+str(bad)
 for i in z.infolist():
  p=PurePosixPath(i.filename)
  assert not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename,'Unsafe archive path'
  r={'name':i.filename,'size':i.file_size,'directory':i.is_dir()}
  if not i.is_dir():
   data=z.read(i);r['sha256']=hashlib.sha256(data).hexdigest()
   if p.suffix.lower() in ['.txt','.md','.ini','.json','.sh','.lua'] and i.file_size<100000:r['text']=data.decode('utf-8','replace')[:12000]
  rows.append(r)
result={'source':source,'zip_sha256':hashlib.sha256(local.read_bytes()).hexdigest(),'entries':rows,'crc_verified':True}
(base/'inspection.json').write_bytes(json.dumps(result,ensure_ascii=False,indent=2).encode());print(json.dumps(result,ensure_ascii=False,indent=2))
