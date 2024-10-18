import re
from enum import Enum
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import (
    TextNode,
    text_type_text,
    text_node_to_html_node
)
from inline_markdown import text_to_textnodes

BlockType = Enum("BlockType", ["paragraph", "heading", "code", "quote", "unordered_list", "ordered_list"])

def markdown_to_blocks(markdown):
    segments = markdown.split('\n\n')
    blocks = [segment.strip() for segment in segments if len(segment.strip()) > 0]
    return blocks

def block_to_block_type(block):
    heading_pattern = r"^#{1,6} .+"
    if re.match(heading_pattern, block):
        return BlockType.heading
    
    code_pattern = r"```[\s\S]*?```$"
    if re.match(code_pattern, block):
        return BlockType.code
    
    lines = block.split('\n')
    
    quote_pattern = r"^>.*"
    ok = True
    for line in lines:
        if not re.match(quote_pattern, line.strip()):
            ok = False
    if ok:
        return BlockType.quote


    unordered_list_pattern = r"^[*-] .+"
    ok = True
    for line in lines:
        if not re.match(unordered_list_pattern, line.strip()):
            ok = False
    if ok:
        return BlockType.unordered_list
    
    ordered_list_pattern = r"^\d+\. .+"
    ok = True

    for line in lines:
        if not re.match(ordered_list_pattern, line.strip()):
            ok = False 
    
    for i in range(len(lines)):
        if f"{i+1}" != lines[i].strip()[0]:
            ok = False

    if ok:
        return BlockType.ordered_list

    return BlockType.paragraph

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.heading: 
                html_nodes.append(markdown_heading_to_html_node(block))
            case BlockType.code:
                html_nodes.append(markdown_code_to_html_node(block))
            case BlockType.quote:
                html_nodes.append(markdown_quote_to_html_node(block))
            case BlockType.unordered_list:
                html_nodes.append(markdown_unordered_list_to_html_node(block))
            case BlockType.ordered_list:
                html_nodes.append(markdown_ordered_list_to_html_node(block))
            case BlockType.paragraph:
                html_nodes.append(markdown_paragraph_to_html_node(block))
    
    return ParentNode("div", html_nodes)

def markdown_heading_to_html_node(heading):
    heading = heading.strip()
    if heading.startswith("######"):
        return LeafNode("h6", heading.replace("######", "").strip())
    if heading.startswith("#####"):
        return LeafNode("h5", heading.replace("#####", "").strip())
    if heading.startswith("####"):
        return LeafNode("h4", heading.replace("####", "").strip())
    if heading.startswith("###"):
        return LeafNode("h3", heading.replace("###", "").strip())
    if heading.startswith("##"):
        return LeafNode("h2", heading.replace("##", "").strip())
    if heading.startswith("#"):
        return LeafNode("h1", heading.replace("#", "").strip())

def markdown_quote_to_html_node(quote):
    quotes = quote.strip().split("\n")
    for i in range(len(quotes)):
        quotes[i] = quotes[i].replace(">", "").strip()
    return LeafNode("blockquote", " ".join(quotes))

def markdown_code_to_html_node(code):
    code_lines = code.replace("```", "").strip().split("\n")
    for i in range(len(code_lines)):
        code_lines[i] = code_lines[i].strip()
    return LeafNode("code", "\n".join(code_lines))

def markdown_unordered_list_to_html_node(unordered_list):
    items = unordered_list.split("\n")
    list_items = []
    for item in items:
        text_nodes = text_to_textnodes(item.strip()[2:].strip())
        if len(text_nodes) == 1:
            list_items.append(LeafNode('li', text_nodes[0].text))
        elif len(text_nodes) > 1:
            html_nodes = []
            for tn in text_nodes:
                html_nodes.append(text_node_to_html_node(tn))
            list_items.append(ParentNode('li', html_nodes))

    return ParentNode('ul', list_items)

def markdown_ordered_list_to_html_node(ordered_list):
    items = ordered_list.split("\n")
    list_items = []
    for item in items:
        text_nodes = text_to_textnodes(item.strip()[2:].strip())
        if len(text_nodes) == 1:
            list_items.append(LeafNode('li', text_nodes[0].text))
        elif len(text_nodes) > 1:
            html_nodes = []
            for tn in text_nodes:
                html_nodes.append(text_node_to_html_node(tn))
            list_items.append(ParentNode('li', html_nodes))

    return ParentNode('ol', list_items)

def markdown_paragraph_to_html_node(paragraph):
    text_nodes = text_to_textnodes(" ".join(paragraph.split('\n')))
    if len(text_nodes) == 1:
        return text_node_to_html_node(text_nodes[0])
    elif len(text_nodes) > 1:
        html_nodes = []
        for tn in text_nodes:
            html_nodes.append(text_node_to_html_node(tn))
        return ParentNode('p', html_nodes)

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            return line.replace("#", "").strip()
    
    raise ValueError("Wrong makdown format (no title)")