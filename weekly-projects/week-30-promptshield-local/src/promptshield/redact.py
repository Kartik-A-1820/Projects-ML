import re
def redact(text,patterns=("api_key","password","secret")):
    out=str(text)
    for key in patterns:
        out=re.sub(rf"(?i)({re.escape(key)}\s*[:=]\s*)([^\s,;]+)",r"\1[REDACTED]",out)
    return out
