#!/bin/bash

LOG_FILE="/var/log/stuck_processes.log"
MAX_RUNTIME_MINUTES=1
MAX_RUNTIME_SECONDS=$((MAX_RUNTIME_MINUTES * 60))

# Ensure log file exists and is writable
touch "$LOG_FILE" || { echo "Cannot write to $LOG_FILE"; exit 1; }

echo "Search for processes older than $MAX_RUNTIME_MINUTES minutes... $(date)" | tee -a "$LOG_FILE"

# Get current timestamp
NOW=$(date +%s)

# Get processes with runtime
ps -eo pid,etimes,comm --no-headers | while read -r pid etimes comm; do
    # Skip if etimes is not a number
    if ! [[ "$etimes" =~ ^[0-9]+$ ]]; then
        continue
    fi
    
    if [ "$etimes" -gt "$MAX_RUNTIME_SECONDS" ]; then
        minutes=$((etimes / 60))
        seconds=$((etimes % 60))
        echo "PID: $pid | Time: ${minutes}m ${seconds}s | Command: $comm" | tee -a "$LOG_FILE"
    fi
done
