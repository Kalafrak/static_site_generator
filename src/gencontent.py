import os

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

def generate_page(from_path, template_path, dest_path):
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

    dest_directory = os.path.dirname(dest_path)
    os.makedirs(dest_directory, exist_ok=True)
    with open(dest_path, mode='w') as f:
        f.write(template_replaced_content)

