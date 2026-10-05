#!/usr/bin/env bash
# Upgrade an isolated Evangelion Rice 1.5 install to SUBCULT and roll it back.
set -euo pipefail
root=$(cd -- "$(dirname -- "$0")/.." && pwd)
fixtures=$root/tests/fixtures/evangelion-1.5
test_root=$(mktemp -d)
trap 'rm -rf -- "$test_root"' EXIT
home=$test_root/home
pass(){ printf 'PASS  %s\n' "$1"; }
fail(){ printf 'FAIL  %s\n' "$1" >&2; exit 1; }
run_install(){ PYTHONDONTWRITEBYTECODE=1 HOME=$home XDG_STATE_HOME=$test_root/state SUBCULT_SKIP_ACTIVATE=1 SUBCULT_RELEASE_ARTIFACT_NESTED=1 SUBCULT_CROSS_CHANNEL_NESTED=1 "$root/install.sh" "$@"; }
# Rollback restores files and links; directories created by the install may remain empty.
tree(){ (cd "$home" && find . \( -type f -o -type l \) -printf '%p %y %m\n' | sort && find . -type f -exec sha256sum {} + | sort) | sha256sum; }
run_rollback(){ HOME=$home XDG_STATE_HOME=$test_root/state SUBCULT_SKIP_ACTIVATE=1 "$root/rollback.sh" "$@"; }

mkdir -p "$home/.config/omarchy/plugins/evangelion.motion" "$home/.local/bin" \
  "$home/.config/systemd/user" "$home/.local/share/evangelion-rice"
printf '{"id":"evangelion.motion"}\n' >"$home/.config/omarchy/plugins/evangelion.motion/manifest.json"
printf '#!/usr/bin/env sh\n' >"$home/.local/bin/magi-affinity"
chmod +x "$home/.local/bin/magi-affinity"
printf '[Unit]\n' >"$home/.config/systemd/user/magi-start-page.service"
printf '{"terminal":"foot","project_dir":"/srv/work"}\n' >"$home/.config/omarchy/evangelion.json"
printf '# shell\n' >"$home/.config/omarchy/evangelion.bash"
cp "$fixtures/workspaces.json" "$home/.config/omarchy/workspaces.json"
printf '{"user":"edited"}\n' >"$home/.config/omarchy/scenes.json"
printf 'export KEEP=1\n\n# Evangelion Rice\n[[ -r $HOME/.config/omarchy/evangelion.bash ]] && source "$HOME/.config/omarchy/evangelion.bash"\n' >"$home/.bashrc"
before=$(tree)

plan=$(run_install --dry-run --preset default)
[[ $plan == *"RETIRE    legacy"*"evangelion.motion"* && $plan == *"UNHOOK    legacy"* ]] || fail "plan omitted legacy retirement"
pass "upgrade plan lists retired Evangelion paths"

run_install --apply --preset default --yes >"$test_root/install.log" 2>&1 || { tail -40 "$test_root/install.log" >&2; fail "upgrade install failed"; }
[[ ! -e $home/.config/omarchy/plugins/evangelion.motion && ! -e $home/.local/bin/magi-affinity ]] || fail "legacy suite remained installed"
[[ ! -e $home/.config/systemd/user/magi-start-page.service && ! -e $home/.local/share/evangelion-rice ]] || fail "legacy services or data remained"
[[ -x $home/.local/bin/subcult-affinity && -f $home/.config/omarchy/plugins/subcult.motion/manifest.json ]] || fail "SUBCULT suite missing after upgrade"
cmp -s <(printf '{"terminal":"foot","project_dir":"/srv/work"}\n') "$home/.config/omarchy/subcult.json" || fail "user configuration was not carried over"
cmp -s "$root/omarchy/workspaces.json" "$home/.config/omarchy/workspaces.json" || fail "unedited legacy default was not replaced"
[[ $(cat "$home/.config/omarchy/scenes.json") == '{"user":"edited"}' ]] || fail "edited configuration was replaced"
! grep -q 'evangelion' "$home/.bashrc" && grep -q 'export KEEP=1' "$home/.bashrc" || fail "legacy shell hook not removed cleanly"
pass "upgrade retires Evangelion paths and keeps user settings"

run_rollback >/dev/null
after=$(tree)
[[ -f $home/.config/omarchy/plugins/evangelion.motion/manifest.json && -x $home/.local/bin/magi-affinity ]] || fail "rollback did not restore legacy suite"
[[ ! -e $home/.local/bin/subcult-affinity && ! -e $home/.config/omarchy/subcult.json ]] || fail "rollback left SUBCULT files"
[[ $before == "$after" ]] || fail "rollback did not restore the exact legacy tree"
pass "rollback restores the Evangelion install exactly"
