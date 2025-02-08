import logging
from atlassian import Jira
import sys
import re


SCRIPTNAME = "create-history-task.py"
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

def create_history_task(target_branch, project_key):
    # Параметры для новой задачи
    issue_dict = {
        'project': {'key': f'{project_key}'},  # Ключ проекта
        'summary': f'Выпуск {target_branch}',  # Название задачи
        'description': '',  # Описание задачи
        'issuetype': {'name': 'Story'},  # Тип задачи, например, "Task", "Bug" и т.д.
        'priority': {'name': 'Medium'},  # Приоритет задачи
        # Дополнительные поля могут быть добавлены по необходимости
    }

    # Создание задачи
    try:
        response = jira.issue_create(fields=issue_dict)
        logger.info(f"History task created with ID: {response['key']}")
    except Exception as e:
        logger.error(e)
        logger.error('44: Error create history task')


if __name__ == '__main__':
    username = sys.argv[1]
    password = sys.argv[2]
    target_branch = sys.argv[3]
    project_dict = {
        '<jira-project/project-settings/mouse-on-details>': '<jira-project/project-settings/details/key>',
    }

    jira = connect_to_jira(username=username, password=password)
    pattern = r"release\/\d+\.\d+\.\d+"
    tmp = re.search(pattern=pattern, string=target_branch)

    if tmp.group(0) == target_branch:
        create_history_task(target_branch=target_branch, project_key=project_dict['12001'])
    else:
        create_history_task(target_branch=target_branch, project_key=project_dict['10100'])