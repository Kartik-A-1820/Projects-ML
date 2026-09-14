import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from driftwatch.synthetic import reference_data,stream_window
from driftwatch.monitor import DriftMonitor
from driftwatch.alerts import PersistentAlert

ref=reference_data();m=DriftMonitor();a=PersistentAlert()
for i,shift in enumerate([0,0,.2,.8,.8,.8,0,0]):
    rows=m.inspect(ref,stream_window(seed=100+i,shift=shift))
    any_drift=any(r.drifted for r in rows)
    print(i,shift,[(r.feature,round(r.severity,3),r.drifted) for r in rows],'alert',a.update(any_drift))
