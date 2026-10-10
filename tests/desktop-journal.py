#!/usr/bin/env python3
import json, os, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
    env={**os.environ,'XDG_CONFIG_HOME':tmp+'/config','XDG_STATE_HOME':tmp+'/state','SUBCULT_OPERATIONS_STATE':tmp+'/events','SUBCULT_OPERATIONS_CONFIG':tmp+'/policy.json'}
    def run(*args):return subprocess.run([str(ROOT/'bin/subcult-journal'),*args],env=env,capture_output=True,text=True)
    assert json.loads(run('search').stdout)['count']==0 and not Path(tmp+'/events').exists()
    assert json.loads(run('event','focus-on').stdout)['recorded'] is False
    assert not Path(tmp+'/events').exists()
    assert run('enable').returncode==0
    assert run('session','start').returncode==0
    assert run('session','start').returncode!=0
    assert run('event','focus-on').returncode==0
    assert run('note','password=secret alice@example.com').returncode==0
    values=json.loads(run('search','','--category','focus').stdout);assert values['count']==1
    path=Path(tmp+'/events/events.jsonl');before=path.read_bytes();assert b'secret' not in before and b'alice@example.com' not in before
    assert run('search').returncode==0 and path.read_bytes()==before
    assert run('session','end').returncode==0
    assert json.loads(run('summary').stdout)['events_by_category']['focus']==1
    assert run('disable').returncode==0
    assert json.loads(run('event','focus-off').stdout)['recorded'] is False
print('Opt-in journal events, sanitized notes, read-only search, filters, and sessions passed')
