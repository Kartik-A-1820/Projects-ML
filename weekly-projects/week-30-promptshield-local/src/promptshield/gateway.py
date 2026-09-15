from .redact import redact
class SecureToolGateway:
    def __init__(self,policy,audit=None,max_tool_calls=4):
        self.policy=policy;self.audit=audit;self.max_tool_calls=max_tool_calls;self.calls={}
    def request(self,session_id,objective,tool,args,observation="",approved=False):
        n=self.calls.get(session_id,0)
        if n>=self.max_tool_calls:
            decision={"allowed":False,"reason":"tool_budget_exceeded","risk":"high","require_approval":False}
        else:
            decision=self.policy.authorize(tool,args,observation,approved).__dict__
        self.calls[session_id]=n+1
        event={"session_id":session_id,"objective":objective,"tool":tool,"args":redact(args),"observation":redact(observation),**decision}
        if self.audit:self.audit.write(event)
        return event
