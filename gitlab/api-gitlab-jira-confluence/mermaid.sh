#!/bin/bash

username=$1
password=$2
source_branch=$3
target_branch=$4
gitlab_url=$5
group_name=$6
project_name=$7
access_token=$8
workspace=$9

if python3 $workspace/check_page_exist.py "$username" "$password" "$target_branch"; then
    python3 $workspace/update_gitgraph.py "$username" "$password" "$source_branch" "$target_branch" "$gitlab_url" "$group_name" "$project_name" "$access_token"
    mmdc -i diagram.mmd -o diagram.svg
    python3 $workspace/confluence_page_exist.py "$username" "$password" "$target_branch"
    python3 $workspace/jira_project_releases.py "$username" "$password" "$source_branch" "$target_branch"
    python3 $workspace/create-history-task.py "$username" "$password" "$target_branch"
else
    python3 $workspace/create_gitgraph.py "$access_token" "$target_branch" "$gitlab_url" "$group_name" "$project_name"
    mmdc -i diagram.mmd -o diagram.svg
    python3 $workspace/confluence_page_not_exist.py "$username" "$password" "$target_branch"
    python3 $workspace/jira_project_releases.py "$username" "$password" "$source_branch" "$target_branch"
    python3 $workspace/create-history-task.py "$username" "$password" "$target_branch"
fi
