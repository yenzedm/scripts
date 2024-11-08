#!/bin/bash

DIRECTORY=$1 
SEARCH_STRING=$2
for FILE in "$DIRECTORY"/*; do 
    if [[ -f "$FILE" ]]; then 
        if grep -q "$SEARCH_STRING" "$FILE"; then
            echo "string is found: $FILE" 
	fi
    fi
done
