import unittest

from textnode import TextNode, TextType
from textnode import text_node_to_html_node
from inline_markdown import split_nodes_delimiter
from inline_markdown import extract_markdown_images
from inline_markdown import extract_markdown_links
from inline_markdown import split_nodes_image
from inline_markdown import split_nodes_link
from inline_markdown import text_to_textnodes


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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_matches(self):
        node = TextNode("Just plain text, no images here.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_no_matches(self):
        node = TextNode("Just plain text, no links here.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_at_start(self):
        node = TextNode("![a](u) trailing", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "u"),
                TextNode(" trailing", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_at_end(self):
        node = TextNode("leading ![a](u)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("leading ", TextType.TEXT),
                TextNode("a", TextType.IMAGE, "u"),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_adjacent(self):
        node = TextNode("![a](u)![b](v)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "u"),
                TextNode("b", TextType.IMAGE, "v"),
            ],
            split_nodes_image([node]),
        )

    def test_split_links_ignores_images(self):
        node = TextNode("before ![img](https://x.com/a.png) after", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_split_images_ignores_links(self):
        node = TextNode("before [anchor](https://example.com) after", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_preserves_non_text_nodes(self):
        nodes = [
            TextNode("prefix ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("[a](u)", TextType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("prefix ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("a", TextType.LINK, "u"),
            ],
            split_nodes_link(nodes),
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )

if __name__ == "__main__":
    unittest.main()