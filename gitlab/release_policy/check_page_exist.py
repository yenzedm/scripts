from atlassian import Confluence
import sys
import re
import logging


SCRIPTNAME = "check_page_exist.py"
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
        logger.error('25: confluence connect error')
        return None

def check_page_exist(confluence, target_branch, space_key, page_version):
    page_name = f'Mermaid {page_version}'
    response = confluence.page_exists(space_key, page_name)
    if response:
            logger.info(f"page {page_name} exist")
            sys.exit(0)
    else:
        logger.info(f"35: page {page_name} does not exist")
        sys.exit(1)


if __name__ == '__main__':
    username = sys.argv[1]
    password = sys.argv[2]
    target_branch = sys.argv[3]
    space_key = 'recfaces'

    pattern = r"\d+\.\d+\.\d+"
    target_match = re.search(pattern, target_branch)
    page_version = target_match.group(0)

    confluence = connect_to_confluence(username=username, password=password)

    check_page_exist(confluence=confluence, target_branch=target_branch, space_key=space_key, page_version=page_version)