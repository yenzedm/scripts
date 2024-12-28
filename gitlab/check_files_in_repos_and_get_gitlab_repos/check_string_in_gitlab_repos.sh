#!/bin/bash

SEARCH_STRING=$1
TEMP_DIR="gitlab_repos"
BRANCH_NAME=$2

if [[ -z "$SEARCH_STRING" || -z "$BRANCH_NAME" ]]; then
    echo "Usage: $0 <gitlab_url> <private_token> <search_string> <branch_name>"
    exit 1
fi

# Create temp directory for repos
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR" || exit 1

# Get a list of repos through GitLab API
echo "Get the list of repos..."
repos=$(</home/eremeevda/rf_infra/templates/scripts_rf/gitlab/check_repo_urls.txt)

# Check a list is not empty
if [ -z "$repos" ]; then
    echo "Failed to get repositories. Check the token and URL."
    exit 1
fi

# Loop through the repositories and look for the line
for repo in $repos; do
    repo_name=$(basename "$repo" .git)
    
    # Clone repo
    echo "Clone repo $repo..."
    git clone -q -b "$BRANCH_NAME" "$repo" "$repo_name"
    
    # Go to the repo directory
    cd "$repo_name" || continue

    # Find the line in repo
    echo "Search string '$SEARCH_STRING' in repo $repo_name..."
    results=$(git grep -n "$SEARCH_STRING")

    if [ -n "$results" ]; then
        echo "Found in $repo_name:"
        echo "$results"
    else
        echo "Str not found in $repo_name."
    fi

    # Return back and delete the clone repo
    cd ..
    rm -rf "$repo_name"
done

# Delete temp directory
cd ..
rm -rf "$TEMP_DIR"