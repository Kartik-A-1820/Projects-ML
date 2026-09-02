from visiontrack.core import Detection, IoUTracker, LineCrossingCounter, iou

def test_iou():
    assert iou((0,0,10,10),(0,0,10,10)) == 1.0
    assert iou((0,0,10,10),(20,20,30,30)) == 0.0

def test_track_id_persists():
    t=IoUTracker(iou_threshold=.1)
    a=t.update([Detection((0,0,20,20),.9,0,'car')])[0].track_id
    b=t.update([Detection((2,2,22,22),.8,0,'car')])[0].track_id
    assert a==b

def test_crossing_event():
    t=IoUTracker(iou_threshold=.05); c=LineCrossingCounter((0,50,100,50))
    c.update(t.update([Detection((10,20,30,40),.9,0,'car')]),0)
    c.update(t.update([Detection((10,35,30,55),.9,0,'car')]),1)
    ev=c.update(t.update([Detection((10,45,30,65),.9,0,'car')]),2)
    assert len(ev)==1
