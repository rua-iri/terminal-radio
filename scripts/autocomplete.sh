#!/bin/bash

function _terminal_radio {
    local cur opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    opts="play update logs show"

    COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )   
}

complete -F _terminal_radio terminal_radio