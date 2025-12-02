if status is-interactive
    if type -q fzf
        fzf --fish | source
        set -x FZF_DEFAULT_COMMAND "fd --type f --strip-cwd-prefix --hidden"
        set -x FZF_CTRL_T_COMMAND "fd --strip-cwd-prefix --hidden"
        set -x FZF_ALT_C_COMMAND "fd --type d --strip-cwd-prefix --hidden"
        set -x FZF_DEFAULT_OPTS "--height ~50% --layout reverse"
        set -x FZF_CTRL_T_OPTS $FZF_DEFAULT_OPTS
        set -x FZF_ALT_C_OPTS $FZF_DEFAULT_OPTS
    end
end
