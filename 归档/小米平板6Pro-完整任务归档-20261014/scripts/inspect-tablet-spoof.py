import requests,json,zipfile,io,hashlib
from pathlib import Path
p=Path('work/game-fps-research/tablet-spoof');p.mkdir(parents=True,exist_ok=True)
s=requests.Session();s.headers['User-Agent']='Codex-tablet-research'
r=s.get('https://api.github.com/repos/ByRafaelSystem/Tablet-Spoofing-/releases',timeout=30);r.raise_for_status();j=r.json()
p.joinpath('releases.json').write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')
for rel in j[:2]:
 print('RELEASE',rel['tag_name'],rel['published_at'])
 for a in rel['assets']:
  print('ASSET',a['name'],a['size'],a['browser_download_url'],a.get('digest'))
  if a['name'].lower().endswith('.zip'):
   raw=s.get(a['browser_download_url'],timeout=30);raw.raise_for_status();b=raw.content
   dest=p/a['name'];dest.write_bytes(b);print('SHA256',hashlib.sha256(b).hexdigest())
   z=zipfile.ZipFile(io.BytesIO(b));print('FILES',z.namelist())
   for n in z.namelist():
    if n.endswith(('.sh','.prop','.json','.txt')) and z.getinfo(n).file_size<100000:
     print('FILE',n,'\n',z.read(n).decode('utf-8',errors='replace'))
   break
 break
