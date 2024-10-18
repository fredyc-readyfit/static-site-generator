import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        splitted = node.text.split(delimiter)

        if len(splitted) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")

        for i in range(len(splitted)):
            if len(splitted[i].strip()) == 0:
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(f"{splitted[i]}", node.text_type))
            else:
                new_nodes.append(TextNode(f"{splitted[i]}", text_type))

    return new_nodes

def extract_markdown_images(text):
    markdown_images = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", text)
    return markdown_images

def extract_markdown_links(text):
    markdown_links = re.findall(r"\[([^\]]*)\]\(([^)]+)\)", text)
    return markdown_links

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        text = node.text
        markdown_images = extract_markdown_images(text)
        for markdown_image in markdown_images:
            i = text.index(f"![{markdown_image[0]}]({markdown_image[1]})")
            sub_text = text[:i]
            if (len(sub_text.strip())) > 0:
                new_nodes.append(TextNode(sub_text, node.text_type))
            new_nodes.append(TextNode(markdown_image[0], text_type_image, markdown_image[1]))
            text = text.replace(f"{sub_text}![{markdown_image[0]}]({markdown_image[1]})", "")
        
        if (len(text.strip())) > 0:
           new_nodes.append(TextNode(text, node.text_type))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        text = node.text
        markdown_links = extract_markdown_links(text)
        for markdown_link in markdown_links:
            i = text.index(f"[{markdown_link[0]}]({markdown_link[1]})")
            sub_text = text[:i]
            if (len(sub_text.strip())) > 0:
                new_nodes.append(TextNode(sub_text, node.text_type))
            new_nodes.append(TextNode(markdown_link[0], text_type_link, markdown_link[1]))
            text = text.replace(f"{sub_text}[{markdown_link[0]}]({markdown_link[1]})", "")
        
        if (len(text.strip())) > 0:
            new_nodes.append(TextNode(text, node.text_type))

    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, text_type_text)
    text_nodes = split_nodes_delimiter([node], '**', text_type_bold)
    text_nodes = split_nodes_delimiter(text_nodes, '*', text_type_italic)
    text_nodes = split_nodes_delimiter(text_nodes, '`', text_type_code)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes