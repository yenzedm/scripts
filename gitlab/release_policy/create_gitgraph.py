import sys
import urllib3
import logging
import requests
import json
import re

  
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCRIPTNAME = "create_gitgraph.py"
logger = logging.getLogger(SCRIPTNAME)
logger.setLevel(logging.DEBUG)
console_out = logging.StreamHandler()
strfmt = '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)
console_out.setFormatter(formatter)
logger.addHandler(console_out)

def create_gitgraph(target_branch, access_token, gitlab_url, group_name, project_name, target_version):
    headers = {
        'PRIVATE-TOKEN': access_token,
        'Content-Type': 'application/json'
    }

    get_project = f'{gitlab_url}/api/v4/projects/{group_name}%2f{project_name}'
    response = requests.get(get_project, headers=headers, verify=False)
    if '404' in response.text:
        logger.error(f"27: {response.text}")
        sys.exit(1)

    data = json.loads(response.content)
    project_id = data['id']

    get_events = f"{gitlab_url}/api/v4/projects/{project_id}/events"
    response = requests.get(get_events, headers=headers, verify=False)
    if '"error":"404 Not Found' in response.text:
        logger.error(f"38: {response.text}")
        sys.exit(1)

    tmp = json.loads(response.text)
    for event in tmp:
        if event['push_data']['ref'] == f'{target_branch}' and event['push_data']['action'] == 'created' and event['push_data']['commit_count'] == 0:
            target_date_and_time = event['created_at']
            break

    with open('diagram.mmd', 'w') as file:
        file.write(f'gitGraph:\ncommit\nbranch develop\ncheckout develop\ncommit tag:"Начало сборки Build {target_version}"\nbranch {target_branch}\ncheckout {target_branch}\ncommit tag:"Отладка {target_version}" type: HIGHLIGHT id:"{target_date_and_time}"')


if __name__ == '__main__':
    access_token = sys.argv[1]
    target_branch = sys.argv[2]
    gitlab_url = sys.argv[3]
    group_name = sys.argv[4]
    project_name = sys.argv[5]

    pattern = r"\d+\.\d+\.\d+.\d+"
    target_match = re.search(pattern, target_branch)
    target_version = target_match.group(0)

    create_gitgraph(target_branch=target_branch, access_token=access_token, gitlab_url=gitlab_url, group_name=group_name, project_name=project_name, target_version=target_version)
