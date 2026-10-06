#!/usr/bin/env python3
"""The tmux fragment follows the applied affinity palette and never blocks it."""
import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = json.loads((ROOT / "omarchy/theme-variants.json").read_text())


def stub(directory, name, body):
    path = directory / name
    path.write_text("#!/bin/sh\n" + body + "\n")
    path.chmod(0o755)


with tempfile.TemporaryDirectory() as directory:
    base = Path(directory)
    fake, state, config = base / "bin", base / "state", base / "config"
    fake.mkdir()
    (state / "omarchy/current/theme").mkdir(parents=True)
    log = base / "tmux.log"
    for name in ("subcult-terminal-profile", "subcult-bar-refresh", "omarchy-shell",
                 "omarchy-notification-send", "subcult-motion"):
        stub(fake, name, "exit 0")
    stub(fake, "tmux", f'printf "%s\\n" "$*" >> "{log}"; exit 0')
    target = config / "tmux/themes/subcult.tmux.conf"
    env = {**os.environ, "HOME": str(base / "home"), "XDG_STATE_HOME": str(state),
           "XDG_CONFIG_HOME": str(config), "PATH": f"{fake}:{os.environ['PATH']}",
           "SUBCULT_VARIANT_REGISTRY": str(ROOT / "omarchy/theme-variants.json")}
    for inherited in ("HYPRLAND_INSTANCE_SIGNATURE", "SUBCULT_SKIP_ACTIVATE", "SUBCULT_TMUX_THEME"):
        env.pop(inherited, None)

    def apply(profile, **extra):
        return subprocess.run([str(ROOT / "bin/subcult-affinity"), "set", profile],
                              env={**env, **extra}, text=True, capture_output=True)

    for profile, row in REGISTRY["affinities"].items():
        assert apply(profile).returncode == 0, profile
        fragment = target.read_text()
        assert f"active {row['label']} palette" in fragment, profile
        assert f'#[fg=#{row["dark"]},bg=#{row["accent"]},bold] #S' in fragment, profile
        assert f'#[fg=#{row["dark"]},bg=#{row["accent2"]},bold] #h ' in fragment, profile
        assert f'"fg=#{row["muted"]}"' in fragment, profile
        assert f'mode-style "bg=#{row["accent"]},fg=#{row["dark"]}"' in fragment, profile
        assert '%H:%M' in fragment and '' in fragment and '' in fragment, profile
        assert 'status-left-length 80' in fragment and 'status-right-length 120' in fragment, profile
        assert "{{" not in fragment and "$" not in fragment, profile
    assert log.read_text().count(f"source-file -- {target}") == len(REGISTRY["affinities"])

    # A failed palette apply leaves the previous fragment in place.
    before = target.read_text()
    stub(fake, "subcult-terminal-profile", "exit 1")
    assert apply("acid").returncode == 1
    assert target.read_text() == before

    # Activation-free installs write the fragment without touching a tmux server.
    stub(fake, "subcult-terminal-profile", "exit 0")
    log.unlink()
    assert apply("paper", SUBCULT_SKIP_ACTIVATE="1").returncode == 0
    assert "PAPER STOCK" in target.read_text() and not log.exists()

print("PASS  tmux fragment follows every affinity palette, rollback, and skip-activate")
