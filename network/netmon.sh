#!/bin/bash

INTERFACE="eth0"
INTERVAL=1

echo "🔍 Monitoring network interface: $INTERFACE"
echo "Enter Ctrl+C for exit."
echo

while true; do
    RX1=$(cat /sys/class/net/$INTERFACE/statistics/rx_bytes)
    TX1=$(cat /sys/class/net/$INTERFACE/statistics/tx_bytes)
    sleep $INTERVAL
    RX2=$(cat /sys/class/net/$INTERFACE/statistics/rx_bytes)
    TX2=$(cat /sys/class/net/$INTERFACE/statistics/tx_bytes)

    RX_RATE=$(( (RX2 - RX1) / INTERVAL / 1024 ))
    TX_RATE=$(( (TX2 - TX1) / INTERVAL / 1024 ))

    echo "⬇️ IN: ${RX_RATE} KB/s | ⬆️ OUT: ${TX_RATE} KB/s"
done

# IN — (download) in KB/s.
# OUT —(upload) in KB/s.
