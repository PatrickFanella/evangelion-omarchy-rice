# SUBCULT plugin distribution audit

This is the evolving audit of every directory under `omarchy/plugins/`, updated
for the v1.5 development baseline. The machine-readable evidence is
`plugin-audit.json`.

## Classification rules

- **Standalone** means isolated installation and runtime have already passed
  without any unbundled suite file. No current plugin meets that bar.
- **Optionally integrated** means the plugin has independent user value and is
  a plausible extraction target, but its current source still needs a declared
  helper, native API guard, or static fallback.
- **Suite-only** means its purpose or safety depends on coordinated suite
  state, services, configuration, or complete replacement behavior.
- **Compatibility-only** means it reskins/adapts another plugin or integration
  rather than providing a primary standalone product.

This classification is deliberately stricter than “the QML file loads on this
laptop.” Hard sibling imports, implicit first-party services, commands outside
the plugin directory, private state paths, and unversioned schemas all count as
dependencies.

## Inventory

| Plugin | Kind | Classification | Principal coupling / degradation gap |
|---|---|---|---|
| `subcult.agents` | bar | Compatibility-only | Icon adapter + upstream agents source |
| `subcult.intrusion` | service | Suite-only | Motion, intrusion state/command, Hyprland |
| `subcult.closed-door` | bar | Optionally integrated | Motion + `subcult-focus`; missing state looks inactive |
| `subcult.battery` | service | Suite-only | Cloned safety service + alert/profile commands |
| `subcult.bluetooth` | bar | Compatibility-only | Icon adapter + upstream Bluetooth source |
| `subcult.cava` | bar | Optionally integrated | Motion hard import; Cava absence already hides cleanly |
| `subcult.clipboard` | overlay | Suite-only | Security-sensitive cloned clipboard backend |
| `subcult.communications` | bar | Optionally integrated | Motion + SUBCULT aggregation command and IPC |
| `subcult.context` | bar | Suite-only | Context schema, policy, inspector, automation, profiles |
| `subcult.device-osd` | service | Suite-only | Suite monitor/event/IPC contract |
| `subcult.dropbox` | bar | Compatibility-only | Icon adapter + upstream Dropbox source |
| `subcult.health` | bar | Optionally integrated | Motion + SUBCULT health command; failure appears nominal |
| `subcult.icon-theme` | library/service | Compatibility-only | Component library for native widget adapters |
| `subcult.lock` | service | Suite-only | PAM/session-lock safety and suite motion/sound |
| `subcult.idle` | service | Suite-only | Coordinated idle/screensaver lifecycle |
| `subcult.media` | bar | Optionally integrated | Native `omarchy.media` API + motion hard import |
| `subcult.mission` | bar | Optionally integrated | Mission command/schema + motion |
| `subcult.mode-transition` | service | Suite-only | Coordinated modes, context, Hyprland, motion |
| `subcult.motion` | service/library | Suite-only | Current suite configuration and state paths |
| `subcult.notifications` | service | Suite-only | Full notification-daemon replacement + context/motion |
| `subcult.operating-profile` | service | Suite-only | Context automation and transactional profiles |
| `subcult.performance` | service | Suite-only | Aggregate collector, preserved opt-in state, privacy contract, motion |
| `subcult.power` | bar | Suite-only | Cloned native panel + broad Omarchy command API |
| `subcult.power-sequence` | service | Suite-only | UPower transition lifecycle + suite sound/IPC |
| `subcult.privacy` | bar | Optionally integrated | Safety helper/probes + motion; actions need separate review |
| `subcult.tailscale` | bar | Compatibility-only | Icon adapter + upstream Tailscale source |
| `subcult.thermal` | service | Suite-only | Shell half of suite monitor and alert policy |
| `subcult.update-operation` | service | Suite-only | Events exist only inside suite update wrapper |
| `subcult.workspace-osd` | service | Suite-only | Suite Hyprland event/state and workspace labels |
| `subcult.workspaces` | bar | Suite-only | Cloned native widget + suite labels/motion |
| `subcult.world-clock` | bar | Optionally integrated | Clock command/schema, motion, project-specific zone default |
| `neon.overdrive` | bar | Compatibility-only | External-theme compatibility; superseded by native Cava |

The automated contract verifies that all 34 tracked directories appear exactly once,
all non-orphan entries match their manifests and entry points, declared sibling
imports match the source, and no entry is mislabeled as verified standalone.

## Dependency findings

- Eighteen plugins hard-import `subcult.motion`; four icon wrappers
  hard-import `subcult.icon-theme`. QML import failure occurs before any
  graceful runtime fallback can render.
- Several widgets initialize a plausible nominal default and ignore a failed
  process. Missing commands can therefore look healthy instead of explicitly
  unavailable.
- The context, motion, mission, clock, privacy, health, focus, and presentation
  commands have no independently versioned protocol today.
- Native-service access such as `firstPartyServiceFor("omarchy.media")` and
  file-path composition through `OMARCHY_PATH` need declared Omarchy API ranges.
- Replacement plugins for lock, notifications, clipboard, battery, power, and
  workspaces carry more security or compatibility risk than marketplace value;
  they stay suite-only.
- The local-only empty `subcult.tray` directory discovered during the audit
  was removed. Git never tracked or published it, so it is not a distributable
  plugin and is intentionally absent from the inventory.

## First marketplace candidates

1. **`subcult.cava`** — visually distinctive, tiny surface, no SUBCULT command
   or private schema, and already collapses to zero width when optional Cava is
   unavailable. Extraction needs a local/static motion fallback, a portable
   path to its bundled `cava.conf`, and isolated present/absent tests.
2. **`subcult.media`** — broadly useful and delegates playback behavior to
   Omarchy's native media service rather than duplicating playerctl logic. It
   already hides when no player is active. Extraction needs a native-service
   capability/version guard and a local/static motion fallback.

Neither recommendation is a standalone-support claim. SO1-383 must now decide
whether the common motion surface warrants a tiny runtime, should be vendored,
or should be removed from marketplace plugins. SO1-385 must prove isolated
installation with runtime present, absent, stale, and incompatible before
either plugin is advertised as standalone.
