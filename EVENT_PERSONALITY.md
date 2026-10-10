# Event cues and session summaries

Event cues start disabled. Enable with `subcult-personality enable`, then preview
the decision with `subcult-personality preview mission-complete`. Cues respond
to workspace kits, recipes, completed missions, and journal session boundaries.
They reuse the existing short mode-transition card and its Full / Reduced / Off
motion behavior. There is no ambient loop, repeated animation, or polling daemon.

Quiet hours default to 22:00–07:00. Focus mode suppresses these optional cues.
A global 30-second cooldown prevents cue bursts. Configure those choices in
`~/.config/omarchy/personality.json`. `disable` stops future cues.

Sound starts off. `subcult-personality sound on` only requests the existing
workflow cue; it does not enable the global sound switch or a sound category,
change quiet hours, change volume, or use the preview command that bypasses
normal audio authority. A cue can therefore remain silent after this setting.
Missing visual/audio providers are reported instead of starting a new service.

```sh
subcult-personality status
subcult-personality preview recipe-applied
subcult-personality enable
subcult-personality sound off
subcult-personality disable
subcult-personality session-summary
```

The dashboard's Session summary button reads the journal summary on demand.
Start and end a session with `subcult-journal session start` and `session end`
after enabling journal recording. Summaries report duration and counts of retained
events, capped at 100 event groups. They do not claim application usage time or
productivity. Deduplicated event counts can span a session boundary, which the
summary reports explicitly. No new tracking system or browser data collection
is introduced.
