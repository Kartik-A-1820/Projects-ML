"""File inventory only; never labels code presence as a successful runtime test."""
import argparse
import json
from pathlib import Path
import re

def collect(root):
    root=Path(root)
    report={'scope':'repository_file_inventory_only','series':{}}
    for directory,prefix in [('weekly-projects','week'),('data-science-labs','ds-week')]:
        records=[]
        for project in sorted((root/directory).glob(prefix+'-*')):
            match=re.match(rf'{prefix}-(\d+)-',project.name)
            if not match or not project.is_dir():
                continue
            files=[path for path in project.rglob('*') if path.is_file() and '__pycache__' not in path.parts and '.pytest_cache' not in path.parts]
            implementation=[path for path in files if path.suffix in ('.py','.ipynb') and 'tests' not in path.relative_to(project).parts]
            expected=['README.md','requirements.txt'] + (['architecture.md'] if directory=='weekly-projects' else ['DATASET.md'])
            missing=[path for path in expected if not (project/path).is_file()]
            if not implementation:missing.append('implementation (.py/.ipynb)')
            if not any(path.name.startswith('test_') and path.suffix=='.py' for path in files):missing.append('tests')
            records.append({'week':int(match.group(1)),'path':project.relative_to(root).as_posix(),'missing':missing,'runtime_verified':False})
        present={item['week'] for item in records}
        report['series'][directory]={'projects':records,'missing_weeks_up_to_latest_present':[week for week in range(1,max(present,default=0)+1) if week not in present]}
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=json.dumps(collect(args.root),indent=2)+'\n'
    if args.output:args.output.write_text(result)
    else:print(result)
