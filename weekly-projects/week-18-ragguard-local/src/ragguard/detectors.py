import re
from .normalize import normalize_text

PATTERNS = [
    r"ignore (all|any|the)? ?previous instructions",
    r"reveal (the )?(system prompt|hidden instructions|api keys?|secrets?)",
    r"print (environment variables|env vars)",
    r"do not answer the user",
    r"override (the )?(policy|rules|instructions)",
    r"act as (the )?system",
]

def injection_score(text: str):
    t = normalize_text(text).lower()
    hits = [p for p in PATTERNS if re.search(p,t)]
    score = min(1.0, 0.34 * len(hits) + (0.20 if "system" in t and "prompt" in t else 0.0))
    return score, hits

def secret_leak_score(text: str):
    t = normalize_text(text)
    rules = {"api_key":r"\b(?:sk|api)[-_][A-Za-z0-9_-]{12,}\b","bearer":r"\bBearer\s+[A-Za-z0-9._-]{12,}","password_assignment":r"(?i)\bpassword\s*[:=]\s*\S+"}
    hits=[name for name,pat in rules.items() if re.search(pat,t)]
    return min(1.0,0.5*len(hits)),hits
