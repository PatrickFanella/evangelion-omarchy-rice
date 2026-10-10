#!/usr/bin/env python3
import json,os,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as raw:
    env={**os.environ,"XDG_CONFIG_HOME":raw+"/config","XDG_STATE_HOME":raw+"/state"}
    cmd=[str(ROOT/"bin/subcult-workspace-kit")]
    def run(*args):return subprocess.run([*cmd,*args],env=env,text=True,capture_output=True)
    value=json.loads(run("list").stdout)
    assert [x["label"] for x in value["kits"]]==["Dash","Development","Browsing","Journal","Social Media","Mail","Media","Chat","Calendar","Misc"]
    before=list(Path(raw).rglob("*"));plan=json.loads(run("preview","2").stdout)
    assert before==list(Path(raw).rglob("*")) and plan["read_only"]
    assert run("launch","2","--confirm","stale").returncode!=0
    folder=Path(raw)/"config/omarchy";folder.mkdir(parents=True)
    value["kits"][1]["apps"]=[{"label":"Injection","argv":["missing-app","x; touch /tmp/NEVER"]}]
    (folder/"workspace-kits.json").write_text(json.dumps(value))
    assert not json.loads(run("preview","2").stdout)["actions"][0]["available"]
    commands=Path(raw)/"bin";commands.mkdir()
    fake=commands/"hyprctl"
    fake.write_text("#!/usr/bin/env python3\nimport json,os,sys\nif 'activeworkspace' in sys.argv: print('{\"id\":1}')\nelse:\n with open(os.environ['KIT_LOG'],'a') as f: f.write(json.dumps(sys.argv[1:])+'\\n')\n print('ok')\n")
    fake.chmod(0o755)
    env["PATH"]=str(commands)+os.pathsep+env["PATH"];env["KIT_LOG"]=str(Path(raw)/"launches")
    plan=json.loads(run("preview","3").stdout)
    assert run("launch","3","--confirm",plan["plan_id"]).returncode==0
    calls=[json.loads(x) for x in Path(env["KIT_LOG"]).read_text().splitlines()]
    assert calls[0]==["dispatch","workspace","3"] and all(x[0:2]==["dispatch","exec"] for x in calls[1:])
    value["kits"][0]["links"]=[{"label":"Bad","url":"https://name:secret@example.com"}]
    (folder/"workspace-kits.json").write_text(json.dumps(value))
    assert run("list").returncode!=0
print("PASS workspace kit preview, availability, confirmation and link validation")
