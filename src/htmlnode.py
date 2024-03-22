class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""
        res = ""
        for key, val in self.props.items():
            res += f' {key}="{val}"'
        return res

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf nodes must have a value")
        if not self.tag:
            return f"{self.value}"
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent nodes must have a tag")
        if not self.children:
            raise ValueError("Parent nodes must have children")
        return f"<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"


TEXT_TYPE_TO_HTML_TAG = {
    "text": None,
    "bold": "b",
    "italic": "i",
    "code": "code",
    "link": "a",
    "image": "img"
}


def text_node_to_html_node(text_node):
    if text_node.text_type not in TEXT_TYPE_TO_HTML_TAG.keys():
        raise ValueError(f"{text_node.text_type} is not a valid type")
    tag = TEXT_TYPE_TO_HTML_TAG[text_node.text_type]
    value = text_node.text
    props = None
    if text_node.url:
        props = {"href": text_node.url}
        if tag == "img":
            props["alt"] = value
            value = ""
    return LeafNode(tag, value, props)
