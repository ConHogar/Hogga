import os

ROOT_DIR = "."
REQUIRED_LINKS = [
    "/hogga-servicios/",
    "/turismo/",
    "/negocios/",
    "/decisiones/",
    "/blog/",
    "/contacto/"
]

def check_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None
    
    if '<header class="main-header">' not in content:
        return None
    
    missing = []
    for link in REQUIRED_LINKS:
        if f'href="{link}"' not in content:
            missing.append(link)
    
    has_brand_text = '<span class="brand-text">Hogga</span>' in content
    has_webp_logo = 'logo.webp' in content
    
    return {
        "missing_links": missing,
        "missing_brand_text": not has_brand_text,
        "missing_logo": not has_webp_logo
    }

def main():
    count = 0
    issues = {}
    for root, dirs, files in os.walk(ROOT_DIR):
        if "go" in dirs:
            dirs.remove("go")
        if ".git" in dirs:
            dirs.remove(".git")
        
        for name in files:
            if name.endswith(".html"):
                path = os.path.join(root, name)
                res = check_file(path)
                if res:
                    count += 1
                    if res["missing_links"] or res["missing_brand_text"] or res["missing_logo"]:
                        issues[path] = res
    
    print(f"Checked {count} files with headers.")
    if not issues:
        print("All headers are uniform and correct!")
    else:
        for path, issue in issues.items():
            print(f"Issue in {path}:")
            if issue["missing_links"]:
                print(f"  Missing links: {issue['missing_links']}")
            if issue["missing_brand_text"]:
                print(f"  Missing brand-text span")
            if issue["missing_logo"]:
                print(f"  Missing logo.webp")

if __name__ == "__main__":
    main()
