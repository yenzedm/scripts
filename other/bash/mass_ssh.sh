#!/bin/bash

processing=false  # processing start flag

while IFS= read -r ip; do
    # If we encounter "start", we turn on processing from the next line
    if [[ "$ip" == "start" ]]; then
        processing=true
        continue
    fi
    
    # Skip comments and empty lines
    [[ -z "$ip" || "$ip" =~ ^# ]] && continue

    # If we encounter "stop", we exit the loop
    if [[ "$ip" == "stop" ]]; then
        break
    fi

    # If processing has not yet started, skip the line
    if ! $processing; then
        continue
    fi
    echo "------------------------------------------"
    echo "Collector: $ip"
    if [[ -f "$1" ]]; then
        # This looks like a file path → passed as stdin
        ssh -o ConnectTimeout=5 -o BatchMode=yes "$ip" bash < "$1"
    elif [[ " $* " =~ " --scp " ]]; then
        what=$2
        where=$3
        scp $2 "$ip:$where"
        echo "File $what copied in $where"
    else
        # think this is a command
        ssh -n -o ConnectTimeout=5 -o BatchMode=yes "$ip" "$1"
    fi
    echo "------------------------------------------"
done < "${@: -1}"

######## use script ######
# ./mass_ssh.sh "<command>" <file with server's names from .ssh/config>
# ./mass_ssh.sh ./you-script.sh <file with server's names from .ssh/config>
# ./mass_ssh.sh --scp <wha>t <where> <file with server's names from .ssh/config>
