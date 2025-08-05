#!/bin/bash
# Reset all variables that might be used by the system
# Clear terminal screen
clear

unset os architecture kernelrelease externalip loadaverage

# Main monitoring functionality
if [[ $# -eq 0 ]]
then
{
    # Check Internet connection
    ping -c 1 google.com &> /dev/null && echo "Internet: Connected" || echo "Internet: Disconnected"

    echo "====================================="

    # Get OS type
    os=$(uname -o)
    echo "Operating System Type : $os"

    echo "====================================="

    # Get OS name and version
    cat /etc/os-release | grep 'NAME\|VERSION' | grep -v 'VERSION_ID' | grep -v 'PRETTY_NAME' > /tmp/osrelease
    echo -n "OS Name : " && cat /tmp/osrelease | grep -v "VERSION" | cut -f2 -d\"
    echo -n "OS Version : " && cat /tmp/osrelease | grep -v "NAME" | cut -f2 -d\"

    echo "====================================="

    # Get system architecture
    architecture=$(uname -m)
    echo "Architecture : $architecture"

    echo "====================================="

    # Get kernel release
    kernelrelease=$(uname -r)
    echo "Kernel Release : $kernelrelease"

    echo "====================================="

    # Get hostname
    echo "Hostname : $HOSTNAME"

    echo "====================================="

    # Get internal IPs with interfaces
    echo "Internal IPs:"
    ip -br addr show | awk '!/LOOPBACK/ && /UP/ {gsub(/\/.+/, "", $3); print $1 ": " $3}'

    echo "====================================="

    # Get external IP address
    externalip=$(curl -s ifconfig.me ; echo)
    echo "External IP : $externalip"

    echo "====================================="

    # Get DNS nameservers
    echo "Name Servers:"
    (resolvectl status 2>/dev/null || systemd-resolve --status 2>/dev/null || cat /etc/resolv.conf) | grep -E "DNS Servers|nameserver" | awk '{print $0}' | sed 's/^[ \t]*//'

    echo "====================================="

    # Get logged in users
    who > /tmp/who
    echo "Logged In users : " && cat /tmp/who

    echo "====================================="

    #CPU info
    echo "CPU INFO:"
    echo "$(grep "model name" /proc/cpuinfo | head -n 1 | cut -d ':' -f 2 | sed 's/^[ \t]*//')" && echo "Cores: $(grep "cpu cores" /proc/cpuinfo | head -n 1 | cut -d ':' -f 2 | sed 's/^[ \t]*//')" && echo "Threads: $(grep -c "^processor" /proc/cpuinfo)" && echo "Cache: $(grep "cache size" /proc/cpuinfo | head -n 1 | cut -d ':' -f 2 | sed 's/^[ \t]*//')" && echo "Flags: $(grep "flags" /proc/cpuinfo | head -n 1 | cut -d ':' -f 2 | sed 's/^[ \t]*//' | tr ' ' '\n' | tr '\n' ' ')"

    echo "====================================="

    # Get CPU usage information
    vmstat 1 2 | tail -1 | awk '{printf "CPU Usage: %.1f%%\n", 100 - $15}'

    echo "====================================="

    #top processes using CPU
    echo "top processes using CPU:"
    top -b -n 1 -o %CPU | head -n 18 | tail -n +7

    echo "====================================="

    # Get total RAM
    free -h | awk '/^Mem:/ {print "Total RAM: "$2}'

    echo "====================================="

    # Get RAM usage
    free | grep Mem | awk '{printf "RAM Usage: %.1f%%\n", ($2 - $7) / $2 * 100.0}'

    echo "====================================="

    # Top processes using RAM
    echo "top processes using RAM:"
    top -b -n 1 -o %MEM | head -n 18 | tail -n +7

    echo "====================================="
    
    # Get SWAP usage
    free | grep Swap | awk '{if ($2 == 0) print "Swap is disabled"; else printf "Swap Usage: %.1f%%\n", $3/$2 * 100.0}'

    echo "====================================="

    # Top processes using SWAP
    echo "top processes using SWAP:"
    for file in /proc/[0-9]*/status; do
        name=$(awk '/^Name:/ {print $2}' "$file")
        pid=$(basename "$(dirname "$file")")
        swap=$(awk '/^VmSwap:/ {print $2}' "$file")
        [ -n "$swap" ] && echo "$pid $name $(echo "$swap" | awk '{print $1 / 1024 " Mb"}')"
    done | sort -k 3 -n -r | head -n 20 

    echo "====================================="

    #Get disks info
    echo "Disk Usages :"
    df -h | grep '^/dev/' | while read -r line; do
        cur_space=$(echo "$line" | awk '{print $(NF-1)}' | sed 's/%//')
        partition=$(echo "$line" | awk '{print $1}')
        echo "$partition: $cur_space% used"; done   

    echo "====================================="

    # Get system load average
    loadaverage=$(top -n 1 -b | grep "load average:" | awk '{print $(NF-2) $(NF-1) $NF}')
    echo "Load Average : $loadaverage"

    echo "====================================="

    # Get system uptime
    tecuptime=$(uptime | awk '{print $3,$4}' | cut -f1 -d,)
    echo "System Uptime Days/(HH:MM) : $tecuptime"

    # Clean up variables
    unset os architecture kernelrelease internalip externalip nameserver loadaverage
 
    # Remove temporary files
    rm /tmp/osrelease /tmp/who &> /dev/null
}
fi
