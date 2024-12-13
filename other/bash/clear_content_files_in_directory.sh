#!/bin/bash

directory="$1"

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
