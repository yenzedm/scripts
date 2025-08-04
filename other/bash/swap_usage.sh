#!/bin/bash
for file in /proc/[0-9]*/status; do
    name=$(awk '/^Name:/ {print $2}' "$file")
    pid=$(basename "$(dirname "$file")")
    swap=$(awk '/^VmSwap:/ {print $2}' "$file")
    [ -n "$swap" ] && echo "$pid $name $(echo "$swap" | awk '{print $1 / 1024 " Mb"}')"
done | sort -k 3 -n -r | head -n 20
