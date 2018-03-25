#!/bin/bash
GITVIPER_DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# actual GitViper scripts
alias gitviper='python3 ${GITVIPER_DIRECTORY}/GitViper.py'
function todo() { gvclear; python3 "${GITVIPER_DIRECTORY}/TaskList.py" "$@" | gvless; }

# utility functions
function gvless() { less --raw-control-chars --quit-if-one-screen --no-init; }
function gvclear() { tput reset; }

alias q='gvclear'

# git shortcuts
alias s="gvclear && gitviper"
alias c="gitviper_commit"
alias a="gitviper_add"
alias a.="gitviper_add_all"
alias d="gvclear && git diff"
alias ds="d --staged"

# logs
alias log="gitviper -t -b -s -st -ln -1 | gvless"
alias log2="git log --stat --date=relative"
alias graph='git log --graph --oneline --decorate --all'
alias gt="g --since='6am'"
alias gg="git log --graph --abbrev-commit --decorate --format=format:'%C(yellow)%h %C(reset)%C(red)(%ar)%C(reset) %C(dim white)%an%C(reset)%C(auto)%d%C(reset) %C(white)%s%C(reset)' --all"

# git function calls without git prefix
function checkout() { gvclear; git checkout "$@"; gitviper; }
function reset() { gvclear; git reset "$@"; gitviper; }
function push() { gvclear; git push "$@"; gitviper; }
function pull() { gvclear; git pull "$@"; gitviper; }
function fetch() { gvclear; git fetch "$@"; gitviper; }
function stash() { gvclear; git stash save "$@"; gitviper; }
function pop() {
	gvclear;
	ID="$1"
	if [ "$#" -lt 1 ]; then
		ID="0";
	fi
	git stash pop stash@{$ID};
	gitviper;
}

# functions used by aliases
function gitviper_add() { git add "$@"; s; }
function gitviper_add_all() { git add . "$@"; s; }
function gitviper_commit() { gvclear; git commit -m "$@"; gitviper; }
function gitviper_log() { git log "$@" --pretty=format:'%C(cyan)%ad|%C(green)%an|%Cgreen%d %Creset%s' --date=relative --all | column -ts'|' | gvless; }