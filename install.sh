#!/usr/bin/env bash
set -Eeuo pipefail
root=$(cd -- "$(dirname -- "$0")" && pwd)
state_root=${XDG_STATE_HOME:-$HOME/.local/state}/subcult-rice
dry_run=false apply=false assume_yes=false preset=default component_arg= shell_choice=auto shell_opt_out=false tmux_opt_out=false start_page_opt_in=false
transaction_started=false backup_root= manifest=
readonly all_components=(theme tools shell hypr start-page services extras shell-integration neon-overdrive)
readonly legacy_plugin_ids=(
  so1omon.angel-intrusion so1omon.atfield so1omon.battery so1omon.cava
  so1omon.clipboard so1omon.communications so1omon.device-osd so1omon.health
  so1omon.lock so1omon.magi-idle so1omon.media so1omon.mission
  so1omon.notifications so1omon.operating-profile so1omon.power
  so1omon.power-sequence so1omon.privacy so1omon.thermal
  so1omon.update-operation so1omon.workspace-osd so1omon.workspaces
  so1omon.world-clock
)
# Evangelion Rice 1.x paths that the SUBCULT suite replaces. Upgrades move
# them into the rollback snapshot instead of deleting them.
readonly legacy_suite_paths=(
  .config/omarchy/plugins/evangelion.agents
  .config/omarchy/plugins/evangelion.angel-intrusion
  .config/omarchy/plugins/evangelion.atfield
  .config/omarchy/plugins/evangelion.battery
  .config/omarchy/plugins/evangelion.bluetooth
  .config/omarchy/plugins/evangelion.cava
  .config/omarchy/plugins/evangelion.clipboard
  .config/omarchy/plugins/evangelion.command-palette
  .config/omarchy/plugins/evangelion.communications
  .config/omarchy/plugins/evangelion.context
  .config/omarchy/plugins/evangelion.demo
  .config/omarchy/plugins/evangelion.device-osd
  .config/omarchy/plugins/evangelion.dropbox
  .config/omarchy/plugins/evangelion.health
  .config/omarchy/plugins/evangelion.icon-theme
  .config/omarchy/plugins/evangelion.localization
  .config/omarchy/plugins/evangelion.lock
  .config/omarchy/plugins/evangelion.magi-idle
  .config/omarchy/plugins/evangelion.media
  .config/omarchy/plugins/evangelion.mission
  .config/omarchy/plugins/evangelion.mode-transition
  .config/omarchy/plugins/evangelion.motion
  .config/omarchy/plugins/evangelion.notifications
  .config/omarchy/plugins/evangelion.operating-profile
  .config/omarchy/plugins/evangelion.operations-log
  .config/omarchy/plugins/evangelion.performance
  .config/omarchy/plugins/evangelion.power
  .config/omarchy/plugins/evangelion.power-sequence
  .config/omarchy/plugins/evangelion.privacy
  .config/omarchy/plugins/evangelion.scene-editor
  .config/omarchy/plugins/evangelion.settings
  .config/omarchy/plugins/evangelion.tailscale
  .config/omarchy/plugins/evangelion.thermal
  .config/omarchy/plugins/evangelion.update-operation
  .config/omarchy/plugins/evangelion.workspace-names
  .config/omarchy/plugins/evangelion.workspace-osd
  .config/omarchy/plugins/evangelion.workspaces
  .config/omarchy/plugins/evangelion.world-clock
  .local/bin/eva-capabilities .local/bin/eva-terminal-profile
  .local/bin/eva-user-config .local/bin/magi-activity-mode
  .local/bin/magi-affinity .local/bin/magi-ambient
  .local/bin/magi-bar-refresh .local/bin/magi-battery-alert
  .local/bin/magi-boot-sequence .local/bin/magi-capture .local/bin/magi-clock
  .local/bin/magi-command-palette .local/bin/magi-command-telemetry
  .local/bin/magi-communications .local/bin/magi-context
  .local/bin/magi-context-automation .local/bin/magi-control-reference
  .local/bin/magi-demo .local/bin/magi-deployment
  .local/bin/magi-device-monitor .local/bin/magi-device-osd
  .local/bin/magi-disclosure .local/bin/magi-downloads
  .local/bin/magi-extension-state .local/bin/magi-focus
  .local/bin/magi-health .local/bin/magi-i18n .local/bin/magi-intrusion
  .local/bin/magi-machine-profile .local/bin/magi-media
  .local/bin/magi-migrate .local/bin/magi-mission .local/bin/magi-motion
  .local/bin/magi-onboard .local/bin/magi-operating-profile
  .local/bin/magi-operations-log .local/bin/magi-performance
  .local/bin/magi-performance-budget .local/bin/magi-power-sequence
  .local/bin/magi-presentation .local/bin/magi-privacy
  .local/bin/magi-recovery .local/bin/magi-resilience
  .local/bin/magi-rice-health .local/bin/magi-scene
  .local/bin/magi-screensaver .local/bin/magi-screensaver-mode
  .local/bin/magi-settings .local/bin/magi-snapshot .local/bin/magi-sound
  .local/bin/magi-start-page .local/bin/magi-suite-update
  .local/bin/magi-terminal-context .local/bin/magi-theme-variant
  .local/bin/magi-thermal-alert .local/bin/magi-topology
  .local/bin/magi-update .local/bin/magi-visual .local/bin/magi-workspace-osd
  .local/bin/magi-workspaces
  .config/systemd/user/magi-affinity.path .config/systemd/user/magi-affinity.service
  .config/systemd/user/magi-start-page.service .config/systemd/user/magi-topology.service
  .config/omarchy/hooks/post-boot.d/magi-boot-sequence.hook
  .config/omarchy/hooks/theme-set.d/eva-terminal-profile.hook
  .config/omarchy/hooks/theme-set.d/magi-affinity.hook
  .config/omarchy/evangelion.json .config/omarchy/evangelion-update.json
  .config/omarchy/evangelion.bash .config/omarchy/evangelion.zsh .config/omarchy/evangelion.fish
  .config/omarchy/magi-command-telemetry.bash .config/omarchy/magi-clock.json
  .config/omarchy/magi-terminal-context.json
  .config/nvim/lua/plugins/eva-terminal-profile.lua
  .local/lib/evangelion-rice .local/share/evangelion-rice
)
readonly legacy_units=(magi-affinity.path magi-affinity.service magi-start-page.service magi-topology.service)
# SHA-256 of Evangelion 1.5 defaults whose content names retired wallpapers,
# workspaces, or repositories. Unedited copies take the SUBCULT default;
# edited copies are preserved.
declare -A legacy_defaults=(
  [workspaces.json]=270fcf6229a2774a5c660a28a0f19278e1139edfa817ca4e9b605e7b09a39d3c
  [scenes.json]=a2533dcc7acb45c9a923611ac8ea4fdf8aa142d78ae21fb30ecaad34a445b3fc
)

usage(){ cat <<'EOF'
Usage: ./install.sh [--dry-run | --apply] [--preset minimal|default|full]
                    [--components NAME[,NAME...]] [--shell auto|bash|zsh|fish]
                    [--with-start-page] [--no-shell-integration] [--no-tmux-integration] [--yes]

minimal: theme + tools
default: minimal + shell + Hyprland + services
full:    default + application extras + detected-shell integration

Use --list-components for selectable components. --components overrides the
preset. --with-start-page adds the optional hosted browser start page.
Complete config replacements require interactive confirmation or --yes.
EOF
}
list_components(){ cat <<'EOF'
theme              SUBCULT theme, palettes, and wallpapers
tools              SUBCULT commands installed in ~/.local/bin
shell              Omarchy plugins, menus, hooks, and shell configuration
hypr               Hyprland bindings, behavior, and appearance configuration
start-page         Optional local SUBCULT start page, command, and user service
services           User systemd units for affinity and topology restoration
extras             Fastfetch and Neovim integrations
shell-integration  Bash, Zsh, or Fish startup integration (optional)
neon-overdrive     Compatibility widget for a detected Neon Overdrive theme
EOF
}
while (($#)); do
  case $1 in
    --dry-run) dry_run=true;; --apply) apply=true;; --yes|-y) assume_yes=true;;
    --preset) shift; preset=${1:-};; --components) shift; component_arg=${1:-};;
    --shell) shift; shell_choice=${1:-};; --no-shell-integration) shell_opt_out=true;;
    --no-tmux-integration) tmux_opt_out=true;;
    --with-start-page) start_page_opt_in=true;;
    --list-components) list_components; exit 0;; -h|--help) usage; exit 0;;
    *) printf 'Unknown option: %s\n' "$1" >&2; usage >&2; exit 2;;
  esac
  shift
done
$dry_run && $apply && { echo "Choose either --dry-run or --apply" >&2; exit 2; }
$dry_run || $apply || { echo "Choose --dry-run to preview or --apply to install." >&2; exit 2; }

declare -A selected=()
select_component(){
  local requested=$1 valid=false component
  for component in "${all_components[@]}"; do [[ $requested == "$component" ]] && valid=true; done
  $valid || { printf 'Unknown component: %s\n' "$requested" >&2; exit 2; }
  selected[$requested]=1
}
if [[ -n $component_arg ]]; then
  IFS=',' read -ra requested_components <<<"$component_arg"
  for component in "${requested_components[@]}"; do select_component "$component"; done
else
  case $preset in
    minimal) preset_components=(theme tools);;
    default) preset_components=(theme tools shell hypr services);;
    full) preset_components=(theme tools shell hypr services extras shell-integration);;
    *) printf 'Unknown preset: %s\n' "$preset" >&2; exit 2;;
  esac
  for component in "${preset_components[@]}"; do select_component "$component"; done
fi
$shell_opt_out && unset 'selected[shell-integration]'
$start_page_opt_in && select_component start-page

standalone_theme=$HOME/.config/omarchy/themes/subcult
if [[ ${selected[theme]:-0} == 1 && -d $standalone_theme/.git ]]; then
  cat >&2 <<EOF
CHANNEL CONFLICT // $standalone_theme is a Git-installed standalone theme.
Switch to another theme and remove that clone before activating the complete
suite. The installer will not merge suite-owned files into a Git-owned tree.
EOF
  exit 3
fi

preflight_args=()
[[ ${SUBCULT_SKIP_ACTIVATE:-0} == 1 ]] && preflight_args+=(--source-only)
[[ ${selected[start-page]:-0} == 1 ]] && preflight_args+=(--with-start-page)
"$root/preflight.py" "${preflight_args[@]}"
if [[ ${selected[neon-overdrive]:-0} == 1 ]] && ! "$root/bin/subcult-capabilities" has neon-overdrive; then
  echo "Neon Overdrive integration was requested but ~/.config/omarchy/themes/neon-overdrive/scripts/neon-control was not detected." >&2
  exit 1
fi

declare -a plan_component=() plan_source=() plan_target=() plan_mode=() plan_action=()
add_file(){
  local component=$1 source=$2 target=$3 mode=$4 policy=${5:-replace} action
  [[ ${selected[$component]:-0} == 1 ]] || return 0
  if [[ $policy == preserve && -f $target && -n ${legacy_defaults[${target##*/}]:-} ]] &&
    [[ $(sha256sum "$target" | cut -d' ' -f1) == "${legacy_defaults[${target##*/}]}" ]]; then action=replace
  elif [[ $policy == preserve && ( -e $target || -L $target ) ]]; then action=preserve
  elif [[ -f $target ]] && cmp -s "$source" "$target"; then action=unchanged
  elif [[ -e $target || -L $target ]]; then action=replace
  else action=create; fi
  plan_component+=("$component"); plan_source+=("$source"); plan_target+=("$target"); plan_mode+=("$mode"); plan_action+=("$action")
}
add_tree(){
  local component=$1 source_root=$2 target_root=$3 mode=$4 source rel
  [[ ${selected[$component]:-0} == 1 ]] || return 0
  while IFS= read -r source; do
    rel=${source#"$source_root/"}
    [[ $rel == __pycache__/* || $rel == *.pyc ]] && continue
    [[ $component == tools && $rel == subcult-start-page ]] && continue
    [[ $component == services && $rel == subcult-start-page.service ]] && continue
    add_file "$component" "$source" "$target_root/$rel" "$mode"
  done < <(find "$source_root" -type f | sort)
}
add_tree tools "$root/bin" "$HOME/.local/bin" 755
add_tree tools "$root/studio" "$HOME/.local/share/subcult-rice/studio" 644
add_tree tools "$root/lib" "$HOME/.local/lib/subcult-rice" 644
add_tree tools "$root/recovery" "$HOME/.local/share/subcult-rice/recovery" 644
add_tree tools "$root/migrations" "$HOME/.local/share/subcult-rice/migrations" 644
add_tree tools "$root/omarchy/i18n" "$HOME/.local/share/subcult-rice/i18n" 644
add_file tools "$root/VERSION" "$HOME/.local/share/subcult-rice/.suite-version" 644
add_file tools "$root/dependencies.tsv" "$HOME/.local/share/subcult-rice/dependencies.tsv" 644
add_file tools "$root/omarchy/performance-budgets.json" "$HOME/.local/share/subcult-rice/performance/performance-budgets.json" 644
add_file tools "$root/omarchy/performance-inventory.json" "$HOME/.local/share/subcult-rice/performance/performance-inventory.json" 644
add_file tools "$root/omarchy/rice-health.json" "$HOME/.local/share/subcult-rice/rice-health.json" 644
add_file tools "$root/omarchy/snapshot-manifest.json" "$HOME/.local/share/subcult-rice/snapshot-manifest.json" 644
add_file tools "$root/omarchy/settings-schema.json" "$HOME/.local/share/subcult-rice/settings-schema.json" 644
add_file tools "$root/omarchy/commands.json" "$HOME/.local/share/subcult-rice/commands.json" 644
add_file tools "$root/omarchy/theme-variants.json" "$HOME/.local/share/subcult-rice/theme-variants.json" 644
add_file tools "$root/omarchy/activity-modes.json" "$HOME/.local/share/subcult-rice/activity-modes.json" 644
add_file tools "$root/omarchy/heat-history.json" "$HOME/.local/share/subcult-rice/heat-history.json" 600
add_file tools "$root/omarchy/desktop-recipes.json" "$HOME/.local/share/subcult-rice/desktop-recipes.json" 600
add_file tools "$root/omarchy/dashboard.json" "$HOME/.local/share/subcult-rice/dashboard.json" 600
add_file tools "$root/omarchy/desktop-journal.json" "$HOME/.local/share/subcult-rice/desktop-journal.json" 600
add_file tools "$root/omarchy/adaptive-bar.json" "$HOME/.local/share/subcult-rice/adaptive-bar.json" 600
add_file tools "$root/omarchy/workspace-kits.json" "$HOME/.local/share/subcult-rice/workspace-kits.json" 600
add_file tools "$root/omarchy/disclosure.json" "$HOME/.local/share/subcult-rice/disclosure.json" 644
add_file shell "$root/omarchy/update.json" "$HOME/.config/omarchy/subcult-update.json" 644 preserve
add_tree theme "$root/theme" "$HOME/.config/omarchy/themes/subcult" 644
add_tree theme "$root/theme/brand/fonts" "$HOME/.local/share/fonts/subcult" 644
add_tree shell "$root/omarchy/plugins" "$HOME/.config/omarchy/plugins" 644
if [[ ${selected[shell]:-0} == 1 ]]; then
  for index in "${!plan_target[@]}"; do
    [[ ${plan_target[$index]} == "$HOME/.config/omarchy/plugins/neon.overdrive/"* ]] && plan_action[$index]=omit
  done
fi
add_tree neon-overdrive "$root/omarchy/plugins/neon.overdrive" "$HOME/.config/omarchy/plugins/neon.overdrive" 644
add_file shell "$root/omarchy/extensions/omarchy-menu.jsonc" "$HOME/.config/omarchy/extensions/omarchy-menu.jsonc" 644
subcult_config_source=$root/omarchy/subcult.json
[[ ! -e $HOME/.config/omarchy/subcult.json && -f $HOME/.config/omarchy/evangelion.json ]] &&
  subcult_config_source=$HOME/.config/omarchy/evangelion.json
add_file shell "$subcult_config_source" "$HOME/.config/omarchy/subcult.json" 644 preserve
add_file shell "$root/omarchy/resilience.json" "$HOME/.config/omarchy/resilience.json" 644 preserve
add_file shell "$root/omarchy/sound.json" "$HOME/.config/omarchy/sound.json" 600 preserve
add_file shell "$root/omarchy/activity-modes.json" "$HOME/.config/omarchy/activity-modes.json" 600 preserve
add_file shell "$root/omarchy/disclosure.json" "$HOME/.config/omarchy/disclosure.json" 600 preserve
add_file shell "$root/omarchy/operations-log.json" "$HOME/.config/omarchy/operations-log.json" 600 preserve
add_file shell "$root/omarchy/performance.json" "$HOME/.config/omarchy/performance.json" 644 preserve
for file in command-telemetry.json subcult-clock.json subcult-terminal-context.json motion.json operating-profiles.json shell.json thermal-alerts.json; do add_file shell "$root/omarchy/$file" "$HOME/.config/omarchy/$file" 644; done
add_file shell "$root/omarchy/topologies.json" "$HOME/.config/omarchy/topologies.json" 644 preserve
add_file shell "$root/omarchy/media.json" "$HOME/.config/omarchy/media.json" 644 preserve
add_file shell "$root/omarchy/heat-history.json" "$HOME/.config/omarchy/heat-history.json" 600 preserve
add_file shell "$root/omarchy/desktop-recipes.json" "$HOME/.config/omarchy/desktop-recipes.json" 600 preserve
add_file shell "$root/omarchy/dashboard.json" "$HOME/.config/omarchy/dashboard.json" 600 preserve
add_file shell "$root/omarchy/desktop-journal.json" "$HOME/.config/omarchy/desktop-journal.json" 600 preserve
add_file shell "$root/omarchy/adaptive-bar.json" "$HOME/.config/omarchy/adaptive-bar.json" 600 preserve
add_file shell "$root/omarchy/workspace-kits.json" "$HOME/.config/omarchy/workspace-kits.json" 600 preserve
add_file shell "$root/omarchy/workspaces.json" "$HOME/.config/omarchy/workspaces.json" 644 preserve
add_file shell "$root/omarchy/visual.json" "$HOME/.config/omarchy/visual.json" 644 preserve
add_file shell "$root/omarchy/scenes.json" "$HOME/.config/omarchy/scenes.json" 644 preserve
add_tree shell "$root/omarchy/hooks" "$HOME/.config/omarchy/hooks" 755
for file in bindings.lua hyprland.lua looknfeel.lua; do add_file hypr "$root/hypr/$file" "$HOME/.config/hypr/$file" 644; done
add_file start-page "$root/bin/subcult-start-page" "$HOME/.local/bin/subcult-start-page" 755
add_file start-page "$root/systemd/subcult-start-page.service" "$HOME/.config/systemd/user/subcult-start-page.service" 644
add_tree start-page "$root/start-page" "$HOME/.local/share/subcult-rice/start-page" 644
add_tree services "$root/systemd" "$HOME/.config/systemd/user" 644
add_file extras "$root/fastfetch/config.jsonc" "$HOME/.config/fastfetch/config.jsonc" 644
add_file extras "$root/nvim/lua/plugins/subcult-terminal-profile.lua" "$HOME/.config/nvim/lua/plugins/subcult-terminal-profile.lua" 644
add_file shell-integration "$root/shell/subcult-command-telemetry.bash" "$HOME/.config/omarchy/subcult-command-telemetry.bash" 644
add_file shell-integration "$root/shell/subcult.bash" "$HOME/.config/omarchy/subcult.bash" 644
add_file shell-integration "$root/shell/subcult.zsh" "$HOME/.config/omarchy/subcult.zsh" 644
add_file shell-integration "$root/shell/subcult.fish" "$HOME/.config/omarchy/subcult.fish" 644

if [[ ${selected[shell-integration]:-0} == 1 ]]; then
  [[ $shell_choice == auto ]] && shell_choice=$(basename "${SHELL:-bash}")
  case $shell_choice in
    bash) rc_target=$HOME/.bashrc; rc_line='[[ -r $HOME/.config/omarchy/subcult.bash ]] && source "$HOME/.config/omarchy/subcult.bash"' ;;
    zsh) rc_target=$HOME/.zshrc; rc_line='[[ -r $HOME/.config/omarchy/subcult.zsh ]] && source "$HOME/.config/omarchy/subcult.zsh"' ;;
    fish) rc_target=$HOME/.config/fish/config.fish; rc_line='test -r "$HOME/.config/omarchy/subcult.fish"; and source "$HOME/.config/omarchy/subcult.fish"' ;;
    *) printf 'Unsupported shell integration: %s; use --shell bash|zsh|fish or --no-shell-integration\n' "$shell_choice" >&2; exit 2 ;;
  esac
  if grep -qF "$rc_line" "$rc_target" 2>/dev/null; then rc_action=unchanged
  elif [[ -e $rc_target ]]; then rc_action=append
  else rc_action=create; fi
else rc_action=skip; fi
tmux_action=skip
if [[ ${selected[tools]:-0} == 1 ]] && ! $tmux_opt_out; then
  tmux_plan=$(python3 "$root/scripts/tmux-install-plan.py")
  IFS=$'\t' read -r tmux_action tmux_target tmux_line <<<"$tmux_plan"
fi
legacy_suite_retire=false
[[ ${selected[shell]:-0} == 1 && ${selected[tools]:-0} == 1 ]] && legacy_suite_retire=true
legacy_rc_files=()
$legacy_suite_retire && for legacy_rc in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.config/fish/config.fish"; do
  grep -qF '.config/omarchy/evangelion.' "$legacy_rc" 2>/dev/null && legacy_rc_files+=("$legacy_rc")
done

components=$(printf '%s\n' "${!selected[@]}" | sort | paste -sd, -)
printf 'SUBCULT INSTALL PLAN // %s\n' "$components"
changes=0 replacements=0
if [[ ${selected[shell]:-0} == 1 ]]; then
  for legacy_id in "${legacy_plugin_ids[@]}"; do
    legacy_target=$HOME/.config/omarchy/plugins/$legacy_id
    if [[ -d $legacy_target ]]; then
      printf '%-9s %-18s %s\n' MIGRATE shell "$legacy_target"
      changes=$((changes+1))
    fi
  done
fi
$legacy_suite_retire && for legacy_path in "${legacy_suite_paths[@]}"; do
  if [[ -e $HOME/$legacy_path || -L $HOME/$legacy_path ]]; then
    printf '%-9s %-18s %s\n' RETIRE legacy "$HOME/$legacy_path"
    changes=$((changes+1))
  fi
done
for legacy_rc in "${legacy_rc_files[@]}"; do
  printf '%-9s %-18s %s\n' UNHOOK legacy "$legacy_rc"
  changes=$((changes+1))
done
for index in "${!plan_target[@]}"; do
  printf '%-9s %-18s %s\n' "${plan_action[$index]^^}" "${plan_component[$index]}" "${plan_target[$index]}"
  [[ ${plan_action[$index]} == unchanged || ${plan_action[$index]} == preserve || ${plan_action[$index]} == omit ]] || changes=$((changes+1))
  [[ ${plan_action[$index]} == replace ]] && replacements=$((replacements+1))
done
if [[ $rc_action != skip ]]; then
  printf '%-9s %-18s %s\n' "${rc_action^^}" shell-integration "$rc_target"
  [[ $rc_action == unchanged ]] || changes=$((changes+1))
fi
if [[ $tmux_action != skip ]]; then
  printf '%-9s %-18s %s\n' "${tmux_action^^}" tmux-integration "$tmux_target"
  [[ $tmux_action == unchanged ]] || changes=$((changes+1))
fi
printf '\nPLAN SUMMARY // %d changes · %d complete-file replacements\n' "$changes" "$replacements"
$dry_run && { echo "DRY RUN COMPLETE // no target files changed"; exit 0; }

((replacements)) && printf '\nWARNING // %d existing complete configuration files will be replaced.\n' "$replacements" >&2
if ! $assume_yes; then
  [[ -t 0 ]] || { echo "Confirmation required; rerun interactively or pass --yes." >&2; exit 2; }
  read -r -p 'Apply this transaction? [y/N] ' answer
  [[ $answer == [yY] || $answer == [yY][eE][sS] ]] || { echo "Installation cancelled."; exit 1; }
fi

stamp=$(date +%Y%m%d-%H%M%S)-$$
backup_root=$state_root/install-backups/$stamp
manifest=$backup_root/manifest.tsv
mkdir -p "$backup_root/files"
printf '# SUBCULT Rice rollback manifest v2\n' >"$manifest"
transaction_started=true
backup_target(){
  local target=$1 rel=${1#/}
  if [[ -e $target || -L $target ]]; then
    mkdir -p "$backup_root/files/$(dirname "$rel")"; cp -a "$target" "$backup_root/files/$rel"; printf 'restore\t%s\n' "$target" >>"$manifest"
  else printf 'remove\t%s\n' "$target" >>"$manifest"; fi
}
transaction_failed(){
  local code=$?; trap - ERR; set +e
  if $transaction_started; then printf 'INSTALL FAILED // automatically restoring %s\n' "$backup_root" >&2; SUBCULT_SKIP_ACTIVATE=1 "$root/rollback.sh" "$backup_root" >&2; fi
  exit "$code"
}
trap transaction_failed ERR
if [[ ${selected[shell]:-0} == 1 ]]; then
  for legacy_id in "${legacy_plugin_ids[@]}"; do
    legacy_target=$HOME/.config/omarchy/plugins/$legacy_id
    [[ -d $legacy_target ]] || continue
    mkdir -p "$backup_root/legacy-plugins"
    mv -- "$legacy_target" "$backup_root/legacy-plugins/$legacy_id"
    printf 'restore-dir\t%s\n' "$legacy_target" >>"$manifest"
  done
fi
for index in "${!plan_target[@]}"; do
  [[ ${plan_action[$index]} == unchanged || ${plan_action[$index]} == preserve || ${plan_action[$index]} == omit ]] && continue
  backup_target "${plan_target[$index]}"
  install -Dm"${plan_mode[$index]}" "${plan_source[$index]}" "${plan_target[$index]}"
done
if $legacy_suite_retire && [[ ${SUBCULT_SKIP_ACTIVATE:-0} != 1 ]]; then
  for unit in "${legacy_units[@]}"; do
    [[ -e $HOME/.config/systemd/user/$unit ]] && systemctl --user disable --now "$unit" >/dev/null 2>&1 || true
  done
fi
$legacy_suite_retire && for legacy_path in "${legacy_suite_paths[@]}"; do
  legacy_target=$HOME/$legacy_path
  [[ -e $legacy_target || -L $legacy_target ]] || continue
  mkdir -p "$(dirname "$backup_root/legacy/$legacy_path")"
  mv -- "$legacy_target" "$backup_root/legacy/$legacy_path"
  printf 'restore-legacy\t%s\n' "$legacy_target" >>"$manifest"
done
for legacy_rc in "${legacy_rc_files[@]}"; do
  backup_target "$legacy_rc"
  sed -i -e '/^# Evangelion Rice$/d' -e '\|\.config/omarchy/evangelion\.|d' "$legacy_rc"
done
if [[ $rc_action != skip && $rc_action != unchanged ]]; then
  backup_target "$rc_target"; mkdir -p "$(dirname "$rc_target")"; [[ -e $rc_target ]] || : >"$rc_target"
  printf '\n# SUBCULT Rice\n%s\n' "$rc_line" >>"$rc_target"
fi
if [[ $tmux_action != skip && $tmux_action != unchanged ]]; then
  backup_target "$tmux_target"
  mkdir -p "$(dirname "$tmux_target")"
  printf '\n# SUBCULT affinity palette\n%s\n' "$tmux_line" >>"$tmux_target"
fi
[[ ${SUBCULT_FORCE_INSTALL_FAILURE:-0} == 1 ]] && false
if [[ ${SUBCULT_SKIP_ACTIVATE:-0} != 1 ]]; then
  [[ ${selected[shell]:-0} == 1 ]] && omarchy-shell -q shell rescanPlugins
  [[ ${selected[hypr]:-0} == 1 ]] && hyprctl reload >/dev/null
  [[ ${selected[theme]:-0} == 1 ]] && command -v fc-cache >/dev/null && fc-cache "$HOME/.local/share/fonts/subcult" >/dev/null 2>&1 || true
  if [[ ${selected[services]:-0} == 1 || ${selected[start-page]:-0} == 1 ]]; then
    systemctl --user daemon-reload
    if [[ ${selected[services]:-0} == 1 ]]; then
      systemctl --user enable --now subcult-affinity.path subcult-topology.service >/dev/null
    fi
    if [[ ${selected[start-page]:-0} == 1 ]]; then
      systemctl --user enable --now subcult-start-page.service >/dev/null
    fi
  fi
fi
if [[ -f $root/RELEASE-PROVENANCE.json ]]; then
  "$root/scripts/build-release" verify-root "$root"
else
  # The installer owns this transaction's activation check. Avoid recursively
  # running historical upgrade/channel installers inside it; those gates run
  # directly in CI and in the contributor validation entry point.
  SUBCULT_SOURCE_ONLY=${SUBCULT_SKIP_ACTIVATE:-0} \
    SUBCULT_CROSS_CHANNEL_NESTED=1 \
    SUBCULT_RELEASE_ARTIFACT_NESTED=1 \
    "$root/validate.sh"
fi
mkdir -p "$state_root"; printf '%s\n' "$backup_root" >"$state_root/last-install-backup"
transaction_started=false; trap - ERR
printf 'INSTALL COMPLETE // rollback snapshot: %s\n' "$backup_root"
