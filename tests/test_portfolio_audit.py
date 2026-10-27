from scripts.audit_portfolio import collect

def test_inventory_detects_missing_code_without_claiming_verification(tmp_path):
    for path in ['weekly-projects/week-01-demo','weekly-projects/week-03-demo','data-science-labs/ds-week-02-demo']:
        (tmp_path/path).mkdir(parents=True)
        (tmp_path/path/'README.md').write_text('demo')
    result=collect(tmp_path)
    weekly=result['series']['weekly-projects']
    assert weekly['missing_weeks_up_to_latest_present']==[2]
    assert 'implementation (.py/.ipynb)' in weekly['projects'][0]['missing']
    assert weekly['projects'][0]['runtime_verified'] is False
    assert result['series']['data-science-labs']['missing_weeks_up_to_latest_present']==[1]
