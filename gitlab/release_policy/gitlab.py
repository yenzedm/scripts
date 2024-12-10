import requests
import sys
import json
import logging
import urllib3

 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCRIPTNAME = "release_policy_gitlab"
logger = logging.getLogger(SCRIPTNAME)
logger.setLevel(logging.DEBUG)
console_out = logging.StreamHandler()
strfmt = '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)
console_out.setFormatter(formatter)
logger.addHandler(console_out)

def main(GITLAB_URL, ACCESS_TOKEN, GROUP_NAME, PROJECT_NAME, SOURCE_BRANCH, TARGET_BRANCH):
    headers = {
        'PRIVATE-TOKEN': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    GET_PROJECT = requests.get(f'{GITLAB_URL}/api/v4/projects/{GROUP_NAME}%2f{PROJECT_NAME}', headers=headers, verify=False)
    data = json.loads(GET_PROJECT.content)
    PROJECT_ID = data['id']

    check_target_branch = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/repository/branches"

    response = requests.get(check_target_branch, headers=headers, verify=False)

    if response.status_code == 404:
        logger.error(f"39: can't get a list of branches {response.status_code}")
        sys.exit(1)
    else:
        tmp = json.loads(response.text)
        flag = True
        for branch in tmp:
            if branch['name'] == TARGET_BRANCH:
                flag = False
                break
        if flag:    
            logger.error(f"49: branch {TARGET_BRANCH} does not exist")
            sys.exit(1)
    if SOURCE_BRANCH == 'develop':
        logger.info(f'52: skip protected {SOURCE_BRANCH} branch')
        sys.exit(0)
    else:
        protected_branches = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/protected_branches"

        response = requests.get(protected_branches, headers=headers, verify=False)
        
        if response.status_code == 200 and 'build' in SOURCE_BRANCH and SOURCE_BRANCH in response.text:
            logger.info(f"61: branch {SOURCE_BRANCH} already protected and limited")
            sys.exit(0)

        elif SOURCE_BRANCH not in response.text:
            logger.info(f"66: add {SOURCE_BRANCH} in protected branches")
            payload = {
                "name": SOURCE_BRANCH,
                "push_access_level": 0,  
                "merge_access_level": 0,    
            }
            create_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/protected_branches"
            response = requests.post(create_url, headers=headers, json=payload, verify=False)

            if response.status_code == 201:
                logger.info(f'76: protected branch "{SOURCE_BRANCH}" created with no push/merge permissions.')
            else:
                logger.error(f"78: failed to protect branch. Status code: {response.status_code}, Response: {response.text}")


if __name__ == '__main__':
    GITLAB_URL = sys.argv[1] 
    ACCESS_TOKEN = sys.argv[2]
    GROUP_NAME = sys.argv[3]
    PROJECT_NAME = sys.argv[4]
    SOURCE_BRANCH = sys.argv[5]
    TARGET_BRANCH = sys.argv[6]

    main(GITLAB_URL, ACCESS_TOKEN, GROUP_NAME, PROJECT_NAME, SOURCE_BRANCH, TARGET_BRANCH)
