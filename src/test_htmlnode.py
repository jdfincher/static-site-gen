import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    
    def test_to_html_props(self):
        expected = 'href="https://www.coolsite.com" target="not_sure"'
        node = HTMLNode(props={"href": "https://www.coolsite.com",
                               "target": "not_sure"})
        test_node = node.props_to_html()
        self.assertEqual(expected,test_node)

    def test_values(self):
        node = HTMLNode(
            'p',
            'some text',
            None,
            {'href': "https://www.web.com",
             'target': "_blank"}
        )

        self.assertEqual(node.tag,'p')
        self.assertEqual(node.value,'some text')
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {'href': "https://www.web.com",
             'target': "_blank"})

    def test_repr(self):

        node = HTMLNode(
            'p',
            'some text',
            None,
            {'href': 'https://www.web.com',
             'target': '_blank'}
        )

        self.assertEqual(node.__repr__(),
                         "HTMLNode(p, some text, None, {'href': 'https://www.web.com', 'target': '_blank'})")
    
    def test_p_leaf_to_html(self):
        node = LeafNode("p","Hello World!")
        self.assertEqual(node.to_html(), "<p>Hello World!</p>")
        
    def test_a_leaf_to_html(self):
        node = LeafNode('a','Click Here!',{"href": "https://www"})
        self.assertEqual(node.to_html(), '<a href="https://www">Click Here!</a>')
    
    def test_values_leafnode(self):
        node = LeafNode('a','Click Here!',{"href": "https://www"})
        self.assertEqual(node.tag,'a')
        self.assertEqual(node.value, 'Click Here!')
        self.assertEqual(node.children, None)
        self.assertEqual(node.props,{"href": "https://www"})

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_hrml_with_great_grandchildren(self):
        great_grandchild = LeafNode("i", "great_grandchild")
        great_grandchild2 = LeafNode("b", "great_grandchild2")
        grandchild = ParentNode("p", [great_grandchild, great_grandchild2])
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), 
                         "<div><span><p><i>great_grandchild</i><b>great_grandchild2</b></p></span></div>")

if __name__ == '__main__':
    unittest.main()

