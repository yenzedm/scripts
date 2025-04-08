#!/bin/bash

# Operating systems on which the script ran:
# red os, ubuntu 24

sudo gitlab-runner stop
sudo gitlab-runner uninstall
sudo rm -f /usr/local/sbin/gitlab-runner
sudo userdel -r gitlab-runner
sudo rm -rf /etc/gitlab-runner
sudo rm -rf /home/gitlab-runner
sudo rm -rf /var/log/gitlab-runner
sudo rm -rf /var/lib/gitrab-runner

echo "GitLab Runner has been successfully removed."
