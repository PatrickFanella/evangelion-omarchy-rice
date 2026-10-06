#!/usr/bin/env python3
"""Exercise tmux config edits through the installer and rollback transaction."""
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("tmux_plan", ROOT / "scripts/tmux-install-plan.py")
planner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(planner)

with tempfile.TemporaryDirectory() as temporary:
    base = Path(temporary)
    suite, home, state = base / "suite", base / "home", base / "state"
    suite.mkdir()
    home.mkdir()
    for name in ("install.sh", "rollback.sh", "VERSION", "dependencies.tsv"):
        shutil.copy2(ROOT / name, suite / name)
    for name in ("bin", "lib", "recovery", "migrations", "omarchy", "shell"):
        shutil.copytree(ROOT / name, suite / name, ignore=shutil.ignore_patterns("__pycache__"))
    (suite / "scripts").mkdir()
    shutil.copy2(ROOT / "scripts/tmux-install-plan.py", suite / "scripts/tmux-install-plan.py")
    # Isolate config transactions from desktop activation and the full source gate.
    for name in ("preflight.py", "validate.sh"):
        path = suite / name
        path.write_text("#!/bin/sh\nexit 0\n")
        path.chmod(0o755)
    env = {**os.environ, "HOME": str(home), "XDG_CONFIG_HOME": str(home / ".config"),
           "XDG_STATE_HOME": str(state), "SUBCULT_SKIP_ACTIVATE": "1"}
    env.pop("SUBCULT_TMUX_THEME", None)

    def install(*args, failure=False):
        result = subprocess.run([str(suite / "install.sh"), *args], env=env |
                                {"SUBCULT_FORCE_INSTALL_FAILURE": "1" if failure else "0"},
                                text=True, capture_output=True)
        assert result.returncode == (1 if failure else 0), result.stderr
        return result.stdout

    def rollback():
        subprocess.run([str(suite / "rollback.sh")], env=env, check=True, capture_output=True)

    def snapshot():
        return Path((state / "subcult-rice/last-install-backup").read_text().strip())

    config = home / ".config/tmux/tmux.conf"
    theme = home / ".config/tmux/themes/subcult.tmux.conf"
    with patch.dict(os.environ, env, clear=True), patch.object(planner.shutil, "which", return_value=None):
        assert planner.plan()[0] == "skip"
    # Simulate tmux availability without involving the user's running server.
    commands = base / "commands"
    commands.mkdir()
    (commands / "tmux").write_text("#!/bin/sh\nexit 0\n")
    (commands / "tmux").chmod(0o755)
    env["PATH"] = str(commands) + ":" + env["PATH"]
    assert "CREATE    tmux-integration" in install("--dry-run", "--components", "tools")
    assert not config.exists() and not state.exists()
    install("--apply", "--components", "tools", "--yes", failure=True)
    assert not config.exists(), "failed transaction left a new tmux config"
    install("--apply", "--components", "tools", "--yes")
    assert config.read_text().count("source-file -q " + str(theme)) == 1
    first = snapshot()
    install("--apply", "--components", "tools", "--yes")
    assert config.read_text().count(str(theme)) == 1
    assert str(config) not in (snapshot() / "manifest.tsv").read_text()
    subprocess.run([str(suite / "rollback.sh"), str(first)], env=env, check=True, capture_output=True)
    assert not config.exists(), "rollback retained a created tmux config"

    original = "set -g status-position top\nsource-file ~/old-theme.conf\n"
    config.write_text(original)
    install("--apply", "--components", "tools", "--yes", failure=True)
    assert config.read_text() == original, "failure did not restore existing config"
    install("--apply", "--components", "tools", "--yes", "--no-tmux-integration")
    assert config.read_text() == original
    install("--apply", "--components", "shell-integration", "--yes")
    assert config.read_text() == original, "unselected tools edited tmux"
    install("--apply", "--components", "tools", "--yes")
    assert config.read_text().startswith(original) and config.read_text().rstrip().endswith(str(theme))
    rollback()
    assert config.read_text() == original

    local = config.parent / "tmux.local.conf"
    local.write_text('source-file "' + str(theme) + '"\n')
    config.write_text('source-file "$HOME/.config/tmux/tmux.local.conf"\n')
    assert "UNCHANGED tmux-integration" in install("--dry-run", "--components", "tools")
    before = config.read_bytes()
    install("--apply", "--components", "tools", "--yes")
    assert config.read_bytes() == before
    local.write_text('# source-file "' + str(theme) + '"\n')
    assert "APPEND    tmux-integration" in install("--dry-run", "--components", "tools")
    local.write_text('source-file "$HOME/.config/tmux/tmux.conf"\n')
    assert "APPEND    tmux-integration" in install("--dry-run", "--components", "tools"), "include cycle failed"

    config.unlink()
    legacy = home / ".tmux.conf"
    legacy.write_text(original)
    install("--apply", "--components", "tools", "--yes")
    assert str(theme) in legacy.read_text() and not config.exists()
    rollback()
    assert legacy.read_text() == original
    legacy.unlink()
    real = home / "managed-tmux.conf"
    real.write_text(original)
    config.symlink_to(real)
    install("--apply", "--components", "tools", "--yes")
    rollback()
    assert config.is_symlink() and real.read_text() == original

    config.unlink()
    custom = home / "custom config/tmux/tmux.conf"
    custom.parent.mkdir(parents=True)
    custom.write_text(original)
    env["XDG_CONFIG_HOME"] = str(home / "custom config")
    install("--apply", "--components", "tools", "--yes")
    assert "source-file -q '" in custom.read_text()
    rollback()
    assert custom.read_text() == original

print("PASS  tmux source installation, dry run, opt-out, repeat install, includes, XDG, symlinks, and rollback")
