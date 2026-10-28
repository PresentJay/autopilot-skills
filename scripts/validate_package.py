"""Validate packaged links, metadata, templates, and the shipped state checker."""
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


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
    print(f"PACKAGE VERIFIED: {validate()}")
