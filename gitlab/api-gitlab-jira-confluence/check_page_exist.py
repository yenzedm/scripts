from atlassian import Confluence
import sys
import re
import logging


SCRIPTNAME = "check_page_exist.py"
logger = logging.getLogger(SCRIPTNAME) # initializing and declaring the logger name
logger.setLevel(logging.DEBUG) # set the logging level
console_out = logging.StreamHandler() # connect the logging handler to stdout
strfmt = '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s' # we define the format of the message in the log so that it looks beautiful
datefmt = '%Y-%m-%d %H:%M:%S' # determine the date and time format in the log
formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt) # create a formatting handler with previously defined formats
console_out.setFormatter(formatter) # apply formatting for output
logger.addHandler(console_out) # include an output handler in the output

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
    space_key = '<confluence/project/space tools/overview/key>'

    pattern = r"\d+\.\d+\.\d+"
    target_match = re.search(pattern, target_branch)
    page_version = target_match.group(0)

    confluence = connect_to_confluence(username=username, password=password)

    check_page_exist(confluence=confluence, target_branch=target_branch, space_key=space_key, page_version=page_version)