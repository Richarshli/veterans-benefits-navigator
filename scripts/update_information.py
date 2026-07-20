#!/usr/bin/env python3
from __future__ import annotations
import datetime as dt
import json
import shutil
import ssl
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
SOURCES=ROOT/'config/official-sources.json'
BENEFITS=ROOT/'config/benefits.json'
CURRENT=ROOT/'data/current/benefits.json'
HISTORY=ROOT/'data/history'
USER_AGENT='VeteransBenefitsNavigator/1.0 (+public GitHub civic information project)'

def read(path): return json.loads(path.read_text(encoding='utf-8'))
def allowed(url, domains):
    parsed=urlparse(url); host=(parsed.hostname or '').lower()
    return parsed.scheme=='https' and any(host==d or host.endswith('.'+d) for d in domains)
def check(source, timeout):
    req=urllib.request.Request(source['url'],headers={'User-Agent':USER_AGENT,'Accept':'text/html,application/json;q=0.9,*/*;q=0.5'})
    try:
        with urllib.request.urlopen(req,timeout=timeout,context=ssl.create_default_context()) as response:
            return {'id':source['id'],'name':source['name'],'url':source['url'],'ok':200 <= response.status < 400,'status':response.status,'checked_at':dt.datetime.now(dt.timezone.utc).isoformat()}
    except urllib.error.HTTPError as exc:
        return {'id':source['id'],'name':source['name'],'url':source['url'],'ok':False,'status':exc.code,'checked_at':dt.datetime.now(dt.timezone.utc).isoformat(),'error':str(exc)}
    except Exception as exc:
        return {'id':source['id'],'name':source['name'],'url':source['url'],'ok':False,'status':None,'checked_at':dt.datetime.now(dt.timezone.utc).isoformat(),'error':str(exc)}
def atomic_write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile('w',encoding='utf-8',dir=path.parent,delete=False) as f:
        json.dump(data,f,indent=2); f.write('\n'); tmp=Path(f.name)
    tmp.replace(path)
def main():
    source_config=read(SOURCES); benefit_config=read(BENEFITS)
    domains=source_config['allowed_domains']; timeout=int(source_config.get('timeout_seconds',25))
    for source in source_config['sources']:
        if not allowed(source['url'],domains): raise ValueError(f"Unapproved source URL: {source['url']}")
    results=[check(source,timeout) for source in source_config['sources']]
    now=dt.datetime.now(dt.timezone.utc)
    output={'last_checked':now.isoformat(),'benefits':benefit_config['benefits'],'sources':results}
    atomic_write(CURRENT,output)
    HISTORY.mkdir(parents=True,exist_ok=True)
    atomic_write(HISTORY/(now.strftime('%Y-%m-%dT%H-%M-%SZ')+'.json'),output)
    print(f"Checked {len(results)} official sources: {sum(x['ok'] for x in results)} available, {sum(not x['ok'] for x in results)} need review.")
    return 0
if __name__=='__main__':
    try: raise SystemExit(main())
    except Exception as exc:
        print(f'Updater failed: {exc}',file=sys.stderr); raise SystemExit(1)
