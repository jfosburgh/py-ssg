from block_types import *
from htmlnode import HTMLNode, ParentNode, text_node_to_html_node
from textnode import text_to_textnodes


def markdown_to_blocks(markdown):
    uncleaned_blocks = markdown.split("\n\n")
    cleaned_blocks = [block.strip() for block in uncleaned_blocks]
    return [block for block in cleaned_blocks if block != '']


def block_to_block_type(block):
    if block.startswith("#"):
        start = block.split(" ")[0]
        if len(start) <= 6 and all([l == "#" for l in start]):
            return block_type_heading
    if block.startswith('```') and block.endswith('```'):
        return block_type_code
    lines = block.split("\n")
    if all([line.startswith(">") for line in lines]):
        return block_type_quote
    if all([line[0] in ['-', '*'] for line in lines]):
        return block_type_unordered_list
    if lines[0][:2] == '1.':
        ol = True
        current = 1
        for line in lines:
            if not line.startswith(str(current)+"."):
                ol = False
                break
            current += 1
        if ol:
            return block_type_ordered_list
    return block_type_paragraph


def text_to_html_nodes(text):
    children = text_to_textnodes(text)
    return [text_node_to_html_node(child) for child in children]


def heading_to_html_node(heading_block):
    parts = heading_block.split(" ")
    level = len(parts[0])
    text = " ".join(parts[1:])
    return ParentNode(f"h{level}", text_to_html_nodes(text))


def code_to_html_node(code_block):
    text = code_block.split('```')[1].strip()
    return ParentNode(
        "pre", 
        [ParentNode("code", text_to_html_nodes(text))]
    )


def quote_to_html_node(quote_block):
    text = "\n".join([part.strip() for part in quote_block.split(">")[1:]])
    return ParentNode("blockquote", text_to_html_nodes(text))


def ul_to_html_node(ul_block):
    lines = [line[1:].strip() for line in ul_block.split("\n")]
    children = [ParentNode("li", text_to_html_nodes(line)) for line in lines]
    return ParentNode("ul", children)


def ol_to_html_node(ol_block):
    lines = [".".join(line.split(".")[1:]).strip() for line in ol_block.split("\n")]
    children = [ParentNode("li", text_to_html_nodes(line)) for line in lines]
    return ParentNode("ol", children)


def paragraph_to_html_node(paragraph_block):
    return ParentNode("p", text_to_html_nodes(paragraph_block))


block_type_to_parser = {
    block_type_heading: heading_to_html_node,
    block_type_code: code_to_html_node,
    block_type_quote: quote_to_html_node,
    block_type_unordered_list: ul_to_html_node,
    block_type_ordered_list: ol_to_html_node,
    block_type_paragraph: paragraph_to_html_node
}


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    block_types = [block_to_block_type(block) for block in blocks]
    for block, block_type in zip(blocks, block_types):
        children.append(block_type_to_parser[block_type](block))
    return ParentNode(tag="div", children=children)
