import os
from block_markdown import markdown_to_html_node

def generate_pages_recursive_old(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        # Construct the full path of the entry
        entry_path = os.path.join(dir_path_content, entry)

        # If the entry is a file, generate page if it's a markdown file
        if os.path.isfile(entry_path) and entry.endswith(".md"):
            # Generate the destination file path
            dest_file_path = os.path.join(dest_dir_path, entry[:-3] + ".html")
            # Generate the page using the template
            generate_page(entry_path, template_path, dest_file_path)

        # If the entry is a directory, recursively generate pages
        elif os.path.isdir(entry_path):
            # Generate pages recursively for the subdirectory
            generate_pages_recursive_old(entry_path, template_path, dest_dir_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        # Construct the full path of the entry
        entry_path = os.path.join(dir_path_content, entry)

        # If the entry is a file, generate page if it's a markdown file
        if os.path.isfile(entry_path) and entry.endswith(".md"):
            # Generate the destination file path
            dest_file_path = os.path.join(dest_dir_path, entry[:-3] + ".html")
            # Generate the page using the template
            generate_page(entry_path, template_path, dest_file_path)

        # If the entry is a directory, recursively generate pages
        elif os.path.isdir(entry_path):
            # Generate pages recursively for the subdirectory
            sub_dest_dir_path = os.path.join(dest_dir_path, entry)  # Update destination directory for subfolder
            generate_pages_recursive(entry_path, template_path, sub_dest_dir_path)  # Pass subfolder's destination directory path

def generate_page(from_path, template_path, dest_path):
    # Print the source, template, and destination paths
    print(f" * {from_path} {template_path} -> {dest_path}")
    
    # Open and read the markdown file
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    # Open and read the template file
    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    # Convert markdown to HTML
    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    # Extract title from markdown
    title = extract_title(markdown_content)
    
    # Replace placeholders in the template with title and HTML content
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    # Create destination directory if it doesn't exist
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    
    # Write the modified template to the destination file
    to_file = open(dest_path, "w")
    to_file.write(template)
    to_file.close()

def extract_title(md):
    # Split markdown content into lines
    lines = md.split("\n")
    # Iterate over each line
    for line in lines:
        # Check if line starts with "# " indicating an h1 header
        if line.startswith("# "):
            # Return the title text (excluding "# ")
            return line[2:]
    # If no h1 header is found, raise an exception
    raise ValueError("No title found")
