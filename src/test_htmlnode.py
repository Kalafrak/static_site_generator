import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_none(self):
        node = HTMLNode("a", "This is a link", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_empty_dict(self):
        node = HTMLNode("a", "This is a link", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_multiple(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("a", "Google", None, props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')


if __name__ == "__main__":
    unittest.main()