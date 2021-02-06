#!/bin/bash
GITVIPER_DIRECTORY="$( builtin cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source ${GITVIPER_DIRECTORY}/autocomplete.bash

# actual GitViper scripts
alias gitviper='python3 ${GITVIPER_DIRECTORY}/GitViper.py'
function tasklist() { python3 "${GITVIPER_DIRECTORY}/TaskList.py" "$@" | gvless; }

# utility functions
function gvless() { less --raw-control-chars --quit-if-one-screen --no-init; }
function gvclear() { tput reset; }

alias q='gvclear'
alias gv='gitviper'

# git shortcuts
alias s="gvclear && gitviper"
alias c="gitviper_commit"
alias a="gitviper_add"
alias a.="gitviper_add_all"
alias d="gvclear && git diff"
alias ds="d --staged"

# TaskView shortcuts
alias tasks='gvclear && tasklist'

# logs
# alias log="gitviper log | gvless"
function log() { gitviper log "$@" | gvless; }
alias graph='git log --graph --oneline --decorate --all'
alias gt="graph --since='6am'"

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
