HISTFILE=~/.histfile HISTSIZE=1000 SAVEHIST=1000
bindkey -e
autoload -U select-word-style
select-word-style bash
WORDCHARS=vared

ZINIT_HOME="${XDG_DATA_HOME:-${HOME}/.local/share}/zinit/zinit.git"
[ ! -d $ZINIT_HOME ] && mkdir -p "$(dirname $ZINIT_HOME)"
[ ! -d $ZINIT_HOME/.git ] && git clone https://github.com/zdharma-continuum/zinit.git "$ZINIT_HOME"
source "${ZINIT_HOME}/zinit.zsh"

zinit light romkatv/powerlevel10k
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

zinit light zsh-users/zsh-syntax-highlighting

zinit light marlonrichert/zsh-autocomplete
bindkey "^I" menu-select
bindkey "$terminfo[kcbt]" menu-select
bindkey -M menuselect "^I" menu-complete
bindkey -M menuselect "$terminfo[kcbt]"	reverse-menu-complete
bindkey -M menuselect  "${terminfo[kcub1]}" .backward-char
bindkey -M menuselect  "${terminfo[kcuf1]}"  .forward-char
bindkey -M menuselect "^M" .accept-line

zinit load zsh-users/zsh-history-substring-search
HISTORY_SUBSTRING_SEARCH_HIGHLIGHT_FOUND=
HISTORY_SUBSTRING_SEARCH_HIGHLIGHT_NOT_FOUND=fg=red
bindkey "$terminfo[kcuu1]" history-substring-search-up
bindkey "$terminfo[kcud1]" history-substring-search-down

FZF_DEFAULT_COMMAND="fd --type f --strip-cwd-prefix --hidden"
FZF_CTRL_T_COMMAND="fd --strip-cwd-prefix --hidden"
FZF_ALT_C_COMMAND="fd --type d --strip-cwd-prefix --hidden"
FZF_DEFAULT_OPTS="--height ~50% --layout reverse"
source <(fzf --zsh)
bindkey '^F' fzf-file-widget

eval "$(zoxide init zsh --cmd cd)"

bindkey "${terminfo[kLFT5]}"  backward-word
bindkey "${terminfo[kRIT5]}" forward-word
bindkey "${terminfo[khome]}" beginning-of-line
bindkey "${terminfo[kend]}" end-of-line
bindkey "${terminfo[kich1]}" overwrite-mode
bindkey "${terminfo[kbs]}" backward-delete-char
bindkey "${terminfo[kdch1]}" delete-char
bindkey "${terminfo[kcub1]}" backward-char
bindkey "${terminfo[kcuf1]}" forward-char
bindkey "${terminfo[kpp]}" beginning-of-buffer-or-history
bindkey "${terminfo[knp]}" end-of-buffer-or-history
bindkey "^[[1;3D" backward-word
bindkey "^[[1;3C" forward-word

if (( ${+terminfo[smkx]} && ${+terminfo[rmkx]} )); then
	autoload -Uz add-zle-hook-widget
	function zle_application_mode_start { echoti smkx }
	function zle_application_mode_stop { echoti rmkx }
	add-zle-hook-widget -Uz zle-line-init zle_application_mode_start
	add-zle-hook-widget -Uz zle-line-finish zle_application_mode_stop
fi

alias cat='bat --style=-full'
alias ls="ls --color --group-directories-first --human-readable --literal --hyperlink -v"