#!/bin/bash

GITLAB_URL=$1      
PRIVATE_TOKEN=$2

if [[ -z "$GITLAB_URL" || -z "$PRIVATE_TOKEN" ]]; then
    echo "Usage: $0 https://<gitlab_url> <private_token>"
    exit 1
fi

echo "" > all_gitlab_projects_urls.txt
for ((i=1; ; i+=1)); do
    contents=$(curl --insecure "$GITLAB_URL/api/v4/projects?private_token=$PRIVATE_TOKEN&per_page=100&page=$i")
    if jq -e '. | length == 0' >/dev/null; then 
       break
    fi <<< "$contents"
    echo "$contents" | jq -r '.[].ssh_url_to_repo' >> all_gitlab_projects_urls.txt
done
