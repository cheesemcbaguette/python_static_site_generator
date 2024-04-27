import unittest
from inline_markdown import (
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    split_nodes_delimiter,
    text_to_textnodes
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        old_nodes = [TextNode("This is text with a **bolded** word", "text")]
        new_nodes = split_nodes_delimiter(old_nodes, "**", "bold")
        expected_nodes = [
            TextNode("This is text with a ", "text"),
            TextNode("bolded", "bold"),
            TextNode(" word", "text")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_italic(self):
        old_nodes = [TextNode("This is *italic* text", "text")]
        new_nodes = split_nodes_delimiter(old_nodes, "*", "italic")
        expected_nodes = [
            TextNode("This is ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text", "text")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_code(self):
        old_nodes = [TextNode("This is text with a `code block` word", "text")]
        new_nodes = split_nodes_delimiter(old_nodes, "`", "code")
        expected_nodes = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_no_delimiter_found(self):
        old_nodes = [TextNode("This is text without delimiters", "text")]
        new_nodes = split_nodes_delimiter(old_nodes, "*", "bold")
        self.assertEqual(new_nodes, old_nodes)

class TestInlineMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

class TestSplitNodesImage(unittest.TestCase):
    def test_split_image(self):
            node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
                text_type_text,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
                [
                    TextNode("This is text with an ", text_type_text),
                    TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                ],
                new_nodes,
            )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", text_type_image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example2.com)",
            "text",
        )
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://example.com"),
            TextNode(" and another ", text_type_text),
            TextNode("second link", text_type_link, "https://example2.com"),
        ]
        self.assertEqual(new_nodes, expected_nodes)

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected_nodes)

if __name__ == "__main__":
    unittest.main()