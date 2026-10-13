import subprocess,time,json
from pathlib import Path
adb=['adb','-s','1916b8f1']
pkgs=['com.android.settings','bin.mt.plus','com.android.systemui','com.android.fileexplorer','com.miui.securitycenter','com.miui.calculator','com.miui.notes','com.omarea.vtools']
rows=[]
for pkg in pkgs:
    start=time.time()
    def sh(s):return subprocess.check_output(adb+['shell',s],text=True,encoding='utf-8',errors='replace')
    before=sh('pm art dump '+pkg)
    try: result=sh('cmd package compile -m speed -f '+pkg)
    except subprocess.CalledProcessError as e:result=e.output
    after=sh('pm art dump '+pkg)
    rows.append({'package':pkg,'before':before,'result':result,'after':after,'elapsed_sec':round(time.time()-start,2)})
    Path('work/selected-aot-results.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    print(pkg,result.strip(),round(time.time()-start,1),'sec',flush=True)
