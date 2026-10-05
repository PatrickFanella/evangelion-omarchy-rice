#!/usr/bin/env python3
"""Manual authority, per-action opt-in, fallback, and atomic undo tests."""
import json,os,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CLI=ROOT/"bin/subcult-activity-mode";DEFAULT=ROOT/"omarchy/activity-modes.json"
with tempfile.TemporaryDirectory() as raw:
 base=Path(raw);fake=base/"bin";fake.mkdir();config=base/"activity.json";state=base/"state";shell=base/"shell.json";core=base/"core.json";sound=base/"sound.json";motion=base/"motion.json";log=base/"log"
 shell.write_text(json.dumps({"bar":{"layout":{"left":[{"id":"subcult.workspaces"},{"id":"subcult.media"},{"id":"subcult.cava"}],"center":[],"right":[{"id":"subcult.world-clock"},{"id":"subcult.privacy"}]}}}));before=shell.read_bytes()
 for path in (core,sound,motion):path.write_text('{"baseline":true}\n')
 stub='''#!/bin/sh
name=$(basename "$0")
case "$name:$1:$2" in
 "omarchy-shell:notifications:dndState") echo off;;
 "omarchy-shell:notifications:setDnd") echo "$3";;
 "powerprofilesctl:get:") echo balanced;;
 "powerprofilesctl:list:") echo '* balanced:';;
 "subcult-context:decorative:disable") [ "${SUBCULT_ACTIVITY_FAIL_CONTEXT:-0}" != 1 ] || exit 1;;
esac
printf '%s\\n' "$name $*" >> "$SUBCULT_ACTIVITY_TEST_LOG"
'''
 for name in ("omarchy-shell","subcult-motion","subcult-sound","powerprofilesctl","subcult-context","subcult-topology"):
  path=fake/name;path.write_text(stub);path.chmod(0o755)
 env={**os.environ,"PATH":str(fake)+os.pathsep+os.environ.get("PATH",""),"SUBCULT_ACTIVITY_DEFAULT":str(DEFAULT),"SUBCULT_ACTIVITY_CONFIG":str(config),"SUBCULT_ACTIVITY_STATE":str(state),"SUBCULT_ACTIVITY_SHELL":str(shell),"SUBCULT_ACTIVITY_CORE":str(core),"SUBCULT_ACTIVITY_SOUND":str(sound),"SUBCULT_ACTIVITY_MOTION":str(motion),"SUBCULT_ACTIVITY_TEST_LOG":str(log)}
 def run(*args,ok=True,extra=None):
  value=subprocess.run([str(CLI),*args],env={**env,**(extra or {})},text=True,capture_output=True)
  if ok:assert value.returncode==0,value.stderr
  return value
 initial=json.loads(run("preview","gaming").stdout);assert initial["authority"]=="manual-confirmed" and initial["will_apply"]==0
 enabled=json.loads(run("enable","gaming","all").stdout);assert enabled["unsupported"]==1 and enabled["will_apply"]==5
 assert run("apply","gaming","--confirm","wrong",ok=False).returncode!=0 and shell.read_bytes()==before
 applied=json.loads(run("apply","gaming","--confirm",enabled["plan_id"]).stdout);assert applied["actions"]==["notifications","motion","audio","widgets","context"] and applied["undo_available"]
 ids=[x["id"] for rows in json.loads(shell.read_text())["bar"]["layout"].values() for x in rows];assert "subcult.privacy" in ids and not ({"subcult.media","subcult.cava","subcult.world-clock"}&set(ids))
 run("undo");assert shell.read_bytes()==before and not (state/"last-transaction/state.json").exists()
 quiet=json.loads(run("enable","quiet","all").stdout);failed=run("apply","quiet","--confirm",quiet["plan_id"],ok=False,extra={"SUBCULT_ACTIVITY_FAIL_CONTEXT":"1"});assert "previous state restored" in failed.stderr and shell.read_bytes()==before
 assert config.stat().st_mode & 0o777==0o600
 source=CLI.read_text();assert 'automatic":False' in source and "Confirmation mismatch" in source and "unsupported" in source
print("PASS  manual activity modes per-action opt-in transparent plans capability fallback atomic rollback and undo")
