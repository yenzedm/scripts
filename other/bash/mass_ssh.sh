while IFS= read -r ip; do
    echo "Collector: $ip"
    ssh -n -o ConnectTimeout=5 -o BatchMode=yes "$ip" "$1"
done < $2


######## chrony ##########
# use: ./mass_ssh "<command>" <path/to/file>
# path/to/file must contain IP addresses. 1 ip address 1 line
#
# all
# ls -ld /etc/chrony.conf
# sed -i 's|server|#server|g' /etc/chrony.conf
# sed -i '1i server 10.10.10.10 iburst' /etc/chrony.conf
# systemctl restart chronyd.service
# chronyc sources -v
# grep server /etc/chrony.conf
# localectl set-locale LANG=ru_RU.UTF-8
# source /etc/locale.conf

########################
