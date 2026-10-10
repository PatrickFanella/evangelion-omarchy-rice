# Workspace kits

The ten default workspaces are Dash, Development, Browsing, Journal, Social
Media, Mail, Media, Chat, Calendar, and Misc. Icons remain the default bar
display. Workspace names are still editable independently of launch kits.

Open **Workspace kits** from the command palette. Select a workspace, inspect
the plan, and type LAUNCH. The CLI provides the same preview and confirmation:

```bash
subcult-workspace-kit list
subcult-workspace-kit preview 2
subcult-workspace-kit launch 2 --confirm PLAN_ID
```

Configure `~/.config/omarchy/workspace-kits.json`. Each kit has an ID, label,
directory, terminal profile, application argument arrays, and named HTTP(S)
links. Development starts T3 Code and the default browser. Social Media uses
Zen. Journal starts Obsidian; add your RSS reader or its URL to that kit.
Dash includes the local dashboard; add your own homelab links. Mail, Chat,
Calendar and Misc leave application choices open rather than guessing accounts.

Missing executables appear as skipped actions in the preview. Directories must
exist. There is no automatic launch on workspace selection and no package
installation. Confirmation is invalidated when configuration or capabilities
change. Application launches are not reversible. Repeated launches can create
new windows; existing single-instance applications may reuse their windows.

New windows use Hyprland's
[workspace exec rule](https://wiki.hypr.land/Configuring/Dispatchers/).
Argument arrays are shell-quoted only at that dispatcher boundary. A helper
changes the working directory and directly executes the selected program.

Terminal profiles affect new terminals only. User paths and links are local
configuration and are not part of portable identity exports.
