from datasynth.generator import generate
from datasynth.privacy import pii_hits,nearest_overlap
from datasynth.quality import gate_dataset,label_balance
from datasynth.utility import train_on_synth_test_on_real
REF=[{"text":"card payment failed","label":"payment"},{"text":"refund missing","label":"refund"},{"text":"forgot password","label":"account"},{"text":"track package","label":"shipping"}]
def test_generation_deterministic(): assert generate("payment",3,7)==generate("payment",3,7)
def test_pii_detection(): assert "email" in pii_hits("write to a@example.com")
def test_near_copy_detected(): assert nearest_overlap("card payment failed",REF)>=.99
def test_gate_rejects_pii_and_copy():
    rows=[{"text":"email me at a@example.com","label":"account","generator":"x"},{"text":"card payment failed","label":"payment","generator":"x"},{"text":"shipment is delayed badly","label":"shipping","generator":"x"}]
    g=gate_dataset(rows,REF,.8); assert len(g["rejected"])==2 and len(g["accepted"])==1
def test_label_balance(): assert label_balance([{"label":"a"},{"label":"a"},{"label":"b"}])==.5
def test_utility_proxy_bounds():
    synth=[]
    for i,l in enumerate(["payment","refund","account","shipping"]): synth += generate(l,5,10+i)
    score=train_on_synth_test_on_real(synth,REF); assert 0<=score<=1
