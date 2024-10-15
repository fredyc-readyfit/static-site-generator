import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)
from markdown_helpers import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)

class TestMarkdownHelpers(unittest.TestCase):
    def test_split_nodes_bold(self):
        node = TextNode("This is text with a **bold** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(len(new_nodes), 3)
        self.assertListEqual(
            [
                TextNode('This is text with a ', text_type_text),
                TextNode('bold', text_type_bold),
                TextNode(' word', text_type_text)
            ],
            new_nodes
        )

    def test_split_nodes_bold_multiword(self):
        node = TextNode("This is text with a **bold** word and **another**", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(len(new_nodes), 4)
        self.assertListEqual(
            [
                TextNode('This is text with a ', text_type_text),
                TextNode('bold', text_type_bold),
                TextNode(' word and ', text_type_text),
                TextNode('another', text_type_bold)
            ],
            new_nodes
        )
    
    def test_split_nodes_italic(self):
        node = TextNode("This is text with a *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(len(new_nodes), 3)
        self.assertListEqual(
            [
                TextNode('This is text with a ', text_type_text),
                TextNode('italic', text_type_italic),
                TextNode(' word', text_type_text)
            ],
            new_nodes
        )
    
    def test_split_nodes_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        self.assertEqual(len(new_nodes), 3)
        self.assertListEqual(
            [
                TextNode('bold', text_type_bold),
                TextNode(' and ', text_type_text),
                TextNode('italic', text_type_italic),
            ],
            new_nodes
        )

    def test_split_nodes_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(len(new_nodes), 3)
        self.assertListEqual(
            [
                TextNode('This is text with a ', text_type_text),
                TextNode('code block', text_type_code),
                TextNode(' word', text_type_text)
            ],
            new_nodes
        )
    
    def test_split_nodes_exception(self):
        node = TextNode("This is text with a *wrong format", text_type_text)
        self.assertRaises(ValueError, split_nodes_delimiter, [node], "*", text_type_italic)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ],
            extract_markdown_images(text)
        )
    
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"), 
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ],
            extract_markdown_links(text)
        )
    
    def test_split_nodes_image(self):
        node = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif)", text_type_text)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertListEqual(
            [
                TextNode('rick roll', text_type_image, 'https://i.imgur.com/aKaOqIh.gif'),
            ],
            new_nodes
        ) 

    def test_split_nodes_image_multi(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", text_type_text)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertListEqual(
            [
                TextNode('This is text with a ', text_type_text),
                TextNode('rick roll', text_type_image, 'https://i.imgur.com/aKaOqIh.gif'),
                TextNode(' and ', text_type_text),
                TextNode('obi wan', text_type_image, 'https://i.imgur.com/fJRm4Vk.jpeg'),
            ],
            new_nodes
        )

    def test_split_nodes_link(self):
        node = TextNode("[to boot dev](https://www.boot.dev)", text_type_text)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertListEqual(
            [
                TextNode('to boot dev', text_type_link, 'https://www.boot.dev'),
            ],
            new_nodes
        )
    
    def test_split_nodes_link_multi(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", text_type_text)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertListEqual(
            [
                TextNode('This is text with a link ', text_type_text),
                TextNode('to boot dev', text_type_link, 'https://www.boot.dev'),
                TextNode(' and ', text_type_text),
                TextNode('to youtube', text_type_link, 'https://www.youtube.com/@bootdotdev'),
            ],
            new_nodes
        )
    
    def test_split_nodes_link_and_image(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", text_type_text)
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertEqual(len(new_nodes), 4)
        self.assertListEqual(
            [
                TextNode('This is text with a link ', text_type_text),
                TextNode('to boot dev', text_type_link, 'https://www.boot.dev'),
                TextNode(' and a ', text_type_text),
                TextNode('rick roll', text_type_image, 'https://i.imgur.com/aKaOqIh.gif'),
            ],
            new_nodes
        )
    
    def test_text_to_textnodes(self):
        text_nodes = text_to_textnodes('This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)')
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            text_nodes
        )


if __name__ == "__main__":
    unittest.main()
