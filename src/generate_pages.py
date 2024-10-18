import os
from blocks_markdown import (
    markdown_to_html_node,
    extract_title
)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as file:
        markdown = file.read()
    
    with open(template_path, 'r') as file:
        template = file.read()
    
    html_node = markdown_to_html_node(markdown)
    title = extract_title(markdown)
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_node.to_html())

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as file:
        file.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_dir_list = os.listdir(dir_path_content)
    for file in content_dir_list:
        if os.path.isfile(os.path.join(dir_path_content, file)):
            from_path = os.path.join(dir_path_content, file)
            dest_path = os.path.join(dest_dir_path, file.replace('md', 'html'))
            generate_page(from_path, template_path, dest_path)

        else:
            subdir_path_content = os.path.join(dir_path_content, file)
            dest_subdir_path = os.path.join(dest_dir_path, file)
            generate_pages_recursive(subdir_path_content, template_path, dest_subdir_path)
