#!/bin/bash
# Reset all variables that might be used by the system
# Clear terminal screen
clear

unset tecreset os architecture kernelrelease internalip externalip nameserver loadaverage

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
    echo -e "System Monitor Script v1.1"
}
fi

# Main monitoring functionality when no options are provided
if [[ $# -eq 0 ]]
then
{
    # Define color reset variable
    tecreset=$(tput sgr0)

    # Check Internet connection
    ping -c 1 google.com &> /dev/null && echo -e '\E[32m'"Internet: $tecreset Connected" || echo -e '\E[32m'"Internet: $tecreset Disconnected"

    # Get OS type
    os=$(uname -o)
    echo -e '\E[32m'"Operating System Type :" $tecreset $os

    # Get OS name and version
    cat /etc/os-release | grep 'NAME\|VERSION' | grep -v 'VERSION_ID' | grep -v 'PRETTY_NAME' > /tmp/osrelease
    echo -n -e '\E[32m'"OS Name :" $tecreset && cat /tmp/osrelease | grep -v "VERSION" | cut -f2 -d\"
    echo -n -e '\E[32m'"OS Version :" $tecreset && cat /tmp/osrelease | grep -v "NAME" | cut -f2 -d\"

    # Get system architecture
    architecture=$(uname -m)
    echo -e '\E[32m'"Architecture :" $tecreset $architecture

    # Get kernel release
    kernelrelease=$(uname -r)
    echo -e '\E[32m'"Kernel Release :" $tecreset $kernelrelease

    # Get hostname
    echo -e '\E[32m'"Hostname :" $tecreset $HOSTNAME

    # Get internal IP address
    internalip=$(hostname -I)
    echo -e '\E[32m'"Internal IP :" $tecreset $internalip

    # Get external IP address
    externalip=$(curl -s ipecho.net/plain;echo)
    echo -e '\E[32m'"External IP : $tecreset "$externalip

    # Get DNS nameservers (properly filtered)
    nameservers=$(grep -E '^nameserver' /etc/resolv.conf | awk '{print $2}' | tr '\n' ' ')
    echo -e '\E[32m'"Name Servers :" $tecreset $nameservers

    # Get logged in users
    who > /tmp/who
    echo -e '\E[32m'"Logged In users :" $tecreset && cat /tmp/who

    # Get CPU usage information (added feature)
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8"% free"}')
    echo -e '\E[32m'"CPU Usage :" $tecreset $cpu_usage

    # Get RAM and swap usage
    free -h | grep -v + > /tmp/ramcache
    echo -e '\E[32m'"Ram Usages :" $tecreset
    cat /tmp/ramcache | grep -v "Swap"
    echo -e '\E[32m'"Swap Usages :" $tecreset
    cat /tmp/ramcache | grep -v "Mem"

    # Get disk usage information
    df -h| grep 'Filesystem\|/dev/sd*' > /tmp/diskusage
    echo -e '\E[32m'"Disk Usages :" $tecreset
    cat /tmp/diskusage

    # Get system load average
    loadaverage=$(top -n 1 -b | grep "load average:" | awk '{print $10 $11 $12}')
    echo -e '\E[32m'"Load Average :" $tecreset $loadaverage

    # Get system uptime
    tecuptime=$(uptime | awk '{print $3,$4}' | cut -f1 -d,)
    echo -e '\E[32m'"System Uptime Days/(HH:MM) :" $tecreset $tecuptime

    # Clean up variables
    unset tecreset os architecture kernelrelease internalip externalip nameserver loadaverage

    # Remove temporary files
    rm /tmp/osrelease /tmp/who /tmp/ramcache /tmp/diskusage &> /dev/null
}
fi
shift $(($OPTIND -1))