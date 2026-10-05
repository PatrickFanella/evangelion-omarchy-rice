# Monitor topology profiles

SUBCULT can remember local display arrangements without changing the default
desktop behavior. Profiles remain disabled until explicitly enabled, and their
configuration stays private under `~/.config/omarchy/topologies.json`.

## Save and preview

Arrange displays and workspaces normally, then save the current topology:

```bash
subcult-topology save home-dock
subcult-topology status
subcult-topology preview home-dock
```

The identity uses connector names, display model descriptions, dimensions, and
internal/external classification. It deliberately excludes EDIDs, serials,
device IDs, host paths, window titles, and application content. SUBCULT labels a
shape as `laptop`, `dock`, `projector`, `ultrawide`, `multi-monitor`, or
`unknown`.

Preview is read-only and returns an exact plan ID. A manual apply requires that
ID, so a display change between preview and confirmation cannot silently apply
a stale plan:

```bash
subcult-topology apply home-dock --confirm PLAN_ID
subcult-topology undo
```

Apply records the prior monitor and window/workspace arrangement first. Undo
restores it. SUBCULT moves existing workspaces and windows; it never closes,
relaunches, or rewrites application data. A failed apply attempts the same
rollback automatically.

## Hot-plug restoration

```bash
subcult-topology enable
subcult-topology disable
```

When enabled, the user service listens to Hyprland monitor events and waits
1.5 seconds after the last event before acting. Rapid dock changes therefore
collapse into one evaluation. A known identity restores its saved layout. An
unknown identity is a safe no-op, leaving Hyprland's current arrangement
untouched. The debounce can be set from 250–10000 ms in `topologies.json`.

If the service is unavailable, profiles remain usable manually. Inspect it with
`systemctl --user status subcult-topology.service`.
