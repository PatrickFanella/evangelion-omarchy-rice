#!/usr/bin/env python3
"""Configurable loopback port contract for the MAGI start page."""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))
import magi_start_page as page

with tempfile.TemporaryDirectory() as directory:
    config = Path(directory) / "omarchy/evangelion.json"
    config.parent.mkdir()
    env = {"XDG_CONFIG_HOME": directory}
    with mock.patch.dict(os.environ, env, clear=False):
        os.environ.pop("EVA_START_PAGE_PORT", None)
        assert page.port() == 8765, "absent configuration must keep the historical port"
        config.write_text("{not json")
        assert page.port() == 8765
        for rejected in (80, 70000, "8766", True, None, 8765.5):
            config.write_text(json.dumps({"start_page_port": rejected}))
            assert page.port() == 8765, f"invalid port accepted: {rejected!r}"
        config.write_text(json.dumps({"start_page_port": 8766}))
        assert page.port() == 8766 and page.origin() == "http://127.0.0.1:8766"
        with mock.patch.dict(os.environ, {"EVA_START_PAGE_PORT": "9123"}):
            assert page.port() == 9123
        with mock.patch.dict(os.environ, {"EVA_START_PAGE_PORT": "22"}):
            assert page.port() == 8766, "invalid override must fall back to configuration"
        launcher = subprocess.run(["bash", ROOT / "bin/magi-start-page", "port"], text=True, capture_output=True,
                                  env={**os.environ, "EVA_START_PAGE_PORT": ""}, check=True)
        assert launcher.stdout.strip() == "8766", launcher.stdout

template = json.loads((ROOT / "omarchy/evangelion.json").read_text())
assert template["start_page_port"] == page.DEFAULT_PORT
server = (ROOT / "start-page/server.py").read_text()
assert '("127.0.0.1", PORT)' in server and "8765" not in server, "server must bind the resolved port"
assert "8765" not in (ROOT / "preflight.py").read_text(), "preflight must probe the resolved port"
print("PASS  start-page port configuration, validation, override, and fallback contracts")
