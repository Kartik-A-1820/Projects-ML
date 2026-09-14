from edgevision.synthetic import make_frame
from edgevision.quality import assess_quality
from edgevision.detector import detect
from edgevision.pipeline import EdgeVisionPipeline

def test_clean_frame_quality():
    img,_=make_frame(seed=1)
    assert assess_quality(img)['accepted']

def test_dark_frame_rejected():
    img,_=make_frame(seed=1,low_light=True)
    assert not assess_quality(img)['accepted']

def test_defect_detected():
    img,_=make_frame(defect=True,seed=2)
    assert detect(img)

def test_clean_has_fewer_or_no_hits():
    clean,_=make_frame(defect=False,seed=2); bad,_=make_frame(defect=True,seed=2)
    assert len(detect(clean))<=len(detect(bad))

def test_frame_stride():
    p=EdgeVisionPipeline(frame_stride=2); img,_=make_frame(seed=3)
    assert p.process(1,img)['status']=='skipped'
    assert p.process(2,img)['status']=='processed'
