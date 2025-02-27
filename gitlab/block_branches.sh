#!/bin/bash

# can use with scripts/other/python/add_quotes.py

project_group=$1 
source_branch=$2
target_branch=$3
gitlab_token=$4

# project_group for this list is test-group1
test1_list=("project1" "project2")

# project_group for this list is test-group2
test2_list=("project1" "project2")


if [[ project_group == "test-group1"]]; then
    tmp=$test1_list
elif [[ project_group == "test-group2"]]; then
    tmp=$test2_list
else
    echo "Wrong project group $project_group! Should be 'KBS' or 'rf-general' or 'RF'"
    exit 1

for item in "${tmp[@]}"; do
    echo "$item"
    python3 gitlab.py https://gitlab.hq.lan $gitlab_token $project_group $item $source_branch $target_branch
done
