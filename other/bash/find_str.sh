#!/bin/bash

DIRECTORY=$1
SEARCH_STRING=$2

if [ "$1" == "--help" ]; then
    echo "This script clears all contents in the files of a specified directory"
    echo "Usage: $0 <directory>"
    exit 1
fi

if [[ -z "$DIRECTORY" || -z "$SEARCH_STRING" ]]; then
    echo "Usage: $0 <directory> <search_string>"
    exit 1
fi

find "$DIRECTORY" -type f | while read -r FILE; do
    if grep -q "$SEARCH_STRING" "$FILE"; then
        echo "String is found in: $FILE"
    fi
done