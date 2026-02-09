import unittest

from textnode import TextNode, TextType
from textnode import text_node_to_html_node


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


if __name__ == "__main__":
    unittest.main()