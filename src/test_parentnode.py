import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_parent_with_leaf_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_parent_with_leaf_children_and_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            { 
                "class": "cool-class"
            }
        )
        self.assertEqual(node.to_html(), '<p class="cool-class"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')
    
    def test_parent_with_parent_child(self):
        node = ParentNode(
            'div',
            [
                ParentNode('p', [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ])
            ]
        )
        self.assertEqual(node.to_html(), '<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>')

    def test_parent_with_parent_children(self):
        node = ParentNode(
            'div',
            [
                ParentNode('p', [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ]),
                LeafNode('img', "Image", {"src": "https://example.com/image.png", "alt": "An Image"}),
                ParentNode('p', [ LeafNode("b", "Bold text") ])
            ]
        )
        self.assertEqual(node.to_html(), '<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><img src="https://example.com/image.png" alt="An Image">Image</img><p><b>Bold text</b></p></div>')
    
    def test_parent_without_children(self):
        node = ParentNode('div', [])
        self.assertEqual(node.to_html(), '<div></div>')

if __name__ == "__main__":
    unittest.main()
