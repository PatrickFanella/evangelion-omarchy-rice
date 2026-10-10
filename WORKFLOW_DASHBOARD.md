# Workspace-aware dashboard

The start page now reads workspace names from the same identity file as the bar.
Its Workspace tools card follows the active workspace, showing configured kit
tools and links. The Attention / Queue card combines network and thermal state
with a small local task/build feed. It does not launch desktop applications.

Edit `~/.config/omarchy/dashboard.json` to add links, tasks, and build summaries.
An empty `workspaces` list shows a row everywhere; otherwise use workspace IDs
1–10. An existing integration can atomically replace this file. No external
account, remote polling, project path, or arbitrary provider command is assumed.

```json
{
  "schema_version": 1,
  "links": [{"label":"Homelab","url":"https://your-dashboard.example/","workspaces":[1]}],
  "tasks": [{"label":"Review release","state":"active","updated_at":1791648000,"workspaces":[2]}],
  "builds": [{"label":"Rice validation","state":"passed","updated_at":1791648000,"workspaces":[2]}]
}
```

Task states: pending, active, done. Build states: pending, running, passed, failed,
unknown. Missing timestamps explicitly display as unknown, not live. Links must
be HTTP(S), without embedded credentials, query parameters, or fragments. The
dashboard never requests them until you click. Each collection is capped at 40
configured rows and eight displayed feed rows. Invalid configuration produces
an unavailable notice. Data stays on the existing loopback service.
