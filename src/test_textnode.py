import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from utils import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node,node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        
    def test_code(self):
        node = TextNode("This is code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, 'www.link.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.props, {'href': 'www.link.com'})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, 'www.web.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.props, {'src': 'www.web.com',
                                           'alt': 'This is an image node'})
    
    def test_split_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),
                                     TextNode("bold", TextType.BOLD),
                                     TextNode(" word", TextType.TEXT)])

    def test_split_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"_", TextType.ITALIC)
        self.assertEqual(new_nodes,
                         [TextNode("This is text with an ", TextType.TEXT),
                          TextNode("italic", TextType.ITALIC),
                          TextNode(" word", TextType.TEXT)])

    def test_split_code(self):
        node = TextNode("This is text with a `code` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertEqual(new_nodes,
                         [TextNode("This is text with a ", TextType.TEXT),
                          TextNode("code", TextType.CODE),
                          TextNode(" word", TextType.TEXT)])
    def test_extract_image(self):
        markdown = "This is some text with an image ![some text](https://somethingcool.com)"
        result = extract_markdown_images(markdown)
        self.assertEqual(result,[('some text', 'https://somethingcool.com')])

    def test_extract_link(self):
        markdown = "This is some link [alt text](https://something)"
        result = extract_markdown_links(markdown)
        self.assertEqual(result,
                         [('alt text', 'https://something')])

    def test_extract_multiple_image(self):
        markdown = "This is a multiple ![image](https://www) ![image2](https://www)"
        result = extract_markdown_images(markdown)
        self.assertEqual(result,
                         [('image', 'https://www'),('image2', 'https://www')])

    def test_extract_link_mixed(self):
        markdown = "This has an ![image](https://blah) and [link](https://bleh)"
        result = extract_markdown_links(markdown)
        self.assertEqual(result,
                         [('link', 'https://bleh')])

    def test_extract_empty(self):
        markdown = "This is just plain text"
        result = extract_markdown_images(markdown)
        self.assertEqual(result,[])

    def test_extract_empty_alt(self):
        markdown = "This is an empty altext ![](https://www)"
        result = extract_markdown_images(markdown)
        self.assertEqual(result, [("",'https://www')])

if __name__ == '__main__':
    unittest.main()
