"""Resolve the loopback port owned by the MAGI start page."""
import json
import os
from pathlib import Path

DEFAULT_PORT = 8765


def config_path():
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "omarchy/evangelion.json"


def valid(value):
    return isinstance(value, int) and not isinstance(value, bool) and 1024 <= value <= 65535


def port(path=None):
    """EVA_START_PAGE_PORT, then evangelion.json start_page_port, then 8765."""
    override = os.environ.get("EVA_START_PAGE_PORT", "")
    if override.isdigit() and valid(int(override)):
        return int(override)
    try:
        value = json.loads((path or config_path()).read_text()).get("start_page_port")
    except (OSError, json.JSONDecodeError, AttributeError):
        value = None
    return value if valid(value) else DEFAULT_PORT


def origin(number=None):
    return f"http://127.0.0.1:{number or port()}"
