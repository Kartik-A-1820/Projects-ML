from pathlib import Path
import argparse,sys
ROOT=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT/'src'))
from smartresume.core import match_resume_to_job,result_to_dict
def main():
    p=argparse.ArgumentParser(); p.add_argument('--resume',required=True); p.add_argument('--job',required=True); a=p.parse_args()
    r=result_to_dict(match_resume_to_job(Path(a.resume).read_text(),Path(a.job).read_text()))
    print('overall_score='+str(r['overall_score'])); print('lexical_score='+str(r['lexical_score'])); print('skill_score='+str(r['skill_score'])); print('matched_skills='+', '.join(r['matched_skills'])); print('missing_skills='+', '.join(r['missing_skills']))
if __name__=='__main__': main()
