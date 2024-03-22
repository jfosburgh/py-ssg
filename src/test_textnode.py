import unittest

from textnode import TextNode, extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from htmlnode import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_type_neq(self):
        node = TextNode("This is a text node", "itallic")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_text_neq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a different text node", "bold")
        self.assertNotEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("This is a text node", "bold", "https://boot.dev")
        node2 = TextNode("This is a text node", "bold", "https://bood.dev")
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", "bold", "https://boot.dev")
        node2 = TextNode("This is a text node", "bold", "https://boot.dev")
        self.assertEqual(node, node2)

    def test_conversion(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual("<b>This is a text node</b>", text_node_to_html_node(node).to_html())

        node = TextNode("This is a text node", "italic")
        self.assertEqual("<i>This is a text node</i>", text_node_to_html_node(node).to_html())

        node = TextNode("This is a text node", "text")
        self.assertEqual("This is a text node", text_node_to_html_node(node).to_html())

        node = TextNode("This is a text node", "code")
        self.assertEqual("<code>This is a text node</code>", text_node_to_html_node(node).to_html())

        node = TextNode("This is a text node", "link", "https://boot.dev")
        self.assertEqual('<a href="https://boot.dev">This is a text node</a>', text_node_to_html_node(node).to_html())

        node = TextNode("This is a text node", "image", "https://boot.dev")
        self.assertEqual('<img href="https://boot.dev" alt="This is a text node">', text_node_to_html_node(node).to_html())

    def test_split(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual([node], split_nodes_delimiter([node], "**", "bold"))

        node2 = TextNode("This is text with a `code block` word", "text")
        old_nodes = [node, node2]
        new_nodes = [
            node, 
            TextNode("This is text with a ", "text"), 
            TextNode("code block", "code"), 
            TextNode(" word", "text")
        ]
        self.assertEqual(new_nodes, split_nodes_delimiter(old_nodes, "`", "code"))
        self.assertEqual(old_nodes, split_nodes_delimiter(old_nodes, "*", "italic"))

        node = TextNode("This is text with an *italic* word", "text")
        old_nodes = [node]
        new_nodes = [
            TextNode("This is text with an ", "text"), 
            TextNode("italic", "italic"), 
            TextNode(" word", "text")
        ]
        self.assertEqual(new_nodes, split_nodes_delimiter(old_nodes, "*", "italic"))

        node = TextNode("This is text with a **bold** word", "text")
        old_nodes = [node]
        new_nodes = [
            TextNode("This is text with a ", "text"), 
            TextNode("bold", "bold"), 
            TextNode(" word", "text")
        ]
        self.assertEqual(new_nodes, split_nodes_delimiter(old_nodes, "**", "bold"))

        self.assertRaises(ValueError, split_nodes_delimiter, [node], "*", "italic")

        node = TextNode("This is text with *invalid** markdown", "text")
        self.assertRaises(ValueError, split_nodes_delimiter, [node], "*", "italic")

        node = TextNode("This is text with invalid** markdown", "text")
        self.assertRaises(ValueError, split_nodes_delimiter, [node], "*", "italic")

        node = TextNode("This is text with invalid** markdown", "text")
        self.assertRaises(ValueError, split_nodes_delimiter, [node], "**", "bold")

        node = TextNode("**This text is all bold**", "text")
        new_node = TextNode("This text is all bold", "bold")
        self.assertEqual([new_node], split_nodes_delimiter([node], "**", "bold"))

    def test_image_extract(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png"), ("another", "https://i.imgur.com/dfsdkjfd.png")]
        self.assertEqual(expected, extract_markdown_images(text))

        text = "This is text with no images"
        expected = []
        self.assertEqual(expected, extract_markdown_images(text))

        text = "![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertEqual(expected, extract_markdown_images(text))

    def test_link_extract(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        self.assertEqual(expected, extract_markdown_links(text))

        text = "This is text with no links"
        expected = []
        self.assertEqual(expected, extract_markdown_links(text))

        # text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        # expected = []
        # self.assertEqual(expected, extract_markdown_links(text))

        text = "[Back Home](/)"
        expected = [("Back Home", "/")]
        self.assertEqual(expected, extract_markdown_links(text))


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)",
            "text",
        )
        expected = [
            TextNode("This is text with an ", "text"),
            TextNode("image", "image", "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and ", "text"),
            TextNode("another", "image", "https://i.imgur.com/dfsdkjfd.png"),
        ]
        self.assertEqual(expected, split_nodes_image([node]))

        node = TextNode("This is a node with no images", "text")
        self.assertEqual([node], split_nodes_image([node]))


    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
            "text"
        )
        expected = [
            TextNode("This is text with a ", "text"),
            TextNode("link", "link", "https://www.example.com"),
            TextNode(" and ", "text"),
            TextNode("another", "link", "https://www.example.com/another"),
        ]
        self.assertEqual(expected, split_nodes_link([node]))

        node = TextNode("This is a node with no links", "text")
        self.assertEqual([node], split_nodes_link([node]))

        # node = TextNode(
        #     "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)",
        #     "text",
        # )
        # self.assertEqual([node], split_nodes_link([node]))


    def test_text_to_nodes(self):
        text_type_text = "text"
        text_type_bold = "bold"
        text_type_italic = "italic"
        text_type_code = "code"
        text_type_image = "image"
        text_type_link = "link"

        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"

        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(expected, text_to_textnodes(text))


if __name__ == "__main__":
    unittest.main()
