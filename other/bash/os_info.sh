#!/bin/bash
# Reset all variables that might be used by the system
# Clear terminal screen
clear

unset os architecture kernelrelease internalip externalip nameserver loadaverage

# Main monitoring functionality
if [[ $# -eq 0 ]]
then
{
    # Check Internet connection
    ping -c 1 google.com &> /dev/null && echo "Internet: Connected" || echo "Internet: Disconnected"

    # Get OS type
    os=$(uname -o)
    echo "Operating System Type : $os"

    # Get OS name and version
    cat /etc/os-release | grep 'NAME\|VERSION' | grep -v 'VERSION_ID' | grep -v 'PRETTY_NAME' > /tmp/osrelease
    echo -n "OS Name : " && cat /tmp/osrelease | grep -v "VERSION" | cut -f2 -d\"
    echo -n "OS Version : " && cat /tmp/osrelease | grep -v "NAME" | cut -f2 -d\"

    # Get system architecture
    architecture=$(uname -m)
    echo "Architecture : $architecture"

    # Get kernel release
    kernelrelease=$(uname -r)
    echo "Kernel Release : $kernelrelease"

    # Get hostname
    echo "Hostname : $HOSTNAME"

    # Get internal IPs with interfaces
    echo "Internal IPs:"
    ip -br addr show | awk '!/LOOPBACK/ && /UP/ {gsub(/\/.+/, "", $3); print $1 ": " $3}'

    # Get external IP address
    externalip=$(curl -s ifconfig.me ; echo)
    echo "External IP : $externalip"

    # Get DNS nameservers
    nameservers=$(grep -E '^nameserver' /etc/resolv.conf | awk '{print $2}' | tr '\n' ' ')
    echo "Name Servers : $nameservers"

    # Get logged in users
    who > /tmp/who
    echo "Logged In users : " && cat /tmp/who

    # Get CPU usage information
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8"% free"}')
    echo "CPU Usage : $cpu_usage"

    # Get RAM and swap usage
    free | grep Mem | awk '{printf "RAM Usage: %.1f%%\n", ($2 - $7) / $2 * 100.0}'
    free | grep Swap | awk '{printf "Swap Usage: %.1f%%\n", $3/$2 * 100.0}'

    echo "Disk Usages :"
    df -h | grep '^/dev/' | while read -r line; do
        cur_space=$(echo "$line" | awk '{print $(NF-1)}' | sed 's/%//')
        partition=$(echo "$line" | awk '{print $1}')
        echo "$partition: $cur_space% used"; done   

    # Get system load average
    loadaverage=$(top -n 1 -b | grep "load average:" | awk '{print $11 $12 $13}')
    echo "Load Average : $loadaverage"

    # Get system uptime
    tecuptime=$(uptime | awk '{print $3,$4}' | cut -f1 -d,)
    echo "System Uptime Days/(HH:MM) : $tecuptime"

    # Clean up variables
    unset os architecture kernelrelease internalip externalip nameserver loadaverage

    # Remove temporary files
    rm /tmp/osrelease /tmp/who /tmp/diskusage &> /dev/null
}
fi
shift $(($OPTIND -1))
