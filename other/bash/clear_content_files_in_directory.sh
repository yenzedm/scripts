#!/bin/bash

log_directory="$1"

if [ -d "$log_directory" ]; then
    for file in "$log_directory"/*; do
        if [ -f "$file" ]; then 
            > "$file"
            echo "cleared: $file"
        fi
    done
else
    echo "directory $log_directory not found."
fi
