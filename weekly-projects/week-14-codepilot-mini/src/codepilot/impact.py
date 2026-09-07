def reverse_import_map(files):
    out={}
    for f in files:
        for imp in f.imports:
            out.setdefault(imp,[]).append(f.path)
    return {k:sorted(v) for k,v in out.items()}
