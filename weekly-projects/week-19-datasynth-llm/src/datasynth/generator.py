import random

TEMPLATES={
"payment":["my {channel} payment was {problem}","{channel} transaction keeps {problem}","why did the {channel} purchase get {problem}"],
"refund":["my refund is still {status}","when will the reimbursement be {status}","refund for my return remains {status}"],
"account":["I need help with {account_issue}","please help me {account_issue}","my login has an {account_issue}"],
"shipping":["my package is {delivery}","shipment status says {delivery}","the courier delivery is {delivery}"]}
VALUES={"channel":["card","debit card","online"],"problem":["declined","rejected","failing"],"status":["pending","missing","unprocessed"],"account_issue":["resetting the password","recovering access","unlocking the account"],"delivery":["delayed","stuck in transit","not moving"]}

def generate(label,n=5,seed=42):
    rng=random.Random(seed);out=[]
    for _ in range(n):
        t=rng.choice(TEMPLATES[label])
        for k,vals in VALUES.items(): t=t.replace("{"+k+"}",rng.choice(vals))
        out.append({"text":t,"label":label,"generator":"template-v1"})
    return out
