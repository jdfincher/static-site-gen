class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        string = ''
        if len(self.props) > 0:
            for key,value in self.props.items():
                string += (key+'='+'"'+value+'"'+' ')
        return string[:(len(string)-1)]
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"



class LeafNode(HTMLNode):
    def __init__(self,tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value property missing")
        if self.tag is None:
            return self.value
        if self.props is not None:
            open_tag = f"<{self.tag} {self.props_to_html()}>"
        else:
            open_tag = f"<{self.tag}>"
        close_tag = f"</{self.tag}>"
        
        return f"{open_tag}{self.value}{close_tag}"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag property missing")
        if self.children is None:
            raise ValueError("Children property missing")
        if self.props is not None:
            open_tag = f"<{self.tag} {self.props_to_html()}>"
        else:
            open_tag = f"<{self.tag}>"
        close_tag = f"</{self.tag}>"
        children = ""
        for child in self.children:
            children += child.to_html()

        return f"{open_tag}{children}{close_tag}"

        
