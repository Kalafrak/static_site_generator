import unittest

from textnode import TextNode, TextType
from textnode import text_node_to_html_node
from textnode import split_nodes_delimiter
from textnode import extract_markdown_images
from textnode import extract_markdown_links


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("Howdy!", TextType.LINK)
        node2 = TextNode("Howdy Partner!", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("Howdy!", TextType.LINK, "https://wowhead.com")
        node2 = TextNode("Howdy!", TextType.LINK, "https://youtube.com")
        self.assertNotEqual(node, node2)

    def test_tt_not_eq(self):
        node = TextNode("Howdy!", TextType.IMAGE)
        node2 = TextNode("Howdy!", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://wowhead.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://wowhead.com"})

    def test_image(self):
        node = TextNode("A bear", TextType.IMAGE, "https://example.com/bear.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/bear.png", "alt": "A bear"},
        )

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is **bold** text!", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(new_node, [TextNode("This is ", TextType.TEXT),
                                        TextNode("bold", TextType.BOLD),
                                        TextNode(" text!", TextType.TEXT),
                                        ])
        
    def test_delim_italic(self):
        node = TextNode("This is _italic_ text!", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(new_node, [TextNode("This is ", TextType.TEXT),
                                        TextNode("italic", TextType.ITALIC),
                                        TextNode(" text!", TextType.TEXT),
                                        ])
        
    def test_delim_code(self):
        node = TextNode("This is `code` text!", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(new_node, [TextNode("This is ", TextType.TEXT),
                                        TextNode("code", TextType.CODE),
                                        TextNode(" text!", TextType.TEXT),
                                        ])
        
    def test_delim_bold_multiple(self):
        node = TextNode("**This** is **bold** text!", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(new_node, [TextNode("This", TextType.BOLD), 
                                        TextNode(" is ", TextType.TEXT),
                                        TextNode("bold", TextType.BOLD),
                                        TextNode(" text!", TextType.TEXT),
                                        ])
        
    def test_no_delim(self):
        node = TextNode("This is bold text!", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(new_node, [TextNode("This is bold text!", TextType.TEXT)])

    def test_delim_error(self):
        node = TextNode("This is **invalid bold text", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)


if __name__ == "__main__":
    unittest.main()