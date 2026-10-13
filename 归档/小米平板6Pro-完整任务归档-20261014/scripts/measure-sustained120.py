import time,re,json,statistics,sys
from pathlib import Path
from importlib.machinery import SourceFileLoader
a=SourceFileLoader('dev','work/adb-device.py').load_module()
secs=int(sys.argv[1]) if len(sys.argv)>1 else 180
label=sys.argv[2] if len(sys.argv)>2 else 'user-training180sec-global120'
out=Path('work/game-fps-research/prepared');start=time.monotonic();frames=set();last=0;polls=[];health=[];errors=[]
names=[]
for line in a.sh('dumpsys SurfaceFlinger --list').splitlines():
 if 'SurfaceView[com.tencent.tmgp.pubgmhd' in line and '(BLAST)' in line:
  m=re.search(r'RequestedLayerState\{(.+?) parentId=',line)
  if m:names.append(m.group(1))
assert names;layer=names[-1]
thermal=a.root('for z in /sys/class/thermal/thermal_zone*; do case "$(cat $z/type)" in cpu_therm|gpuss-0|cpu-1-7) echo "$z/temp";; esac; done').splitlines()
thermal=[p for p in thermal if p.startswith('/sys/')]
def status():
 b=a.sh('dumpsys battery');h={'seconds':round(time.monotonic()-start,2)}
 for k in ['level','temperature']:
  m=re.search(r'^\s*'+k+r':\s*(\d+)',b,re.M);h[k]=int(m.group(1)) if m else None
 h['nodes']=a.root('cat '+' '.join(thermal+['/sys/class/kgsl/kgsl-3d0/gpuclk','/sys/class/kgsl/kgsl-3d0/gpubusy','/sys/devices/system/cpu/cpufreq/policy7/scaling_max_freq']),check=False).strip().splitlines()
 return h
health.append(status());nexthealth=30;nextprint=30;print('Started '+str(secs)+'sec measurement',flush=True)
while time.monotonic()-start<secs:
 t=time.monotonic()
 try:raw=a.sh("dumpsys SurfaceFlinger --latency '"+layer.replace("'","'\\''")+"'",timeout=4)
 except Exception as exc:
  errors.append({'seconds':time.monotonic()-start,'error':str(exc)})
  (out/(label+'-checkpoint.json')).write_bytes(json.dumps({'frames':sorted(frames),'polls':polls,'health':health,'errors':errors},ensure_ascii=False).encode())
  time.sleep(.25);continue
 vals=[]
 for l in raw.splitlines()[1:]:
  x=l.split()
  if len(x)==3 and x[1].isdigit():
   ts=int(x[1])
   if 0<ts<9223372036854775807:vals.append(ts)
 if vals:
  if last==0:last=max(vals)
  else:frames.update(v for v in vals if v>last);last=max([last]+vals)
 polls.append({'seconds':round(time.monotonic()-start,3),'duration':time.monotonic()-t,'frames':len(frames)})
 elapsed=time.monotonic()-start
 if elapsed>=nexthealth:health.append(status());nexthealth+=30
 if elapsed>=nextprint:
  fs=sorted(frames);recent=[f for f in fs if fs[-1]-f<=30e9]
  fps=(len(recent)-1)/((recent[-1]-recent[0])/1e9) if len(recent)>1 else 0
  print(json.dumps({'seconds':round(elapsed),'recent30sec_fps':round(fps,2),'battery_temp_c':health[-1]['temperature']/10}),flush=True);nextprint+=30
  (out/(label+'-checkpoint.json')).write_bytes(json.dumps({'frames':sorted(frames),'polls':polls,'health':health,'errors':errors},ensure_ascii=False).encode())
 time.sleep(.25)
fs=sorted(frames);ds=[(y-x)/1e6 for x,y in zip(fs,fs[1:])];span=(fs[-1]-fs[0])/1e9
bins=[]
for i in range(int(span)//10):
 f=[t for t in fs if i*10e9<=t-fs[0]<(i+1)*10e9];bins.append({'start':i*10,'fps':len(f)/10})
result={'label':label,'errors':errors,'actual_frame_count':len(fs),'frame_span_seconds':span,'average_fps':(len(fs)-1)/span,'interval_p50_ms':statistics.median(ds),'interval_p95_ms':sorted(ds)[int(.95*(len(ds)-1))],'interval_p99_ms':sorted(ds)[int(.99*(len(ds)-1))],'interval_over16_7ms_count':sum(x>16.7 for x in ds),'interval_over25ms_count':sum(x>25 for x in ds),'max_poll_gap_seconds':max(y['seconds']-x['seconds'] for x,y in zip(polls,polls[1:])),'bins10sec':bins,'health_node_order':thermal+['gpuclk','gpubusy','cpu7_max'],'health':health,'polls':polls,'timestamps':fs}
(out/(label+'.json')).write_bytes(json.dumps(result,ensure_ascii=False,indent=2).encode())
print(json.dumps({k:v for k,v in result.items() if k not in ['health','health_node_order','polls','timestamps','bins10sec']},ensure_ascii=False),flush=True)
