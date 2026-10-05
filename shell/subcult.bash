# SUBCULT Rice shell integration.
export PATH="$HOME/.local/bin:$PATH"
subcult_tools_env="${XDG_STATE_HOME:-$HOME/.local/state}/subcult-rice/tools/tools.env"
[[ -r $subcult_tools_env ]] && source "$subcult_tools_env"
unset subcult_tools_env
[[ -r $HOME/.config/omarchy/subcult-command-telemetry.bash ]] && source "$HOME/.config/omarchy/subcult-command-telemetry.bash"
