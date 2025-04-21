#!/bin/bash

bashdays_box() {
    local headertext="$1"
    local message="$2"

    local white=$'\e[38;5;007m'
    local reset=$'\e[0m'
    local color

    case "$headertext" in
        INFO)  color=$'\e[38;5;39m' ;;
        OK)    color=$'\e[38;5;34m' ;;
        DONE)  color=$'\e[38;5;34m' ;;
        WARN)  color=$'\e[38;5;214m' ;;
        ERROR) color=$'\e[38;5;196m' ;;
        DEBUG) color=$'\e[38;5;244m' ;;
        TASK)  color=$'\e[38;5;141m' ;;
        NOTE)  color=$'\e[38;5;45m' ;;
        *)     color=$'\e[38;5;244m' ;;
    esac

    local headerpadding=$(( ${#message} - ${#headertext} ))
    local header=${message:0:headerpadding}

    echo -e "\n${color}╭ ${headertext} ${header//?/─}────╮" \
        "\n│   ${message//?/ }   │" \
        "\n│   ${white}${message}${color}   │" \
        "\n│   ${message//?/ }   │" \
        "\n╰──${message//?/─}────╯${reset}"
}

bashdays_box "$1" "$2"
