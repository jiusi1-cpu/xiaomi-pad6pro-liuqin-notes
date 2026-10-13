import subprocess,json,time
from pathlib import Path
SERIAL='1916b8f1'
TARGET='com.omarea.vtools/com.omarea.vtools.AccessibilitySceneMode'
def shell(cmd):
    return subprocess.check_output(['adb','-s',SERIAL,'shell',cmd],text=True).strip()
old=shell('settings get secure enabled_accessibility_services')
active=shell('settings get secure accessibility_enabled')
Path('work/scene-accessibility-before.json').write_text(json.dumps({'enabled_services':old,'accessibility_enabled':active},indent=2))
if TARGET not in old.split(':') or active!='1':
    raise RuntimeError('Scene service not already authorized/enabled')
other=':'.join(x for x in old.split(':') if x!=TARGET)
shell("settings put secure enabled_accessibility_services '"+other+"'")
time.sleep(1)
shell("settings put secure enabled_accessibility_services '"+old+"'")
time.sleep(2)
state=shell('dumpsys accessibility')
Path('work/accessibility-after-rebind.txt').write_text(state)
print('\n'.join(l for l in state.splitlines() if any(t in l for t in ['Bound services','Enabled services','Crashed services','AccessibilitySceneMode'])))
