#/usr/bin/env bash

function _get_gitviper_commands() {
    echo status
    echo log
    echo tasks
    echo stash
    echo branch
}

_gitviper_command_list()
{
    # Avoid auto completing multiple values
    if [ "${#COMP_WORDS[@]}" == "2" ]; then
        COMPREPLY=($(compgen -W "$(_get_gitviper_commands)" -- "${COMP_WORDS[1]}"))
    #elif [ "${#COMP_WORDS[@]}" == "3" ]; then
        #COMPREPLY=($(compgen -W "$(_get_gitviper_commands)" -- "${COMP_WORDS[1]}"))
        #return
    fi
    return
}

complete -F _gitviper_command_list gitviper
complete -F _gitviper_command_list gv