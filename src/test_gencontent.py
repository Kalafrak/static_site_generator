import unittest

from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_basic_title(self):
        markdown = "# Hello"
        actual = extract_title(markdown)
        self.assertEqual(actual, "Hello")

    def test_extra_whitespace(self):
        markdown = "# Spaced Out "
        actual = extract_title(markdown)
        self.assertEqual(actual, "Spaced Out")

    def test_multi_line(self):
        markdown = """This is some intro text.

Some more paragraph content here.

# The Real Title

And then more content below the title.
"""
        actual = extract_title(markdown)
        self.assertEqual(actual, "The Real Title")

    def test_no_title(self):
        markdown = """This is some intro text.

Some more paragraph content here.

Oh no! There's no title!

And then more content below the title.
"""
        with self.assertRaises(Exception):
            extract_title(markdown)
        


if __name__ == "__main__":
    unittest.main()
