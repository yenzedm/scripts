import requests
import sys
import json
import logging
import urllib3

  
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCRIPTNAME = "gitlab.py"
logger = logging.getLogger(SCRIPTNAME)
logger.setLevel(logging.DEBUG)
console_out = logging.StreamHandler()
strfmt = '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)
console_out.setFormatter(formatter)
logger.addHandler(console_out)

def main(gitlab_url, access_token, group_name, project_name, source_branch, target_branch):
    headers = {
        'PRIVATE-TOKEN': access_token,
        'Content-Type': 'application/json'
    }

    GET_PROJECT = requests.get(f'{gitlab_url}/api/v4/projects/{group_name}%2f{project_name}', headers=headers, verify=False)
    data = json.loads(GET_PROJECT.content)
    PROJECT_ID = data['id']

    check_target_branch = f"{gitlab_url}/api/v4/projects/{PROJECT_ID}/repository/branches"

    response = requests.get(check_target_branch, headers=headers, verify=False)

    if response.status_code == 404:
        logger.error(f"39: can't get a list of branches {response.status_code}")
        sys.exit(1)
    else:
        tmp = json.loads(response.text)
        flag = True
        for branch in tmp:
            if branch['name'] == target_branch:
                flag = False
                break
        if flag:    
            logger.error(f"49: branch {target_branch} does not exist")
            sys.exit(1)
    if 'develop' in source_branch and 'build' not in target_branch and 'hotfix' not in target_branch and 'rc' not in target_branch:
        protected_branches = f"{gitlab_url}/api/v4/projects/{PROJECT_ID}/protected_branches"

        response = requests.get(protected_branches, headers=headers, verify=False)

        if target_branch not in response.text:
            logger.info(f"59: add {target_branch} in protected branches")
            payload = {
                "name": target_branch,
                "push_access_level": 0,  
                "merge_access_level": 0,    
            }
            create_url = f"{gitlab_url}/api/v4/projects/{PROJECT_ID}/protected_branches"
            response = requests.post(create_url, headers=headers, json=payload, verify=False)

            if response.status_code == 201:
                logger.info(f'69: protected branch "{target_branch}" created with no push/merge permissions.')
            else:
                logger.error(f"71: failed to protect branch. Status code: {response.status_code}, Response: {response.text}")
    elif source_branch == 'develop':
        logger.info(f'73: skip protected {source_branch} branch')
        sys.exit(0)
    else:
        protected_branches = f"{gitlab_url}/api/v4/projects/{PROJECT_ID}/protected_branches"

        response = requests.get(protected_branches, headers=headers, verify=False)

        if source_branch not in response.text:
            logger.info(f"87: add {source_branch} in protected branches")
            payload = {
                "name": source_branch,
                "push_access_level": 0,  
                "merge_access_level": 0,    
            }
            create_url = f"{gitlab_url}/api/v4/projects/{PROJECT_ID}/protected_branches"
            response = requests.post(create_url, headers=headers, json=payload, verify=False)

            if response.status_code == 201:
                logger.info(f'97: protected branch "{source_branch}" created with no push/merge permissions.')
            else:
                logger.error(f"99: failed to protect branch. Status code: {response.status_code}, Response: {response.text}")


if __name__ == '__main__':
    gitlab_url = sys.argv[1]
    access_token = sys.argv[2]
    group_name = sys.argv[3]
    project_name = sys.argv[4]
    source_branch = sys.argv[5]
    target_branch = sys.argv[6]

    main(gitlab_url, access_token, group_name, project_name, source_branch, target_branch)
