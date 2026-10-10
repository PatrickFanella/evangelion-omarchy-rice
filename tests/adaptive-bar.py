#!/usr/bin/env python3
import json,os,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as raw:
    env={**os.environ,"XDG_CONFIG_HOME":raw+"/config"}
    def run(*args):return subprocess.run([str(ROOT/"bin/subcult-adaptive-bar"),*args],env=env,text=True,capture_output=True)
    assert json.loads(run("status").stdout)["enabled"] is False
    assert json.loads(run("enable").stdout)["enabled"] is True
    assert run("unpin","subcult.privacy").returncode!=0
    assert run("rule","subcult.media","11").returncode!=0
    assert run("pin","subcult.world-clock").returncode==0
    assert json.loads(run("disable").stdout)["enabled"] is False
for name in ("media","cava","mission","world-clock"):
    assert "AdaptiveVisibility" in (ROOT/f"omarchy/plugins/subcult.{name}/BarWidget.qml").read_text()
print("PASS adaptive bar configuration, protected indicators and widget integration")
