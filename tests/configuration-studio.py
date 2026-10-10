#!/usr/bin/env python3
import copy, json, sys, tempfile, importlib.machinery, importlib.util, threading, urllib.request, urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'lib'))
import subcult_studio as s
with tempfile.TemporaryDirectory() as tmp:
    s.d.CONFIG=Path(tmp)/'config';s.d.STATE=Path(tmp)/'state';s.RECEIPT=s.d.STATE/'studio-last.json';s.refresh=lambda:[]
    value=s.state()['preset'];value['workspaces'][3]['name']='Journal';value['workspaces'][0]['name']='Home';value['motion']='reduced'
    plan=s.preview(value);assert not s.d.STATE.exists() and not s.d.CONFIG.exists()
    try:s.apply(value,'old')
    except ValueError:pass
    else:raise AssertionError('stale plan accepted')
    assert s.apply(value,plan['plan_id'])['status']=='applied'
    assert s.state()['preset']['workspaces'][0]['name']=='Home'
    assert s.state()['preset']['motion']=='reduced'
    assert s.undo()['status']=='undone' and not (s.d.CONFIG/'shell.json').exists()
    bad=copy.deepcopy(value);bad['layout']['left'].remove('subcult.workspaces')
    try:s.preview(bad)
    except ValueError:pass
    else:raise AssertionError('required widget removed')
    assert s.apply(value,s.preview(value)['plan_id'])['status']=='applied'
    path=s.d.CONFIG/'workspaces.json';path.write_text(path.read_text()+' ')
    try:s.undo()
    except ValueError:pass
    else:raise AssertionError('newer edit overwritten')
    loader=importlib.machinery.SourceFileLoader('studio_server',str(ROOT/'bin/subcult-studio'));spec=importlib.util.spec_from_loader(loader.name,loader);server_module=importlib.util.module_from_spec(spec);loader.exec_module(server_module)
    server=server_module.ThreadingHTTPServer(('127.0.0.1',0),server_module.Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();url='http://127.0.0.1:'+str(server.server_port)
    def http(path,headers=None,data=None):
        req=urllib.request.Request(url+path,headers=headers or {},data=json.dumps(data).encode() if data else None)
        try:
            with urllib.request.urlopen(req,timeout=3) as response:return response.status,json.load(response)
        except urllib.error.HTTPError as error:return error.code,json.load(error)
    try:
        code,state=http('/api/state');assert code==200 and state['token']==server_module.TOKEN
        assert http('/api/state',{'Host':'evil.example'})[0]==403
        assert http('/api/preview',data={'preset':value})[0]==403
        headers={'Origin':url,'Content-Type':'application/json','X-Studio-Token':state['token']}
        assert http('/api/preview',headers,{'preset':value})[0]==200
        headers['Origin']='https://evil.example';assert http('/api/preview',headers,{'preset':value})[0]==403
    finally:server.shutdown();server.server_close();thread.join()
print('Studio draft, stale plans, transaction, guarded undo, and required indicators passed')
