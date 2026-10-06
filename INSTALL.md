# Installation guide

## Prerequisites

SUBCULT Rice customizes an existing Omarchy installation; it does not install
Arch Linux, Omarchy, Hyprland, or a graphical session. Activation must run as
the desktop user inside a supported Wayland/Hyprland session.

Required tools are normally part of Omarchy:

```bash
omarchy pkg add bash python jq lua coreutils
```

Recommended for the reference experience:

```bash
omarchy pkg add xdg-terminal-exec fastfetch btop
omarchy pkg add ghostty  # or alacritty, foot, kitty
```

Full optional integration set:

```bash
omarchy pkg add neovim cava playerctl wireplumber pulseaudio-utils \
  wl-clipboard xdg-utils procps-ng networkmanager tailscale \
  power-profiles-daemon lm_sensors brightnessctl socat bat util-linux \
  uwsm libnotify git
```

Optional packages are feature-scoped. `dependencies.tsv` is the canonical
inventory; `./check-dependencies.sh` prints only what this machine lacks.

## Preflight and preview

```bash
./preflight.py
./preflight.py --json
./check-dependencies.sh
./install.sh --dry-run --preset default
```

Preflight reads versions, session state, dependencies, writable targets, free
space, conflicting services, port 8765, hotkeys, displays, applications,
batteries, sensors, audio, and networking. It performs no writes.

If `~/.config/omarchy/themes/subcult` is a Git-installed standalone theme,
the suite installer exits read-only with `CHANNEL CONFLICT`. Switch to another
theme and remove that clone before retrying; the installer never merges suite
files into another channel's Git tree.

## Presets and components

```bash
./install.sh --apply --preset minimal
./install.sh --apply --preset default
./install.sh --apply --preset full
./install.sh --apply --components theme,tools,shell
./install.sh --list-components
```

| Component | Target | Update policy |
|---|---|---|
| `theme` | `~/.config/omarchy/themes/subcult/` | Individual files created/replaced |
| `tools` | Named `subcult-*` commands in `~/.local/bin/` | Created/replaced |
| `shell` | Omarchy plugins, menu, hooks, JSON config | Complete configs replaced; `subcult.json` preserved |
| `hypr` | `~/.config/hypr/{bindings,hyprland,looknfeel}.lua` | Complete files replaced |
| `start-page` | `~/.local/share/subcult-rice/start-page/` | Created/replaced |
| `services` | `~/.config/systemd/user/subcult-*` | Named units replaced and enabled |
| `extras` | Fastfetch and Neovim user config | Named files replaced |
| `shell-integration` | Shell startup file plus Omarchy scripts | One source stanza appended; scripts replaced |
| `neon-overdrive` | Optional compatibility plugin | Requires detected external integration |

The installer does not merge Lua or `shell.json`; they are complete
replacements shown in the plan. It does not remove unrelated target-directory
files. Use `--shell bash|zsh|fish` to override detection or
`--no-shell-integration` to avoid startup-file edits.

The `tools` component also appends the SUBCULT tmux theme source line when tmux
is installed or a user tmux configuration exists. Existing configuration is
preserved, repeat installs avoid duplicate source lines, and rollback restores
the prior file. Use `--no-tmux-integration` to skip this edit.

## Transactions and backups

All preflight checks finish before mutation. Every changed target is copied to
a unique snapshot and recorded in `manifest.tsv`; new targets are recorded for
removal. Copy, activation, or validation errors automatically invoke rollback.

```text
~/.local/state/subcult-rice/install-backups/<timestamp>-<pid>/
├── manifest.tsv
├── files/
└── legacy-plugins/
```

Repeated installs skip byte-identical files. Use `--yes` only after reviewing
the dry-run from the same checkout.

## First-run verification

```bash
omarchy theme set subcult
omarchy restart shell
./validate.sh
subcult-capabilities | jq .
systemctl --user --no-pager status subcult-affinity.path subcult-start-page.service
subcult-start-page open
```

Cycle the wallpaper with `omarchy theme bg next` and open the SUBCULT menu with
`Super + M`. Missing optional widgets should
collapse rather than leave errors or empty blocks.
