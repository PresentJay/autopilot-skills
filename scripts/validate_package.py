"""Validate packaged links, metadata, templates, and the shipped state checker."""
import importlib.util
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://presentjay.github.io/autopilot-skills/"


class SitePage(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.meta, self.canonicals, self.alternates, self.targets = {}, [], {}, []
        self.language = None
        self.structured = []
        self.json_script = None
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "html":
            self.language = attrs.get("lang")
        if tag == "meta":
            self.meta[attrs.get("name") or attrs.get("property")] = attrs.get("content", "")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs.get("href"))
        if tag == "link" and attrs.get("rel") == "alternate" and "hreflang" in attrs:
            self.alternates[attrs["hreflang"]] = attrs.get("href")
        if tag in ("a", "link", "script", "img"):
            target = attrs.get("href") or attrs.get("src")
            if target:
                self.targets.append(target)
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.json_script = ""

    def handle_data(self, data):
        if self.json_script is not None:
            self.json_script += data

    def handle_endtag(self, tag):
        if tag == "script" and self.json_script is not None:
            self.structured.append(json.loads(self.json_script))
            self.json_script = None


def validate_site(directory):
    """Inspect rendered output: source-link checks cannot catch Liquid mistakes."""
    pages = {}
    for path in directory.rglob("*.html"):
        route = path.relative_to(directory).as_posix()
        url = SITE_URL + (route[:-10] if route.endswith("index.html") else route)
        text = path.read_text()
        assert "{{" not in text and "{%" not in text, f"Unrendered Liquid: {path}"
        page = SitePage(text)
        assert page.canonicals == [url], f"Canonical mismatch: {path}"
        assert page.language, f"Missing page language: {path}"
        for key in ("description", "og:title", "og:description", "og:url", "og:image", "twitter:card"):
            assert page.meta.get(key), f"Missing {key}: {path}"
        assert page.meta["og:url"] == url, f"Share URL mismatch: {path}"
        image = page.meta["og:image"]
        assert image.startswith(SITE_URL), f"Unexpected share image: {path}"
        page.targets.append(image)
        pages[url] = page
    assert pages, "No rendered HTML pages"
    for url, page in pages.items():
        assert page.alternates.get(page.language) == url, f"Missing self language alternative: {url}"
        for lang, target in page.alternates.items():
            assert target in pages, f"Missing language target: {target}"
            if lang != "x-default":
                assert pages[target].language == lang, f"Wrong language target: {target}"
                assert pages[target].alternates.get(page.language) == url, f"Nonreciprocal language link: {url}"
        for target in page.targets:
            resolved = urljoin(url, target)
            parsed = urlsplit(resolved)
            if parsed.netloc != urlsplit(SITE_URL).netloc or parsed.scheme not in ("http", "https"):
                continue
            assert resolved.split("#")[0].split("?")[0].startswith(SITE_URL), f"Link outside project site: {resolved}"
            relative = unquote(parsed.path[len(urlsplit(SITE_URL).path):])
            linked = directory / relative
            if not relative or parsed.path.endswith("/"):
                linked = linked / "index.html"
            assert linked.is_file(), f"Broken rendered link: {url}: {target}"
    tree = ET.parse(directory / "sitemap.xml")
    locations = {element.text for element in tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
    assert set(pages) <= locations, f"Pages missing from sitemap: {set(pages) - locations}"
    assert all(url.startswith(SITE_URL) for url in locations), "Sitemap points outside project site"
    assert len({page.meta["description"] for page in pages.values()}) == len(pages), "Duplicate page descriptions"
    return len(pages)


def validate(root=ROOT):
    skill = root / "skills/autopilot"
    text = (skill / "SKILL.md").read_text()
    frontmatter = text.split("---", 2)[1]
    assert re.search(r'^name: autopilot$', frontmatter, re.M), "Missing skill name"
    desc = re.search(r'^description: (.+)$', frontmatter, re.M)
    assert desc and len(desc[1]) < 500, "Description must be concise"
    version = re.search(r'^  version: "(\d+\.\d+\.\d+)"$', frontmatter, re.M)
    assert version, "Version belongs in metadata.version"
    assert json.loads((root / "package.json").read_text())["version"] == version[1], "Version mismatch"
    for file in skill.rglob("*.md"):
        for target in re.findall(r'\]\(([^)]+)\)', file.read_text()):
            if target.startswith(("https://", "http://", "#")):
                continue
            linked = (file.parent / target.split("#")[0]).resolve()
            assert skill.resolve() in linked.parents and linked.is_file(), f"Missing/outside resource: {file}: {target}"
    spec = importlib.util.spec_from_file_location("check_state", skill / "scripts/check_state.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    template = json.loads((skill / "templates/state.json").read_text())
    module.validate(template)
    metadata = (skill / "agents/openai.yaml").read_text()
    assert "$autopilot" in metadata, "Missing explicit invocation example"
    assert 'allow_implicit_invocation: false' not in metadata, "Do not change invocation policy without user request"
    docs = root / "docs"
    for file in docs.rglob("*.html"):
        for target in re.findall(r'href="([^"]+)"', file.read_text()):
            if target.startswith(("https://", "http://", "#")) or "{{" in target:
                continue
            if target.startswith("/autopilot-skills/"):
                linked = docs / target[len("/autopilot-skills/"):]
            else:
                linked = file.parent / target
            if target.endswith("/"):
                linked = linked / "index.html"
            assert linked.is_file() or (linked.suffix == ".html" and linked.with_suffix(".md").is_file()), f"Broken docs link: {file}: {target}"
    return version[1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, help="Jekyll output to check in addition to the package")
    args = parser.parse_args()
    print(f"PACKAGE VERIFIED: {validate()}")
    if args.site_dir:
        print(f"SITE VERIFIED: {validate_site(args.site_dir)} pages")
