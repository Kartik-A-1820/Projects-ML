"""UCI HAR loader, synthetic smoke fixture, leakage-safe feature engineering and subject split."""
from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile
import numpy as np
import pandas as pd
from scipy.signal import welch
from sklearn.model_selection import GroupShuffleSplit

SEED=20261031
URL='https://archive.ics.uci.edu/static/public/240/human+activity+recognition+using+smartphones.zip'
CHANNELS=[f'{kind}_{axis}' for kind in ('body_acc','body_gyro','total_acc') for axis in 'xyz']
LABELS=['WALKING','WALKING_UPSTAIRS','WALKING_DOWNSTAIRS','SITTING','STANDING','LAYING']

def download(root='data'):
    root=Path(root); root.mkdir(parents=True,exist_ok=True)
    target=root/'uci_har.zip'
    if not target.exists(): urlretrieve(URL,target)
    with ZipFile(target) as outer:
        names=outer.namelist()
        inner=[n for n in names if n.endswith('UCI HAR Dataset.zip')]
        if inner:
            import io
            with ZipFile(io.BytesIO(outer.read(inner[0]))) as z: z.extractall(root)
        else: outer.extractall(root)
    path=root/'UCI HAR Dataset'
    if not path.exists():
        paths=list(root.rglob('Inertial Signals'))
        if not paths: raise FileNotFoundError('Inertial Signals missing in UCI archive')
        path=paths[0].parent.parent
    return path

def load_real(root='data/UCI HAR Dataset'):
    root=Path(root)
    if not (root/'train').exists(): raise FileNotFoundError(f'{root} not found; see DATASET.md')
    all_x=[]; all_y=[]; all_subject=[]; all_split=[]
    for split in ('train','test'):
        base=root/split
        signals=[np.loadtxt(base/'Inertial Signals'/f'{c}_{split}.txt',dtype=np.float32) for c in CHANNELS]
        x=np.stack(signals,axis=-1).astype(np.float32)
        y=np.loadtxt(base/f'y_{split}.txt',dtype=np.int64)-1
        subjects=np.loadtxt(base/f'subject_{split}.txt',dtype=np.int64)
        assert x.shape==(len(y),128,9)
        all_x.append(x);all_y.append(y);all_subject.append(subjects);all_split.extend([split]*len(y))
    return np.concatenate(all_x),np.concatenate(all_y),np.concatenate(all_subject),np.array(all_split), 'uci_har_real'

def synthetic(seed=SEED,n_subjects=24,windows_per_subject=36):
    """Synthetic six-class signals for execution only; NEVER report as benchmark evidence."""
    rng=np.random.default_rng(seed);t=np.arange(128,dtype=np.float32)/50
    X=[];Y=[];S=[];SP=[]
    for subj in range(n_subjects):
        scale=rng.uniform(.65,1.4); phase=rng.uniform(0,2*np.pi)
        for k in range(windows_per_subject):
            label=(k+subj)%6
            freq=[1.6,2.2,1.1,.10,.13,.04][label]
            amp=[1.2,1.3,1.1,.12,.17,.045][label]
            base=amp*np.sin(2*np.pi*freq*t+phase)
            body=np.stack([base, .7*np.cos(2*np.pi*freq*t+phase),.35*base],axis=-1)
            gyro=np.stack([.4*base,.3*base,.6*np.cos(2*np.pi*freq*t+phase)],axis=-1)
            gravity=np.broadcast_to(np.array([.05,.1,.98],np.float32),(128,3))
            total=body+gravity
            signal=np.concatenate([body,gyro,total],axis=-1)*scale
            signal+=rng.normal(0,.06,signal.shape)
            X.append(signal.astype(np.float32));Y.append(label);S.append(subj);SP.append('train' if subj<n_subjects-6 else 'test')
    return np.stack(X),np.array(Y),np.array(S),np.array(SP),'synthetic_smoke_NOT_REAL'

def split_subjects(subjects,original_split,seed=SEED):
    subjects=np.asarray(subjects); original_split=np.asarray(original_split)
    train_pool=np.where(original_split=='train')[0]; test=np.where(original_split=='test')[0]
    assert not set(subjects[train_pool]) & set(subjects[test])
    splitter=GroupShuffleSplit(n_splits=1,test_size=.25,random_state=seed)
    keep,cal=next(splitter.split(train_pool,groups=subjects[train_pool]))
    pool=train_pool[keep];calibration=train_pool[cal]
    splitter=GroupShuffleSplit(n_splits=1,test_size=.25,random_state=seed+1)
    keep,val=next(splitter.split(pool,groups=subjects[pool]))
    out={'train':pool[keep], 'validation':pool[val], 'calibration':calibration, 'test':test}
    for a,ia in out.items():
        for b,ib in out.items():
            if a!=b: assert set(subjects[ia]).isdisjoint(set(subjects[ib])),(a,b)
    return out

def engineer(x):
    """Only within-window causal sensor statistics; no subject IDs, targets, future windows."""
    x=np.asarray(x,dtype=np.float32)
    if x.ndim!=3 or x.shape[1:]!=(128,9): raise ValueError('Expected N x 128 x 9')
    result={}
    for j,c in enumerate(CHANNELS):
        a=x[:,:,j]
        result[c+'_mean']=a.mean(axis=1)
        result[c+'_std']=a.std(axis=1)
        result[c+'_rms']=np.sqrt((a*a).mean(axis=1))
        result[c+'_iqr']=np.percentile(a,75,axis=1)-np.percentile(a,25,axis=1)
        result[c+'_jerk_rms']=np.sqrt(np.square(np.diff(a,axis=1)*50).mean(axis=1))
        fft=np.abs(np.fft.rfft(a-a.mean(axis=1,keepdims=True),axis=1))**2
        result[c+'_spectral_energy']=np.log1p(fft[:,1:].sum(axis=1))
        result[c+'_dominant_hz']=np.argmax(fft[:,1:],axis=1).astype(np.float32)*50/128+50/128
    for start,kind in ((0,'body_acc'),(3,'body_gyro'),(6,'total_acc')):
        mag=np.linalg.norm(x[:,:,start:start+3],axis=2)
        result[kind+'_magnitude_mean']=mag.mean(axis=1)
        result[kind+'_magnitude_std']=mag.std(axis=1)
        result[kind+'_magnitude_jerk']=np.sqrt((np.diff(mag,axis=1)**2).mean(axis=1))*50
        axes=x[:,:,start:start+3]
        for a,b in ((0,1),(0,2),(1,2)):
            aa=axes[:,:,a]-axes[:,:,a].mean(axis=1,keepdims=True)
            bb=axes[:,:,b]-axes[:,:,b].mean(axis=1,keepdims=True)
            corr=(aa*bb).mean(axis=1)/(aa.std(axis=1)*bb.std(axis=1)+1e-5)
            result[f'{kind}_corr_{a}{b}']=corr
    df=pd.DataFrame(result).astype('float32')
    return df.replace([np.inf,-np.inf],np.nan)

def rotate_and_noise(x,seed=SEED,noise=.03,rotation=True,drop_gyro=False):
    rng=np.random.default_rng(seed);z=np.array(x,copy=True,dtype=np.float32)
    if rotation:
        theta=rng.uniform(-.35,.35)
        R=np.array([[np.cos(theta),-np.sin(theta),0],[np.sin(theta),np.cos(theta),0],[0,0,1]],np.float32)
        for j in (0,3,6): z[:,:,j:j+3]=z[:,:,j:j+3]@R.T
    z+=rng.normal(0,noise,z.shape).astype(np.float32)
    if drop_gyro: z[:,:,3:6]=0
    return z
