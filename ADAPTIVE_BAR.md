# Adaptive bar

Enable with `subcult-adaptive-bar enable`; disable restores normal widget
visibility without rewriting the bar layout. The feature is off by default.

Media and Cava appear for activity or workspace 7. The mission timer appears
during an active/paused mission or in Development and Journal. The world clock
appears during an elapsed mission or in Dash and Calendar. Open popups keep
their widgets visible. Missing media still follows its existing availability
rule. A hidden Cava widget stops its Cava process.

```bash
subcult-adaptive-bar status
subcult-adaptive-bar enable
subcult-adaptive-bar pin subcult.world-clock
subcult-adaptive-bar rule subcult.mission 2 4 9
subcult-adaptive-bar disable
```

Configuration is preserved in `~/.config/omarchy/adaptive-bar.json`.
Workspace, privacy, health, power and communications widgets are protected.
Native controls and third-party widgets are unmanaged and keep their normal
visibility. Pinning an optional widget overrides its adaptive rule, but cannot
make a missing capability available.

Decisions react to the compositor workspace and the existing widget state.
No process/window titles, polling daemon or new plugin service is added.
This works with stock and custom bars that honor widget visibility.
