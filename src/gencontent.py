import os
from pathlib import Path

from markdown_blocks import markdown_to_html_node
from htmlnode import ParentNode

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            stripped_prefix = line.removeprefix("# ")
            stripped_line = stripped_prefix.strip()
            return stripped_line
    raise Exception("No title found!")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path) as f:
        from_file = f.read()
    with open(template_path) as t:
        template_file = t.read()
    from_html_node = markdown_to_html_node(from_file)
    from_html_string = from_html_node.to_html()
    from_title = extract_title(from_file)
    template_replaced_title = template_file.replace("{{ Title }}", from_title)
    template_replaced_content = template_replaced_title.replace("{{ Content }}", from_html_string)
    template_replaced_href = template_replaced_content.replace('href="/', f'href="{basepath}')
    template_replaced_src = template_replaced_href.replace('src="/', f'src="{basepath}')

    dest_directory = os.path.dirname(dest_path)
    os.makedirs(dest_directory, exist_ok=True)
    with open(dest_path, mode='w') as f:
        f.write(template_replaced_src)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_list = os.listdir(dir_path_content)
    for item in content_list:
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path):
            generate_page(item_path, template_path, os.path.join(dest_dir_path, Path(item).with_suffix(".html")), basepath)
        else:
            generate_pages_recursive(item_path, template_path, os.path.join(dest_dir_path, item), basepath)


