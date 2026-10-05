# Upgrade, rollback, and removal

## Upgrade from v1.5.0 to v1.5.1

Download the v1.5.1 archive and checksum from GitHub Releases, then verify and
install using the same preset or component selection as before:

```bash
sha256sum --check subcult-omarchy-rice-1.5.1.tar.gz.sha256
tar -xzf subcult-omarchy-rice-1.5.1.tar.gz
cd subcult-omarchy-rice-1.5.1
./scripts/build-release verify-root .
./install.sh --dry-run --preset default
./install.sh --apply --preset default
```

This patch needs no configuration-schema migration. It preserves workspace
names and user preferences. Reload the shell with `omarchy restart shell` if
the updated labels are not visible, then check `subcult-presentation` twice to
launch and dismiss the layout. Restore the printed installer snapshot with
`./rollback.sh <snapshot>` if needed.

## Guided migration into v1.5

The v1.5 suite includes a versioned configuration migration assistant. Preview
is always read-only and reports the detected source version, target version,
preserved preferences, every complete-file replacement, ownership, conflicts,
and the exact decisions still required:

```bash
subcult-migrate preview
subcult-migrate preview --json
subcult-migrate status --json
```

Apply refuses to start until every reported conflict has an explicit `keep` or
`replace` choice. Conflict IDs come directly from the preview; for example:

```bash
subcult-migrate apply \
  --resolve shell=replace \
  --resolve hyprland=replace \
  --resolve bindings=keep \
  --resolve looknfeel=replace
```

`keep` leaves that exact user file untouched. `replace` first captures its
bytes and permissions. The resulting snapshot path is printed and may be
restored explicitly with `subcult-migrate rollback <snapshot>`. No choice implies
permission, and there is no “reset everything” fallback.

If power loss or process termination interrupts an apply, the active journal
blocks additional migrations. Inspect `subcult-migrate status --json`, then run
`subcult-migrate recover`. Recovery validates every required backup before
restoring anything and returns all touched files to their pre-apply state.
Static desktop recovery remains separately available through `subcult-recovery`.

## Upgrade from v1.4.1 to v1.5

Download and verify the v1.5.0 archive, then preview both the configuration
migration and the same installer selection used for v1.4.1:

```bash
sha256sum --check subcult-omarchy-rice-1.5.0.tar.gz.sha256
tar -xzf subcult-omarchy-rice-1.5.0.tar.gz
cd subcult-omarchy-rice-1.5.0
./scripts/build-release verify-root .
subcult-migrate preview
./install.sh --dry-run --preset default
./install.sh --apply --preset default
snapshot=$(cat ~/.local/state/subcult-rice/last-install-backup)
./validate.sh
```

Replace `default` with the prior preset or component list. The installer
preserves affinity, operating profile, resilience, sound, activity-mode,
disclosure, operations-log policy, performance, topology, media, workspace,
visual, scene, and core user configuration. History remains local state and is
not overwritten. New sound categories, coordinated activity actions, and
context automation remain disabled until explicitly opted in.

Confirm compact defaults with `subcult-disclosure status`, inspect the new private
archive with `subcult-operations-log status`, and preview—not apply—an activity
mode with `subcult-activity-mode preview focus`. To return to the exact pre-v1.5
filesystem state:

```bash
./rollback.sh "$snapshot"
omarchy restart shell
systemctl --user restart subcult-start-page.service
hyprctl reload
hyprctl configerrors
```

Rollback restores the files owned by this transaction and removes newly
created v1.5 files; it does not delete pre-existing local history or unrelated
configuration.

## Upgrade from v1.3.1 to v1.4

v1.4 preserves the v1.3.1 desktop behavior while adding distribution metadata,
cross-channel safeguards, and public release packaging. Do not install the
standalone theme over an existing suite—or the suite over a Git-installed
standalone theme—because both own the `subcult` theme path.

Download the new archive and matching checksum from the GitHub release, verify
them, and preview the same preset or components used previously:

```bash
sha256sum --check subcult-omarchy-rice-1.4.1.tar.gz.sha256
tar -xzf subcult-omarchy-rice-1.4.1.tar.gz
cd subcult-omarchy-rice-1.4.1
./scripts/build-release verify-root .
./preflight.py
./install.sh --dry-run --preset default
./install.sh --apply --preset default
snapshot=$(cat ~/.local/state/subcult-rice/last-install-backup)
./validate.sh
```

Replace `default` with the prior selection. Personal `subcult.json`, motion,
context, affinity, and profile choices remain preserved. To return to the exact
pre-v1.4 filesystem state:

```bash
./rollback.sh "$snapshot"
omarchy restart shell
hyprctl reload
hyprctl configerrors
```

Git-checkout users may use `git pull --ff-only` instead of downloading an
archive, after confirming `git status --short` is clean. Arch users must first
deactivate a source/archive activation, install the package, and then explicitly
run `subcult-rice setup`; see `ARCH_PACKAGING.md` and `CROSS_CHANNEL.md`.

## Upgrade from v1.3.0 to v1.3.1

v1.3.1 changes shell plugins, affinity commands, and start-page assets. Update
the checkout and preview the same preset or components used for v1.3.0:

```bash
git status --short
git pull --ff-only
./preflight.py
./install.sh --dry-run --preset default
./install.sh --apply --preset default
snapshot=$(cat ~/.local/state/subcult-rice/last-install-backup)
./validate.sh
```

Replace `default` with the previously installed preset or explicit component
selection. Personal `subcult.json`, motion, context automation, and affinity
mode choices remain preserved. A normal browser refresh fetches versioned,
no-store start-page assets; clearing Zen or Chromium profile data is not
required.

Verify the live semantic projection and restart-free palette path:

```bash
curl --fail http://127.0.0.1:8765/api/desktop | jq .
subcult-bar-refresh status | jq .
```

To restore the exact pre-v1.3.1 files from this transaction:

```bash
./rollback.sh "$snapshot"
omarchy restart shell
systemctl --user restart subcult-start-page.service
```

The restart after rollback is necessary because an older on-disk start-page or
shell implementation may have been restored. It is not part of normal affinity
switching or the v1.3.1 upgrade path.

## Upgrade from v1.2 to v1.3

Preserve local repository edits, update, and preview the same preset or explicit
component selection used for v1.2:

```bash
git status --short
git pull --ff-only
./preflight.py
./install.sh --dry-run --preset default
./install.sh --apply --preset default
omarchy theme set subcult
./validate.sh
```

Record the exact snapshot printed by `install.sh` before doing anything else:

```bash
snapshot=$(cat ~/.local/state/subcult-rice/last-install-backup)
test -f "$snapshot/manifest.tsv"
```

The transaction preserves `~/.config/omarchy/subcult.json` and adds missing
v1.3 context/ambient defaults in memory without silently opting into automation.
The context controller ignores unknown persisted schemas until an explicit
refresh publishes clean schema v1. Verify the new layer without enabling
automation:

```bash
subcult-context status --json
subcult-context refresh --json
subcult-context explain
subcult-context-automation preview
```

To return to the exact pre-v1.3 filesystem state, use the recorded snapshot:

```bash
./rollback.sh "$snapshot"
omarchy restart shell
hyprctl reload
hyprctl configerrors
```

Rollback restores every replaced file and removes every file created by that
single v1.3 transaction. It does not reverse older transactions or delete
preserved personal configuration. If the shell component was not part of your
v1.3 selection, omit the shell restart; if Hyprland was not selected, the reload
is harmless but optional.

## Upgrade from v1.1

Keep any local repository edits, update, and preview the same preset used for
v1.1:

```bash
git status --short
git pull --ff-only
./preflight.py
./install.sh --dry-run --preset default
./install.sh --apply --preset default
omarchy theme set subcult
./validate.sh
```

Replace `default` with `minimal`, `full`, or your prior explicit component
selection. The transaction preserves `~/.config/omarchy/subcult.json` and
the selected `motion.mode`; it adds the coordinated motion token profile and
dynamic shell services. Verify the resolved setting with `subcult-motion show`.

To return to the exact pre-upgrade state, run `./rollback.sh` with the snapshot
printed by the apply transaction, then run `omarchy restart shell` and
`hyprctl reload`. Rolling back restores replaced files and removes files newly
created by that transaction; it does not erase older snapshots or personal
configuration that the installer did not own.

## Upgrade from v1.0-era installs

Update without overwriting local uncommitted work, then preview:

```bash
git status --short
git pull --ff-only
./preflight.py
./install.sh --dry-run --preset default
```

Apply the preset previously used, or explicit components. The shell component
moves old `so1omon.*` plugin directories into the rollback snapshot and installs
public `subcult.*` IDs. It updates layouts, manifests, QML modules, and
services together while preserving `~/.config/omarchy/subcult.json`.

```bash
./install.sh --apply --preset default
omarchy theme set subcult
./validate.sh
```

Do not manually rename plugin directories.

## Recover a transaction

Failed transactions roll back automatically. To reverse a successful latest
transaction:

```bash
cat ~/.local/state/subcult-rice/last-install-backup
./rollback.sh
```

For an older transaction, inspect its manifest first:

```bash
snapshot=~/.local/state/subcult-rice/install-backups/<snapshot-name>
less "$snapshot/manifest.tsv"
./rollback.sh "$snapshot"
```

## Safe uninstall-equivalent recovery

There is intentionally no broad recursive uninstall command. A fresh install
is removed safely by rolling back its installation snapshot. With multiple
apply transactions, each snapshot represents only its delta:

1. Save personal edits made after installation.
2. List snapshots newest first with
   `ls -1dt ~/.local/state/subcult-rice/install-backups/*`.
3. Inspect each `manifest.tsv`.
4. Roll back applicable snapshots newest to oldest until the initial install
   is reversed.
5. Verify repository source with `SUBCULT_SOURCE_ONLY=1 ./validate.sh`.
6. Reapply the prior non-SUBCULT theme and restart the shell if needed.

Do not recursively delete `~/.config/omarchy`, `~/.config/hypr`, or the backup
tree. They can contain unrelated data and the only copies of replaced files.
