from enum import Enum

from htmlnode import ParentNode
from inline_markdown import *
from textnode import TextNode
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        n = 0
        for line in lines:
            n += 1
            if not line.startswith(f"{n}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = []
    splits = markdown.split("\n\n")
    for split in splits:
        block = split.strip()
        if block != "":
            blocks.append(block)
    return blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            text = " ".join(block.split("\n"))
            paragraph_children = text_to_children(text)
            node = ParentNode(tag="p", children=paragraph_children, props=None)
            children.append(node)
        elif block_type == BlockType.HEADING:
            level = len(block) - len(block.lstrip("#"))
            tag = f"h{level}"
            text = block.lstrip("# ")
            heading_children = text_to_children(text)
            node = ParentNode(tag=tag, children=heading_children, props=None)
            children.append(node)
        elif block_type == BlockType.CODE:
            stripped_backticks = block.strip("`")
            text = stripped_backticks.lstrip("\n")
            text_node = TextNode(text, TextType.CODE)
            html_node = text_node_to_html_node(text_node)
            node = ParentNode(tag="pre", children=[html_node])
            children.append(node)
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            stripped_lines = [line.lstrip(">") for line in lines]
            stripped_lines_whitespace = [line.strip() for line in stripped_lines]
            text = " ".join(stripped_lines_whitespace)
            quote_children = text_to_children(text)
            node = ParentNode(tag="blockquote", children=quote_children, props=None)
            children.append(node)
        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            stripped_lines = [line.lstrip("- ") for line in lines]
            li_nodes = [ParentNode("li", text_to_children(line)) for line in stripped_lines]
            node = ParentNode(tag="ul", children=li_nodes, props=None)
            children.append(node)
        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            stripped_lines = [line.split(". ", 1)[1] for line in lines]
            li_nodes = [ParentNode("li", text_to_children(line)) for line in stripped_lines]
            node = ParentNode(tag="ol", children=li_nodes, props=None)
            children.append(node)
    return ParentNode(tag="div", children=children, props=None)



def text_to_children(text):
    textnodes = text_to_textnodes(text)
    htmlnodes = []
    for textnode in textnodes:
        htmlnode = text_node_to_html_node(textnode)
        htmlnodes.append(htmlnode)
    return htmlnodes
