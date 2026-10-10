#!/usr/bin/env python3
import json, os, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
import subcult_workflow as w
with tempfile.TemporaryDirectory() as tmp:
    w.d.CONFIG=Path(tmp)
    value={'schema_version':1,'links':[{'label':'Lab','url':'https://lab.example/','workspaces':[1]}],'tasks':[{'label':'Review <script>','state':'active','workspaces':[2]}],'builds':[{'label':'Check','state':'failed','workspaces':[2]}]}
    (Path(tmp)/'dashboard.json').write_text(json.dumps(value))
    first=w.surface(1);second=w.surface(2)
    assert first['label']=='Dash' and second['label']=='Development'
    assert first['links'] and not first['tasks']
    assert second['tasks'][0]['updated_at'] is None
    assert second['attention'][0]['label']=='Build failed: Check'
    for url in ['javascript:alert(1)','https://user:pass@lab.example/','https://lab.example/?token=secret']:
        try:w.safe_link({'label':'Bad','url':url})
        except ValueError:pass
        else:raise AssertionError(url)
    value['tasks'][0]['state']='invalid';(Path(tmp)/'dashboard.json').write_text(json.dumps(value))
    assert w.surface(4)['attention'][0]['state']=='unavailable'
assert 'escapeHtml(row.label)' in (ROOT/'start-page/app.js').read_text()
print('Workspace names, scoped feeds, freshness, invalid data, and link validation passed')
