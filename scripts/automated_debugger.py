#!/usr/bin/env python3
from __future__ import annotations
import compileall, datetime as dt, json, subprocess, sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]; REPORTS=ROOT/'reports'
class Parser(HTMLParser): pass

def check(name,func):
    try: func(); return {'name':name,'passed':True,'detail':'OK'}
    except Exception as exc: return {'name':name,'passed':False,'detail':str(exc)}
def required_files():
    required=['index.html','style.css','app.js','README.md','DISCLAIMER.md','config/benefits.json','config/official-sources.json','data/current/benefits.json','scripts/update_information.py']
    missing=[p for p in required if not (ROOT/p).exists()]
    if missing: raise AssertionError('Missing: '+', '.join(missing))
def valid_json():
    for path in ROOT.rglob('*.json'): json.loads(path.read_text(encoding='utf-8'))
def valid_html(): Parser().feed((ROOT/'index.html').read_text(encoding='utf-8'))
def valid_python():
    if not compileall.compile_dir(str(ROOT/'scripts'),quiet=1,force=True): raise AssertionError('Python compilation failed')
def valid_js():
    result=subprocess.run(['node','--check','app.js'],cwd=ROOT,capture_output=True,text=True)
    if result.returncode: raise AssertionError(result.stderr.strip())
def valid_data():
    data=json.loads((ROOT/'data/current/benefits.json').read_text())
    if not data.get('benefits'): raise AssertionError('No benefit records')
    ids=set()
    for item in data['benefits']:
        for key in ['id','title','category','summary','official_url']:
            if not item.get(key): raise AssertionError(f"{item.get('id','unknown')} missing {key}")
        if item['id'] in ids: raise AssertionError('Duplicate id '+item['id'])
        ids.add(item['id'])
        if urlparse(item['official_url']).scheme!='https': raise AssertionError('Non-HTTPS URL')
def main():
    REPORTS.mkdir(exist_ok=True)
    checks=[check('Required files',required_files),check('JSON validation',valid_json),check('HTML parse',valid_html),check('Python syntax',valid_python),check('JavaScript syntax',valid_js),check('Benefit data validation',valid_data)]
    status='PASSED' if all(c['passed'] for c in checks) else 'FAILED'
    report={'generated_at':dt.datetime.now(dt.timezone.utc).isoformat(),'status':status,'checks':checks}
    (REPORTS/'latest-debug-report.json').write_text(json.dumps(report,indent=2)+'\n')
    lines=['# Automated Debug Report','',f"Status: **{status}**",'']+[f"- {'PASS' if c['passed'] else 'FAIL'} — {c['name']}: {c['detail']}" for c in checks]
    (REPORTS/'latest-debug-report.md').write_text('\n'.join(lines)+'\n')
    print(status)
    return 0 if status=='PASSED' else 1
if __name__=='__main__': raise SystemExit(main())
