import requests,json,zipfile,hashlib,subprocess,concurrent.futures
from pathlib import Path
p=Path('work/game-fps-research/prepared');p.mkdir(parents=True,exist_ok=True)
adb=['adb','-s','1916b8f1']
def sh(c):
 return subprocess.check_output(adb+['shell',c],text=True,encoding='utf-8',errors='replace',timeout=40)
def root(c):return sh("su -c '"+c.replace("'","'\\''")+"'")
def release(repo):
 s=requests.Session();s.headers['User-Agent']='Codex-tablet-preparation'
 r=s.get('https://api.github.com/repos/'+repo+'/releases/latest',timeout=30);r.raise_for_status();j=r.json()
 (p/(repo.split('/')[1]+'-release.json')).write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')
 a=next(x for x in j['assets'] if x['name'].endswith('.zip'))
 r=s.get(a['browser_download_url'],timeout=60);r.raise_for_status();b=r.content;h=hashlib.sha256(b).hexdigest()
 if a.get('digest'):assert a['digest']=='sha256:'+h
 (p/a['name']).write_bytes(b)
 z=zipfile.ZipFile(p/a['name']);listing=z.namelist()
 texts={n:z.read(n).decode('utf-8',errors='replace') for n in listing if n.endswith(('.sh','.json','.prop')) and z.getinfo(n).file_size<200000}
 (p/(repo.split('/')[1]+'-zip-text.json')).write_text(json.dumps(texts,ensure_ascii=False,indent=2),encoding='utf-8')
 return {'repo':repo,'tag':j['tag_name'],'published':j['published_at'],'asset':a['name'],'url':a['browser_download_url'],'sha256':h,'digest':a.get('digest'),'files':listing,'module.prop':texts.get('module.prop'),'body':j['body'][:1800]}
def baseline():
 props=json.loads('{}')
 props['root']=root('id');props['battery']=sh('dumpsys battery');props['density']=sh('wm density');props['props']=sh('getprop')
 props['modules']=root('ls -la /data/adb/modules /data/adb/modules_update 2>/dev/null; /data/adb/ksud --help; /data/adb/ksud module --help')
 props['window']='\n'.join(x for x in sh('dumpsys window').splitlines() if 'mCurrentFocus' in x)
 (p/'device-before.json').write_text(json.dumps(props,ensure_ascii=False,indent=2),encoding='utf-8')
 return {k:v for k,v in props.items() if k!='props'}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 tasks=[ex.submit(release,'LSPosed/ZygiskNext'),ex.submit(release,'AlirezaParsi/COPG'),ex.submit(baseline)]
 for t in tasks:
  try:print(json.dumps(t.result(),ensure_ascii=False),flush=True)
  except Exception as e:print(type(e).__name__,str(e),flush=True)
