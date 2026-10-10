#!/usr/bin/env python3
"""Exercise notification timing without waiting or sending real notifications."""
import contextlib, io, json, os, runpy, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as directory:
    base=Path(directory)
    os.environ["XDG_CONFIG_HOME"]=str(base/"config")
    os.environ["XDG_STATE_HOME"]=str(base/"state")
    config=base/"config/omarchy/thermal-alerts.json";config.parent.mkdir(parents=True)
    cfg={"warning_c":90,"critical_c":98,"warning_clear_c":85,"critical_clear_c":92,"warning_cooldown_seconds":3600,"critical_cooldown_seconds":900,"warning_sustained_seconds":120,"critical_sustained_seconds":60,"poll_seconds":30}
    config.write_text(json.dumps(cfg))
    with contextlib.redirect_stdout(io.StringIO()):module=runpy.run_path(str(ROOT/"bin/subcult-thermal-alert"))
    state=module["STATE"]
    def evaluate(temp,elapsed):
        output=io.StringIO()
        with contextlib.redirect_stdout(output):module["evaluate"](temp,dry=True,now=10000+elapsed,quiet=True)
        return output.getvalue().strip()
    def reset():state.unlink(missing_ok=True)

    # A single peak and a return below the threshold never notify.
    assert evaluate(100,0)=="" and evaluate(70,30)==""
    reset()
    for seconds in (0,30,60,90):assert evaluate(90,seconds)==""
    assert evaluate(90,120)=="notify=warning"
    assert evaluate(91,150)==""  # One notification during the same episode.
    reset()
    assert evaluate(98,0)=="" and evaluate(98,30)==""
    assert evaluate(98,60)=="notify=critical"
    assert evaluate(98,90)=="" and evaluate(95,120)==""  # No downgrade warning.

    # Falling below warning entry resets its timer even inside hysteresis.
    reset()
    for seconds in (0,30,60):assert evaluate(92,seconds)==""
    assert evaluate(89,90)=="" and evaluate(92,120)==""
    for seconds in (150,180,210):assert evaluate(92,seconds)==""
    assert evaluate(92,240)=="notify=warning"

    # Critical duration is independent of earlier warm readings.
    reset()
    for seconds in (0,30,60):assert evaluate(95,seconds)==""
    assert evaluate(99,90)==""
    assert evaluate(99,120)=="notify=warning"
    assert evaluate(99,150)=="notify=critical"

    # Missing samples, clock rollback, and policy changes restart timing.
    reset();evaluate(99,0)
    assert evaluate(99,100)=="" and evaluate(99,130)==""
    assert evaluate(99,160)=="notify=critical"
    reset();evaluate(99,60)
    assert evaluate(99,30)=="" and evaluate(99,60)==""
    assert evaluate(99,90)=="notify=critical"
    reset();evaluate(99,0)
    cfg["critical_c"]=99;config.write_text(json.dumps(cfg))
    assert evaluate(99,30)=="" and evaluate(99,60)==""
    assert evaluate(99,90)=="notify=critical"

    # A second sustained episode waits for the previous alert's cooldown.
    reset();evaluate(100,0);evaluate(100,30)
    assert evaluate(100,60)=="notify=critical"
    evaluate(70,90)
    for seconds in range(120,960,30):assert evaluate(100,seconds)==""
    assert evaluate(100,960)=="notify=critical"

    # Sensor loss and disabled monitoring clear pending durations.
    reset();evaluate(100,0)
    globals_=module["check"].__globals__;globals_["temperatures"]=lambda:(None,"unavailable")
    module["check"](quiet=True)
    assert "critical_since" not in json.loads(state.read_text())
    evaluate(100,30);module["DISABLED"].touch();module["check"](quiet=True)
    assert "critical_since" not in json.loads(state.read_text())

print("PASS sustained thermal alerts, spike rejection, hysteresis, cooldowns, gaps and reset behavior")
