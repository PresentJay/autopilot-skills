import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validate_package", ROOT / "scripts/validate_package.py")
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class PackageChecks(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        shutil.copytree(ROOT / "skills", self.root / "skills", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy2(ROOT / "package.json", self.root / "package.json")
        shutil.copytree(ROOT / "docs", self.root / "docs")

    def test_package_and_documentation_links_resolve(self):
        self.assertEqual(package.validate(self.root), json.loads((self.root / "package.json").read_text())["version"])

    def test_broken_and_outside_skill_reference_rejected(self):
        entry = self.root / "skills/autopilot/SKILL.md"
        baseline = entry.read_text()
        for target in ("references/missing.md", "../../../outside.md"):
            with self.subTest(target=target):
                entry.write_text(baseline + f"\n[Resource]({target})\n")
                with self.assertRaisesRegex(AssertionError, "resource"):
                    package.validate(self.root)

    def test_version_mismatch_rejected(self):
        path = self.root / "package.json"
        data = json.loads(path.read_text())
        data["version"] = "0.0.0"
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(AssertionError, "Version mismatch"):
            package.validate(self.root)

    def test_broken_documentation_link_rejected(self):
        path = self.root / "docs/ko/index.html"
        path.write_text(path.read_text() + '<a href="missing.html">broken</a>')
        with self.assertRaisesRegex(AssertionError, "Broken docs link"):
            package.validate(self.root)
