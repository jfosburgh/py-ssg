import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode()
        self.assertEqual("", node.props_to_html())
        
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(' href="https://www.google.com"', node.props_to_html())

        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())

    def test_leaf_node(self):
        node = LeafNode(None)
        self.assertRaises(ValueError, node.to_html)

        node = LeafNode(None, "Raw text")
        self.assertEqual("Raw text", node.to_html())

        node = LeafNode("a", "Link text")
        self.assertEqual('<a>Link text</a>', node.to_html())

        node = LeafNode("a", "Link text", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual('<a href="https://www.google.com" target="_blank">Link text</a>', node.to_html())

    def test_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "div",
                    [
                        LeafNode("a", "Link text")
                    ],
                    props={"class": "test"}
                )

            ],
        )
        self.assertEqual('<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<div class="test"><a>Link text</a></div></p>', node.to_html())



if __name__ == "__main__":
    unittest.main()
