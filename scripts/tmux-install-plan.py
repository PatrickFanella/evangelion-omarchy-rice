#!/usr/bin/env python3
"""Read-only plan for adding the affinity theme to the user's tmux config."""
import os
from pathlib import Path
import shlex
import shutil


def source_paths(config):
    try:
        lines = config.read_text().splitlines()
    except (OSError, UnicodeError):
        return
    for line in lines:
        try:
            words = shlex.split(line, comments=True)
        except ValueError:
            continue
        if not words or words[0] not in ("source-file", "source"):
            continue
        for word in words[1:]:
            if word.startswith("-"):
                continue
            yield Path(os.path.expandvars(os.path.expanduser(word)))
            break


def includes_theme(config, theme, seen=None):
    seen = set() if seen is None else seen
    identity = config.resolve()
    if identity in seen or len(seen) >= 32:
        return False
    seen.add(identity)
    for source in source_paths(config):
        if not source.is_absolute():
            continue
        if source.resolve() == theme.resolve():
            return True
        if includes_theme(source, theme, seen):
            return True
    return False


def plan():
    home = Path.home()
    config_home = Path(os.environ.get("XDG_CONFIG_HOME") or home / ".config")
    legacy = home / ".tmux.conf"
    xdg = config_home / "tmux/tmux.conf"
    target = xdg if xdg.exists() else legacy if legacy.exists() else xdg
    # Back up the actual file, preserving a dotfile-manager symlink and its bytes.
    target = target.resolve()
    theme = Path(os.environ.get("SUBCULT_TMUX_THEME") or config_home / "tmux/themes/subcult.tmux.conf")
    if not shutil.which("tmux") and not target.exists():
        return "skip", target, ""
    if includes_theme(target, theme):
        action = "unchanged"
    else:
        action = "append" if target.exists() else "create"
    # Absolute paths also cover custom XDG roots and filenames containing spaces.
    line = "source-file -q " + shlex.quote(str(theme))
    return action, target, line


if __name__ == "__main__":
    print("\t".join(map(str, plan())))
