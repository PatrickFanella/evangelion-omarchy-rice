# SUBCULT Rice Zsh integration.
export PATH="$HOME/.local/bin:$PATH"
subcult_tools_env="${XDG_STATE_HOME:-$HOME/.local/state}/subcult-rice/tools/tools.env"
[[ -r $subcult_tools_env ]] && source "$subcult_tools_env"
unset subcult_tools_env
