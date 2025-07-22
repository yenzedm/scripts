#!/bin/bash
# Reset all variables that might be used by the system
# Clear terminal screen
clear

unset os architecture kernelrelease internalip externalip nameserver loadaverage

# Process command line options
while getopts iv name
do
    case $name in
        i) iopt=1;;  # Installation flag
        v) vopt=1;;  # Version flag
        *) echo "Invalid argument";;
    esac
done

# Install script to /usr/bin if -i option is set
if [[ ! -z $iopt ]]
then
{
    wd=$(pwd)
    basename "$(test -L "$0" && readlink "$0" || echo "$0")" > /tmp/scriptname
    scriptname=$(echo -e -n $wd/ && cat /tmp/scriptname)
    su -c "cp $scriptname /usr/bin/monitor" root && echo "Congratulations! Script Installed, now run monitor Command" || echo "Installation failed"
}
fi

# Show version if -v option is set
if [[ ! -z $vopt ]]
then
{
    echo "System Monitor Script v1.1"
}
fi

# Main monitoring functionality when no options are provided
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

    # Get internal IP address
    internalip=$(hostname -I)
    echo "Internal IP : $internalip"

    # Get external IP address
    externalip=$(curl -s ipecho.net/plain;echo)
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
    free -h | grep -v + > /tmp/ramcache
    echo "Ram Usages :"
    cat /tmp/ramcache | grep -v "Swap"
    echo "Swap Usages :"
    cat /tmp/ramcache | grep -v "Mem"

    # Get disk usage information
    df -h| grep 'Filesystem\|/dev/sd*' > /tmp/diskusage
    echo "Disk Usages :"
    cat /tmp/diskusage

    # Get system load average
    loadaverage=$(top -n 1 -b | grep "load average:" | awk '{print $10 $11 $12}')
    echo "Load Average : $loadaverage"

    # Get system uptime
    tecuptime=$(uptime | awk '{print $3,$4}' | cut -f1 -d,)
    echo "System Uptime Days/(HH:MM) : $tecuptime"

    # Clean up variables
    unset os architecture kernelrelease internalip externalip nameserver loadaverage

    # Remove temporary files
    rm /tmp/osrelease /tmp/who /tmp/ramcache /tmp/diskusage &> /dev/null
}
fi
shift $(($OPTIND -1))
