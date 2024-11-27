from atlassian import Confluence
import sys
import re
import logging

SCRIPTNAME = "release_policy_confluence"
logger = logging.getLogger(SCRIPTNAME) # Initialize and declare logger name
logger.setLevel(logging.DEBUG) # Set logging level
console_out = logging.StreamHandler() # Attach log handler to stdout
strfmt = '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s' # Define log message format for better readability
datefmt = '%Y-%m-%d %H:%M:%S' # Define date and time format in logs
formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt) # Create formatter with the defined formats
console_out.setFormatter(formatter) # Apply formatting to the log output
logger.addHandler(console_out) # Enable log output handler

def compare_versions(version1, version2):
    # Split version strings into components separated by dots
    v1_parts = list(map(int, version1.split('.')))
    v2_parts = list(map(int, version2.split('.')))
    
    # Pad the shorter list with zeros if versions have different lengths
    length = max(len(v1_parts), len(v2_parts))
    v1_parts.extend([0] * (length - len(v1_parts)))
    v2_parts.extend([0] * (length - len(v2_parts)))
    
    # Compare components sequentially
    for part1, part2 in zip(v1_parts, v2_parts):
        if part1 > part2:
            return version1
        elif part1 < part2:
            return version2

def create_release_version(confluence, username, password, space_key, parent_page_name):
    # Retrieve all child pages of the specified parent page
    confluence = connect_to_confluence(username, password)
    page_id = confluence.get_page_id(space_key, parent_page_name)
    children = confluence.cql(f"""
        type = page 
        and ancestor = {page_id}
        order by created DESC
    """)
    result = []
    for child in children['results']:
        result.append(child['title'])

    # Extract version numbers from child page titles
    pattern = r"\d+\.\d+\.\d+"
    list_release_version = []
    for page_name in result:
        version = re.search(pattern, page_name)
        tmp = version.group(0)
        list_release_version.append(tmp)

    # Compare and select the largest version
    release_version = '0.0'
    for release in list_release_version:
        release_version = compare_versions(release_version, release)
    
    return release_version

def connect_to_confluence(username, password):
    try:
        _confluence = Confluence(
            url='https://confluence.eosan.ru',
            username=username,
            password=password)
        return _confluence
    except:
        print('Confluence connection error')
        return None

def main(USERNAME, PASSWORD, SOURCE_BRANCH, TARGET_BRANCH, SPACE_KEY, PARENT_PAGE_NAME, target_version, source_version):
    if target_version == source_version:
        page_name = f'Mermaid {create_release_version(confluence, USERNAME, PASSWORD, SPACE_KEY, PARENT_PAGE_NAME)}'
        page_id = confluence.get_page_id(SPACE_KEY, page_name)

        # Retrieve page content
        page = confluence.get_page_by_id(page_id, expand="body.storage,version")

        # Extract current page body content
        body_html = page['body']['storage']['value']

        old_lines = """commit\ type:\ HIGHLIGHT"""

        new_lines = f"""commit tag:"readonly"\n    branch {TARGET_BRANCH}\n    checkout {TARGET_BRANCH}\n    commit type: HIGHLIGHT"""

        # Replace old string and add new content
        updated_body = re.sub(old_lines, new_lines, body_html, flags=re.VERBOSE)

        # Update the page in Confluence
        response = confluence.update_page(
            page_id=page_id,
            title=page['title'],
            body=updated_body,
            representation='storage'
        )

        if response:
            logger.info(f"Page {page_name} updated successfully")
        else:
            logger.error(f"Error in 100 false response for {page_name}")
    elif 'rc' in SOURCE_BRANCH and 'build' in TARGET_BRANCH:
        page_name = f'Mermaid {create_release_version(confluence, USERNAME, PASSWORD, SPACE_KEY, PARENT_PAGE_NAME)}'
        page_id = confluence.get_page_id(SPACE_KEY, page_name)

        # Retrieve page content
        page = confluence.get_page_by_id(page_id, expand="body.storage,version")

        # Extract current page body content
        body_html = page['body']['storage']['value']

        old_lines = """commit\ type:\ HIGHLIGHT"""

        new_lines = f'''commit tag:"readonly"\n    branch {TARGET_BRANCH}\n    checkout {TARGET_BRANCH}\n    commit tag:"readonly"'''

        # Replace old string and add new content
        updated_body = re.sub(old_lines, new_lines, body_html, flags=re.VERBOSE)

        # Update the page in Confluence
        response = confluence.update_page(
            page_id=page_id,
            title=page['title'],
            body=updated_body,
            representation='storage'
        )

        if response:
            logger.info(f"Page {page_name} updated successfully")
        else:
            logger.error(f"Error in 129 false response for {page_name}")
    elif SOURCE_BRANCH == 'develop' and 'build' in TARGET_BRANCH:
        page_name = f'Mermaid {create_release_version(confluence, USERNAME, PASSWORD, SPACE_KEY, PARENT_PAGE_NAME)}'
        page_id = confluence.get_page_id(SPACE_KEY, page_name)

        # Retrieve page content
        page = confluence.get_page_by_id(page_id, expand="body.storage,version")

        # Extract current page body content
        body_html = page['body']['storage']['value']

        # Update macro content
        old_lines = rf"""commit\ type:\ HIGHLIGHT"""
        new_lines = f"""commit tag:"readonly"\n    checkout {SOURCE_BRANCH}\n    commit\n    branch {TARGET_BRANCH}\n    checkout {TARGET_BRANCH}\n    commit type: HIGHLIGHT"""

        # Replace old string and add new content
        updated_body = re.sub(old_lines, new_lines, body_html, flags=re.VERBOSE)

        # Update the page in Confluence
        response = confluence.update_page(
            page_id=page_id,
            title=page['title'],
            body=updated_body,
            representation='storage'
        )

        if response:
            logger.info(f"Page {page_name} updated successfully")
        else:
            logger.error(f"Error in 158 false response for {page_name}")
    elif SOURCE_BRANCH == 'develop' and 'rc1' in TARGET_BRANCH:
        page_name = f'Mermaid {target_version}'
        page_id = confluence.get_page_id(SPACE_KEY, PARENT_PAGE_NAME)
        
        mermaid_macro = f"""<ac:structured-macro ac:name="mermaid-macro"><ac:plain-text-body><![CDATA[gitGraph:\n    commit\n    branch develop\n    checkout develop\n    commit\n    branch {TARGET_BRANCH}\n    checkout {TARGET_BRANCH}\n    commit type: HIGHLIGHT]]></ac:plain-text-body>\n    </ac:structured-macro>"""

        confluence.create_page(SPACE_KEY, f'Mermaid {target_version}', body=mermaid_macro, parent_id=page_id, representation='storage')

        response = confluence.page_exists(SPACE_KEY, page_name, type=None)

        if response:
            logger.info(f"Page {page_name} created successfully")
        else:
            logger.error(f"Error in 170 false response for {page_name}")


if __name__ == '__main__':
    USERNAME = sys.argv[1]
    PASSWORD = sys.argv[2]
    SOURCE_BRANCH = sys.argv[3]
    TARGET_BRANCH = sys.argv[4]
    SPACE_KEY = 'recfaces'
    PARENT_PAGE_NAME = '70.01.10.87 - Mermaid'


    pattern = r"\d+\.\d+\.\d+.\d+"
    target_match = re.search(pattern, TARGET_BRANCH)
    source_match = re.search(pattern, SOURCE_BRANCH)
    try:
        target_version = target_match.group(0)
        source_version = source_match.group(0)
    except:
        source_version = None

    confluence = connect_to_confluence(USERNAME, PASSWORD)

    main(USERNAME, PASSWORD, SOURCE_BRANCH, TARGET_BRANCH, SPACE_KEY, PARENT_PAGE_NAME, target_version, source_version)
