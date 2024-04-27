import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_eq_text(self):
        node = HtmlNode("h1", "Hello World")
        node2 = HtmlNode("h1", "Hello World")
        self.assertEqual(node.value, node2.value)

    def test_props_to_html(self):
        node1 = HtmlNode(tag="a", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node1.props_to_html(), ' href="https://www.google.com" target="_blank"')

        node2 = HtmlNode(tag="div", props={"class": "container"})
        self.assertEqual(node2.props_to_html(), ' class="container"')

    def test_repr(self):
        node = HtmlNode(tag="p", value="Hello, world!", props={"class": "paragraph"})
        self.assertEqual(repr(node), 'HtmlNode(tag=p, value=Hello, world!, children=None, props={\'class\': \'paragraph\'})')

class TestLeafNode(unittest.TestCase):
    def test_render_html(self):
        leaf_node1 = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(leaf_node1.to_html(), '<p>This is a paragraph of text.</p>')

        leaf_node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(leaf_node2.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_value_required(self):
        with self.assertRaises(ValueError):
            LeafNode("p")

class TestParentNode(unittest.TestCase):
    def test_render_html(self):
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

    def test_tag_required(self):
        with self.assertRaises(ValueError):
            ParentNode()

    def test_children_required(self):
        with self.assertRaises(ValueError):
            ParentNode("p", [])

    def test_nested_nodes(self):
        inner_node = ParentNode(
            "div",
            [
                LeafNode("span", "Inner span"),
                LeafNode(None, "Inner text"),
            ]
        )
        outer_node = ParentNode(
            "div",
            [
                inner_node,
                LeafNode("p", "Paragraph"),
            ]
        )
        expected_html = '<div><div><span>Inner span</span>Inner text</div><p>Paragraph</p></div>'
        self.assertEqual(outer_node.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()