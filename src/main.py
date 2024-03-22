import os, shutil

from blocks import markdown_to_html_node

def copy_dir(source, target):
    if os.path.exists(target):
        shutil.rmtree(target)
    os.mkdir(target)
    for path in os.listdir(source):
        if os.path.isdir(os.path.join(source, path)):
            copy_dir(os.path.join(source, path), os.path.join(target, path))
        if os.path.isfile(os.path.join(source, path)):
            shutil.copy(os.path.join(source, path), os.path.join(target, path))


def extract_title(markdown):
    first_line = markdown.strip().split("\n")[0]
    if not markdown.startswith("# "):
        raise ValueError("Markdown must start with an h1 header")
    return first_line[2:]


def generate_page(from_path, template_path, dest_path): 
    assert os.path.exists(from_path), f"No file found at {from_path}"
    markdown = open(from_path, 'r').read()

    assert os.path.exists(template_path), f"No template file found at {template_path}"
    template = open(template_path, 'r').read()

    root_node = markdown_to_html_node(markdown)
    html = root_node.to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, 'w') as outf:
        outf.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for path in os.listdir(dir_path_content):
        next_path = os.path.join(dir_path_content, path)
        if os.path.isdir(next_path):
            generate_pages_recursive(next_path, template_path, os.path.join(dest_dir_path, path))
        if os.path.isfile(next_path) and next_path.endswith(".md"):
            generate_page(next_path, template_path, os.path.splitext(os.path.join(dest_dir_path, path))[0]+".html")


def main():
    copy_dir("./static/", "./public")
    generate_pages_recursive("./content/", "./template.html", "./public/")

if __name__ == "__main__":
    main()
