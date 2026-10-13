import subprocess,json
from pathlib import Path
def shell(command):
    return subprocess.check_output(['adb','-s','1916b8f1','shell',command],text=True).strip()
rows=[r.split(None,3) for r in shell("su -c 'ps -A -o USER,PID,PPID,NAME'").splitlines()[1:] if r.strip()]
result={}
for package in ['bin.mt.plus','com.omarea.vtools']:
    ids={r[1] for r in rows if r[3]==package}
    selected=[]
    seen=set()
    changed=True
    while changed:
        changed=False
        for r in rows:
            if (r[1] in ids or r[2] in ids) and r[1] not in seen:
                selected.append(r)
                seen.add(r[1])
                ids.add(r[1])
                changed=True
    result[package]=selected
print(json.dumps(result,indent=2))
Path('work/app-process-evidence.json').write_text(json.dumps(result,indent=2))
