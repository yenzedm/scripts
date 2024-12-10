from atlassian import Confluence
import sys
import logging
import re


SCRIPTNAME = "confluence_page_exist.py"
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

def create_html_block():
    with open('diagram.svg', 'r') as file:
        tmp = f"""
    <ac:structured-macro ac:name="html">
        <ac:plain-text-body><![CDATA[{file.read()}]]></ac:plain-text-body>
    </ac:structured-macro>
    """
        return tmp

def update_html_block(confluence, page_version, space_key):
    page_name = f'Mermaid {page_version}'
    page_id = confluence.get_page_id(space_key, page_name)

    macro_body = create_html_block()
    response = confluence.update_page(page_id=page_id, title=page_name, body=macro_body)
    if response:
        logger.info(f'43: the {page_name} updated')
    else:
        logger.error(f'45: the {page_name} is not updated')


if __name__ == '__main__':
    username = sys.argv[1]
    password = sys.argv[2]
    target_branch = sys.argv[3]
    space_key = 'recfaces'

    pattern = r"\d+\.\d+\.\d+"
    target_match = re.search(pattern, target_branch)
    page_version = target_match.group(0)

    confluence = connect_to_confluence(username=username, password=password)
    update_html_block(confluence=confluence, page_version=page_version, space_key=space_key)
