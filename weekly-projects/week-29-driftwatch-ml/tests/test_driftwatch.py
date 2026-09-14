from driftwatch.synthetic import reference_data,stream_window
from driftwatch.monitor import DriftMonitor
from driftwatch.alerts import PersistentAlert
from driftwatch.performance import DelayedLabelPerformance

def test_stable_window_mostly_clean():
    r=DriftMonitor().inspect(reference_data(seed=1),stream_window(seed=2,shift=0))
    assert sum(x.drifted for x in r)<=1

def test_strong_shift_detected():
    r=DriftMonitor().inspect(reference_data(seed=1),stream_window(seed=2,shift=1.0))
    assert any(x.drifted for x in r)

def test_small_batch_guard():
    r=DriftMonitor(min_batch_size=500).inspect(reference_data(n=100,seed=1),stream_window(n=100,seed=2,shift=1))
    assert all(x.reason=='insufficient_samples' for x in r)

def test_persistence_blocks_single_spike():
    a=PersistentAlert(persistence_windows=2)
    assert not a.update(True)
    assert not a.update(False)

def test_persistence_triggers_on_repeated_drift():
    a=PersistentAlert(persistence_windows=2);a.update(True)
    assert a.update(True)

def test_delayed_labels():
    p=DelayedLabelPerformance();p.add_prediction('a',1,.9);p.add_prediction('b',0,.7)
    assert p.accuracy() is None
    p.add_label('a',1)
    assert p.accuracy()==1.0
