#!/usr/bin/env python3
import importlib.machinery, importlib.util, json, os, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
loader=importlib.machinery.SourceFileLoader('heat',str(ROOT/'bin/subcult-heat'));spec=importlib.util.spec_from_loader(loader.name,loader);heat=importlib.util.module_from_spec(spec);loader.exec_module(heat)
rows=heat.contributors({('7','10'):('browser',100),('8','10'):('browser',20),('9','1'):('old',200)},{('7','10'):('browser',300),('8','10'):('browser',120),('9','2'):('new',9999)},2,100)
assert rows==[{'name':'browser','cpu_percent':150.0}],rows
with tempfile.TemporaryDirectory() as tmp:
    env={**os.environ,'XDG_CONFIG_HOME':tmp+'/config','XDG_STATE_HOME':tmp+'/state','SUBCULT_PROC_ROOT':tmp+'/proc','SUBCULT_SYS_ROOT':tmp+'/sys'}
    def run(*args):return subprocess.run([str(ROOT/'bin/subcult-heat'),*args],env=env,text=True,capture_output=True)
    assert json.loads(run('status').stdout)['sample_count']==0
    assert not Path(tmp+'/state').exists()
    assert run('sample','--seconds','.1').returncode!=0
    assert run('enable').returncode==0
    assert run('sample','--seconds','.1').returncode==0
    path=Path(tmp+'/state/subcult-rice/heat-history.json');assert path.stat().st_mode&0o777==0o600
    assert json.loads(path.read_text())[0]['temperature_c'] is None
    assert run('disable').returncode==0
    assert run('sample').returncode!=0
    assert run('clear').returncode==0 and not path.exists()
print('Heat grouping, PID reuse, opt-in collection, missing sensors, and deletion passed')
