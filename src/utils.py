from textnode import *
from htmlnode import *
import re

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {'href': text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', '', {'src': text_node.url,
                                        'alt': text_node.text})
        case _:
            raise Exception('Not a valid TextType')

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Mismatched delimiters!")
        for i, part in enumerate(parts):
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        original_text = node.text
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            alt = image[0]
            src = image[1]
            string_list = original_text.split(f"![{alt}]({src})", 1)
            if string_list[0] != '':
                new_nodes.append(TextNode(string_list[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, src))
            if len(string_list) > 1:
                original_text = string_list[1]
        if len(original_text) != 0:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        original_text = node.text
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            alt = link[0]
            src = link[1]
            string_list = original_text.split(f"[{alt}]({src})", 1)
            if string_list[0] != '':
                new_nodes.append(TextNode(string_list[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, src))
            if len(string_list) > 1:    
                original_text = string_list[1]
        if len(original_text) != 0:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)  

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def text_to_textnodes(text):
    node = TextNode(text,TextType.TEXT)
    nodes = split_nodes_image([node])
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes
    





