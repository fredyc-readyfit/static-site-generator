import unittest

from blocks_markdown import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    extract_title
)
from leafnode import LeafNode

class BlocksMarkdownTests(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                """* This is the first list item in a list block
* This is a list item
* This is another list item"""
            ],
            blocks
        )
    
    def test_markdown_to_blocks_with_whitespace(self):
        markdown = """        # This is a heading               

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
* This is a list item
* This is another list item 
        """
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                """* This is the first list item in a list block
* This is a list item
* This is another list item"""
            ],
            blocks
        )

    def test_markdown_to_blocks_with_empty_blocks(self):
        markdown = """        # This is a heading               

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
* This is a list item
* This is another list item




        """
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                """* This is the first list item in a list block
* This is a list item
* This is another list item"""
            ],
            blocks
        )

    def test_block_to_block_type_headings(self):
        block_heading_1 = "# This is a heading"
        block_heading_2 = "## This is a heading"
        block_heading_3 = "### This is a heading"
        block_heading_4 = "#### This is a heading"
        block_heading_5 = "##### This is a heading"
        block_heading_6 = "###### This is a heading"
        block_not_heading = "This is not a heading"

        block_type = block_to_block_type(block_heading_1)
        self.assertEqual(BlockType.heading, block_type)

        block_type = block_to_block_type(block_not_heading)
        self.assertEqual(BlockType.paragraph, block_type)

        block_type = block_to_block_type(block_heading_2)
        self.assertEqual(BlockType.heading, block_type)

        block_type = block_to_block_type(block_heading_3)
        self.assertEqual(BlockType.heading, block_type)

        block_type = block_to_block_type(block_not_heading)
        self.assertEqual(BlockType.paragraph, block_type)

        block_type = block_to_block_type(block_heading_4)
        self.assertEqual(BlockType.heading, block_type)

        block_type = block_to_block_type(block_heading_5)
        self.assertEqual(BlockType.heading, block_type)

        block_type = block_to_block_type(block_not_heading)
        self.assertEqual(BlockType.paragraph, block_type)

        block_type = block_to_block_type(block_heading_6)
        self.assertEqual(BlockType.heading, block_type)

    def test_block_to_block_type_code(self):
        block = """```
        some code
        ```"""
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.code, block_type)

        block="```some code ```"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.code, block_type)

        block = "```some code ```\nthis is not code"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.paragraph, block_type)

    def test_block_to_block_type_quote(self):
        block = "> quote"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.quote, block_type)

        block = """> quote
        > quote
        > quote""" 
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.quote, block_type)

        block = """> quote
        > quote
        > quote
        not a block quote""" 
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.paragraph, block_type)

    def test_block_to_block_type_unordered_list(self):
        block = "* list item"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.unordered_list, block_type)

        block = """* item
        - item
        * item""" 
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.unordered_list, block_type)

        block = """- item
        - item
        - item
        not an item""" 
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.paragraph, block_type)
    
    def test_block_to_block_type_ordered_list(self):
        block = "1. list item"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.ordered_list, block_type)

        block = """1. item
        2. item
        3. item""" 
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.ordered_list, block_type)

        block = """1. item
        3. item
        2. item""" 
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.paragraph, block_type)

        block = """1. item
        2. item
        3. item
        not an item""" 
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.paragraph, block_type)

    def test_markdown_to_html_node(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        html_node = markdown_to_html_node(markdown)

        self.assertEqual(
            html_node.to_html(),
            '<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul></div>'
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )
    def test_code(self):
        md = """
```this is
a code
block
```

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><code>this is\na code\nblock</code><p>this is paragraph text</p></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )
    
    def test_extract_title(self):
        markdown = """# This is a heading     

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        title = extract_title(markdown)
        self.assertEqual(title, "This is a heading")

    def test_extract_title_end(self):
        markdown = """

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

# This is a heading     
"""
        title = extract_title(markdown)
        self.assertEqual(title, "This is a heading")

    def test_extract_title_exception(self):
        markdown = """
This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        self.assertRaises(ValueError, extract_title, markdown)

if __name__ == "__main__":
    unittest.main()