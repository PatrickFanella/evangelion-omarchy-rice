#!/usr/bin/env python3
"""Regression coverage for desktop session detection without an exported instance."""
import importlib.util
import os
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("preflight", ROOT / "preflight.py")
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


def session_status(environment, monitor_data, activation=True):
    with patch.dict(os.environ, environment, clear=True), \
         patch.object(preflight, "monitors", return_value=monitor_data), \
         patch.object(preflight, "run", return_value=None):
        report = preflight.build_report(activation)
    return next(check for check in report["checks"] if check["name"] == "active-session")


desktop = {"XDG_SESSION_TYPE": "wayland", "XDG_CURRENT_DESKTOP": "Hyprland"}
monitor = [{"name": "eDP-1", "width": 3456, "height": 2160, "scale": 2}]
check = session_status(desktop, monitor)
assert check["status"] == "pass", check
assert "ipc=responsive" in check["detail"], check
assert session_status(desktop, [])["status"] == "blocker"
assert session_status(desktop | {"HYPRLAND_INSTANCE_SIGNATURE": "instance"}, [])["status"] == "pass"
assert session_status(desktop | {"XDG_SESSION_TYPE": "tty"}, monitor)["status"] == "blocker"
assert session_status(desktop | {"XDG_CURRENT_DESKTOP": "GNOME"}, monitor)["status"] == "blocker"
assert session_status({}, [], activation=False)["status"] == "pass"
print("PASS  preflight session detection with responsive IPC and no exported signature")
