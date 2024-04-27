class HtmlNode:
    # Constructor
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        html_value = ""
        if self.props != None and isinstance(self.props, dict):
            for key, value in self.props.items():
                html_value = html_value + " " + key + "=\"" + value + "\""
        
        return html_value

    def __repr__(self):
        return f"HtmlNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

# Create a LeafNode that inherits HtmlNode
class LeafNode(HtmlNode):
    # defines a constructor without children and a mandatory value
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("LeafNode requires a value.")
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode requires a value.")
        
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

# Create a ParentNode that inherits HtmlNode      
class ParentNode(HtmlNode):
    def __init__(self, tag=None, children=None, props=None):
        if tag is None:
            raise ValueError("ParentNode requires a tag.")
        if children is None or not children:
            raise ValueError("ParentNode must have at least one child.")
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"