from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import ast, re

TOKEN=re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

@dataclass
class CodeFile:
    path:str
    text:str
    symbols:tuple[str,...]
    imports:tuple[str,...]

def python_metadata(text):
    symbols=[]; imports=[]
    try:
        tree=ast.parse(text)
    except SyntaxError:
        return (),()
    for node in ast.walk(tree):
        if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
            symbols.append(node.name)
        elif isinstance(node,ast.Import):
            imports.extend(a.name for a in node.names)
        elif isinstance(node,ast.ImportFrom):
            module=node.module or ""
            imports.append(module)
            imports.extend(a.name for a in node.names)
    return tuple(sorted(set(symbols))),tuple(sorted(set(imports)))

def scan_repository(root,extensions=None,max_file_bytes=250000):
    root=Path(root)
    extensions=set(extensions or [".py",".md",".yaml",".yml",".toml",".json"])
    out=[]
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in extensions:
            continue
        if any(part.startswith(".") for part in p.relative_to(root).parts):
            continue
        if p.stat().st_size>max_file_bytes: continue
        text=p.read_text(encoding="utf-8",errors="ignore")
        symbols,imports=python_metadata(text) if p.suffix==".py" else ((),())
        out.append(CodeFile(str(p.relative_to(root)).replace("\\","/"),text,symbols,imports))
    return out
