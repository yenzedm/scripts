#!/bin/bash

if ! command -v iostat >/dev/null 2>&1; then
    # command not found
    echo "Create tunnel..."
    ssh -i .ssh/test -o ConnectTimeout=5 -o StrictHostKeyChecking=accept-new -N -L 9999:mirror.yandex.ru:80 user@<server> -f
    echo "Create remote repo..."
    cat <<EOF> /etc/yum.repos.d/remote.repo
[remote]
name=RedOS - Base
baseurl=http://127.0.0.1:9999/redos/8.0/\$basearch/os
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-RED-SOFT
enabled=1
EOF
    echo "Install sysstat"
    yum install -y --disablerepo="*" --enablerepo=remote sysstat
    sleep 2
    echo "Delete remote repo..."
    rm -rf /etc/yum.repos.d/remote.repo
    echo "Close tunnel..."
    kill -9 $(ps aux | grep -E 'ssh.*(-L|-R|-D| -f | -N )' | grep <user> | awk '{print $2}')
else
    # command found
    echo "Command installed"
fi
