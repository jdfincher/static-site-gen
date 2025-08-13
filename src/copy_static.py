import os
import shutil
from block import *
from htmlnode import *

def clear_and_copy(src,dest,delete=True):
    
    if delete:
        if os.path.exists(dest):
            delete = False
            shutil.rmtree(dest)
            os.mkdir(dest)
        else:
            os.mkdir(dest)
    if not os.path.exists(dest):
        os.mkdir(dest)
    src_list = os.listdir(src)
    for item in src_list:
        path = os.path.join(src,item)
        if os.path.isfile(path):
            shutil.copy(path,dest)
        if os.path.isdir(path):
            new_dest = os.path.join(dest,item)
            new_src = os.path.join(src,item)
            clear_and_copy(new_src , new_dest, False)

def extract_title(markdown):
    with open(markdown, 'r') as f:
        md = f.read()
    list_md = md.split('\n\n')
    if not list_md[0].startswith("#"):
        raise Exception("h1 header not found at start of document")
    title = list_md[0].strip('#').strip()
    return title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        md = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    node = markdown_to_html_node(md)
    content = node.to_html()
    title = extract_title(from_path)
    temp_with_title = template.replace('{{ Title }}', title)
    final_page = temp_with_title.replace('{{ Content }}', content)
    directory = os.path.dirname(dest_path)
    if os.path.exists(directory):
        with open(dest_path, 'w') as f:
            f.write(final_page)
    else:
        path_to_make = os.path.normpath(dest_path)
        dir_to_make = os.path.dirname(path_to_make)
        os.makedirs(dir_to_make)
        with open(dest_path, 'w') as f:
            f.write(final_page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_list = []
    if not os.path.isfile(dir_path_content):
        content_list = os.listdir(dir_path_content)
    else:
        generate_page(dir_path_content, template_path, dest_dir_path)
    if content_list:
        for item in content_list:
            file_path = os.path.join(dir_path_content, item)
            if os.path.isfile(file_path) and file_path.endswith('md'):
                dest_path = os.path.join(dest_dir_path, item)
                dest_path, ext = os.path.splitext(dest_path)
                dest_path += '.html'
                from_path = os.path.join(dir_path_content, item)
                print(f"Destination:{dest_path}\nSource:{from_path}")
                generate_page(from_path, template_path, dest_path)
            elif os.path.isdir(file_path):
                dest_path = os.path.join(dest_dir_path, item)
                from_path = os.path.join(dir_path_content, item)
                generate_pages_recursive(from_path, template_path, dest_path)
            else:
                continue

            

        
