import os
from html import escape
from datetime import date, datetime

BASE_URL = "https://hogga.cl"
TODAY = date.today().isoformat()

INCLUDE_DIRS = [
    "blog",
    "hogga-destinos",
    "hogga-conecta",
    "proveedores",
    "buscar",
    "contacto",
    "terminos-y-condiciones",
    "politica-privacidad",
]

RULES = {
    "blog": {"priority": "0.7", "changefreq": "weekly"},
    "hogga-destinos": {"priority": "0.8", "changefreq": "weekly"},
    "hogga-conecta": {"priority": "0.9", "changefreq": "monthly"},
    "proveedores": {"priority": "0.6", "changefreq": "monthly"},
    "buscar": {"priority": "0.7", "changefreq": "weekly"},
    "contacto": {"priority": "0.4", "changefreq": "yearly"},
    "terminos-y-condiciones": {"priority": "0.2", "changefreq": "yearly"},
    "politica-privacidad": {"priority": "0.2", "changefreq": "yearly"},
}

EXCLUDE_FILES = {
    # "draft.html",
}

EXCLUDE_DIRS = {
    "go",
    "partials",
    "drafts",
    "test",
    "tests",
    "__pycache__",
}

def url_path_from_fs(fs_path: str) -> str:
    """
    Convert filesystem path like 'blog/post/index.html' to URL path '/blog/post/'
    """
    p = fs_path.replace("\\", "/")

    if p.startswith("./"):
        p = p[1:]

    if not p.startswith("/"):
        p = "/" + p

    if p.endswith("/index.html"):
        p = p[:-10]

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

def is_noindex(fs_path: str) -> bool:
    """
    Return True if the HTML file contains a robots noindex directive.
    """
    try:
        with open(fs_path, "r", encoding="utf-8") as f:
            content = f.read().lower()
        return 'name="robots"' in content and "noindex" in content
    except Exception:
        return False

def is_sitemap_excluded(fs_path: str) -> bool:
    """
    Return True if the file contains a manual sitemap exclusion marker.
    Example: <!-- sitemap:exclude -->
    """
    try:
        with open(fs_path, "r", encoding="utf-8") as f:
            content = f.read().lower()
        return "<!-- sitemap:exclude -->" in content
    except Exception:
        return False

urls_xml = []

def add_url(url_path: str, priority: str, changefreq: str, lastmod: str):
    loc = escape(f"{BASE_URL}{url_path}")
    urls_xml.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>""")
    print(f"Included: {loc}")

home_lastmod = lastmod_from_fs("index.html") if os.path.exists("index.html") else TODAY
add_url("/", priority="1.0", changefreq="weekly", lastmod=home_lastmod)

seen = {"/"}

for directory in INCLUDE_DIRS:
    if not os.path.isdir(directory):
        continue

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            if not file.endswith(".html"):
                continue
            if file in EXCLUDE_FILES:
                continue

            fs_path = os.path.join(root, file)

            if is_noindex(fs_path):
                continue

            if is_sitemap_excluded(fs_path):
                continue

            url_path = url_path_from_fs(fs_path)

            if url_path in seen:
                continue
            seen.add(url_path)

            section = section_for_url_path(url_path)
            rule = rule_for_section(section)

            priority = rule["priority"]

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