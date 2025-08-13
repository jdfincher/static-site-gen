#!/usr/bin/env python
from copy_static import * 
import os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(script_dir, '..' ,'static')
    public_dir = os.path.join(script_dir, '..', 'public')
    dir_path_content = os.path.join(script_dir, '..', 'content')
    template_path = os.path.join(script_dir, '..', 'template.html')
    dest_dir_path = os.path.join(script_dir, '..', 'public')

    clear_and_copy(static_dir, public_dir, True)
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path)

    
    

main()

