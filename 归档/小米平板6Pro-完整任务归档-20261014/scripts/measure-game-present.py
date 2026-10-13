import time,re,json,sys,statistics
from pathlib import Path
from importlib.machinery import SourceFileLoader
a=SourceFileLoader('dev','work/adb-device.py').load_module()
secs=int(sys.argv[1]) if len(sys.argv)>1 else 20
label=sys.argv[2] if len(sys.argv)>2 else 'post-spoof'
out=Path('work/game-fps-research/prepared');frames=set();samples=[];last=0;layer=None;start=time.monotonic()
def names():
 vals=[]
 for line in a.sh('dumpsys SurfaceFlinger --list').splitlines():
  if 'SurfaceView[com.tencent.tmgp.pubgmhd' in line and '(BLAST)' in line:
   m=re.search(r'RequestedLayerState\{(.+?) parentId=',line)
   if m:vals.append(m.group(1))
 return vals
ns=names();assert ns,'Game render surface absent';layer=ns[-1];print('Sampling',layer,secs,'seconds',flush=True)
while time.monotonic()-start<secs:
 raw=a.sh("dumpsys SurfaceFlinger --latency '"+layer.replace("'","'\\''")+"'")
 vals=[]
 for l in raw.splitlines()[1:]:
  x=l.split()
  if len(x)==3 and x[1].isdigit():
   t=int(x[1])
   if 0<t<9223372036854775807:vals.append(t)
 if vals:
  if last==0:last=max(vals)
  else:
   new=[v for v in vals if v>last];frames.update(new);last=max(vals+[last])
  samples.append({'elapsed':round(time.monotonic()-start,3),'refresh_period_ns':raw.splitlines()[0],'latest':max(vals),'new_total':len(frames)})
 time.sleep(.4)
f=sorted(frames);d=[(y-x)/1e6 for x,y in zip(f,f[1:])];dur=(f[-1]-f[0])/1e9 if len(f)>1 else 0
result={'scene_label':label,'sampling_seconds':secs,'layer':layer,'unique_presented_frames':len(f),'frame_span_seconds':dur,'presented_fps':(len(f)-1)/dur if dur else None,'interval_median_ms':statistics.median(d) if d else None,'interval_p95_ms':sorted(d)[int(.95*(len(d)-1))] if d else None,'samples':samples,'timestamps':f,'battery':a.sh('dumpsys battery')}
(out/(label+'-presented.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('timestamps','samples','battery')},ensure_ascii=False),flush=True)
