# Desktop recipes

`subcult-recipe open` previews Development, Journal / Writing, Browsing, Media,
and Local & Homelab recipes. Each coordinates a workspace, existing affinity
scene, focus mode, and motion preference. Edit `~/.config/omarchy/desktop-recipes.json`
to customize them. Recipes never activate automatically.

```sh
subcult-recipe list
subcult-recipe preview write
subcult-recipe apply write --confirm PLAN_ID
subcult-recipe undo
```

The confirmation must match a fresh preview, including current desktop state.
Unavailable required controllers block activation. Optional scene capabilities
retain the existing scene controller's degraded behavior. Sound stays `keep`
in every shipped recipe; the scene controller retains its explicit audio authority.

Add `--launch-apps` to both preview and apply to launch the workspace kit after
settings succeed. Undo restores settings and the previous workspace; it does
not close applications. A failed settings transaction attempts rollback and
reports incomplete restoration. If someone applies another scene, recipe undo
refuses to overwrite that newer scene transaction. One recipe receipt is retained;
apply another recipe only after deciding whether to undo the previous one.
