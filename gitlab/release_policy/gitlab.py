import requests
import sys
import json
import logging


#Logger initialization
SCRIPTNAME = "release_policy_gitlab"
logger = logging.getLogger(SCRIPTNAME) # Initialize and declare logger name
logger.setLevel(logging.DEBUG) # Set logging level
console_out = logging.StreamHandler() # Attach log handler to stdout
strfmt = '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s' # Define log message format for better readability
datefmt = '%Y-%m-%d %H:%M:%S' # Define date and time format in logs
formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt) # Create formatter with the defined formats
console_out.setFormatter(formatter) # Apply formatting to the log output
logger.addHandler(console_out) # Enable log output handler

def main(GITLAB_URL, ACCESS_TOKEN, GROUP_NAME, PROJECT_NAME, SOURCE_BRANCH, TARGET_BRANCH):
    # Set authorization headers
    headers = {
        'PRIVATE-TOKEN': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    GET_PROJECT = requests.get(f'{GITLAB_URL}/api/v4/projects/{GROUP_NAME}%2f{PROJECT_NAME}', headers=headers, verify=False)
    data = json.loads(GET_PROJECT.content)
    PROJECT_ID = data['id']

    check_target_branch = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/repository/branches?branch={TARGET_BRANCH}"

    # Check if the TARGET_BRANCH exists
    response = requests.get(check_target_branch, headers=headers, verify=False)

    if response.status_code == 404:
        logger.error(f"35: Branch {TARGET_BRANCH} does not exist")
        sys.exit(1)

    # Transfer to protected_branch both branches
    if 'rc' in SOURCE_BRANCH and 'build' in TARGET_BRANCH:
        #Get a list of all protected branches
        protected_branches = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/protected_branches"

        response = requests.get(protected_branches, headers=headers, verify=False)

        if SOURCE_BRANCH not in response.text:
            # The branch is not protected, create a new protected branch with restrictions
            logger.info(f"47: Add {SOURCE_BRANCH} in protected branches")
            payload = {
                "name": SOURCE_BRANCH,
                "push_access_level": 0,  
                "merge_access_level": 0,    
            }
            create_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/protected_branches"
            response = requests.post(create_url, headers=headers, json=payload, verify=False)

            if response.status_code == 201:
                logger.info(f'57: Protected branch "{SOURCE_BRANCH}" created with no push/merge permissions.')
            else:
                logger.error(f"59: Failed to protect branch. Status code: {response.status_code}, Response: {response.text}")
        else:
            logger.info(f"61: Branch {SOURCE_BRANCH} is protected")
            sys.exit(0)

        if TARGET_BRANCH not in response.text:
            # The branch is not protected, create a new protected branch with restrictions
            logger.info(f"66: Add {TARGET_BRANCH} in protected branches")
            payload = {
                "name": TARGET_BRANCH,
                "push_access_level": 0,  
                "merge_access_level": 0,    
            }
            create_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/protected_branches"
            response = requests.post(create_url, headers=headers, json=payload, verify=False)

            if response.status_code == 201:
                logger.info(f'76: Protected branch "{TARGET_BRANCH}" created with no push/merge permissions.')
            else:
                logger.error(f"78: Failed to protect branch. Status code: {response.status_code}, Response: {response.text}")
        else:
            logger.info(f"80: Branch {TARGET_BRANCH} is protected")
            sys.exit(0)
    elif SOURCE_BRANCH == 'develop':
        logger.info(f'83: Skip protected {SOURCE_BRANCH} branch')
        sys.exit(0)
    else:
        protected_branches = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/protected_branches"

        # Get a list of all protected branches
        response = requests.get(protected_branches, headers=headers, verify=False)
        
        if response.status_code == 200 and 'build' in SOURCE_BRANCH and SOURCE_BRANCH in response.text:
            logger.info(f"92: Branch {SOURCE_BRANCH} already protected and limited")
            sys.exit(0)

        elif SOURCE_BRANCH not in response.text:
            # The branch is not protocted, create a new protected branch with restrictions
            logger.info(f"97: Add {SOURCE_BRANCH} in protected branches")
            payload = {
                "name": SOURCE_BRANCH,
                "push_access_level": 0,  
                "merge_access_level": 0,    
            }
            create_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/protected_branches"
            response = requests.post(create_url, headers=headers, json=payload, verify=False)

            if response.status_code == 201:
                logger.info(f'107: Protected branch "{SOURCE_BRANCH}" created with no push/merge permissions.')
            else:
                logger.error(f"109: Failed to protect branch. Status code: {response.status_code}, Response: {response.text}")


if __name__ == '__main__':
    GITLAB_URL = sys.argv[1] 
    ACCESS_TOKEN = sys.argv[2]
    GROUP_NAME = sys.argv[3]
    PROJECT_NAME = sys.argv[4]
    SOURCE_BRANCH = sys.argv[5]
    TARGET_BRANCH = sys.argv[6]

    main(GITLAB_URL, ACCESS_TOKEN, GROUP_NAME, PROJECT_NAME, SOURCE_BRANCH, TARGET_BRANCH)
