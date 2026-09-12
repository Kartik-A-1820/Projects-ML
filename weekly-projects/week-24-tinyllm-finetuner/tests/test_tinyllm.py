import torch
from tinyllm.model import TinyEncoder
from tinyllm.tokenizer import HashTokenizer
def test_tokenizer_shape():
    assert HashTokenizer().encode("hello world").shape[0]==20
def test_lora_reduces_trainable_params():
    full=TinyEncoder(mode="full");lora=TinyEncoder(mode="lora",rank=4)
    assert lora.trainable_parameters()<full.trainable_parameters()
def test_masked_rank_forward():
    m=TinyEncoder(mode="lora",rank=4,active_rank=2)
    x=torch.randint(1,50,(2,20));assert m(x).shape==(2,4)
