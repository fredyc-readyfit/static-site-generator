import unittest

from textnode import (
    TextNode, 
    text_type_text, 
    text_type_bold,
    text_type_italic, 
    text_type_code, 
    text_type_link, 
    text_type_image, 
    text_node_to_html_node
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode('This is a text node', 'bold')
        node2 = TextNode('This is a text node', 'bold')
        self.assertEqual(node, node2)
    
    def test_eq_url(self):
        node = TextNode('This is a text node', 'bold', 'https://www.boot.dev')
        node2 = TextNode('This is a text node', 'bold', 'https://www.boot.dev')
        self.assertEqual(node, node2)
    
    def test_eq_different(self):
        node = TextNode('This is a text node', 'bold', 'https://www.boot.dev')
        node2 = TextNode('This is another text node', 'bold', 'https://www.boot.dev')
        self.assertNotEqual(node, node2)
    
    def test_eq(self):
        node = TextNode('This is a text node', 'bold')
        self.assertEqual(f"{node}", "TextNode(This is a text node, bold, None)")

    def test_eq(self):
        node = TextNode('This is a text node', 'bold', 'https://www.boot.dev')
        self.assertEqual(f"{node}", "TextNode(This is a text node, bold, https://www.boot.dev)") 

    def test_text_to_html_text(self):
        node = TextNode('This is a text node', text_type_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, node.text)

    def test_text_to_html_bold(self):
        node = TextNode('This is a text node', text_type_bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, node.text)

    def test_text_to_html_italic(self):
        node = TextNode('This is a text node', text_type_italic)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, node.text)

    def test_text_to_html_code(self):
        node = TextNode('This is a code node', text_type_code)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, node.text)

    def test_text_to_html_link(self):
        node = TextNode('This is a link node', text_type_link)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, node.text)
        self.assertEqual(html_node.props["href"], node.url)

    def test_text_to_html_image(self):
        node = TextNode('This is a image node', text_type_image)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props["src"], node.url)
        self.assertEqual(html_node.props["alt"], node.text)

if __name__ == "__main__":
    unittest.main()
