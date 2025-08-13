import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from utils import * 
from block import *

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

    def test_missing_alt_brackets(self):
        markdown = "This is missing alt brackets (https://www)"
        result = extract_markdown_images(markdown)
        self.assertEqual(result, [])

    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ],
        new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://internet) and some other [link](https://interwebs.cool) as well",
            TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://internet"),
                TextNode(" and some other ", TextType.TEXT,),
                TextNode("link", TextType.LINK, "https://interwebs.cool"),
                TextNode(" as well", TextType.TEXT),
            ],
            new_nodes
        )
    
    def test_double_split(self):
        node = TextNode(
            "This is text with a [link](coolwebsite) and an ![image](of_a_cat) with a [link](to_a_dog?) why?",
            TextType.TEXT)
        image_nodes = split_nodes_image([node])
        all_nodes = split_nodes_link(image_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT,),
                TextNode("link", TextType.LINK, "coolwebsite"),
                TextNode(" and an ", TextType.TEXT,),
                TextNode("image", TextType.IMAGE, "of_a_cat"),
                TextNode(" with a ", TextType.TEXT,),
                TextNode("link", TextType.LINK, "to_a_dog?"),
                TextNode(" why?", TextType.TEXT,)
            ],
            all_nodes
        )
    def test_markdown_to_text(self):
        text = "This is **bold** and _italic_ and even more *italic*. ![here](is_an_image) and here is a [link](something)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and even more ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(". ", TextType.TEXT),
                TextNode("here", TextType.IMAGE, "is_an_image"),
                TextNode(" and here is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "something")
            ],
            nodes
        )
    def test_markdown_to_text2(self):    
        text2 = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes2 = text_to_textnodes(text2)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes2
        )
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_block_to_block_type(self):
        block = ">This is a block quote\n>with a few lines"
        block2 = "1. This is an ordered\n2. list with two lines"
        block3 = "# HEADING"
        block4 = "## 2 HEADING"
        block5 = "###### 6 Heading"
        block6 = "```\nThis is a code block\n```"
        block7 = "- this is an unordered\n- list of things"
        block8 = "This is a regular paragraph"
        blocktype = block_to_block_type(block)
        blocktype2 = block_to_block_type(block2)
        blocktype3 = block_to_block_type(block3)
        blocktype4 = block_to_block_type(block4)
        blocktype5 = block_to_block_type(block5)
        blocktype6 = block_to_block_type(block6)
        blocktype7 = block_to_block_type(block7)
        blocktype8 = block_to_block_type(block8)
        self.assertEqual(blocktype, BlockType.QUOTE)
        self.assertEqual(blocktype2, BlockType.OLIST)
        self.assertEqual(blocktype3, BlockType.HEADING)
        self.assertEqual(blocktype4, BlockType.HEADING)
        self.assertEqual(blocktype5, BlockType.HEADING)
        self.assertEqual(blocktype6, BlockType.CODE)
        self.assertEqual(blocktype7, BlockType.UOLIST)
        self.assertEqual(blocktype8, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
> this is a quote block
> test did it work?
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>this is a quote block test did it work?</blockquote></div>"
        )

    def test_orderedlist(self):
        md = """
1. First item
2. Second item
"""     
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li></ol></div>"
        )

    def test_unorderedlist(self):
        md = """
- this is another
- test for lists
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>this is another</li><li>test for lists</li></ul></div>"
        )

    def test_heading(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

###### Heading 6

####### Also Heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h6>Heading 6</h6><h6>Also Heading 6</h6></div>"
        )
    def test_all_types_in_one(self):
        md = """
# Heading 1 with _italic_   

Paragraph with 
**inline bold**
characters.

- an unorder list
- with a ![image](link)

1. also ordered list
2. with a [link](somewhere)

```
this is some code
with **bold** that
should not be changed
```

> here is a quote
> that has some **bold** text
"""
        self.maxDiff = None
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
'<div><h1>Heading 1 with <i>italic</i></h1><p>Paragraph with <b>inline bold</b> characters.</p><ul><li>an unorder list</li><li>with a <img src="link" alt="image"></li></ul><ol><li>also ordered list</li><li>with a <a href="somewhere">link</a></li></ol><pre><code>this is some code\nwith **bold** that\nshould not be changed\n</code></pre><blockquote>here is a quote that has some <b>bold</b> text</blockquote></div>'
        )
    def test_parser_heading(self):
        md = "# Heading with _italic_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading with <i>italic</i></h1></div>"
        )

    def test_parser_paragraph(self):
        md = "Paragraph with **inline bold** characters."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Paragraph with <b>inline bold</b> characters.</p></div>"
        )

    def test_parser_quote(self):
        md = "> here is a quote\n> that has some **bold** text"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>here is a quote that has some <b>bold</b> text</blockquote></div>"
        )

if __name__ == '__main__':
    unittest.main()
