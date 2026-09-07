from __future__ import annotations
from pathlib import Path
import subprocess, shlex

def guarded_replace(root,relative_path,old,new):
    root=Path(root).resolve()
    target=(root/relative_path).resolve()
    if root not in target.parents:
        raise ValueError("path escapes repository")
    text=target.read_text(encoding="utf-8")
    if old not in text:
        raise ValueError("expected text not found")
    target.write_text(text.replace(old,new,1),encoding="utf-8")
    return target

def run_tests(root,command="python -m pytest -q",timeout=30):
    allowed=("python -m pytest","pytest")
    if not any(command.startswith(x) for x in allowed):
        raise ValueError("test command not allowlisted")
    p=subprocess.run(shlex.split(command),cwd=root,capture_output=True,text=True,timeout=timeout)
    return {"exit_code":p.returncode,"stdout":p.stdout,"stderr":p.stderr}
