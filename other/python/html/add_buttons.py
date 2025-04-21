import re
from pathlib import Path

buttons_file = Path("buttons.txt")
template_file = Path("template.html")
output_file = Path("index.html")

def clean_anchor(text):
    cleaned = re.sub(r'^\s*[\d\.\s]+', '', text.strip())
    return cleaned

def parse_buttons(file_path):
    result = []
    current_block = None

    with open(file_path, encoding="utf-8") as f:
        for line in f:
            if "|" in line:
                path, name = line.strip().split("|", 1)
                path = path.strip()
                name = name.strip()
                if path:
                    if current_block:
                        result.append(current_block)
                    current_block = {"path": path, "name": name, "submenu": []}
                else:
                    if current_block:
                        current_block["submenu"].append(name.strip())
        if current_block:
            result.append(current_block)
    return result

def generate_menu(blocks):
    html = ""
    for idx, block in enumerate(blocks, start=1):
        menu_id = f"menu{idx}"
        html += f'    <div class="dropdown-container" id="{menu_id}">\n'
        html += f'        <button class="main-button" onclick="loadPage(\'{block["path"]}\'), toggleDropdown(\'{menu_id}\')">{block["name"]}</button>\n'
        if block["submenu"]:
            html += '        <div class="dropdown-menu">\n'
            for item in block["submenu"]:
                anchor = clean_anchor(item)
                html += f'            <button onclick="scrollToElement(\'{anchor}\')">{item}</button>\n'
            html += '        </div>\n'
        html += '    </div>\n\n'
    return html

def insert_menu(template, menu_html):
    output = []
    in_menu = False
    for line in template:
        if '<div class="menu">' in line:
            output.append(line)
            in_menu = True
            continue
        if in_menu and '</div>' in line:
            output.append(menu_html)
            output.append(line)
            in_menu = False
            continue
        if not in_menu:
            output.append(line)
    return output

if __name__ == "__main__":
    blocks = parse_buttons(buttons_file)
    menu_html = generate_menu(blocks)
    template_lines = template_file.read_text(encoding="utf-8").splitlines(keepends=True)
    final_output = insert_menu(template_lines, menu_html)
    output_file.write_text("".join(final_output), encoding="utf-8")
