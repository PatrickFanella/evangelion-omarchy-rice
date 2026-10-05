# Theme variants

SUBCULT Rice keeps identity and presentation separate. Wallpaper affinity
selects SUBCULT, Acid Block, Paper Stock, VIOLET, or INK chroma; a theme
variant resolves that shared palette as Standard Press, OLED Blackout,
Paper Daylight, or High Contrast. This inheritance model provides every
affinity/variant combination without copied themes or changed wallpaper rules.

Use the **Affinity → Theme treatment** row in SUBCULT Control Center, or:

```bash
subcult-theme-variant list
subcult-theme-variant status
subcult-theme-variant preview oled
subcult-theme-variant revert
subcult-theme-variant apply daylight
```

`preview` immediately coordinates theme colors, shell surfaces, Hyprland
borders, and the terminal palette while preserving the committed variant.
Additional previews keep the original rollback point. `revert` restores it;
`apply` commits a selection and clears any preview. Variant state is private
(`0600`) under `~/.local/state/subcult-rice/theme-variant`.

Standard preserves the existing baseline. OLED uses true-black primary
surfaces; Daylight supplies light surfaces and affinity-specific dark accents;
High Contrast targets at least 7:1 primary text contrast. Automated tests cover
the complete 5 × 4 matrix, seven wallpaper mappings, panels, accents, bar icons,
transaction semantics, and terminal coordination.

Wallpaper Auto affinity remains authoritative. Changing treatment never changes
the wallpaper or active SUBCULT unit, and changing wallpaper retains the treatment.
`subcult-affinity palette` reports both dimensions as JSON.
