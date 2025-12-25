"""
Generates sitemap.xml for hogga.cl
Run manually after adding or removing pages.

Improvements:
- Uses real lastmod per file (filesystem mtime) instead of "today" for everything.
- Distinguishes /blog/ (index) priority vs individual blog posts.
"""

import os
from datetime import date, datetime

BASE_URL = "https://hogga.cl"
TODAY = date.today().isoformat()

# Only scan these folders if they exist
INCLUDE_DIRS = [
    "blog",
    "negocios",
    "turismo",
    "hogga-servicios",
    "proveedores",
    "decisiones",  # <-- agrega esto
    "contacto",
    "terminos-y-condiciones",
    "politica-privacidad",
    "bases-legales-concursos-instagram",
]

# Rules by top-level section
RULES = {
    "blog": {"priority": "0.7", "changefreq": "weekly"},
    "negocios": {"priority": "0.8", "changefreq": "weekly"},
    "turismo": {"priority": "0.8", "changefreq": "weekly"},
    "hogga-servicios": {"priority": "0.9", "changefreq": "weekly"},
    "proveedores": {"priority": "0.6", "changefreq": "monthly"},
    "decisiones": {"priority": "0.8", "changefreq": "weekly"},  # <-- opcional pero recomendado
    "contacto": {"priority": "0.4", "changefreq": "yearly"},
    "terminos-y-condiciones": {"priority": "0.2", "changefreq": "yearly"},
    "politica-privacidad": {"priority": "0.2", "changefreq": "yearly"},
    "bases-legales-concursos-instagram": {"priority": "0.2", "changefreq": "yearly"},
}

# Add any exact filenames you never want indexed (e.g., "draft.html")
EXCLUDE_FILES = {
    # "draft.html",
}

def url_path_from_fs(fs_path: str) -> str:
    """
    Convert filesystem path like 'blog/post/index.html' to URL path '/blog/post/'
    """
    p = fs_path.replace("\\", "/")

    # Normalize leading './'
    if p.startswith("./"):
        p = p[1:]  # remove the dot, keep leading slash

    # Ensure leading slash
    if not p.startswith("/"):
        p = "/" + p

    # index.html should map to directory URL
    if p.endswith("/index.html"):
        p = p[:-10]  # remove 'index.html'
    return p

def section_for_url_path(url_path: str) -> str:
    """
    Return top-level directory name, e.g. '/blog/x/' -> 'blog'
    """
    parts = url_path.strip("/").split("/")
    return parts[0] if parts and parts[0] else ""

def rule_for_section(section: str):
    return RULES.get(section, {"priority": "0.5", "changefreq": "weekly"})

def lastmod_from_fs(fs_path: str) -> str:
    """
    Use filesystem modification time as lastmod (YYYY-MM-DD).
    """
    ts = os.path.getmtime(fs_path)
    return datetime.fromtimestamp(ts).date().isoformat()

urls_xml = []

def add_url(url_path: str, priority: str, changefreq: str, lastmod: str):
    loc = f"{BASE_URL}{url_path}"
    urls_xml.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

# Home first (keep lastmod as today; you can also tie it to index.html if you want)
add_url("/", priority="1.0", changefreq="weekly", lastmod=TODAY)

seen = set(["/"])

for directory in INCLUDE_DIRS:
    if not os.path.isdir(directory):
        continue

    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith(".html"):
                continue
            if file in EXCLUDE_FILES:
                continue

            fs_path = os.path.join(root, file)
            url_path = url_path_from_fs(fs_path)

            # Avoid duplicates (just in case)
            if url_path in seen:
                continue
            seen.add(url_path)

            section = section_for_url_path(url_path)
            rule = rule_for_section(section)

            # Default rule priority
            priority = rule["priority"]

            # Optional fine-tune: blog index vs blog posts
            # Keep /blog/ at 0.7, set posts to 0.6
            if section == "blog" and url_path != "/blog/":
                priority = "0.6"

            lastmod = lastmod_from_fs(fs_path)

            add_url(
                url_path,
                priority=priority,
                changefreq=rule["changefreq"],
                lastmod=lastmod
            )

sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls_xml)}
</urlset>
"""

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap)

print("✅ sitemap.xml generado correctamente")
