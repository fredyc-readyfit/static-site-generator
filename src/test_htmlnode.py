import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_anchor(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode(tag='a', value='anchor', props=props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_props_to_html_img(self):
        props = { "src": "https://example.com/image.png", "alt": "An image alternative text" }
        node = HTMLNode(tag='img', props=props)
        self.assertEqual(node.props_to_html(), ' src="https://example.com/image.png" alt="An image alternative text"')
 
    def test_props_to_html_empty(self):
        node = HTMLNode(tag='h1', value='A title')
        self.assertEqual(node.props_to_html(), '')

if __name__ == "__main__":
    unittest.main()
