# Choose and maintain an installation channel

SUBCULT Rice has three supported ownership channels. Pick one before
installing; combining channels does not unlock additional features.

| Goal | Channel | What it installs | Best for |
|---|---|---|---|
| Just the look | Omarchy theme gallery/Git theme | Palette, app theme fragments, and seven wallpapers | Users who want native Omarchy theming without SUBCULT |
| Complete SUBCULT desktop | Tagged release archive | Theme, tools, shell, Hyprland integration, start page, and selected services | Most users who want the whole experience |
| Follow development | Git checkout | The same suite payload, from a mutable source checkout | Contributors and testers |
| Managed system package | Arch package | Immutable source under `/usr/share/subcult-rice`; user activation remains explicit | Arch users who want pacman ownership |

SUBCULT plugins are suite-internal components in v1.4. They are not standalone
marketplace products and must not be copied or advertised as independently
installable plugins. `SUBCULT_RUNTIME.md` defines a future architectural boundary,
not a published runtime package or supported fourth channel.

## Common prerequisites, capabilities, limitations, and support

All channels require an existing Omarchy installation. The complete suite
supports Omarchy `>=4.0.0,<5.0.0`, Hyprland `>=0.56.0,<0.57.0`, and x86_64.
Suite activation runs as the desktop user in an active Wayland/Hyprland session.
Run `./preflight.py --json` for capabilities and blockers; optional hardware,
SUBCULT context, Cava, media, weather, and sensor integrations degrade or hide when
unavailable. See `INSTALL.md` for packages and `README.md` for the tested matrix.

Support covers the published channel workflows and version ranges. Local edits,
third-party shell forks, unsupported Omarchy/Hyprland versions, vendor hardware
tools, and mixed ownership are best-effort. Bug reports should include preflight
and validation output, the selected channel/version, and redacted reproduction
steps—never private desktop state.

## Just the look: theme channel

Not published yet. `scripts/export-theme` builds the declarative theme payload
into `build/omarchy-subcult-theme/`, but no public repository carries it, so use
the complete suite for now. `PatrickFanella/omarchy-subcult-theme` is an older,
separate Subcult theme with a different palette, not this payload.

Once published, the channel installs with `omarchy theme install <repository>`
and updates through Omarchy's normal theme flow. To remove it, select another
theme first, then remove only the SUBCULT theme clone. This channel cannot
provide SUBCULT widgets, workspace identities, commands, motion, start page,
services, or affinity automation.

The theme and suite both own `~/.config/omarchy/themes/subcult`. The suite
installer refuses to merge into a Git-owned theme clone. Switch away and remove
the standalone clone before moving to the suite.

## Complete suite: tagged release archive

Download the archive and matching `.sha256` from the Gitea release, then:

```bash
sha256sum --check subcult-omarchy-rice-2.0.0.tar.gz.sha256
tar -xzf subcult-omarchy-rice-2.0.0.tar.gz
cd subcult-omarchy-rice-2.0.0
./scripts/build-release verify-root .
./preflight.py
./install.sh --dry-run --preset default
./install.sh --apply --preset default
omarchy theme set subcult
./validate.sh
```

Use `minimal`, `default`, `full`, or explicit components as documented in
`INSTALL.md`. Upgrade by downloading and verifying the new exact release, then
previewing and applying the same selection. Each apply records an exact snapshot:

```bash
./rollback.sh /path/printed/by/install
```

For removal, roll transactions back newest to oldest as described in
`UPGRADING.md`. There is deliberately no recursive uninstall command.

## Development checkout

```bash
git clone https://git.subcult.tv/PatrickFanella/subcult-omarchy-rice.git
cd subcult-omarchy-rice
git status --short
./preflight.py
./install.sh --dry-run --preset default
./install.sh --apply --preset default
```

Before updating, preserve local work and use `git pull --ff-only`. Preview and
apply the same component selection. Rollback/removal semantics are identical to
the release archive. A checkout tracks moving development source, so ordinary
users should prefer a tagged archive.

## Managed Arch package

After installing the package with pacman or an AUR helper, activate it explicitly
as the desktop user:

```bash
subcult-rice preflight
subcult-rice plan --preset default
subcult-rice apply --preset default
subcult-rice status
```

Pacman owns only immutable system files; it never mutates a home directory.
Use `subcult-rice rollback`, then remove the package through pacman when
leaving this channel. Full setup, upgrade, deactivation, and removal commands
are in `ARCH_PACKAGING.md`.

## Switching channels

Do not layer multiple owners over the same files. Theme → suite requires removing
the inactive Git theme clone. Git/archive → Arch requires rolling back user
activation before installing and explicitly activating the package. Arch →
Git/archive requires deactivation and package removal first. The tested matrix,
conflict behavior, and CI evidence are in `CROSS_CHANNEL.md`.
