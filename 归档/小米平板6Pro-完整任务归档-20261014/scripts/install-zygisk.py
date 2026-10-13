import subprocess,json,hashlib
from pathlib import Path
adb=['adb','-s','1916b8f1'];p=Path('work/game-fps-research/prepared')
def run(args,timeout=100):
 r=subprocess.run(adb+args,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=timeout)
 print(r.stdout+r.stderr,flush=True);r.check_returncode();return r.stdout
def root(c):return run(['shell',"su -c '"+c.replace("'","'\\''")+"'"])
f=p/'Zygisk-Next-1.5.1-862-56ae062-release.zip';assert hashlib.sha256(f.read_bytes()).hexdigest()=='17c506ffea119f03e5e9d9c70acd400efdd804f35d8968d0d56a5d66fea9f3ab'
root('/data/adb/ksud module list')
run(['push',str(f),'/data/local/tmp/zygisk-next-official.zip'])
root('sha256sum /data/local/tmp/zygisk-next-official.zip')
log=root('/data/adb/ksud module install /data/local/tmp/zygisk-next-official.zip')
(p/'zygisk-install.log').write_text(log,encoding='utf-8')
root('/data/adb/ksud module list; ls -la /data/adb/modules /data/adb/modules_update 2>/dev/null')
