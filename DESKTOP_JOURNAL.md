# Desktop journal

Search the sanitized operations index from the dashboard or command palette:

```sh
subcult-journal search "focus" --category focus --limit 20
subcult-journal search "" --since 1791648000
subcult-journal open
```

Read-only search creates no files and does not change retention. The existing
operations log remains the single bounded store, with its entry/day/byte limits,
deduplication, redaction, export, and confirmed deletion controls.

Automatic journal hooks start disabled. `subcult-journal enable` allows workspace
kit, recipe, focus, and mission events to be recorded. Hooks write named state
changes, never window titles, command lines, keystrokes, application usage, or
browser history. Updates/builds can be recorded by your own automation with
`subcult-journal event update`, `build-passed`, or `build-failed`.

```sh
subcult-journal enable
subcult-journal session start
subcult-journal note "Review the dashboard layout"
subcult-journal session end
subcult-journal summary
subcult-journal disable
```

Notes are explicit user input and use existing sanitization; avoid adding secrets.
Session summaries count up to 100 retained event groups and report this limit.
They do not measure productivity or time spent in applications. Disabling stops
new journal hooks; existing notification and operations logging keep their own
behavior. Use `subcult-operations-log clear-plan` then `clear --confirm TOKEN`
to delete the shared index, or `export DESTINATION` for a private JSON export.
