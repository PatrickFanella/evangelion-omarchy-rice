# SUBCULT Rice Fish integration.
fish_add_path --prepend "$HOME/.local/bin"
set -l subcult_tools_env (set -q XDG_STATE_HOME; and echo "$XDG_STATE_HOME/subcult-rice/tools/tools.fish"; or echo "$HOME/.local/state/subcult-rice/tools/tools.fish")
test -r "$subcult_tools_env"; and source "$subcult_tools_env"
