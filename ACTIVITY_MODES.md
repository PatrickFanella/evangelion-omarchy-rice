# Coordinated activity modes

Work, Focus, Gaming, Presentation, Travel, and Quiet modes coordinate the
notification gate, motion, SUBCULT sound authority, power profile, displays,
optional widgets, and decorative context policy. They are explicitly manual:
the suite never infers an activity or applies one from ambient/context data.

Every shipped action starts opted out. Inspect the recommendation, enable only
the actions you want, inspect the resulting exact plan, then confirm that plan:

```bash
subcult-activity-mode preview focus | jq
subcult-activity-mode enable focus notifications
subcult-activity-mode enable focus motion
subcult-activity-mode enable focus widgets
plan=$(subcult-activity-mode preview focus)
subcult-activity-mode apply focus --confirm "$(jq -r .plan_id <<<"$plan")"
subcult-activity-mode undo
```

`enable MODE all` is an explicit shortcut; `disable MODE ACTION` removes one
authority. Use `target MODE ACTION VALUE` to customize a recommended target.
Display actions accept `keep` or `profile:NAME`, where NAME is an already saved
`subcult-topology` profile.

The preview reports every action as Apply or Skip, including why unsupported
hardware or providers will be skipped. Unsupported capabilities never make the
whole mode fail. Once mutation starts, any failure restores notification state,
power, display topology, shell layout, sound, motion, and context configuration
from a private transaction. Safety widgets are never hidden by Calm mode.

Configuration is preserved at `~/.config/omarchy/activity-modes.json`; the
private undo transaction is under
`~/.local/state/subcult-rice/activity-mode/last-transaction`.
