from continuallearn.features import HashingTextEncoder
from continuallearn.replay import ReplayBuffer
from continuallearn.metrics import forgetting
from continuallearn.trainer import ContinualTrainer
def test_encoder_shape():assert HashingTextEncoder(64).encode(['hello world']).shape==(1,64)
def test_buffer_capacity():
    b=ReplayBuffer(2);b.add('a',[('x','1'),('y','2'),('z','3')]);assert len(b.items)==2
def test_forgetting():assert forgetting([{'a':.9},{'a':.6}])['a']==.30000000000000004
def test_learning():
    t=ContinualTrainer(dim=128,replay_per_task=2);r=t.learn('a',[('refund card','billing'),('password login','account')],epochs=20);assert 'a' in r['scores']
