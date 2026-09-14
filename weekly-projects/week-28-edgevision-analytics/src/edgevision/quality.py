import numpy as np

def focus_score(image):
    gx=np.abs(np.diff(image,axis=1)).mean(); gy=np.abs(np.diff(image,axis=0)).mean()
    return float((gx+gy)/2)

def assess_quality(image,min_brightness=.15,max_brightness=.92,min_focus_score=.015):
    brightness=float(image.mean()); focus=focus_score(image); reasons=[]
    if brightness<min_brightness: reasons.append('too_dark')
    if brightness>max_brightness: reasons.append('too_bright')
    if focus<min_focus_score: reasons.append('low_focus')
    return {'accepted':not reasons,'brightness':brightness,'focus_score':focus,'reasons':reasons}
