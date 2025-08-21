from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type.TEXT:
            new_nodes.append(node)
            continue
        split_node = []
        parts = node.text.split(delimiter)
        if len(parts) % 2 != 0:
            raise ValueError(f"TextNode with text type {text_type} must have an even number of parts when split by '{delimiter}'")
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                split_node.append(TextNode(parts[i], text_type.TEXT))
            else:
                split_node.append(TextNode(parts[i], text_type))
            new_nodes.extend(split_node)
            
        
    return new_nodes