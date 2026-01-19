import os
import re

ROOT_DIR = "/Users/NickA/Hogga"

def update_header(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    # Skip if already updated
    if '<span class="brand-text">Hogga</span>' in content:
        print(f"Skipping (already present): {file_path}")
        return

    # Skip files that don't have the header
    if '<header class="main-header">' not in content:
        return

    # Regex to find the brand link content
    # It looks for <a class="brand" ...> ... </a>
    # We want to insert the span before the closing </a>
    
    pattern = re.compile(r'(<a class="brand"[^>]*>[\s\S]*?)(\s*</a>)', re.MULTILINE)
    
    def replacer(match):
        inner_content = match.group(1)
        closing_tag = match.group(2)
        
        # Double check we don't duplicate if regex matches weirdly (though the first check handles most)
        if 'brand-text' in inner_content:
            return match.group(0)
            
        return f'{inner_content}\n        <span class="brand-text">Hogga</span>{closing_tag}'

    new_content, count = pattern.subn(replacer, content)

    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {file_path}")
    else:
        print(f"No match found in: {file_path}")

def main():
    for root, dirs, files in os.walk(ROOT_DIR):
        # exclusions
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        if '.git' in dirs:
            dirs.remove('.git')
            
        for name in files:
            if name.endswith(".html"):
                update_header(os.path.join(root, name))

if __name__ == "__main__":
    main()
