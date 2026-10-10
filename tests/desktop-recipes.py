#!/usr/bin/env python3
import json, os, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
    base=Path(tmp);mock=base/'bin';mock.mkdir()
    # A complete mock desktop proves transaction order and restoration without changing the host.
    calls=base/'calls';state=base/'state';state.mkdir()
    for name,body in {'hyprctl':'echo "$*" >> "$CALLS"; if [ "$1" = -j ]; then echo \'{"id":3}\'; fi', 'subcult-focus':'echo "focus $*" >> "$CALLS"; [ "$1" != status ] || echo inactive','subcult-motion':'echo "motion $*" >> "$CALLS"; [ "$1" != status ] || echo full','subcult-scene':'if [ "$1" = preview ]; then echo \'{"plan_id":"scene-test"}\'; else echo "scene $*" >> "$CALLS"; echo ok; fi'}.items():
        p=mock/name;p.write_text('#!/bin/sh\n'+body+'\n');p.chmod(0o755)
    env={**os.environ,'PATH':str(mock)+':'+os.environ['PATH'],'CALLS':str(calls),'XDG_CONFIG_HOME':tmp+'/config','XDG_STATE_HOME':str(state)}
    def run(*args):return subprocess.run([str(ROOT/'bin/subcult-recipe'),*args],env=env,capture_output=True,text=True)
    plan=json.loads(run('preview','write').stdout);assert not plan['unavailable'];assert not (state/'subcult-rice').exists()
    assert run('apply','write','--confirm','stale').returncode!=0
    assert run('apply','write','--confirm',plan['plan_id']).returncode==0
    text=calls.read_text();assert text.index('scene apply')<text.index('focus on')<text.index('motion set reduced')<text.index('dispatch workspace 4')
    assert run('undo').returncode==0
    assert 'dispatch workspace 3' in calls.read_text()
    assert not (state/'subcult-rice/recipe-last.json').exists()
    assert run('preview','unknown').returncode!=0
print('Recipe preview, stale refusal, ordered apply, and undo passed')
