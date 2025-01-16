#!/bin/bash

directory="$1"

if [ "$1" == "--help" ]; then
    echo "This script clears all contents in the files of a specified directory"
    echo "Usage: $0 <directory>"
    exit 1
fi

if [[ -z "$directory" ]]; then
    echo "This script clears all contents in the files of a specified directory"
    echo "Usage: $0 <directory>"
    exit 1
fi

if [ -d "$directory" ]; then
    for file in "$directory"/*; do
        if [ -f "$file" ]; then 
            > "$file"
            echo "cleared: $file"
        fi
    done
else
    echo "directory $directory not found."
fi
