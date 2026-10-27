"""Fallback: copy verified project files into a local Projects-ML checkout."""
import argparse
import shutil
import subprocess
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True, help='Path to an existing Projects-ML git checkout')
    p.add_argument('--push', action='store_true')
    args = p.parse_args()
    repo = Path(args.repo).resolve()
    src = Path(__file__).resolve().parents[1]
    if not (repo / '.git').exists():
        raise ValueError('repo must be an existing Git checkout')
    dest = repo / 'weekly-projects' / 'week-37-contracttrace-agent-transactions'
    if dest.exists():
        raise FileExistsError('refusing to overwrite existing project')
    for path in src.rglob('*'):
        if not path.is_file() or any(x in path.parts for x in ('__pycache__', '.pytest_cache')):
            continue
        if path.suffix in ('.pyc', '.sqlite', '.db') or path.name == '.env':
            continue
        target = dest / path.relative_to(src)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    print(f'Copied project to {dest}')
    if args.push:
        subprocess.run(['git','-C',str(repo),'add',str(dest.relative_to(repo))],check=True)
        subprocess.run(['git','-C',str(repo),'commit','-m','Week 37: ContractTrace verified agent transactions'],check=True)
        subprocess.run(['git','-C',str(repo),'push','origin','main'],check=True)


if __name__ == '__main__':
    main()
