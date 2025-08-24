import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_node = []
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown, formatted section not closed")
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                split_node.append(TextNode(parts[i], TextType.TEXT))
            else:
                split_node.append(TextNode(parts[i], text_type))
        new_nodes.extend(split_node)
            
        
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        org_text = node.text
        images = extract_markdown_images(org_text)
        if not images:
            new_nodes.append(node)
            continue
        
        for image in images:
            parts = org_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(parts) != 2:
                raise ValueError("Invalid markdown image syntax")
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1]
                )
            )
            org_text = parts[1]
        if org_text != "":
            new_nodes.append(TextNode(org_text, TextType.TEXT))     
        
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        org_text = node.text
        links = extract_markdown_links(org_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        
        for link in links:
            parts = org_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(parts) != 2:
                raise ValueError("Invalid markdown link syntax")
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    link[0],
                    TextType.LINK,
                    link[1]
                )
            )
            org_text = parts[1]
        if org_text != "":
            new_nodes.append(TextNode(org_text, TextType.TEXT))     
        
    return new_nodes

def text_to_textnodes(text):
        nodes = [TextNode(text, TextType.TEXT)]
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        nodes = split_nodes_image(nodes)
        nodes = split_nodes_link(nodes)
        return nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
    
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

