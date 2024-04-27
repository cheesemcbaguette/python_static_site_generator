import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_image,
    text_type_link,
    text_type_bold,
    text_type_italic,
    text_type_code
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
        new_nodes = []
        # loop through nodes
        for old_node in old_nodes:
            # if node not text type then append node
            if old_node.text_type != text_type_text:
                new_nodes.append(old_node)
                continue

            split_nodes = []
            # split nodes with delimiter
            sections = old_node.text.split(delimiter)

            # if the number of sections isn't even it means that the number of delimiter is either odd or missing
            if len(sections) % 2 == 0:
                raise ValueError("Invalid markdown, formatted section not closed")
            
            # loop through sections
            for i in range(len(sections)):
                # if section is empty then do nothing
                if sections[i] == "":
                    continue
                # if even then we append the text_type_text value ('text')
                if i % 2 == 0:
                    split_nodes.append(TextNode(sections[i], text_type_text))

                # else we append the text_type value
                else:
                    split_nodes.append(TextNode(sections[i], text_type))
                    
            # append the content of the split nodes to new_nodes
            new_nodes.extend(split_nodes)
        return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    # loop through nodes
    for old_node in old_nodes:
        # if node not text type then append node
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        # assign the old node text to the original_text variable
        original_text = old_node.text
        # extract the images from original_text
        images = extract_markdown_images(original_text)
        # if no image was found then append old node
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        # if some image was found loop through them
        for image in images:
            # split the original text once with the format '[("image", "image-url")]
            # what will remain is the text before the image markdown and after the image markdown
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            
            # create a new text node only if the text before the image isn't empty
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))

            # append a new text node to new_nodes
            new_nodes.append(
                TextNode(
                    # image alt text
                    image[0],
                    # text type image
                    text_type_image,
                    # image url
                    image[1],
                )
            )
            original_text = sections[1]
        
        # create a new text node only if the text after the image isn't empty
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    # loop through nodes
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            # If the node is not of type 'text', append it to the new nodes list and continue to the next iteration
            new_nodes.append(old_node)
            continue
        original_text = old_node.text  # Get the original text from the old node
        links = extract_markdown_links(original_text)  # Extract links from the original text
        if len(links) == 0:
            # If no links are found in the original text, append the old node to the new nodes list and continue
            new_nodes.append(old_node)
            continue

        # Iterate over each link found in the original text
        for link in links:
            # Split the original text into two sections based on the link markdown syntax
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            
            if len(sections) != 2:
                # If the split doesn't result in two sections, raise a ValueError indicating invalid markdown syntax
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                # If there is text before the link markdown, create a new text node and append it to the new nodes list
                new_nodes.append(TextNode(sections[0], text_type_text))
            # Create a new link node with the link text and URL, and append it to the new nodes list
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            original_text = sections[1]  # Update the original text to the remaining section
        if original_text != "":
            # If there is remaining text after processing all links, create a new text node and append it to the new nodes list
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes  # Return the list of new nodes

def text_to_textnodes(text):
    # Split text into text nodes using the splitting functions
    nodes = split_nodes_delimiter([TextNode(text, "text")], "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes