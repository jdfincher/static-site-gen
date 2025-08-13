from enum import Enum
from textnode import TextNode
from htmlnode import ParentNode
from utils import *

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UOLIST = "unordered_list"
    OLIST = "ordered_list"
    PARAGRAPH = "paragraph"

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    strip_blocks = []
    for block in blocks:
        strip_blocks.append(block.strip())
    return strip_blocks

def block_to_block_type(block):
    if block.startswith('#'):
        return BlockType.HEADING
    elif block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    split_block = block.split('\n')
    quote_count = 0
    uolist_count = 0
    olist_count = 0
    num = 1
    for piece in split_block:
        if piece.startswith('>'):
            quote_count += 1    
        elif piece.startswith('- '):
            uolist_count += 1
        elif piece.startswith((str(num)+'. ')):
            olist_count += 1
            num += 1
    if quote_count == len(split_block):
        return BlockType.QUOTE
    
    elif uolist_count == len(split_block):
        return BlockType.UOLIST

    elif olist_count == len(split_block):
        return BlockType.OLIST

    else:
        return BlockType.PARAGRAPH

def block_type_to_tag(block_type, count=0):
    match block_type:
        case BlockType.HEADING:
            if count == 1:
                return 'h1'
            elif count == 2:
                return 'h2'
            elif count == 3:
                return 'h3'
            elif count == 4:
                return 'h4'
            elif count == 5:
                return 'h5'
            elif count == 6:
                return 'h6'
            elif count > 6:
                return 'h6'
            else:
                return 'h6'
        case BlockType.CODE:
            return 'code'
        case BlockType.QUOTE:
            return 'blockquote'
        case BlockType.UOLIST:
            return 'ul'
        case BlockType.OLIST:
            return 'ol'
        case BlockType.PARAGRAPH:
            return 'p'
        case _:
            raise Exception("Invalid BlockType")

def clean_block_text(text, block_type):
    if block_type == BlockType.HEADING:
        while text.startswith('#'):
            text = text.lstrip('#')
        return text.strip()
    
    elif block_type == BlockType.QUOTE:
        clean = []
        split_text = text.split('\n')
        for line in split_text:
            if line.startswith('> '):
                clean_line = line[2:]
            elif line.startswith('>'):
                clean_line = line[1:]
            clean.append(clean_line.strip())
        return ' '.join(clean)
    
    elif block_type == BlockType.UOLIST:
        clean = []
        split_text = text.split('\n')
        for line in split_text:
            if line.startswith('- '):
                clean_line = line[2:]
            elif line.startswith('* '):
                clean_line = line[2:]
            else:
                clean_line = line
            clean.append(clean_line.strip())
        return '\n'.join(clean)
    
    elif block_type == BlockType.OLIST:
        clean = []
        split_text = text.split('\n')
        for line in split_text:
            if '. ' in line:
                clean_line = line.split('. ', 1)[1]
            else:
                clean_line = line
            clean.append(clean_line.strip())
        return '\n'.join(clean)

    elif block_type == BlockType.CODE:
        if text.startswith('```') and text.endswith('```'):
            content = text[3:-3]
            if content.startswith('\n'):
                content = content[1:]
            return content
    elif block_type == BlockType.PARAGRAPH:
        split_text = text.split('\n')
        joined = ' '.join(line.strip() for line in split_text)
        return joined.strip()
    else:
        raise Exception("Invalid BlockType, only HEADING, QUOTE, UOLIST and OLIST need cleaning")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    new_nodes = []
    for node in text_nodes:
        new_nodes.append(text_node_to_html_node(node))
    return new_nodes

def list_to_children(text):
    children = []
    split_list = text.split('\n')
    for item in split_list:
        if item.strip():
            item_children = text_to_children(item)
            children.append(ParentNode('li',item_children))
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    blocks = [block for block in blocks if block.strip()]
    outer_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        count = 0
        if block.startswith('#'):
            for char in block:
                if char == '#':
                    count += 1
                else: 
                    break
        tag = block_type_to_tag(block_type, count)
        clean_text = clean_block_text(block, block_type)
        if block_type == BlockType.HEADING:
            children = text_to_children(clean_text)
            parent = ParentNode(tag, children)
            outer_children.append(parent)

        elif block_type == BlockType.CODE:
            contents = TextNode(clean_text,TextType.TEXT)
            child = text_node_to_html_node(contents)
            parent = ParentNode(tag, [child])
            grand_parent = ParentNode('pre', [parent])
            outer_children.append(grand_parent)

        elif block_type == BlockType.QUOTE:
            children = text_to_children(clean_text)
            parent = ParentNode(tag, children)
            outer_children.append(parent)

        elif block_type == BlockType.UOLIST:
            children = list_to_children(clean_text)
            parent = ParentNode(tag, children)
            outer_children.append(parent)

        elif block_type == BlockType.OLIST:
            children = list_to_children(clean_text)
            parent = ParentNode(tag, children)
            outer_children.append(parent)

        elif block_type == BlockType.PARAGRAPH:
            children = text_to_children(clean_text)
            parent = ParentNode(tag, children)
            outer_children.append(parent)

    return ParentNode('div',outer_children)    

    
    
