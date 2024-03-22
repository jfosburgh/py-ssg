import re


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if type(node) != TextNode or delimiter not in node.text:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 3 != 0:
            raise ValueError(f"{node.text} is not valid markdown")
        for i in range(len(parts)):
            if parts[i] == '':
                if i % 3 == 1:
                    raise ValueError(f"{node.text} has no content within delimiter {delimiter}")
                continue
            if i % 3 == 1:
                new_nodes.append(TextNode(parts[i], text_type))
            else:
                new_nodes.append(TextNode(parts[i], node.text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if type(node) != TextNode:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue

        current_text = node.text
        for image_tup in images:
            parts = current_text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
            if parts[0] != '':
                new_nodes.append(TextNode(parts[0], "text"))
            new_nodes.append(TextNode(image_tup[0], "image", image_tup[1]))
            current_text = parts[1]

        if current_text != "":
            new_nodes.append(TextNode(current_text, "text"))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if type(node) != TextNode:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        current_text = node.text
        for image_tup in links:
            parts = current_text.split(f"[{image_tup[0]}]({image_tup[1]})", 1)
            if parts[0] != '':
                new_nodes.append(TextNode(parts[0], "text"))
            new_nodes.append(TextNode(image_tup[0], "link", image_tup[1]))
            current_text = parts[1]

        if current_text != "":
            new_nodes.append(TextNode(current_text, "text"))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r" \[(.*?)\]\((.*?)\)", text)


def text_to_textnodes(text):
    nodes = [TextNode(text, "text")]
    for text_type, delimiter in zip(["bold", "italic", "code"], ["**", "*", "`"]):
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
