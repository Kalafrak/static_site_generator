from textnode import TextNode
from textnode import TextType

def main():
    book = TextNode("Testing the code!", TextType.ITALIC, "https://www.wowhead.com")
    print(book)

main()