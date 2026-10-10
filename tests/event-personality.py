#!/usr/bin/env python3
import importlib.machinery, importlib.util, json, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
loader=importlib.machinery.SourceFileLoader('personality',str(ROOT/'bin/subcult-personality'));spec=importlib.util.spec_from_loader(loader.name,loader);p=importlib.util.module_from_spec(spec);loader.exec_module(p)
with tempfile.TemporaryDirectory() as tmp:
    p.d.CONFIG=Path(tmp)/'config';p.d.STATE=Path(tmp)/'state';p.LAST=p.d.STATE/'personality-last.json'
    assert p.emit('mission-complete')['reason']=='disabled' and not p.d.STATE.exists()
    value=p.policy();value['enabled']=True;p.d.atomic(p.d.CONFIG/'personality.json',value)
    assert p.decision('mission-complete',hour=23,focus=False)['reason']=='quiet-hours'
    assert p.decision('mission-complete',hour=12,focus=True)['reason']=='focus-active'
    calls=[]
    def run(argv,**kw):calls.append(argv);return 'inactive' if argv==['subcult-focus','status'] else ''
    p.d.run=run;p.time.localtime=lambda:type('Clock',(),{'tm_hour':12})()
    result=p.emit('mission-complete');assert result['one_shot'] and any('mode-transition' in row for row in calls)
    assert not any(row[0]=='subcult-sound' for row in calls)
    assert p.emit('recipe-applied')['reason']=='cooldown'
    value['sound']=True;p.d.atomic(p.d.CONFIG/'personality.json',value);p.LAST.unlink();p.d.probe=lambda *_: {'cues':{'nominal':{'audible':False}}}
    assert p.emit('session-end')['sound_audible'] is False
    assert not any('preview' in row or row==['subcult-sound','nominal'] for row in calls)
print('Disabled cues, quiet/focus suppression, one-shot visual, cooldown, and sound authority passed')
