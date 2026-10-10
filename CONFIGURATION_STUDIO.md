# Configuration studio

Open the command palette's **Configuration studio**, or run `subcult-studio open`.
The terminal hosts a loopback server on port 8766 until Ctrl+C. No user service
is enabled. Use `subcult-studio serve` to open the URL yourself.

The studio edits all ten workspace names, icons and accents, the icon/number/name
display preference, widget order and section, motion mode, density, opacity,
gaps and borders. Its live preview approximates the bar; actual fonts, available
widgets and monitor size still determine the desktop result. Monitor scale stays
outside the editor.

Preview shows the exact changed fields. Apply requires that same draft and
unchanged configuration files; browser plans expire after five minutes. Each
apply stores one private undo receipt. Undo refuses if any edited file changed
after apply. Missing runtime commands are reported; saved settings remain ready
for the next session. File-write failures restore the preceding configuration.

Required indicators cannot be removed. Existing widget settings and unrelated
configuration fields are preserved. Export contains only visual/workspace/layout
fields, without links, directories, credentials, or monitor settings. Import is
validated and becomes a draft. Symbolic-link configuration files are refused.
The server checks loopback Host, same Origin and an in-memory request token;
it exposes no arbitrary file path, shell command, or remote fetch API.
