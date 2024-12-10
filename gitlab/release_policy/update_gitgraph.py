from atlassian import Confluence
import sys
import urllib3
import logging
import requests
import json
import re
from time import sleep
import os.path

  
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCRIPTNAME = "update_gitgraph.py"
logger = logging.getLogger(SCRIPTNAME)
logger.setLevel(logging.DEBUG)
console_out = logging.StreamHandler()
strfmt = '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)
console_out.setFormatter(formatter)
logger.addHandler(console_out)

def connect_to_confluence(username, password):
    try:
        _confluence = Confluence(
            url='https://confluence.eosan.ru',
            username=username,
            password=password)
        return _confluence
    except:
        logger.error('29: confluence connect error')
        return None

def download_diagram(confluence, space_key, target_version):
    pattern = r"\d+\.\d+\.\d+"
    target_match = re.search(pattern, target_version)
    page_version = target_match.group(0)
    page_name = f'Mermaid {page_version}'
    page_id = confluence.get_page_id(space_key, page_name)
    confluence.download_attachments_from_page(page_id)
    if os.path.exists('diagram.mmd'):
        logger.info('download diagram.mmd is successful')
        return True
    else:
        logger.error('46: something wrong with downloading')
        return False

def upload_diagram(confluence, space_key, target_version):
    pattern = r"\d+\.\d+\.\d+"
    target_match = re.search(pattern, target_version)
    page_version = target_match.group(0)
    page_name = f'Mermaid {page_version}'
    page_id = confluence.get_page_id(space_key, page_name)
    confluence.attach_file('diagram.mmd', page_id=page_id, space=space_key)

def main(username, password, source_branch, target_branch, gitlab_url, group_name, project_name, access_token, space_key, parent_page_name, target_version):
    headers = {
        'PRIVATE-TOKEN': access_token,
        'Content-Type': 'application/json'
    }

    GET_PROJECT = requests.get(f'{gitlab_url}/api/v4/projects/{group_name}%2f{project_name}', headers=headers, verify=False)
    data = json.loads(GET_PROJECT.content)
    PROJECT_ID = data['id']

    get_events = f"{gitlab_url}/api/v4/projects/{PROJECT_ID}/events"
    response = requests.get(get_events, headers=headers, verify=False)

    tmp = json.loads(response.text)
    try:
        if source_branch != 'develop':
            for event in tmp:
                if event['push_data']['ref'] == f'{source_branch}' and event['push_data']['action'] == 'created' and event['push_data']['commit_count'] == 0:
                    source_date_and_time = event['created_at']
                    break
        else:
            source_date_and_time = None
    except:
        source_date_and_time = ''
        logger.warning(f"104: Date of created source branch is not found")
        pass

    try:
        for event in tmp:
            if event['push_data']['ref'] == f'{target_branch}' and event['push_data']['action'] == 'created' and event['push_data']['commit_count'] == 0:
                target_date_and_time = event['created_at']
                break
    except:
        target_date_and_time = ''
        logger.warning(f"113: Date of created target branch is not found")
        pass
    
    if 'rc' in source_branch and 'rc' in target_branch:
        with open('diagram.mmd', 'r') as file:
            tmp = file.read()
            old_lines = fr'commit.*{target_version}.*Z"'
            new_lines = f'''commit tag:"Отладка" type: REVERSE id:"{source_date_and_time}"\nbranch {target_branch}\ncheckout {target_branch}\ncommit tag:"Отладка {target_version}" type: HIGHLIGHT id:"{target_date_and_time}"'''

            updated_file = re.sub(old_lines, new_lines, tmp, flags=re.VERBOSE)
            sleep(3)
            with open('diagram.mmd', 'w+') as file:
                file.write(updated_file)
            
    elif 'rc' in source_branch and 'build' in target_branch:
        with open('diagram.mmd', 'r+') as file:
            tmp = file.read()

            old_lines = fr'commit.*{target_version}.*Z"'
            new_lines = f'''commit tag:"Отладка" type: REVERSE id:"{source_date_and_time}"\nbranch {target_branch}\ncheckout {target_branch}\ncommit tag:"Выдача {target_version}" type: HIGHLIGHT id:"{target_date_and_time}"'''

            updated_file = re.sub(old_lines, new_lines, tmp, flags=re.VERBOSE)
            sleep(3)
            with open('diagram.mmd', 'w+') as file:
                file.write(updated_file)

    elif 'build' in source_branch and 'hotfix' in target_branch or 'hotfix' in source_branch and 'hotfix' in target_branch:
        with open('diagram.mmd', 'r+') as file:
            tmp = file.read()
            old_lines = fr'commit.*{target_version}.*Z"'
            new_lines = f'''commit tag:"Выдача" type: REVERSE id:"{source_date_and_time}"\nbranch {target_branch}\ncheckout {target_branch}\ncommit tag:"BugFix {target_version}" type: HIGHLIGHT id:"{target_date_and_time}"'''

            updated_file = re.sub(old_lines, new_lines, tmp, flags=re.VERBOSE)
            sleep(3)
            with open('diagram.mmd', 'w+') as file:
                file.write(updated_file)
    else:
        with open('diagram.mmd', 'r+') as file:
            tmp = file.read()
            old_lines = fr'commit.*BugFix.*Z"'
            tmp1 = re.search(old_lines, tmp)
            new_lines = f'''{tmp1.group(0)}\ncheckout {source_branch}\ncommit tag:"Начало сборки Build {target_version}"\nbranch {target_branch}\ncheckout {target_branch}\ncommit tag:"Отладка {target_version}" type: HIGHLIGHT id:"{target_date_and_time}"'''
            updated_file = re.sub(old_lines, new_lines, tmp, flags=re.VERBOSE)
            sleep(3)
            with open('diagram.mmd', 'w+') as file:
                file.write(updated_file)

if __name__ == '__main__':
    username = sys.argv[1]
    password = sys.argv[2]
    source_branch = sys.argv[3]
    target_branch = sys.argv[4]
    gitlab_url = sys.argv[5]
    group_name = sys.argv[6]
    project_name = sys.argv[7]
    access_token = sys.argv[8]
    space_key = 'recfaces'
    parent_page_name = '70.01.10.87 - Mermaid'


    pattern = r"\d+\.\d+\.\d+.\d+"
    target_match = re.search(pattern, target_branch)
    source_match = re.search(pattern, source_branch)
    target_version = target_match.group(0)

    confluence = connect_to_confluence(username=username, password=password)
    if download_diagram(confluence=confluence, space_key=space_key, target_version=target_version):
        sleep(5)
        main(
            username=username,
            password=password,
            source_branch=source_branch,
            target_branch=target_branch,
            gitlab_url=gitlab_url,
            group_name=group_name,
            project_name=project_name,
            access_token=access_token,
            space_key=space_key,
            parent_page_name=parent_page_name,
            target_version=target_version
        )
        upload_diagram(confluence=confluence, space_key=space_key, target_version=target_version)