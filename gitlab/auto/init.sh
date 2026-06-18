#!/bin/bash

repo="$1"
group_id="$2"
token="$3"

json_data=$(jq -n \
  --arg name "$repo" \
  --arg desc "$repo" \
  --arg path "$repo" \
  --arg ns "$group_id" \
  '{name: $name, description: $desc, path: $path, namespace_id: ($ns | tonumber), initialize_with_readme: false}')

curl --request POST \
     --header "PRIVATE-TOKEN: $token" \
     --header "Content-Type: application/json" \
     --data "$json_data" \
     --url "http://192.168.1.124/api/v4/projects/"

cd $repo 
git init
git branch -m dev
git config --local user.name "Administrator"
git config --local user.email "gitlab_admin_e1b530@example.com"
git add .
git commit -m "init commit"
git remote add origin git@192.168.1.124:myappgroup/$repo.git
git push origin dev
