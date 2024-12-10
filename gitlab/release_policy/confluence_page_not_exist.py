from atlassian import Confluence
import sys
import re
import logging


SCRIPTNAME = "confluence_page_not_exist.py"
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

def create_html_block():
    with open('diagram.svg', 'r') as file:
        tmp = f"""
    <ac:structured-macro ac:name="html">
        <ac:plain-text-body><![CDATA[{file.read()}]]></ac:plain-text-body>
    </ac:structured-macro>
    """
        return tmp

def create_page(confluence, space_key, parent_page_name, page_version):
    page_name = f'Mermaid {page_version}'
    page_id = confluence.get_page_id(space_key, parent_page_name)
    macro_body = create_html_block()
    confluence.create_page(space_key, page_name, body=macro_body, parent_id=page_id, representation='storage')

    response = confluence.page_exists(space_key, page_name, type=None)
    if response:
        logger.info(f"page {page_name} created successfully")
    else:
        logger.error(f"47: the {page_name} does not exist")
        return False
    
    return True

def upload_diagram(confluence, space_key, page_version):
    page_name = f'Mermaid {page_version}'
    page_id = confluence.get_page_id(space_key, page_name)
    response = confluence.attach_file('diagram.mmd', page_id=page_id, space=space_key)
    if response:
        logger.info(f"diagram.mmd upload into the {page_name} successfully")
    else:
        logger.error(f"59: Something wrong file diagram.mmd does not upload into the {page_name}")


if __name__ == '__main__':
    username = sys.argv[1]
    password = sys.argv[2]
    target_branch = sys.argv[3]
    space_key = 'recfaces'
    parent_page_name = '70.01.10.87 - Mermaid'

    pattern = r"\d+\.\d+\.\d+"
    target_match = re.search(pattern, target_branch)
    page_version = target_match.group(0)

    confluence = connect_to_confluence(username=username, password=password)
    if create_page(confluence=confluence, space_key=space_key, parent_page_name=parent_page_name, page_version=page_version):
        upload_diagram(confluence=confluence, space_key=space_key, page_version=page_version)