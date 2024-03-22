import unittest

from blocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node
from block_types import *

class TestHTMLNode(unittest.TestCase):
    def test_markdown_blocks(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is a list item\n* This is another list item"
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item"
        ]
        self.assertEqual(expected, markdown_to_blocks(markdown))

        markdown = "\n\n# This is a heading\n\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.   \n\n    * This is a list item\n* This is another list item    "
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item"
        ]
        self.assertEqual(expected, markdown_to_blocks(markdown))

        blocks = [
            ("# This is a heading", block_type_heading),
            ("#This is not a heading", block_type_paragraph),
            ("#### Another heading", block_type_heading),
            ("This is a paragraph of text. It has some **bold** and *italic* words inside of it.", block_type_paragraph),
            ("* This is a list item\n* This is another list item", block_type_unordered_list),
            ("- This is a list item\n- This is another list item", block_type_unordered_list),
            ("- This is a list item\n* This is another list item", block_type_unordered_list),
            ("* This is a list item\nThis is another list item", block_type_paragraph),
            ("1. List Item 1\n2. List Item 2", block_type_ordered_list),
            ("1. List Item 1\n3. List Item 2", block_type_paragraph),
            ("1. List Item 1\n2.List Item 2", block_type_ordered_list),
            ("```Code block line 1\nCode block line 2", block_type_paragraph),
            ("```Code block line 1\nCode block line 2```", block_type_code),
            (">List Item 1\nList Item 2", block_type_paragraph),
            (">List Item 1\n>List Item 2", block_type_quote),
        ]
        for block, block_type in blocks:
            self.assertEqual(block_type, block_to_block_type(block))


    def test_markdown_to_node(self):
        def assert_equals_html(unit, expected, markdown):
            actual = markdown_to_html_node(markdown).to_html()
            unit.assertEqual(expected, actual)

        markdown = "# Heading 1"
        expected = "<div><h1>Heading 1</h1></div>"
        assert_equals_html(self, expected, markdown)
        
        markdown += "\n\n### Subheading"
        expected = "<div><h1>Heading 1</h1><h3>Subheading</h3></div>"
        assert_equals_html(self, expected, markdown)
        
        markdown += "\n\n>First line of quote\n>Second line of quote"
        expected = "<div><h1>Heading 1</h1><h3>Subheading</h3><blockquote>First line of quote\nSecond line of quote</blockquote></div>"
        assert_equals_html(self, expected, markdown)

        markdown += "\n\n```Code block line one\nCode block line 2```"
        expected = "<div><h1>Heading 1</h1><h3>Subheading</h3><blockquote>First line of quote\nSecond line of quote</blockquote><pre><code>Code block line one\nCode block line 2</code></pre></div>"
        assert_equals_html(self, expected, markdown)

        markdown += "\n\n-UL item 1\n*UL item 2"
        expected = "<div><h1>Heading 1</h1><h3>Subheading</h3><blockquote>First line of quote\nSecond line of quote</blockquote><pre><code>Code block line one\nCode block line 2</code></pre><ul><li>UL item 1</li><li>UL item 2</li></ul></div>"
        assert_equals_html(self, expected, markdown)

        markdown += "\n\n1. OL item 1\n2. OL item 2"
        expected = "<div><h1>Heading 1</h1><h3>Subheading</h3><blockquote>First line of quote\nSecond line of quote</blockquote><pre><code>Code block line one\nCode block line 2</code></pre><ul><li>UL item 1</li><li>UL item 2</li></ul><ol><li>OL item 1</li><li>OL item 2</li></ol></div>"
        assert_equals_html(self, expected, markdown)

        markdown += "\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it."
        expected = "<div><h1>Heading 1</h1><h3>Subheading</h3><blockquote>First line of quote\nSecond line of quote</blockquote><pre><code>Code block line one\nCode block line 2</code></pre><ul><li>UL item 1</li><li>UL item 2</li></ul><ol><li>OL item 1</li><li>OL item 2</li></ol><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p></div>"
        assert_equals_html(self, expected, markdown)


if __name__ == "__main__":
    unittest.main()
