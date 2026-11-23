"""Negative controls for failures only visible after Jekyll renders a site."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validate_package", ROOT / "scripts/validate_package.py")
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class RenderedSiteChecks(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.url = package.SITE_URL
        self.page = f'''<!doctype html><html lang="en"><head>
<link rel="canonical" href="{self.url}">
<link rel="alternate" hreflang="en" href="{self.url}">
<meta name="description" content="A useful mission handoff.">
<meta property="og:title" content="Autopilot">
<meta property="og:description" content="A useful mission handoff.">
<meta property="og:url" content="{self.url}">
<meta property="og:image" content="{self.url}share.png">
<meta name="twitter:card" content="summary_large_image">
</head><body></body></html>'''
        (self.root / "index.html").write_text(self.page)
        (self.root / "share.png").write_bytes(b"image fixture")
        (self.root / "sitemap.xml").write_text(f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{self.url}</loc></url></urlset>')

    def test_rendered_fixture_passes(self):
        self.assertEqual(package.validate_site(self.root), 1)

    def test_missing_canonical_is_rejected(self):
        (self.root / "index.html").write_text(self.page.replace(f'<link rel="canonical" href="{self.url}">', ''))
        with self.assertRaisesRegex(AssertionError, "Canonical"):
            package.validate_site(self.root)

    def test_unrendered_template_is_rejected(self):
        (self.root / "index.html").write_text(self.page + "{{ page.url }}")
        with self.assertRaisesRegex(AssertionError, "Unrendered Liquid"):
            package.validate_site(self.root)

    def test_missing_sitemap_page_is_rejected(self):
        (self.root / "sitemap.xml").write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"/>')
        with self.assertRaisesRegex(AssertionError, "missing from sitemap"):
            package.validate_site(self.root)

    def test_wrong_language_and_broken_link_are_rejected(self):
        for addition, error in [(f'<link rel="alternate" hreflang="ko" href="{self.url}">', "Wrong language"),
                                ('<a href="missing.html">Missing</a>', "Broken rendered link")]:
            with self.subTest(error=error):
                (self.root / "index.html").write_text(self.page + addition)
                with self.assertRaisesRegex(AssertionError, error):
                    package.validate_site(self.root)
