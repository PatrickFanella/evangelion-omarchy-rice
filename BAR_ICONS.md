# Bar icon unification

The SUBCULT bar keeps Omarchy's upstream implementations behind transparent
adapters. The adapter loads from `$OMARCHY_PATH`, forwards
the bar and settings objects, and delegates `open`, `close`, and `toggle` to the
native widget. This retains upstream click bindings, panels, tooltips, IPC, and
live status behavior without copying vendor code into this repository.

| Surface | Installed ID | Native implementation | Treatment |
| --- | --- | --- | --- |
| Agents | `subcult.agents` | `omarchy.agents` | Tinted native agent glyph and panel |
| Bluetooth | `subcult.bluetooth` | `omarchy.bluetooth` | Tinted native radio states and panel |
| Dropbox | `subcult.dropbox` | `omarchy.dropbox` | Tinted recognizable vendor mark |
| Tailscale | `subcult.tailscale` | `omarchy.tailscale` | Tinted recognizable vendor mark |
| StatusNotifier tray | `omarchy.tray` | Omarchy tray | Symbolic icons inherit bar foreground; full-color vendor artwork is preserved |

The resting bar foreground is SUBCULT lavender `#B9A8E6`, shared by native
widget glyphs and symbolic StatusNotifier icons. There are no per-widget frames
or decorative halos. Native widgets remain responsible for active, disabled,
warning, and urgent colors, while green, amber, and red stay reserved for real
state changes. The stock tray deliberately leaves full-color StatusNotifier
artwork intact, so it stays upstream rather than being forked or recolored.

Wallpaper affinity replaces the resting token without changing those semantic
rules:

| Affinity | Resting bar/icon token |
| --- | --- |
| SUBCULT / PRESS (neutral) | lavender `#B9A8E6` |
| Acid Block | soft acid green `#7FE8B5` |
| Paper Stock | warm paper `#D9D1C2` |
| Violet Field | pale violet `#C4B5FD` |
| Ink Run | muted lavender-grey `#A9A3BC` |

Each token has at least 4.5:1 contrast against its generated bar background.
`subcult-affinity palette [PROFILE]` reports the resolved colors as JSON. Auto and
manual affinity modes use the same table, so changing a wallpaper cannot reset
the bar to the general near-white panel foreground.

Successful affinity transactions immediately push the generated palette into
the running shell with `subcult-bar-refresh`; no process restart is involved. The
command is idempotent and is also available in the Field Affinity menu for
manual recovery. A failed IPC attempt records an actionable status while
leaving the correct on-disk palette ready for a later retry.

## Compatibility and fallback

The adapters require the corresponding first-party Omarchy plugin beneath
`$OMARCHY_PATH/shell/plugins`. Run `./preflight.py` before installation after a
major Omarchy upgrade. If an upstream widget moves or changes incompatibly,
replace its `subcult.*` ID in `~/.config/omarchy/shell.json` with the native
ID shown above and restart the shell. This is a per-widget fallback; the rest of
the theme remains active.

Because all source lookup is based on `$OMARCHY_PATH`, no username, home path,
screen name, or machine-specific path is embedded in the adapters.
