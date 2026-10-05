#!/usr/bin/env python3
import json, os, stat, subprocess, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BIN=ROOT/"bin/subcult-settings"

with tempfile.TemporaryDirectory() as raw:
    tmp=Path(raw); home=tmp/"home"; commands=tmp/"bin"; commands.mkdir(); (home/".config/omarchy").mkdir(parents=True)
    shell=home/".config/omarchy/shell.json"; shell.write_text(json.dumps({"bar":{"position":"top","layout":{"left":[{"id":"subcult.workspaces"},{"id":"subcult.media"}]}}})); shell.chmod(0o640)
    config=home/".config/omarchy/subcult.json"; config.write_text(json.dumps({"ambient":{"enabled":True}}))
    command='''#!/bin/sh
case "$1" in
 status) case "$(basename "$0")" in subcult-affinity) printf 'mode=auto\\nactive=violet\\n';; subcult-operating-profile) printf 'mode=auto\\n';; subcult-theme-variant) printf '{"active":"standard"}\\n';; *) printf 'full\\n';; esac;;
 create) mkdir -p "$SUBCULT_SETTINGS_STATE/fake"; cp "$SUBCULT_SETTINGS_SHELL" "$SUBCULT_SETTINGS_STATE/fake/shell.json";;
 diff) printf '{"plan_id":"restore-plan"}\\n';;
 restore) cp "$SUBCULT_SETTINGS_STATE/fake/shell.json" "$SUBCULT_SETTINGS_SHELL";;
esac
exit 0
'''
    for name in ("subcult-affinity","subcult-theme-variant","subcult-motion","subcult-operating-profile","subcult-ambient","subcult-sound","subcult-snapshot","subcult-visual","omarchy-shell","playerctl"):
        path=commands/name; path.write_text(command); path.chmod(0o755)
    env={**os.environ,"PATH":str(commands)+":"+os.environ["PATH"],"SUBCULT_SETTINGS_HOME":str(home),"SUBCULT_SETTINGS_DATA":str(ROOT),"SUBCULT_SETTINGS_SCHEMA":str(ROOT/"omarchy/settings-schema.json"),"SUBCULT_SETTINGS_SHELL":str(shell),"SUBCULT_SETTINGS_CONFIG":str(config),"SUBCULT_SETTINGS_STATE":str(home/"state"),"SUBCULT_SETTINGS_SKIP_ACTIVATE":"1"}
    def call(*args,ok=True):
        result=subprocess.run([str(BIN),*args],env=env,text=True,capture_output=True)
        if ok: assert result.returncode==0,result.stderr
        return result
    status_value=json.loads(call("status").stdout)
    assert len(status_value["settings"])==19 and len(status_value["categories"])==10
    privacy=next(x for x in status_value["settings"] if x["id"]=="privacy.indicator")
    assert privacy["read_only"] and privacy["value"]=="always-on"
    before=shell.read_bytes(); plan=json.loads(call("preview","display.bar-position","bottom").stdout)
    assert shell.read_bytes()==before and plan["before"]=="top" and plan["after"]=="bottom"
    assert call("apply","display.bar-position","bottom","--confirm","wrong",ok=False).returncode!=0
    assert shell.read_bytes()==before
    applied=json.loads(call("apply","display.bar-position","bottom","--confirm",plan["plan_id"]).stdout)
    assert json.loads(shell.read_text())["bar"]["position"]=="bottom" and applied["undo_available"]
    assert stat.S_IMODE(shell.stat().st_mode)==0o640 and stat.S_IMODE((home/"state/last.json").stat().st_mode)==0o600
    undone=json.loads(call("undo").stdout)
    assert shell.read_bytes()==before and undone["restored"]=="top"
    assert call("preview","privacy.indicator","always-on",ok=False).returncode!=0
    assert call("preview","unknown.setting","x",ok=False).returncode!=0

qml=(ROOT/"omarchy/plugins/subcult.settings/Service.qml").read_text()
for phrase in ("WlrKeyboardFocus.Exclusive","subcult-settings", "Key_Up", "Key_Left", "Key_Return", "Key_A", "Key_U", "Key_Escape", "Motion.MotionState", "Localization.I18n"):
    assert phrase in qml
shell_config=json.loads((ROOT/"omarchy/shell.json").read_text())
assert any(x["id"]=="subcult.settings" for x in shell_config["plugins"])
assert "SUPER + CTRL + ALT + S" in (ROOT/"hypr/bindings.lua").read_text()
assert 'record.get("setting")=="theme.variant"' in BIN.read_text()
print("PASS  schema-backed control center preview confirmation capability safety and exact undo")
