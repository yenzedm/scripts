from atlassian import Jira
import json
import datetime
import sys
import logging
from time import sleep


SCRIPTNAME = "jira_project_releases.py"
logger = logging.getLogger(SCRIPTNAME)
logger.setLevel(logging.DEBUG)
console_out = logging.StreamHandler()
strfmt = '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)
console_out.setFormatter(formatter)
logger.addHandler(console_out)

def connect_to_jira(username, password):
    try:
        _jira = Jira(
            url='https://jira.eosan.ru',
            username=username,
            password=password)
        return _jira
    except:
        logger.error('27: jira connect error')
        return None

def create_release(jira, space_key, project_id, target_branch, ru_date, global_date):
    tmp = target_branch + ' - open'
    try:
        response = jira.add_version(project_key=space_key, project_id=project_id, version=tmp, is_released=False)
    except Exception as e:
        logger.info(f"35: Error create release: {e}")

    try:
        response = jira.get_project_versions(key=space_key)
    except Exception as e:
        logger.error(f"40: Error get releases: {e}")
    sleep(3)

    release_id = ''
    for release in response:
        if target_branch in release['name']:
            release_id = release['id']

    try:
        response = jira.update_version(version=release_id, is_released=False, start_date=global_date)
        logger.info(f"{target_branch} added successfully")
    except Exception as e:
        logger.error(f"52: Error update release: {e}")
    

def update_release(jira, space_key, global_date, ru_date, source_branch, target_branch):
    try:
        response = jira.get_project_versions(key=space_key)
    except Exception as e:
        logger.error(f"59: Error get releases: {e}")
    sleep(3)

    release_id = ''
    for release in response:
        if source_branch in release['name']:
            release_id = release['id']
            release_start_date = release['startDate']

    tmp = source_branch + ' - ' + ru_date

    try:
        response = jira.update_version(version=release_id, name=tmp, is_released=False, start_date=release_start_date, release_date=global_date)
        logger.info(f"{source_branch} updated successfully")
    except Exception as e:
        logger.error(f"74: Error update release: {e}")


if __name__ == '__main__':
    username = sys.argv[1]
    password = sys.argv[2]
    source_branch = sys.argv[3]
    target_branch = sys.argv[4]
    project_dict = {
        '<jira-project/project-settings/details/key>': '<jira-project/project-settings/mouse-on-details>',
    }

    tmp = datetime.date.today()
    global_date = tmp.isoformat()
    ru_date = tmp.strftime("%d-%m-%Y")

    jira = connect_to_jira(username=username, password=password)
    for space_key, project_id in project_dict.items():
        if 'develop' not in source_branch:
            update_release(jira=jira, space_key=space_key, global_date=global_date, ru_date=ru_date, source_branch=source_branch, target_branch=target_branch)
        create_release(jira=jira, space_key=space_key, project_id=project_id, target_branch=target_branch, ru_date=ru_date, global_date=global_date)