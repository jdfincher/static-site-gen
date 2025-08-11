#!/usr/bin/env python
from textnode import *
from htmlnode import *

def main():
    textnode = TextNode( "something",
                        "bold",
                        "https://something.com")
    print(textnode)
    htmlnode = HTMLNode('tag',
                        'some value',
                        props={"href": "https://someawesomesite.com", "target": "what is a target"})
    print(htmlnode)


main()

