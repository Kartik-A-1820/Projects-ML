import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from driftwatch.synthetic import reference_data,stream_window
from driftwatch.monitor import DriftMonitor
from driftwatch.alerts import PersistentAlert

ref=reference_data(seed=7);m=DriftMonitor();a=PersistentAlert(persistence_windows=2)
shifts=[0]*10+[0.8]*6
alerts=[];drift_flags=[]
for i,s in enumerate(shifts):
    rows=m.inspect(ref,stream_window(seed=1000+i,shift=s))
    d=any(r.drifted for r in rows);drift_flags.append(d);alerts.append(a.update(d))
false_alarm_rate=sum(drift_flags[:10])/10
first=next((i for i,x in enumerate(alerts[10:],start=10) if x),None)
delay=None if first is None else first-10
print({'false_alarm_rate':false_alarm_rate,'detection_delay_windows':delay,'raw_drift_flags':drift_flags,'persistent_alerts':alerts})
