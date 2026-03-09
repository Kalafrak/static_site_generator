from textnode import TextNode, TextType
import re



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError("invalid markdown syntax")
            else:
                for i in range(len(parts)):
                    if parts[i] == "":
                        continue
                    if i % 2 == 0:
                        new_nodes.append(TextNode(parts[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(parts[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            image_tuples = extract_markdown_images(node.text)
            if image_tuples == []:
                new_nodes.append(node)
            else:
                remaining_text = node.text
                for image_tuple in image_tuples:
                    alt_text = image_tuple[0]
                    url = image_tuple[1]
                    sections = remaining_text.split(f"![{alt_text}]({url})", 1)
                    if len(sections) != 2:
                        new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                        remaining_text = ""
                        break
                    remaining_text = sections[1]
                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                if remaining_text != "":
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            link_tuples = extract_markdown_links(node.text)
            if link_tuples == []:
                new_nodes.append(node)
            else:
                remaining_text = node.text
                for link_tuple in link_tuples:
                    alt_text = link_tuple[0]
                    url = link_tuple[1]
                    sections = remaining_text.split(f"[{alt_text}]({url})", 1)
                    if len(sections) != 2:
                        new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                        remaining_text = ""
                        break
                    remaining_text = sections[1]
                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextType.LINK, url))
                if remaining_text != "":
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes
